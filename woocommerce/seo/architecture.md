# CHARMED PARIS — Architecture du site, URLs, maillage, multilingue

> Domaine utilisé dans les exemples : `https://charmedparis.com` (**à confirmer** : achat). Recommandation : `.com` en principal (FR à la racine, EN sous `/en/`), et acheter aussi `charmedparis.fr`, `charmed-paris.com`, `charmed-paris.fr` en **redirection 301** vers le `.com` (protection de marque, pas de contenu dupliqué). Un `.fr` géolocalise vers la France et gênerait la version anglaise.
> Version canonique : **HTTPS, sans www** (`https://charmedparis.com/`), slash final partout (réglage WordPress par défaut). `www` → 301 vers sans-www.

---

## 1. Réglages WordPress / WooCommerce

### 1.1 Permaliens (Réglages → Permaliens)

| Réglage | Valeur FR | Valeur EN (traduite avec TranslatePress SEO Pack) | Pourquoi |
|---|---|---|---|
| Structure des articles | `/journal/%postname%/` | `/en/journal/%postname%/` | Blog isolé dans un dossier (suivi Search Console par dossier), pas de date dans l'URL |
| Base de catégorie (articles) | `journal/rubrique` | `journal/topic` | Évite `/category/` |
| Base des étiquettes | `journal/tag` | `journal/tag` | Archives d'étiquettes en noindex de toute façon |
| **Base de catégorie produit** | `parures` | `jewelry-sets` | URL de catégorie = mot-clé : `/parures/eclat/` |
| Base d'étiquette produit | `parures/tag` | `jewelry-sets/tag` | noindex (pas d'étiquettes produit publiques) |
| Base d'attribut produit | (vide, archives désactivées) | — | Pas d'archives d'attributs |
| **Base produit** | Base personnalisée : `/parure/` | `/jewelry-set/` | Court, stable, **sans `%product_cat%`** : l'URL d'un produit ne change pas si on change sa catégorie, et pas de doublons quand un produit est dans plusieurs catégories (univers + cadeaux) |

**Page Boutique** (WooCommerce → Réglages → Produits) : page « Toutes les parures », slug `boutique` (EN : `shop`). Ne pas donner à la page Boutique le même slug que la base de catégorie (`parures`) : la pagination `/parures/page/2/` serait interprétée comme une catégorie et renverrait une 404.

**Pages WooCommerce** (WooCommerce → Réglages → Avancé) : Panier `/panier/` (EN `/en/cart/`), Validation `/commande/` (EN `/en/checkout/`), Mon compte `/mon-compte/` (EN `/en/my-account/`), CGV `/cgv/` (EN `/en/terms/`).

**Produits par page** : 36 (Apparence → Personnaliser → WooCommerce → Catalogue). Avec 30 produits, aucune page de catégorie n'est paginée ; la boutique ne l'est pas non plus. À revoir au-delà de 36 produits.

**Ne pas activer** l'option Rank Math « Supprimer la base de catégorie produit » ni « Supprimer la base produit » : risque de conflits avec les pages et le blog.

### 1.2 Rank Math — réglages clés

- Titres & métas → Produits : modèle `%title% | CHARMED PARIS` ; puis title **manuel** pour chaque produit (cf. CSV).
- Titres & métas → Catégories produit : modèle `%term% | CHARMED PARIS`, title manuel par catégorie.
- **noindex** : étiquettes produit, attributs, archives d'auteur, archives de date, étiquettes d'articles, résultats de recherche, pages de pagination du blog au-delà de la 1 (option « noindex paginated pages » : **non**, on garde index sur les pages 2+ ; voir §6), pièces jointes (redirigées vers le parent).
- Sitemap : inclure Pages, Articles, Produits, Catégories produit, Catégories d'articles. Exclure étiquettes, attributs, auteurs. Images incluses.
- WooCommerce : « Remove Schema Markup on Shop Archives » = non (on garde l'ItemList), « Noindex hidden products » = oui.
- Catégorie principale : renseigner pour **chaque produit** son univers (jamais une catégorie cadeau) → fil d'Ariane et schéma BreadcrumbList cohérents.

---

## 2. Arborescence complète (FR / EN)

Légende : **[I]** indexée, **[NI]** noindex, **[R]** redirection.

```
/                                         Accueil [I]                          /en/  [I]
├── /boutique/                            Toutes les parures [I]               /en/shop/
│
├── /parures/                             (base de catégorie, pas de page propre → 301 vers /boutique/) [R]
│   ├── /parures/sculpture/               Univers Sculpture (7) [I]            /en/jewelry-sets/sculpture/
│   ├── /parures/eclat/                   Univers Éclat (11) [I]               /en/jewelry-sets/sparkle/
│   ├── /parures/couleur-precieuse/       Univers Couleur précieuse (7) [I]    /en/jewelry-sets/colored-stones/
│   ├── /parures/joaillerie-argent-925/   Univers Joaillerie 925 (3) [I]       /en/jewelry-sets/sterling-silver-925/
│   ├── /parures/mixte/                   Univers Mixte (2) [I]                /en/jewelry-sets/unisex/
│   ├── /parures/dorees/                  Parures dorées (transversale) [I]    /en/jewelry-sets/gold/
│   │
│   └── /parures/idees-cadeaux/           Hub Idées cadeaux [I]                /en/jewelry-sets/gift-ideas/
│       ├── noel/                         Cadeau de Noël [I]                   christmas/
│       ├── saint-valentin/               Saint-Valentin [I]                   valentines-day/
│       ├── fete-des-meres/               Fête des mères [I]                   mothers-day/
│       ├── anniversaire/                 Anniversaire [I]                     birthday/
│       ├── mariage/                      Mariage & témoins [I]                wedding/
│       ├── moins-de-60-euros/            Budget ≤ 60 € [I si ≥ 6 produits]    (pas d'équivalent EN au lancement)
│       ├── moins-de-100-euros/           Budget ≤ 100 € [I]                   under-100/
│       └── cadeau-precieux/              Argent 925 & moissanite [I]          fine-gifts/
│
├── /parure/{slug-produit}/               30 fiches produits [I]               /en/jewelry-set/{slug}/
│
├── /ecrin-cadeau/                        L'écrin & le packaging [I]           /en/gift-box/
├── /matieres-et-entretien/               Matières & entretien (pilier) [I]    /en/materials-and-care/
├── /livraison-et-retours/                Livraison, douane, retours [I]       /en/shipping-and-returns/
├── /faq/                                 FAQ [I]                              /en/faq/
├── /notre-histoire/                      La marque [I]                        /en/our-story/
├── /contact/                             Contact [I]                          /en/contact/
├── /journal/                             Journal (blog) [I]                   /en/journal/
│   └── /journal/{slug-article}/          12 articles [I]                      /en/journal/{slug}/
│
├── /cgv/                                 CGV [I, peu de valeur mais utile aux IA et à Merchant Center]  /en/terms/
├── /mentions-legales/                    [NI]                                 /en/legal-notice/
├── /politique-de-confidentialite/        [NI]                                 /en/privacy-policy/
├── /cookies/                             [NI]                                 /en/cookies/
├── /retractation/                        Formulaire de rétractation [NI]      /en/cancellation-form/
│
├── /panier/  /commande/  /mon-compte/    [NI + exclus du sitemap + Disallow]  /en/cart/ /en/checkout/ /en/my-account/
└── /?s=… (recherche)                     [NI + Disallow]
```

### 2.1 Catégories WooCommerce à créer

| Catégorie | Slug FR | Slug EN | Parent | Rôle | Produits (SKU) |
|---|---|---|---|---|---|
| Sculpture | `sculpture` | `sculpture` | — | Univers (catégorie principale) | JS0S3W, JS8445, JSM1BZ, JS411P, JSG813, JS63WT, JSGRQR |
| Éclat | `eclat` | `sparkle` | — | Univers | JS4EXR, JS5N68, JSFAV7, JS63VP, JSJB3S, JSC940, JS4P8D, JS4AH6, JSQS6W, JS1AQ5, JS2KBV |
| Couleur précieuse | `couleur-precieuse` | `colored-stones` | — | Univers | JS0DGC, JSDYG2, JS3GGZ, JS9XM9, JSB541, JS4EPC, JSX3G6 |
| Joaillerie 925 | `joaillerie-argent-925` | `sterling-silver-925` | — | Univers | JSSFYS, JS1PPS, JSDQA1 |
| Mixte | `mixte` | `unisex` | — | Univers | JSVKMZ, JSCT1F |
| Parures dorées | `dorees` | `gold` | — | Transversale (jamais principale) | Tous les produits à finition dorée (hors « ton argenté », « ton or rose », argent 925) — liste à valider sur les fiches |
| Idées cadeaux | `idees-cadeaux` | `gift-ideas` | — | Hub | (sous-catégories) |
| Noël, Saint-Valentin, Fête des mères, Anniversaire, Mariage, Moins de 60 €, Moins de 100 €, Cadeau précieux | voir arbo | voir arbo | Idées cadeaux | Pages cadeaux (jamais principales) | Sélection manuelle : 6–12 produits par page, basée sur le prix et le style |

Règles :
- **Une catégorie principale par produit = son univers** (Rank Math → Catégorie principale).
- Une page cadeau n'est indexée que si elle a **≥ 6 produits** et un texte propre (≥ 250 mots, FAQ courte). Sinon noindex jusqu'à ce qu'elle soit remplie (« Moins de 60 € » dépend des prix finaux ; une page « moins de 50 € » n'aurait qu'un produit, Molten Art à 49 €).
- Les pages saisonnières gardent **la même URL toute l'année** (pas de `noel-2026`). Hors saison : texte « Prochaine fête des mères : … », sélection maintenue, page toujours indexée.
- **Mixte (2 produits) et Joaillerie 925 (3 produits)** : pages légères ; enrichir avec un texte expert (moissanite, argent 925, cordon) pour éviter la page « vide ». Si Mixte reste à 2 produits, l'indexer quand même mais la placer dans le menu secondaire.

### 2.2 Slugs produits

Format : `{nom-modele}-{pieces}-{finition}` en minuscules, sans accents, sans mots vides, ≤ 5–6 mots. Le slug ne contient **ni le SKU ni la marque**. Liste complète dans `mots-cles-par-page.csv` (FR) et `mots-cles-par-page-en.csv` (EN). Exemple : `/parure/molten-art-collier-boucles-dorees/` ↔ `/en/jewelry-set/molten-art-gold-necklace-earrings/`.

Les noms Royal Sapphire Halo, Emerald Dreams, Emerald Square sont renommés (Royal Blue Halo, Green Dreams, Green Square) : cf. `strategie-seo.md` §7. Si la synchronisation Branvas réécrit les noms, désactiver la mise à jour des titres côté connecteur (**à confirmer** : comportement de la synchro REST sur les champs titre/description).

---

## 3. Multilingue (FR par défaut, EN sous `/en/`)

### 3.1 Plugin : **TranslatePress** (décision arrêtée le 23/11/2026, `BRIEF.md`)

Licence Personal (≈ 99 €/an, **SEO Pack inclus** : hreflang, slugs traduits, titles/metas Rank Math traduits, sitemap multilingue). WPML et Polylang sont écartés : ils dupliquent chaque produit WooCommerce (un produit FR + un produit EN), ce qui casse la synchronisation Branvas (stock, prix, commandes).

| Point | Avec TranslatePress | À faire |
|---|---|---|
| Produits | **Un seul produit WooCommerce** par parure ; l'EN est une couche de traduction (titre, descriptions, attributs, alt, slug) | Traduire chaque champ dans l'éditeur visuel ou TranslatePress → Traduction de chaînes |
| Synchro Branvas | Stock, prix et commandes inchangés (même ID produit) | **Tester une commande passée sur `/en/` et vérifier qu'elle remonte dans Branvas** (décision BRIEF) |
| Slugs | SEO Pack : slug de chaque produit, catégorie, page traduit | Vérifier aussi la traduction des **bases** `parure` → `jewelry-set`, `parures` → `jewelry-sets`, `boutique` → `shop` (TranslatePress → Traduction de chaînes → Slugs ; **à vérifier** selon la version) ; à défaut, garder les bases FR sous `/en/` plutôt que de bricoler |
| Rank Math | SEO Pack traduit title, meta description, Open Graph, alt ; ajoute les URLs EN et les `hreflang` au sitemap Rank Math | Saisir les titles/metas EN de `mots-cles-par-page-en.csv` (rédigés en anglais natif, pas en traduction automatique) |
| Devise | **EUR au lancement**, aussi sur `/en/` | Multidevise (GBP/USD/CAD) plus tard via un plugin dédié, à réévaluer |
| E-mails et pages Woo | Chaînes traduisibles (panier, commande, e-mails transactionnels) | Relire les e-mails EN |
| Traduction automatique | Disponible (DeepL / Google) | Autorisée comme premier jet **uniquement** ; relecture obligatoire, jamais publiée brute |

Réglages TranslatePress :
- Langue par défaut : Français (France) ; langue ajoutée : Anglais, préfixe d'URL `en`. « Utiliser un sous-répertoire pour la langue par défaut » = **non** (FR à la racine).
- **Pas de redirection automatique selon la langue du navigateur ou l'IP** (Googlebot crawle surtout depuis les États-Unis et doit voir le FR). Sélecteur de langue en en-tête et pied de page (liens `<a>` crawlables) ; bandeau discret « Read this page in English? » à la place de la redirection.
- Pages non encore traduites : TranslatePress affiche le texte FR sous `/en/` → **ne pas lier / ne pas mettre dans le sitemap** les pages EN non traduites (SEO Pack → exclure du sitemap ou `noindex` temporaire). Traduire en priorité : accueil, boutique, 5 univers, 30 produits, Livraison et retours, Matières, FAQ, CGV.

### 3.2 hreflang

Chaque page indexable déclare (généré par TranslatePress SEO Pack, vérifié dans le code source) :

```html
<link rel="alternate" hreflang="fr-FR" href="https://charmedparis.com/parure/molten-art-collier-boucles-dorees/" />
<link rel="alternate" hreflang="en" href="https://charmedparis.com/en/jewelry-set/molten-art-gold-necklace-earrings/" />
<link rel="alternate" hreflang="x-default" href="https://charmedparis.com/parure/molten-art-collier-boucles-dorees/" />
```

- `fr-FR` (et non `fr`) : le marché visé est la France ; la Belgique / Suisse francophones tombent sur le FR via `x-default` / Google. Variante : `fr` si on veut viser toute la francophonie (**décision à prendre** ; code de langue dans TranslatePress → Général).
- `en` sans région : une seule version anglaise pour UK, US, CA.
- `x-default` = version FR (langue d'origine du site). Alternative : faire de x-default un sélecteur de langue — pas utile ici.
- Règles : réciprocité (FR ↔ EN), URL absolues, canonical **auto-référent dans chaque langue** (jamais un canonical EN → FR), uniquement des URLs indexables en 200. Pas de hreflang sur panier / commande / compte.
- Sitemap : Rank Math + SEO Pack ajoutent les URLs EN et leurs `hreflang` dans le sitemap ; on soumet `sitemap_index.xml`.

---

## 4. Navigation

### 4.1 En-tête (FR ; EN identique, traduit)

1. **Parures** (méga-menu) : Sculpture · Éclat · Couleur précieuse · Joaillerie 925 · Mixte · Parures dorées · **Toutes les parures**
2. **Idées cadeaux** : *[mise en avant saisonnière en 1re position : Noël jusqu'au 24/12, puis Saint-Valentin, puis Fête des mères]* · Anniversaire · Mariage · Moins de 60 € · Moins de 100 € · Cadeau précieux
3. **L'écrin** (`/ecrin-cadeau/`)
4. **Matières & entretien**
5. **Journal**
+ icônes Recherche · Compte · Panier · sélecteur **FR | EN**

Bandeau d'annonce (fin d'année) : « Commande avant le 4 décembre pour une livraison avant Noël en France. Droits et taxes inclus. » (EN : « Order by December 8 for Christmas delivery to the US & UK — December 4 for Canada. Duties included. »). Aucune promesse au-delà.

### 4.2 Pied de page

- Parures : 5 univers + Parures dorées
- Cadeaux : les 8 pages cadeaux
- Aide : Livraison et retours · FAQ · Matières & entretien · Contact · Rétractation
- Marque : Notre histoire · L'écrin · Journal
- Légal : CGV · Mentions légales · Confidentialité · Cookies · Gérer mes cookies

Liens de pied de page en HTML (pas en JS), même ordre dans les deux langues.

---

## 5. Fil d'Ariane

Rank Math → Réglages généraux → Fil d'Ariane : activé, séparateur `›`, libellé accueil « Accueil » / « Home », « Afficher la catégorie principale » = oui. Remplacer le fil WooCommerce du thème par `rank_math_the_breadcrumbs()` (ou le bloc Rank Math) pour n'avoir qu'**un seul** BreadcrumbList.

| Type de page | Fil d'Ariane |
|---|---|
| Univers | Accueil › Parures › Éclat |
| Page cadeau | Accueil › Idées cadeaux › Noël |
| Fiche produit | Accueil › Parures › Sculpture › Parure Molten Art (catégorie principale = univers) |
| Article | Accueil › Journal › Titre de l'article |
| Page éditoriale | Accueil › Matières & entretien |

« Parures » pointe vers `/boutique/` (la base `/parures/` est redirigée).

---

## 6. Maillage interne

**Principe : chaque page reçoit des liens de 3 niveaux (menu, contexte, pied de page) et en émet vers le niveau au-dessus et à côté.**

| Depuis | Vers | Comment |
|---|---|---|
| Accueil | 5 univers, hub cadeaux + page saisonnière, L'écrin, Matières, 4–8 produits | Blocs « Les univers », « Offrir », sélection produits ; textes d'ancre descriptifs (« parures dorées Sculpture », pas « en savoir plus ») |
| Univers | Ses produits ; 2 univers voisins ; Matières & entretien (ancre matière : « laiton doré », « argent 925 et moissanite synthétique ») ; 1–2 pages cadeaux | Texte sous la grille + bloc « Explore aussi » |
| Page cadeau | 6–12 produits ; 2–3 univers ; L'écrin ; Livraison (date limite) ; 1 article guide | Intro + sélection + FAQ |
| Fiche produit | Univers (fil d'Ariane + lien dans la description) ; 3–4 produits du même univers (« Tu aimeras aussi » = produits apparentés / ventes croisées) ; 1–2 pages cadeaux pertinentes ; Matières & entretien ; Livraison et retours | Ventes croisées WooCommerce pour l'offre « 2e parure » (**à valider**) |
| Article | 1 page cadeau + 1 univers + 2–3 produits ; 1 autre article | Liens dans le corps, dans les 30 % premiers du texte pour le principal |
| Matières & entretien | Chaque univers + articles matières | Tableau par univers avec liens |
| FR ↔ EN | Sélecteur de langue vers la **page équivalente** (pas vers l'accueil) | TranslatePress |

Règles : 3 à 10 liens contextuels par page ; aucune page indexable à plus de 3 clics de l'accueil ; pas de `nofollow` interne ; ancres variées et naturelles ; vérifier les pages orphelines tous les mois (Rank Math → Analyse des liens ou Screaming Frog).

---

## 7. Filtres, tri, paramètres, pagination

Avec 30 produits, **pas de filtres à facettes multiples** au lancement. Seulement :
- tri WooCommerce (`?orderby=`) ;
- éventuellement un filtre « Finition » (doré / ton argenté / argent 925) et « Prix » sur `/boutique/`.

| URL | Traitement |
|---|---|
| `?orderby=…`, `?min_price=`, `?max_price=`, `?filter_*`, `?query_type_*`, `?rating_filter=` | `noindex, follow` + canonical vers l'URL sans paramètre (Rank Math le fait pour les paramètres connus ; vérifier) + `Disallow` dans robots.txt pour `orderby` et `add-to-cart` |
| `?add-to-cart=…` | Disallow + liens d'ajout au panier en `rel="nofollow"` (natif Woo) |
| `?s=…&post_type=product` | noindex + Disallow |
| `?utm_*`, `?gclid`, `?fbclid` | Canonical vers l'URL propre (auto) |
| Combinaison de filtres utile pour le SEO (ex. « parure dorée ») | **Ne pas l'indexer en tant que filtre** : en faire une vraie catégorie (c'est le cas de `/parures/dorees/`) |
| Pagination `/page/2/` (blog, boutique au-delà de 36 produits) | `index, follow`, **canonical auto-référent** (pas vers la page 1), titles uniques « – Page 2 », pas de texte d'intro répété |
| Variations produit (s'il y en a : **à confirmer**, ex. bague ajustable) | Une seule URL produit, pas d'URL par variation indexée (`?attribute_…` → canonical produit) |
| Pièces jointes / pages média | Rank Math : redirection vers le parent |

---

## 8. Pages à ne pas indexer

| Page | Méthode |
|---|---|
| Panier, Commande, Mon compte (+ endpoints `commande-recue`, `mot-de-passe-perdu`, etc.) | noindex (WooCommerce + Rank Math), exclus du sitemap, Disallow robots, **exclus du cache** |
| Recherche interne | noindex + Disallow |
| Mentions légales, Confidentialité, Cookies, Formulaire de rétractation | noindex, follow (restent liés en pied de page, obligatoires) |
| Étiquettes produit / d'articles, archives auteur et date, attributs | noindex (Rank Math) ou désactivées |
| Pages cadeaux avec < 6 produits | noindex temporaire |
| Version EN d'un produit non traduit | Non publiée |
| Pages de remerciement, landing pages publicitaires dupliquées | noindex |
| Environnement de préproduction | Protégé par mot de passe (HTTP auth) **et** « Demander aux moteurs de ne pas indexer » ; jamais seulement l'un des deux |

Mettre la CGV en **indexable** : elle sert à Merchant Center et aux IA (politique de retour, délais).

---

## 9. Redirections à prévoir dès le lancement

- `www` → sans-www, `http` → `https`, domaines secondaires → `.com` (au niveau DNS / hébergeur, en 301).
- `/parures/` → `/boutique/` ; `/en/jewelry-sets/` → `/en/shop/`.
- `/shop/` (FR, s'il est tapé) → `/boutique/`.
- Produit retiré définitivement du catalogue Branvas → 301 vers le produit le plus proche du même univers, sinon vers l'univers (détail dans `technique-checklist.md`).
- Gérer toutes les redirections dans **Rank Math → Redirections** (un seul endroit).
