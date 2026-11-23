<?php
/**
 * Réglages du thème : WooCommerce > Réglages > Produits > CHARMED PARIS.
 *
 * Toutes les options sont préfixées « charmed_ ». Lecture : charmed_opt( 'bundle_percent' ).
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

/**
 * Valeurs par défaut (faits Branvas au 22/11/2026, voir woocommerce/source/FAITS-BRANVAS.md).
 */
function charmed_defaults(): array {
	return array(
		// Remise « 2e parure ».
		'bundle_enabled'          => 'yes',
		'bundle_percent'          => '15',
		'bundle_label'            => '',      // Vide = libellé traduit « 2e parure −15 % ».
		'bundle_mode'             => 'once',  // once = une seule parure remisée ; pairs = une par paire.
		'bundle_categories'       => array(), // Slugs product_cat éligibles ; vide = tous les produits.
		'bundle_exclude_sale'     => 'no',
		'bundle_with_coupons'     => 'no',    // Cumul avec un code promo.
		// Livraison (un seul service Branvas : pas d'express).
		'free_shipping_threshold' => '',      // Vide = lu dans la méthode « Livraison gratuite » de WooCommerce.
		'threshold_after_bundle'  => 'yes',   // Seuil calculé après la remise 2e parure.
		'hide_paid_when_free'     => 'yes',
		'delivery_days_default'   => '4–9',   // France, jours ouvrés, commande → livraison (90 % des colis).
		// Checkout.
		'phone_required'          => 'all',   // all | except_us_gb | woo.
		// Stock synchronisé par Branvas : ne jamais afficher la quantité (valeur fictive type 1000).
		'hide_stock_qty'          => 'yes',
		// Noël 2026 (Branvas).
		'xmas_packaging_start'    => '2026-11-20',
		'xmas_packaging_end'      => '2026-12-24',
		'xmas_deadline'           => '2026-12-04', // Europe et Canada.
		// Légal.
		'order_button_label'      => '',      // Vide = « Commander avec obligation de paiement » traduit (L221-14).
		'show_strikethrough'      => 'no',    // Prix barrés interdits au lancement (L112-1-1).
	);
}

/**
 * Lit une option du thème avec sa valeur par défaut.
 *
 * @param string $key Clé sans le préfixe.
 * @return mixed
 */
function charmed_opt( string $key ) {
	$defaults = charmed_defaults();
	$default  = $defaults[ $key ] ?? '';
	$value    = get_option( 'charmed_' . $key, $default );
	if ( '' === $value && '' !== $default && ! is_array( $default ) ) {
		$value = $default;
	}
	return apply_filters( 'charmed_option_' . $key, $value );
}

/**
 * Vrai si l'option vaut « yes ».
 *
 * @param string $key Clé.
 */
function charmed_opt_yes( string $key ): bool {
	return 'yes' === charmed_opt( $key );
}

/**
 * Section dans l'onglet Produits.
 */
add_filter(
	'woocommerce_get_sections_products',
	static function ( $sections ) {
		$sections['charmed'] = __( 'CHARMED PARIS', 'charmed-paris' );
		return $sections;
	}
);

add_filter(
	'woocommerce_get_settings_products',
	static function ( $settings, $current_section ) {
		if ( 'charmed' !== $current_section ) {
			return $settings;
		}

		$cats = array();
		$terms = get_terms(
			array(
				'taxonomy'   => 'product_cat',
				'hide_empty' => false,
			)
		);
		if ( ! is_wp_error( $terms ) ) {
			foreach ( $terms as $term ) {
				$cats[ $term->slug ] = $term->name;
			}
		}
		$d = charmed_defaults();

		return array(
			array(
				'title' => __( 'Remise « 2e parure »', 'charmed-paris' ),
				'type'  => 'title',
				'desc'  => __( 'Remise calculée côté serveur sur la parure la moins chère du panier (frais négatif, TVA ventilée par WooCommerce). Visible au panier, au paiement, dans la commande et les e-mails.', 'charmed-paris' ),
				'id'    => 'charmed_bundle',
			),
			array(
				'title'   => __( 'Activer', 'charmed-paris' ),
				'id'      => 'charmed_bundle_enabled',
				'type'    => 'checkbox',
				'default' => $d['bundle_enabled'],
			),
			array(
				'title'             => __( 'Pourcentage', 'charmed-paris' ),
				'id'                => 'charmed_bundle_percent',
				'type'              => 'number',
				'default'           => $d['bundle_percent'],
				'custom_attributes' => array(
					'min'  => 1,
					'max'  => 90,
					'step' => 1,
				),
			),
			array(
				'title'       => __( 'Libellé', 'charmed-paris' ),
				'id'          => 'charmed_bundle_label',
				'type'        => 'text',
				'default'     => '',
				'placeholder' => __( '2e parure −15 %', 'charmed-paris' ),
				'desc_tip'    => __( 'Laisser vide pour le libellé automatique traduit (FR/EN).', 'charmed-paris' ),
			),
			array(
				'title'   => __( 'Mode', 'charmed-paris' ),
				'id'      => 'charmed_bundle_mode',
				'type'    => 'select',
				'default' => $d['bundle_mode'],
				'options' => array(
					'once'  => __( 'Une seule parure remisée (la moins chère), dès 2 parures', 'charmed-paris' ),
					'pairs' => __( 'Une parure remisée par paire (les moins chères)', 'charmed-paris' ),
				),
			),
			array(
				'title'   => __( 'Catégories éligibles', 'charmed-paris' ),
				'id'      => 'charmed_bundle_categories',
				'type'    => 'multiselect',
				'class'   => 'wc-enhanced-select',
				'options' => $cats,
				'default' => array(),
				'desc'    => __( 'Vide = tous les produits.', 'charmed-paris' ),
			),
			array(
				'title'   => __( 'Exclure les produits en promotion', 'charmed-paris' ),
				'id'      => 'charmed_bundle_exclude_sale',
				'type'    => 'checkbox',
				'default' => $d['bundle_exclude_sale'],
			),
			array(
				'title'   => __( 'Cumulable avec un code promo', 'charmed-paris' ),
				'id'      => 'charmed_bundle_with_coupons',
				'type'    => 'checkbox',
				'default' => $d['bundle_with_coupons'],
				'desc'    => __( 'Décoché : la remise disparaît dès qu’un code promo est appliqué (protège la marge).', 'charmed-paris' ),
			),
			array(
				'type' => 'sectionend',
				'id'   => 'charmed_bundle',
			),

			array(
				'title' => __( 'Livraison', 'charmed-paris' ),
				'type'  => 'title',
				'desc'  => __( 'Branvas propose un seul service (pas d’express, pas de date garantie). Configurez dans WooCommerce > Réglages > Expédition une méthode « Forfait » et une méthode « Livraison gratuite » avec montant minimum : voir tech/installation.md.', 'charmed-paris' ),
				'id'    => 'charmed_shipping',
			),
			array(
				'title'       => __( 'Seuil de livraison offerte (affichage)', 'charmed-paris' ),
				'id'          => 'charmed_free_shipping_threshold',
				'type'        => 'text',
				'default'     => '',
				'placeholder' => __( 'auto', 'charmed-paris' ),
				'desc_tip'    => __( 'Vide = lu automatiquement dans la méthode « Livraison gratuite ». Sert aux textes (bandeau, réassurance). Le seuil réel reste celui de la méthode WooCommerce.', 'charmed-paris' ),
			),
			array(
				'title'   => __( 'Seuil calculé après la remise 2e parure', 'charmed-paris' ),
				'id'      => 'charmed_threshold_after_bundle',
				'type'    => 'checkbox',
				'default' => $d['threshold_after_bundle'],
			),
			array(
				'title'   => __( 'Masquer le forfait quand la livraison est offerte', 'charmed-paris' ),
				'id'      => 'charmed_hide_paid_when_free',
				'type'    => 'checkbox',
				'default' => $d['hide_paid_when_free'],
			),
			array(
				'title'    => __( 'Délai affiché par défaut (jours ouvrés)', 'charmed-paris' ),
				'id'       => 'charmed_delivery_days_default',
				'type'     => 'text',
				'default'  => $d['delivery_days_default'],
				'desc_tip' => __( 'France : 4–9 (source Branvas, 90 % des colis, de la commande à la livraison). Les autres pays utilisent la table du thème (filtre charmed_delivery_days).', 'charmed-paris' ),
			),
			array(
				'type' => 'sectionend',
				'id'   => 'charmed_shipping',
			),

			array(
				'title' => __( 'Paiement et stock', 'charmed-paris' ),
				'type'  => 'title',
				'id'    => 'charmed_checkout',
			),
			array(
				'title'   => __( 'Téléphone au paiement', 'charmed-paris' ),
				'id'      => 'charmed_phone_required',
				'type'    => 'select',
				'default' => $d['phone_required'],
				'options' => array(
					'all'          => __( 'Obligatoire pour toutes les destinations (recommandé)', 'charmed-paris' ),
					'except_us_gb' => __( 'Obligatoire sauf États-Unis et Royaume-Uni (règle minimale Branvas)', 'charmed-paris' ),
					'woo'          => __( 'Laisser le réglage WooCommerce', 'charmed-paris' ),
				),
				'desc'    => __( 'Branvas exige un téléphone pour livrer hors États-Unis et Royaume-Uni (douane, DHL).', 'charmed-paris' ),
			),
			array(
				'title'   => __( 'Ne jamais afficher la quantité en stock', 'charmed-paris' ),
				'id'      => 'charmed_hide_stock_qty',
				'type'    => 'checkbox',
				'default' => $d['hide_stock_qty'],
				'desc'    => __( 'Le stock est synchronisé par Branvas avec une valeur fictive : ne pas modifier les quantités à la main.', 'charmed-paris' ),
			),
			array(
				'title'       => __( 'Libellé du bouton de commande', 'charmed-paris' ),
				'id'          => 'charmed_order_button_label',
				'type'        => 'text',
				'default'     => '',
				'placeholder' => __( 'Commander avec obligation de paiement', 'charmed-paris' ),
				'desc_tip'    => __( 'Article L221-14 du Code de la consommation. Vide = libellé traduit automatiquement (FR/EN).', 'charmed-paris' ),
			),
			array(
				'title'   => __( 'Afficher les prix barrés', 'charmed-paris' ),
				'id'      => 'charmed_show_strikethrough',
				'type'    => 'checkbox',
				'default' => 'no',
				'desc'    => __( 'Décoché (recommandé au lancement) : seul le prix payé est affiché, pas de prix barré ni de badge « Promo ». Un prix barré doit être le plus bas prix pratiqué sur les 30 derniers jours (L112-1-1).', 'charmed-paris' ),
			),
			array(
				'type' => 'sectionend',
				'id'   => 'charmed_checkout',
			),

			array(
				'title' => __( 'Noël', 'charmed-paris' ),
				'type'  => 'title',
				'desc'  => __( 'Dates Branvas 2026. Format AAAA-MM-JJ, fuseau horaire du site (Europe/Paris).', 'charmed-paris' ),
				'id'    => 'charmed_xmas',
			),
			array(
				'title'   => __( 'Emballage de Noël offert : début', 'charmed-paris' ),
				'id'      => 'charmed_xmas_packaging_start',
				'type'    => 'text',
				'default' => $d['xmas_packaging_start'],
			),
			array(
				'title'   => __( 'Emballage de Noël offert : fin', 'charmed-paris' ),
				'id'      => 'charmed_xmas_packaging_end',
				'type'    => 'text',
				'default' => $d['xmas_packaging_end'],
			),
			array(
				'title'   => __( 'Date limite de commande pour Noël (Europe)', 'charmed-paris' ),
				'id'      => 'charmed_xmas_deadline',
				'type'    => 'text',
				'default' => $d['xmas_deadline'],
			),
			array(
				'type' => 'sectionend',
				'id'   => 'charmed_xmas',
			),
		);
	},
	10,
	2
);

/**
 * Vide les caches dépendant des réglages à l'enregistrement.
 */
add_action(
	'woocommerce_update_options_products_charmed',
	static function () {
		delete_transient( 'charmed_fs_threshold' );
	}
);
