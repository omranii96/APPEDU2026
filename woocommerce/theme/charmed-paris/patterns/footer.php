<?php
/**
 * Title: Pied de page
 * Slug: charmed-paris/footer
 * Categories: footer
 * Block Types: core/template-part/footer
 * Inserter: no
 *
 * Liens légaux obligatoires (CGV, mentions légales, confidentialité, cookies, rétractation L221-21).
 * Les URL pointent vers les slugs français ; TranslatePress les traduit sur /en/.
 *
 * @package CharmedParis
 */

$shop  = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/boutique/' );
$page  = static fn( string $slug ): string => esc_url( home_url( '/' . $slug . '/' ) );
$priv  = get_privacy_policy_url() ? get_privacy_policy_url() : home_url( '/politique-de-confidentialite/' );
?>
<!-- wp:group {"tagName":"footer","className":"cp-footer","style":{"spacing":{"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|40"}}},"layout":{"type":"constrained"}} -->
<footer class="wp-block-group cp-footer" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--40)">
	<!-- wp:columns {"align":"wide"} -->
	<div class="wp-block-columns alignwide">
		<!-- wp:column {"width":"40%"} -->
		<div class="wp-block-column" style="flex-basis:40%">
			<!-- wp:charmed/wordmark {"size":26,"link":false} /-->
			<!-- wp:paragraph -->
			<p><?php esc_html_e( 'Des parures prêtes à offrir. Ouvre. Laisse-toi charmer.', 'charmed-paris' ); ?></p>
			<!-- /wp:paragraph -->
			<!-- wp:charmed/promo-notice {"parts":"delivery,ddp","variant":"inline","context":"product"} /-->
		</div>
		<!-- /wp:column -->
		<!-- wp:column -->
		<div class="wp-block-column">
			<!-- wp:heading {"level":2} --><h2 class="wp-block-heading"><?php esc_html_e( 'Boutique', 'charmed-paris' ); ?></h2><!-- /wp:heading -->
			<!-- wp:list {"className":"is-style-plain"} -->
			<ul class="wp-block-list is-style-plain">
				<li><a href="<?php echo esc_url( $shop ); ?>"><?php esc_html_e( 'Toutes les parures', 'charmed-paris' ); ?></a></li>
				<li><a href="<?php echo esc_url( home_url( '/#cadeaux' ) ); ?>"><?php esc_html_e( 'Idées cadeaux', 'charmed-paris' ); ?></a></li>
				<li><a href="<?php echo $page( 'entretien' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><?php esc_html_e( 'Entretien des bijoux', 'charmed-paris' ); ?></a></li>
			</ul>
			<!-- /wp:list -->
		</div>
		<!-- /wp:column -->
		<!-- wp:column -->
		<div class="wp-block-column">
			<!-- wp:heading {"level":2} --><h2 class="wp-block-heading"><?php esc_html_e( 'Aide', 'charmed-paris' ); ?></h2><!-- /wp:heading -->
			<!-- wp:list {"className":"is-style-plain"} -->
			<ul class="wp-block-list is-style-plain">
				<li><a href="<?php echo $page( 'livraison' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><?php esc_html_e( 'Livraison', 'charmed-paris' ); ?></a></li>
				<li><a href="<?php echo $page( 'retours-et-retractation' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><?php esc_html_e( 'Retours et rétractation', 'charmed-paris' ); ?></a></li>
				<li><a href="<?php echo $page( 'contact' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><?php esc_html_e( 'Contact', 'charmed-paris' ); ?></a></li>
			</ul>
			<!-- /wp:list -->
			<!-- wp:charmed/withdrawal-link /-->
		</div>
		<!-- /wp:column -->
		<!-- wp:column -->
		<div class="wp-block-column">
			<!-- wp:heading {"level":2} --><h2 class="wp-block-heading"><?php esc_html_e( 'Informations légales', 'charmed-paris' ); ?></h2><!-- /wp:heading -->
			<!-- wp:list {"className":"is-style-plain"} -->
			<ul class="wp-block-list is-style-plain">
				<li><a href="<?php echo $page( 'cgv' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><?php esc_html_e( 'Conditions générales de vente', 'charmed-paris' ); ?></a></li>
				<li><a href="<?php echo $page( 'mentions-legales' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><?php esc_html_e( 'Mentions légales', 'charmed-paris' ); ?></a></li>
				<li><a href="<?php echo esc_url( $priv ); ?>"><?php esc_html_e( 'Confidentialité', 'charmed-paris' ); ?></a></li>
				<li><a href="<?php echo $page( 'cookies' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>"><?php esc_html_e( 'Cookies', 'charmed-paris' ); ?></a></li>
			</ul>
			<!-- /wp:list -->
		</div>
		<!-- /wp:column -->
	</div>
	<!-- /wp:columns -->
	<!-- wp:paragraph {"align":"wide","className":"cp-legal","style":{"spacing":{"padding":{"top":"18px"}}}} -->
	<p class="alignwide cp-legal" style="padding-top:18px">© <?php echo esc_html( wp_date( 'Y' ) ); ?> CHARMED PARIS · <?php esc_html_e( 'Prix TTC en euros', 'charmed-paris' ); ?></p>
	<!-- /wp:paragraph -->
</footer>
<!-- /wp:group -->
