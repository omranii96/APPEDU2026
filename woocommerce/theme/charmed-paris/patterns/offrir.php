<?php
/**
 * Title: Offrir — l'écrin et les packagings
 * Slug: charmed-paris/offrir
 * Categories: charmed-paris
 * Viewport Width: 1400
 *
 * Faits packaging (FAQ fournisseur 12872188) : une seule boîte à bijoux par commande (pièces
 * suivantes en sachets scellés), ligne 925 en écrin velours bleu sans logo, pas de message cadeau,
 * bordereau sans prix. Ne jamais citer le fournisseur côté client.
 *
 * @package CharmedParis
 */

$xmas = function_exists( 'charmed_xmas_state' ) && charmed_xmas_state()['packaging'];
?>
<!-- wp:group {"align":"wide","anchor":"offrir","style":{"spacing":{"padding":{"top":"var:preset|spacing|50","bottom":"var:preset|spacing|70"}}},"layout":{"type":"default"}} -->
<div id="offrir" class="wp-block-group alignwide" style="padding-top:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--70)">
	<!-- wp:columns {"verticalAlignment":"center","style":{"spacing":{"blockGap":{"left":"56px"}}}} -->
	<div class="wp-block-columns are-vertically-aligned-center">
		<!-- wp:column {"verticalAlignment":"center"} -->
		<div class="wp-block-column is-vertically-aligned-center"><!-- wp:charmed/packshots /--></div>
		<!-- /wp:column -->
		<!-- wp:column {"verticalAlignment":"center"} -->
		<div class="wp-block-column is-vertically-aligned-center">
			<!-- wp:paragraph {"className":"cp-eyebrow"} --><p class="cp-eyebrow"><?php esc_html_e( 'L’écrin Charmed', 'charmed-paris' ); ?></p><!-- /wp:paragraph -->
			<!-- wp:heading --><h2 class="wp-block-heading"><?php esc_html_e( 'Chaque commande part prête à offrir', 'charmed-paris' ); ?></h2><!-- /wp:heading -->
			<!-- wp:list {"className":"cp-steps"} -->
			<ul class="wp-block-list cp-steps">
				<li><?php esc_html_e( 'Un carton d’envoi à notre logo et, à l’intérieur, une boîte à bijoux à tiroir nouée d’un ruban.', 'charmed-paris' ); ?></li>
				<li><?php esc_html_e( 'Une pochette en velours, une chamoisine d’entretien et une carte de conseils.', 'charmed-paris' ); ?></li>
				<li><?php esc_html_e( 'Plusieurs parures ? Elles voyagent dans le même colis : la première dans la boîte à bijoux, les suivantes dans des sachets refermables.', 'charmed-paris' ); ?></li>
				<li><?php esc_html_e( 'Joaillerie 925 : la parure arrive dans un écrin en velours bleu.', 'charmed-paris' ); ?></li>
				<li><?php esc_html_e( 'Aucun prix sur le bordereau : tu peux l’envoyer directement à la personne que tu gâtes.', 'charmed-paris' ); ?></li>
				<?php if ( $xmas ) : ?>
				<li><?php esc_html_e( 'Jusqu’au 24 décembre : papier cadeau de fête, ruban et carte de Noël, offerts.', 'charmed-paris' ); ?></li>
				<?php endif; ?>
			</ul>
			<!-- /wp:list -->
		</div>
		<!-- /wp:column -->
	</div>
	<!-- /wp:columns -->
</div>
<!-- /wp:group -->
