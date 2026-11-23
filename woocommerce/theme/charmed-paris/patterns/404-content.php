<?php
/**
 * Title: Contenu 404
 * Slug: charmed-paris/404-content
 * Categories: charmed-paris
 * Inserter: no
 *
 * @package CharmedParis
 */

$shop = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/' );
?>
<!-- wp:group {"layout":{"type":"flex","orientation":"vertical","justifyContent":"center"}} -->
<div class="wp-block-group">
	<!-- wp:charmed/wordmark {"size":48,"link":false} /-->
	<!-- wp:heading {"level":1,"textAlign":"center","fontSize":"xx-large"} --><h1 class="wp-block-heading has-text-align-center has-xx-large-font-size"><?php esc_html_e( 'Cet écrin est vide.', 'charmed-paris' ); ?></h1><!-- /wp:heading -->
	<!-- wp:paragraph {"align":"center"} --><p class="has-text-align-center"><?php esc_html_e( 'La page que tu cherches n’existe pas ou a changé d’adresse.', 'charmed-paris' ); ?></p><!-- /wp:paragraph -->
	<!-- wp:search {"label":"<?php echo esc_attr__( 'Rechercher une parure', 'charmed-paris' ); ?>","showLabel":false,"buttonText":"<?php echo esc_attr__( 'Rechercher', 'charmed-paris' ); ?>","query":{"post_type":"product"}} /-->
	<!-- wp:buttons --><div class="wp-block-buttons"><!-- wp:button --><div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( $shop ); ?>"><?php esc_html_e( 'Voir les parures', 'charmed-paris' ); ?></a></div><!-- /wp:button --></div><!-- /wp:buttons -->
</div>
<!-- /wp:group -->
