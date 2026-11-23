# Architecture des automatisations CRM

CHARMED PARIS · outil recommandé : **Brevo Standard** (voir `choix-outil.md`). L'équivalent Klaviyo est indiqué pour chaque étape. Site **bilingue FR + EN** : chaque flow existe dans les deux langues.

Textes des e-mails : `emails-flows.md` (FR) et `emails-flows-en.md` (EN). Mêmes identifiants (B1, P2, NO3…) dans les deux fichiers.
Textes des e-mails transactionnels WooCommerce de base et des **3 relances panier** : `woocommerce/contenus/microcopy.md` (écrits par un autre agent, non repris ici).
Faits logistiques : `woocommerce/source/FAITS-BRANVAS.md`, qui fait foi.

---

## 0. Règles communes à tous les flows

### 0.1 Langue : un seul workflow, deux branches

- Attribut contact **`LANGUE`** = `fr` | `en`.
- **Détection**, par ordre de priorité :
  1. Langue de la page où le formulaire a été rempli (champ caché ajouté par le plugin multilingue : WPML, Polylang ou TranslatePress).
  2. Langue de la commande (méta de commande ajoutée par le plugin multilingue, à vérifier sur la préproduction).
  3. Repli sur le pays : FR, BE, CH, LU, MC → `fr` ; tous les autres → `en`.
  4. Mise à jour possible par la cliente dans le centre de préférences.
- **Structure** : chaque workflow commence par une condition `LANGUE = en ?`. Branche oui : modèles EN. Branche non : modèles FR (repli par défaut). Les délais et les conditions sont **identiques** dans les deux branches, pour ne maintenir qu'une seule logique.
- Klaviyo : *Conditional split* sur la propriété `language`.

### 0.2 Pays et délais réels de livraison

Source : FAQ Branvas, 90 % des colis, **de la commande à la livraison**, en jours ouvrés. Préparation de 1 à 2 jours ouvrés. Transporteur DHL (USPS aux États-Unis). **Un seul mode de livraison, pas d'express, pas de date garantie.** Droits et taxes payés (DDP) : rien à payer à la livraison.

| Pays (`PAYS`) | Délai total | `DELAI_MIN` | `DELAI_MAX` |
|---|---|---|---|
| France, Allemagne, Espagne | 4–9 j. ouvrés | 4 | 9 |
| Pays-Bas | 4–6 | 4 | 6 |
| Italie | 3–10 | 3 | 10 |
| Irlande | 5–11 | 5 | 11 |
| Royaume-Uni | 3–7 | 3 | 7 |
| États-Unis | 3–8 | 3 | 8 |
| Canada | 4–8 | 4 | 8 |
| Australie | 3–8 | 3 | 8 |
| Autres pays (dont Belgique, Suisse et Luxembourg tant que Branvas ne publie pas leur délai) | 4–12 | 4 | 12 |

- `DATE_LIVRAISON_MAX` = date de commande + `DELAI_MAX` jours ouvrés. Calculée à la commande (attribut de commande, ou champ calculé par un snippet ou par Make/Zapier).
- Dans les e-mails, on écrit « dans 9 cas sur 10 » ou « en général », **jamais « garanti »**.

### 0.3 Base légale de chaque envoi

| Type | Flows | Consentement marketing requis ? |
|---|---|---|
| **Transactionnel** (lié à la commande) | P1 expédition, P2 écrin, e-mails natifs Woo | Non. |
| **Service** (information sur le produit acheté, **sans promotion**) | P3 entretien | Non. Ces e-mails restent donc strictement sans code ni produit mis en avant. |
| **Demande d'avis** | P4 (Judge.me) | Traité comme un envoi marketing léger. Envoyé aux clientes non opposées, avec un lien de désinscription Judge.me. À valider avec ton conseil juridique. |
| **Marketing** | Bienvenue, navigation, panier, cross-sell, anniversaire, réactivation, temps forts, Le Cercle, parrainage | **Oui** : opt-in e-mail (case non pré-cochée et double opt-in, voir `segmentation-et-fidelite.md` §5). |
| **SMS marketing** | NO-SMS, SV-SMS, FM-SMS, RS-SMS | **Oui** : opt-in SMS **séparé**, mention « STOP » dans chaque SMS. |
| **Retour en stock** | RS1 | Consentement spécifique : la demande « préviens-moi » pour **ce** produit. Un seul e-mail. |

> Option juridique non retenue par défaut : l'« exception client » (art. L34-5 CPCE) autorise la prospection par e-mail des clientes pour des produits analogues, si elles ont été informées et ont pu s'y opposer au moment de la commande. On préfère une **case opt-in non pré-cochée** pour une base propre et sans ambiguïté. À revoir avec un juriste si le taux d'opt-in au checkout est très bas.

### 0.4 Données et événements nécessaires

**Attributs contact (Brevo)**
`PRENOM`, `LANGUE`, `PAYS`, `OPT_IN_EMAIL` (date, source, texte affiché), `OPT_IN_SMS` (idem), `SMS`, `DATE_ANNIV` (jj/mm, sans l'année), `NB_COMMANDES`, `CA_TOTAL`, `DATE_DERNIERE_COMMANDE`, `UNIVERS_PREFERE`, `ACHAT_CADEAU` (`oui`, `non` ou `inconnu`), `CERCLE` (oui/non + date d'entrée), `SCORE_R`, `SCORE_F`, `SCORE_M`, `SEGMENT_RFM`, `CODE_BIENVENUE`, `CODE_ANNIV`, `CODE_X`, `DATE_LIVRAISON`, `DATE_LIVRAISON_MAX`, `DATE_AVIS_PREVUE`, `SAV_OUVERT` (oui/non), `RETRACTATION` (oui/non).

**Événements**

| Événement | Source | Utilisé par |
|---|---|---|
| `contact_confirmed` (double opt-in validé) | Formulaire Brevo | Bienvenue |
| `product_viewed` | Traceur Brevo ou snippet, **après consentement cookies** | Navigation abandonnée |
| `cart_updated` / panier abandonné | Plugin Brevo for WooCommerce | Panier |
| `order_created` (statut « En cours ») | Plugin Brevo | Post-achat, sortie de flows |
| `tracking_added` (numéro DHL écrit par Branvas dans la commande) | Plugin de suivi ou snippet | P1 |
| `out_for_delivery` / `delivered` | Plugin de suivi connecté à DHL : TrackShip + Advanced Shipment Tracking, AfterShip ou Parcel Panel, **compatibilité avec le champ de suivi Branvas à tester** | P2, P3, P4, X1 |
| `order_refunded` / rétractation | Woo | Exclusions |
| `back_in_stock` | Plugin Woo « préviens-moi », sur le passage du stock de 0 à plus de 0 (synchro Branvas) | Retour en stock |

**Si aucun plugin ne sait lire la livraison réelle** : repli sur `DATE_LIVRAISON_MAX` partout où ce document dit « livraison réelle ». C'est moins précis mais sûr, car on n'écrit jamais trop tôt.

**Statut de commande** : Branvas n'expédie que les commandes payées (« En cours »). Le passage à « Terminée » par Branvas est **à confirmer**. S'il existe, il peut servir de déclencheur de secours pour P1.

### 0.5 Pression marketing et priorités

- **Plafond** : 3 e-mails marketing par contact et par semaine au maximum, flows et campagnes compris. Un seul SMS marketing par semaine au maximum, quatre temps forts par an au maximum.
- **Écart minimum** de 20 h entre deux e-mails marketing. Les e-mails transactionnels et de service ne comptent pas.
- **Priorités** en cas de conflit, de la plus haute à la plus basse :
  1. Transactionnel (P1, P2).
  2. Panier abandonné.
  3. Retour en stock.
  4. Bienvenue.
  5. Navigation abandonnée.
  6. Post-achat de service (P3).
  7. Anniversaire.
  8. Cross-sell.
  9. Temps forts.
  10. Réactivation.
  11. Campagnes ponctuelles.
- **Une seule promotion active à la fois** par contact. Les codes ne se cumulent pas (règle Woo : « usage individuel uniquement »).
- **Heures d'envoi** :
  - E-mails : entre 8 h et 21 h dans le fuseau du contact. Un déclencheur nocturne est retenu jusqu'à 8 h.
  - SMS France : du lundi au samedi, de 10 h à 19 h, jamais le dimanche ni un jour férié (recommandations de la profession, AF2M).
  - SMS Royaume-Uni : mêmes plages.
  - **Pas de SMS aux États-Unis au lancement** : l'enregistrement 10DLC ou toll-free est obligatoire, et la TCPA est très stricte.
- **Expéditeur** : `CHARMED PARIS <bonjour@charmedparis.fr>` (domaine à acheter : il était libre au 22/11/2026). Les réponses arrivent dans une vraie boîte, lue. Expéditeur SMS : `CHARMED`.
- **Délivrabilité** :
  - SPF, DKIM et DMARC (au départ `p=none`, puis `quarantine`).
  - Désabonnement en un clic (List-Unsubscribe).
  - Montée en charge progressive les 4 premières semaines, en commençant par les contacts les plus récents.
- **Pied de page** de tous les e-mails : raison sociale et adresse **de CHARMED PARIS** (jamais celle de Branvas), lien de désinscription, lien vers le centre de préférences (langue, fréquence, univers, anniversaire).

### 0.6 Codes promo

| Code | Valeur | Validité | Règles |
|---|---|---|---|
| Bienvenue (`BV-xxxxxx`, unique) | −10 % | 14 jours | Première commande seulement, une utilisation, non cumulable |
| Cross-sell (`X-xxxxxx`, unique) | −10 % sur la parure suivante | 14 jours | Une utilisation. Test A/B prévu contre l'absence de code (voir §5) |
| Anniversaire (`AN-xxxxxx`, unique) | −10 % (−15 % pour Le Cercle) | 30 jours (de J−3 à J+27) | Un code par an |
| Réactivation (`RV-xxxxxx`, unique) | Livraison offerte sans minimum | 14 jours | Une utilisation |
| Le Cercle | Livraison offerte sans minimum et 15 € tous les 3 achats | Voir `segmentation-et-fidelite.md` | Coupon Woo restreint aux e-mails des membres |
| Parrainage | 10 € pour la filleule et 10 € pour la marraine, dès 59 € | Voir `segmentation-et-fidelite.md` | Géré par un plugin |

- Les codes uniques sont **créés dans WooCommerce**, en masse (plugin type Smart Coupons, ou WP-CLI), puis **importés dans une collection de codes Brevo**. Chaque e-mail tire un code de la collection.
- Le code « 2e parure −15 % » de la maquette s'applique **dans le même panier**. Il ne se cumule pas avec les codes ci-dessus.

### 0.7 Exclusions globales (vérifiées à chaque étape marketing)

- Désinscrit·e, adresse en erreur définitive (hard bounce), plainte pour spam.
- `SAV_OUVERT = oui` : réclamation en cours, aucune promo tant qu'elle n'est pas réglée.
- Rétractation ou remboursement dans les 30 derniers jours : pas de cross-sell ni de demande d'avis sur la commande concernée.
- Commande passée pendant le flow : sortie immédiate des flows de conquête (bienvenue, navigation, panier, réactivation).

---

## 1. Bienvenue (B0 à B4)

**Objectif** : confirmer l'inscription, présenter la marque et les 5 univers, transformer l'inscription en première commande grâce au code −10 %.
**Klaviyo** : liste « Newsletter » avec double opt-in, puis flow *Welcome Series*.

| Étape | Déclencheur ou délai | Contenu | Conditions |
|---|---|---|---|
| **B0** | Inscription (pop-up, pied de page, centre de préférences) | E-mail de **confirmation** (double opt-in) | Envoi immédiat. Sans clic sous 48 h : un seul rappel (B0 bis), puis abandon. |
| **B1** | Confirmation (`contact_confirmed`) + 0 min | Merci, code −10 % valable 14 jours, l'idée de l'écrin | Si `NB_COMMANDES ≥ 1` : variante **B1-cliente** sans code. |
| **B2** | B1 + 2 jours | Les 5 univers, comment choisir | Sortie si commande |
| **B3** | B2 + 3 jours (J+5) | Pour soi ou pour offrir : écrin, chamoisine, pochette, carte d'entretien, livraison et retours | Sortie si commande |
| **B4** | J+11 | Rappel factuel : le code est valable jusqu'au {date} | Seulement si le code n'est pas utilisé. Sortie si commande. |

- **Sortie** : commande passée, avec bascule vers le post-achat. Désinscription.
- **Après B4** : le contact rejoint les campagnes régulières (1 à 2 par mois au lancement).
- **Objectif chiffré** : voir `segmentation-et-fidelite.md` §6.

---

## 2. Navigation abandonnée (N1, N2)

**Objectif** : rappeler une parure regardée, sans pression ni code.
**Prérequis** : traceur actif **après consentement cookies**, et contact identifié (cookie Brevo associé à l'e-mail). Volume faible attendu.
**Klaviyo** : flow *Browse Abandonment* sur l'événement *Viewed Product*.

| Étape | Délai | Contenu |
|---|---|---|
| Déclencheur | `product_viewed` sur une fiche parure | |
| Attente | 4 h | |
| Contrôle | Aucun ajout au panier ni commande depuis la consultation. Pas dans le flow panier. Pas de commande ces 7 derniers jours. Pas déjà entré dans ce flow ces 14 derniers jours. | |
| **N1** | +4 h | La parure regardée (image, nom, univers, prix) et 2 détails concrets (matière, ce qu'il y a dans l'écrin) |
| Attente | 2 jours | |
| **N2** | +2 j | 3 parures du même univers, le guide « comment choisir », la réassurance (livraison, retours) |

- **Sortie** : ajout au panier, qui fait basculer vers le flow panier. Commande. Clic suivi d'un achat.
- **Pas de code promo** dans ce flow : on ne veut pas apprendre aux visiteuses à attendre une remise.

---

## 3. Panier abandonné (renvoi vers microcopy)

**Les textes des 3 relances sont dans `woocommerce/contenus/microcopy.md` et ne sont pas repris ici.** Ce document fixe seulement la mécanique.

| Étape | Délai recommandé | Notes |
|---|---|---|
| Déclencheur | Panier abandonné (plugin Brevo for WooCommerce), contact identifié et opt-in marketing | Klaviyo : *Started Checkout* ou *Added to Cart* |
| Relance 1 | +1 h | Contenu dynamique du panier : image, nom, prix, lien de retour au panier |
| Relance 2 | +24 h | |
| Relance 3 | +72 h | Recommandation : **pas de code par défaut**. Si le panier fait moins de 50 €, rappeler le seuil de livraison offerte. |

- Si `microcopy.md` fixe d'autres délais, **ses délais font foi**. Il suffit d'aligner le workflow.
- **Sortie** : commande, panier vidé, désinscription.
- **Branches FR et EN** : comme partout, selon `LANGUE`.
- **Paniers des inscrites en bienvenue** : le flow panier prend la priorité, et la bienvenue est mise en pause pendant le flow panier (72 h).

---

## 4. Post-achat (P1 à P4)

**Objectif** : rassurer pendant l'attente (expédition depuis l'étranger, plusieurs jours), réussir l'ouverture de l'écrin, faire durer la dorure, obtenir de **vrais** avis.

### Chronologie type, commande en France (en jours ouvrés, 4 à 9 jusqu'à la livraison)

```
J0      commande payée (« En cours »)        → e-mail natif Woo (microcopy.md)
J+1/2   préparation, n° DHL écrit dans Woo   → P1 « Ta parure est en route »
J+4…    « en cours de livraison » DHL        → P2 « Ton écrin arrive »  (repli : J+4 ouvrés)
J+4…9   livraison réelle (dans 9 cas sur 10) → —
Liv.+2  jours                                → P3 Conseils d'entretien (service, sans promo)
J+21    (calendaire)                         → X1 cross-sell (voir §5, règle d'écart avec P4)
Liv.+14 jours                                → P4 Demande d'avis (envoyée par Judge.me)
Liv.+21 jours                                → P4b Rappel d'avis (une seule fois, Judge.me)
```

| Étape | Déclencheur | Repli si l'événement manque | Contenu | Base |
|---|---|---|---|---|
| **P1** | `tracking_added` | Statut « Terminée », si Branvas le pose (à confirmer) | Lien de suivi DHL, délai réel du pays, « rien à payer à la livraison », ce qu'il y a dans le colis | Transactionnel |
| **P2** | `out_for_delivery` DHL | Commande + `DELAI_MIN` jours ouvrés, à 8 h, si la livraison n'est pas encore confirmée | « Ton écrin arrive » : comment l'ouvrir, quoi garder. Variantes **pour soi** et **cadeau**. Question en un clic « pour toi ou pour offrir ? » si `ACHAT_CADEAU = inconnu`. Un souci ? Écris-nous dans les 10 jours. | Transactionnel |
| **P3** | `delivered` + 2 jours | `DATE_LIVRAISON_MAX` + 2 jours | Entretien, adapté à l'univers de la parure (doré, zircons, argent 925 et moissanite, cordon) | Service : **aucune promo** |
| **P4** | `delivered` + 14 jours | `DATE_LIVRAISON_MAX` + 14 jours | Demande d'avis (texte dans `emails-flows*.md`, à coller dans Judge.me) | Voir §0.3 |
| **P4b** | P4 + 7 jours, si aucun avis | — | Rappel unique, plus court | |

**Points de configuration :**

- **P1 et l'e-mail natif « Commande terminée »** : si `microcopy.md` prévoit déjà un e-mail natif avec le suivi, **un seul des deux doit partir**. Recommandation : garder P1, plus riche, et désactiver le natif « Commande terminée » dans WooCommerce. Ou l'inverse, mais jamais les deux.
- **P4 dans Judge.me** :
  - Déclencheur sur la livraison réelle, si l'intégration de suivi le permet (à vérifier). Sinon, sur « Terminée » + (`DELAI_MAX` + 14) jours, soit environ 25 jours pour la France.
  - Brevo n'envoie **pas** de demande d'avis en doublon.
  - Avis **sans contrepartie** au lancement. Si un jour une contrepartie est offerte, elle doit être signalée sur l'avis (obligation d'information sur les avis en ligne, Code de la consommation).
- **Exclusions** : P3 et P4 ne partent pas si `SAV_OUVERT = oui` ou si une rétractation est en cours.
- **Commande cadeau livrée à une autre adresse** : aucun e-mail ne part vers la destinataire. On n'a ni son adresse ni son consentement.
- **Réclamation** : Branvas ne traite les colis abîmés, les défauts et les erreurs d'article que s'ils sont signalés **dans les 10 jours suivant la livraison, photos à l'appui**. P2 et P3 invitent donc à écrire vite. Ils rappellent aussi que la garantie légale de conformité de 2 ans reste valable : on ne la restreint jamais.
- **Klaviyo** : flow sur *Fulfilled Order*, avec les événements de livraison d'AfterShip ou d'un autre outil de suivi.

---

## 5. Cross-sell 2e parure (X1, X2)

**Objectif** : une deuxième parure, pour soi ou à offrir, chez les clientes satisfaites.

| Étape | Délai | Contenu | Conditions |
|---|---|---|---|
| Déclencheur | Commande + 21 jours calendaires | | Opt-in marketing. Livraison confirmée depuis au moins 5 jours (repli : `DATE_LIVRAISON_MAX` dépassée). Pas de SAV ni de rétractation. Pas d'autre commande depuis. |
| Règle d'écart avec P4 | Si `DATE_AVIS_PREVUE` tombe à 2 jours ou moins de J+21, X1 part **3 jours après** P4 | | Évite deux sollicitations le même jour |
| **X1** | | 3 parures choisies selon `UNIVERS_PREFERE` (même univers ou univers voisin, voir `segmentation-et-fidelite.md` §2), code −10 % valable 14 jours | Variante **cadeau** si `ACHAT_CADEAU = oui` : « une pour toi cette fois ? » ou « à qui l'offrir ensuite ? » |
| **X2** | X1 + 10 jours | Rappel factuel : le code expire le {date} | Seulement si X1 a été ouvert ou cliqué et que le code n'est pas utilisé |

- **Test A/B** à partir de 500 envois : X1 avec code contre X1 sans code (simple sélection). On garde le code seulement s'il augmente **la marge totale**, pas seulement le taux de conversion.
- **Sortie** : commande, désinscription.

---

## 6. Anniversaire (A1, A2)

**Prérequis** : `DATE_ANNIV` (jour et mois seulement) saisie **volontairement**, avec la mention de son usage (pop-up étape 2, centre de préférences, espace client). Champ facultatif, jamais obligatoire. La date n'est modifiable qu'une fois par an (anti-abus).

| Étape | Délai | Contenu |
|---|---|---|
| **A1** | `DATE_ANNIV` − 3 jours, à 9 h | Bon anniversaire, code −10 % (−15 % pour Le Cercle) valable 30 jours, 3 parures de l'univers préféré |
| **A2** | A1 + 20 jours | Seulement si le code n'est pas utilisé : rappel bref, date d'expiration |

- **Conditions** : opt-in marketing, pas de SAV ouvert, un code par contact et par an.
- **Klaviyo** : flow sur la *date property* `birthday`.

---

## 7. Réactivation 90 jours (R1 à R3)

**Objectif** : faire revenir une cliente qui n'a pas recommandé depuis 90 jours. Sinon, connaître ses préférences, ou la laisser partir proprement.

| Étape | Délai | Contenu | Conditions |
|---|---|---|---|
| Déclencheur | `DATE_DERNIERE_COMMANDE` + 90 jours | | Opt-in marketing. Aucune commande depuis. N'est pas dans un autre flow de conquête. |
| **R1** | J90 | Nouveautés de l'univers préféré, sans code | |
| **R2** | J97 | Livraison offerte sans minimum, code valable 14 jours | Seulement si R1 n'a pas été cliqué |
| **R3** | J111 | « On reste en contact ? » : choisir sa fréquence (normale, ou temps forts seulement), changer d'univers ou de langue, ou se désinscrire en un clic | Seulement si R1 et R2 n'ont pas été cliqués |

- **Après R3, sans clic ni visite pendant 90 jours** : statut « dormante », un envoi par mois au maximum (temps forts). **Après 12 mois sans clic** : suppression des envois marketing (*sunset*), pour protéger la délivrabilité.
- **Abonnées jamais clientes** : même logique, déclenchée 90 jours après le dernier clic. R1 présente alors les parures les plus consultées (pas « les plus vendues » tant qu'on n'a pas de chiffres réels). R2 offre la livraison offerte.
- **Ouvertures** : Apple Mail Privacy Protection gonfle les taux d'ouverture. L'engagement se mesure donc aux **clics et aux visites**, pas aux ouvertures.
- **Klaviyo** : flow *Win-back* sur *Placed Order*, avec un filtre « n'a pas commandé depuis ».

---

## 8. Temps forts « offrir » : Noël, Saint-Valentin, fête des mères

**Objectif** : aider à offrir **à temps**. Les seules dates mises en avant sont des **dates limites réelles de livraison**, calculées depuis les délais Branvas. Ce n'est pas une urgence inventée. Aucun compte à rebours, aucun « stock limité ».
**Audience** : opt-in marketing, envoyé d'abord au segment `ACHAT_CADEAU = oui`, puis à tous.
**Format** : campagnes programmées (dates fixes). En Brevo, plus simple en **campagnes segmentées par `LANGUE` et `PAYS`** qu'en workflow.

### 8.1 Noël 2026 (dates officielles Branvas)

- **Date limite de commande pour une livraison avant Noël** :
  - Europe et Canada : **vendredi 4 décembre 2026**.
  - Royaume-Uni, États-Unis et Australie : **mardi 8 décembre 2026**.
  - Reste du monde : **lundi 30 novembre 2026**.
  - Au-delà, pas de garantie.
- **Emballage de Noël offert jusqu'au 24 décembre**, automatique : papier cadeau de fête, ruban, décorations, carte de Noël. Le papier nid d'abeille en plus est réservé aux offres Scale et VIP.
- **Pas de gravure ni de personnalisation**, à ne jamais promettre.
- Afficher les mêmes dates dans le bandeau, les fiches produits et le checkout (cohérence avec le site).

| Envoi | Europe et Canada (FR + EN) | Royaume-Uni, États-Unis, Australie (EN) | Reste du monde (EN, FR si `LANGUE = fr`) |
|---|---|---|---|
| **NO1** idées par budget et par univers, emballage offert, date limite | Mardi 24 nov. | Mardi 24 nov. | Mardi 24 nov. |
| **NO2** « il reste une semaine » (factuel) | Lundi 30 nov. | Mardi 1er déc. | — (la date limite tombe ce jour-là) |
| **NO3** « dernier jour conseillé : demain » | Jeudi 3 déc. | Lundi 7 déc. | Samedi 28 nov. |
| **SMS NO** (opt-in SMS uniquement) | Vendredi 4 déc., 10 h | Royaume-Uni seulement : mardi 8 déc., 10 h | — |
| **NO4** « après la date limite » : commander quand même, sans promesse de date, avec la carte « Ton écrin arrive » à imprimer et glisser sous le sapin (PDF à préparer, FR et EN) | Lundi 7 déc. | Mercredi 9 déc. | Mardi 1er déc. |

- **Exclusions** : commande passée dans les 48 dernières heures (pour NO2 et NO3). Commande non encore livrée (on n'en rajoute pas).
- **Black Friday (vendredi 27 novembre 2026)** : ne pas créer d'opération de remise en vitesse. Pas d'envoi ce jour-là. C'est cohérent avec le ton de la marque.

### 8.2 Saint-Valentin 2027 (dimanche 14 février)

**Dates limites calculées** pour une livraison au plus tard le vendredi 12 février : « vendredi 12 février » moins `DELAI_MAX` jours ouvrés. **À remplacer par la date officielle Branvas si elle est publiée.**

| Zone | Commander au plus tard |
|---|---|
| France, Allemagne, Espagne | Lundi 1er février 2027 |
| Royaume-Uni | Mercredi 3 février 2027 |
| États-Unis | Mardi 2 février 2027 |
| Autres pays | Vendredi 12 février moins `DELAI_MAX` (Italie : 29 janvier ; Irlande : 28 janvier ; reste du monde : 27 janvier) |

| Envoi | Date (France) | Contenu |
|---|---|---|
| **SV1** | Mardi 19 janv. | Offrir, ou se faire offrir : le lien à transférer, date limite |
| **SV2** | Jeudi 28 janv. | Rappel de la date limite (lundi) |
| **SMS SV** | Samedi 30 janv., 11 h | Opt-in SMS |

Royaume-Uni et États-Unis : SV1 le mardi 19 janvier, SV2 le lundi 1er février. SMS au Royaume-Uni le mardi 2 février.

### 8.3 Fête des mères 2027 (les dates diffèrent selon le pays)

| Pays | Date | Commander au plus tard (calcul) |
|---|---|---|
| **France** | Dimanche 30 mai 2027 | **Vendredi 14 mai** (9 jours ouvrés avant le vendredi 28 mai, lundi de Pentecôte du 17 mai exclu) |
| Belgique, Suisse | Dimanche 9 mai 2027 | Délai non publié par Branvas. Calcul prudent sur 12 jours ouvrés : **lundi 19 avril** (à confirmer) |
| Royaume-Uni, Irlande (*Mothering Sunday*) | Dimanche 7 mars 2027 | Royaume-Uni : **mercredi 24 février**. Irlande : **jeudi 18 février**. |
| États-Unis, Canada, Australie | Dimanche 9 mai 2027 | **Mardi 27 avril** |

| Envoi | Moment | Contenu |
|---|---|---|
| **FM1** | Environ 12 jours avant la date limite du pays | Idées par univers, date limite |
| **FM2** | Veille de la date limite | Rappel factuel |
| **SMS FM** | Jour de la date limite, 10 h à 11 h | France et Royaume-Uni, opt-in SMS |

Dates précises FM1 et FM2 : France, 3 et 13 mai. Belgique et Suisse, 7 et 16 avril. Royaume-Uni et Irlande, 10 février et la veille de la date limite du pays. États-Unis, Canada et Australie, 15 et 26 avril.

> **Fête des pères** : seulement si la petite ligne homme existe. Même mécanique, avec une date propre à chaque pays.

---

## 9. Retour en stock (RS1)

**Prérequis** :
- Bouton « Préviens-moi » sur les fiches en rupture (plugin Woo type *Back In Stock Notifier*, à choisir), avec la mention « On t'écrit une seule fois, quand cette parure revient ». Pas d'inscription à la newsletter sans case dédiée.
- Branvas ne publie **ni quantités ni date de réassort**. On ne promet donc rien.

| Étape | Déclencheur | Contenu |
|---|---|---|
| **RS1** | Stock de la parure qui repasse de 0 à plus de 0 (synchro Branvas), puis le plugin ajoute le contact à une liste Brevo ou déclenche l'événement `back_in_stock` | « Elle est de nouveau disponible », lien direct vers la fiche. **Un seul e-mail.** |
| **SMS RS** | Même déclencheur | Seulement si opt-in SMS **et** demande faite par SMS |

- **Si la parure repasse en rupture avant l'envoi** : annuler. Le plugin vérifie le stock au moment de l'envoi, à tester.
- **Pas de mention de rareté** (« plus que 3 », « vite »).
- **Klaviyo** : flow natif *Back in Stock* (WooCommerce supporté, à vérifier).

---

## 10. Le Cercle et parrainage (flows techniques)

Règles du programme : voir `segmentation-et-fidelite.md` §3 et §4.

| Flow | Déclencheur | E-mails |
|---|---|---|
| **Entrée dans Le Cercle** | 2e commande conservée (délai de rétractation de 14 jours écoulé), **ou** une commande de 150 € ou plus conservée. `CERCLE = oui`, e-mail ajouté à la liste des e-mails autorisés du coupon Woo « livraison offerte membre ». | **C1** Bienvenue dans Le Cercle |
| **Palier 15 €** | Tous les 3 achats conservés dans Le Cercle | **C2** « Tes 15 € sont prêts », code valable 60 jours |
| **Invitation au parrainage** | Livraison + 30 jours, sans rétractation ni SAV, 1re commande | **PA1** « Offre 10 €, reçois 10 € » |
| **Récompense de la marraine** | Commande de la filleule conservée (14 jours écoulés) | **PA2** « Merci, tes 10 € sont là » (ou e-mail natif du plugin, mais pas les deux) |

---

## 11. Ordre de mise en place

1. **Semaine 1 : fondations.**
   - Domaine d'envoi et authentification SPF, DKIM, DMARC.
   - Plugin Brevo et plugin multilingue.
   - Attributs, avec la langue et le pays.
   - Bannière cookies (CMP).
   - Formulaires avec double opt-in.
   - Centre de préférences.
2. **Semaine 1, en urgence calendaire : Noël.** NO1 part le 24 novembre. Il faut donc d'abord le domaine, le double opt-in et B0/B1, puis NO1 à NO4.
3. **Semaine 2.** Panier (textes de microcopy), puis post-achat P1 à P3, plugin de suivi DHL et Judge.me (P4).
4. **Semaine 3.** Bienvenue complète (B2 à B4), anniversaire, retour en stock.
5. **Mois 2.** Cross-sell, réactivation (premières clientes à J90 vers fin février), Le Cercle, parrainage, navigation abandonnée (si le test du traceur est concluant).
6. **Chaque mois.** Revue des KPI (`segmentation-et-fidelite.md` §6), un test A/B par flow à la fois.
