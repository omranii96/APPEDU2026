# CHARMED PARIS — Stratégie SEO (FR par défaut + EN sous /en/)

> Document du consultant SEO. Sources, par ordre de priorité : `woocommerce/source/FAITS-BRANVAS.md` (gagne en cas de conflit ; sa section « Règles de rédaction légales » et `woocommerce/legal/points-de-vigilance.md` priment sur tout le reste), `woocommerce/source/branvas-faq/`, `woocommerce/BRIEF.md`, `branvas-photos/bundles.csv`. Tout le reste est marqué **à confirmer**.
> Rédigé le 22/11/2026. Fichiers liés : `architecture.md`, `mots-cles-par-page.csv`, `mots-cles-par-page-en.csv`, `schema/`, `technique-checklist.md`, `plan-editorial.md`.

---

## 1. Point de départ

| Sujet | Fait vérifié | À confirmer |
|---|---|---|
| Offre | Uniquement des **parures** : 30 retenues sur 81, 5 univers : Sculpture (7), Éclat (11), Couleur précieuse (7), Joaillerie 925 (3), Mixte (2) | Composition exacte (nombre de pièces, longueurs, poids) : à relever sur chaque fiche Branvas, qui fait foi |
| Métal doré | Laiton doré **à l'or véritable par électrolyse** + revêtement anti-ternissement. Pas massif, pas vermeil. Épaisseur en microns **non publiée** → en français **« doré »** ; « doré à l'or X carats » quand le carat est relevé ; « doré à l'or fin » **seulement si 24 carats** | Carat de la dorure par produit ; métal de base exact des pièces Liquid Sculpture (le CSV cite « eco-zinc alloy » pour Baroque Pearl Flow) |
| Argent | Argent 925 véritable (Branvas annonce un poinçon 925) | Ne pas écrire « poinçonné » sans document du produit (règle juridique). **UK : ligne 925 exclue** tant que le poinçonnage britannique n'est pas vérifié (obligatoire au-delà de 7,78 g) |
| Moissanite | Moissanite créée en laboratoire → à nommer **« moissanite synthétique »** (décret 2002-65) ; EN « lab-grown moissanite ». Pierres ≥ 0,1 ct livrées avec **certificat GRA**. Carats exprimés en équivalent diamant (DEW) | Poids des pierres de nos 3 parures (≥ 0,1 ct ou non) |
| Perles | Perles **de culture d'eau douce véritables**, sauf si la fiche dit « simulated pearl » | Vérifier les fiches Baroque Pearl Flow, Liquid Art Pearl ; nature des « white beads » de Petal Bloom |
| Nickel / plomb / hypoallergénique | Branvas dit « nickel-safe, lead-free », **mais en UE interdiction d'écrire « sans nickel », « sans plomb », « hypoallergénique », « certifié », « testé » sans rapport par SKU** | Rapports de test (300–800 $ / article) |
| Eau | Retirer avant douche/baignade ; eau, savon, chlore réduisent la durée de la dorure → **« à garder au sec »** | — |
| Expédition | Depuis des entrepôts **aux États-Unis et en Chine**, **aucun entrepôt UE**. DHL (UE), USPS (US). **Un seul mode, pas d'express, pas de date garantie**. Préparation 1–2 jours ouvrés | — |
| Délais totaux (9 colis sur 10, jours ouvrés) | France 4–9 ; UK 3–7 ; US 3–8 ; Canada 4–8 ; Australie 3–8 ; reste du monde 4–12 | — |
| Droits | **DDP** : droits et taxes d'import payés, rien à payer à la livraison. 101 pays | TVA de la vente à la charge de CHARMED PARIS (FR, et UK/US/CA si on y vend : **à confirmer avec un comptable**) |
| Noël 2026 | Packaging de Noël offert du 20/11 au 24/12 (abonnées). **Date limite de commande pour livraison avant Noël : Europe et Canada vendredi 4 décembre 2026 ; US/UK/Australie mardi 8 décembre** | — |
| Packaging | Carton d'envoi au logo + **boîte à bijoux à tiroir avec ruban** (logo, beige métallisé), pochette velours, chamoisine, carte avec conseils d'entretien (logo en VIP), bordereau sans prix. **Une seule boîte à bijoux par commande** : les parures suivantes arrivent en sachets scellés. **Pas de message cadeau** (sauf carte VIP). Moissanite : **écrin velours bleu** (sans logo) | Visuels réels avec logo : `charmed-paris/img/pack-*.webp` |
| Personnalisation | **Aucune gravure ni personnalisation** possible | — |
| Pierres d'Éclat / Couleur précieuse | Zircone cubique → à nommer **« oxyde de zirconium »** ou « zircone » (« zircon » = autre pierre, naturelle : à éviter) ; EN « cubic zirconia » | — |
| Codes-barres | **Pas d'EAN/GTIN** → Merchant Center : `identifier_exists = no` (marque propre) | — |
| Retours | Branvas couvre seulement colis endommagé / défaut / mauvais article (10 jours). **La rétractation 14 jours (UE et UK) est à la charge de CHARMED PARIS**, retour à une adresse fournie par la marque | Adresse de retour (France idéalement), frais de retour client ou offerts |
| Prix | Fourchettes maquette : Sculpture 49–59 €, Éclat 59–79 €, Couleur précieuse 69–89 €, Joaillerie 925 149–249 €, Mixte 49 € | Prix définitifs EUR, GBP, USD, CAD |
| Offres panier | « Livraison offerte dès 50 € », « 2e parure −15 % » (maquette). **Prix barrés interdits au lancement** (L112-1-1), jamais le prix conseillé Branvas en prix barré, pas de faux Black Friday | À valider ; règle Branvas pour un seuil : 20–30 % au-dessus du panier moyen ; la 2e parure n'a pas son propre écrin (à dire) |
| Avis | Aucun ; Branvas n'en fournit pas | Outil d'avis réel (Judge.me, etc.) |
| Domaine / marque | Domaines libres au 22/11/2026 | Achat, dépôt INPI/EUIPO (et UKIPO/USPTO si EN) |

**Conséquence SEO :** domaine neuf, zéro autorité, zéro avis, 30 produits, deux langues. Les têtes de requête (« parure bijoux », « jewelry set ») sont inaccessibles à court terme. On vise la **longue traîne**, les **pages cadeaux** (occasion + budget), les **univers** (style + matière), des **contenus matières factuels** (conversion + citation par les IA) et **Google Merchant Center** pour apparaître dans Shopping sans autorité de domaine.

---

## 2. Ce que montrent les SERP françaises (observation du 22/11/2026)

Requêtes observées : « parure bijoux femme collier boucles d'oreilles doré », « coffret bijoux femme idée cadeau parure », « parure argent 925 moissanite femme », « idée cadeau bijoux femme moins de 50 euros », « bijoux fantaisie dorés marque française ». **Aucune donnée de volume** disponible (pas d'accès Keyword Planner / Semrush / Ahrefs) : les priorités sont qualitatives (haute / moyenne / basse), **à recaler avec Search Console après 2–3 mois**.

1. **Têtes de requête tenues par les gros acteurs** : Galeries Lafayette, Histoire d'Or, Maty, Swarovski, Zalando, Cdiscount, Auchan, Vinted, Le Dénicheur.
2. **« Coffret bijoux femme » est ambigu** (coffrets parfum Sephora, boîtes de rangement, parures en coffret) → seulement en secondaire, sous la forme « parure en coffret cadeau ».
3. **Le vocabulaire matière domine** : « doré à l'or fin », « plaqué or 18 carats », « acier inoxydable doré », « argent 925 », « zirconias / oxydes de zirconium ». Beaucoup de concurrents emploient ces termes sans y avoir droit ; nous, non (« doré », « oxyde de zirconium », « moissanite synthétique »). Une page « Matières & entretien » factuelle est un levier SEO, de confiance et de citation IA.
4. **L'acier inoxydable est l'argument concurrent** (« ne ternit pas », « résiste à l'eau »). Aucune de nos 30 parures n'est en acier : on ne joue pas sur ce terrain, on assume « à garder au sec ».
5. **Parures argent 925** : surtout argent + oxydes de zirconium (Maty ~70 €, Morellato ~119 €, Pd Paola ~145 €, prix vus le 22/11/2026). Les **parures moissanite complètes sont quasi absentes** (surtout des bagues isolées) → niche exploitable : « parure moissanite », « parure argent 925 moissanite ». Argument factuel différenciant : moissanite synthétique, argent 925, certificat GRA pour les pierres ≥ 0,1 ct (**à confirmer par produit**).
6. **Pages « cadeau à moins de X € »** présentes chez Nomination, Petite Mendigote, Histoire d'Or : sélection courte, filtrée par budget.
7. **Concurrents de positionnement** (fantaisie dorée, ~25–150 €) : Zag Bijoux, Agatha Paris, Gas Bijoux, Bohm Paris, Ikita, Huguette Paris, Emoi Emoi, Caroline Najman.

> **Vigilance « Paris » et origine** : expédition depuis les États-Unis ou la Chine. Ne jamais écrire « expédié de France », « fabriqué à Paris », « made in France », « créé dans notre atelier », « bijoux français ». Sur le site, dire « Expédié depuis nos partenaires logistiques internationaux, droits et taxes inclus » (formulation **à valider**), sans citer Branvas.

---

## 3. Intentions de recherche FR

Priorité : **H** = haute (dès le lancement), **M** = moyenne (mois 2–6), **B** = basse (plus tard). Sans volumes chiffrés.

### 3.1 Transactionnelles

| Requête | Page cible | Priorité | Commentaire |
|---|---|---|---|
| parure bijoux femme | `/boutique/` | M | Très concurrentielle |
| parure collier et boucles d'oreilles | `/boutique/` + univers | H | Formulation exacte de l'offre |
| ensemble collier boucles d'oreilles | `/boutique/` | H | Synonyme courant, moins disputé |
| parure dorée | `/parures/dorees/` | H | Majorité du catalogue (« parure dorée à l'or fin » : non ciblée, sauf pièces 24 ct) |
| bijoux fantaisie dorés | `/parures/dorees/` + Éclat | M | Large mais vocabulaire de la cible |
| parure oxyde de zirconium / parure zircone (et « parure zircon », capté par l'article explicatif) | `/parures/eclat/` + article | H | Correspond à Éclat ; « zircon » n'est jamais écrit comme matière de nos produits |
| parure pierres de couleur / zircone rose, bleue, verte | `/parures/couleur-precieuse/` | M | Longue traîne par couleur |
| parure argent 925 moissanite / parure moissanite | `/parures/joaillerie-argent-925/` | H | Niche peu couverte |
| parure argent 925 femme | `/parures/joaillerie-argent-925/` | M | Concurrence Maty / Histoire d'Or |
| bijoux sculpturaux / bijoux organiques dorés | `/parures/sculpture/` | M | Vocabulaire tendance |
| parure perles d'eau douce / perles baroques | `/parures/sculpture/` | M | Possible depuis la confirmation Branvas (perles de culture d'eau douce), **à vérifier par fiche** |
| collier cordon pendentif lune | `/parures/mixte/` + fiche | B | 2 produits |
| parure avec bague | fiches Pink Pavé, Crescent Glow | B | 2 produits avec bague selon le CSV |
| [nom de produit] + charmed paris | fiches | H | Requêtes de marque |

### 3.2 Cadeau

| Requête | Page cible | Priorité | Saison |
|---|---|---|---|
| idée cadeau femme bijoux | `/parures/idees-cadeaux/` | H | Toute l'année |
| idée cadeau noël femme bijoux | `/parures/idees-cadeaux/noel/` | **H, urgent** | Jusqu'au 4/12/2026 pour une livraison garantie avant Noël en France |
| coffret cadeau bijoux femme / parure en coffret | `/parures/idees-cadeaux/` + `/ecrin-cadeau/` | H | Toute l'année |
| cadeau saint valentin femme bijoux | `/parures/idees-cadeaux/saint-valentin/` | H | Janvier → 14/02 |
| cadeau fête des mères bijoux | `/parures/idees-cadeaux/fete-des-meres/` | H | Avril → fin mai (date 2027 **à confirmer**, a priori dim. 30/05/2027) |
| cadeau anniversaire femme bijoux (30, 40, 50 ans) | `/parures/idees-cadeaux/anniversaire/` | M | Toute l'année |
| cadeau bijoux moins de 50 € | `/parures/idees-cadeaux/moins-de-50-euros/` | M | **Ouvrir seulement si ≥ 6 parures ≤ 50 € TTC**, sinon « moins de 60 € » |
| cadeau bijoux moins de 100 € | `/parures/idees-cadeaux/moins-de-100-euros/` | M | Toute l'année |
| bijoux témoin de mariage / parure invitée mariage | `/parures/idees-cadeaux/mariage/` | M | Mars–septembre |
| cadeau bijou précieux femme | `/parures/idees-cadeaux/cadeau-precieux/` | B | Fin d'année |
| quel bijou offrir à sa femme | article | H | Toute l'année |

### 3.3 Informationnelles

| Requête | Page cible | Priorité |
|---|---|---|
| différence plaqué or et doré à l'or fin | `/matieres-et-entretien/` + article | H |
| moissanite c'est quoi / moissanite synthétique ou diamant | article + univers 925 | H |
| comment entretenir bijoux dorés | `/matieres-et-entretien/` + article | H |
| peut-on se doucher avec des bijoux dorés | article (réponse honnête : non) | M |
| zircon ou oxyde de zirconium (différence) | article | M |
| perle de culture d'eau douce c'est quoi | article / section matières | M |
| délai livraison / droits de douane bijoux commandés hors UE | `/livraison-et-retours/` + FAQ | M (réassurance DDP) |
| longueur collier femme | guide (dimensions **à confirmer**) | B |

### 3.4 Requêtes à NE PAS cibler

- « bijoux waterproof », « bijoux qui ne craignent pas l'eau », « bijoux acier inoxydable », « bijoux qui ne noircissent pas / ne ternissent pas »
- « plaqué or » comme mot-clé produit (épaisseur non publiée) — admis seulement dans un article explicatif
- « vermeil », « or massif », « sans nickel », « hypoallergénique », « bijoux pour peau sensible », « certifié », « testé dermatologiquement »
- « zircon », « saphir », « émeraude », « diamant » comme matière ; « moissanite » sans « synthétique » (« taille émeraude » = forme de coupe, admis)
- « bijou personnalisé », « bijou gravé », « prénom », « message cadeau » (pas de personnalisation, pas de message cadeau hors carte VIP)
- « promo », « prix barré », « soldes », « Black Friday » fictifs
- « livraison express », « livraison 24 h / 48 h », « expédié de France », « made in France »

---

## 4. Stratégie anglaise (/en/ — UK, US, Canada)

### 4.1 Pourquoi et comment

- Branvas livre 101 pays en DDP, avec des délais **plus courts vers les US (3–8 j) et le UK (3–7 j)** que vers la France. Le marché anglophone est donc logistiquement crédible.
- **Une seule version anglaise** au lancement, `hreflang="en"` (pas de `en-GB` / `en-US` séparés tant qu'on n'a pas de prix, de livraison et de contenus distincts). Scinder en `/en-gb/` et `/en-us/` seulement si le trafic le justifie.
- **Orthographe** : « jewelry » (US) dans les URLs et les titles, car c'est le plus gros marché de recherche ; « jewellery » (UK, Canada) dans les textes, les metas et les mots-clés secondaires. Google rapproche les deux formes, mais on couvre les deux explicitement. Décision **à valider**.
- **Ne pas traduire mot à mot** : les titles EN reprennent les formulations natives (« necklace and earring set », « gift for her », « gift set »), pas « parure ».
- **Devise** : prix affichés en GBP pour le UK, USD pour les US, CAD pour le Canada (WooCommerce Multilingual & Multicurrency, cf. `architecture.md`), en **prix ronds saisis à la main**, pas en conversion automatique. Prix **à confirmer**.
- **Taxes** : TVA UK sur les ventes B2C ≤ 135 £ à collecter par le vendeur, sales tax US selon les États, GST/HST au Canada : **à confirmer avec un comptable avant d'ouvrir chaque pays**. L'affichage TTC / HT en dépend.
- **Royaume-Uni : ne pas ouvrir avant l'immatriculation TVA UK** (règle juridique), et **ligne argent 925 exclue au UK** tant que le poinçonnage britannique n'est pas vérifié (obligatoire au-delà de 7,78 g). Ordre d'ouverture recommandé : US et Canada d'abord, UK ensuite. La version `/en/` reste indexable pour tous les anglophones ; les pays bloqués sont gérés au checkout et dans Merchant Center.
- **Vocabulaire EN autorisé** (Branvas) : « gold-plated » (accepté), « 14K gold-plated » seulement si le carat est relevé sur la fiche, « 925 sterling silver », « lab-grown moissanite », « genuine cultured freshwater pearls », « cubic zirconia ». **Interdits** : « gold vermeil », « solid gold », « waterproof », « tarnish-free », « hypoallergenic », « nickel-free » (la version EN est aussi lue dans l'UE et au UK), « diamond », « handmade in Paris », « ships from France », « express shipping ».
- Le contenu EN doit être **réécrit** (même ton, en anglais natif) : tutoiement → « you » chaleureux et direct ; signature « Open it. Let yourself be charmed. » (traduction **à valider**).

### 4.2 Intentions EN prioritaires

| Query (EN) | Page cible | Priorité | Note |
|---|---|---|---|
| necklace and earring set | `/en/shop/` | H | Équivalent naturel de « parure » |
| jewelry set for women / jewellery set | `/en/shop/` | M | Concurrentiel (Amazon, Etsy, Pandora, Swarovski) |
| gold jewelry set / gold-plated necklace and earring set | `/en/jewelry-sets/gold/` | H | |
| cubic zirconia jewelry set | `/en/jewelry-sets/sparkle/` | H | |
| moissanite jewelry set / sterling silver moissanite necklace and earrings | `/en/jewelry-sets/sterling-silver-925/` | H | Niche ; non vendu au UK pour l'instant |
| sculptural gold jewelry / organic gold jewelry | `/en/jewelry-sets/sculpture/` | M | |
| freshwater pearl jewelry set | `/en/jewelry-sets/sculpture/` | M | Selon fiches |
| jewelry gift set for her / jewelry gift box | `/en/jewelry-sets/gift-ideas/` | H | |
| christmas jewelry gifts for her | `/en/jewelry-sets/gift-ideas/christmas/` | **H, urgent** | Order-by US/UK 8/12/2026, Canada 4/12/2026 |
| valentine's day jewelry gifts for her | `/en/jewelry-sets/gift-ideas/valentines-day/` | H | 14/02/2027 |
| mother's day jewelry gift | `/en/jewelry-sets/gift-ideas/mothers-day/` | H | UK Mothering Sunday 07/03/2027, US/CA 09/05/2027 (**à confirmer**) |
| birthday jewelry gift for her | `/en/jewelry-sets/gift-ideas/birthday/` | M | |
| bridesmaid jewelry set / wedding guest jewelry | `/en/jewelry-sets/gift-ideas/wedding/` | M | |
| jewelry gifts under 100 | `/en/jewelry-sets/gift-ideas/under-100/` | M | Seuils par devise à fixer après les prix |
| is gold-plated jewelry waterproof / can you shower with gold-plated jewelry | article EN | M | Réponse honnête : non |
| what is moissanite | article EN | H | |

### 4.3 Calendrier EN spécifique

Black Friday 27/11/2026 (en cours) ; order-by Noël US/UK **8/12/2026**, Canada **4/12/2026** ; Saint-Valentin 14/02/2027 ; Mothering Sunday UK 07/03/2027 ; Mother's Day US/CA 09/05/2027 (dates 2027 **à confirmer**).

---

## 5. Positionnement réaliste pour un domaine neuf

**Promesse en une phrase :** *la parure prête à offrir* — un collier et ses boucles assortis, dans un écrin, avec des matières expliquées honnêtement et les droits de douane déjà payés.

1. **Capter la marque et les 30 noms de produits** (FR + EN).
2. **Pages cadeaux = cœur du trafic non-marque** (occasion × budget × style). Intro utile (≥ 250 mots), sélection éditorialisée, FAQ courte, liens vers les univers, **date limite de commande visible** en période de fête.
3. **Univers = catégories expertes** : style + matière, 300–500 mots sous la grille, 2 lignes au-dessus.
4. **Matières & entretien = page pilier** : tableau factuel par univers (métal, dorure, pierres, perles, entretien) — réponse aux comparaisons qui dominent les SERP, source citable par les IA.
5. **Livraison & retours** : DDP, délais par pays (9 colis sur 10), pas d'express, rétractation 14 jours. Réassurance clé pour un envoi hors UE.
6. **Journal = 12 contenus FR** (+ adaptation EN des 5 plus universels), chacun lié à 1 page cadeau + 1 univers + 2–3 produits.
7. **Google Merchant Center (fiches gratuites)** FR + UK/US/CA dès le lancement.
8. **Netlinking léger et propre** (budget **à confirmer**) : partenariats créatrices avec lien (`rel="sponsored"` si rémunéré), RP cadeaux de Noël / fête des mères. Jamais de fausses mentions presse.

Horizon indicatif, sans garantie : marque dès l'indexation ; longue traîne cadeaux / univers en 3–6 mois ; têtes de requête ≥ 12 mois.

---

## 6. Plugin SEO : **Rank Math** (recommandé)

| Critère | Rank Math (gratuit) | Yoast (gratuit) |
|---|---|---|
| Schéma Product WooCommerce | Généré automatiquement (Pro pour champs avancés) | Complet seulement avec **Yoast WooCommerce SEO (payant)** |
| Redirections 301 + moniteur 404 | Inclus | Yoast Premium |
| Plusieurs mots-clés par page | Oui | Premium |
| noindex granulaire (tags, attributs, archives) | Oui | Oui |
| Fil d'Ariane avec catégorie principale | Oui | Oui |
| Compatibilité WPML (titles, metas, sitemap, hreflang) | Officielle | Officielle |

**Choix : Rank Math gratuit au lancement**, Pro (tarif **à confirmer**) seulement pour des schémas personnalisés avancés. Raison : redirections (indispensables vu les ruptures et retraits de produits côté fournisseur), schéma Woo et catégorie principale inclus sans surcoût.

Modules à activer : Schema, WooCommerce, Sitemap, Redirections, 404 Monitor, Image SEO, Instant Indexing (IndexNow / Bing), Breadcrumbs. À désactiver : Local SEO (pas de boutique physique, **à confirmer**), News Sitemap, Video Sitemap.

**Un seul plugin SEO**, aucun plugin de schéma en plus (doublons de JSON-LD).

---

## 7. Règles éditoriales (FR et EN)

**Ton :** tutoiement (FR) / « you » direct (EN), phrases courtes, chaleureux, pas de superlatifs creux.

| Branvas dit (CSV / fiche) | FR | EN | Jamais |
|---|---|---|---|
| gold-plated, gold-toned, warm gold finish | « doré » | « gold-plated » | « plaqué or », « vermeil », « or massif », « doré à l'or fin » (sauf 24 ct) / « vermeil », « solid gold » |
| 14K / 18K / 24K gold plated (carat relevé sur la fiche) | « doré à l'or 14 carats » (ou 18) ; « doré à l'or fin » **uniquement** pour 24 carats | « 14K gold-plated » | « or 14 carats » / « 14K gold » |
| white gold plated | « ton argenté » (nature de la dorure **à confirmer**) | « silver-tone » | « or blanc », « argent » / « white gold », « silver » |
| rose gold | « ton or rose » | « rose gold-tone » | « or rose » / « rose gold » seul |
| eco-brass / eco-zinc alloy | « laiton » / « alliage de zinc » | « brass » / « zinc alloy » | « recyclé », « éco-responsable » (sans preuve) |
| sterling silver | « argent 925 » | « 925 sterling silver » | « poinçonné », « certifié » sans document du produit ; « argent massif » |
| moissanite | « moissanite synthétique » (« créée en laboratoire » en complément) ; « certificat GRA » seulement si pierre ≥ 0,1 ct confirmée ; expliquer le poids DEW | « lab-grown moissanite », « GRA certificate » | « moissanite » seule, « diamant », « diamant de synthèse » / « diamond » |
| cubic zirconia, CZ, crystal | « oxyde de zirconium » ou « zircone » (titres courts) | « cubic zirconia » | « zircon » (pierre naturelle différente), « cristal », « saphir », « émeraude » / « crystal », « sapphire », « emerald » (comme matière) |
| pearls | « perles de culture d'eau douce » (sauf fiche « simulated pearl » → « perles d'imitation ») | « genuine cultured freshwater pearls » | « perles naturelles », « perles fines » / « natural pearls » |

**Mentions obligatoires sur chaque fiche (FR) :** « À garder au sec », composition, matières, « Expédiée sous 1 à 2 jours ouvrés, livrée en 4 à 9 jours ouvrés en France (9 colis sur 10) », « Droits et taxes inclus », « Une boîte à bijoux par commande », rétractation 14 jours, garantie légale 2 ans, prix TTC, et en saison la **date limite de commande pour Noël (4 décembre 2026)**. Infos GPSR (nom, adresse postale et e-mail de CHARMED PARIS comme opérateur responsable, référence produit, avertissements) : cf. `technique-checklist.md`.

**Noms de produits :** nom de modèle (anglais, cohérent FR/EN) + descripteur. Trois noms citent une pierre fine alors que ce sont des oxydes de zirconium : **Royal Sapphire Halo, Emerald Dreams, Emerald Square** → renommer « Royal Blue Halo », « Green Dreams », « Green Square » (risque de dénomination trompeuse des pierres ; décret n° 2002-65 en France — **à confirmer par un juriste**). « Emerald Cut Halo » peut rester (« taille émeraude » = coupe). Les deux CSV utilisent déjà ces noms.

**Interdits absolus :** faux avis, notes, compteurs de ventes, « stock limité », comptes à rebours, logos presse, **prix barrés et « promos » fictives** (aucun prix de référence au lancement), « livraison express », « message cadeau », « un écrin par parure », mention de Branvas côté cliente. Golden Luxe Crystal est aussi renommé « Golden Luxe Drop » (éviter « crystal »).

---

## 8. KPI et pilotage

- Search Console (propriété domaine, rapports par dossier `/` et `/en/`) : clics marque vs non-marque, requêtes cadeaux, pages indexées, rapports « Fiches de marchand » et « Extraits de produits ».
- Merchant Center : produits approuvés / refusés par pays, clics des fiches gratuites.
- GA4 avec consentement (CNIL) : conversion par page d'entrée (cadeaux vs univers vs articles), par langue.
- Revue mensuelle : recaler les priorités H/M/B sur les impressions réelles de Search Console.

## Sources observées (SERP du 22/11/2026)

- [Galeries Lafayette — Parures de bijoux femme](https://www.galerieslafayette.com/c/femme/bijoux-et-joaillerie/parures)
- [Swarovski — Parure Favor ton doré](https://www.swarovski.com/fr-FR/p-5528953/Parure-Favor-Ton-dore-Placage-de-ton-or)
- [Cdiscount — parures or femme](https://www.cdiscount.com/bijouterie/r-bijoux+femme+en+or+parure.html)
- [Maty — parure argent 925 zirconias](https://www.maty.com/en/Bijoux/0286699/parure-argent-925-collier-bracelet-pampilles-zirconias.html)
- [Galeries Lafayette — parure Morellato argent 925](https://www.galerieslafayette.com/p/parure+de+bijoux+nobile-morellato/2013251846197/52)
- [Galeries Lafayette — parure Pd Paola](https://www.galerieslafayette.com/p/forever-parure+collier+et+boucles+d+oreilles+forever-pd+paola/81549146/52)
- [Histoire d'Or — idées cadeaux](https://www.histoiredor.com/fr_FR/c/idees-cadeaux/?pmax=100&pmin=0)
- [Nomination — Jewellery under 50 €](https://www.nomination.com/eu_en/gifts/jewellery-under-50)
- [Petite Mendigote — sélection cadeaux](https://petitemendigote.com/en/collections/selection-cadeaux)
- [Huguette Paris — idées cadeau](https://huguetteparis.com/en/blogs/news/idees-cadeau)
- [ajluxe — marques de bijoux françaises](https://ajluxe.com/fr/blogs/jewelry-guide/meilleures-marques-de-bijoux-francaises)
- [La Redoute — bijoux fantaisie](https://www.laredoute.fr/pplp/100/157878/640/cat-83849.aspx?pgnt=17)
- [Sephora — coffrets (SERP « coffret bijoux femme » ambiguë)](https://www.sephora.fr/p-P1000216583.html)
- Faits fournisseur : `woocommerce/source/FAITS-BRANVAS.md` et `woocommerce/source/branvas-faq/` (FAQ officielle lue le 22/11/2026)
