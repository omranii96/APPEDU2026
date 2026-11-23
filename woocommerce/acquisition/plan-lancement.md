# CHARMED PARIS — Plan de lancement paid social & shopping (90 jours)

> Période : **lundi 23 novembre 2026 → samedi 20 février 2027** (J+90), avec la préparation de la fête des mères 2027.
> Sources : `woocommerce/BRIEF.md` et **`woocommerce/source/FAITS-BRANVAS.md` (prioritaire en cas de conflit)**.
> Marchés : **France d'abord**, site bilingue FR + EN, test anglophone **Royaume-Uni** (sous conditions, voir §9).
> Convention : **[FAIT]** = vérifié dans les sources ; **[HYP]** = hypothèse de travail, à remplacer par la donnée réelle dès qu'elle existe ; **[À CONFIRMER]** = à vérifier avant d'engager de l'argent.

---

## 0. Ce qu'il faut retenir (1 minute)

1. **Le calendrier de Noël est très court.** Date limite Branvas pour une livraison avant Noël : **Europe vendredi 4 décembre 2026**, Royaume-Uni mardi 8 décembre **[FAIT]**. On a donc **≈ 8 jours de vente « Noël garanti »** si le site est en ligne le vendredi 27 novembre. Noël 2026 sert de **sprint de test en conditions réelles**, pas de pari de rentabilité.
2. **L'économie unitaire est serrée.** Panier moyen visé ≈ 72 € → marge ≈ 24 € (≈ 35 € en franchise de TVA), ROAS d'équilibre ≈ 3 (≈ 2). Molten Art seule à 49 € laisse **≈ 12,50 €** avant pub [calcul §2]. Aucune campagne froide ne doit pousser une parure seule sous 59 €. Les leviers : panier ≥ 69 €, « 2e parure −15 % », hero products à 59–79 €.
3. **On n'invente rien** : pas de faux prix barrés (Black Friday compris), pas de stock limité, pas de compte à rebours fictif, pas d'avis. Les **seules urgences réelles** sont les dates Branvas (4/12 Europe, 8/12 UK) et la fin de l'emballage de fête (24/12) — on les affiche telles quelles, avec leur source logique (« date limite de notre atelier d'expédition »).
4. **Arguments vrais et différenciants** à marteler : parure assortie (collier + boucles pensés ensemble), **écrin + pochette velours + chamoisine inclus** dans chaque commande, **droits et taxes déjà payés (rien à payer à la livraison)**, emballage de fête offert jusqu'au 24/12, perles de culture d'eau douce véritables (Liquid Art, selon fiche), argent 925 poinçonné + moissanite (ligne Joaillerie).
5. **Ordre des canaux** : Google Merchant Center gratuit (J0) → Meta Advantage+ (J4) → TikTok (dès qu'on a de la vidéo exploitable, Spark Ads avec créatrices en janvier) → Pinterest (janvier, pour Saint-Valentin et fête des mères).

---

## 1. Prérequis bloquants (avant le 1er euro de pub)

| # | Action | Échéance | Pourquoi |
|---|---|---|---|
| 1 | Abonnement Branvas actif (essai compris) + logo approuvé (< 24 h) | 23/11 | Les droits d'usage des photos/vidéos/mannequins Branvas en pub n'existent **que pendant l'abonnement** [FAIT]. Sans logo approuvé, les échantillons partent sans marque. |
| 2 | **Commande d'échantillons** (code NEW30 : −30 $ dès 100 $) : Molten Art, Solar Sphere, Golden Luxe, Liquid Art Pearl, Emerald Square (+ 1 Blush Dreams si budget) | 23/11 | Réception estimée 4–9 jours ouvrés (≈ 27/11–4/12). Indispensable pour filmer le **vrai** unboxing, vérifier l'écrin réel (boîte à tiroir avec ruban selon Branvas), l'échelle des pièces, la carte de Noël. |
| 3 | Commander le **pack vidéo pro Branvas (279 $)** : 1 vidéo packing 45 s avec ton logo + 2 vidéos produit 20–30 s | 23/11 | Seule façon d'avoir de la vidéo marquée exploitable **avant le 4/12**. [À CONFIRMER : délai de livraison du pack] |
| 4 | Recherche d'antériorité **INPI/EUIPO** « CHARMED PARIS » (et UKIPO si test UK) + vérifier l'activité de @charmed_paris | 23–24/11 | Ne pas investir en notoriété payante sur un nom attaquable. |
| 5 | Site en ligne : CGV (rétractation 14 j **à ta charge**, adresse de retour en France), mentions légales, RGPD, bandeau cookies certifié (Consent Mode v2), prix TTC, délais **France 4–9 jours ouvrés, sans express**, mention DDP, opérateur GPSR | 26/11 | Obligations légales + conditions d'approbation Meta/Google. |
| 6 | Tracking : plugin officiel Meta for WooCommerce (Pixel + API Conversions, déduplication), TikTok for WooCommerce, Pinterest for WooCommerce, Google for WooCommerce (flux Merchant Center + GA4) | 26/11 | Sans événements Purchase fiables, l'algorithme Advantage+ n'apprend rien. |
| 7 | Vérification du domaine (Meta Business, TikTok, Pinterest, Merchant Center), vérification d'entreprise Meta | 26/11 | Évite les blocages de diffusion au démarrage. |
| 8 | Commande test réelle de bout en bout (paiement → Branvas « En cours » → suivi écrit dans la commande) | 26/11 | Vérifie que seules les commandes payées partent et que le suivi remonte. |
| 9 | Bandeau site + fiches + checkout : « Commande avant le **vendredi 4 décembre** pour une livraison avant Noël (France/Europe). Au-delà, nous ne pouvons pas la garantir. » | 26/11 | Demandé par Branvas, et c'est la seule « urgence » légitime. |
| 10 | Carte cadeau électronique (ex. extension gratuite PW WooCommerce Gift Cards) | 3/12 | Seule offre honnête pour les achats de Noël **après** le 4/12. |

---

## 2. Économie unitaire et CPA cible

### 2.1 Hypothèses de calcul

- **[FAIT]** Coût Molten Art (JSGRQR) : 16,87 $ ; PVC Branvas 46 $. Solar Sphere (JS1AQ5) : 22,01 $ (probablement coût unitaire, à confirmer).
- **[FAIT]** Livraison Branvas : **8,99 $ par commande**, quel que soit le nombre de pièces, **packaging marqué inclus** (coffret d'envoi, écrin à ruban, pochette velours, chamoisine, carte). Frais de paiement Branvas : **2,9 % + 0,30 $** par transaction.
- **[FAIT]** Une commande = **un seul écrin** : les pièces supplémentaires arrivent dans un sachet scellé dans le même colis. → À dire clairement sur le site pour l'offre « 2e parure −15 % » (sinon déception à l'unboxing).
- **[HYP]** Change 1 $ = 0,93 € (+ 1 % de frais de change bancaire) ; 1 $ = 0,79 £.
- **[HYP]** Frais Stripe côté cliente : 1,5 % + 0,25 € (cartes UE) ; 2,5 % + 0,20 £ (cartes UK).
- **[HYP]** Provision rétractation/SAV : **5 % du CA HT** (la rétractation 14 jours est à ta charge, Branvas ne la couvre pas [FAIT]).
- **[FAIT]** TVA 20 % collectée par toi (France) si l'entreprise y est assujettie. Les tableaux supposent l'assujettissement. **[HYP] En franchise en base de TVA**, le prix TTC devient le CA encaissé : la marge au panier moyen passe d'≈ 24 € à **≈ 35 €** et le ROAS d'équilibre de ≈ 3 à **≈ 2** (statut et seuils 2027 à confirmer avec l'expert-comptable).
- **[HYP]** Livraison offerte sur les commandes issues de la pub (cas prudent).
- Prix de vente = ceux de la maquette, **à valider**.

### 2.2 Marge de contribution par commande (avant publicité)

Marge de contribution = CA HT − (coût produit + livraison Branvas + frais Branvas/change) − frais Stripe − provision retours.

| Panier (TTC) | CA HT | Coût produit | Livraison | Frais Branvas + change | Stripe | Provision retours | **Marge = CPA d'équilibre** | ROAS d'équilibre (CA TTC / pub) |
|---|---|---|---|---|---|---|---|---|
| Molten Art au PVC 46 $ ≈ 42,78 € | 35,65 € | 15,69 € | 8,36 € | 1,23 € | 0,89 € | 1,78 € | **7,70 €** | 5,6 |
| **Molten Art 49 €** | 40,83 € | 15,69 € | 8,36 € | 1,23 € | 0,98 € | 2,04 € | **12,53 €** | 3,9 |
| Molten Art 49 € + livraison payée 4,90 € | 44,92 € | 15,69 € | 8,36 € | 1,23 € | 1,06 € | 2,25 € | **16,34 €** | 3,3 |
| Molten Art 55 € | 45,83 € | 15,69 € | 8,36 € | 1,23 € | 1,07 € | 2,29 € | **17,19 €** | 3,2 |
| Molten Art 59 € | 49,17 € | 15,69 € | 8,36 € | 1,23 € | 1,14 € | 2,46 € | **20,30 €** | 2,9 |
| 2 × Molten Art (49 + 41,65 avec −15 %) | 75,54 € | 31,38 € | 8,36 € | 1,84 € | 1,61 € | 3,78 € | **28,57 €** | 3,2 |
| Solar Sphere 69 € (coût 22,01 $) | 57,50 € | 20,47 € | 8,36 € | 1,41 € | 1,28 € | 2,88 € | **23,10 €** | 3,0 |
| Solar Sphere + Molten Art (69 + 41,65) | 92,21 € | 36,16 € | 8,36 € | 2,03 € | 1,91 € | 4,61 € | **39,14 €** | 2,8 |
| [HYP] Sculpture 59 € (coût 18 $) | 49,17 € | 16,74 € | 8,36 € | 1,27 € | 1,14 € | 2,46 € | **19,20 €** | 3,1 |
| [HYP] Éclat / Couleur précieuse 79 € (coût 29 $) | 65,83 € | 26,97 € | 8,36 € | 1,67 € | 1,44 € | 3,29 € | **24,11 €** | 3,3 |
| [HYP] Joaillerie 925 189 € (coût 80 $) | 157,50 € | 74,40 € | 8,36 € | 3,53 € | 3,08 € | 7,88 € | **60,25 €** | 3,1 |

Hypothèse de coût des autres parures : ratio coût/PVC de Molten Art (≈ 37 %) appliqué aux PVC médians Branvas. **À remplacer par les coûts réels relevés dans le compte Branvas avant le 30/11.**

### 2.3 CPA cibles retenus

| Indicateur | Valeur | Règle |
|---|---|---|
| Panier moyen visé (mix) | **[HYP] ≈ 72 € TTC** (≈ 1,1 parure/commande) | Hero products à 59–79 € + offre 2e parure |
| Marge de contribution au panier visé | **≈ 24 €** si assujettie à la TVA ; **≈ 35 €** en franchise en base de TVA | Recalculer chaque semaine avec le vrai panier moyen |
| **CPA d'équilibre (BE-CPA)** | **24 €** (TVA) / 35 € (franchise) | = marge de contribution de la 1re commande |
| **ROAS d'équilibre** | **≈ 3** (TVA) / **≈ 2** (franchise) | 72 € ÷ 24 € ; 72 € ÷ 35 € |
| **CPA cible phase test (J0–J30)** | **≤ 24 €** (ROAS ≥ 3) | On accepte l'équilibre pour acheter de la donnée |
| **CPA cible phase scale (J30+)** | **≤ 18 €** (ROAS ≥ 4) | 75 % du BE-CPA → ≈ 6 € de profit par commande |
| CPA plafond (coupe) | **36 €** (1,5 × BE) | Au-delà sur 3 jours glissants : réduire ou couper |
| Molten Art vendue seule à 49 € | BE-CPA **12,50 €** | **Jamais en hero de campagne froide.** Produit d'entrée dans le catalogue et en ajout panier. |
| Joaillerie 925 | BE-CPA ≈ 60 € | Campagne séparée seulement après J+30 (panier élevé, cycle de décision plus long) |

### 2.4 Ce que le CPA cible impose en amont (contrôle de cohérence)

CPA = CPC ÷ taux de conversion (session → achat). Pour un CPA de 24 € :

| Taux de conversion site | CPC lien maximum | Commentaire |
|---|---|---|
| 1,0 % | 0,24 € | Irréaliste en Meta FR bijoux au T4 |
| 1,5 % | 0,36 € | Difficile |
| 2,0 % | 0,48 € | Atteignable avec bonnes créas + période cadeau |
| 3,0 % | 0,72 € | Typique d'un trafic chaud / retargeting / Google Shopping |

**Ordres de grandeur [HYP], à recaler après 7 jours** : CPM France ≈ **7–11 $** (≈ 6,5–10 €), plus haut fin novembre/mi-décembre ; CTR lien 0,8–1,5 % ; CPC lien ≈ 0,45–1,00 € ; **taux de conversion bijoux ≈ 0,7–1,5 %** pour une boutique neuve sans avis. Avec ces valeurs, le CPA « naturel » se situe entre **30 et 140 €** : le CPA d'équilibre de 24 € n'est atteignable qu'en haut de fourchette (conversion ≥ 2 % grâce à l'intention cadeau, au retargeting et à Google Shopping, CPC ≤ 0,50 €). Conclusion honnête : **la rentabilité à la 1re commande n'est pas acquise** ; elle dépend du panier moyen, du taux de conversion et des créas. Si, après 1 000 € dépensés, le CPA moyen dépasse 36 € avec un panier < 70 €, on arrête de monter les budgets et on retravaille offre, prix et créas (§6.4).

---

## 3. Calendrier 90 jours

### Vue d'ensemble

| Phase | Dates | Objectif | Budget pub/jour (palier) |
|---|---|---|---|
| **0. Préparation express + pré-lancement** | lun 23/11 → jeu 26/11 | Prérequis §1, échantillons, seeding, comptes, liste d'attente | 0–10 € (pub « bientôt » optionnelle) |
| **1. Lancement + sprint Noël garanti** | ven 27/11 → ven 4/12 (FR/UE) | Premières ventes, apprentissage pixel, test des angles « cadeau » | 40–60 € |
| **2. Noël sans garantie de délai** | sam 5/12 → jeu 24/12 | Emballage de fête offert (vrai jusqu'au 24/12), carte cadeau, « pour soi » | 20–35 € puis 10 € |
| **3. Pause + bilan** | ven 25/12 → dim 3/01 | Ne pas acheter des CPM chers sans délai à vendre ; analyse | 0–10 € (retargeting) |
| **4. Janvier « pour soi » + contenus UGC** | lun 4/01 → dim 10/01 | Tester les premières vidéos de créatrices, angle achat pour soi | 30–40 € |
| **5. Saint-Valentin** | lun 11/01 → dim 14/02 | Pic FR (date conseillée de commande **ven 29/01**), test UK (date conseillée **mer 3/02**) | 50–120 € FR + 25–40 € UK |
| **6. Bilan J+90 + Mothering Sunday UK** | lun 15/02 → sam 20/02 | Bilan, coupe des canaux non rentables, lancement Mothering Sunday UK (7/03) | 30–60 € |
| **Horizon : fête des mères FR** | production mars–avril, pub 26/04 → 14/05 | Fête des mères **dim 30 mai 2027** (date conseillée de commande **ven 14/05** [HYP calculée]) | selon bilan J+90 |

### Détail des phases

#### Phase 0 — Préparation express et pré-lancement (23 → 26 novembre)

- **Instagram / TikTok** (voir `organique.md`, semaine 1) : 1 publication par jour, sujet unique « l'écrin s'ouvre bientôt ». Contenu = photos/vidéos Branvas retouchées (autorisé en pré-lancement avec abonnement actif [FAIT]) + maquette « l'écrin qui s'ouvre ».
- **Liste d'attente** (Brevo, hébergé UE) : formulaire « Sois prévenue de l'ouverture », consentement RGPD explicite. Contrepartie **réelle et permanente** si on en propose une (ex. livraison offerte sur la 1re commande) ; jamais « réservé aux 100 premières ».
- **Seeding** : 8 à 12 créatrices identifiées (voir `organique.md` §5), commandes passées directement à leur adresse dans Branvas (elles reçoivent le vrai colis marqué, emballage de Noël inclus). Réception 4–9 jours ouvrés → contenus attendus **à partir du 5–10 décembre** : ils serviront surtout pour la phase 2 et janvier, pas pour le sprint du 27/11–4/12.
- **Pub « bientôt » optionnelle** : 5–10 €/jour, objectif « prospects » vers la liste d'attente, Meta uniquement. À ne lancer que si le formulaire et le pixel sont prêts.
- **Google Merchant Center** : soumettre le flux dès que les fiches sont en ligne (vérification souvent de quelques jours [HYP]). Fiches gratuites = canal sans coût le plus rapide.
- **Black Friday (ven 27/11)** : **pas de remise barrée**. Une boutique neuve n'a pas de « prix antérieur » (le prix de référence d'une réduction doit être le plus bas pratiqué dans les 30 jours précédents — art. L112-1-1 du Code de la consommation). Angle possible en organique : « Ici, le prix affiché est le prix. »

#### Phase 1 — Lancement et sprint Noël garanti (27 novembre → 4 décembre)

- **Message central** : « Commande avant le vendredi 4 décembre pour qu'elle arrive avant Noël. Écrin, pochette velours et emballage de fête inclus. Droits et taxes déjà payés. »
- **Meta** : 1 campagne Advantage+ ventes (§4.1) à 30 €/j + 1 campagne de test créatif à 15–20 €/j. Créas : vidéo packing Branvas (si livrée), statiques et carrousels à partir des visuels Branvas + `pack-noel-f.webp`, détourés `cut/` sur fonds de marque (`prompts-visuels.md`).
- **Google** : fiches gratuites + campagne Shopping standard 10 €/j dès l'approbation du flux (§4.4).
- **TikTok** : lancement à 20 €/j **uniquement si** on dispose d'au moins 3 vidéos 9:16 natives (pack vidéo Branvas, vidéo de l'échantillon filmée par toi). Sinon, report à la phase 4.
- **Pinterest** : organique seulement (épingles produits via catalogue), pas de pub avant janvier.
- **UK** : pas de pub UK pour Noël (enregistrement TVA UK non réalisable à temps, voir §9) — sauf si déjà fait.

#### Phase 2 — Noël sans garantie de délai (5 → 24 décembre)

- **Dès le samedi 5/12** : retirer de toutes les pubs toute mention « avant Noël ». Bandeau : « Livraison en 4 à 9 jours ouvrés : nous ne pouvons plus garantir une arrivée avant Noël. »
- Angles autorisés : **carte cadeau électronique** (livrée par e-mail, immédiate) ; **emballage de fête offert jusqu'au 24/12** (fait Branvas) ; **« pour toi »** (se faire plaisir pour les fêtes) ; Nouvel An.
- Budget : réduire à 20–35 €/j sur les seules annonces gagnantes de la phase 1, puis **10 €/j du 14 au 24/12** (carte cadeau + retargeting).
- Intégrer les premières vidéos de créatrices reçues (droits signés, §5 de `organique.md`) en test.

#### Phase 3 — Pause et bilan (25 décembre → 3 janvier)

- Campagnes froides en pause. Retargeting 5–10 €/j (visiteurs 30 j, paniers abandonnés) avec angle « pour toi / argent de Noël ».
- Bilan : CPA réel par angle, panier moyen réel, taux de rétractation, délais réels mesurés (date commande → livraison DHL), retours qualitatifs des clientes (sans les utiliser comme témoignages sans accord).
- **Collecte d'avis** : e-mail post-livraison J+10 via l'outil d'avis (Judge.me ou équivalent). Les vrais avis pourront ensuite apparaître dans les pubs (texte exact, prénom + initiale, avec accord).

#### Phase 4 — Janvier « pour soi » (4 → 10 janvier)

- Nouveau test créatif : 6–10 vidéos UGC (créatrices seedées), angle « pour soi », « avant/après tenue », « parure vs dépareillé ».
- Soldes d'hiver (à partir du **mercredi 13 janvier 2027** [À CONFIRMER par arrêté]) : **ne pas y participer** au lancement (pas d'historique de prix, marge trop serrée). On mise sur Saint-Valentin.

#### Phase 5 — Saint-Valentin (11 janvier → 14 février)

- **Date conseillée de commande France : vendredi 29 janvier 2027.** Calcul : délai max 9 jours ouvrés → lundi 1er février pour une livraison le vendredi 12 février ; marge de 1 jour ouvré prise en plus. **[À CONFIRMER]** auprès de Branvas : date officielle Saint-Valentin et impact du **Nouvel An chinois (samedi 6 février 2027)** sur les entrepôts en Chine. Si Branvas publie une autre date, c'est elle qui fait foi.
- Montée en charge : 11–17/01 palier 2 (50 €/j), 18–29/01 palier 3 (80–120 €/j) si règles de scale respectées ; 30/01–13/02 carte cadeau + « livraison sans garantie avant le 14 » à 15–20 €/j.
- Pinterest : campagne catalogue + considération dès le 11/01 (les recherches Saint-Valentin démarrent tôt sur Pinterest [HYP]).
- UK : test (§9), date conseillée de commande **mercredi 3 février 2027** (délai UK 3–7 jours ouvrés [FAIT] → vendredi 12 février).
- Angles : cadeau pour elle (acheteurs hommes et femmes), « pour lui » avec la ligne Mixte sur cordon et le packaging homme, Galentine's (cadeau entre amies) le 13/02.

#### Phase 6 — Bilan J+90 et Mothering Sunday UK (15 → 20 février)

- Bilan complet (§7.3), décision canal par canal : garder / réduire / couper.
- **UK Mothering Sunday : dimanche 7 mars 2027** (3 semaines avant Pâques, 28 mars 2027). Date conseillée de commande **mercredi 24 février**. Si le test Saint-Valentin UK a tenu ses seuils, lancer 25–50 €/j du 15 au 24/02.

#### Horizon — Fête des mères France (dimanche 30 mai 2027)

- Calcul : dimanche 30 mai (Pentecôte le 16 mai, donc pas de report) [FAIT calendaire, À CONFIRMER officiellement]. Date conseillée de commande **vendredi 14 mai** [HYP : 9 jours ouvrés, lundi de Pentecôte 17 mai exclu].
- Mars : recruter 6–10 créatrices « maman/fille » (vraies relations, vrais produits). Avril : production. Pinterest dès le 1er avril. Pub Meta/TikTok du 26 avril au 14 mai, puis carte cadeau jusqu'au 29 mai.

---

## 4. Structure de campagnes

Nomenclature : `PLATEFORME_PAYS_OBJECTIF_TYPE_ANGLE_DATE` (ex. `META_FR_VENTES_ADV+_CADEAU_2611`). Annonces : `CONCEPT##_FORMAT_HOOK#_LANGUE` (ex. `C01_916_H2_FR`). UTM : `utm_source={plateforme}&utm_medium=paid_social&utm_campaign={nom}&utm_content={annonce}`.

### 4.1 Meta (Facebook + Instagram)

| Campagne | Type | Budget | Ciblage | Contenu | Rôle |
|---|---|---|---|---|---|
| **C1 — Prospection** | Campagne **Advantage+ ventes** (objectif Achat, Pixel + API Conversions) | 30 €/j au départ | France, 18+ ; audience Advantage+ sans restriction (suggestion : femmes 25–45 ans) ; placements Advantage+ | 6–10 annonces : 3 vidéos 9:16, 2 vidéos 4:5, 2 statiques 4:5, 1 carrousel, 1 catalogue (Advantage+ catalogue dès que le catalogue est synchronisé) | Volume, apprentissage |
| **C2 — Test créatif** | Campagne ventes manuelle, budget au niveau de l'ensemble (ABO) | 15–20 €/j (1 ensemble par concept, 3 variantes de hook) | Large, France, 18+ | 1 concept = 1 ensemble = 3 annonces (même corps, 3 hooks différents) | Trouver les gagnants à promouvoir dans C1 (même ID de publication pour garder les interactions réelles) |
| **C3 — Retargeting** (à partir de ≈ 2 000 visiteurs/mois) | Ventes, catalogue dynamique | 5–10 €/j | Visiteurs 14 j, ajouts panier 7 j non acheteurs | Catalogue + rappel des arguments vrais (écrin inclus, droits payés, délais) | Récupérer les paniers |
| **C4 — Joaillerie 925** (après J+30) | Advantage+ ventes | 15–20 €/j | France | Moissanite, argent 925 poinçonné, certificat GRA si ≥ 0,1 ct, **écrin velours bleu (non marqué)** [FAIT] | Panier élevé |
| **C5 — UK** (phase 5) | Advantage+ ventes | 25–40 €/j | Royaume-Uni | Versions EN des concepts | Test marché (§9) |

Règles Meta :
- Exclure les acheteuses des 30 derniers jours de la prospection (paramètre « clientes existantes » de la campagne Advantage+).
- Ne pas cumuler plus de 2 campagnes de prospection actives au palier 1 : le budget doit rester concentré.
- Activer l'étiquette « Informations sur l'IA » de Meta pour tout visuel généré par IA représentant une personne (voir `prompts-visuels.md` §1).
- Partenariats créatrices : publier via « Partenariat rémunéré » (annonces partenaires) avec l'autorisation de la créatrice.

### 4.2 TikTok

| Campagne | Type | Budget | Contenu |
|---|---|---|---|
| **T1 — Prospection** | Ventes (Web), optimisation Achat ; campagne automatisée Smart+ si disponible sur le compte | 20 €/j [À CONFIRMER : minimum par groupe d'annonces affiché dans le compte] | 5–8 vidéos 9:16 natives, son tendance libre de droits commerciaux (bibliothèque commerciale TikTok uniquement) |
| **T2 — Spark Ads créatrices** (janvier) | Ventes, publications des créatrices boostées (code d'autorisation) | 20–40 €/j | Vidéos UGC des scripts `concepts-creatifs.md` §3, avec la mention « Contenu de marque » activée |

- TikTok se fatigue vite : rafraîchir 2–3 créas par semaine.
- Étiquette « contenu généré par IA » obligatoire sur TikTok pour tout contenu réaliste généré par IA.
- **TikTok Shop** : pas au lancement. À étudier après J+90 (délais, obligations vendeur).

### 4.3 Pinterest

| Campagne | Type | Budget | Contenu |
|---|---|---|---|
| **P0 — Organique** | Catalogue (Pinterest for WooCommerce), épingles produit enrichies | 0 € | Dès J0 |
| **P1 — Catalogue / Shopping** | Ventes catalogue | 10–15 €/j à partir du 11/01 | Toutes les parures, titres « Parure collier et boucles… » |
| **P2 — Considération** | Trafic / clic sortant | 5–10 €/j à partir du 11/01 | Épingles « idées cadeau Saint-Valentin », « parure mariage invitée », « tenue soirée » (4:5 et 2:3) |

### 4.4 Google Shopping (Merchant Center d'abord)

1. **J0 — Fiches gratuites** : flux via Google for WooCommerce. Attributs : `brand` = CHARMED PARIS, `mpn` = SKU Branvas (ex. JSGRQR), `identifier_exists` = no (pas de GTIN [FAIT]), `material` exact (« laiton doré », « argent 925 »…), `gender` = female (ou unisex pour la ligne Mixte), `age_group` = adult, prix TTC, délais d'expédition et de livraison réels (France 4–9 jours ouvrés), politique de retour 14 jours.
2. **Titres** : `Parure collier et boucles d'oreilles {style} dorée — {Nom} | CHARMED PARIS` (ne jamais écrire « plaqué or », « or » seul, « waterproof », « hypoallergénique », « sans nickel »).
3. **J+5 environ, après approbation** : campagne **Shopping standard** 10 €/j, enchères au CPC manuel (plafond 0,40 € [HYP]) ou « Maximiser les clics » plafonné, mots-clés négatifs (« pas cher », « argent massif », « or 18 carats », « occasion », « vinted »).
4. **Après 30 conversions** : tester **Performance Max** (flux seul, sans créas trompeuses) à 15–20 €/j contre le Shopping standard.
5. **Google Ads Search** : pas au lancement (concurrence des grands acteurs sur « parure bijoux »). Exception : une campagne marque « charmed paris » à 3 €/j dès que des recherches de marque apparaissent.

---

## 5. Budgets de test par paliers

| Palier | Dates indicatives | Meta | TikTok | Google | Pinterest | UK | **Total/jour** | Condition d'entrée |
|---|---|---|---|---|---|---|---|---|
| **P0 — Pré-lancement** | 23–26/11 | 0–10 € | 0 | 0 (fiches gratuites) | 0 | 0 | **0–10 €** | Liste d'attente + pixel OK |
| **P1 — Test** | 27/11–4/12 | 45–50 € | 0–20 € | 10 € | 0 | 0 | **55–80 €** | Prérequis §1 tous verts |
| **P1b — Après date limite** | 5–13/12 | 20–30 € | 0–10 € | 10 € | 0 | 0 | **30–50 €** | — |
| **P1c — Carte cadeau** | 14–24/12 | 10 € | 0 | 5 € | 0 | 0 | **15 €** | — |
| **P0 — Pause** | 25/12–3/01 | 5–10 € | 0 | 5 € | 0 | 0 | **10–15 €** | — |
| **P2 — Relance** | 4–17/01 | 40–50 € | 20–30 € | 10 € | 15 € | 25 € (dès le 11/01) | **85–130 €** | CPA phase 1 ≤ 36 € ou nouvelles créas UGC prêtes |
| **P3 — Scale Saint-Valentin** | 18–29/01 | 60–120 € | 30–60 € | 15–20 € | 20 € | 25–40 € (jusqu'au 3/02) | **150–260 €** | CPA 7 j ≤ 24 € et panier ≥ 70 € |
| **P1d — Après date limite** | 30/01–13/02 | 15–20 € | 10 € | 10 € | 10 € | 10 € (après le 3/02) | **55–60 €** | — |
| **P2 UK — Mothering Sunday** | 15–24/02 | — | — | — | — | 25–50 € | **25–50 €** | Seuils UK §9 tenus |

**Enveloppe 90 jours estimée [HYP]** : scénario prudent (on reste en P1/P2) **≈ 3 000 €** ; scénario central **≈ 5 500 €** ; scénario scale Saint-Valentin **≈ 9 000 €**. Hors pub : échantillons ≈ 200–250 $, pack vidéo Branvas 279 $, seeding créatrices ≈ 30–40 € par créatrice (coût produit + livraison), rémunération UGC éventuelle 80–200 € par vidéo [HYP marché FR].

**Garde-fou de perte maximale** : si 1 500 € sont dépensés sans atteindre un CPA moyen ≤ 36 €, on **arrête toute montée de palier** et on revient à P1 le temps de retravailler l'offre (§6.4).

---

## 6. Règles de coupe et de scale

### 6.1 Coupe au niveau de l'annonce (Meta et TikTok)

| Signal | Seuil de jugement | Action |
|---|---|---|
| Taux d'accroche vidéo (vues 3 s ÷ impressions) | < 25 % après 1 000 impressions | Couper ou remplacer le hook (garder le corps) |
| Taux de rétention (ThruPlay ou vues 6 s ÷ vues 3 s) | < 30 % | Raccourcir, couper le milieu |
| CTR lien | < 0,8 % après 2 000 impressions | Couper |
| CPC lien | > 1,20 € après 30 € dépensés | Couper (sauf si taux d'ajout panier > 10 %) |
| Ajouts panier | 0 après une dépense de 1 × CPA cible (24 €) | Couper |
| Achats | 0 après 2 × CPA cible (48 €) avec moins de 3 ajouts panier | Couper |
| Achats | 0 après 2 × CPA cible avec ≥ 3 ajouts panier | Ne pas couper : vérifier la fiche produit, les frais au checkout, le délai affiché |
| Commentaires négatifs ou questions récurrentes | dès apparition | Répondre honnêtement ; si un commentaire signale une promesse ambiguë, corriger la créa |

### 6.2 Coupe au niveau de la campagne

- CPA sur 3 jours glissants > 36 € (1,5 × BE) : **−30 % de budget**.
- CPA sur 3 jours glissants > 48 € (2 × BE) : **pause** et retour en test créatif.
- Fréquence prospection > 3,0 sur 7 jours : **rafraîchir les créas** (sans augmenter le budget).
- Ne jamais juger avant 3 jours complets ou 2 × CPA cible dépensés.

### 6.3 Scale

- **Vertical** : CPA 3 jours ≤ 24 € **et** ≥ 3 achats → **+20 % de budget toutes les 48 h** (jamais plus de +30 % d'un coup sur Meta, pour ne pas relancer l'apprentissage).
- **Passage scale** : CPA 7 jours ≤ 18 € → palier supérieur.
- **Horizontal** : une annonce gagnante de C2 passe dans C1 (même publication). Décliner le gagnant en 3 nouveaux hooks + 2 formats (9:16, 4:5) + version EN pour le UK.
- **Google Shopping** : produit avec ≥ 30 clics et 0 vente → baisser l'enchère de 30 % ; produit avec ROAS ≥ 4 → +20 %.
- **Pinterest** : CPC sortant ≤ 0,40 € [HYP] et ≥ 1 vente / 50 € → +20 %.

### 6.4 Si rien ne fonctionne (après 1 500 € de pub)

Dans cet ordre : (1) fiche produit et checkout (frais visibles tôt, délais clairs, photos portées) ; (2) offre (seuil de livraison offerte, 2e parure −15 %, prix des hero products) ; (3) nouvelles créas UGC réelles ; (4) concentrer le budget sur Google Shopping + organique + micro-influence le temps de récolter les premiers avis réels.

---

## 7. KPI et tableau de bord

### 7.1 KPI par étape de l'entonnoir

| Étape | KPI | Vert | Orange | Rouge | Source |
|---|---|---|---|---|---|
| Attention | Taux d'accroche vidéo 3 s | ≥ 30 % | 25–30 % | < 25 % | Meta / TikTok |
| Attention | CPM Meta FR | ≤ 7 $ | 7–11 $ | > 11 $ | Meta |
| Intérêt | **CTR lien** | ≥ 1,2 % | 0,8–1,2 % | < 0,8 % | Meta / TikTok / Pinterest |
| Intérêt | **CPC lien** | ≤ 0,50 € | 0,50–0,90 € | > 0,90 € | idem |
| Considération | Taux de rebond page produit (GA4, engagement < 10 s) | ≤ 55 % | 55–70 % | > 70 % | GA4 |
| Considération | **Taux d'ajout panier** (sessions avec ajout ÷ sessions) | ≥ 8 % | 5–8 % | < 5 % | GA4 / Woo |
| Achat | Taux de checkout → achat | ≥ 45 % | 30–45 % | < 30 % | Woo |
| Achat | **Taux de conversion** (session → achat) | ≥ 2 % | 1–2 % | < 1 % (alerte < 0,7 %) | GA4 |
| Achat | **Panier moyen TTC** | ≥ 72 € | 62–72 € | < 62 € | Woo |
| Achat | Part des commandes à 2 parures et + | ≥ 15 % | 8–15 % | < 8 % | Woo |
| Rentabilité | **CPA** | ≤ 18 € | 18–24 € | > 36 € (coupe) | Plateformes + Woo |
| Rentabilité | ROAS (CA TTC ÷ pub) | ≥ 4 | 3–4 (2–3 en franchise) | < 2,5 (< 1,7 en franchise) | idem |
| Rentabilité | **MER** (CA total ÷ pub totale, toutes plateformes) | ≥ 3,5 | 3–3,5 | < 3 (< 2 en franchise) | Woo + factures |
| Après-vente | Taux de rétractation | ≤ 5 % | 5–8 % | > 8 % | Woo |
| Après-vente | Délai réel commande → livraison (France) | ≤ 9 j ouvrés | — | > 9 j ouvrés | Suivi DHL |

Les seuils sont des **hypothèses de départ** pour une marque neuve sans avis ; on les remplace par les moyennes réelles du compte après 14 jours.

### 7.2 Rituel

- **Chaque jour (10 min)** : dépense, CPA, achats, commentaires à modérer/répondre, anomalies de suivi.
- **Lundi et jeudi** : décisions de coupe/scale selon §6 (jamais d'une heure à l'autre).
- **Chaque lundi** : recalcul du panier moyen, de la marge de contribution et du CPA cible ; tableur « MER hebdo » (CA Woo, pub par plateforme, coûts Branvas réels payés).

### 7.3 Bilan J+90 (semaine du 15 février)

CPA et ROAS par canal et par angle, panier moyen, taux de rétractation, délais réels, coût d'acquisition des clientes vs marge, nombre et contenu des avis réels collectés, performance UK vs FR, décision de budget pour la fête des mères.

---

## 8. Messages : ce qu'on peut dire, ce qu'on ne dit jamais

| On dit (vrai) | On ne dit jamais |
|---|---|
| « Doré à l'or fin », « doré » (laiton doré par électrolyse à l'or véritable + vernis anti-ternissement) | « Plaqué or », « or », « or 18 carats », « vermeil » |
| « À garder au sec », « à retirer avant la douche ou la baignade » | « Waterproof », « ne craint pas l'eau », « ne noircit jamais » |
| « Zircons » / « oxydes de zirconium » | « Diamants », « cristaux Swarovski » |
| « Moissanite de laboratoire, argent 925 poinçonné », « certificat GRA pour les pierres de 0,1 ct et plus » | « Comme un diamant », « certifié » sans le document du produit |
| « Perles de culture d'eau douce » (si la fiche produit le confirme) | « Perles naturelles » ; « perles véritables » si la fiche dit « simulated » |
| « Écrin, pochette velours et chamoisine inclus » | « Coffret personnalisé », « gravure » (impossible [FAIT]) |
| « Droits et taxes déjà payés : rien à payer à la livraison » | Un pays d'expédition précis ; « expédié de France » |
| « Livraison en 4 à 9 jours ouvrés » (France) ; « 3 à 7 jours ouvrés » (UK) | « Livraison express », « livré en 48 h », « date garantie » |
| « Commande avant le 4 décembre pour une livraison avant Noël (Europe) » | Compte à rebours, « derniers exemplaires », « stock limité » |
| « Pensé à Paris », « sélection CHARMED PARIS » [À CONFIRMER : formulation à valider selon la réalité de l'activité] | « Fabriqué en France », « fait main à Paris », « créatrice parisienne » |
| — | « Sans nickel », « sans plomb », « hypoallergénique », « testé dermatologiquement » (pas de rapport par SKU [FAIT]) |
| — | Faux avis, faux témoignages, chiffres de ventes, « vu dans la presse », « best-seller » sans donnée |
| — | Le nom Branvas dans tout support client [FAIT] |

**Version EN** (même règles) : « gold-plated » est accepté par Branvas, mais pas « gold vermeil » ; **au Royaume-Uni, « silver » / « sterling silver » sur une pièce de plus de 7,78 g exige un poinçon d'un bureau de garantie britannique (Hallmarking Act 1973)** → ligne Joaillerie 925 exclue du test UK sauf vérification du poids pièce par pièce [À CONFIRMER]. Jamais « waterproof », « hypoallergenic », « nickel-free ». Taxes : « Duties and import taxes already paid — nothing to pay on delivery » (à vérifier pour le UK, voir §9).

---

## 9. Test marché anglophone

### 9.1 Recommandation : Royaume-Uni, sous 4 conditions

**Pourquoi le UK** : délai Branvas le plus court hors US (**3–7 jours ouvrés** [FAIT]), même fuseau horaire ou presque, forte culture du cadeau bijou (Christmas, Valentine's, **Mothering Sunday 7 mars 2027**), CPM généralement plus élevés que la France mais panier plus élevé [HYP], et le site est déjà bilingue.

**Conditions avant le 1er euro au UK** :
1. **TVA britannique** : pour les envois ≤ 135 £, la TVA UK (20 %) est due **au moment de la vente** par le vendeur, qui doit s'enregistrer auprès du HMRC (pas de seuil pour un vendeur non établi) [À CONFIRMER avec l'expert-comptable]. Le DDP de Branvas couvre les droits et taxes à l'import, **pas forcément** cette TVA de vente. Sans enregistrement, pas de test UK.
2. **Ligne Joaillerie 925 exclue** (Hallmarking Act, §8) sauf pièces < 7,78 g confirmées.
3. **Adresse de retour** et conditions de rétractation UK (Consumer Contracts Regulations 2013 : 14 jours) ; coût du retour UK → France à intégrer.
4. **Publicité** : CAP Code / ASA — les contenus de créatrices UK portent « Ad » ou « #ad » en tête ; prix en livres TTC ; site en anglais britannique (« jewellery », « colour », « personalised »).

**Alternative si la TVA UK n'est pas réglée à temps : Irlande** (UE, même droit de la consommation, TVA via le guichet OSS depuis la France, délai 5–11 jours ouvrés [FAIT], marché plus petit). Les États-Unis (3–8 jours ouvrés) sont à garder pour plus tard : taxe de vente par État, concurrence et CPM élevés.

### 9.2 Économie unitaire UK [HYP]

| Panier (TTC) | CA HT | Coût produit | Livraison | Frais Branvas + change | Stripe | Provision retours | **Marge = CPA d'équilibre** |
|---|---|---|---|---|---|---|---|
| Molten Art 45 £ | 37,50 £ | 13,33 £ | 7,10 £ | 1,04 £ | 1,32 £ | 1,88 £ | **12,83 £** |
| Molten Art 49 £ | 40,83 £ | 13,33 £ | 7,10 £ | 1,04 £ | 1,43 £ | 2,04 £ | **15,90 £** |
| Solar Sphere 59 £ | 49,17 £ | 17,39 £ | 7,10 £ | 1,20 £ | 1,68 £ | 2,46 £ | **19,34 £** |
| [HYP] Golden Luxe 69 £ (coût 29 $) | 57,50 £ | 22,91 £ | 7,10 £ | 1,42 £ | 1,93 £ | 2,88 £ | **21,27 £** |

Provision retours UK à revoir à la hausse si l'adresse de retour est en France.

### 9.3 Plan de test UK

| Étape | Dates | Budget | Contenu | Seuil pour continuer |
|---|---|---|---|---|
| Préparation | décembre | 0 € | Enregistrement TVA UK, fiches EN, prix en £, 3–4 créatrices UK seedées (envoi direct Branvas, 3–7 jours) | Conditions 9.1 remplies |
| Test Valentine's | lun 11/01 → mer 3/02 | 25–40 €/j (≈ 22–35 £) Meta Advantage+ UK + 15–20 €/j TikTok UK à partir du 18/01 | 6 concepts EN (`concepts-creatifs.md`), dont 2 UGC UK | Après 600 € : CPA ≤ 20 £ et CTR lien ≥ 1 % |
| Mothering Sunday | lun 15/02 → mer 24/02 | 25–50 €/j si seuil tenu | Angle « for Mum », concept 14 EN | CPA ≤ 18 £ → plan UK fête des mères/été |
| Décision | semaine du 8/03 | — | Bilan FR vs UK | Garder le UK uniquement si MER ≥ 3 |

---

## 10. Risques et parades

| Risque | Parade |
|---|---|
| Site pas en ligne le 27/11 | Le sprint Noël se réduit : concentrer 100 % du budget sur Meta C1 + Google, 3–4 jours seulement ; ne pas prolonger « avant Noël » après le 4/12. |
| Échantillons ou pack vidéo en retard | Créas à partir des photos/vidéos Branvas (droits OK pendant l'abonnement) et détourés `cut/` ; aucune vidéo « unboxing réel » publiée avant d'avoir le vrai colis. |
| Les visuels Branvas de packaging sont des **maquettes** de rendu du logo (dorure à chaud, 1 couleur) [FAIT] | Remplacer par des photos du vrai colis dès réception ; vérifier que la carte de Noël réelle correspond (texte en anglais « Merry Christmas » sur la maquette). |
| Mannequins Branvas = **générés par IA** [FAIT] | Les traiter comme des images de synthèse (mention « Image virtuelle » ou étiquette IA de la plateforme, voir `prompts-visuels.md`). |
| Abonnement Branvas arrêté | Tous les médias Branvas doivent être retirés [FAIT] → produire dès janvier un fonds de visuels propres (photos d'échantillons, UGC avec cession de droits). |
| Rupture d'un hero product (stock 0, réassort sans date [FAIT]) | Toujours 2 hero products actifs ; annonce catalogue qui exclut les produits à 0. |
| Nouvel An chinois (6/02/2027) et Saint-Valentin | Demander la date officielle à Branvas début janvier ; avancer la date conseillée si nécessaire. |
| Plainte « une seule boîte pour deux parures » | L'écrire sur la fiche, au panier et dans la FAQ ; proposer « une commande par destinataire » pour offrir à deux personnes. |
| Marque non disponible | Recherche INPI/EUIPO avant la pub (prérequis 4). |
