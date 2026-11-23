# CHARMED PARIS — Checklist SEO technique WooCommerce

> À dérouler en préproduction, puis à revérifier le jour du lancement. Case = action concrète. Faits fournisseur : `woocommerce/source/FAITS-BRANVAS.md`.

---

## 0. Socle

- [ ] HTTPS partout (obligatoire aussi pour la connexion Branvas), HSTS activé après vérification.
- [ ] Une seule version d'hôte : `https://charmedparis.com/` ; `www` et `http` → 301 ; domaines secondaires (.fr, charmed-paris.*) → 301 (**achat à confirmer**).
- [ ] PHP 8.2+ et WooCommerce à jour (Branvas exige Woo 3.5+), hébergement avec cache serveur et HTTP/2 ou HTTP/3 (hébergeur **à confirmer**).
- [ ] Préproduction protégée par mot de passe **et** « Demander aux moteurs de ne pas indexer ». Au lancement : décocher l'option et vérifier `robots.txt` + l'absence de `noindex` global.
- [ ] Un seul plugin SEO (Rank Math), un seul plugin de cache, aucun plugin de schéma en plus.
- [ ] **Synchro Branvas** : vérifier sur un produit test si une mise à jour Branvas (prix, stock) **écrase le titre, la description, le slug ou les images** réécrits. Si oui, désactiver la synchro de ces champs ou documenter la procédure (**à confirmer**). Le stock doit rester synchronisé (une rupture côté fournisseur passe à 0).

---

## 1. Vitesse et Core Web Vitals

Objectifs (75e centile mobile, données terrain CrUX / Search Console) : **LCP < 2,5 s, INP < 200 ms, CLS < 0,1**.

### 1.1 Intro Three.js de l'accueil (maquette `charmed-paris/charmed-site.html`, Three.js r128)

- [ ] **Ne charger Three.js que sur l'accueil**, jamais sur les catégories, fiches, panier, checkout (dequeue conditionnel `is_front_page()`).
- [ ] **Le HTML de la page existe sans la 3D** : H1, texte d'intro, liens vers les univers et la première grille de produits sont dans le HTML initial (pas injectés en JS, pas dessinés dans le canvas). Googlebot et les IA lisent ce HTML.
- [ ] **Image poster comme élément LCP** : une image statique (`box-closed.webp` ou un visuel d'écrin, 720×720 aujourd'hui) en `<img fetchpriority="high" width height>` ; le canvas se superpose une fois prêt. Ne jamais faire du canvas l'élément LCP.
- [ ] Chargement différé : `import()` dynamique de Three.js après `requestIdleCallback` / premier scroll ou interaction ; script en `type="module"` ou `defer`, jamais bloquant dans le `<head>`.
- [ ] Hébergement local de `three.min.js` (pas de CDN tiers en production, une connexion de moins), version **à mettre à jour** (r128 est ancienne), minifiée, compressée Brotli.
- [ ] Textures et modèles compressés (WebP/KTX2, glTF Draco si modèle), poids total de l'intro < 500 Ko visé (**à mesurer**).
- [ ] `prefers-reduced-motion: reduce` → pas d'animation, poster seul. Mobile bas de gamme (`navigator.hardwareConcurrency <= 4` ou `deviceMemory <= 4`) → poster seul.
- [ ] Intro limitée à **260vh (170vh sur mobile)**, lien « Passer l'intro » visible dès l'arrivée, et **aucune intro pour le trafic publicitaire** (les pubs pointent vers les fiches produits et pages d'atterrissage, pas vers l'accueil) — décision BRIEF du 23/11/2026. Pas de scroll bloqué : la page défile et le contenu reste accessible même si la 3D ne charge pas.
- [ ] Hauteur réservée pour le canvas (CSS `aspect-ratio` ou hauteur fixe) → CLS nul.
- [ ] Boucle de rendu arrêtée quand le canvas sort de l'écran (`IntersectionObserver`) et quand l'onglet est masqué → INP et batterie.

### 1.2 Général

- [ ] Cache de pages (WP Rocket, LiteSpeed Cache ou cache hébergeur — **à choisir**) avec **exclusion** de `/panier/`, `/commande/`, `/mon-compte/`, `/en/cart/`, `/en/checkout/`, `/en/my-account/` et des cookies Woo (`woocommerce_items_in_cart`, `wp_woocommerce_session_*`).
- [ ] Désactiver les fragments de panier AJAX (`wc-cart-fragments`) hors pages qui en ont besoin, ou passer au panier en blocs.
- [ ] Polices : Bodoni Moda, Jost, DM Mono **hébergées localement** (aussi pour le RGPD : pas de Google Fonts en direct), sous-ensemble latin, `font-display: swap`, préchargement de la police du H1 seulement. Limiter les graisses (2 par famille).
- [ ] CSS critique en ligne, reste différé ; JS non critique en `defer` ; supprimer les scripts de plugins inutilisés page par page.
- [ ] Scripts tiers (Meta Pixel, TikTok, GA4, widget d'avis) chargés **après consentement** et en différé.
- [ ] Mesurer avant / après : PageSpeed Insights (mobile) sur accueil, 1 univers, 1 fiche, 1 article ; suivre le rapport Core Web Vitals de Search Console.

---

## 2. Images

- [ ] **Résolution** : les photos Branvas du dépôt font **400×400 px**, les détourés `cut/` 700×700, les packagings 720–800 px. C'est faible pour le zoom produit, Google Images et Merchant Center (recommandé : 800 px et plus, 1 200 px idéalement). Vérifier si les images synchronisées dans WooCommerce sont plus grandes (**à confirmer**) ; sinon commander des échantillons et faire ses propres photos (portées, écrin), droits d'utilisation Branvas valables seulement pendant l'abonnement.
- [ ] Format : WebP pour toutes les images, AVIF si l'hébergement et le plugin le permettent (Converter for Media, ShortPixel, Imagify — **à choisir**), avec repli JPEG/PNG automatique.
- [ ] Attributs `width` / `height` sur toutes les images ; `loading="lazy"` sauf l'image LCP (1re image de la fiche, poster de l'accueil) en `fetchpriority="high"` sans lazy.
- [ ] Tailles WooCommerce : image principale 1 200 px (si source suffisante), vignettes 600 px, `srcset` actif.
- [ ] Noms de fichiers descriptifs **avant upload** : `parure-molten-art-collier-boucles-dorees-charmed-paris-1.webp`, `-portee.webp`, `-ecrin.webp`. Jamais `JSGRQR.webp` ni de nom citant le fournisseur.
- [ ] Image principale Merchant Center : fond neutre, produit seul, **sans texte ni logo incrusté ni badge promo**.
- [ ] Sitemap d'images : inclus par Rank Math.

### 2.1 Modèle d'alt text — images produit

Format : `Parure {Nom} de CHARMED PARIS : {pièces} {finition}{, pierres/perles} — {vue}`

| Vue | Exemple FR | Exemple EN |
|---|---|---|
| Packshot | « Parure Molten Art de CHARMED PARIS : collier à chaînes superposées et boucles d'oreilles dorées aux formes fluides » | « Molten Art set by CHARMED PARIS: layered gold-tone chain necklace and fluid sculptural earrings » |
| Détail | « Boucle d'oreille de la parure Solar Sphere, dôme doré parsemé d'oxydes de zirconium, vue de près » | « Close-up of a Solar Sphere stud earring, gold-plated dome with cubic zirconia » |
| Portée | « Collier et boucles Blush Dreams portés : argent 925 et moissanites roses » | « Blush Dreams necklace and earrings worn: 925 sterling silver and pink moissanite » |
| Pièces séparées | « Les trois pièces de la parure Pink Pavé : collier barrette, créoles et bague ouverte, zircones roses » | « The three Pink Pavé pieces: bar necklace, hoops and open ring with pink cubic zirconia » |

Règles : 80–125 caractères, décrire ce qu'on voit (forme, couleur, matière vérifiée), une seule fois la marque, pas de bourrage de mots-clés, jamais « plaqué or », « or », « diamant », « cristal », « waterproof ». Images décoratives (motifs, séparateurs) : `alt=""`.

### 2.2 Modèle d'alt text — packaging

| Image | Alt FR | Alt EN |
|---|---|---|
| Coffret fermé | « Coffret d'envoi blanc CHARMED PARIS fermé, logo sur le couvercle » | « Closed white CHARMED PARIS shipping box with logo » |
| Écrin ouvert | « Boîte à bijoux CHARMED PARIS ouverte avec ruban, une parure dorée posée dans son écrin » | « Open CHARMED PARIS drawer jewelry box with ribbon and a gold-tone set inside » |
| Contenu | « Contenu du colis CHARMED PARIS : boîte à tiroir, pochette en velours, chamoisine et carte d'entretien » | « Inside the CHARMED PARIS parcel: drawer box, velvet pouch, polishing cloth and care card » |
| Noël | « Emballage de Noël CHARMED PARIS : papier cadeau festif, ruban et carte de Noël » | « CHARMED PARIS Christmas packaging: holiday wrap, ribbon and Christmas card » |
| Moissanite | « Écrin en velours bleu de la ligne Joaillerie 925 » | « Blue velvet box for the sterling silver moissanite line » |

N'afficher que le packaging réellement inclus dans l'offre Branvas souscrite (carte au logo = VIP ; papier nid d'abeille = Scale/VIP ; emballage de Noël = du 20/11 au 24/12 pour les abonnées).

---

## 3. Indexation et exploration

### 3.1 robots.txt (Rank Math → Réglages généraux → Modifier robots.txt)

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /panier/
Disallow: /commande/
Disallow: /mon-compte/
Disallow: /en/cart/
Disallow: /en/checkout/
Disallow: /en/my-account/
Disallow: /*?add-to-cart=
Disallow: /*&add-to-cart=
Disallow: /*?orderby=
Disallow: /*&orderby=
Disallow: /*?s=
Disallow: /*&s=
Disallow: /*?wc-ajax=
Disallow: /*&wc-ajax=

Sitemap: https://charmedparis.com/sitemap_index.xml
```

- Les paramètres de filtre (`filter_*`, `min_price`, `max_price`) **ne sont pas bloqués** : ils sont en `noindex, follow` + canonical (si on les bloquait, Google ne verrait pas le noindex). Cf. `architecture.md` §7.
- Ne pas bloquer `/wp-content/`, `/wp-includes/` ni les fichiers CSS/JS (Google doit rendre la page).
- Robots d'IA : aucune règle = autorisés. Garder autorisés les robots de **recherche** des IA (OAI-SearchBot, PerplexityBot, Claude-SearchBot, Bingbot) pour être cité ; décision sur les robots d'**entraînement** (GPTBot, Google-Extended, ClaudeBot, CCBot) **à prendre** par la marque (les bloquer n'empêche pas d'être cité via la recherche).

### 3.2 Sitemap

- [ ] Rank Math → Sitemap : Pages, Articles, Produits, Catégories produit, Catégories d'articles ; exclus : étiquettes, attributs, auteurs, pages noindex, pages légales noindex.
- [ ] Avec TranslatePress SEO Pack : URLs EN et leurs `hreflang` ajoutées au sitemap Rank Math (`sitemap_index.xml`) ; exclure les pages EN non traduites.
- [ ] Soumettre dans Search Console et Bing Webmaster Tools ; vérifier qu'aucune URL du sitemap ne renvoie 3xx, 4xx ou noindex.
- [ ] Produits en rupture **restent** dans le sitemap (§6).

### 3.3 Canonical

- [ ] Auto-référent sur chaque page indexable, en HTTPS, sans paramètre, avec slash final.
- [ ] Pages filtrées / triées → canonical vers la catégorie sans paramètre.
- [ ] Pagination → canonical auto-référent (page 2 → page 2).
- [ ] FR et EN : chacune son propre canonical (jamais EN → FR).
- [ ] Produit présent dans plusieurs catégories : une seule URL (`/parure/{slug}/`), donc pas de problème de canonical.

### 3.4 hreflang (FR maintenant, EN sous /en/)

- [ ] TranslatePress SEO Pack génère `fr-FR`, `en`, `x-default` (→ FR) sur chaque page ; vérifier la réciprocité dans le code source et avec un outil (Screaming Frog, Ahrefs Webmaster Tools gratuits).
- [ ] Pas de hreflang vers une page noindex, redirigée ou 404 ; pas de hreflang sur les pages Woo (panier…).
- [ ] Pas de redirection automatique par langue du navigateur ou IP ; sélecteur de langue en liens `<a>`.
- [ ] Une page FR sans traduction relue : pas de balise `en` et pas d'URL EN dans le sitemap (TranslatePress afficherait le texte FR sous `/en/`).
- [ ] Plus tard, si versions UK et US distinctes (prix, contenus) : passer à `en-GB`, `en-US`, `en-CA` + `en` générique.

### 3.5 Divers

- [ ] Pages de pièces jointes → redirection vers le parent (Rank Math).
- [ ] Archives d'auteur et de date désactivées ; étiquettes noindex.
- [ ] Recherche interne noindex.
- [ ] Pages 404 utiles (liens vers univers + cadeaux + recherche), code HTTP 404 réel.
- [ ] Rank Math → moniteur 404 activé, revue hebdomadaire le premier mois.

---

## 4. Données structurées

- [ ] Product + Offer (prix TTC EUR, disponibilité synchronisée avec le stock, `itemCondition` neuf) sur chaque fiche ; `brand` = CHARMED PARIS ; `material` réel (cf. `schema/product-solar-sphere-fr.jsonld`).
- [ ] `shippingDetails` (France : préparation 1–2 j, transit 3–7 j ouvrés) et `hasMerchantReturnPolicy` (14 jours) sur les produits ou au niveau Organization.
- [ ] Organization + WebSite sur tout le site ; BreadcrumbList via le fil d'Ariane Rank Math ; FAQPage sur `/faq/` ; ItemList sur univers / cadeaux.
- [ ] **Aucun `aggregateRating` / `review`** tant qu'il n'y a pas d'avis réels affichés. Avis = **avis natifs WooCommerce** (réservés aux « propriétaires vérifiés », demande envoyée par Brevo) : Rank Math les reprend automatiquement dans le schéma Product dès qu'ils existent (cf. `schema/README.md`).
- [ ] Pas de GTIN : laisser le champ vide (ne jamais inventer d'EAN). Rank Math Pro / Woo : champ GTIN vide.
- [ ] Validation : Test des résultats enrichis + Schema Markup Validator ; puis rapports Search Console « Fiches de marchand », « Extraits de produits », « Fil d'Ariane ».

---

## 5. Google Merchant Center et fiches gratuites

- [ ] Créer le compte Merchant Center (et la vérification du site) ; connecter via le plugin officiel **Google for WooCommerce** (anciennement Google Listings & Ads) ; activer les **fiches gratuites** (onglet Shopping, Google Images, recherche).
- [ ] Pays cibles : France (EUR, FR) au lancement ; puis US et Canada (langue EN, **prix en EUR** tant qu'il n'y a pas de multidevise — vérifier que Merchant Center accepte la devise pour ces pays, sinon attendre la multidevise) ; **UK seulement après immatriculation TVA UK, sans la ligne argent 925**. Un flux par pays/langue.
- [ ] Attributs produit : `brand` = CHARMED PARIS ; **`identifier_exists` = no** (pas d'EAN/GTIN chez Branvas ; marque propre) ; `condition` = new ; `google_product_category` = Vêtements et accessoires > Bijoux > Parures de bijoux (*Jewelry Sets* — vérifier l'ID dans la taxonomie Google) ; `material`, `color` ; `product_type` = « Parures > Éclat ».
- [ ] `title` Merchant : « Parure Solar Sphere — collier dôme et puces, doré, oxyde de zirconium | CHARMED PARIS » (≤ 150 car.) ; description réécrite (pas celle du fournisseur).
- [ ] **Livraison** dans Merchant Center : France, **gratuit dès 50 € de commande, 4,90 € en dessous** (décision BRIEF), délai de préparation 1–2 j ouvrés, transit 3–7 j ouvrés ; UK : 2–5 ; US : 2–6 ; Canada : 3–6 (décomposition des délais totaux Branvas). **Pas d'option express.** Date limite de commande Noël : FR/Europe/Canada 4/12/2026, US/UK 8/12/2026.
- [ ] **Retours** dans Merchant Center : 14 jours, par courrier, frais **à confirmer**, adresse de retour à toi (France **à confirmer**).
- [ ] Pages obligatoires accessibles depuis le pied de page : CGV, Livraison et retours, Mentions légales (identité et adresse réelles), Contact (e-mail et, idéalement, téléphone), Confidentialité. Merchant Center refuse les sites « dropshipping » flous (risque « représentation trompeuse ») : identité claire, délais honnêtes, pas d'avis ni de remises fictives.
- [ ] **Aucun prix barré au lancement** (décision BRIEF). Plus tard, prix barré seulement avec un prix de référence réellement pratiqué (le plus bas des 30 derniers jours, L112-1-1), jamais le prix conseillé fournisseur. Ne pas renseigner `sale_price` dans le flux.
- [ ] Surveiller les refus (images, prix incohérents, disponibilité).

---

## 6. Ruptures et retraits de produits Branvas

Branvas ne publie pas les quantités ; rupture temporaire = stock 0 synchronisé ; réassort **sans date** ; produit retiré définitivement = supprimé de la boutique par Branvas.

| Cas | Action SEO |
|---|---|
| Rupture temporaire (stock 0) | Garder la fiche **publiée et indexée**, statut « Rupture de stock » (schéma `OutOfStock` automatique), message honnête « Momentanément indisponible, pas de date de retour annoncée », bloc « Parures proches » du même univers, inscription e-mail de retour en stock (consentement). WooCommerce → Inventaire : **ne pas** masquer les produits en rupture du catalogue, mais les mettre en fin de liste (tri). Jamais de « stock limité ». |
| Rupture > 60 jours (**seuil à valider**) | Retirer des pages cadeaux et de l'accueil ; garder la fiche (elle peut avoir des liens). |
| Produit retiré par Branvas | Avant que la fiche ne disparaisse (ou dès la suppression) : **301** de `/parure/{slug}/` (et `/en/jewelry-set/{slug}/`) vers le produit le plus proche du même univers ; sinon vers l'univers. Créer la redirection dans Rank Math → Redirections. **410** seulement s'il n'y a aucun équivalent et aucun lien entrant. |
| Changement de slug | 301 de l'ancienne URL vers la nouvelle (Rank Math le propose automatiquement) ; mettre à jour les liens internes. |
| Contrôle | Chaque semaine : rapport 404 Rank Math + « Pages » de Search Console + produits refusés dans Merchant Center. |

---

## 7. Contenus dupliqués (descriptions fournisseur)

- [ ] **Ne jamais publier la description Branvas telle quelle** (anglaise, identique chez tous les revendeurs). Branvas autorise et encourage la réécriture.
- [ ] Réécrire les 30 fiches FR (et EN) avec le gabarit :
  1. Accroche (1–2 phrases, ton de marque, tutoiement).
  2. Composition : nombre de pièces, type (collier, boucles, bague), longueurs et dimensions **relevées sur la fiche Branvas**.
  3. Matières (vocabulaire autorisé : `strategie-seo.md` §7).
  4. Comment la porter / à qui l'offrir (lien vers une page cadeau).
  5. Entretien : « À garder au sec » + lien Matières & entretien.
  6. Écrin et livraison : préparation 1–2 j ouvrés, 4–9 j ouvrés en France, droits et taxes inclus, date limite Noël en saison.
  7. Retours 14 jours, garantie légale 2 ans.
  8. Infos sécurité produit (GPSR) : nom et adresse de la personne responsable dans l'UE (toi, ou un représentant mandaté), avertissements (petites pièces, ne pas laisser à la portée des enfants — **à confirmer**), référence produit.
- [ ] Description courte Woo (sous le prix) : 2–3 puces factuelles, différentes de la description longue.
- [ ] Textes des pages univers et cadeaux uniques (aucun copier-coller entre pages).
- [ ] Versions EN rédigées en anglais natif, pas traduites automatiquement sans relecture.
- [ ] Vérifier l'unicité : recherche Google d'une phrase entre guillemets après publication ; Siteliner ou Screaming Frog pour les doublons internes.
- [ ] Ne jamais citer Branvas ni « dropshipping » côté cliente (droits d'image et positionnement marque blanche).

---

## 8. Search Console, Bing, mesure

- [ ] Search Console : propriété **domaine** (DNS) ; sitemap soumis ; vérifier l'indexation des 5 univers, des pages cadeaux et de 5 fiches avec l'outil d'inspection d'URL ; demander l'indexation de la page Noël **dès maintenant** (date limite FR 4/12/2026).
- [ ] Bing Webmaster Tools (import depuis Search Console) + IndexNow via Rank Math (Bing alimente plusieurs moteurs de réponse IA).
- [ ] GA4 + mode de consentement v2 avec bannière conforme CNIL (refus aussi simple que l'acceptation) ; mesure des conversions e-commerce.
- [ ] Rapports mensuels : requêtes, pages, CTR des titles (réécrire les titles à fort taux d'impressions et faible CTR), fiches de marchand, Core Web Vitals.

---

## 9. Conformité qui touche le SEO

- [ ] Prix TTC en euros (TVA 20 %) affichés partout en FR ; en EN, affichage selon les règles fiscales de chaque pays (**à confirmer avec un comptable**).
- [ ] Mentions légales, CGV, rétractation 14 jours (formulaire type), garantie légale de conformité 2 ans, médiateur de la consommation (**à désigner**), RGPD/cookies.
- [ ] Aucune allégation non prouvée : « sans nickel », « hypoallergénique », « waterproof », « certifié », « testé », « plaqué or », « vermeil », « fabriqué en France », « expédié de France », « livraison express ».
- [ ] Origine de l'expédition honnête dans Livraison et retours (entrepôts hors UE, droits et taxes inclus).
