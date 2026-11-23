<?php
/**
 * Fonction de rétractation en ligne (art. L221-21 du Code de la consommation, en vigueur
 * depuis le 19 juin 2026 — ordonnance 2026-2 ; libellés exacts à vérifier dans le décret 2026-3,
 * ils sont donc configurables).
 *
 * Module autonome : chargé par le thème, il peut aussi être copié tel quel dans
 * wp-content/mu-plugins/ pour survivre à un changement de thème (recommandé en production) ;
 * le thème ne le recharge pas s'il est déjà actif.
 *
 * Fonctionnement :
 *  - lien « Me rétracter » (libellé configurable) dans le pied de page (bloc charmed/withdrawal-link
 *    ou shortcode [charmed_withdrawal_link]) et dans Mon compte > Commandes (bouton par commande) ;
 *  - page contenant [charmed_withdrawal_form] : n° de commande, e-mail, nom, articles concernés ;
 *  - envoi : e-mail au marchand, accusé de réception horodaté à la cliente (copie de la déclaration,
 *    support durable), note privée sur la commande, et trace dans « WooCommerce > Rétractations ».
 *
 * Réglages : WooCommerce > Réglages > Avancé > Rétractation.
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

if ( defined( 'CHARMED_WITHDRAWAL_LOADED' ) ) {
	return;
}
define( 'CHARMED_WITHDRAWAL_LOADED', true );

/**
 * Libellés et réglages.
 */
function charmed_withdrawal_label(): string {
	$v = trim( (string) get_option( 'charmed_withdrawal_label', '' ) );
	return '' !== $v ? $v : __( 'Me rétracter', 'charmed-paris' );
}

function charmed_withdrawal_confirm_label(): string {
	$v = trim( (string) get_option( 'charmed_withdrawal_confirm_label', '' ) );
	return '' !== $v ? $v : __( 'Confirmer ma rétractation', 'charmed-paris' );
}

function charmed_withdrawal_merchant_email(): string {
	$v = sanitize_email( (string) get_option( 'charmed_withdrawal_email', '' ) );
	if ( $v ) {
		return $v;
	}
	$from = sanitize_email( (string) get_option( 'woocommerce_email_from_address', '' ) );
	return $from ? $from : (string) get_option( 'admin_email' );
}

/**
 * URL de la page de rétractation (option, sinon page au slug « retractation »).
 *
 * @param WC_Order|null $order Commande à préremplir.
 */
function charmed_withdrawal_url( $order = null ): string {
	$page_id = (int) get_option( 'charmed_withdrawal_page_id', 0 );
	if ( ! $page_id ) {
		$page    = get_page_by_path( 'retractation' );
		$page_id = $page ? (int) $page->ID : 0;
	}
	if ( ! $page_id || 'publish' !== get_post_status( $page_id ) ) {
		return '';
	}
	$url = (string) get_permalink( $page_id );
	if ( $order instanceof WC_Order ) {
		$url = add_query_arg(
			array(
				'order' => $order->get_id(),
				'key'   => $order->get_order_key(),
			),
			$url
		);
	}
	return (string) apply_filters( 'charmed_withdrawal_url', $url, $order );
}

/*
 * Réglages (WooCommerce > Réglages > Avancé > Rétractation).
 */
add_filter(
	'woocommerce_get_sections_advanced',
	static function ( $sections ) {
		$sections['charmed_withdrawal'] = __( 'Rétractation', 'charmed-paris' );
		return $sections;
	}
);
add_filter(
	'woocommerce_get_settings_advanced',
	static function ( $settings, $section ) {
		if ( 'charmed_withdrawal' !== $section ) {
			return $settings;
		}
		return array(
			array(
				'title' => __( 'Fonction de rétractation en ligne', 'charmed-paris' ),
				'type'  => 'title',
				'desc'  => __( 'Obligatoire depuis le 19 juin 2026 (L221-21). Vérifiez les libellés exacts imposés par le décret d’application avant la mise en ligne.', 'charmed-paris' ),
				'id'    => 'charmed_withdrawal',
			),
			array(
				'title'    => __( 'Page du formulaire', 'charmed-paris' ),
				'id'       => 'charmed_withdrawal_page_id',
				'type'     => 'single_select_page',
				'class'    => 'wc-page-search',
				'desc_tip' => __( 'Page contenant le shortcode [charmed_withdrawal_form]. À exclure du cache de page.', 'charmed-paris' ),
			),
			array(
				'title'       => __( 'Libellé du lien / bouton', 'charmed-paris' ),
				'id'          => 'charmed_withdrawal_label',
				'type'        => 'text',
				'placeholder' => __( 'Me rétracter', 'charmed-paris' ),
			),
			array(
				'title'       => __( 'Libellé du bouton de confirmation', 'charmed-paris' ),
				'id'          => 'charmed_withdrawal_confirm_label',
				'type'        => 'text',
				'placeholder' => __( 'Confirmer ma rétractation', 'charmed-paris' ),
			),
			array(
				'title'       => __( 'E-mail du marchand', 'charmed-paris' ),
				'id'          => 'charmed_withdrawal_email',
				'type'        => 'email',
				'placeholder' => charmed_withdrawal_merchant_email(),
			),
			array(
				'type' => 'sectionend',
				'id'   => 'charmed_withdrawal',
			),
		);
	},
	10,
	2
);

/*
 * Trace des demandes (type de contenu privé, lecture seule dans l'admin).
 */
add_action(
	'init',
	static function () {
		register_post_type(
			'charmed_withdrawal',
			array(
				'labels'          => array(
					'name'          => __( 'Rétractations', 'charmed-paris' ),
					'singular_name' => __( 'Rétractation', 'charmed-paris' ),
				),
				'public'          => false,
				'show_ui'         => true,
				'show_in_menu'    => class_exists( 'WooCommerce' ) ? 'woocommerce' : true,
				'show_in_rest'    => false,
				'supports'        => array( 'title', 'editor' ),
				'capability_type' => 'shop_order',
				'map_meta_cap'    => true,
				'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
			)
		);
	}
);

/**
 * Lien de rétractation (pied de page).
 */
function charmed_render_withdrawal_link(): string {
	$url = charmed_withdrawal_url();
	if ( ! $url ) {
		return current_user_can( 'manage_woocommerce' ) ? '<p class="cp-admin-note">' . esc_html__( 'Rétractation : créez la page du formulaire (WooCommerce > Réglages > Avancé > Rétractation).', 'charmed-paris' ) . '</p>' : '';
	}
	$attrs = function_exists( 'charmed_wrap' ) ? charmed_wrap( array( 'class' => 'cp-withdrawal-link' ) ) : 'class="cp-withdrawal-link"';
	return sprintf( '<p %1$s><a href="%2$s">%3$s</a></p>', $attrs, esc_url( $url ), esc_html( charmed_withdrawal_label() ) );
}
add_shortcode( 'charmed_withdrawal_link', 'charmed_render_withdrawal_link' );

/**
 * La commande est-elle encore concernée ? (Délai légal : 14 jours après réception ; on laisse une
 * marge large car la date de livraison n'est pas connue : 90 jours après la commande, filtrable.)
 *
 * @param WC_Order $order Commande.
 */
function charmed_withdrawal_order_eligible( WC_Order $order ): bool {
	$ok      = in_array( $order->get_status(), array( 'processing', 'completed', 'on-hold' ), true );
	$created = $order->get_date_created();
	if ( $ok && $created ) {
		$ok = ( time() - $created->getTimestamp() ) <= (int) apply_filters( 'charmed_withdrawal_max_days', 90 ) * DAY_IN_SECONDS;
	}
	return (bool) apply_filters( 'charmed_withdrawal_order_eligible', $ok, $order );
}

// Mon compte > Commandes : bouton par commande.
add_filter(
	'woocommerce_my_account_my_orders_actions',
	static function ( $actions, $order ) {
		if ( $order instanceof WC_Order && charmed_withdrawal_order_eligible( $order ) ) {
			$url = charmed_withdrawal_url( $order );
			if ( $url ) {
				$actions['charmed-withdraw'] = array(
					'url'  => $url,
					'name' => charmed_withdrawal_label(),
				);
			}
		}
		return $actions;
	},
	10,
	2
);

// Détail d'une commande (Mon compte et page de confirmation).
add_action(
	'woocommerce_order_details_after_order_table',
	static function ( $order ) {
		if ( $order instanceof WC_Order && is_account_page() && charmed_withdrawal_order_eligible( $order ) ) {
			$url = charmed_withdrawal_url( $order );
			if ( $url ) {
				printf( '<p class="cp-withdrawal-order"><a class="button" href="%1$s">%2$s</a></p>', esc_url( $url ), esc_html( charmed_withdrawal_label() ) );
			}
		}
	}
);

/**
 * Formulaire [charmed_withdrawal_form].
 */
function charmed_withdrawal_form(): string {
	// phpcs:disable WordPress.Security.NonceVerification.Recommended -- lecture de paramètres d'affichage.
	if ( isset( $_GET['cp_withdrawal'] ) && 'sent' === $_GET['cp_withdrawal'] ) {
		$ref = isset( $_GET['ref'] ) ? sanitize_text_field( wp_unslash( $_GET['ref'] ) ) : '';
		return '<div class="cp-withdrawal cp-withdrawal--sent" role="status"><p><strong>' . esc_html__( 'Ta demande de rétractation est enregistrée.', 'charmed-paris' ) . '</strong></p><p>' . esc_html(
			sprintf(
				/* translators: %s: reference */
				__( 'Référence : %s. Un accusé de réception daté vient de t’être envoyé par e-mail. Nous revenons vers toi avec les modalités de retour.', 'charmed-paris' ),
				$ref
			)
		) . '</p></div>';
	}
	$error = isset( $_GET['cp_withdrawal'] ) && 'error' === $_GET['cp_withdrawal'];

	$order = null;
	if ( isset( $_GET['order'], $_GET['key'] ) ) {
		$candidate = wc_get_order( absint( $_GET['order'] ) );
		if ( $candidate instanceof WC_Order && hash_equals( $candidate->get_order_key(), sanitize_text_field( wp_unslash( $_GET['key'] ) ) ) ) {
			$order = $candidate;
		}
	}
	// phpcs:enable

	$number = $order ? $order->get_order_number() : '';
	$email  = $order ? $order->get_billing_email() : ( is_user_logged_in() ? wp_get_current_user()->user_email : '' );
	$name   = $order ? trim( $order->get_billing_first_name() . ' ' . $order->get_billing_last_name() ) : '';

	ob_start();
	?>
	<form class="cp-withdrawal" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
		<?php if ( $error ) : ?>
			<p class="cp-withdrawal__error" role="alert"><?php esc_html_e( 'Merci de renseigner ton nom, ton e-mail et ton numéro de commande.', 'charmed-paris' ); ?></p>
		<?php endif; ?>
		<p><?php esc_html_e( 'Tu disposes de 14 jours après la réception de ta commande pour te rétracter, sans avoir à te justifier.', 'charmed-paris' ); ?></p>
		<p>
			<label for="cpw-number"><?php esc_html_e( 'Numéro de commande', 'charmed-paris' ); ?> *</label>
			<input id="cpw-number" name="order_number" type="text" required value="<?php echo esc_attr( $number ); ?>">
		</p>
		<p>
			<label for="cpw-email"><?php esc_html_e( 'E-mail utilisé pour la commande', 'charmed-paris' ); ?> *</label>
			<input id="cpw-email" name="email" type="email" required autocomplete="email" value="<?php echo esc_attr( $email ); ?>">
		</p>
		<p>
			<label for="cpw-name"><?php esc_html_e( 'Nom et prénom', 'charmed-paris' ); ?> *</label>
			<input id="cpw-name" name="name" type="text" required autocomplete="name" value="<?php echo esc_attr( $name ); ?>">
		</p>
		<fieldset>
			<legend><?php esc_html_e( 'Articles concernés', 'charmed-paris' ); ?></legend>
			<?php if ( $order ) : ?>
				<?php foreach ( $order->get_items() as $item_id => $item ) : ?>
					<label class="cp-withdrawal__item"><input type="checkbox" name="items[]" value="<?php echo esc_attr( $item->get_name() . ' × ' . $item->get_quantity() ); ?>" checked> <?php echo esc_html( $item->get_name() . ' × ' . $item->get_quantity() ); ?></label>
				<?php endforeach; ?>
			<?php else : ?>
				<label class="screen-reader-text" for="cpw-items"><?php esc_html_e( 'Articles concernés', 'charmed-paris' ); ?></label>
				<textarea id="cpw-items" name="items_text" rows="3" placeholder="<?php esc_attr_e( 'Toute la commande, ou les parures concernées', 'charmed-paris' ); ?>"></textarea>
			<?php endif; ?>
		</fieldset>
		<p>
			<label for="cpw-msg"><?php esc_html_e( 'Commentaire (facultatif)', 'charmed-paris' ); ?></label>
			<textarea id="cpw-msg" name="message" rows="3"></textarea>
		</p>
		<input type="hidden" name="action" value="charmed_withdrawal">
		<input type="hidden" name="order_id" value="<?php echo esc_attr( $order ? (string) $order->get_id() : '' ); ?>">
		<input type="hidden" name="back" value="<?php echo esc_url( (string) get_permalink() ); ?>">
		<span class="cp-hp" aria-hidden="true"><label for="cpw-web">Website</label><input id="cpw-web" name="website" type="text" tabindex="-1" autocomplete="off"></span>
		<p><button type="submit" class="wp-element-button"><?php echo esc_html( charmed_withdrawal_confirm_label() ); ?></button></p>
	</form>
	<?php
	return (string) ob_get_clean();
}
add_shortcode( 'charmed_withdrawal_form', 'charmed_withdrawal_form' );

/**
 * Traitement de la déclaration.
 */
function charmed_withdrawal_handle(): void {
	// phpcs:disable WordPress.Security.NonceVerification.Missing -- formulaire légal public : doit fonctionner même depuis une page en cache ; anti-spam par champ piège + limite.
	$back = isset( $_POST['back'] ) ? esc_url_raw( wp_unslash( $_POST['back'] ) ) : home_url( '/' );
	$back = wp_validate_redirect( $back, home_url( '/' ) );

	if ( ! empty( $_POST['website'] ) ) {
		wp_safe_redirect( $back );
		exit;
	}
	$number  = isset( $_POST['order_number'] ) ? sanitize_text_field( wp_unslash( $_POST['order_number'] ) ) : '';
	$email   = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) ) : '';
	$name    = isset( $_POST['name'] ) ? sanitize_text_field( wp_unslash( $_POST['name'] ) ) : '';
	$message = isset( $_POST['message'] ) ? sanitize_textarea_field( wp_unslash( $_POST['message'] ) ) : '';
	$items   = isset( $_POST['items'] ) ? array_map( 'sanitize_text_field', (array) wp_unslash( $_POST['items'] ) ) : array();
	if ( ! empty( $_POST['items_text'] ) ) {
		$items[] = sanitize_textarea_field( wp_unslash( $_POST['items_text'] ) );
	}
	$order_id = isset( $_POST['order_id'] ) ? absint( $_POST['order_id'] ) : 0;
	// phpcs:enable

	if ( '' === $number || ! is_email( $email ) || '' === $name ) {
		wp_safe_redirect( add_query_arg( 'cp_withdrawal', 'error', $back ) );
		exit;
	}

	$ip   = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
	$rate = 'charmed_wd_' . md5( $ip . wp_salt( 'nonce' ) );
	$hits = (int) get_transient( $rate );
	if ( $hits >= 10 ) {
		wp_safe_redirect( add_query_arg( 'cp_withdrawal', 'error', $back ) );
		exit;
	}
	set_transient( $rate, $hits + 1, HOUR_IN_SECONDS );

	// Retrouver la commande (n° = ID par défaut ; filtre pour un plugin de numérotation).
	$order = $order_id ? wc_get_order( $order_id ) : null;
	if ( ! $order instanceof WC_Order ) {
		$found = apply_filters( 'charmed_withdrawal_find_order', null, $number );
		$order = $found instanceof WC_Order ? $found : wc_get_order( absint( preg_replace( '/\D/', '', $number ) ) );
	}
	$matched = $order instanceof WC_Order && 0 === strcasecmp( (string) $order->get_billing_email(), $email );

	$ref   = 'RTR-' . wp_date( 'Ymd' ) . '-' . strtoupper( wp_generate_password( 6, false, false ) );
	$local = wp_date( 'd/m/Y H:i:s T' );
	$utc   = gmdate( 'c' );

	$declaration = implode(
		"\n",
		array(
			sprintf( /* translators: %s: reference */ __( 'Référence : %s', 'charmed-paris' ), $ref ),
			sprintf( /* translators: 1: local date, 2: UTC date */ __( 'Reçue le : %1$s (UTC %2$s)', 'charmed-paris' ), $local, $utc ),
			sprintf( /* translators: %s: name */ __( 'Nom : %s', 'charmed-paris' ), $name ),
			sprintf( /* translators: %s: email */ __( 'E-mail : %s', 'charmed-paris' ), $email ),
			sprintf( /* translators: %s: order number */ __( 'Commande : %s', 'charmed-paris' ), $number ),
			sprintf( /* translators: %s: items */ __( 'Articles : %s', 'charmed-paris' ), $items ? implode( ' ; ', $items ) : __( 'toute la commande', 'charmed-paris' ) ),
			$message ? sprintf( /* translators: %s: comment */ __( 'Commentaire : %s', 'charmed-paris' ), $message ) : '',
			'',
			__( 'Je notifie par la présente ma rétractation du contrat portant sur la vente des biens ci-dessus.', 'charmed-paris' ),
		)
	);

	$post_id = wp_insert_post(
		array(
			'post_type'    => 'charmed_withdrawal',
			'post_status'  => 'private',
			'post_title'   => $ref . ' — ' . $number,
			'post_content' => $declaration,
		)
	);
	if ( $post_id && ! is_wp_error( $post_id ) ) {
		update_post_meta( $post_id, '_order_number', $number );
		update_post_meta( $post_id, '_order_matched', $matched ? 'yes' : 'no' );
	}

	if ( $matched ) {
		$order->add_order_note( __( 'Demande de rétractation reçue en ligne.', 'charmed-paris' ) . "\n" . $declaration, 0, false );
		$order->update_meta_data( '_charmed_withdrawal_ref', $ref );
		$order->save();
	}

	$shop = wp_specialchars_decode( get_bloginfo( 'name' ), ENT_QUOTES );
	wp_mail(
		charmed_withdrawal_merchant_email(),
		sprintf( '[%1$s] %2$s %3$s%4$s', $shop, __( 'Rétractation', 'charmed-paris' ), $number, $matched ? '' : ' — ' . __( 'COMMANDE NON RETROUVÉE (vérifier)', 'charmed-paris' ) ),
		$declaration,
		array( 'Reply-To: ' . $name . ' <' . $email . '>' )
	);
	wp_mail(
		$email,
		sprintf( /* translators: 1: shop name, 2: reference */ __( '[%1$s] Accusé de réception de ta rétractation (%2$s)', 'charmed-paris' ), $shop, $ref ),
		__( 'Bonjour,', 'charmed-paris' ) . "\n\n" . __( 'Nous accusons réception de ta demande de rétractation, dont voici la copie :', 'charmed-paris' ) . "\n\n" . $declaration . "\n\n" . __( 'Nous revenons vers toi avec les modalités de retour. Le remboursement intervient au plus tard 14 jours après réception de ta demande (il peut être différé jusqu’à la récupération des articles).', 'charmed-paris' ) . "\n\n" . $shop
	);

	do_action( 'charmed_withdrawal_received', $ref, $order instanceof WC_Order ? $order : null, $declaration );

	wp_safe_redirect(
		add_query_arg(
			array(
				'cp_withdrawal' => 'sent',
				'ref'           => rawurlencode( $ref ),
			),
			$back
		)
	);
	exit;
}
add_action( 'admin_post_nopriv_charmed_withdrawal', 'charmed_withdrawal_handle' );
add_action( 'admin_post_charmed_withdrawal', 'charmed_withdrawal_handle' );

/**
 * Création en un clic de la page « Rétractation » (notice admin tant qu'elle n'existe pas).
 */
add_action(
	'admin_notices',
	static function () {
		if ( ! current_user_can( 'manage_woocommerce' ) || charmed_withdrawal_url() ) {
			return;
		}
		$url = wp_nonce_url( admin_url( 'admin-post.php?action=charmed_withdrawal_create_page' ), 'charmed_withdrawal_create_page' );
		printf(
			'<div class="notice notice-warning"><p>%1$s <a class="button" href="%2$s">%3$s</a></p></div>',
			esc_html__( 'Rétractation en ligne (L221-21) : la page du formulaire n’existe pas encore.', 'charmed-paris' ),
			esc_url( $url ),
			esc_html__( 'Créer la page', 'charmed-paris' )
		);
	}
);
add_action(
	'admin_post_charmed_withdrawal_create_page',
	static function () {
		if ( ! current_user_can( 'manage_woocommerce' ) ) {
			wp_die( esc_html__( 'Accès refusé.', 'charmed-paris' ) );
		}
		check_admin_referer( 'charmed_withdrawal_create_page' );
		$id = wp_insert_post(
			array(
				'post_type'    => 'page',
				'post_status'  => 'publish',
				'post_title'   => __( 'Rétractation', 'charmed-paris' ),
				'post_name'    => 'retractation',
				'post_content' => "<!-- wp:shortcode -->\n[charmed_withdrawal_form]\n<!-- /wp:shortcode -->",
			)
		);
		if ( $id && ! is_wp_error( $id ) ) {
			update_option( 'charmed_withdrawal_page_id', (int) $id );
		}
		wp_safe_redirect( admin_url( 'admin.php?page=wc-settings&tab=advanced&section=charmed_withdrawal' ) );
		exit;
	}
);
