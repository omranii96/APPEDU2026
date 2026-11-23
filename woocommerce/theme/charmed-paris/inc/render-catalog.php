<?php
/**
 * Rendu des sections produits à partir des VRAIS produits WooCommerce :
 * charmed/coffrets, charmed/file-parures, charmed/univers.
 *
 * Le HTML rendu est complet et utilisable sans JS (liste défilante / grille, liens produits,
 * ajout au panier par lien natif ?add-to-cart=ID). Les scripts ne font qu'animer ce DOM.
 *
 * @package CharmedParis
 */

defined( 'ABSPATH' ) || exit;

/**
 * Arguments de sélection communs aux blocs produits.
 *
 * @param array $a Attributs du bloc.
 */
function charmed_selection_args( array $a ): array {
	return array(
		'category' => (string) ( $a['category'] ?? '' ),
		'ids'      => (string) ( $a['ids'] ?? '' ),
		'skus'     => (string) ( $a['skus'] ?? '' ),
		'limit'    => (int) ( $a['limit'] ?? 8 ),
		'orderby'  => (string) ( $a['orderby'] ?? 'menu_order' ),
	);
}

/**
 * Message affiché quand aucun produit ne correspond (visible uniquement des administrateurs).
 *
 * @param string $block Nom du bloc.
 */
function charmed_empty_notice( string $block ): string {
	if ( ! current_user_can( 'edit_theme_options' ) ) {
		return '';
	}
	return '<p class="cp-admin-note">' . esc_html(
		sprintf(
			/* translators: %s: block name */
			__( '%s : aucun produit publié ne correspond à la sélection (catégorie, IDs ou SKU). Message visible des administrateurs uniquement.', 'charmed-paris' ),
			$block
		)
	) . '</p>';
}

/**
 * Image produit (détourée si renseignée) avec srcset.
 *
 * @param array  $p     Données produit.
 * @param string $class Classe.
 * @param string $sizes Attribut sizes.
 * @param bool   $eager Chargement prioritaire.
 */
function charmed_product_img( array $p, string $class, string $sizes, bool $eager = false ): string {
	if ( ! $p['image_id'] ) {
		return function_exists( 'wc_placeholder_img' ) ? wc_placeholder_img( 'woocommerce_single', array( 'class' => $class ) ) : '';
	}
	return wp_get_attachment_image(
		$p['image_id'],
		'charmed-cutout',
		false,
		array(
			'class'    => $class . ( $p['is_cutout'] ? ' is-cutout' : '' ),
			'alt'      => $p['name'],
			'sizes'    => $sizes,
			'loading'  => $eager ? 'eager' : 'lazy',
			'decoding' => 'async',
		)
	);
}

/**
 * Bloc charmed/coffrets : carrousel de coffrets qui s'ouvrent sur leur parure.
 *
 * @param array $a Attributs.
 */
function charmed_render_coffrets( array $a ): string {
	$products = charmed_get_showcase_products( charmed_selection_args( $a ) );
	if ( ! $products ) {
		return charmed_empty_notice( 'charmed/coffrets' );
	}
	wp_enqueue_style( 'charmed-sections' );
	wp_enqueue_script( 'charmed-coffrets' );

	$items = array_map( 'charmed_product_data', $products );
	$n     = count( $items );
	/* translators: %d: number of sets */
	$eyebrow = ! empty( $a['eyebrow'] ) ? $a['eyebrow'] : sprintf( _n( '%d parure à découvrir', '%d parures à découvrir', $n, 'charmed-paris' ), $n );
	$heading = ! empty( $a['heading'] ) ? $a['heading'] : __( 'Choisis ton coffret', 'charmed-paris' );
	$intro   = ! empty( $a['intro'] ) ? $a['intro'] : __( 'Fais tourner les coffrets. Celui qui arrive devant toi s’ouvre sur sa parure.', 'charmed-paris' );

	$closed = charmed_asset( 'img/box-closed.webp' );
	$closed_sm = charmed_asset( 'img/box-closed-400.webp' );
	$open   = charmed_asset( 'img/box-open.webp' );
	$open_sm = charmed_asset( 'img/box-open-400.webp' );
	$first  = $items[0];

	ob_start();
	?>
	<section <?php echo charmed_wrap( array( 'class' => 'cp-cof alignfull', 'id' => 'coffrets', 'aria-labelledby' => 'cp-cof-title' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
		<div class="cp-wrap cp-cof__head">
			<p class="cp-eyebrow"><?php echo esc_html( $eyebrow ); ?></p>
			<h2 id="cp-cof-title"><?php echo esc_html( $heading ); ?></h2>
			<p><?php echo esc_html( $intro ); ?></p>
		</div>
		<div class="cp-cof__stage" tabindex="0" aria-roledescription="<?php esc_attr_e( 'carrousel', 'charmed-paris' ); ?>" aria-label="<?php esc_attr_e( 'Coffrets : flèches gauche et droite pour tourner', 'charmed-paris' ); ?>">
			<ul class="cp-cof__ring">
				<?php foreach ( $items as $k => $p ) : ?>
					<li class="cp-cof__item" data-index="<?php echo (int) $k; ?>">
						<div class="cp-cof__box" aria-hidden="true">
							<span class="cp-cof__sh"></span>
							<img class="cp-cof__closed" src="<?php echo esc_url( $closed_sm ); ?>" srcset="<?php echo esc_url( $closed_sm ); ?> 400w, <?php echo esc_url( $closed ); ?> 720w" sizes="(max-width: 760px) 46vw, 420px" width="720" height="720" alt="" loading="lazy" decoding="async">
							<img class="cp-cof__open" src="<?php echo esc_url( $open_sm ); ?>" srcset="<?php echo esc_url( $open_sm ); ?> 400w, <?php echo esc_url( $open ); ?> 720w" sizes="(max-width: 760px) 46vw, 420px" width="720" height="720" alt="" loading="lazy" decoding="async">
							<span class="cp-cof__glow"></span>
						</div>
						<?php echo charmed_product_img( $p, 'cp-cof__jw', '(max-width: 760px) 40vw, 300px' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
						<div class="cp-cof__card">
							<?php if ( $p['univers'] ) : ?>
								<p class="cp-eyebrow cp-cof__tag"><?php echo esc_html( $p['univers'] ); ?></p>
							<?php endif; ?>
							<h3 class="cp-cof__name"><a href="<?php echo esc_url( $p['url'] ); ?>"><?php echo esc_html( $p['name'] ); ?></a></h3>
							<p class="cp-cof__line"><?php echo esc_html( $p['line'] ); ?></p>
							<p class="cp-price"><?php echo wp_kses_post( $p['price_html'] ); ?></p>
							<?php echo charmed_add_to_cart_link( $p, 'cp-btn cp-btn--ghost cp-cof__add' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
						</div>
					</li>
				<?php endforeach; ?>
			</ul>
			<div class="cp-cof__hand" aria-hidden="true"><i>←</i><?php esc_html_e( 'Fais tourner', 'charmed-paris' ); ?><i>→</i></div>
		</div>
		<div class="cp-wrap cp-cof__info">
			<button class="cp-cof__arrow cp-cof__prev" type="button" aria-label="<?php esc_attr_e( 'Coffret précédent', 'charmed-paris' ); ?>">←</button>
			<div class="cp-cof__text" aria-live="polite">
				<p class="cp-eyebrow cp-cof__tag"><?php echo esc_html( $first['univers'] ); ?></p>
				<h3 class="cp-cof__name"><a href="<?php echo esc_url( $first['url'] ); ?>"><?php echo esc_html( $first['name'] ); ?></a></h3>
				<p class="cp-cof__line"><?php echo esc_html( $first['line'] ); ?></p>
				<div class="cp-cof__buy">
					<p class="cp-price"><?php echo wp_kses_post( $first['price_html'] ); ?></p>
					<?php echo charmed_add_to_cart_link( $first, 'cp-btn cp-btn--ghost cp-cof__add' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
				</div>
			</div>
			<button class="cp-cof__arrow cp-cof__next" type="button" aria-label="<?php esc_attr_e( 'Coffret suivant', 'charmed-paris' ); ?>">→</button>
		</div>
		<div class="cp-cof__dots" role="group" aria-label="<?php esc_attr_e( 'Choisir un coffret', 'charmed-paris' ); ?>"></div>
	</section>
	<?php
	return (string) ob_get_clean();
}

/**
 * Bloc charmed/file-parures : « La file des parures » (vues Une / La file / Toutes) avec étiquette.
 *
 * @param array $a Attributs.
 */
function charmed_render_file_parures( array $a ): string {
	$products = charmed_get_showcase_products( charmed_selection_args( $a + array( 'limit' => 9 ) ) );
	if ( ! $products ) {
		return charmed_empty_notice( 'charmed/file-parures' );
	}
	wp_enqueue_style( 'charmed-sections' );
	wp_enqueue_script( 'charmed-file' );

	$items   = array_map( 'charmed_product_data', $products );
	$n       = count( $items );
	$heading = ! empty( $a['heading'] ) ? $a['heading'] : __( 'La file des parures', 'charmed-paris' );
	$first   = $items[0];
	$xmas    = charmed_xmas_state()['packaging'];
	// Une seule boîte à bijoux par commande (les pièces suivantes : sachets scellés) : ne pas promettre un écrin par parure.
	$extra   = __( 'Écrin, pochette en velours, chamoisine', 'charmed-paris' );

	ob_start();
	?>
	<section <?php echo charmed_wrap( array( 'class' => 'cp-file is-focus alignfull', 'id' => 'pieces', 'aria-labelledby' => 'cp-file-title' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
		<h2 id="cp-file-title" class="cp-file__h"><?php echo esc_html( $heading ); ?></h2>
		<div class="cp-file__stage" tabindex="0" aria-label="<?php esc_attr_e( 'Parures : flèches gauche et droite pour passer à la suivante', 'charmed-paris' ); ?>">
			<div class="cp-file__top">
				<p class="cp-file__title"><b>CHARMED PARIS</b><br>
					<?php
					/* translators: 1: section title, 2: number of sets */
					echo esc_html( sprintf( _n( '%1$s · %2$d écrin', '%1$s · %2$d écrins', $n, 'charmed-paris' ), $heading, $n ) );
					?>
				</p>
				<div class="cp-file__views" role="group" aria-label="<?php esc_attr_e( 'Affichage', 'charmed-paris' ); ?>">
					<button type="button" data-v="focus" aria-pressed="true"><?php esc_html_e( 'Une', 'charmed-paris' ); ?></button>
					<button type="button" data-v="queue" aria-pressed="false"><?php esc_html_e( 'La file', 'charmed-paris' ); ?></button>
					<button type="button" data-v="grid" aria-pressed="false"><?php esc_html_e( 'Toutes', 'charmed-paris' ); ?></button>
				</div>
			</div>
			<nav class="cp-file__rail" aria-label="<?php esc_attr_e( 'Choisir une parure', 'charmed-paris' ); ?>"></nav>
			<ol class="cp-file__items">
				<?php foreach ( $items as $k => $p ) : ?>
					<?php $no = str_pad( (string) ( $k + 1 ), 2, '0', STR_PAD_LEFT ); ?>
					<li class="cp-file__item"
						data-no="<?php echo esc_attr( $no ); ?>"
						data-code="<?php echo esc_attr( $p['code'] ); ?>"
						data-sku="<?php echo esc_attr( $p['sku'] ); ?>"
						data-univers="<?php echo esc_attr( $p['univers'] ); ?>"
						data-short="<?php echo esc_attr( $p['short'] ); ?>"
						data-pieces="<?php echo esc_attr( (string) wp_json_encode( $p['pieces'] ) ); ?>">
						<span class="cp-file__floor" aria-hidden="true"></span>
						<div class="cp-file__ph"><?php echo charmed_product_img( $p, 'cp-file__img', '(max-width: 760px) 62vw, 440px', 0 === $k ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></div>
						<span class="cp-file__scan" aria-hidden="true"></span>
						<p class="cp-file__lbl" aria-hidden="true"><?php echo esc_html( $no . ' ' . mb_strtoupper( $p['short'] ) . ' · ' . $p['price_text'] ); ?></p>
						<div class="cp-file__fb">
							<h3><a href="<?php echo esc_url( $p['url'] ); ?>"><?php echo esc_html( $p['name'] ); ?></a></h3>
							<p class="cp-file__line"><?php echo esc_html( $p['line'] ); ?></p>
							<p class="cp-price"><?php echo wp_kses_post( $p['price_html'] ); ?></p>
							<?php echo charmed_add_to_cart_link( $p, 'cp-btn cp-btn--small' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
						</div>
					</li>
				<?php endforeach; ?>
			</ol>
			<div class="cp-file__name" aria-live="polite"><small class="cp-file__meta"></small><p class="cp-file__big"><?php echo esc_html( $first['short'] ); ?></p></div>
			<p class="cp-file__hint" aria-hidden="true" data-grid="<?php esc_attr_e( 'Clique sur une parure pour l’ouvrir', 'charmed-paris' ); ?>"><?php esc_html_e( 'Glisse, ou utilise les flèches ← →', 'charmed-paris' ); ?></p>
			<aside class="cp-ticket" aria-label="<?php esc_attr_e( 'Étiquette de la parure', 'charmed-paris' ); ?>">
				<span class="cp-ticket__string" aria-hidden="true"></span>
				<div class="cp-ticket__head">
					<span class="cp-ticket__brand"><?php echo charmed_wordmark_html(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?><span>Paris</span></span>
					<span class="cp-ticket__no">
						<?php
						/* translators: %s: number, e.g. 01 */
						printf( esc_html__( 'Écrin n°%s', 'charmed-paris' ), '<span data-t="no">01</span>' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
						?>
					</span>
				</div>
				<div class="cp-ticket__code"><b data-t="code"><?php echo esc_html( $first['code'] ); ?></b><span data-t="name"><?php echo esc_html( $first['short'] ); ?></span></div>
				<ul class="cp-ticket__rows" data-t="rows" data-included="<?php esc_attr_e( 'inclus', 'charmed-paris' ); ?>">
					<?php foreach ( $first['pieces'] as $piece ) : ?>
						<li><span><?php echo esc_html( $piece ); ?></span><span><?php esc_html_e( 'inclus', 'charmed-paris' ); ?></span></li>
					<?php endforeach; ?>
					<li class="cp-ticket__extra"><span><?php echo esc_html( $extra ); ?></span><span><?php esc_html_e( '1 par commande', 'charmed-paris' ); ?></span></li>
				</ul>
				<div class="cp-ticket__total"><span><?php esc_html_e( 'Total parure', 'charmed-paris' ); ?></span><b data-t="price"><?php echo wp_kses_post( $first['price_html'] ); ?></b></div>
				<div data-t="add"><?php echo charmed_add_to_cart_link( $first, 'cp-ticket__add' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></div>
				<div class="cp-ticket__bar" aria-hidden="true"></div>
				<div class="cp-ticket__sku" data-t="sku"><?php echo esc_html( trim( $first['sku'] . ' · CHARMED PARIS', ' ·' ) ); ?></div>
				<div class="cp-ticket__foot"><span><?php echo esc_html( $xmas ? __( 'Emballage de Noël offert', 'charmed-paris' ) : __( 'Prêt à offrir', 'charmed-paris' ) ); ?></span><span>Paris</span></div>
			</aside>
			<div class="cp-file__curl" aria-hidden="true"></div>
		</div>
	</section>
	<?php
	return (string) ob_get_clean();
}

/**
 * Bloc charmed/univers : les univers = catégories produit WooCommerce.
 *
 * @param array $a Attributs : slugs (liste ordonnée) ou parent (slug), heading, eyebrow.
 */
function charmed_render_univers( array $a ): string {
	if ( ! taxonomy_exists( 'product_cat' ) ) {
		return '';
	}
	$slugs = array_values( array_filter( array_map( 'trim', explode( ',', (string) ( $a['slugs'] ?? 'sculpture,eclat,couleur-precieuse,joaillerie-925,mixte' ) ) ) ) );
	$query = array(
		'taxonomy'   => 'product_cat',
		'hide_empty' => true,
	);
	if ( ! empty( $a['parent'] ) ) {
		$parent = get_term_by( 'slug', (string) $a['parent'], 'product_cat' );
		$query['parent'] = $parent ? (int) $parent->term_id : -1;
	} elseif ( $slugs ) {
		$query['slug']    = $slugs;
		$query['orderby'] = 'slug__in';
	}
	$terms = get_terms( $query );
	if ( is_wp_error( $terms ) || ! $terms ) {
		return charmed_empty_notice( 'charmed/univers' );
	}
	wp_enqueue_style( 'charmed-sections' );

	$fallback = array(
		'sculpture'         => 'img/univers/sculpture.webp',
		'eclat'             => 'img/univers/eclat.webp',
		'couleur-precieuse' => 'img/univers/couleur-precieuse.webp',
		'joaillerie-925'    => 'img/univers/joaillerie-925.webp',
		'mixte'             => 'img/univers/mixte.webp',
	);
	$taglines = array(
		'sculpture'         => __( 'métal doré', 'charmed-paris' ),
		'eclat'             => __( 'doré · oxydes de zirconium', 'charmed-paris' ),
		'couleur-precieuse' => __( 'pierres de couleur', 'charmed-paris' ),
		'joaillerie-925'    => __( 'argent 925 · moissanite synthétique', 'charmed-paris' ),
		'mixte'             => __( 'sur cordon', 'charmed-paris' ),
	);
	$heading = ! empty( $a['heading'] ) ? $a['heading'] : __( 'Choisis ton éclat', 'charmed-paris' );
	$eyebrow = ! empty( $a['eyebrow'] ) ? $a['eyebrow'] : __( 'Les univers', 'charmed-paris' );
	$shop    = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/' );

	ob_start();
	?>
	<section <?php echo charmed_wrap( array( 'class' => 'cp-univers', 'id' => 'univers', 'aria-labelledby' => 'cp-uni-title' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
		<div class="cp-head-row">
			<div><p class="cp-eyebrow"><?php echo esc_html( $eyebrow ); ?></p><h2 id="cp-uni-title"><?php echo esc_html( $heading ); ?></h2></div>
			<a class="cp-btn cp-btn--ghost" href="<?php echo esc_url( $shop ); ?>"><?php esc_html_e( 'Tout voir', 'charmed-paris' ); ?></a>
		</div>
		<ul class="cp-univers__rail">
			<?php foreach ( $terms as $term ) : ?>
				<?php
				$thumb = (int) get_term_meta( $term->term_id, 'thumbnail_id', true );
				$link  = get_term_link( $term );
				/* translators: %d: number of sets */
				$count = sprintf( _n( '%d parure', '%d parures', (int) $term->count, 'charmed-paris' ), (int) $term->count );
				$tag   = $taglines[ $term->slug ] ?? '';
				?>
				<li>
					<a class="cp-uni" href="<?php echo esc_url( is_wp_error( $link ) ? $shop : $link ); ?>">
						<?php
						if ( $thumb ) {
							echo wp_get_attachment_image(
								$thumb,
								'charmed-univers',
								false,
								array(
									'class'   => 'cp-uni__img',
									'alt'     => '',
									'sizes'   => '(max-width: 760px) 70vw, 300px',
									'loading' => 'lazy',
								)
							);
						} elseif ( isset( $fallback[ $term->slug ] ) ) {
							printf( '<img class="cp-uni__img" src="%s" width="400" height="400" alt="" loading="lazy" decoding="async">', esc_url( charmed_asset( $fallback[ $term->slug ] ) ) );
						}
						?>
						<span class="cp-uni__meta"><?php echo esc_html( $tag ? $count . ' · ' . $tag : $count ); ?></span>
						<h3><?php echo esc_html( $term->name ); ?></h3>
						<?php if ( $term->description ) : ?>
							<p><?php echo esc_html( wp_trim_words( wp_strip_all_tags( $term->description ), 14, '…' ) ); ?></p>
						<?php endif; ?>
					</a>
				</li>
			<?php endforeach; ?>
		</ul>
	</section>
	<?php
	return (string) ob_get_clean();
}
