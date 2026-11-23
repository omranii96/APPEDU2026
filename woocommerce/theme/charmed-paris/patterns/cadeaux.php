<?php
/**
 * Title: Offrir selon ton budget
 * Slug: charmed-paris/cadeaux
 * Categories: charmed-paris, woo-commerce
 * Viewport Width: 1400
 *
 * Liens vers la boutique filtrée par prix (paramètres natifs min_price / max_price).
 *
 * @package CharmedParis
 */

$shop = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/' );
$u    = static fn( array $q ): string => esc_url( add_query_arg( $q, $shop ) );
?>
<!-- wp:group {"align":"wide","anchor":"cadeaux","style":{"spacing":{"padding":{"top":"var:preset|spacing|70","bottom":"var:preset|spacing|50"}}},"layout":{"type":"default"}} -->
<div id="cadeaux" class="wp-block-group alignwide" style="padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--50)">
	<!-- wp:paragraph {"className":"cp-eyebrow"} --><p class="cp-eyebrow"><?php esc_html_e( 'Idées cadeaux', 'charmed-paris' ); ?></p><!-- /wp:paragraph -->
	<!-- wp:heading --><h2 class="wp-block-heading"><?php esc_html_e( 'Offrir, selon ton budget', 'charmed-paris' ); ?></h2><!-- /wp:heading -->
	<!-- wp:html -->
	<div class="wp-block-columns cp-budgets">
		<a class="wp-block-column cp-budget" href="<?php echo $u( array( 'max_price' => 50 ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><span><?php esc_html_e( 'Jusqu’à', 'charmed-paris' ); ?></span><p class="cp-budget__amount">50 €</p><span><?php esc_html_e( 'Parures Sculpture et Mixte', 'charmed-paris' ); ?></span></a>
		<a class="wp-block-column cp-budget" href="<?php echo $u( array( 'min_price' => 50, 'max_price' => 100 ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><span><?php esc_html_e( 'De 50 à', 'charmed-paris' ); ?></span><p class="cp-budget__amount">100 €</p><span><?php esc_html_e( 'Parures Éclat et Couleur précieuse', 'charmed-paris' ); ?></span></a>
		<a class="wp-block-column cp-budget" href="<?php echo $u( array( 'min_price' => 100 ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><span><?php esc_html_e( 'Plus de', 'charmed-paris' ); ?></span><p class="cp-budget__amount">100 €</p><span><?php esc_html_e( 'Joaillerie argent 925 et moissanite synthétique', 'charmed-paris' ); ?></span></a>
	</div>
	<!-- /wp:html -->
</div>
<!-- /wp:group -->
