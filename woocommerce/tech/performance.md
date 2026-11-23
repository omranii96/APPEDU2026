# CHARMED PARIS — performance (budget et stratégie)

Version du 23/11/2026. S'applique au thème `woocommerce/theme/charmed-paris/`. Mesures de poids faites sur les
fichiers du thème (gzip -9) ; les temps sont des **objectifs**, à mesurer en préproduction (PageSpeed Insights mobile,
puis données réelles CrUX / Search Console après lancement).

## 1. Budget

| Indicateur (mobile, 4G, p75) | Objectif | Seuil d'alerte |
|---|---|---|
| **LCP** | **< 2,0 s** (exigence : < 2,5 s) | 2,5 s |
| **CLS** | **< 0,05** (exigence : < 0,1) | 0,1 |
| **INP** | < 200 ms | 200 ms |
| TTFB (page en cache) | < 200 ms ; sans cache < 800 ms | 800 ms |
| JS du thème au premier rendu (accueil) | **≤ 20 Ko gz** (mesuré : ≈ 14 Ko gz non minifié, ≈ 8 Ko minifié) | 30 Ko |
| JS total au premier rendu (thème + Woo + extensions) | ≤ 120 Ko gz | 170 Ko |
| Three.js | **0 Ko au premier rendu** ; 149 Ko gz chargés après interaction / temps mort | — |
| CSS (accueil) | ≤ 15 Ko gz thème (mesuré : base 3,0 + sections 5,4 + intro 2,3 Ko) + CSS des blocs Woo | 40 Ko |
| Polices | 2 préchargées : Bodoni Moda 46 Ko + Jost 27 Ko ; italique (30 Ko) et DM Mono (15 Ko) à la demande | 150 Ko |
| Images au-dessus de la ligne de flottaison | 0 (héros en CSS + texte) ; ≤ 120 Ko si un poster est ajouté | 200 Ko |
| Poids total accueil (premier rendu, hors Three) | ≤ 900 Ko | 1,5 Mo |
| Requêtes au premier rendu | ≤ 40 | 60 |

Poids mesurés des scripts du thème (gz) : intro 5,3 Ko · file-parures 3,2 · coffrets 2,3 · cart 1,7 · packshots 0,9 ·
header 0,4. Tous chargés en `defer`, **uniquement si le bloc correspondant est rendu** (intro : accueil seulement).

## 2. Intro Three.js

Principe : **le LCP ne dépend jamais de WebGL.**

1. **Rendu serveur d'abord.** L'intro est du HTML : logo (texte Bodoni + parenthèses CSS), « Ouvre. », H1
   « CHARMED PARIS », anneau doré en CSS. L'élément LCP est du **texte** servi dans le HTML, affiché dès la police
   préchargée (`font-display: swap`, police auto-hébergée, pas de connexion tierce).
2. **Aucun Three.js côté PHP.** `three-r128.min.js` (auto-hébergé, MIT) n'est jamais mis en file d'attente : `intro.js`
   (5 Ko gz, `defer`, accueil seulement) l'injecte :
   - à la **première interaction** (scroll, molette, toucher, clavier, pointeur), ou
   - sur **temps mort** (`requestIdleCallback`, délai max 4 s après `load`) ;
   - **jamais** si `prefers-reduced-motion: reduce`, Save-Data, `navigator.deviceMemory < 2`, WebGL absent, ou visite
     publicitaire (`utm_*`, `gclid`, `fbclid`, `ttclid`, `msclkid` : décision du 23/11, pas d'intro pour le trafic pub).
   Sans WebGL, l'animation DOM continue avec l'anneau CSS (repli).
3. **Pas de CLS.** La classe `cp-js cp-motion` (et `cp-ad`) est posée par un script en ligne de 300 octets dans
   `<head>` ; la hauteur du mode film (**260vh desktop, 170vh mobile**, décision du 23/11) est donc connue au premier
   rendu. L'en-tête est `position: fixed` sur l'accueil (pas de décalage quand il devient plein).
4. **Version mobile allégée** (écran < 700 px ou pointeur tactile) : antialiasing coupé, `devicePixelRatio` plafonné à
   1,5 (2 sur desktop), tore 24×120 segments (48×220 desktop), 300 particules (900), environnement PMREM 512×256
   (1024×512), `powerPreference: low-power`, pas de suivi du pointeur.
5. **Économie CPU/GPU** : boucle `requestAnimationFrame` arrêtée quand l'intro sort de l'écran
   (IntersectionObserver) ou que l'onglet est caché ; sans WebGL, la boucle s'arrête quand la scène est immobile.
6. **« Passer l'intro »** : lien visible en permanence en mode film, ancre vers les coffrets.
7. **Poster statique (optionnel)** : si `assets/img/intro-poster.webp` existe, le thème l'affiche et le précharge avec
   `fetchpriority="high"` (filtre `charmed_intro_poster`). À produire : capture 1600×900 de l'image finale de l'intro
   (anneau ouvert), WebP qualité 70, **≤ 80 Ko** ; version 900×1600 pour mobile si besoin. Sans fichier : zéro octet,
   l'anneau CSS sert de poster.
8. **Option de gain** : construire un sous-ensemble de Three r128 (`esbuild` sur `three.module.js`, exports utilisés
   seulement) : 132 Ko gz au lieu de 149 Ko (−11 %). Testé, non livré (intérêt faible, maintenance) ; commande :
   `npx esbuild entry.js --bundle --minify --format=iife --global-name=THREE --target=es2018`.

## 3. Carrousel, file des parures, packagings

- HTML complet rendu côté serveur à partir des vrais produits (liste défilante / grille sans JS) ; le JS ne fait que
  positionner les éléments. Pas de données JSON en double dans la page.
- Hauteurs des scènes fixées en CSS (`clamp()`, `min()`) → pas de CLS à l'initialisation.
- Animations en `transform` / `opacity` / `filter` uniquement ; boucles stoppées dès que tout est immobile ou hors écran.
- Ajout au panier : un seul `fetch` Store API (le nonce n'est rafraîchi qu'en cas de refus) ; pas de jQuery,
  pas de `cart-fragments` (retiré hors pages boutique).

## 4. Images

| Usage | Taille source | Taille WP | `sizes` | Format |
|---|---|---|---|---|
| Parure détourée (coffrets, file) | 700–1760 px carré, fond transparent | `charmed-cutout` 880 + `charmed-cutout-sm` 440 + tailles WP | `(max-width:760px) 62vw, 440px` | WebP (alpha) ; AVIF si l'hébergeur le génère |
| Fiche produit (galerie) | ≥ 1200 px carré | `woocommerce_single` 1000, vignettes 300 | gérés par Woo | WebP |
| Univers (catégorie) | 900×1200 | `charmed-univers` 600×800 | `(max-width:760px) 70vw, 300px` | WebP |
| Packagings (thème) | 800–1000 px | fichiers `-600` fournis (36–59 Ko) + original | `(max-width:900px) 92vw, 560px` | WebP |
| Boîtes du carrousel (thème) | 720 px | variante 400 px (12–17 Ko) | `(max-width:760px) 46vw, 420px` | WebP |

Règles :
- WordPress 6.5+ génère `srcset` ; activer la sortie **WebP/AVIF** (filtre `image_editor_output_format` ou extension de
  l'hébergeur / LiteSpeed). Les photos Branvas téléchargées font 400×400 : pour la fiche produit, récupérer les plus
  grandes versions synchronisées par Branvas (**taille réelle à vérifier après connexion**).
- `loading="lazy"` partout (aucune image produit au-dessus de la ligne de flottaison sur l’accueil) ; `decoding="async"` ; `width`/`height`
  toujours renseignés (CLS).
- Les PNG détourés (`charmed-paris/cut/`) sont déjà en WebP 700 px (58–89 Ko) : viser ≤ 60 Ko (qualité 75).
- Images de repli des univers fournies en 400×400 : à remplacer par les images de catégorie 900×1200.

## 5. Polices

- Auto-hébergées (theme.json `fontFace`), sous-ensemble latin, `font-display: swap`, variables (une seule requête par
  famille pour toutes les graisses).
- Préchargées : Bodoni Moda romain (logo, titres) et Jost (texte). Non préchargées : Bodoni italique, DM Mono.
- Ne pas ajouter de Google Fonts via une extension (doublon + transfert de données hors UE).

## 6. Cache et serveur

- **Cache de page** pour les visiteuses non connectées, panier vide (cookie `woocommerce_items_in_cart` absent).
  Exclusions : panier, commande, mon compte, `/retractation/`, `?add-to-cart=`, `wc-ajax`, `/wp-json/`.
  Le thème est compatible : aucun nonce indispensable en dur (Store API : nonce rafraîchi par `GET /cart`),
  messages de Noël calculés au rendu → **purger le 5/12 et le 25/12**.
- **Cache objet Redis** : sessions Woo, requêtes produits ; les sélections des vitrines sont en transient versionné
  (invalidé à chaque mise à jour produit / stock / synchro Branvas).
- **OPcache**, PHP 8.2+, HTTP/2 ou 3, compression **Brotli** (sinon gzip), en-têtes `Cache-Control` 1 an + `immutable`
  pour `/wp-content/themes/charmed-paris/assets/` (fichiers versionnés `?ver=`).
- CDN optionnel (Cloudflare, Bunny — POP européens) pour les assets ; ne pas mettre en cache `/wp-json/`.
- WP-Cron par vraie tâche cron ; Action Scheduler surveillé (WooCommerce > État > Actions planifiées).

## 7. Côté WooCommerce

- Hors pages boutique, le thème retire : CSS classiques Woo, `wc-cart-fragments`, `wc-add-to-cart`, `woocommerce.js`.
  Il **conserve** l'attribution des commandes (sourcebuster) et les scripts des passerelles de paiement.
  Désactivable : `add_filter( 'charmed_trim_woo_assets', '__return_false' );`
- Mini-panier (bloc) : ses scripts sont chargés à l'ouverture.
- Limiter les extensions ; aucune extension « slider », « page builder » ou « avis » tierce (avis natifs Woo).
- Mesurer après chaque extension ajoutée (TranslatePress, cookies, SEO, paiement) : ce sont elles qui feront exploser
  le budget JS, pas le thème.

## 8. Contrôle

- Avant lancement : PageSpeed mobile sur l'accueil, une catégorie, une fiche produit, le panier ; WebPageTest
  « Moto G4 / 4G » ; vérifier l'absence de requête vers `three-r128.min.js` dans la cascade avant interaction.
- Après lancement : Search Console « Signaux Web essentiels », alerte si LCP p75 > 2,5 s ou CLS > 0,1.
- Test de non-régression : désactiver JS → l'accueil reste lisible et l'achat possible (liens `?add-to-cart=`).
