<?php
/**
 * Title: En-tête
 * Slug: charmed-paris/header
 * Categories: header
 * Block Types: core/template-part/header
 * Inserter: no
 *
 * Navigation, logo CHARMED PARIS (HTML/CSS), recherche produits, langue, compte, mini-panier WooCommerce.
 *
 * @package CharmedParis
 */

$shop = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/boutique/' );
$cat  = static function ( string $slug ) use ( $shop ): string {
	$link = taxonomy_exists( 'product_cat' ) ? get_term_link( $slug, 'product_cat' ) : '';
	return is_string( $link ) && $link ? $link : $shop;
};
?>
<!-- wp:group {"tagName":"header","className":"cp-header","layout":{"type":"constrained"}} -->
<header class="wp-block-group cp-header">
	<!-- wp:group {"align":"wide","className":"cp-header__inner","layout":{"type":"default"}} -->
	<div class="wp-block-group alignwide cp-header__inner">
		<!-- wp:navigation {"className":"cp-header__nav","overlayMenu":"mobile","ariaLabel":"<?php echo esc_attr__( 'Navigation principale', 'charmed-paris' ); ?>","layout":{"type":"flex","justifyContent":"left"}} -->
		<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Parures', 'charmed-paris' ); ?>","url":"<?php echo esc_url( $shop ); ?>","kind":"custom"} /-->
		<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Cadeaux', 'charmed-paris' ); ?>","url":"<?php echo esc_url( home_url( '/#cadeaux' ) ); ?>","kind":"custom"} /-->
		<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Joaillerie 925', 'charmed-paris' ); ?>","url":"<?php echo esc_url( $cat( 'joaillerie-argent-925' ) ); ?>","kind":"custom"} /-->
		<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Homme', 'charmed-paris' ); ?>","url":"<?php echo esc_url( $cat( 'homme' ) ); ?>","kind":"custom"} /-->
		<!-- /wp:navigation -->

		<!-- wp:group {"className":"cp-header__brand","layout":{"type":"flex","justifyContent":"center"}} -->
		<div class="wp-block-group cp-header__brand"><!-- wp:charmed/wordmark {"size":22} /--></div>
		<!-- /wp:group -->

		<!-- wp:group {"className":"cp-header__tools","layout":{"type":"flex","flexWrap":"nowrap","justifyContent":"right"}} -->
		<div class="wp-block-group cp-header__tools">
			<!-- wp:search {"label":"<?php echo esc_attr__( 'Rechercher une parure', 'charmed-paris' ); ?>","showLabel":false,"placeholder":"<?php echo esc_attr__( 'Rechercher une parure', 'charmed-paris' ); ?>","buttonText":"<?php echo esc_attr__( 'Rechercher', 'charmed-paris' ); ?>","buttonPosition":"button-only","buttonUseIcon":true,"isSearchFieldHidden":true,"query":{"post_type":"product"}} /-->
			<!-- wp:charmed/language-switcher /-->
			<!-- wp:woocommerce/customer-account {"displayStyle":"icon_only","iconStyle":"line"} /-->
			<!-- wp:woocommerce/mini-cart {"addToCartBehaviour":"open_drawer","hasHiddenPrice":true} /-->
		</div>
		<!-- /wp:group -->
	</div>
	<!-- /wp:group -->
</header>
<!-- /wp:group -->
