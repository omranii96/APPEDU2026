<?php
/**
 * Règles commerciales côté serveur.
 *
 *  1. Remise « 2e parure −15 % » sur la parure la moins chère (frais négatif via woocommerce_cart_calculate_fees).
 *  2. Livraison offerte : seuil lu dans la méthode « Livraison gratuite », recalculé après la remise,
 *     forfait masqué quand la livraison est offerte (un seul service Branvas, pas d'express).
 *  3. Téléphone obligatoire au paiement (Branvas : requis hors États-Unis / Royaume-Uni).
 *  4. Quantités de stock jamais affichées (stock fictif synchronisé par Branvas).
 *  5. Délais réels (Branvas, jours ouvrés, 90 % des colis) et calendrier de Noël.
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

use Automattic\WooCommerce\Utilities\NumberUtil;

/* =========================================================================
 * 1. Remise « 2e parure »
 * ========================================================================= */

/**
 * Libellé de la remise (traduit si l'option est vide).
 */
function charmed_bundle_label(): string {
	$label = trim( (string) get_option( 'charmed_bundle_label', '' ) );
	if ( '' === $label ) {
		/* translators: %s: percentage, e.g. 15 */
		$label = sprintf( __( '2e parure −%s %%', 'charmed-paris' ), charmed_bundle_percent() );
	}
	return (string) apply_filters( 'charmed_bundle_label', $label );
}

/**
 * Pourcentage de remise (1–90).
 */
function charmed_bundle_percent(): int {
	return max( 1, min( 90, (int) charmed_opt( 'bundle_percent' ) ) );
}

/**
 * Le produit est-il éligible à la remise ?
 *
 * @param WC_Product $product Produit ou variation.
 */
function charmed_bundle_is_eligible( WC_Product $product ): bool {
	$slugs = array_filter( (array) charmed_opt( 'bundle_categories' ) );
	$pid   = $product->get_parent_id() ? $product->get_parent_id() : $product->get_id();
	$ok    = true;
	if ( $slugs ) {
		$ok = has_term( $slugs, 'product_cat', $pid );
	}
	if ( $ok && charmed_opt_yes( 'bundle_exclude_sale' ) && $product->is_on_sale() ) {
		$ok = false;
	}
	return (bool) apply_filters( 'charmed_bundle_is_eligible', $ok, $product );
}

/**
 * Calcule la remise pour un panier.
 *
 * Chaque unité éligible est listée avec son prix unitaire HT et sa TVA (lus sur les lignes du
 * panier, déjà calculées par WooCommerce), triée du moins cher au plus cher ; la remise porte sur
 * la moins chère (mode « once ») ou sur une unité par paire (mode « pairs »).
 *
 * @param WC_Cart $cart Panier.
 * @return array{ex: float, tax: float, units: int}
 */
function charmed_bundle_compute( WC_Cart $cart ): array {
	$zero = array(
		'ex'    => 0.0,
		'tax'   => 0.0,
		'units' => 0,
	);
	if ( ! charmed_opt_yes( 'bundle_enabled' ) ) {
		return $zero;
	}
	if ( ! charmed_opt_yes( 'bundle_with_coupons' ) && $cart->get_applied_coupons() ) {
		return $zero;
	}

	$units = array();
	foreach ( $cart->get_cart() as $item ) {
		$product = $item['data'] ?? null;
		$qty     = (int) ( $item['quantity'] ?? 0 );
		if ( ! $product instanceof WC_Product || $qty < 1 || ! charmed_bundle_is_eligible( $product ) ) {
			continue;
		}
		if ( isset( $item['line_subtotal'] ) && ( (float) $item['line_subtotal'] > 0 || 0.0 === (float) $product->get_price() ) ) {
			$ex  = (float) $item['line_subtotal'] / $qty;
			$tax = (float) ( $item['line_subtotal_tax'] ?? 0 ) / $qty;
		} else {
			$ex  = (float) wc_get_price_excluding_tax( $product );
			$tax = (float) wc_get_price_including_tax( $product ) - $ex;
		}
		for ( $i = 0; $i < $qty; $i++ ) {
			$units[] = array( $ex, $tax );
		}
	}

	$count = count( $units );
	if ( $count < 2 ) {
		return $zero;
	}
	usort(
		$units,
		static function ( $a, $b ) {
			return ( $a[0] + $a[1] ) <=> ( $b[0] + $b[1] );
		}
	);

	$n   = 'pairs' === charmed_opt( 'bundle_mode' ) ? intdiv( $count, 2 ) : 1;
	$pct = charmed_bundle_percent() / 100;
	$ex  = 0.0;
	$tax = 0.0;
	for ( $i = 0; $i < $n; $i++ ) {
		$ex  += $units[ $i ][0] * $pct;
		$tax += $units[ $i ][1] * $pct;
	}

	return apply_filters(
		'charmed_bundle_compute',
		array(
			'ex'    => $ex,
			'tax'   => $tax,
			'units' => $n,
		),
		$cart
	);
}

/**
 * Ajoute la remise comme frais négatif.
 *
 * Le montant transmis est HT : pour un frais négatif, WooCommerce répartit lui-même la TVA au
 * prorata des classes de taxe du panier (WC_Cart_Totals::get_fees_from_cart), ce qui fait
 * apparaître la remise TTC exacte (15 % du prix TTC) quand les prix sont saisis TTC à 20 %.
 * Sans TVA activée, line_subtotal = prix affiché, le calcul reste juste.
 */
add_action(
	'woocommerce_cart_calculate_fees',
	static function ( WC_Cart $cart ) {
		if ( is_admin() && ! wp_doing_ajax() ) {
			return;
		}
		$b = charmed_bundle_compute( $cart );
		if ( $b['ex'] <= 0 ) {
			return;
		}
		$amount = wc_tax_enabled() ? $b['ex'] : $b['ex'] + $b['tax'];
		$cart->add_fee( charmed_bundle_label(), -1 * NumberUtil::round( $amount, wc_get_rounding_precision() ), true, '' );
	}
);

/* =========================================================================
 * 2. Livraison offerte (méthode conditionnelle)
 * ========================================================================= */

/**
 * Seuil de livraison offerte (TTC) : option, sinon montant minimum de la 1re méthode
 * « Livraison gratuite » active trouvée dans les zones d'expédition.
 */
function charmed_free_shipping_threshold(): float {
	$opt = trim( (string) get_option( 'charmed_free_shipping_threshold', '' ) );
	if ( '' !== $opt && is_numeric( str_replace( ',', '.', $opt ) ) ) {
		return (float) str_replace( ',', '.', $opt );
	}
	$cached = get_transient( 'charmed_fs_threshold' );
	if ( false !== $cached ) {
		return (float) $cached;
	}
	$min = 0.0;
	if ( class_exists( 'WC_Shipping_Zones' ) ) {
		$zones   = WC_Shipping_Zones::get_zones();
		$methods = array();
		foreach ( $zones as $zone ) {
			$methods = array_merge( $methods, (array) ( $zone['shipping_methods'] ?? array() ) );
		}
		foreach ( $methods as $method ) {
			if ( 'free_shipping' === $method->id && 'yes' === $method->enabled && in_array( $method->requires, array( 'min_amount', 'either' ), true ) && (float) $method->min_amount > 0 ) {
				$min = $min > 0 ? min( $min, (float) $method->min_amount ) : (float) $method->min_amount;
			}
		}
	}
	set_transient( 'charmed_fs_threshold', $min, HOUR_IN_SECONDS );
	return $min;
}
add_action( 'woocommerce_update_options_shipping', static function () { delete_transient( 'charmed_fs_threshold' ); } );
add_action( 'woocommerce_shipping_zone_method_added', static function () { delete_transient( 'charmed_fs_threshold' ); } );
add_action( 'woocommerce_shipping_zone_method_deleted', static function () { delete_transient( 'charmed_fs_threshold' ); } );
add_action( 'woocommerce_shipping_zone_method_status_toggled', static function () { delete_transient( 'charmed_fs_threshold' ); } );

/**
 * Le seuil de la méthode « Livraison gratuite » est recalculé APRÈS la remise 2e parure
 * (WooCommerce ne tient pas compte des frais). Ne peut que retirer la gratuité, jamais l'accorder.
 */
add_filter(
	'woocommerce_shipping_free_shipping_is_available',
	static function ( $available, $package, $method ) {
		if ( ! $available || ! charmed_opt_yes( 'threshold_after_bundle' ) || 'min_amount' !== $method->requires ) {
			return $available;
		}
		$cart = function_exists( 'WC' ) ? WC()->cart : null;
		if ( ! $cart ) {
			return $available;
		}
		$b = charmed_bundle_compute( $cart );
		if ( $b['ex'] <= 0 ) {
			return $available;
		}
		$incl  = $cart->display_prices_including_tax();
		$total = (float) $cart->get_displayed_subtotal();
		if ( 'yes' !== $method->ignore_discounts ) {
			$total -= (float) $cart->get_discount_total();
			if ( $incl ) {
				$total -= (float) $cart->get_discount_tax();
			}
		}
		$total -= $incl ? ( $b['ex'] + $b['tax'] ) : $b['ex'];
		return NumberUtil::round( $total, wc_get_price_decimals() ) >= (float) $method->min_amount;
	},
	10,
	3
);

/**
 * Quand la livraison est offerte, on ne propose qu'elle (plus le retrait éventuel).
 */
add_filter(
	'woocommerce_package_rates',
	static function ( $rates ) {
		if ( ! charmed_opt_yes( 'hide_paid_when_free' ) ) {
			return $rates;
		}
		$free = array();
		$keep = array();
		foreach ( $rates as $key => $rate ) {
			if ( 'free_shipping' === $rate->get_method_id() ) {
				$free[ $key ] = $rate;
			} elseif ( in_array( $rate->get_method_id(), array( 'local_pickup', 'pickup_location' ), true ) ) {
				$keep[ $key ] = $rate;
			}
		}
		return $free ? $free + $keep : $rates;
	},
	100
);

/* =========================================================================
 * 3. Téléphone obligatoire
 * ========================================================================= */

/**
 * Pays où le téléphone reste facultatif selon le mode.
 */
function charmed_phone_exempt_countries(): array {
	return 'except_us_gb' === charmed_opt( 'phone_required' ) ? (array) apply_filters( 'charmed_phone_exempt_countries', array( 'US', 'GB' ) ) : array();
}

// Mode « all » : force l'option WooCommerce (lue par le paiement classique ET le bloc Paiement).
add_filter(
	'pre_option_woocommerce_checkout_phone_field',
	static function ( $pre ) {
		return 'all' === charmed_opt( 'phone_required' ) ? 'required' : $pre;
	}
);

// Mode « except_us_gb » : requis via la locale pays (appliquée aussi par le bloc Paiement).
add_filter(
	'woocommerce_get_country_locale',
	static function ( $locale ) {
		if ( 'except_us_gb' !== charmed_opt( 'phone_required' ) || ! function_exists( 'WC' ) ) {
			return $locale;
		}
		$exempt = charmed_phone_exempt_countries();
		foreach ( array_keys( WC()->countries->get_shipping_countries() ) as $cc ) {
			$locale[ $cc ]['phone']['required'] = ! in_array( $cc, $exempt, true );
		}
		return $locale;
	}
);

/**
 * Validation serveur commune.
 *
 * @param string $country Pays de livraison.
 * @param string $phone   Téléphone (livraison, sinon facturation).
 */
function charmed_phone_missing( string $country, string $phone ): bool {
	if ( 'woo' === charmed_opt( 'phone_required' ) ) {
		return false;
	}
	if ( in_array( $country, charmed_phone_exempt_countries(), true ) ) {
		return false;
	}
	return '' === trim( $phone );
}

function charmed_phone_message(): string {
	return __( 'Ajoute un numéro de téléphone : le transporteur en a besoin pour livrer ta parure (douane, avis de passage).', 'charmed-paris' );
}

// Paiement classique.
add_action(
	'woocommerce_after_checkout_validation',
	static function ( $data, $errors ) {
		$country = ! empty( $data['ship_to_different_address'] ) ? ( $data['shipping_country'] ?? '' ) : ( $data['billing_country'] ?? '' );
		$phone   = ( $data['shipping_phone'] ?? '' ) ?: ( $data['billing_phone'] ?? '' );
		if ( charmed_phone_missing( (string) $country, (string) $phone ) ) {
			$errors->add( 'charmed_phone', charmed_phone_message() );
		}
	},
	10,
	2
);

// Bloc Paiement (Store API).
add_action(
	'woocommerce_store_api_checkout_update_order_from_request',
	static function ( $order ) {
		if ( ! $order instanceof WC_Order ) {
			return;
		}
		$country = $order->get_shipping_country() ?: $order->get_billing_country();
		$phone   = $order->get_shipping_phone() ?: $order->get_billing_phone();
		if ( charmed_phone_missing( (string) $country, (string) $phone ) && class_exists( '\Automattic\WooCommerce\StoreApi\Exceptions\RouteException' ) ) {
			throw new \Automattic\WooCommerce\StoreApi\Exceptions\RouteException( 'charmed_phone_required', esc_html( charmed_phone_message() ), 400 );
		}
	}
);

/**
 * Recopie le téléphone de facturation dans l'adresse de livraison si elle n'en a pas :
 * Branvas transmet l'adresse de livraison au transporteur.
 *
 * @param WC_Order $order Commande.
 */
function charmed_copy_phone_to_shipping( $order ): void {
	if ( $order instanceof WC_Order && '' === (string) $order->get_shipping_phone() && '' !== (string) $order->get_billing_phone() && $order->get_shipping_address_1() ) {
		$order->set_shipping_phone( $order->get_billing_phone() );
	}
}
add_action( 'woocommerce_checkout_create_order', 'charmed_copy_phone_to_shipping' );
add_action( 'woocommerce_store_api_checkout_update_order_from_request', 'charmed_copy_phone_to_shipping', 20 );

/* =========================================================================
 * 4. Stock : jamais de quantité affichée
 * ========================================================================= */
add_filter(
	'pre_option_woocommerce_stock_format',
	static function ( $pre ) {
		return charmed_opt_yes( 'hide_stock_qty' ) ? 'no_amount' : $pre;
	}
);

/* =========================================================================
 * 5. Délais et Noël
 * ========================================================================= */

/**
 * Délai total (commande → livraison, 90 % des colis, jours ouvrés) par pays. Source Branvas 22/11/2026.
 *
 * @param string $country Code pays ISO (vide = pays de la cliente, sinon pays de la boutique).
 */
function charmed_delivery_days( string $country = '' ): string {
	if ( '' === $country && function_exists( 'WC' ) && WC()->customer ) {
		$country = (string) WC()->customer->get_shipping_country();
	}
	if ( '' === $country && function_exists( 'WC' ) ) {
		$country = (string) WC()->countries->get_base_country();
	}
	$map = apply_filters(
		'charmed_delivery_days',
		array(
			'FR' => (string) charmed_opt( 'delivery_days_default' ),
			'DE' => '4–9',
			'ES' => '4–9',
			'NL' => '4–6',
			'IT' => '3–10',
			'IE' => '5–11',
			'GB' => '3–7',
			'US' => '3–8',
			'CA' => '4–8',
			'AU' => '3–8',
			'*'  => '4–12',
		)
	);
	return (string) ( $map[ strtoupper( $country ) ] ?? $map['*'] );
}

/**
 * Timestamp (fin de journée, fuseau du site) d'une date AAAA-MM-JJ.
 *
 * @param string $ymd Date.
 * @param bool   $end Fin de journée.
 */
function charmed_date_ts( string $ymd, bool $end = true ): int {
	$d = DateTimeImmutable::createFromFormat( '!Y-m-d', $ymd, wp_timezone() );
	if ( ! $d ) {
		return 0;
	}
	return $end ? $d->setTime( 23, 59, 59 )->getTimestamp() : $d->getTimestamp();
}

/**
 * État du calendrier de Noël.
 *
 * @return array{packaging: bool, before_deadline: bool, deadline: int, packaging_end: int}
 */
function charmed_xmas_state(): array {
	$now      = time();
	$start    = charmed_date_ts( (string) charmed_opt( 'xmas_packaging_start' ), false );
	$end      = charmed_date_ts( (string) charmed_opt( 'xmas_packaging_end' ) );
	$deadline = charmed_date_ts( (string) charmed_opt( 'xmas_deadline' ) );
	return array(
		'packaging'       => $start && $end && $now >= $start && $now <= $end,
		'before_deadline' => $deadline && $now <= $deadline,
		'deadline'        => $deadline,
		'packaging_end'   => $end,
	);
}

/**
 * Messages de réassurance (bandeau, fiche produit, panier, paiement).
 *
 * @param string[] $parts shipping | bundle | delivery | xmas | ddp.
 * @param string   $context bar | product | cart.
 * @return string[] Messages texte (non échappés).
 */
function charmed_promo_messages( array $parts, string $context = 'bar' ): array {
	$out = array();
	foreach ( $parts as $part ) {
		switch ( $part ) {
			case 'xmas':
				$x = charmed_xmas_state();
				if ( ! $x['packaging'] ) {
					break;
				}
				/* translators: date format for the Christmas deadline (PHP date()), e.g. "vendredi 4 décembre" */
				$fmt = _x( 'l j F', 'xmas date format', 'charmed-paris' );
				if ( $x['before_deadline'] ) {
					/* translators: %s: date, e.g. "vendredi 4 décembre" */
					$out[] = sprintf( __( 'Noël : commande avant le %s pour une livraison avant le 24 (Europe)', 'charmed-paris' ), wp_date( $fmt, $x['deadline'] ) );
				} else {
					/* translators: %s: date */
					$out[] = sprintf( __( 'Commandes après le %s : livraison avant Noël non garantie', 'charmed-paris' ), wp_date( $fmt, $x['deadline'] ) );
				}
				if ( 'bar' === $context ) {
					/* translators: %s: date, e.g. "24 décembre" */
					$out[] = sprintf( __( 'Emballage de Noël offert jusqu’au %s', 'charmed-paris' ), wp_date( _x( 'j F', 'short date format', 'charmed-paris' ), $x['packaging_end'] ) );
				}
				break;
			case 'shipping':
				$t = charmed_free_shipping_threshold();
				if ( $t > 0 ) {
					/* translators: %s: amount, e.g. "50 €" */
					$out[] = sprintf( __( 'Livraison offerte dès %s', 'charmed-paris' ), charmed_price_plain( $t ) );
				}
				break;
			case 'bundle':
				if ( charmed_opt_yes( 'bundle_enabled' ) ) {
					$out[] = charmed_bundle_label();
				}
				break;
			case 'delivery':
				$days  = 'product' === $context ? charmed_delivery_days( function_exists( 'WC' ) ? (string) WC()->countries->get_base_country() : 'FR' ) : charmed_delivery_days();
				/* translators: %s: business days range, e.g. "4–9" */
				$out[] = sprintf( __( 'Livraison en %s jours ouvrés, suivie', 'charmed-paris' ), $days );
				break;
			case 'ddp':
				$out[] = __( 'Droits et taxes inclus, rien à payer à la livraison', 'charmed-paris' );
				break;
		}
	}
	return array_values( array_filter( (array) apply_filters( 'charmed_promo_messages', $out, $parts, $context ) ) );
}

/**
 * Montant sans HTML (« 50 € »), sans décimales inutiles.
 *
 * @param float $amount Montant.
 */
function charmed_price_plain( float $amount ): string {
	$decimals = ( floor( $amount ) === $amount ) ? 0 : wc_get_price_decimals();
	return html_entity_decode(
		wp_strip_all_tags(
			wc_price(
				$amount,
				array(
					'decimals' => $decimals,
				)
			)
		),
		ENT_QUOTES,
		'UTF-8'
	);
}

/**
 * Rappel délai + Noël sous le bouton du paiement classique (le bloc Paiement utilise le template
 * page-checkout.html du thème).
 */
add_action(
	'woocommerce_review_order_before_payment',
	static function () {
		$msgs = charmed_promo_messages( array( 'delivery', 'ddp', 'xmas' ), 'cart' );
		if ( $msgs ) {
			echo '<p class="cp-checkout-note">' . esc_html( implode( ' · ', $msgs ) ) . '</p>';
		}
	}
);

/* =========================================================================
 * 6. Légal : bouton de commande, pas de prix barré
 * ========================================================================= */

/**
 * Libellé du bouton final (L221-14) : « Commander avec obligation de paiement ».
 */
function charmed_order_button_label(): string {
	$label = trim( (string) get_option( 'charmed_order_button_label', '' ) );
	return '' !== $label ? $label : __( 'Commander avec obligation de paiement', 'charmed-paris' );
}

// Paiement classique.
add_filter( 'woocommerce_order_button_text', static fn() => charmed_order_button_label(), 99 );

// Bloc Paiement : filtre officiel d'extensibilité « placeOrderButtonLabel » (wc.blocksCheckout).
add_action(
	'wp_enqueue_scripts',
	static function () {
		if ( ! function_exists( 'is_checkout' ) || ! is_checkout() || ! wp_script_is( 'wc-blocks-checkout', 'registered' ) ) {
			return;
		}
		wp_register_script( 'charmed-checkout-label', false, array( 'wc-blocks-checkout' ), CHARMED_VERSION, true );
		wp_enqueue_script( 'charmed-checkout-label' );
		wp_add_inline_script(
			'charmed-checkout-label',
			sprintf(
				'(function(l){var c=window.wc&&window.wc.blocksCheckout;if(c&&c.registerCheckoutFilters){c.registerCheckoutFilters("charmed-paris",{placeOrderButtonLabel:function(){return l;}});}})(%s);',
				wp_json_encode( charmed_order_button_label() )
			)
		);
	}
);

/**
 * Pas de prix barré par défaut : seul le prix réellement payé est affiché, sans badge « Promo ».
 * (Un prix de référence doit être le plus bas prix des 30 derniers jours, L112-1-1 ; ne jamais
 * utiliser le prix conseillé du fournisseur comme prix barré.)
 */
add_filter(
	'woocommerce_format_sale_price',
	static function ( $html, $regular, $sale ) {
		if ( charmed_opt_yes( 'show_strikethrough' ) ) {
			return $html;
		}
		return '<ins>' . ( is_numeric( $sale ) ? wc_price( $sale ) : $sale ) . '</ins>';
	},
	99,
	3
);
add_filter( 'woocommerce_sale_flash', static fn( $html ) => charmed_opt_yes( 'show_strikethrough' ) ? $html : '', 99 );
add_filter(
	'render_block_woocommerce/product-sale-badge',
	static fn( $html ) => charmed_opt_yes( 'show_strikethrough' ) ? $html : ''
);
