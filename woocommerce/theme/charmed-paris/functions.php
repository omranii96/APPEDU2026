<?php
/**
 * CHARMED PARIS — fonctions du thème.
 *
 * Le code est découpé par responsabilité dans inc/ :
 *  - setup.php       supports du thème, traductions, tailles d'images, catégories de patterns
 *  - settings.php    réglages (WooCommerce > Réglages > Produits > CHARMED PARIS)
 *  - assets.php      styles/scripts, préchargements, allègement des assets WooCommerce
 *  - products.php    lecture des vrais produits WooCommerce pour les sections vitrines + champs produit
 *  - commerce.php    remise « 2e parure », livraison offerte, téléphone obligatoire, délais, stock, Noël
 *  - blocks.php      blocs dynamiques charmed/* (rendu serveur) + shortcodes équivalents
 *  - render-*.php    fonctions de rendu des blocs
 *  - newsletter.php  traitement du formulaire d'inscription
 *  - seo.php         données structurées produit (marque, MPN, pas d'EAN)
 *  - i18n.php        sélecteur de langue (TranslatePress / Polylang / WPML)
 *  - withdrawal.php  bouton de rétractation en ligne (L221-21) — copiable en mu-plugin
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

define( 'CHARMED_VERSION', '0.2.0' );
define( 'CHARMED_DIR', get_template_directory() );
define( 'CHARMED_URI', get_template_directory_uri() );

$charmed_includes = array(
	'setup',
	'settings',
	'assets',
	'products',
	'commerce',
	'render-brand',
	'render-catalog',
	'blocks',
	'newsletter',
	'seo',
	'i18n',
	'withdrawal', // Ignoré s'il est déjà chargé comme mu-plugin.
);

foreach ( $charmed_includes as $charmed_file ) {
	require_once CHARMED_DIR . '/inc/' . $charmed_file . '.php';
}
unset( $charmed_includes, $charmed_file );
