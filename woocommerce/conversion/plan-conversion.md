# CHARMED PARIS — Plan de conversion (FR + EN)

> Version du 22/11/2026. Sources : `BRIEF.md`, `source/FAITS-BRANVAS.md` (prioritaire), maquette `charmed-paris/charmed-site.html`.
> Convention : **[fait]** = vérifié dans les sources ; **[calcul]** = détaillé dans `offres-et-panier-moyen.md` ; **[hyp.]** = hypothèse à valider par les données ; **[à vérifier]** = à confirmer avant mise en ligne.

---

## 0. Les 7 règles qui priment sur le reste

1. **Le produit et le prix doivent être visibles en moins de 3 secondes, sur toutes les pages.** L'intro 3D est un bonus pour les visiteuses qui arrivent sans intention d'achat. Elle ne doit jamais se placer entre une cliente venue d'une pub et la parure qu'elle a vue.
2. **Les pubs n'atterrissent jamais sur l'accueil avec intro.** Elles mènent à une fiche produit, à une page univers ou à une page d'atterrissage sans intro (§2).
3. **La réassurance repose uniquement sur des faits** : délais Branvas au 90e centile, droits et taxes payés (DDP), packaging inclus, bordereau sans prix, 14 jours de rétractation, paiement sécurisé. Pas d'avis, de compteur, de stock ou de presse inventés.
4. **Pas de surprise au checkout** : frais de port, délai et date limite de Noël s'affichent dès la fiche produit (obligation légale + première cause d'abandon).
5. **Le panier moyen se joue dans le mini-panier** : mécanique « 2e parure −15 % » + livraison offerte **dès 2 parures (ou dès 89 €)**, seuil calé sur la règle Branvas (panier moyen ≈ 72 € + 20–30 %) [calcul].
6. **Checkout sur une page** : commande sans compte, paiements express en haut, 9 champs au maximum.
7. **Bilingue par l'URL (`/` = FR, `/en/` = EN)**. La devise dépend du pays de livraison, pas de la langue.

---

## 1. Parcours complet par source de trafic

### 1.1 Carte des parcours

| Source | État d'esprit | Atterrissage | Message d'accroche (fait) | CTA principal | Relance |
|---|---|---|---|---|---|
| **Meta prospection** (Reels / Stories) | Découverte, scroll rapide | **Fiche produit** de la parure de la pub (sans intro), ou page « Idées cadeaux » sans intro | « La parure complète, collier + boucles, livrée prête à offrir » | Ajouter au panier | Pixel + CAPI → reciblage vues produit 7 j |
| **Meta reciblage** | A déjà vu, hésite | Fiche produit vue ou panier restauré (lien Brevo/Klaviyo) | Délai réel, retours 14 j, droits payés, 2e parure −15 % | Finaliser ma commande | E-mail panier abandonné H+1, H+24 |
| **TikTok** (UGC unboxing réel, avec mention « partenariat » si contrepartie : loi influence 2023) | Divertissement, ouverture de coffret | `/lp/ouvre/` : page courte sans intro, vidéo verticale en tête puis 4 parures | « Ouvre. Laisse-toi charmer. » + ouverture réelle du coffret | Voir la parure | Pixel TikTok + Events API |
| **Pinterest** | Recherche d'idées, cadeau, mariage | Page univers ou « Offrir selon ton budget » | « Idées cadeaux de 49 € à 249 € » | Voir les parures | Tag Pinterest + catalogue |
| **Google Shopping** (fiches gratuites puis payantes) [à vérifier : pas d'EAN, déclarer `identifier_exists = no` et utiliser marque + MPN = SKU JS…] | Intention forte | Fiche produit | Prix, livraison, retours | Ajouter au panier | — |
| **SEO / direct / Instagram bio** | Curiosité marque | **Accueil avec intro courte** | Signature + coffrets | Choisir mon coffret | Pop-up newsletter (au scroll, pas au chargement) |
| **E-mail / SMS** (opt-in) | Cliente ou abonnée | Page ciblée (nouveautés, univers, Noël) | Contenu, entretien, nouveautés | Découvrir | — |
| **EN — Meta/TikTok US, IE, NL, Nordics** | Idem | `/en/` fiche produit ou `/en/lp/open/` | « Complete sets, gift-ready, duties paid » | Add to bag | Audiences séparées par langue |

### 1.2 Étapes et micro-conversions mesurées

```
Pub → [view_item | intro_passee] → add_to_cart → (mini-panier : 2e parure / seuil) → begin_checkout
     → add_shipping_info → add_payment_info → purchase → e-mails post-achat → avis → 2e commande
```

### 1.3 Post-achat (e-mails transactionnels + flux Brevo/Klaviyo)

| Moment | Contenu (factuel) | Objectif |
|---|---|---|
| Immédiat | Confirmation : récap, prix TTC, **délai estimé « 4 à 9 jours ouvrés en France (9 colis sur 10) »** [fait], lien de rétractation, CGV en PDF (support durable) | Rassurer, obligation légale |
| Envoi (suivi DHL écrit dans la commande par Branvas) [fait] | Numéro de suivi, rappel « rien à payer à la livraison : droits et taxes déjà réglés » [fait] | Réduire les contacts SAV |
| Livraison + 1 j | « Comment entretenir ta parure » : retirer avant douche et baignade, garder au sec, chamoisine et pochette velours dans le colis [fait] | Prévenir l'usure (garantie) |
| Livraison + 7 j | Demande d'avis (outil réel, cf. `stack-plugins.md`), sans incitation qui fausse l'avis | Constituer les avis vérifiés |
| J+10 après livraison | « Un souci avec ta commande ? » (fenêtre de réclamation Branvas : 10 jours avec photos) [fait] | Faire remonter les défauts **pendant** que Branvas les couvre |
| J+30 | Cross-sell : parure complémentaire du même univers, ou ligne homme pour offrir | 2e commande |
| J+60 / saison | Fête des mères, Saint-Valentin, anniversaire (si la date a été donnée volontairement) | Réachat |

**À ne pas faire** : un upsell « 1 clic » après paiement. Chaque commande Branvas est un colis séparé facturé 8,99 $ et les commandes ne sont jamais fusionnées [fait]. Un upsell post-achat crée donc une 2e commande et un 2e frais de port. L'upsell se fait **avant** le paiement (mini-panier).

**Process opérationnel à fixer** : une commande payée chez Branvas ne peut plus être annulée [fait]. Si l'Auto-Fulfillment est actif, une cliente qui corrige son adresse 30 minutes après risque de recevoir son colis à la mauvaise adresse. Recommandation : traitement des commandes 2 fois par jour (par ex. 11 h et 17 h), ce qui laisse une fenêtre de correction, et le dire dans la page Livraison. Ce délai s'ajoute aux 4–9 jours, qui sont comptés depuis le paiement chez Branvas [fait].

---

## 2. L'intro immersive : la garder sans qu'elle tue la conversion

### 2.1 Diagnostic de la maquette
- `.intro{height:520vh}` : il faut **5,2 hauteurs d'écran de scroll** avant d'atteindre les coffrets. Sur un iPhone (environ 844 px), cela fait environ 4 400 px de scroll sans produit ni prix. [fait, mesuré dans le CSS]
- L'intro charge Three.js : risque sur le LCP mobile et sur le budget JS.
- Le header (Femme, Homme, Cadeaux, Collections) est présent pendant l'intro : c'est bien, à conserver.

### 2.2 Règles d'implémentation

| Règle | Détail |
|---|---|
| **Lien « Passer l'intro »** visible dès la 1re image | En haut à droite, 44×44 px minimum, accessible au clavier (`Tab` puis `Entrée`), libellé FR « Passer » / EN « Skip ». Il fait défiler jusqu'à `#coffrets` et déclenche `intro_passee{method:"bouton"}`. |
| **CTA visible dans la 1re image** | Sous le logo : « Voir les parures » (bouton plein) + lien « Idées cadeaux ». La cliente qui sait ce qu'elle veut sort de l'intro en 1 tap. |
| **Longueur** | Desktop : 520vh → **≤ 250vh**. Mobile : **≤ 150vh** ou une version « tap pour ouvrir » (1 geste = l'écrin s'ouvre, puis les coffrets). |
| **Ne la jouer qu'une fois** | Drapeau `cp_intro_vue` en `localStorage` (dans un `try/catch`). Une visiteuse qui revient arrive directement sur les coffrets, intro repliée en bandeau de 60vh. |
| **Trafic pub = pas d'intro** | Si l'URL contient `utm_source`, `fbclid`, `ttclid`, `gclid` ou `epik` (Pinterest), saut automatique vers `#coffrets` + `intro_passee{method:"auto_pub"}`. Les pubs pointent de toute façon vers des fiches ou des `/lp/`. |
| **`prefers-reduced-motion`** | Image fixe (logo + écrin ouvert `box-open.webp`), pas de scroll piégé. `intro_passee{method:"reduced_motion"}`. |
| **Connexions lentes / petits appareils** | Si `navigator.connection.saveData` est vrai, ou `deviceMemory < 4`, ou réseau 2G/3G : version image fixe. |
| **Performance** | Image poster en LCP (WebP ≤ 120 Ko), Three.js chargé en `type="module"` après `load`/`requestIdleCallback`, jamais bloquant. Cible LCP mobile < 2,5 s, CLS < 0,1, INP < 200 ms. |
| **SEO** | Le H1 et un paragraphe texte existent dans le HTML de l'intro (pas seulement dans le canvas). |
| **Mesure** | `intro_progression` à 25/50/75/100 % + `intro_passee`. Seuil d'alerte : si moins de 35 % des sessions de l'accueil atteignent `#coffrets` [hyp.], on raccourcit encore (test A/B n°1). |

### 2.3 Pages d'atterrissage pub (sans intro)
- `/lp/ouvre/` (FR) et `/en/lp/open/` (EN) : vidéo verticale réelle de l'ouverture du coffret (5–8 s, muette, sous-titrée), puis 4 parures avec prix et bouton, puis le bloc réassurance, puis la FAQ courte.
- `/lp/noel/` puis `/en/lp/christmas/` : date limite + packaging de Noël + 6 parures + e-carte cadeau.
- Ces pages ne sont pas indexées (`noindex`) pour éviter le contenu dupliqué. Elles ont le même header, pour que la cliente puisse naviguer.

---

## 3. Réassurance factuelle : textes validés (FR / EN)

À réutiliser partout. Aucun superlatif, aucun chiffre inventé.

| Thème | FR | EN | Source |
|---|---|---|---|
| Délai | Livraison estimée : 4 à 9 jours ouvrés en France (9 colis sur 10). Un seul mode de livraison, suivi DHL. | Estimated delivery: 3–8 business days to the US, 3–7 to the UK (9 in 10 parcels). Tracked. | [fait] P90 Branvas |
| Droits | Droits et taxes d'importation déjà réglés : rien à payer à la livraison. | Duties and import taxes paid: nothing to pay on delivery. | [fait] DDP |
| Prix de livraison | Livraison 4,90 €, offerte dès 2 parures (ou dès 89 €). | Shipping €4.90, free from 2 sets (or €89). | [calcul] recommandation |
| Coffret | Chaque commande arrive dans une boîte à bijoux à ruban, avec pochette en velours et chamoisine. Bordereau sans prix : prêt à offrir. | Every order arrives in a ribboned jewellery box with a velvet pouch and polishing cloth. No prices on the packing slip. | [fait] |
| Plusieurs pièces | Plusieurs parures = un seul colis, une seule boîte à bijoux ; les autres pièces voyagent dans leur sachet scellé. | Several sets ship together in one parcel, with one jewellery box. | [fait], à dire honnêtement pour les cadeaux multiples |
| Retours | 14 jours pour changer d'avis, à compter de la réception. | 14 days to change your mind after delivery. | Légal UE ; frais de retour : cf. `offres-et-panier-moyen.md` §5 |
| Garantie | Garantie légale de conformité 2 ans. | 2-year legal guarantee of conformity (EU). | Légal |
| Paiement | Paiement sécurisé : carte bancaire, Apple Pay, Google Pay, PayPal. | Secure payment: card, Apple Pay, Google Pay, PayPal. | Selon `stack-plugins.md` |
| Matière (dorés) | Laiton doré à l'or fin, finition anti-ternissement. À garder au sec. | Gold-plated brass with anti-tarnish coating. Keep dry. | [fait] ; **jamais** « plaqué or », « vermeil », « waterproof », « sans nickel », « hypoallergénique » |
| Matière (925) | Argent 925, chaque pièce poinçonnée 925. Moissanite de laboratoire ; certificat GRA dès 0,1 ct. | Sterling silver 925, each piece stamped 925. Lab-grown moissanite; GRA certificate from 0.1 ct. | [fait] |
| Noël | Pour une livraison avant Noël en Europe : commande avant le vendredi 4 décembre 2026. Packaging de Noël offert jusqu'au 24 décembre. | Order by Tuesday 8 December 2026 for Christmas delivery to the US and UK (Friday 4 December for Europe and Canada). | [fait] |
| Contact | Une vraie adresse e-mail à ton nom, réponse sous 48 h ouvrées [hyp. : engagement à tenir]. | — | — |

**Interdits** (rappel) : « stock limité », « plus que 2 », compte à rebours, « X personnes regardent », « best-seller » sans données, prix barré sans prix antérieur réel (cf. `legal-checklist.md`), « fabriqué en France » ou « pensé à Paris » si ce n'est pas exact.

---

## 4. Page par page

Pour chaque page : **objectif**, **au-dessus de la ligne de flottaison** (mobile 390×844 en priorité, puis desktop 1440×900), **ordre des blocs**, **frictions à supprimer**, **réassurance**.

### 4.1 Accueil

- **Objectif** : orienter vers un univers ou une fiche en 1 clic. Capter l'e-mail des visiteuses non prêtes à acheter.
- **Au-dessus de la ligne de flottaison (mobile)** :
  - Bandeau d'annonce en 1 ligne, rotatif lent ou fixe : « Noël en Europe : commande avant le 4 décembre · Livraison offerte dès 2 parures ». Après le 4/12 : « Livraison avant Noël non garantie : offre une e-carte cadeau ».
  - Header : logo, Femme / Homme / Cadeaux (menu burger sur mobile), recherche, panier avec compteur, sélecteur **FR | EN**.
  - Intro (règles §2), avec « Passer » et le CTA « Voir les parures » visibles.
- **Ordre des blocs recommandé** (la maquette est presque bonne) :
  1. Intro courte (≤ 250vh desktop / ≤ 150vh mobile)
  2. **Bande de réassurance en 4 icônes** : 4–9 j ouvrés · droits payés · retours 14 j · prête à offrir. *À ajouter juste après l'intro : absent de la maquette.*
  3. Carrousel des coffrets : chaque coffret ouvert affiche le **nom, le prix et un bouton « Ajouter au panier »** (déjà présent) + un lien « Voir la fiche ».
  4. Univers (5 cartes : Sculpture, Éclat, Couleur précieuse, Joaillerie 925, Mixte), avec le prix « dès 49 € ».
  5. « La file des parures » (focus/file/grille) : la vue **« Toutes » (grille) doit être l'onglet par défaut sur mobile**. La file est jolie mais lente pour comparer.
  6. Bloc « La parure » : explication + « 2e parure −15 % ».
  7. Offrir selon ton budget : < 60 €, 60–90 €, 90–150 €, Joaillerie 925 ; occasions.
  8. Packagings réels (photos retouchées logo, légende honnête déjà en place).
  9. Newsletter : remplacer « −10 % » par l'offre retenue (cf. `offres-et-panier-moyen.md` §6).
  10. FAQ courte (5 questions) + footer légal.
- **Frictions à supprimer** : scroll de 520vh ; libellé « Ajouter à l'écrin » (risque d'incompréhension : bouton « Ajouter au panier », tiroir intitulé « Ton écrin », à tester, test n°3) ; pop-up au chargement ; vidéo sonore ; mention « Parures pensées à Paris » (allégation d'origine à justifier, sinon « Une maison parisienne » si le siège est à Paris, cf. `legal-checklist.md`).
- **EN** : même structure, intro identique, textes traduits par une humaine (pas de traduction automatique brute sur les pages clés). Le bandeau Noël EN dépend du pays : US/UK 8/12, Europe/Canada 4/12.

### 4.2 Page univers (catégorie : Sculpture, Éclat, Couleur précieuse, Joaillerie 925, Mixte, Homme, Cadeaux)

- **Objectif** : faire comparer et cliquer vers une fiche en moins de 10 s.
- **Au-dessus de la ligne de flottaison** : H1 court (« Éclat »), 1 phrase de promesse matière factuelle (« Laiton doré à l'or fin et zircons. À garder au sec. »), **puis déjà 2 cartes produits sur mobile (4 sur desktop)**. Pas de bannière héro haute.
- **Cartes produit** : photo carrée (1:1, fond porcelaine cohérent), 2e photo au survol ou au swipe (portée ou coffret ouvert), nom, contenu (« Collier + boucles »), prix TTC, bouton « Ajouter » rapide (ajout direct si pas de variation).
- **Filtres** (simples, 4 maximum) : univers, budget, métal (doré / argent 925), occasion. Tri : « Nos choix » / prix croissant / prix décroissant / nouveautés. Pas de tri « meilleures ventes » tant qu'il n'y a pas de données.
- **Ordre** : H1 → filtres en chips horizontaux → grille → bloc « 2e parure −15 % » au milieu de la grille (après la 6e carte) → texte SEO court en bas (cf. `seo/`) → FAQ univers.
- **Frictions** : pagination (préférer « Voir plus », 12 par 12, 30 produits au total) ; filtres en sidebar sur mobile ; photos 400×400 floues.
  > **Point bloquant qualité** : les photos `branvas-photos/` font 400×400 px [fait]. C'est insuffisant en fiche (zoom) et sur un écran Retina. Il faut récupérer les originaux haute définition dans le compte Branvas (droits d'usage et de modification inclus avec l'abonnement [fait]) : 1600 px minimum, servis en WebP/AVIF.
- **Réassurance** : ligne fine sous le H1 : « Livraison offerte dès 2 parures · Retours 14 j · Droits payés ».

### 4.3 Fiche produit (la page la plus importante : c'est elle qui reçoit les pubs)

- **Objectif** : ajout au panier. Objectif secondaire : ajout d'une 2e parure.
- **Au-dessus de la ligne de flottaison (mobile, dans l'ordre)** :
  1. Galerie swipe (6 visuels maximum) : packshot détouré, porté (photos mannequin Branvas autorisées [fait]), détail fermoir/boucle, **coffret ouvert avec la parure**, échelle (sur buste ou main), vidéo courte si disponible. Indicateur « 1/6 ».
  2. Nom : « Parure Solar Sphere ». Sous-titre factuel : « Collier + puces · laiton doré à l'or fin, zircons ».
  3. Prix TTC en grand, et dessous « Livraison 4,90 € · offerte dès 2 parures (ou dès 89 €) ».
  4. **Bouton « Ajouter au panier »** pleine largeur. Un bouton Apple Pay / Google Pay en dessous est à tester (test n°7) : il peut faire baisser le panier moyen.
  5. Ligne délai dynamique : « Commande aujourd'hui : livraison estimée entre le **jeu. 26/11** et le **mer. 2/12** » (calcul : jours ouvrés + délai de traitement, P90 Branvas [fait]). Pendant la période de Noël : « Pour Noël en Europe : commande avant le vendredi 4 décembre ».
- **Sous la ligne de flottaison (ordre)** :
  6. 3 puces réassurance : droits payés · retours 14 j · boîte à bijoux + pochette velours.
  7. « Complète ta parure : −15 % sur la 2e » : 3 suggestions du même univers ou de prix voisin, ajout en 1 tap.
  8. Accordéons : **Description** (2–3 phrases sensorielles + usage) / **Matières et dimensions** (depuis la fiche Branvas, qui fait foi : dorure et carat, pierres, longueur de chaîne, taille des boucles, poids, type d'attache) [à relever par produit] / **Entretien** (retirer avant douche et baignade, garder au sec, ranger dans la pochette) / **Livraison et retours** / **Sécurité produit** (GPSR : nom et adresse de l'opérateur responsable UE = CHARMED PARIS, référence = SKU, avertissements) [fait : le marchand est responsable UE].
  9. Avis : section masquée tant qu'il n'y a aucun avis. Ensuite, avis réels uniquement, avec la mention de la méthode de vérification (obligation d'information, `legal-checklist.md`).
  10. Cross-sell « Pour lui » (ligne homme) sur les fiches femme, en période cadeaux.
- **Sticky add-to-cart mobile** : barre basse « Solar Sphere · 69 € · Ajouter », qui apparaît quand le bouton principal sort de l'écran.
- **Frictions à supprimer** : description Branvas en anglais copiée telle quelle ; « Choisir une option » sans raison (les parures sont des produits simples) ; zoom qui ouvre une nouvelle page ; avis vides « 0 avis » ; informations de livraison cachées ; coupon visible sur la fiche.
- **Joaillerie 925 (149–249 €)** : ajouter « Paiement en 4× avec PayPal » (si éligible) [à vérifier], le certificat GRA dès 0,1 ct [fait] et la boîte en velours bleu (spécifique moissanite, sans logo [fait]). C'est la seule gamme où le paiement fractionné a un vrai sens.
- **EN** : mêmes blocs ; prix dans la devise du pays de livraison (USD pour les US si activé) ; délai par pays (US 3–8, UK 3–7, IE 5–11, NL 4–6 jours ouvrés) [fait] ; date Noël par pays.

### 4.4 Mini-panier (tiroir latéral « Ton écrin », déjà dans la maquette)

C'est **le principal levier de panier moyen**. Il s'ouvre automatiquement à l'ajout, sans redirection.

- **Au-dessus de la ligne de flottaison du tiroir** :
  1. Titre « Ton écrin (1) » + fermer.
  2. **Barre de progression** : « Ajoute une 2e parure : −15 % sur la moins chère et livraison offerte ». Elle passe à « Livraison offerte ✓ » quand le seuil est atteint. *La maquette calcule déjà ce message (seuil 50 €) : passer le seuil à 89 € et ajouter la règle « ou dès 2 parures » (toute paire de parures dépasse 89 € : minimum 49 € + 41,65 €).*
  3. Ligne produit : vignette, nom, contenu, quantité, prix, supprimer.
  4. **Bloc « La 2e à −15 % »** : 3 vignettes cliquables avec le prix remisé affiché (« 58,65 € au lieu de 69 € dans ton écrin »). Le prix de référence est le prix de vente réel : pas de faux prix barré.
  5. Récap : sous-total, remise 2e parure, livraison, **total TTC**.
  6. Bouton « Commander » plein + boutons express (Apple Pay / Google Pay / PayPal) en dessous.
  7. Microcopy : « Paiement sécurisé · Retours 14 j · Droits payés ».
- **Frictions** : tiroir qui se ferme à l'ajout d'un cross-sell (garder ouvert) ; champ code promo en évidence (le cacher derrière « J'ai un code ») ; recalcul lent (fragments AJAX de Woo à éviter ; utiliser l'API Store / les blocs Cart).
- **Règle claire de l'offre** (à écrire sous le récap) : « −15 % sur la parure la moins chère dès 2 parures dans la même commande. Non cumulable avec [code bienvenue] » (décision `offres-et-panier-moyen.md` §4).

### 4.5 Page panier

- Rôle secondaire (le tiroir fait le travail) : même contenu que le mini-panier en pleine page, + estimation du délai + date limite de Noël + FAQ livraison et retours repliée.
- **Pas de calculateur de frais de port** à saisir : le tarif est fixe (4,90 € ou offert), affiché directement.
- Lien « Continuer mes achats » qui renvoie à la dernière page univers vue, pas à l'accueil (sinon l'intro rejoue).

### 4.6 Checkout

- **Objectif** : maximiser `purchase / begin_checkout` (cible ≥ 55 % [hyp.]).
- **Structure** : 1 page (WooCommerce Checkout Block ou FunnelKit/CheckoutWC, cf. `stack-plugins.md`), header réduit (logo + « Paiement sécurisé », sans menu), pied de page réduit (CGV, confidentialité, contact).
- **Au-dessus de la ligne de flottaison (mobile)** :
  1. Boutons express : Apple Pay, Google Pay, PayPal.
  2. « ou » + E-mail (champ 1, sert aussi au panier abandonné), case **non cochée** « Recevoir les nouveautés et offres par e-mail ».
  3. Récap repliable « Afficher le récapitulatif · 110,65 € ».
- **Champs (9 maximum)** : e-mail, prénom, nom, adresse (avec autocomplétion [à vérifier : plugin ou API Google Places, consentement]), complément (replié « + Ajouter un complément »), code postal, ville, pays (FR par défaut ; en EN par géolocalisation), **téléphone obligatoire hors US/UK** (exigé par le transporteur [fait]) avec l'explication « Uniquement pour le livreur DHL ». Ville et code postal se remplissent entre eux. Supprimer : société, 2e adresse affichée par défaut, notes de commande (ou les replier), création de compte obligatoire.
- **Livraison** : un seul mode, déjà sélectionné, affiché comme une info et non un choix : « Livraison suivie DHL · 4–9 jours ouvrés · 4,90 € / Offerte ». **Pas d'option express** [fait : Branvas n'en propose pas].
- **Paiement** : carte (formulaire intégré Stripe/WooPayments), PayPal, et PayPal 4× pour les paniers éligibles [à vérifier].
- **Bloc légal juste avant le bouton** :
  - Rappel en 1 ligne : « Tu disposes de 14 jours pour te rétracter après réception. »
  - Case ou mention d'acceptation des CGV avec lien (WooCommerce : page « Conditions générales »).
  - **Bouton : « Commander avec obligation de paiement »** (EN : « Place order and pay »). Le « Commander » par défaut de WooCommerce est à remplacer (`legal-checklist.md`).
- **Noël** : ligne au-dessus du bouton, jusqu'au 4/12 : « Pour une livraison avant Noël en Europe, commande avant le vendredi 4 décembre 2026. » Après le 4/12 : « Livraison avant Noël non garantie. » Aucun compte à rebours : seule la date, qui est un fait.
- **Frictions** : redirection vers PayPal pour la carte (utiliser des champs carte intégrés) ; erreurs affichées en haut seulement (validation en ligne, champ par champ) ; captcha visible (préférer un anti-fraude invisible : Stripe Radar) ; changement de devise au checkout.
- **EN** : formats d'adresse US (State + ZIP), UK (Postcode) ; téléphone facultatif US/UK ; prix et taxes : en UE, prix TTC ; aux US, prix hors sales tax (afficher « Duties paid · no extra fees on delivery ») [à vérifier : obligations de sales tax, cf. `legal-checklist.md`].

### 4.7 Page merci (order-received)

- **Objectif** : rassurer, réduire les « où est ma commande ? », préparer la 2e commande et l'avis.
- **Ordre** : « Merci, Prénom. Ta commande n° 1234 est confirmée. » → calendrier visuel « Préparée → Expédiée (e-mail avec suivi) → Livrée entre le X et le Y » → récap de la commande → « Créer mon compte en 1 clic » (mot de passe seul, e-mail prérempli) pour suivre la commande et accéder au formulaire de rétractation → « Une erreur dans l'adresse ? Réponds à l'e-mail de confirmation avant [heure du prochain traitement] » (lié au process §1.3) → partage Instagram/TikTok (« Montre-nous ton écrin : #charmedparis », sans contrepartie qui obligerait à divulguer) → 3 suggestions (sans code de réduction immédiat, pour ne pas inciter à annuler et repasser commande).
- **Tracking** : `purchase` déclenché **une seule fois** (dédoublonnage par `transaction_id`, aussi côté serveur), cf. `tracking-et-tests.md`.
- **Pas d'upsell 1 clic** (cf. §1.3).

### 4.8 Compte client (Mon compte)

- **Objectif** : autonomie (suivi, rétractation, factures) pour moins de SAV.
- **Contenu** : commandes avec le **numéro de suivi DHL** synchronisé par Branvas [fait] ; **bouton / fonction de rétractation** en ligne, disponible pendant les 14 jours (obligation UE depuis le 19/06/2026, `legal-checklist.md`) ; factures PDF ; adresses ; préférences e-mail/SMS (désinscription en 1 clic) ; « Mes envies » (liste de souhaits légère, facultative) ; suppression du compte (RGPD).
- **Frictions** : compte obligatoire pour commander (non) ; mot de passe complexe imposé à la création (laisser la création en 1 clic après achat) ; lien de connexion par e-mail (« magic link ») possible plus tard [à vérifier].

### 4.9 Pages support (souvent oubliées, fortement liées à la conversion)

| Page | Contenu clé |
|---|---|
| Livraison | Délais P90 par pays [fait], DHL, DDP, un seul mode, pas d'express, colis unique, horaires de traitement, date de Noël, procédure colis perdu (signaler 7 jours sans mouvement après la date estimée) [fait] |
| Retours et rétractation | 14 j, procédure, adresse de retour **en France** à toi (pas celle de Branvas) [fait], qui paie le retour, remboursement sous 14 j, formulaire type, bouton de rétractation |
| Entretien | Garder au sec, retirer avant douche/baignade/sport, parfum avant le bijou, chamoisine, pochette |
| Matières | Doré à l'or fin (pas « plaqué or »), argent 925 poinçonné, moissanite de laboratoire, zircons, perles de culture d'eau douce (sauf mention « simulées » sur la fiche) [fait] |
| Guide des tailles | Longueurs de chaîne, taille des boucles, bagues (si la parure en contient) [à relever] |
| FAQ | 10 questions, regroupées en FR et EN |
| Carte cadeau | E-carte cadeau (solution pour les achats tardifs de Noël) |

---

## 5. Bilingue FR + EN : décisions CRO

| Sujet | Recommandation | Pourquoi |
|---|---|---|
| Structure | `charmedparis.com/` (FR, défaut) et `charmedparis.com/en/` (EN). `hreflang` fr-FR / en / x-default = FR. | Un seul domaine, autorité SEO partagée |
| Sélecteur | « FR \| EN » dans le header (texte, pas de drapeau) + en pied de page. **Aucune redirection automatique par IP**. À la place, un bandeau discret « Looks like you're in the US — view in English / USD? ». | Une redirection forcée gêne les francophones à l'étranger et Googlebot |
| Outil | **TranslatePress** (licence avec SEO Pack : slugs traduits, hreflang) en premier choix ; WPML + WooCommerce Multilingual en alternative (cf. `stack-plugins.md`) | TranslatePress traduit sans dupliquer les produits : le produit créé par Branvas via l'API REST reste **un seul objet** (même ID, même SKU, même stock). WPML/Polylang créent une copie EN du produit, d'où un risque pour la synchronisation des stocks et la reconnaissance des commandes EN par Branvas [à vérifier par une commande test] |
| Devise | **Lancement : EUR partout.** Phase 2 : **USD pour les États-Unis** via WooPayments Multi-Currency, avec prix fixés à la main (49 € → 59 $, 69 € → 79 $, 79 € → 89 $), sans conversion automatique à virgules. **GBP seulement après décision TVA UK** | Branvas facture en USD [fait] ; les US convertissent mieux en USD ; le Royaume-Uni impose une TVA UK au vendeur étranger dès la 1re vente ≤ 135 £ [à vérifier avec un comptable] |
| Marchés EN prioritaires | US (3–8 j), Irlande (5–11 j, EUR), Pays-Bas/Nordiques (anglais courant, EUR) ; UK en phase 2 | Délais [fait] et fiscalité |
| Checkout EN | Mêmes moyens de paiement ; PayPal Pay Later (US : Pay in 4, UK : Pay in 3) [à vérifier éligibilité] ; formats d'adresse locaux ; téléphone requis hors US/UK [fait] | — |
| Contenus EN | Traduction humaine relue pour : accueil, 30 fiches, CGV/Terms, livraison, retours, e-mails transactionnels. Le tutoiement devient un « you » chaleureux. Signature : « Open. Be charmed. » [à valider marque] | La traduction automatique brute fait chuter la confiance |
| E-mails | Langue de la commande enregistrée (`order language`) et e-mails transactionnels + flux Brevo/Klaviyo dans cette langue | — |
| Tracking | Paramètre `site_language` + `currency` sur tous les événements ; audiences et campagnes séparées FR/EN (cf. `tracking-et-tests.md`) | — |
| Légal EN | CGV/Terms, Privacy, Cookies, Legal notice traduits ; le droit français s'applique, mais une consommatrice UE garde les protections de son pays de résidence (Rome I, art. 6) | `legal-checklist.md` |

---

## 6. Plan d'action priorisé (avant / après lancement)

| Priorité | Action | Impact attendu |
|---|---|---|
| P0 | Photos HD (≥ 1600 px) depuis le compte Branvas | Conversion fiche, qualité pub |
| P0 | Fiches avec matières exactes relevées dans Branvas (dorure/carat, dimensions, pierres, perles) | Confiance + conformité |
| P0 | Bouton « Commander avec obligation de paiement », CGV, rétractation + bouton, médiateur, GPSR | Légal (bloquant) |
| P0 | Livraison offerte dès 2 parures (seuil 89 €), 4,90 € sinon dans le mini-panier | Panier moyen [calcul] |
| P0 | Délai estimé dynamique + date de Noël 4/12 (bandeau, fiche, checkout) | Conversion et moins de SAV |
| P1 | Intro raccourcie + « Passer » + saut pour le trafic pub + `/lp/` | Conversion accueil |
| P1 | Checkout 1 page, paiements express, champs réduits | Taux de finalisation |
| P1 | Tracking GA4 + Meta CAPI + Consent Mode v2 | Pilotage des pubs |
| P1 | Flux panier abandonné (H+1, H+24) + post-achat (avis J+7, réclamation J+10) | Récupération et avis |
| P2 | Version EN (TranslatePress), puis USD | Nouveaux marchés |
| P2 | E-carte cadeau (avant le 4/12) | Achats tardifs de Noël |
| P3 | Tests A/B (`tracking-et-tests.md`) | Optimisation continue |
