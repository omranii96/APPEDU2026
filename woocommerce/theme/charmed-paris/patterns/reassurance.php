<?php
/**
 * Title: Réassurance
 * Slug: charmed-paris/reassurance
 * Categories: charmed-paris
 * Viewport Width: 1400
 *
 * Textes vérifiés : délai France 4–9 jours ouvrés (90 % des colis), droits inclus (DDP),
 * seuil lu dans WooCommerce, rétractation 14 jours, garantie légale 2 ans.
 * « Moyens de paiement » : à adapter aux passerelles réellement activées.
 *
 * @package CharmedParis
 */

$days      = function_exists( 'charmed_delivery_days' ) ? charmed_delivery_days( 'FR' ) : '4–9';
$threshold = function_exists( 'charmed_free_shipping_threshold' ) ? charmed_free_shipping_threshold() : 0;
$cols      = array(
	/* translators: %s: business days range */
	array( sprintf( __( 'Livraison en %s jours ouvrés', 'charmed-paris' ), $days ), $threshold > 0 && function_exists( 'charmed_price_plain' ) ? sprintf( /* translators: %s: amount */ __( 'Offerte dès %s · droits et taxes inclus', 'charmed-paris' ), charmed_price_plain( $threshold ) ) : __( 'Droits et taxes inclus', 'charmed-paris' ) ),
	array( __( '14 jours pour changer d’avis', 'charmed-paris' ), __( 'Rétractation en ligne, en quelques clics', 'charmed-paris' ) ),
	array( __( 'Paiement sécurisé', 'charmed-paris' ), __( 'Carte bancaire, Apple Pay, PayPal', 'charmed-paris' ) ),
	array( __( 'Prêt à offrir', 'charmed-paris' ), __( 'Boîte à bijoux, ruban, aucun prix sur le bordereau', 'charmed-paris' ) ),
);
?>
<!-- wp:group {"align":"full","className":"cp-reass","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull cp-reass">
	<!-- wp:columns {"align":"wide","style":{"spacing":{"padding":{"top":"28px","bottom":"28px"}}}} -->
	<div class="wp-block-columns alignwide" style="padding-top:28px;padding-bottom:28px">
		<?php foreach ( $cols as $c ) : ?>
		<!-- wp:column -->
		<div class="wp-block-column"><!-- wp:paragraph --><p><strong><?php echo esc_html( $c[0] ); ?></strong><?php echo esc_html( $c[1] ); ?></p><!-- /wp:paragraph --></div>
		<!-- /wp:column -->
		<?php endforeach; ?>
	</div>
	<!-- /wp:columns -->
</div>
<!-- /wp:group -->
