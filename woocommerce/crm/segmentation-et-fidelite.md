# Segmentation, fidélité, parrainage, consentement et KPI

CHARMED PARIS · outil : Brevo (voir `choix-outil.md`) · site bilingue FR + EN · flows décrits dans `flows.md`.

---

## 1. Segments de base (toujours croisés)

| Segment | Règle | Usage |
|---|---|---|
| **Langue** | `LANGUE = fr` ou `en` (détection décrite dans `flows.md` §0.1) | Choix du modèle FR ou EN dans **chaque** envoi |
| **Pays et zone de délai** | `PAYS` → `DELAI_MIN` et `DELAI_MAX` (`flows.md` §0.2) | Dates limites des temps forts, P1 et P2 |
| **Opt-in** | `OPT_IN_EMAIL`, `OPT_IN_SMS` | Seules les opt-in reçoivent du marketing |
| **Clientes ou prospects** | `NB_COMMANDES ≥ 1` ou `= 0` | Bienvenue (B1 ou B1-cliente), réactivation |
| **Engagement** | Clic ou visite du site dans les 90 derniers jours : **engagée**. Sinon **peu engagée**. Après 12 mois sans clic : **sunset**. | Les campagnes courantes visent les engagées. Les ouvertures ne comptent pas (Apple Mail Privacy Protection). |
| **Exclusions** | `SAV_OUVERT`, rétractation ou remboursement de moins de 30 jours, commande pas encore livrée (pour les promos) | Voir `flows.md` §0.7 |

---

## 2. Segments de comportement

### 2.1 Acheteuses cadeau ou pour soi : `ACHAT_CADEAU`

**Signaux, du plus fiable au moins fiable :**
1. **Déclaration** : une case « C'est pour offrir » au checkout, ou un clic « C'est pour offrir / C'est pour moi » dans P2. C'est une donnée déclarée par la cliente (*zero-party data*), donc fiable.
2. **Nom de livraison différent** du nom de facturation.
3. **Date de commande** en période cadeau : du 15 novembre au 24 décembre, du 15 janvier au 14 février, et les 3 semaines avant la fête des mères du pays.

**Règle :**
- `oui` si la cliente l'a déclaré, ou si les signaux 2 et 3 sont présents tous les deux.
- `non` si elle l'a déclaré, ou si le nom de livraison est le même que celui de facturation **hors** période cadeau.
- `inconnu` dans tous les autres cas.
- La dernière déclaration l'emporte toujours.

| | Acheteuse cadeau | Acheteuse pour soi |
|---|---|---|
| Message central | Offrir sans se tromper, arriver à temps, l'écrin | Porter souvent, entretenir, compléter son style |
| P2 | Variante cadeau | Variante pour soi |
| X1 (J+21) | « Et une pour toi cette fois ? » | « La suivante, pour d'autres tenues » |
| Temps forts | **Ciblée en premier**, dès NO1, SV1 et FM1 | Reçoit les temps forts, et peut recevoir « à te faire offrir » (SV1) |
| Pression | Pics saisonniers, plus calme le reste de l'année | Régulière, 1 à 2 e-mails par mois |

### 2.2 Univers préféré : `UNIVERS_PREFERE`

- **Score sur 180 jours glissants** : commande = 3 points, ajout au panier = 2, consultation de fiche = 1 (si le traceur est actif). L'univers qui a le score le plus haut gagne. En cas d'égalité, le plus récent.
- **Sans historique** : on prend le choix fait à l'étape 2 du pop-up (« Ton style ? ») ou dans le centre de préférences.
- **Univers voisins** (pour le cross-sell X1 : 1 parure du même univers + 2 d'un univers voisin) :

| Univers préféré | Voisins proposés |
|---|---|
| Sculpture | Mixte, Éclat |
| Éclat | Couleur précieuse, Sculpture |
| Couleur précieuse | Éclat, Joaillerie 925 |
| Joaillerie 925 | Couleur précieuse, Éclat |
| Mixte | Sculpture |

### 2.3 Panier supérieur à 100 € : segment « Grandes occasions »

- **Règle** : au moins une commande de 100 € TTC ou plus, ou `CA_TOTAL ≥ 150 €`. Avec les prix visés, il s'agit surtout de la **Joaillerie 925** (149 à 249 €) ou des **paniers de 2 parures**.
- **Traitement** :
  - Moins de codes promo : pas de R2 « livraison offerte » (déjà offerte au-dessus du seuil).
  - Plus de service : P3 version 925 avec le certificat GRA pour les pierres de 0,1 carat et plus, réponse personnelle aux questions, avant-première des nouvelles parures 925.
  - Temps forts : mettre en avant la Joaillerie 925 et les paniers de 2 parures, avec −15 % sur la 2e parure dans le même panier (offre du site). **Attention** : il n'y a qu'une boîte à bijoux par commande, la 2e parure arrive en sachet scellé. Pour « une pour soi + une à offrir dans sa boîte », il faut conseiller deux commandes.
- **Ce qu'on ne fait pas** : pas de « VIP » affiché, pas de faux privilège. On reste sur des avantages concrets.

### 2.4 RFM simple (sans outil prédictif)

Le RFM se calcule par segments dynamiques Brevo sur 3 attributs synchronisés depuis Woo : `DATE_DERNIERE_COMMANDE`, `NB_COMMANDES` et `CA_TOTAL`. Les noms exacts des champs remontés par le plugin sont à vérifier. Sinon, un snippet ou Make les met à jour à chaque commande.

| Score | 3 | 2 | 1 |
|---|---|---|---|
| **R** (récence : jours depuis la dernière commande) | 60 jours ou moins | 61 à 180 jours | Plus de 180 jours |
| **F** (fréquence : nombre de commandes conservées) | 3 ou plus | 2 | 1 |
| **M** (montant : CA TTC cumulé) | Plus de 150 € | 80 à 150 € | Moins de 80 € |

| Segment | Règle | Traitement |
|---|---|---|
| **Fidèles** | R3 et F 2 ou plus | Le Cercle, avant-premières, aucune remise en plus nécessaire |
| **Nouvelles** | R3 et F1 | Post-achat, X1 (J+21), parrainage (PA1) |
| **À chouchouter** | R2 et F 2 ou plus | Nouveautés de l'univers préféré, rappel des avantages du Cercle |
| **À réveiller** | R2 et F1 | Flow de réactivation (J90), temps forts |
| **Endormies** | R1 | 1 envoi par mois au maximum (temps forts), puis sunset à 12 mois sans clic |
| **Grandes occasions** (chevauche les autres) | M3 | Voir §2.3 |

Revue trimestrielle : la taille de chaque segment, le passage d'un segment à l'autre, et le CA par segment.

---

## 3. Programme de fidélité « Le Cercle »

**Le principe** : simple, sans points à calculer, avec des avantages concrets qui tiennent dans la marge.

### 3.1 Entrée

L'entrée est automatique, sans inscription. Deux cas :
- **2e commande conservée** (délai de rétractation de 14 jours écoulé).
- **Ou une commande de 150 € ou plus conservée** (typiquement la Joaillerie 925).

Le flow C1 se déclenche alors (`flows.md` §10). On ne sort pas du Cercle, sauf en cas d'abus (rétractations répétées).

### 3.2 Avantages

| Avantage | Détail | Coût réel estimé |
|---|---|---|
| **Livraison offerte sans minimum** | Coupon Woo « livraison offerte » restreint aux e-mails des membres (champ « e-mails autorisés » des coupons), ou plugin de livraison par rôle | Seulement sur les paniers de **moins de 50 €** (au-dessus, la livraison est déjà offerte). Manque à gagner = le tarif de port facturé d'habitude [tarif à définir]. Branvas facture de toute façon 8,99 $ par commande. |
| **Avant-première de 48 h** | Les nouvelles parures sont annoncées par e-mail 48 h avant le site, et seulement quand il y a de **vraies** nouveautés | 0 € |
| **15 € tous les 3 achats** | Code unique dès 79 € d'achat, valable 60 jours (C2) | 15 € TTC, soit 12,50 € HT, pour 4 commandes : environ **3 € HT par commande** |
| **Anniversaire renforcé** | −15 % au lieu de −10 % (A1), sur une commande | Sur 79 € TTC : environ 9,90 € HT, une fois par an |
| **Réponse personnelle** | Une vraie personne répond aux e-mails, en FR ou en EN | Du temps |

### 3.3 Ce qu'on ne promet pas

- Pas de gravure, pas de personnalisation, **pas de message cadeau** (aucun champ possible, carte personnalisée seulement en offre VIP), pas de cadeau physique supplémentaire dans le colis : Branvas expédie en neutre et nous ne touchons pas le colis.
- Pas de « carte insert personnalisée » tant que l'offre Branvas VIP (149 $ par mois) n'est pas prise.
- Pas de « statut » mis en scène ni de rareté. Le Cercle est un remerciement, pas un club fermé.

### 3.4 Mise en place

- Attributs `CERCLE` et `CERCLE_DATE` dans Brevo.
- Compteur `NB_COMMANDES_CERCLE` pour le palier de 15 €.
- Mise à jour à chaque commande conservée.
- **Plugin de points Woo** : seulement plus tard, si le programme prend de l'ampleur (exemples à évaluer : WooCommerce Points and Rewards, YITH Points and Rewards).
- Une page « Le Cercle » sur le site, en FR et en EN, avec les règles exactes ci-dessus.

---

## 4. Parrainage : « Offre 10 €, reçois 10 € »

| Règle | Détail |
|---|---|
| Filleule | 10 € de réduction sur sa **1re commande**, dès 59 € |
| Marraine | 10 € de bon d'achat dès 59 €, **une fois la commande de la filleule conservée** (14 jours après la livraison, sans rétractation) |
| Plafond | 5 parrainages récompensés par an et par marraine |
| Qui peut parrainer | Toute cliente qui a une commande conservée. Invitation automatique à livraison + 30 jours (PA1), et lien disponible dans l'espace client |
| Anti-abus | Pas d'auto-parrainage (même e-mail, même adresse de livraison ou même moyen de paiement). Nouvelles clientes uniquement. Non cumulable avec le code de bienvenue. |
| Coût | 20 € TTC maximum (environ 16,70 € HT) par **nouvelle cliente réellement conservée**. À comparer au coût d'acquisition mesuré sur Meta et Google : ne pas l'estimer, le mesurer. |
| Outil | Plugin WooCommerce de parrainage (à évaluer : AutomateWoo + Refer A Friend, Advanced Coupons ou équivalent). Le plugin crée les codes, Brevo envoie PA1 et PA2 (ou le plugin les envoie, mais pas les deux). |
| Légal | Conditions écrites et accessibles (page dédiée, FR et EN). Le parrainage n'est jamais lié à un avis. |

Dans le formulaire du plugin, la marraine ne saisit pas l'e-mail de son amie à notre place : elle **partage un lien**. On évite ainsi d'écrire à quelqu'un qui n'a rien demandé.

---

## 5. Collecte du consentement

### 5.1 Principes

- **Case jamais pré-cochée**. Un consentement par canal : l'e-mail et le SMS sont séparés.
- **Double opt-in recommandé** pour toutes les inscriptions newsletter (pop-up, pied de page, checkout).
  - **Pour** : une base propre, sans fautes de frappe ni pièges à spam, une preuve solide du consentement et une meilleure délivrabilité.
  - **Contre** : 15 à 30 % des inscrites ne confirment pas.
  - On l'accepte. Le code −10 % n'arrive **qu'après la confirmation** : c'est la meilleure incitation à cliquer.
- **Preuve conservée** pour chaque contact : date et heure, source (pop-up, checkout…), langue, **texte exact affiché** (avec son numéro de version), adresse IP, date de confirmation du double opt-in.
- **Durée de conservation** (repères CNIL) :
  - Prospects : 3 ans après le dernier contact actif (le dernier clic), puis suppression.
  - Clientes : 3 ans après le dernier achat pour la prospection.
- **Cookies** : le traceur Brevo (navigation abandonnée) ne se charge qu'après consentement via la CMP.
- **Politique de confidentialité** (FR et EN) : elle cite Brevo (hébergé dans l'UE), Judge.me, le plugin de suivi, les finalités, les durées et les droits.

### 5.2 Textes des formulaires

**Pop-up, étape 1** : affiché après 20 secondes ou 50 % de défilement, jamais au checkout, une fois tous les 30 jours au maximum. Sur mobile, un bandeau bas plutôt qu'un plein écran.

| | FR | EN |
|---|---|---|
| Titre | Ouvre. Laisse-toi charmer. | Open it. Let yourself be charmed. |
| Texte | −10 % sur ta première parure, et nos nouveautés une à deux fois par mois. | 10% off your first set, plus our new pieces once or twice a month. |
| Bouton | Recevoir mon code | Get my code |
| Mention | En t'inscrivant, tu acceptes de recevoir nos e-mails (nouveautés, offres, conseils). Tu confirmeras ton adresse par e-mail. Désinscription en un clic, à tout moment. Données traitées par CHARMED PARIS et son prestataire Brevo, hébergé dans l'UE. [Politique de confidentialité] | By signing up, you agree to receive our emails (new pieces, offers, care tips). You'll confirm your address by email. Unsubscribe in one click, any time. Data handled by CHARMED PARIS and its provider Brevo, hosted in the EU. [Privacy policy] |

**Pop-up, étape 2** : facultative, après l'envoi du formulaire.
- FR : « Pour mieux t'écrire (facultatif) : ton prénom · ton style (Sculpture / Éclat / Couleur précieuse / Joaillerie 925 / Mixte) · ton anniversaire (jour et mois, pour un petit cadeau le jour J) »
- EN : « Help us write better (optional): first name · your style · your birthday (day and month, for a small gift on the day) »

**Checkout** : deux cases distinctes, non cochées.
- FR :
  - ☐ « Je veux recevoir les nouveautés et offres CHARMED PARIS par e-mail (1 à 2 par mois). »
  - ☐ « Je veux recevoir les rappels avant les fêtes par SMS (4 par an maximum). STOP à tout moment. »
- EN :
  - ☐ « Send me CHARMED PARIS news and offers by email (once or twice a month). »
  - ☐ « Text me holiday reminders (4 a year at most). Reply STOP any time. »

Le numéro de téléphone demandé au checkout pour DHL (obligatoire hors États-Unis et Royaume-Uni) **ne sert jamais au marketing** sans la case SMS cochée.

**« Préviens-moi » (rupture de stock)**
- FR : « On t'écrit une seule fois, quand cette parure revient. »
- EN : « We'll email you once, when this set is back. »
- Une case newsletter séparée, facultative.

**Centre de préférences** (lien dans chaque pied de page) :
- Langue (FR ou EN).
- Fréquence : normale, ou temps forts seulement.
- Univers préférés.
- Anniversaire.
- E-mail oui/non, SMS oui/non.
- Désinscription totale.

### 5.3 SMS : règles

- France et Royaume-Uni uniquement au lancement. Pas de SMS aux États-Unis (enregistrement 10DLC ou toll-free, TCPA).
- Du lundi au samedi, de 10 h à 19 h. Jamais le dimanche ni un jour férié.
- Expéditeur `CHARMED`. Mention STOP dans chaque message. 4 temps forts par an au maximum.

---

## 6. KPI cibles (prudents)

> Ce sont des ordres de grandeur pour une boutique qui démarre, **pas des promesses**. On les recalibre après 3 mois de données réelles. Les taux d'ouverture sont faussés par Apple Mail Privacy Protection : on pilote aux **clics**, aux **commandes** et au **CA attribué** (attribution à 5 jours après un clic).

### Collecte

| KPI | Cible mois 1 à 3 | Cible mois 6 à 12 |
|---|---|---|
| Taux d'inscription au pop-up (visiteuses uniques) | 1,5 à 3 % | 2 à 4 % |
| Taux de confirmation du double opt-in | 70 % ou plus | 75 % ou plus |
| Opt-in e-mail au checkout | 15 à 25 % | 20 à 30 % |
| Opt-in SMS au checkout | 3 à 8 % | 5 à 10 % |

### Flows

| Flow | KPI | Cible prudente |
|---|---|---|
| Bienvenue | Commande dans les 14 jours après la confirmation | 3 à 6 % des confirmées |
| Bienvenue | Taux de clic par e-mail | 3 à 7 % |
| Panier abandonné | Paniers récupérés (sur les paniers identifiés) | 3 à 8 % |
| Navigation abandonnée | Conversion | 0,5 à 2 % (volume faible, à cause des cookies) |
| Demande d'avis (P4 + P4b) | Avis laissés / commandes livrées | 5 à 10 % |
| Cross-sell (X1 + X2) | Conversion | 1 à 3 % |
| Anniversaire | Conversion | 3 à 8 % |
| Réactivation | Retour à l'achat | 1 à 3 % |
| Retour en stock | Conversion | 5 à 15 % |
| Temps forts | CA par e-mail envoyé | À mesurer en 2026, puis cible +10 % en 2027 |

### Santé de la base (seuils d'alerte)

| KPI | Seuil |
|---|---|
| Rebonds (bounces) | Moins de 2 % |
| Plaintes pour spam | **Moins de 0,1 %** (Gmail sanctionne au-delà de 0,3 %) |
| Désinscriptions par campagne | Moins de 0,5 % |
| Désinscriptions par e-mail de flow | Moins de 1 % |
| Part de contacts engagés (clic dans les 90 jours) | 25 % ou plus |

### Business

| KPI | Cible à 6 mois | Cible à 12 mois |
|---|---|---|
| Part du CA attribuée au CRM (e-mail + SMS) | 10 à 15 % | 15 à 25 % |
| Taux de réachat à 12 mois (clientes avec 2 commandes ou plus) | — | 10 à 20 % |
| Membres du Cercle / clientes | 3 à 5 % | 5 à 10 % |
| Nouvelles clientes venues du parrainage | 1 à 3 % | 2 à 5 % |
| Taux de rétractation | À suivre (à nos frais, voir §7) : on enquête au-delà de 8 % | |

---

## 7. Garde-fou sur la marge

**Exemple réel, Molten Art (JSGRQR)**, prix de vente visé : 49 € TTC.

| Ligne | Montant |
|---|---|
| Prix HT (TVA 20 %) | 40,83 € |
| Coût Branvas : produit 16,87 $ + livraison 8,99 $ + frais 2,9 % + 0,30 $ ≈ 26,90 $ | ≈ **23,10 €** (au change d'environ 0,86 €/$, à vérifier) |
| Frais de paiement de la boutique (Stripe ou PayPal, à confirmer) | ≈ 1 € |
| **Marge avant packaging payant, publicité et retours** | **≈ 16,70 €** |
| Avec le code bienvenue −10 % | ≈ 12,60 € |

**Règles qui en découlent :**
1. **Une seule remise par commande** (coupons Woo « usage individuel »). Elles ne se cumulent jamais avec −15 % sur la 2e parure.
2. **Pas de remise de plus de 15 %** sur Sculpture, Éclat et Mixte (les parures à petit prix).
3. Les codes en euros (15 € du Cercle, 10 € du parrainage) ont un **minimum de commande** (79 € et 59 €).
4. **Rétractations à nos frais** : Branvas ne reprend que les colis abîmés, les défauts et les erreurs, signalés dans les 10 jours. Chaque rétractation coûte le port de retour vers notre adresse en France [à définir], plus la remise en vente. Le taux de rétractation est donc surveillé (§6), et P2 et P3 donnent tous les repères pour éviter les mauvaises surprises : taille, matière, entretien.
5. **Coûts réels des autres SKU** (surtout la Joaillerie 925) : à relever dans le compte Branvas **avant** de fixer le −15 % anniversaire du Cercle sur ces parures.
