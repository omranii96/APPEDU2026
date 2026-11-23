# Thème CHARMED PARIS (bloc / FSE)

Thème WordPress 6.5+ / WooCommerce 9+ / PHP 8.1+ tiré de la maquette `charmed-paris/charmed-site.html`.
Installation complète, réglages WooCommerce et connexion Branvas : `woocommerce/tech/installation.md`.
Budget et stratégie de performance : `woocommerce/tech/performance.md`.

## Installer le thème

1. Zipper le dossier `charmed-paris/` (le dossier lui-même, pas son contenu) → Apparence > Thèmes > Ajouter > Téléverser.
2. Activer. Recommandé : copier `inc/withdrawal.php` dans `wp-content/mu-plugins/charmed-withdrawal.php` pour que la
   fonction légale de rétractation survive à un changement de thème (le thème ne la charge pas deux fois).
3. WooCommerce > Réglages > Produits > **CHARMED PARIS** : remise 2e parure, seuil, téléphone, prix barrés, Noël.
4. WooCommerce > Réglages > Avancé > **Rétractation** : cliquer « Créer la page » (notice admin), vérifier les libellés.

## Arborescence

```
style.css            en-tête du thème
theme.json           palette, typo (fontFace auto-hébergées), espacements, largeurs (760 / 1200 px)
functions.php        chargeur des modules inc/
inc/
  setup.php          supports, traductions, tailles d'images (charmed-cutout 880, charmed-univers 600×800)
  settings.php       réglages WooCommerce > Produits > CHARMED PARIS
  assets.php         enqueue conditionnels, préchargements, allègement des scripts Woo hors boutique
  products.php       lecture des vrais produits (catégorie / IDs / SKU) + champs produit (image détourée, code, composition)
  commerce.php       2e parure −15 %, livraison offerte, téléphone, stock, délais, Noël, bouton de commande, prix barrés, avis
  blocks.php         blocs dynamiques charmed/* + shortcodes
  render-brand.php   logo, intro, bandeau, packagings, messages, newsletter
  render-catalog.php coffrets, file des parures, univers, avis vérifiés
  newsletter.php     traitement du formulaire (action charmed_newsletter_subscribe)
  seo.php            JSON-LD produit : marque, MPN = SKU, pas de GTIN
  i18n.php           sélecteur de langue (TranslatePress ; Polylang/WPML lus par compatibilité)
  withdrawal.php     rétractation en ligne L221-21 (copiable en mu-plugin)
templates/           index, front-page, single-product, archive-product, taxonomy-product_cat,
                     product-search-results, page, page-wide, page-cart, page-checkout, 404
parts/               header, footer (→ patterns header/footer, donc traduisibles par gettext)
patterns/            une section de la maquette par fichier + accueil.php (page complète)
assets/css           base.css (global), sections.css (si bloc rendu), intro.css (si intro rendue)
assets/js            cart.js, header.js, coffrets.js, file-parures.js, intro.js, packshots.js, editor-blocks.js
assets/vendor        three-r128.min.js (MIT, non modifié) — jamais enqueue en PHP, chargé à la demande par intro.js
assets/fonts         woff2 latin auto-hébergés + licences OFL
assets/img           boîtes (coffret fermé/ouvert), packagings, images de repli des univers
languages/           charmed-paris.pot, en_US.po/.mo, en_GB.po/.mo (source en français)
```

## Polices (auto-hébergées, déjà incluses)

Fichiers `assets/fonts/*.woff2`, sous-ensemble **latin** (couvre le français : é, œ, €, −, ’), téléchargés depuis Google
Fonts le 22/11/2026, licence SIL OFL 1.1 (`OFL-*.txt`). Aucun appel à Google : conforme RGPD.

| Fichier | Famille | Graisses |
|---|---|---|
| `bodoni-moda-latin-wght.woff2` | Bodoni Moda (variable, axes wght + opsz) | 400–700 |
| `bodoni-moda-italic-latin-400.woff2` | Bodoni Moda italique | 400 |
| `jost-latin-wght.woff2` | Jost (variable) | 300–600 |
| `dm-mono-latin-400.woff2` | DM Mono | 400 |

Pour les remplacer ou ajouter le sous-ensemble latin-ext : https://fonts.google.com/specimen/Bodoni+Moda,
https://fonts.google.com/specimen/Jost, https://fonts.google.com/specimen/DM+Mono (ou https://gwfh.mranftl.com/fonts,
« google-webfonts-helper », format woff2), puis garder les mêmes noms de fichiers ou adapter `theme.json`.

## Blocs et shortcodes

| Bloc | Shortcode | Données |
|---|---|---|
| `charmed/intro` | `[charmed_intro]` | Héros ; film au scroll sur l'accueil seulement |
| `charmed/coffrets` | `[charmed_coffrets skus="JSGRQR,JS1AQ5" limit="8"]` | Vrais produits (category / ids / skus / orderby) |
| `charmed/file-parures` | `[charmed_file_parures category="parures" limit="9"]` | Vrais produits |
| `charmed/univers` | `[charmed_univers slugs="sculpture,eclat"]` | Catégories produit + image de catégorie |
| `charmed/reviews` | `[charmed_reviews limit="6"]` | Avis Woo natifs, acheteuses vérifiées |
| `charmed/promo-notice` | `[charmed_promo parts="xmas,shipping,bundle"]` | Seuil lu dans Woo, dates de Noël, remise |
| `charmed/packshots`, `charmed/marquee`, `charmed/newsletter`, `charmed/wordmark`, `charmed/language-switcher`, `charmed/withdrawal-link` | `[charmed_…]` | — |
| — | `[charmed_withdrawal_form]` | Formulaire de rétractation (page dédiée) |

Champs ajoutés à chaque produit (onglet Général) : **Image détourée (ID média)** — téléverser les PNG/WebP de
`charmed-paris/cut/` —, **Ligne courte**, **Code étiquette**, **Composition** (une pièce par ligne).

## Ajout au panier

Chaque bouton est un lien natif `?add-to-cart=ID` (fonctionne sans JS). `cart.js` l'intercepte et appelle la
**Store API** (`POST /wp-json/wc/store/v1/cart/add-item`, nonce rafraîchi automatiquement, compatible cache de page),
puis déclenche `wc-blocks_added_to_cart` : le bloc **Mini-panier** de l'en-tête se met à jour et s'ouvre.
Produits variables : le bouton mène à la fiche (« Choisir »).

## Règles serveur (inc/commerce.php)

- **2e parure −15 %** : `woocommerce_cart_calculate_fees`, frais négatif HT sur la parure la moins chère (TVA répartie
  par WooCommerce) ; modes « une fois » / « par paire » ; catégories éligibles ; non cumulable avec un code par défaut.
  Testé hors WordPress : 79 € + 49 € → −7,35 € TTC ; 3 × 69 € → −10,35 €.
- **Livraison offerte** : méthode native « Livraison gratuite » (montant minimum 50 €) + « Forfait » 4,90 € ;
  le thème recalcule le seuil après la remise et masque le forfait quand la gratuité s'applique.
- **Téléphone obligatoire** (Branvas : requis hors US/UK), validé côté serveur (paiement classique et bloc).
- **Stock** : jamais de quantité affichée (valeur fictive synchronisée par Branvas).
- **Légal** : bouton « Commander avec obligation de paiement » (classique + bloc via `registerCheckoutFilters`),
  pas de prix barré ni de badge Promo par défaut, rétractation en ligne (`inc/withdrawal.php`).
- **Avis** : avis natifs forcés sur « acheteuses vérifiées uniquement ».

## Traductions

Source en français. `languages/en_US.mo` et `en_GB.mo` fournis (284 chaînes). Régénérer après modification :

```
xgettext --language=PHP --from-code=UTF-8 --add-comments=translators -k__ -k_e -kesc_html__ -kesc_html_e \
  -kesc_attr__ -kesc_attr_e -k_x:1,2c -k_n:1,2 -o languages/charmed-paris.pot functions.php inc/*.php patterns/*.php
msgmerge -U languages/en_US.po languages/charmed-paris.pot && msgfmt -o languages/en_US.mo languages/en_US.po
```

Les contenus (produits, pages, menus, catégories) se traduisent dans **TranslatePress** ; les chaînes des templates
`.html` non issues de patterns (« Tu aimeras aussi », « Aucune parure ne correspond… ») aussi.
