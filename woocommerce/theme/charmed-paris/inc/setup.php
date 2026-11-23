<?php
/**
 * Supports du thème, traductions, tailles d'images, catégories de patterns.
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'after_setup_theme',
	static function () {
		// Traductions : languages/{locale}.mo (convention des thèmes ; source en français, en_US et en_GB fournis).
		load_theme_textdomain( 'charmed-paris', CHARMED_DIR . '/languages' );

		add_theme_support( 'woocommerce' );
		add_theme_support( 'wc-product-gallery-zoom' );
		add_theme_support( 'wc-product-gallery-lightbox' );
		add_theme_support( 'wc-product-gallery-slider' );
		add_theme_support( 'responsive-embeds' );
		add_theme_support( 'editor-styles' );
		add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );

		// Les styles de sections sont aussi chargés dans l'éditeur pour que l'aperçu des blocs soit fidèle.
		add_editor_style( array( 'assets/css/base.css', 'assets/css/sections.css', 'assets/css/intro.css' ) );

		// Parure détourée (coffrets, file des parures) : carré non recadré, 2x de 440 px.
		add_image_size( 'charmed-cutout', 880, 880, false );
		add_image_size( 'charmed-cutout-sm', 440, 440, false );
		// Univers : portrait 3:4.
		add_image_size( 'charmed-univers', 600, 800, true );
	}
);

/**
 * Catégorie de patterns du thème.
 */
add_action(
	'init',
	static function () {
		register_block_pattern_category(
			'charmed-paris',
			array( 'label' => __( 'CHARMED PARIS', 'charmed-paris' ) )
		);
	}
);

/**
 * Libellés lisibles pour les tailles d'images personnalisées dans la médiathèque.
 */
add_filter(
	'image_size_names_choose',
	static function ( $sizes ) {
		$sizes['charmed-cutout'] = __( 'Parure détourée', 'charmed-paris' );
		$sizes['charmed-univers'] = __( 'Univers (3:4)', 'charmed-paris' );
		return $sizes;
	}
);

/**
 * Le thème ne rend pas les classes WooCommerce « columns-x » inutiles : on laisse Woo gérer.
 * Petit utilitaire : URL d'un asset du thème.
 *
 * @param string $path Chemin relatif à assets/.
 */
function charmed_asset( string $path ): string {
	return CHARMED_URI . '/assets/' . ltrim( $path, '/' );
}

/**
 * Version d'un asset pour le cache-busting (filemtime en dev, version du thème sinon).
 *
 * @param string $path Chemin relatif à assets/.
 */
function charmed_asset_ver( string $path ): string {
	$file = CHARMED_DIR . '/assets/' . ltrim( $path, '/' );
	if ( defined( 'WP_DEBUG' ) && WP_DEBUG && file_exists( $file ) ) {
		return (string) filemtime( $file );
	}
	return CHARMED_VERSION;
}

/**
 * Vrai si WooCommerce est actif.
 */
function charmed_has_wc(): bool {
	return class_exists( 'WooCommerce' ) && function_exists( 'WC' );
}

/**
 * Accueil : en-tête transparent superposé à l'intro (header.js le rend plein après l'intro).
 */
add_filter(
	'body_class',
	static function ( $classes ) {
		if ( is_front_page() ) {
			$classes[] = 'cp-has-intro';
		}
		return $classes;
	}
);
