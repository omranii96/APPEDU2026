<?php
/**
 * Styles, scripts, préchargements et allègement des assets WooCommerce.
 *
 * Principe :
 *  - base.css + header.js (≈ 1 Ko) sur toutes les pages ;
 *  - sections.css et les scripts de section ne sont chargés QUE si le bloc correspondant est rendu
 *    (style_handles / enqueue dans le render callback) ;
 *  - intro.js uniquement sur l'accueil (defer) ; Three.js n'est jamais enqueue côté PHP : intro.js le
 *    télécharge à la demande (première interaction ou temps mort), et jamais si prefers-reduced-motion,
 *    Save-Data, ou WebGL absent.
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

/**
 * Enregistrement de tous les assets (front + éditeur).
 */
function charmed_register_assets(): void {
	$css = array(
		'charmed-base'     => 'css/base.css',
		'charmed-sections' => 'css/sections.css',
		'charmed-intro'    => 'css/intro.css',
	);
	foreach ( $css as $handle => $path ) {
		wp_register_style( $handle, charmed_asset( $path ), array(), charmed_asset_ver( $path ) );
	}

	$defer = array(
		'strategy'  => 'defer',
		'in_footer' => true,
	);
	$js = array(
		'charmed-header'    => array( 'js/header.js', array() ),
		'charmed-cart'      => array( 'js/cart.js', array() ),
		'charmed-coffrets'  => array( 'js/coffrets.js', array( 'charmed-cart' ) ),
		'charmed-file'      => array( 'js/file-parures.js', array( 'charmed-cart' ) ),
		'charmed-packshots' => array( 'js/packshots.js', array() ),
		'charmed-intro'     => array( 'js/intro.js', array() ),
	);
	foreach ( $js as $handle => $def ) {
		wp_register_script( $handle, charmed_asset( $def[0] ), $def[1], charmed_asset_ver( $def[0] ), $defer );
	}

	// Données du panier pour cart.js (Store API WooCommerce). Le nonce est rafraîchi par cart.js
	// via l'en-tête « Nonce » des réponses : compatible cache de page.
	wp_localize_script(
		'charmed-cart',
		'charmedCart',
		array(
			'api'     => esc_url_raw( rest_url( 'wc/store/v1/' ) ),
			'nonce'   => charmed_has_wc() ? wp_create_nonce( 'wc_store_api' ) : '',
			'cartUrl' => charmed_has_wc() ? esc_url_raw( wc_get_cart_url() ) : '',
			'i18n'    => array(
				'added'    => __( '%s ajoutée à ton écrin', 'charmed-paris' ),
				'error'    => __( 'Impossible d’ajouter cette parure. Réessaie depuis sa fiche.', 'charmed-paris' ),
				'adding'   => __( 'Ajout…', 'charmed-paris' ),
				'viewCart' => __( 'Voir le panier', 'charmed-paris' ),
			),
		)
	);
}
add_action( 'init', 'charmed_register_assets' );

/**
 * Assets globaux du front.
 */
add_action(
	'wp_enqueue_scripts',
	static function () {
		wp_enqueue_style( 'charmed-base' );
		wp_enqueue_script( 'charmed-header' );
	}
);

/**
 * Classe « cp-js » posée avant le premier rendu (évite le CLS du mode film / carrousels),
 * et « cp-motion » si l'utilisatrice n'a pas demandé à réduire les animations.
 */
add_action(
	'wp_head',
	static function () {
		echo "<script>(function(d){var c=d.documentElement.classList;c.add('cp-js');try{if(!matchMedia('(prefers-reduced-motion: reduce)').matches){c.add('cp-motion');}}catch(e){}})(document);</script>\n";
	},
	0
);

/**
 * Préchargements : polices du logo et du texte (toutes pages), poster de l'intro (accueil) s'il existe.
 */
add_filter(
	'wp_preload_resources',
	static function ( $resources ) {
		$fonts = array( 'fonts/bodoni-moda-latin-wght.woff2', 'fonts/jost-latin-wght.woff2' );
		foreach ( $fonts as $font ) {
			$resources[] = array(
				'href'        => charmed_asset( $font ),
				'as'          => 'font',
				'type'        => 'font/woff2',
				'crossorigin' => 'anonymous',
			);
		}
		if ( is_front_page() ) {
			$poster = charmed_intro_poster();
			if ( $poster ) {
				$resources[] = array(
					'href'          => $poster,
					'as'            => 'image',
					'fetchpriority' => 'high',
				);
			}
		}
		return $resources;
	}
);

/**
 * URL du poster statique de l'intro (assets/img/intro-poster.webp), ou chaîne vide.
 * Voir tech/performance.md pour le produire.
 */
function charmed_intro_poster(): string {
	$rel = 'img/intro-poster.webp';
	$url = file_exists( CHARMED_DIR . '/assets/' . $rel ) ? charmed_asset( $rel ) : '';
	return (string) apply_filters( 'charmed_intro_poster', $url );
}

/**
 * Contexte « boutique » : pages où les scripts/styles classiques de WooCommerce sont utiles.
 */
function charmed_is_shop_context(): bool {
	if ( ! charmed_has_wc() ) {
		return false;
	}
	if ( is_woocommerce() || is_cart() || is_checkout() || is_account_page() ) {
		return true;
	}
	// Pages qui embarquent des shortcodes WooCommerce classiques.
	$post = get_post();
	if ( $post instanceof WP_Post ) {
		foreach ( array( 'products', 'product_page', 'product_category', 'add_to_cart', 'woocommerce_cart', 'woocommerce_checkout', 'woocommerce_my_account' ) as $sc ) {
			if ( has_shortcode( $post->post_content, $sc ) ) {
				return true;
			}
		}
	}
	return false;
}

/**
 * Allègement prudent hors pages boutique.
 *
 * Retiré : CSS classiques Woo (le thème bloc et les blocs Woo apportent les leurs), cart-fragments
 * (inutile avec le bloc Mini-panier), add-to-cart.js (nos sections utilisent la Store API),
 * woocommerce.js (notices de démo, mot de passe du compte).
 * CONSERVÉ volontairement : wc-order-attribution / sourcebuster (attribution des commandes : doit
 * tourner sur les pages d'atterrissage), scripts des blocs Woo (chargés par les blocs eux-mêmes),
 * scripts de passerelles de paiement (Stripe/PayPal gèrent leur propre chargement).
 * Désactivable : add_filter( 'charmed_trim_woo_assets', '__return_false' );
 */
add_action(
	'wp_enqueue_scripts',
	static function () {
		if ( ! charmed_has_wc() || charmed_is_shop_context() || ! apply_filters( 'charmed_trim_woo_assets', true ) ) {
			return;
		}
		foreach ( array( 'woocommerce-layout', 'woocommerce-smallscreen', 'woocommerce-general' ) as $style ) {
			wp_dequeue_style( $style );
		}
		foreach ( array( 'wc-cart-fragments', 'wc-add-to-cart', 'woocommerce' ) as $script ) {
			wp_dequeue_script( $script );
		}
	},
	99
);
