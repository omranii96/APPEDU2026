<?php
/**
 * Formulaire newsletter (admin-post.php, sans JS).
 *
 * Le thème ne stocke aucune adresse : il déclenche l'action « charmed_newsletter_subscribe »
 * à brancher sur l'outil d'e-mailing (Brevo, hébergé en France, recommandé ; ou MailPoet).
 * Exemple (mu-plugin) :
 *   add_action( 'charmed_newsletter_subscribe', function ( $email, $locale ) {
 *       // Appel API Brevo « double opt-in » avec la liste FR ou EN selon $locale.
 *   }, 10, 2 );
 * Sans branchement, l'administrateur reçoit l'inscription par e-mail (solution d'attente).
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

/**
 * Traite l'inscription.
 */
function charmed_newsletter_handle(): void {
	// phpcs:disable WordPress.Security.NonceVerification.Missing -- formulaire public mis en cache : anti-spam par champ piège + limite.
	$back = isset( $_POST['back'] ) ? esc_url_raw( wp_unslash( $_POST['back'] ) ) : home_url( '/' );
	$back = wp_validate_redirect( $back, home_url( '/' ) );

	if ( ! empty( $_POST['website'] ) ) { // Champ piège rempli : robot.
		wp_safe_redirect( add_query_arg( 'cp_news', 'ok', $back ) . '#news' );
		exit;
	}

	$email  = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) ) : '';
	$locale = isset( $_POST['lang'] ) ? sanitize_text_field( wp_unslash( $_POST['lang'] ) ) : get_locale();
	// phpcs:enable

	if ( ! is_email( $email ) ) {
		wp_safe_redirect( add_query_arg( 'cp_news', 'err', $back ) . '#news' );
		exit;
	}

	// Limite : 5 inscriptions par heure et par IP (empreinte hachée, rien n'est conservé au-delà).
	$ip   = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
	$key  = 'charmed_nl_' . md5( $ip . wp_salt( 'nonce' ) );
	$hits = (int) get_transient( $key );
	if ( $hits >= 5 ) {
		wp_safe_redirect( add_query_arg( 'cp_news', 'ok', $back ) . '#news' );
		exit;
	}
	set_transient( $key, $hits + 1, HOUR_IN_SECONDS );

	if ( has_action( 'charmed_newsletter_subscribe' ) ) {
		do_action( 'charmed_newsletter_subscribe', $email, $locale );
	} else {
		wp_mail(
			get_option( 'admin_email' ),
			__( '[CHARMED PARIS] Nouvelle inscription newsletter', 'charmed-paris' ),
			sprintf(
				/* translators: 1: email, 2: locale, 3: date */
				__( "Adresse : %1\$s\nLangue : %2\$s\nDate : %3\$s\n\nÀ importer dans l'outil d'e-mailing (double opt-in recommandé).", 'charmed-paris' ),
				$email,
				$locale,
				wp_date( 'Y-m-d H:i:s T' )
			)
		);
	}

	wp_safe_redirect( add_query_arg( 'cp_news', 'ok', $back ) . '#news' );
	exit;
}
add_action( 'admin_post_nopriv_charmed_newsletter', 'charmed_newsletter_handle' );
add_action( 'admin_post_charmed_newsletter', 'charmed_newsletter_handle' );
