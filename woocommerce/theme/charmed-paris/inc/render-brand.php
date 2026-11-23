<?php
/**
 * Rendu des blocs « marque » : logo, intro écrin, bandeau défilant, packagings, messages promo, newsletter.
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

/**
 * Attributs du conteneur : get_block_wrapper_attributes() dans un bloc, construction manuelle
 * pour un shortcode.
 *
 * @param array $extra Attributs (class, id, data-*...).
 */
function charmed_wrap( array $extra = array() ): string {
	if ( class_exists( 'WP_Block_Supports' ) && null !== WP_Block_Supports::$block_to_render ) {
		return get_block_wrapper_attributes( $extra );
	}
	$out = array();
	foreach ( $extra as $k => $v ) {
		$out[] = sprintf( '%s="%s"', esc_attr( $k ), esc_attr( (string) $v ) );
	}
	return implode( ' ', $out );
}

/**
 * Marque en HTML/CSS : les parenthèses C et D encadrent « HARME », « PARIS » espacé dessous.
 *
 * @param string $class Classe supplémentaire.
 */
function charmed_wordmark_html( string $class = '' ): string {
	return '<span class="cp-wm ' . esc_attr( $class ) . '" aria-hidden="true"><span class="cp-br cp-br--l"></span><span class="cp-wm__mid">HARME</span><span class="cp-br cp-br--r"></span></span>';
}

/**
 * Bloc charmed/wordmark.
 *
 * @param array $a Attributs.
 */
function charmed_render_wordmark( array $a ): string {
	$size = max( 10, min( 120, (int) ( $a['size'] ?? 22 ) ) );
	$sub  = ! empty( $a['showParis'] ) ? '<span class="cp-wm__sub" aria-hidden="true">Paris</span>' : '';
	$tag  = ! empty( $a['tagline'] ) ? '<span class="cp-wm__tagline">' . esc_html__( 'Ouvre. Laisse-toi charmer.', 'charmed-paris' ) . '</span>' : '';
	$inner = charmed_wordmark_html() . $sub . '<span class="screen-reader-text">CHARMED PARIS</span>' . $tag;

	$attrs = charmed_wrap(
		array(
			'class' => 'cp-wordmark',
			'style' => '--cp-wm-size:' . $size . 'px',
		)
	);
	if ( ! isset( $a['link'] ) || $a['link'] ) {
		return sprintf(
			'<div %1$s><a class="cp-wordmark__link" href="%2$s" rel="home" aria-label="%3$s">%4$s</a></div>',
			$attrs,
			esc_url( home_url( '/' ) ),
			esc_attr__( 'CHARMED PARIS, accueil', 'charmed-paris' ),
			$inner
		);
	}
	return '<div ' . $attrs . '>' . $inner . '</div>';
}

/**
 * Bloc charmed/intro : l'écrin qui s'ouvre au scroll.
 *
 * Sans JS / réduction des animations / hors accueil : héros statique (logo, H1, accroche, bouton),
 * hauteur d'un écran. Sur l'accueil avec animations : mode « film » (520vh, scène collante),
 * intro.js anime le DOM et charge Three.js à la demande.
 *
 * @param array $a Attributs.
 */
function charmed_render_intro( array $a ): string {
	$film = is_front_page() || (bool) apply_filters( 'charmed_intro_film_everywhere', false );
	wp_enqueue_style( 'charmed-intro' );
	if ( $film ) {
		wp_enqueue_script( 'charmed-intro' );
	}
	$cta_url  = ! empty( $a['ctaUrl'] ) ? $a['ctaUrl'] : '#coffrets';
	$cta_text = ! empty( $a['ctaText'] ) ? $a['ctaText'] : __( 'Choisir mon coffret', 'charmed-paris' );
	$poster   = charmed_intro_poster();
	$three    = (string) apply_filters( 'charmed_three_src', charmed_asset( 'vendor/three-r128.min.js' ) . '?ver=r128' );

	$attrs = array(
		'class'           => 'cp-intro alignfull',
		'id'              => 'intro',
		'aria-labelledby' => 'cp-intro-title',
	);
	if ( $film ) {
		$attrs['data-film']  = '1';
		$attrs['data-three'] = esc_url( $three );
	}

	ob_start();
	?>
	<section <?php echo charmed_wrap( $attrs ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
		<div class="cp-intro__stage">
			<div class="cp-intro__glow" aria-hidden="true"></div>
			<?php if ( $poster ) : ?>
				<img class="cp-intro__poster" src="<?php echo esc_url( $poster ); ?>" alt="" width="1600" height="900" fetchpriority="high" decoding="async">
			<?php endif; ?>
			<canvas class="cp-intro__gl" aria-hidden="true"></canvas>
			<div class="cp-intro__ring" aria-hidden="true"></div>
			<div class="cp-intro__logo" aria-hidden="true">
				<span class="cp-br cp-br--l"></span>
				<span class="cp-intro__mid">HARME</span>
				<span class="cp-br cp-br--r"></span>
				<span class="cp-intro__paris">PARIS</span>
			</div>
			<p class="cp-intro__it cp-intro__open"><?php esc_html_e( 'Ouvre.', 'charmed-paris' ); ?></p>
			<p class="cp-intro__it cp-intro__t1"><?php esc_html_e( 'Le bijou qu’on offre.', 'charmed-paris' ); ?></p>
			<p class="cp-intro__it cp-intro__t2"><?php esc_html_e( 'Et celui qu’on s’offre.', 'charmed-paris' ); ?></p>
			<div class="cp-intro__final">
				<h1 id="cp-intro-title" class="cp-intro__title"><span class="cp-intro__final-wm">CHARMED</span> <span class="cp-intro__final-sub">PARIS</span></h1>
				<p class="cp-intro__tag"><?php esc_html_e( 'Ouvre. Laisse-toi charmer.', 'charmed-paris' ); ?></p>
				<a class="cp-btn cp-btn--ghost" href="<?php echo esc_url( $cta_url ); ?>"><?php echo esc_html( $cta_text ); ?></a>
			</div>
			<?php if ( $film ) : ?>
				<div class="cp-intro__hint" aria-hidden="true">
					<span class="cp-intro__mouse"></span>
					<span><b class="cp-desk"><?php esc_html_e( 'Descends pour ouvrir l’écrin', 'charmed-paris' ); ?></b><b class="cp-touch"><?php esc_html_e( 'Glisse vers le haut pour ouvrir l’écrin', 'charmed-paris' ); ?></b></span>
					<span class="cp-intro__chevs"><i></i><i></i></span>
				</div>
				<div class="cp-intro__prog" aria-hidden="true"><i></i></div>
			<?php endif; ?>
		</div>
	</section>
	<?php
	return (string) ob_get_clean();
}

/**
 * Bloc charmed/marquee : bandeau défilant (décoratif, une seule copie lue par les lecteurs d'écran).
 *
 * @param array $a Attributs.
 */
function charmed_render_marquee( array $a ): string {
	$raw   = ! empty( $a['words'] ) ? (string) $a['words'] : __( 'Ouvre|Offre|Garde|Laisse-toi charmer|Charmed Paris', 'charmed-paris' );
	$words = array_values( array_filter( array_map( 'trim', explode( '|', $raw ) ) ) );
	if ( ! $words ) {
		return '';
	}
	$spans = '';
	foreach ( $words as $w ) {
		$spans .= '<span>' . esc_html( $w ) . '</span>';
	}
	wp_enqueue_style( 'charmed-sections' );
	return sprintf(
		'<div %1$s><p class="screen-reader-text">%2$s</p><div class="cp-marquee__track" aria-hidden="true">%3$s%3$s</div></div>',
		charmed_wrap( array( 'class' => 'cp-marquee alignfull' ) ),
		esc_html( implode( ', ', $words ) ),
		$spans
	);
}

/**
 * Bloc charmed/packshots : photos des packagings + sélecteur (Femme / Homme / Noël).
 *
 * @param array $a Attributs.
 */
function charmed_render_packshots( array $a ): string {
	wp_enqueue_style( 'charmed-sections' );
	wp_enqueue_script( 'charmed-packshots' );

	$packs = array(
		'noel-f' => array( __( 'Noël · Femme', 'charmed-paris' ), __( 'Packaging de Noël CHARMED PARIS pour elle : boîte blanche, ruban de fête, pochette en velours, carte de Noël', 'charmed-paris' ) ),
		'f'      => array( __( 'Femme', 'charmed-paris' ), __( 'Packaging CHARMED PARIS pour elle : carton d’envoi blanc, boîte à bijoux nouée d’un ruban chocolat, pochette en velours', 'charmed-paris' ) ),
		'h'      => array( __( 'Homme', 'charmed-paris' ), __( 'Packaging CHARMED PARIS pour lui : papier noir, écrin cadre noir, pochette en cuir noir', 'charmed-paris' ) ),
		'noel-h' => array( __( 'Noël · Homme', 'charmed-paris' ), __( 'Packaging de Noël CHARMED PARIS pour lui : papier rouge, pochette en cuir noir, écrin au ruban rouge', 'charmed-paris' ) ),
	);
	$xmas = charmed_xmas_state()['packaging'];
	if ( ! $xmas ) {
		unset( $packs['noel-f'], $packs['noel-h'] );
	}
	$current = ! empty( $a['initial'] ) && isset( $packs[ $a['initial'] ] ) ? $a['initial'] : ( $xmas ? 'noel-f' : 'f' );

	$imgs    = '';
	$buttons = '';
	foreach ( $packs as $key => $p ) {
		$on    = $key === $current;
		$base  = 'img/pack/pack-' . $key;
		$full  = in_array( $key, array( 'noel-f', 'noel-h' ), true ) ? 1000 : 800;
		$imgs .= sprintf(
			'<img class="%1$s" data-pack="%2$s" src="%3$s" srcset="%3$s 600w, %4$s %5$dw" sizes="(max-width: 900px) 92vw, 560px" width="%5$d" height="%5$d" alt="%6$s" loading="lazy" decoding="async">',
			$on ? 'is-on' : '',
			esc_attr( $key ),
			esc_url( charmed_asset( $base . '-600.webp' ) ),
			esc_url( charmed_asset( $base . '.webp' ) ),
			$full,
			esc_attr( $p[1] )
		);
		$buttons .= sprintf( '<button type="button" data-pack="%1$s" aria-pressed="%2$s">%3$s</button>', esc_attr( $key ), $on ? 'true' : 'false', esc_html( $p[0] ) );
	}

	return sprintf(
		'<div %1$s><div class="cp-pack__shot">%2$s<span class="cp-pack__tag">%3$s</span></div><div class="cp-pack__switch" role="group" aria-label="%4$s">%5$s</div><p class="cp-pack__note">%6$s</p></div>',
		charmed_wrap( array( 'class' => 'cp-pack' ) ),
		$imgs,
		esc_html( $packs[ $current ][0] ),
		esc_attr__( 'Choisir le packaging', 'charmed-paris' ),
		$buttons,
		esc_html( $xmas ? __( 'Visuels de nos packagings. En période de Noël, le papier, le ruban et la carte changent ; le contenu peut légèrement varier.', 'charmed-paris' ) : __( 'Visuels de nos packagings ; le contenu peut légèrement varier.', 'charmed-paris' ) )
	);
}

/**
 * Bloc charmed/promo-notice : messages vrais et à jour (seuil lu dans WooCommerce, dates de Noël).
 *
 * @param array $a Attributs : parts (liste), variant (bar|inline|list), context (bar|product|cart).
 */
function charmed_render_promo_notice( array $a ): string {
	$parts   = array_filter( array_map( 'trim', explode( ',', (string) ( $a['parts'] ?? 'xmas,shipping,bundle' ) ) ) );
	$variant = in_array( $a['variant'] ?? 'bar', array( 'bar', 'inline', 'list' ), true ) ? $a['variant'] : 'bar';
	$context = in_array( $a['context'] ?? 'bar', array( 'bar', 'product', 'cart' ), true ) ? $a['context'] : 'bar';
	if ( ! function_exists( 'WC' ) ) {
		return '';
	}
	$msgs = charmed_promo_messages( $parts, $context );
	if ( ! $msgs ) {
		return '';
	}
	$class = 'cp-notice cp-notice--' . $variant . ( 'bar' === $variant ? ' alignfull' : '' );
	if ( 'list' === $variant ) {
		$li = '';
		foreach ( $msgs as $m ) {
			$li .= '<li>' . esc_html( $m ) . '</li>';
		}
		return '<ul ' . charmed_wrap( array( 'class' => $class ) ) . '>' . $li . '</ul>';
	}
	return '<p ' . charmed_wrap( array( 'class' => $class ) ) . '>' . esc_html( implode( ' · ', $msgs ) ) . '</p>';
}

/**
 * Bloc charmed/newsletter : formulaire POST natif (fonctionne sans JS), sans nonce pour rester
 * compatible avec le cache de page (anti-spam : champ piège + limite par IP, voir newsletter.php).
 *
 * @param array $a Attributs.
 */
function charmed_render_newsletter( array $a ): string {
	wp_enqueue_style( 'charmed-sections' );
	$eyebrow = ! empty( $a['eyebrow'] ) ? $a['eyebrow'] : __( 'Le cercle Charmed', 'charmed-paris' );
	$heading = ! empty( $a['heading'] ) ? $a['heading'] : __( 'Les nouvelles parures, en avant-première', 'charmed-paris' );
	$text    = ! empty( $a['text'] ) ? $a['text'] : __( 'Une lettre par mois, pas plus. Désinscription en un clic.', 'charmed-paris' );

	// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- simple affichage d'état.
	$state = isset( $_GET['cp_news'] ) ? sanitize_key( wp_unslash( $_GET['cp_news'] ) ) : '';
	$privacy = get_privacy_policy_url();
	$back    = is_singular() ? (string) get_permalink() : home_url( '/' );

	ob_start();
	?>
	<section <?php echo charmed_wrap( array( 'class' => 'cp-news alignfull', 'id' => 'news' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
		<div class="cp-wrap">
			<p class="cp-eyebrow"><?php echo esc_html( $eyebrow ); ?></p>
			<h2 class="cp-news__title"><?php echo esc_html( $heading ); ?></h2>
			<p class="cp-news__text"><?php echo esc_html( $text ); ?></p>
			<?php if ( 'ok' === $state ) : ?>
				<p class="cp-news__ok" role="status"><?php esc_html_e( 'Bienvenue dans le cercle. Vérifie ta boîte mail pour confirmer ton inscription.', 'charmed-paris' ); ?></p>
			<?php else : ?>
				<?php if ( 'err' === $state ) : ?>
					<p class="cp-news__err" role="alert"><?php esc_html_e( 'Saisis une adresse e-mail valide.', 'charmed-paris' ); ?></p>
				<?php endif; ?>
				<form class="cp-news__form" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
					<span class="cp-br cp-br--l" aria-hidden="true"></span>
					<label class="screen-reader-text" for="cp-news-mail"><?php esc_html_e( 'Ton e-mail', 'charmed-paris' ); ?></label>
					<input id="cp-news-mail" name="email" type="email" required autocomplete="email" placeholder="<?php esc_attr_e( 'ton e-mail', 'charmed-paris' ); ?>">
					<input type="hidden" name="action" value="charmed_newsletter">
					<input type="hidden" name="back" value="<?php echo esc_url( $back ); ?>">
					<input type="hidden" name="lang" value="<?php echo esc_attr( determine_locale() ); ?>">
					<span class="cp-hp" aria-hidden="true"><label for="cp-news-web">Website</label><input id="cp-news-web" name="website" type="text" tabindex="-1" autocomplete="off"></span>
					<button type="submit"><?php esc_html_e( 'Je m’inscris', 'charmed-paris' ); ?></button>
					<span class="cp-br cp-br--r" aria-hidden="true"></span>
				</form>
				<p class="cp-news__legal">
					<?php esc_html_e( 'En t’inscrivant, tu acceptes de recevoir nos e-mails. Tu peux te désinscrire à tout moment.', 'charmed-paris' ); ?>
					<?php if ( $privacy ) : ?>
						<a href="<?php echo esc_url( $privacy ); ?>"><?php esc_html_e( 'Politique de confidentialité', 'charmed-paris' ); ?></a>
					<?php endif; ?>
				</p>
			<?php endif; ?>
		</div>
	</section>
	<?php
	return (string) ob_get_clean();
}
