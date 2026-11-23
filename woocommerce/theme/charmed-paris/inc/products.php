<?php
/**
 * Lecture des VRAIS produits WooCommerce pour les sections vitrines (coffrets, file des parures).
 *
 * Sélection par catégorie (slug), par IDs ou par SKU (les SKU Branvas « JS… »), triée côté serveur.
 * Les IDs sélectionnés sont mis en cache (transient versionné, invalidé à chaque modification
 * produit / synchro Branvas) ; prix, stock et libellés sont relus à chaque rendu.
 *
 * Champs produit ajoutés (onglet Général) — non écrasés par la synchro Branvas a priori
 * (À CONFIRMER en préproduction, voir tech/installation.md) :
 *  - _charmed_cutout_id : ID média de la parure détourée (PNG/WebP transparent, dossier charmed-paris/cut/)
 *  - _charmed_line      : ligne courte de l'étiquette (« Collier et boucles, métal doré »)
 *  - _charmed_code      : code 3 lettres de l'étiquette (« MOL »)
 *  - _charmed_pieces    : composition, une pièce par ligne (« Collier », « Boucles d'oreilles »)
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

/**
 * Version du cache vitrine (incrémentée à chaque changement produit).
 */
function charmed_showcase_cache_version(): int {
	return (int) get_option( 'charmed_showcase_ver', 1 );
}

/**
 * Invalide le cache vitrine.
 */
function charmed_showcase_flush(): void {
	update_option( 'charmed_showcase_ver', charmed_showcase_cache_version() + 1, false );
}
foreach ( array( 'woocommerce_update_product', 'woocommerce_new_product', 'woocommerce_delete_product', 'woocommerce_trash_product', 'woocommerce_product_set_stock_status', 'woocommerce_product_set_visibility', 'edited_product_cat' ) as $charmed_hook ) {
	add_action( $charmed_hook, 'charmed_showcase_flush' );
}
unset( $charmed_hook );

/**
 * Sélectionne des produits.
 *
 * @param array $args {
 *     @type string $category Slugs product_cat séparés par des virgules.
 *     @type string $ids      IDs séparés par des virgules (ordre conservé).
 *     @type string $skus     SKU séparés par des virgules (ordre conservé), ex. « JSGRQR,JS1AQ5 ».
 *     @type int    $limit    Nombre maximum (1–24).
 *     @type string $orderby  menu_order | date | price | popularity | rand.
 * }
 * @return WC_Product[]
 */
function charmed_get_showcase_products( array $args ): array {
	if ( ! charmed_has_wc() ) {
		return array();
	}
	$args = wp_parse_args(
		$args,
		array(
			'category' => '',
			'ids'      => '',
			'skus'     => '',
			'limit'    => 8,
			'orderby'  => 'menu_order',
		)
	);
	$limit = max( 1, min( 24, (int) $args['limit'] ) );
	$key   = 'charmed_sc_' . md5( wp_json_encode( array( $args, charmed_showcase_cache_version(), get_locale() ) ) );
	$ids   = get_transient( $key );

	if ( ! is_array( $ids ) ) {
		$ids = array();
		$list = static function ( string $csv ): array {
			return array_values( array_filter( array_map( 'trim', explode( ',', $csv ) ) ) );
		};

		if ( '' !== trim( (string) $args['skus'] ) ) {
			foreach ( $list( (string) $args['skus'] ) as $sku ) {
				$id = wc_get_product_id_by_sku( $sku );
				if ( $id ) {
					$ids[] = (int) $id;
				}
			}
		} elseif ( '' !== trim( (string) $args['ids'] ) ) {
			$ids = array_map( 'absint', $list( (string) $args['ids'] ) );
		} else {
			$orderby = in_array( $args['orderby'], array( 'menu_order', 'date', 'price', 'popularity', 'rand' ), true ) ? $args['orderby'] : 'menu_order';
			$query   = array(
				'status'     => 'publish',
				'visibility' => 'catalog',
				'limit'      => $limit,
				'orderby'    => $orderby,
				'order'      => 'date' === $orderby || 'popularity' === $orderby ? 'DESC' : 'ASC',
				'return'     => 'ids',
			);
			if ( '' !== trim( (string) $args['category'] ) ) {
				$query['category'] = $list( (string) $args['category'] );
			}
			if ( 'yes' === get_option( 'woocommerce_hide_out_of_stock_items' ) ) {
				$query['stock_status'] = 'instock';
			}
			$ids = wc_get_products( $query );
		}
		$ids = array_slice( array_values( array_unique( array_filter( array_map( 'absint', (array) $ids ) ) ) ), 0, $limit );
		set_transient( $key, $ids, 12 * HOUR_IN_SECONDS );
	}

	$products = array();
	foreach ( $ids as $id ) {
		$product = wc_get_product( $id );
		if ( $product && $product->is_visible() && 'publish' === $product->get_status() ) {
			$products[] = $product;
		}
	}
	return $products;
}

/**
 * Nom court pour l'affichage (« Parure Molten Art » → « Molten Art », « Molten Art Set » → « Molten Art »).
 *
 * @param string $name Nom complet.
 */
function charmed_short_name( string $name ): string {
	$prefixes = apply_filters( 'charmed_name_prefixes', array( 'Parure ', 'Set ' ) );
	foreach ( $prefixes as $p ) {
		if ( 0 === stripos( $name, $p ) ) {
			$name = substr( $name, strlen( $p ) );
			break;
		}
	}
	return trim( (string) preg_replace( '/\s+(Jewelry\s+)?Set$/i', '', $name ) );
}

/**
 * Univers d'un produit = première catégorie hors catégories techniques.
 *
 * @param WC_Product $product Produit.
 */
function charmed_product_univers( WC_Product $product ): ?WP_Term {
	$skip  = apply_filters( 'charmed_univers_skip_slugs', array( 'uncategorized', 'non-classe', 'parures', 'accueil', 'coffrets-accueil', 'homme', 'femme' ) );
	$terms = get_the_terms( $product->get_id(), 'product_cat' );
	if ( ! is_array( $terms ) ) {
		return null;
	}
	foreach ( $terms as $term ) {
		if ( ! in_array( $term->slug, $skip, true ) ) {
			return $term;
		}
	}
	return $terms[0] ?? null;
}

/**
 * Données normalisées d'un produit pour les vitrines.
 *
 * @param WC_Product $product Produit.
 */
function charmed_product_data( WC_Product $product ): array {
	$id      = $product->get_id();
	$name    = $product->get_name();
	$short   = charmed_short_name( $name );
	$univers = charmed_product_univers( $product );

	$line = (string) $product->get_meta( '_charmed_line' );
	if ( '' === $line ) {
		$line = wp_trim_words( wp_strip_all_tags( (string) $product->get_short_description() ), 10, '…' );
	}

	$code = strtoupper( (string) $product->get_meta( '_charmed_code' ) );
	if ( '' === $code ) {
		$code = strtoupper( substr( (string) preg_replace( '/[^A-Za-z]/', '', remove_accents( $short ) ), 0, 3 ) );
	}

	$pieces = array_values( array_filter( array_map( 'trim', preg_split( '/\r\n|\r|\n/', (string) $product->get_meta( '_charmed_pieces' ) ) ) ) );

	$cutout = (int) $product->get_meta( '_charmed_cutout_id' );
	$image  = $cutout ? $cutout : (int) $product->get_image_id();

	$ajax = $product->is_type( 'simple' ) && $product->is_purchasable() && $product->is_in_stock() && $product->supports( 'ajax_add_to_cart' );

	return array(
		'id'         => $id,
		'name'       => $name,
		'short'      => $short,
		'url'        => get_permalink( $id ),
		'price_html' => $product->get_price_html(),
		'price_text' => wp_strip_all_tags( html_entity_decode( $product->get_price_html(), ENT_QUOTES, 'UTF-8' ) ),
		'univers'    => $univers ? $univers->name : '',
		'line'       => $line,
		'code'       => $code,
		'pieces'     => $pieces,
		'sku'        => (string) $product->get_sku(),
		'image_id'   => $image,
		'is_cutout'  => (bool) $cutout,
		'in_stock'   => $product->is_in_stock(),
		'ajax'       => $ajax,
		'add_url'    => $ajax ? add_query_arg( 'add-to-cart', $id, get_permalink( $id ) ) : get_permalink( $id ),
		'add_text'   => $ajax ? __( 'Ajouter à l’écrin', 'charmed-paris' ) : ( $product->is_in_stock() ? __( 'Choisir', 'charmed-paris' ) : __( 'Épuisée', 'charmed-paris' ) ),
	);
}

/**
 * Lien / bouton d'ajout au panier : fonctionne sans JS (GET ?add-to-cart=ID, natif WooCommerce),
 * amélioré par cart.js (Store API, sans rechargement, ouvre le mini-panier).
 *
 * @param array  $p     Données charmed_product_data().
 * @param string $class Classes CSS.
 * @param string $label Libellé (défaut : add_text).
 */
function charmed_add_to_cart_link( array $p, string $class = 'cp-btn', string $label = '' ): string {
	$label = '' !== $label ? $label : $p['add_text'];
	$attrs = $p['ajax'] ? sprintf( ' data-cp-add="%d" data-cp-name="%s" rel="nofollow"', (int) $p['id'], esc_attr( $p['short'] ) ) : '';
	return sprintf(
		'<a class="%1$s" href="%2$s"%3$s aria-label="%4$s">%5$s</a>',
		esc_attr( $class ),
		esc_url( $p['add_url'] ),
		$attrs,
		/* translators: 1: action (Ajouter à l'écrin), 2: product name */
		esc_attr( sprintf( __( '%1$s : %2$s', 'charmed-paris' ), $label, $p['name'] ) ),
		esc_html( $label )
	);
}

/*
 * ---------------------------------------------------------------------------
 * Champs produit (admin).
 * ---------------------------------------------------------------------------
 */
add_action(
	'woocommerce_product_options_general_product_data',
	static function () {
		echo '<div class="options_group charmed-fields">';
		woocommerce_wp_text_input(
			array(
				'id'          => '_charmed_cutout_id',
				'label'       => __( 'Image détourée (ID média)', 'charmed-paris' ),
				'desc_tip'    => true,
				'description' => __( 'ID de la parure détourée (fond transparent) utilisée par les coffrets et la file des parures. Médiathèque > clic sur l’image > ID dans l’URL. Vide = image principale.', 'charmed-paris' ),
				'type'        => 'number',
			)
		);
		woocommerce_wp_text_input(
			array(
				'id'          => '_charmed_line',
				'label'       => __( 'Ligne courte (étiquette)', 'charmed-paris' ),
				'placeholder' => __( 'Collier et boucles, métal doré', 'charmed-paris' ),
			)
		);
		woocommerce_wp_text_input(
			array(
				'id'                => '_charmed_code',
				'label'             => __( 'Code étiquette (3 lettres)', 'charmed-paris' ),
				'custom_attributes' => array( 'maxlength' => 4 ),
			)
		);
		woocommerce_wp_textarea_input(
			array(
				'id'          => '_charmed_pieces',
				'label'       => __( 'Composition (une pièce par ligne)', 'charmed-paris' ),
				'placeholder' => __( "Collier\nBoucles d’oreilles", 'charmed-paris' ),
			)
		);
		echo '</div>';
	}
);

add_action(
	'woocommerce_admin_process_product_object',
	static function ( WC_Product $product ) {
		// phpcs:disable WordPress.Security.NonceVerification.Missing -- nonce vérifié par WooCommerce (save_post).
		if ( isset( $_POST['_charmed_cutout_id'] ) ) {
			$product->update_meta_data( '_charmed_cutout_id', absint( wp_unslash( $_POST['_charmed_cutout_id'] ) ) ?: '' );
		}
		if ( isset( $_POST['_charmed_line'] ) ) {
			$product->update_meta_data( '_charmed_line', sanitize_text_field( wp_unslash( $_POST['_charmed_line'] ) ) );
		}
		if ( isset( $_POST['_charmed_code'] ) ) {
			$product->update_meta_data( '_charmed_code', strtoupper( substr( sanitize_key( wp_unslash( $_POST['_charmed_code'] ) ), 0, 4 ) ) );
		}
		if ( isset( $_POST['_charmed_pieces'] ) ) {
			$product->update_meta_data( '_charmed_pieces', sanitize_textarea_field( wp_unslash( $_POST['_charmed_pieces'] ) ) );
		}
		// phpcs:enable
	}
);
