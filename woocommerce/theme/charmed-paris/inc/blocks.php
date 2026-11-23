<?php
/**
 * Blocs dynamiques charmed/* (rendu serveur) + shortcodes équivalents.
 *
 * Pas d'étape de build : les blocs sont déclarés en PHP ; l'éditeur les affiche via
 * ServerSideRender avec un panneau de réglages généré depuis leurs attributs
 * (assets/js/editor-blocks.js).
 *
 * Shortcodes (pour une page classique, un constructeur ou un widget) :
 *   [charmed_coffrets category="coffrets-accueil" limit="8"]
 *   [charmed_coffrets skus="JSGRQR,JS1AQ5,JS3GGZ"]
 *   [charmed_file_parures category="parures" limit="9"]
 *   [charmed_univers slugs="sculpture,eclat,couleur-precieuse,joaillerie-925,mixte"]
 *   [charmed_promo parts="xmas,shipping,bundle"]   [charmed_promo parts="delivery,ddp,xmas" variant="list" context="product"]
 *   [charmed_newsletter]   [charmed_wordmark size="26"]   [charmed_language_switcher]
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

/**
 * Définitions des blocs.
 */
function charmed_block_definitions(): array {
	$selection = array(
		'category' => array(
			'type'    => 'string',
			'default' => '',
			'label'   => __( 'Catégorie(s) produit (slugs, séparés par des virgules)', 'charmed-paris' ),
		),
		'ids'      => array(
			'type'    => 'string',
			'default' => '',
			'label'   => __( 'Ou IDs produits (ordre conservé)', 'charmed-paris' ),
		),
		'skus'     => array(
			'type'    => 'string',
			'default' => '',
			'label'   => __( 'Ou SKU (ex. JSGRQR,JS1AQ5)', 'charmed-paris' ),
		),
		'orderby'  => array(
			'type'    => 'string',
			'default' => 'menu_order',
			'label'   => __( 'Tri (menu_order, date, price, popularity, rand)', 'charmed-paris' ),
		),
	);

	return array(
		'wordmark'          => array(
			'title'       => __( 'Logo CHARMED PARIS', 'charmed-paris' ),
			'description' => __( 'Wordmark : les parenthèses C et D encadrent HARME.', 'charmed-paris' ),
			'icon'        => 'star-filled',
			'render'      => 'charmed_render_wordmark',
			'attributes'  => array(
				'size'      => array( 'type' => 'number', 'default' => 22, 'label' => __( 'Taille (px)', 'charmed-paris' ) ),
				'showParis' => array( 'type' => 'boolean', 'default' => true, 'label' => __( 'Afficher PARIS', 'charmed-paris' ) ),
				'link'      => array( 'type' => 'boolean', 'default' => true, 'label' => __( 'Lien vers l’accueil', 'charmed-paris' ) ),
				'tagline'   => array( 'type' => 'boolean', 'default' => false, 'label' => __( 'Afficher la signature', 'charmed-paris' ) ),
			),
		),
		'intro'             => array(
			'title'       => __( 'Intro écrin', 'charmed-paris' ),
			'description' => __( 'Ouverture de l’écrin au scroll (animation sur l’accueil uniquement).', 'charmed-paris' ),
			'icon'        => 'format-video',
			'render'      => 'charmed_render_intro',
			'styles'      => array( 'charmed-intro' ),
			'attributes'  => array(
				'ctaText' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Texte du bouton', 'charmed-paris' ) ),
				'ctaUrl'  => array( 'type' => 'string', 'default' => '#coffrets', 'label' => __( 'Lien du bouton', 'charmed-paris' ) ),
			),
		),
		'coffrets'          => array(
			'title'       => __( 'Coffrets (carrousel)', 'charmed-paris' ),
			'description' => __( 'Carrousel de coffrets qui s’ouvrent sur les vrais produits WooCommerce.', 'charmed-paris' ),
			'icon'        => 'products',
			'render'      => 'charmed_render_coffrets',
			'styles'      => array( 'charmed-sections' ),
			'attributes'  => $selection + array(
				'limit'   => array( 'type' => 'number', 'default' => 8, 'label' => __( 'Nombre de coffrets', 'charmed-paris' ) ),
				'eyebrow' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Surtitre (vide = automatique)', 'charmed-paris' ) ),
				'heading' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Titre', 'charmed-paris' ) ),
				'intro'   => array( 'type' => 'string', 'default' => '', 'label' => __( 'Texte', 'charmed-paris' ) ),
			),
		),
		'file-parures'      => array(
			'title'       => __( 'La file des parures', 'charmed-paris' ),
			'description' => __( 'Vues Une / La file / Toutes, avec étiquette, sur les vrais produits.', 'charmed-paris' ),
			'icon'        => 'grid-view',
			'render'      => 'charmed_render_file_parures',
			'styles'      => array( 'charmed-sections' ),
			'attributes'  => $selection + array(
				'limit'   => array( 'type' => 'number', 'default' => 9, 'label' => __( 'Nombre de parures', 'charmed-paris' ) ),
				'heading' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Titre', 'charmed-paris' ) ),
			),
		),
		'univers'           => array(
			'title'       => __( 'Univers (catégories)', 'charmed-paris' ),
			'description' => __( 'Les univers = catégories produit WooCommerce, avec leur image.', 'charmed-paris' ),
			'icon'        => 'category',
			'render'      => 'charmed_render_univers',
			'styles'      => array( 'charmed-sections' ),
			'attributes'  => array(
				'slugs'   => array( 'type' => 'string', 'default' => 'sculpture,eclat,couleur-precieuse,joaillerie-925,mixte', 'label' => __( 'Catégories (slugs, dans l’ordre)', 'charmed-paris' ) ),
				'parent'  => array( 'type' => 'string', 'default' => '', 'label' => __( 'Ou catégorie parente (slug)', 'charmed-paris' ) ),
				'eyebrow' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Surtitre', 'charmed-paris' ) ),
				'heading' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Titre', 'charmed-paris' ) ),
			),
		),
		'marquee'           => array(
			'title'       => __( 'Bandeau défilant', 'charmed-paris' ),
			'description' => __( 'Mots séparés par |. Animation coupée si réduction des animations.', 'charmed-paris' ),
			'icon'        => 'leftright',
			'render'      => 'charmed_render_marquee',
			'styles'      => array( 'charmed-sections' ),
			'attributes'  => array(
				'words' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Mots (séparés par |, vide = défaut traduit)', 'charmed-paris' ) ),
			),
		),
		'packshots'         => array(
			'title'       => __( 'Packagings', 'charmed-paris' ),
			'description' => __( 'Photos des packagings avec sélecteur Femme / Homme / Noël (Noël affiché seulement pendant la période).', 'charmed-paris' ),
			'icon'        => 'archive',
			'render'      => 'charmed_render_packshots',
			'styles'      => array( 'charmed-sections' ),
			'attributes'  => array(
				'initial' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Packaging affiché d’abord (f, h, noel-f, noel-h)', 'charmed-paris' ) ),
			),
		),
		'promo-notice'      => array(
			'title'       => __( 'Messages promo et livraison', 'charmed-paris' ),
			'description' => __( 'Seuil de livraison offerte (lu dans WooCommerce), remise 2e parure, délai réel, droits inclus, date limite de Noël.', 'charmed-paris' ),
			'icon'        => 'megaphone',
			'render'      => 'charmed_render_promo_notice',
			'styles'      => array(),
			'attributes'  => array(
				'parts'   => array( 'type' => 'string', 'default' => 'xmas,shipping,bundle', 'label' => __( 'Messages (xmas, shipping, bundle, delivery, ddp)', 'charmed-paris' ) ),
				'variant' => array( 'type' => 'string', 'default' => 'bar', 'label' => __( 'Style (bar, inline, list)', 'charmed-paris' ) ),
				'context' => array( 'type' => 'string', 'default' => 'bar', 'label' => __( 'Contexte (bar, product, cart)', 'charmed-paris' ) ),
			),
		),
		'newsletter'        => array(
			'title'       => __( 'Newsletter', 'charmed-paris' ),
			'description' => __( 'Inscription (fonctionne sans JS). À brancher sur votre outil d’e-mailing : voir tech/installation.md.', 'charmed-paris' ),
			'icon'        => 'email',
			'render'      => 'charmed_render_newsletter',
			'styles'      => array( 'charmed-sections' ),
			'attributes'  => array(
				'eyebrow' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Surtitre', 'charmed-paris' ) ),
				'heading' => array( 'type' => 'string', 'default' => '', 'label' => __( 'Titre (n’annoncez une remise que si le code existe)', 'charmed-paris' ) ),
				'text'    => array( 'type' => 'string', 'default' => '', 'label' => __( 'Texte', 'charmed-paris' ) ),
			),
		),
		'language-switcher' => array(
			'title'       => __( 'Sélecteur de langue', 'charmed-paris' ),
			'description' => __( 'FR / EN via TranslatePress, Polylang ou WPML (rien ne s’affiche sans plugin multilingue).', 'charmed-paris' ),
			'icon'        => 'translation',
			'render'      => 'charmed_render_language_switcher',
			'styles'      => array(),
			'attributes'  => array(),
		),
	);
}

/**
 * Enregistre les blocs et les shortcodes.
 */
add_action(
	'init',
	static function () {
		wp_register_script(
			'charmed-blocks-editor',
			charmed_asset( 'js/editor-blocks.js' ),
			array( 'wp-blocks', 'wp-element', 'wp-block-editor', 'wp-components', 'wp-server-side-render' ),
			charmed_asset_ver( 'js/editor-blocks.js' ),
			true
		);

		$editor = array();
		foreach ( charmed_block_definitions() as $slug => $def ) {
			$attributes = array();
			$labels     = array();
			foreach ( $def['attributes'] as $key => $attr ) {
				$labels[ $key ]     = $attr['label'];
				$attributes[ $key ] = array(
					'type'    => $attr['type'],
					'default' => $attr['default'],
				);
			}
			$render = $def['render'];
			register_block_type(
				'charmed/' . $slug,
				array(
					'api_version'     => 3,
					'title'           => $def['title'],
					'description'     => $def['description'],
					'category'        => 'theme',
					'icon'            => $def['icon'],
					'attributes'      => $attributes,
					'supports'        => array(
						'html'      => false,
						'align'     => array( 'wide', 'full' ),
						'className' => true,
					),
					'editor_script'   => 'charmed-blocks-editor',
					'style_handles'   => $def['styles'] ?? array(),
					'render_callback' => static function ( $attrs ) use ( $render ) {
						return call_user_func( $render, (array) $attrs );
					},
				)
			);
			$editor[] = array(
				'name'        => 'charmed/' . $slug,
				'title'       => $def['title'],
				'description' => $def['description'],
				'icon'        => $def['icon'],
				'attributes'  => $attributes,
				'labels'      => $labels,
			);

			// Shortcode équivalent : [charmed_coffrets], [charmed_file_parures]...
			add_shortcode(
				'charmed_' . str_replace( '-', '_', $slug ),
				static function ( $atts ) use ( $render, $attributes ) {
					$defaults = array();
					foreach ( $attributes as $key => $attr ) {
						$defaults[ strtolower( $key ) ] = $attr['default'];
					}
					$atts  = shortcode_atts( $defaults, (array) $atts );
					$final = array();
					foreach ( $attributes as $key => $attr ) {
						$value = $atts[ strtolower( $key ) ];
						if ( 'boolean' === $attr['type'] ) {
							$value = filter_var( $value, FILTER_VALIDATE_BOOLEAN );
						} elseif ( 'number' === $attr['type'] ) {
							$value = (int) $value;
						}
						$final[ $key ] = $value;
					}
					return call_user_func( $render, $final );
				}
			);
		}
		add_shortcode( 'charmed_promo', static fn( $atts ) => do_shortcode( '[charmed_promo_notice ' . implode( ' ', array_map( static fn( $k, $v ) => sprintf( '%s="%s"', sanitize_key( (string) $k ), esc_attr( (string) $v ) ), array_keys( (array) $atts ), (array) $atts ) ) . ']' ) );

		wp_localize_script(
			'charmed-blocks-editor',
			'charmedBlocks',
			array(
				'blocks' => $editor,
				'i18n'   => array(
					'settings' => __( 'Réglages', 'charmed-paris' ),
				),
			)
		);
	},
	20
);
