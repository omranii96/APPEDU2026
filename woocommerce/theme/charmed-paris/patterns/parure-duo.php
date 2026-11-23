<?php
/**
 * Title: La parure Charmed (duo + 2e parure)
 * Slug: charmed-paris/parure-duo
 * Categories: charmed-paris
 * Viewport Width: 1400
 *
 * @package CharmedParis
 */

$shop  = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/' );
$label = function_exists( 'charmed_bundle_label' ) ? charmed_bundle_label() : '';
$img   = static fn( string $f ): string => esc_url( get_template_directory_uri() . '/assets/img/univers/' . $f );
?>
<!-- wp:group {"align":"full","className":"cp-parure","backgroundColor":"velours","textColor":"velours-fg","style":{"spacing":{"padding":{"top":"var:preset|spacing|70","bottom":"var:preset|spacing|70"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull cp-parure has-velours-fg-color has-velours-background-color has-text-color has-background" style="padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--70)">
	<!-- wp:columns {"align":"wide","verticalAlignment":"center"} -->
	<div class="wp-block-columns alignwide are-vertically-aligned-center">
		<!-- wp:column {"verticalAlignment":"center"} -->
		<div class="wp-block-column is-vertically-aligned-center">
			<!-- wp:paragraph {"className":"cp-eyebrow","textColor":"or-clair"} --><p class="cp-eyebrow has-or-clair-color has-text-color"><?php esc_html_e( 'La parure Charmed', 'charmed-paris' ); ?></p><!-- /wp:paragraph -->
			<!-- wp:heading --><h2 class="wp-block-heading"><?php esc_html_e( 'Le collier et ses boucles, pensés ensemble.', 'charmed-paris' ); ?></h2><!-- /wp:heading -->
			<!-- wp:paragraph {"textColor":"velours-muted"} -->
			<p class="has-velours-muted-color has-text-color"><?php
			if ( $label ) {
				/* translators: %s: discount label, e.g. "2e parure −15 %" */
				echo esc_html( sprintf( __( 'Rien à assortir : chaque parure est un ensemble, prêt à offrir. Et pour en offrir une, et garder l’autre : %s, appliquée automatiquement au panier.', 'charmed-paris' ), $label ) );
			} else {
				esc_html_e( 'Rien à assortir : chaque parure est un ensemble, prêt à offrir.', 'charmed-paris' );
			}
			?></p>
			<!-- /wp:paragraph -->
			<!-- wp:buttons --><div class="wp-block-buttons"><!-- wp:button {"className":"is-style-outline"} --><div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( $shop ); ?>"><?php esc_html_e( 'Voir les parures', 'charmed-paris' ); ?></a></div><!-- /wp:button --></div><!-- /wp:buttons -->
		</div>
		<!-- /wp:column -->
		<!-- wp:column {"verticalAlignment":"center"} -->
		<div class="wp-block-column is-vertically-aligned-center">
			<!-- wp:html -->
			<div class="cp-duo" aria-hidden="true"><span class="cp-br cp-br--l"></span><span class="cp-duo__pieces"><img src="<?php echo $img( 'sculpture.webp' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>" alt="" width="400" height="400" loading="lazy"><span class="cp-duo__plus">+</span><img src="<?php echo $img( 'eclat.webp' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>" alt="" width="400" height="400" loading="lazy"></span><span class="cp-br cp-br--r"></span></div>
			<!-- /wp:html -->
		</div>
		<!-- /wp:column -->
	</div>
	<!-- /wp:columns -->
</div>
<!-- /wp:group -->
