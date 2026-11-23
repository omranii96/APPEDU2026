<?php
/**
 * Multilingue : sélecteur de langue compatible TranslatePress (recommandé), Polylang et WPML.
 *
 * Les balises hreflang, les URL /en/ et la traduction des contenus (produits, pages, menus)
 * sont gérées par le plugin ; le thème fournit ses chaînes en gettext (text domain charmed-paris,
 * languages/charmed-paris-en_US.mo / -en_GB.mo) et ce sélecteur.
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

/**
 * Langues disponibles, normalisées : [ [ code, name, url, current ] ].
 */
function charmed_languages(): array {
	$out = array();

	// TranslatePress (API publique trp_custom_language_switcher()).
	if ( function_exists( 'trp_custom_language_switcher' ) ) {
		$current = get_locale();
		foreach ( (array) trp_custom_language_switcher() as $code => $lang ) {
			$out[] = array(
				'code'    => strtolower( (string) ( $lang['short_language_name'] ?? substr( (string) $code, 0, 2 ) ) ),
				'name'    => (string) ( $lang['language_name'] ?? $code ),
				'url'     => (string) ( $lang['current_page_url'] ?? '' ),
				'current' => ( $lang['language_code'] ?? $code ) === $current,
			);
		}
		return $out;
	}

	// Polylang.
	if ( function_exists( 'pll_the_languages' ) ) {
		$langs = pll_the_languages(
			array(
				'raw'           => 1,
				'hide_if_empty' => 0,
			)
		);
		foreach ( (array) $langs as $lang ) {
			$out[] = array(
				'code'    => (string) $lang['slug'],
				'name'    => (string) $lang['name'],
				'url'     => (string) $lang['url'],
				'current' => ! empty( $lang['current_lang'] ),
			);
		}
		return $out;
	}

	// WPML.
	$wpml = apply_filters( 'wpml_active_languages', null, array( 'skip_missing' => 0 ) );
	if ( is_array( $wpml ) ) {
		foreach ( $wpml as $lang ) {
			$out[] = array(
				'code'    => (string) $lang['code'],
				'name'    => (string) $lang['native_name'],
				'url'     => (string) $lang['url'],
				'current' => ! empty( $lang['active'] ),
			);
		}
	}
	return $out;
}

/**
 * Bloc charmed/language-switcher : « FR · EN », langue courante non cliquable.
 */
function charmed_render_language_switcher(): string {
	$langs = charmed_languages();
	if ( count( $langs ) < 2 ) {
		return '';
	}
	$items = '';
	foreach ( $langs as $l ) {
		$code = strtoupper( substr( $l['code'], 0, 2 ) );
		if ( $l['current'] ) {
			$items .= sprintf( '<li><span aria-current="true" lang="%1$s">%2$s</span></li>', esc_attr( $l['code'] ), esc_html( $code ) );
		} else {
			$items .= sprintf( '<li><a href="%1$s" hreflang="%2$s" lang="%2$s" title="%3$s">%4$s</a></li>', esc_url( $l['url'] ), esc_attr( $l['code'] ), esc_attr( $l['name'] ), esc_html( $code ) );
		}
	}
	return sprintf(
		'<nav %1$s aria-label="%2$s"><ul>%3$s</ul></nav>',
		charmed_wrap( array( 'class' => 'cp-lang' ) ),
		esc_attr__( 'Langue', 'charmed-paris' ),
		$items
	);
}
