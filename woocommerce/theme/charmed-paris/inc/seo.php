<?php
/**
 * Données structurées produit : marque CHARMED PARIS, MPN = SKU, pas de GTIN/EAN
 * (Branvas ne fournit aucun code-barres ; ne pas en inventer).
 *
 * Pour Google Merchant Center : marque « CHARMED PARIS » + MPN (SKU), ou « identifier_exists = no »
 * (voir tech/installation.md). Le champ natif WooCommerce « GTIN, UPC, EAN ou ISBN » reste vide.
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

add_filter(
	'woocommerce_structured_data_product',
	static function ( $markup, $product ) {
		if ( ! $product instanceof WC_Product ) {
			return $markup;
		}
		$markup['brand'] = array(
			'@type' => 'Brand',
			'name'  => 'CHARMED PARIS',
		);
		$sku = $product->get_sku();
		if ( $sku && empty( $markup['gtin'] ) && empty( $markup['gtin13'] ) ) {
			$markup['mpn'] = $sku;
		}
		return $markup;
	},
	10,
	2
);
