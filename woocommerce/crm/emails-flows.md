# Textes des e-mails des flows : français

CHARMED PARIS · branche `LANGUE = fr`. La version anglaise est dans `emails-flows-en.md`, avec les mêmes identifiants. La mécanique (déclencheurs, délais, conditions) est dans `flows.md`.
Panier abandonné : textes dans `woocommerce/contenus/microcopy.md`, non repris ici.

## Conventions

- **Variables (syntaxe Brevo)** :
  - `{{ contact.PRENOM }}`. Si le prénom est vide, la salutation devient « Bonjour, ».
  - `{{ params.… }}` pour les données de commande ou d'événement.
  - `[[ … ]]` pour un bloc dynamique ou une condition à configurer.
- **Crochets « [à confirmer] »** : information à valider avant l'envoi (packaging retenu, adresse de retour, prix).
- **Signature** : « L'équipe CHARMED PARIS ». Ou le prénom de la fondatrice, si elle veut signer (à décider). La même partout.
- **Mots interdits** : waterproof, plaqué or, vermeil, sans nickel, hypoallergénique, gravure, personnalisation, stock limité, dernières pièces, compte à rebours, et aucun avis ni chiffre de vente inventé.
- **Matières, formulations autorisées** :
  - Sculpture et Éclat : « laiton doré à l'or fin ».
  - Couleur précieuse : « finition argentée [à confirmer selon la fiche] ».
  - Joaillerie 925 : « argent 925 et moissanite de laboratoire ».
  - Perles : « perles de culture d'eau douce » seulement si la fiche Branvas le dit, sinon « perles simulées ».
- **Pied de page commun** :
  - « CHARMED PARIS · [raison sociale, adresse en France] ».
  - « Tu reçois cet e-mail parce que tu t'es inscrite sur charmedparis.fr. »
  - Liens : Mes préférences · Se désinscrire.

---

## Bienvenue

### B0. Confirmation d'inscription (double opt-in)

**Objet** : Un clic pour confirmer
**Pré-header** : Et ton code de bienvenue arrive juste après.

Bonjour {{ contact.PRENOM }},

Merci de vouloir nous suivre.
Il reste une étape : confirme ton adresse. On veut être sûrs que c'est bien toi.

**[Je confirme mon inscription]**

Ton code de bienvenue (−10 % sur ta première parure) arrive dès que tu as cliqué.
Tu n'as rien demandé ? Ignore ce message, on ne t'écrira plus.

L'équipe CHARMED PARIS

### B0 bis. Rappel de confirmation (48 h plus tard, une seule fois)

**Objet** : Ton inscription attend un clic
**Pré-header** : Sans confirmation, on ne t'écrira pas.

Bonjour,

Tu as laissé ton adresse chez nous il y a deux jours. Il manque juste ta confirmation.

**[Je confirme]**

Si tu as changé d'avis, ne fais rien. C'est le dernier message.

### B1. Bienvenue et code (immédiat après confirmation)

**Objet** : Bienvenue. Voici tes −10 %
**Pré-header** : Ouvre. Laisse-toi charmer.

Bonjour {{ contact.PRENOM }},

Bienvenue chez CHARMED PARIS.

Ici, on ne vend que des parures : un collier et ses boucles d'oreilles, pensés ensemble. Tu n'as pas à chercher ce qui va avec quoi. C'est déjà fait.

Notre logo raconte l'idée. Le C et le D s'ouvrent comme les deux côtés d'un écrin. Ta commande arrive dans le sien : une boîte à bijoux à tiroir, fermée d'un ruban à notre logo, avec une pochette en velours, une chamoisine et une carte d'entretien.

Ton code, valable 14 jours, sur ta première commande :

**{{ contact.CODE_BIENVENUE }}**, soit −10 %
*Valable jusqu'au {{ params.DATE_FIN_CODE }}, non cumulable avec une autre offre.*

**[Voir les parures]**

À très vite,
L'équipe CHARMED PARIS

### B1-cliente. Variante si le contact a déjà commandé

**Objet** : Merci de nous suivre
**Pré-header** : Nouveautés, conseils et dates à retenir, pas plus.

Bonjour {{ contact.PRENOM }},

Tu nous connais déjà, merci d'avoir aussi rejoint la liste.
On t'écrira pour les nouvelles parures, les conseils d'entretien et les dates limites avant les fêtes. Une à deux fois par mois, pas plus.

Tu peux choisir ce que tu reçois ici : **[Mes préférences]**

L'équipe CHARMED PARIS

### B2. Les 5 univers (J+2)

**Objet** : Cinq univers. Lequel te ressemble ?
**Pré-header** : Du doré sculpté à l'argent 925.

Bonjour {{ contact.PRENOM }},

Toutes nos parures sont rangées en cinq univers. Pour t'y retrouver vite :

**Sculpture.** Des formes fluides, comme du métal qui coule. Laiton doré à l'or fin. Pour tous les jours, avec un jean comme avec une robe.
**[Voir Sculpture]**

**Éclat.** Du doré et des zircons qui accrochent la lumière. Pour les soirs où tu sors, ou pour donner de l'éclat à un pull noir.
**[Voir Éclat]**

**Couleur précieuse.** Des pierres de couleur, vert, rose, bleu, serties comme de la joaillerie. Quand tu veux une touche de couleur près du visage.
**[Voir Couleur précieuse]**

**Joaillerie 925.** Argent 925 et moissanite de laboratoire. La parure à garder longtemps, ou à offrir pour une vraie occasion.
**[Voir Joaillerie 925]**

**Mixte.** Sur cordon, plus brut. À porter à deux, ou seule.
**[Voir Mixte]**

Tu hésites ? Réponds simplement à cet e-mail avec ta tenue préférée ou l'occasion. On te répond, une vraie personne.

Ton code −10 % court jusqu'au {{ params.DATE_FIN_CODE }}.

L'équipe CHARMED PARIS

### B3. Pour toi, ou pour offrir (J+5)

**Objet** : Ce qu'il y a dans l'écrin
**Pré-header** : Pochette, chamoisine, carte, et pas de mauvaise surprise à la livraison.

Bonjour {{ contact.PRENOM }},

Que ta parure soit pour toi ou pour quelqu'un d'autre, voici ce qui arrive chez toi.

**Dans le colis**
- La parure, dans notre boîte à bijoux à tiroir avec ruban à notre logo. La Joaillerie 925 arrive dans un écrin en velours bleu.
- Une pochette en velours pour la ranger.
- Une chamoisine pour l'essuyer.
- Une carte avec les conseils d'entretien.
- Un bordereau sans aucun prix.

*Tu commandes deux parures ? Elles arrivent dans le même colis, mais il n'y a qu'une boîte à bijoux par commande : la deuxième voyage dans un sachet scellé. Pour offrir chacune dans sa boîte, passe deux commandes séparées (deux colis, deux livraisons).*

**La livraison**
- Envoi suivi par DHL. Le lien de suivi arrive par e-mail.
- En France, la parure arrive en général en 4 à 9 jours ouvrés après ta commande.
- Les droits et taxes sont déjà payés : rien à régler au facteur.
- Livraison offerte dès 50 € [seuil à confirmer].

**Si ce n'est pas la bonne**
- Tu as 14 jours après réception pour changer d'avis.
- Garantie légale de conformité de 2 ans.

C'est pour offrir ? Tu peux la faire livrer directement chez la personne. Le colis arrive prêt à offrir, sans aucun prix. On ne peut pas y glisser de message : prévois ton mot à part.

**[Choisir ma parure]**

L'équipe CHARMED PARIS

### B4. Rappel du code (J+11, si le code n'est pas utilisé)

**Objet** : Ton code est valable jusqu'au {{ params.DATE_FIN_CODE }}
**Pré-header** : Un rappel, rien de plus.

Bonjour {{ contact.PRENOM }},

Petit rappel : ton code de bienvenue **{{ contact.CODE_BIENVENUE }}** (−10 %) est valable jusqu'au {{ params.DATE_FIN_CODE }}.

Si tu n'as pas encore trouvé ta parure, voici celles que tu as le plus regardées :
[[ bloc produits : 3 dernières fiches consultées, sinon 3 parures de l'univers choisi au pop-up, sinon une de chaque univers ]]

**[Utiliser mon code]**

Et si ce n'est pas le moment, aucun souci. On continuera à t'écrire, sans insister.

L'équipe CHARMED PARIS

---

## Navigation abandonnée

### N1. La parure regardée (+4 h)

**Objet** : {{ params.NOM_PRODUIT }}, toujours là
**Pré-header** : Tu l'as regardée tout à l'heure.

Bonjour {{ contact.PRENOM }},

Tu regardais celle-ci :

[[ image produit · {{ params.NOM_PRODUIT }} · univers {{ params.UNIVERS }} · {{ params.PRIX }} € ]]

Deux choses à savoir :
- [[ si Sculpture ou Éclat : « Laiton doré à l'or fin, avec une finition anti-ternissement. » ]] [[ si 925 : « Argent 925 et moissanite de laboratoire. » ]] [[ si Couleur précieuse : « Pierres de couleur, finition argentée [à confirmer]. » ]] [[ si Mixte : « Montée sur cordon. » ]]
- Elle arrive avec ses boucles assorties, dans notre boîte à ruban, avec une pochette en velours et une chamoisine.

**[La revoir]**

Une question sur la taille de la chaîne ou des boucles ? Réponds à cet e-mail.

L'équipe CHARMED PARIS

### N2. Le même univers (+2 jours)

**Objet** : D'autres parures dans le même esprit
**Pré-header** : Si celle-là ne t'a pas tout à fait convaincue.

Bonjour {{ contact.PRENOM }},

Tu aimes l'univers {{ params.UNIVERS }}. En voici trois autres, du plus discret au plus visible :

[[ bloc 3 produits du même univers, triés par prix croissant ]]

Pour choisir, demande-toi :
- Plutôt tous les jours, ou pour les grandes occasions ?
- Plutôt doré, ou plutôt argenté ?
- Encolure ouverte ou col roulé ? Les colliers courts vont mieux sur une encolure ouverte.

Livraison suivie, 14 jours pour changer d'avis.

**[Voir l'univers {{ params.UNIVERS }}]**

L'équipe CHARMED PARIS

---

## Post-achat

### P1. Expédition (dès que le numéro DHL est disponible)

**Objet** : Ta parure est en route
**Pré-header** : Ton lien de suivi DHL est dedans.

Bonjour {{ contact.PRENOM }},

Bonne nouvelle : ta commande n° {{ params.ORDER_ID }} est partie.

**[Suivre mon colis]** → {{ params.TRACKING_URL }}
*N° de suivi DHL : {{ params.TRACKING_NUMBER }}*

**Quand arrive-t-elle ?**
[[ selon `PAYS` : « En France, dans 9 cas sur 10, ta parure arrive au plus tard le {{ params.DATE_LIVRAISON_MAX }}. » ]]
Le suivi peut mettre un ou deux jours avant d'afficher ses premières étapes. C'est normal.

**À la livraison**
Les droits et taxes sont déjà réglés. Tu n'as rien à payer au livreur.

**Ce qu'il y a dans le colis**
Ta parure dans notre boîte à bijoux à ruban (écrin en velours bleu pour la Joaillerie 925), une pochette en velours, une chamoisine, une carte d'entretien et un bordereau sans prix.
[[ si 2 parures ou plus : « La deuxième parure est dans un sachet scellé, dans le même colis : il n'y a qu'une boîte à bijoux par commande. » ]]

**Ta commande**
[[ récapitulatif : image, nom, quantité, prix ]]

Une question ? Réponds à cet e-mail.

L'équipe CHARMED PARIS

### P2. « Ton écrin arrive » (le jour où DHL indique « en cours de livraison », sinon J+4 ouvrés)

**Objet** : Ton écrin arrive
**Pré-header** : Deux minutes pour bien l'ouvrir.

Bonjour {{ contact.PRENOM }},

[[ si événement DHL « en cours de livraison » : « Ton colis est en cours de livraison aujourd'hui. » ]]
[[ sinon : « Ton colis peut arriver dès aujourd'hui. Dans 9 cas sur 10, il est chez toi au plus tard le {{ params.DATE_LIVRAISON_MAX }}. » ]]

**[[ Variante pour soi (`ACHAT_CADEAU = non`) ]]**
Quand tu l'ouvres :
1. Garde la pochette en velours : c'est là que ta parure dort.
2. Mets la chamoisine de côté. Elle sert après chaque port.
3. Lis la carte d'entretien. Elle tient en trente secondes.

Le bon réflexe dès le premier jour : parfum et crème d'abord, bijou ensuite.

**[[ Variante cadeau (`ACHAT_CADEAU = oui`) ]]**
C'est pour offrir ? Quelques idées :
- Ne jette pas le carton d'envoi trop vite : vérifie d'abord que tout y est.
- La pochette en velours et la carte d'entretien font partie du cadeau. Laisse-les dans la boîte.
- Il n'y a ni prix ni message dans le colis. Ton mot, c'est toi qui le glisses ou qui l'envoies.
- Tu l'as fait livrer chez la personne ? Préviens-la qu'un colis DHL arrive à son nom. Rien à payer à la livraison.

**[[ Variante inconnue (`ACHAT_CADEAU = inconnu`) ]]**
Petite question pour mieux t'écrire ensuite, un clic suffit :
**[C'est pour moi]**   **[C'est pour offrir]**

**Un souci à l'ouverture ?**
Colis abîmé, pièce qui manque, pas la bonne parure : écris-nous **dans les 10 jours** après la livraison, avec une photo. On règle ça vite.
*Ta garantie légale de conformité de 2 ans reste valable dans tous les cas.*

L'équipe CHARMED PARIS

### P3. Conseils d'entretien (livraison + 2 jours, e-mail de service, sans promotion)

**Objet** : Pour que ta parure garde son éclat
**Pré-header** : Les cinq gestes qui font la différence.

Bonjour {{ contact.PRENOM }},

Ta parure est arrivée. Voici comment la garder belle longtemps.

**Les gestes de base**
1. **Garde-la au sec.** Retire-la avant la douche, le bain, la piscine, la mer et le sport. L'eau, le savon et le chlore usent la dorure.
2. **Parfum, crème et laque d'abord.** Le bijou se met en dernier et s'enlève en premier.
3. **Essuie-la avec la chamoisine** après l'avoir portée, sans frotter fort.
4. **Range chaque pièce dans la pochette en velours ou dans son sachet refermable**, à l'abri de l'humidité. La salle de bain, ce n'est pas l'idéal.
5. **Pas de produit nettoyant**, pas de dentifrice, pas de bain à ultrasons.

**[[ Bloc selon l'univers de la commande ]]**

**Sculpture et Éclat (laiton doré à l'or fin)**
La dorure est une couche fine, protégée par un vernis anti-ternissement. Essuie doucement, sans appuyer. Pour les zircons, une petite brosse souple et **sèche** dégage le serti.

**Couleur précieuse**
Les pierres sont serties une à une : évite les chocs et ne tire pas sur les pierres. Range le collier à plat pour que la chaîne ne s'emmêle pas.

**Joaillerie 925 (argent 925 et moissanite)**
L'argent peut foncer légèrement au contact de l'air : c'est normal. La chamoisine lui rend sa clarté. La moissanite est une pierre dure, mais son serti reste délicat. Garde aussi le certificat s'il y en a un dans ton colis (pour les pierres de 0,1 carat et plus).

**Mixte (sur cordon)**
Le cordon n'aime ni l'eau ni la traction. Ne le mouille pas, et ne le tire pas pour l'enlever : ouvre le fermoir.

**Un souci ?** Si tu remarques un défaut, écris-nous vite, idéalement dans les 10 jours après la livraison, avec une photo. La garantie légale de 2 ans s'applique dans tous les cas.

L'équipe CHARMED PARIS

### P4. Demande d'avis (livraison + 14 jours, texte à coller dans Judge.me)

**Objet** : Elle te plaît ?
**Pré-header** : Ton avis aide les prochaines à choisir.

Bonjour {{ contact.PRENOM }},

Ça fait deux semaines que ta parure {{ params.NOM_PRODUIT }} est arrivée.

Tu la portes souvent ? Elle ressemble aux photos ? La taille te va ?
Ton avis, même court, aide celles qui hésitent. Et il nous aide, nous, à choisir les prochaines parures.

**[Laisser mon avis]**

Une photo portée est la bienvenue, mais pas obligatoire.
Si quelque chose ne va pas, dis-le aussi. Et réponds à cet e-mail : on préfère le savoir et t'aider.

L'équipe CHARMED PARIS

*On ne t'offre rien en échange de ton avis, positif ou non. Tous les avis publiés viennent de clientes ayant commandé.*

### P4b. Rappel d'avis (P4 + 7 jours, une seule fois)

**Objet** : Trente secondes pour ton avis ?
**Pré-header** : Dernier rappel, promis.

Bonjour {{ contact.PRENOM }},

Si tu as un instant, une note et une phrase suffisent.

**[Donner mon avis]**

Merci, et on ne te relancera plus pour cette commande.

---

## Cross-sell 2e parure

### X1. La suivante (J+21)

**Objet** : Et la prochaine, ce serait laquelle ?
**Pré-header** : Trois idées choisies à partir de ta première parure.

Bonjour {{ contact.PRENOM }},

Tu as ta {{ params.NOM_PRODUIT }} depuis quelques semaines. On espère qu'elle sort souvent.

**[[ Variante pour soi ]]**
Si tu as envie d'une deuxième, pour un autre style ou d'autres tenues, voici trois parures qui vont bien avec la tienne :
[[ bloc 3 produits : 1 du même univers + 2 de l'univers voisin, voir `segmentation-et-fidelite.md` §2 ]]

**[[ Variante cadeau ]]**
Ta dernière parure était un cadeau. Et si la prochaine était pour toi ? Ou pour la prochaine occasion (anniversaire, fête, merci) :
[[ bloc 3 produits, prix comparables à la première commande ]]

Ton code, valable 14 jours : **{{ contact.CODE_X }}**, soit −10 % sur ta prochaine parure.
*Valable jusqu'au {{ params.DATE_FIN_CODE }}, non cumulable.*

**[Voir les parures]**

L'équipe CHARMED PARIS

### X2. Rappel du code (X1 + 10 jours, si X1 a été ouvert ou cliqué et que le code n'est pas utilisé)

**Objet** : Ton code expire le {{ params.DATE_FIN_CODE }}
**Pré-header** : Juste pour que tu le saches.

Bonjour {{ contact.PRENOM }},

Ton code **{{ contact.CODE_X }}** (−10 %) est valable jusqu'au {{ params.DATE_FIN_CODE }}.
Après, il ne fonctionnera plus. Mais nos parures, elles, ne vont nulle part.

**[Revoir ma sélection]**

---

## Anniversaire

### A1. Bon anniversaire (J−3)

**Objet** : Joyeux anniversaire, {{ contact.PRENOM }}
**Pré-header** : Un petit cadeau de notre part, valable 30 jours.

Bonjour {{ contact.PRENOM }},

Ton anniversaire approche. On voulait être là un peu en avance.

Ton cadeau : **{{ contact.CODE_ANNIV }}**
[[ si `CERCLE = oui` : −15 %, sinon : −10 % ]] sur la parure de ton choix, jusqu'au {{ params.DATE_FIN_CODE }}.

Quelques idées dans ton univers préféré :
[[ bloc 3 produits `UNIVERS_PREFERE` ]]

**[Choisir ma parure]**

Belle journée à toi,
L'équipe CHARMED PARIS

### A2. Rappel (A1 + 20 jours, si le code n'est pas utilisé)

**Objet** : Ton cadeau d'anniversaire t'attend encore
**Pré-header** : Valable jusqu'au {{ params.DATE_FIN_CODE }}.

Bonjour {{ contact.PRENOM }},

Ton code d'anniversaire **{{ contact.CODE_ANNIV }}** est valable jusqu'au {{ params.DATE_FIN_CODE }}.
Pas d'obligation, bien sûr. Si tu en as envie, il est là.

**[Voir les parures]**

---

## Réactivation (90 jours)

### R1. Ce qui est nouveau (J90)

**Objet** : Du nouveau depuis ta dernière visite
**Pré-header** : Quelques parures que tu n'as pas encore vues.

Bonjour {{ contact.PRENOM }},

Ça fait un moment. On voulait te montrer ce qui a changé chez nous.

[[ bloc : nouvelles parures de `UNIVERS_PREFERE`. S'il n'y en a pas : les 3 parures de cet univers les plus consultées. Jamais « les plus vendues » sans chiffres réels. ]]

**[Voir les nouveautés]**

L'équipe CHARMED PARIS

### R2. Livraison offerte (J97, si R1 n'a pas été cliqué)

**Objet** : La livraison est pour nous
**Pré-header** : Sans minimum d'achat, pendant 14 jours.

Bonjour {{ contact.PRENOM }},

Si une parure te fait de l'œil, la livraison est offerte sur ta prochaine commande, quel que soit son montant.

Ton code : **{{ params.CODE_RV }}**, valable jusqu'au {{ params.DATE_FIN_CODE }}.

**[Choisir ma parure]**

L'équipe CHARMED PARIS

### R3. On reste en contact ? (J111, si R1 et R2 n'ont pas été cliqués)

**Objet** : On continue de t'écrire ?
**Pré-header** : Tu choisis. Un clic suffit.

Bonjour {{ contact.PRENOM }},

On n'a pas eu de nouvelles depuis un moment, et c'est OK.
On préfère t'écrire moins, mais mieux. Dis-nous ce que tu veux :

**[Continuer comme avant]**
**[Seulement avant les fêtes]** (Noël, Saint-Valentin, fête des mères)
**[Changer d'univers ou de langue]**
**[Ne plus recevoir d'e-mails]**

Sans réponse de ta part, on t'écrira beaucoup moins souvent.

Merci d'avoir été là,
L'équipe CHARMED PARIS

---

## Noël 2026

Dates : Europe et Canada, **vendredi 4 décembre**. Royaume-Uni, États-Unis et Australie : 8 décembre (voir la version EN). Reste du monde : 30 novembre. `{{ params.DATE_LIMITE }}` est renseigné selon le `PAYS`.

### NO1. Idées et date limite (mardi 24 novembre)

**Objet** : Noël : commande avant le {{ params.DATE_LIMITE }}
**Pré-header** : Et l'emballage de fête est offert.

Bonjour {{ contact.PRENOM }},

On préfère te le dire tôt : pour que ta parure arrive avant Noël, commande au plus tard le **{{ params.DATE_LIMITE }}**. Après, on ne peut plus garantir la date.

**Jusqu'au 24 décembre, chaque commande part dans son emballage de fête** : papier cadeau, ruban, décorations et une carte de Noël. C'est offert, tu n'as rien à cocher.

**Des idées, selon la personne**
- Elle porte du doré tous les jours → **Sculpture** [[ 2 produits ]]
- Elle aime briller le soir → **Éclat** [[ 2 produits ]]
- Elle ose la couleur → **Couleur précieuse** [[ 2 produits ]]
- Un cadeau qui compte → **Joaillerie 925** [[ 2 produits ]]

**Par budget** : moins de 60 € · de 60 à 90 € · plus de 150 € [à aligner sur les prix réels]

Tu peux la faire livrer directement chez la personne. Droits et taxes déjà payés, rien à régler à la livraison.

**[Trouver son cadeau]**

L'équipe CHARMED PARIS

### NO2. Il reste une semaine (lundi 30 novembre)

**Objet** : Livraison avant Noël : jusqu'à vendredi
**Pré-header** : Commande au plus tard le {{ params.DATE_LIMITE }}.

Bonjour {{ contact.PRENOM }},

Un rappel pratique : pour une livraison avant Noël, il faut commander au plus tard **{{ params.DATE_LIMITE }}**.

Tu ne sais pas laquelle choisir ? Réponds à cet e-mail avec trois mots sur la personne (son style, ses couleurs, l'occasion). On te propose deux ou trois parures.

[[ bloc 4 produits, un par univers ]]

**[Voir les idées cadeaux]**

L'équipe CHARMED PARIS

### NO3. Dernier jour conseillé : demain (jeudi 3 décembre)

**Objet** : Demain, dernier jour pour Noël
**Pré-header** : Commande avant vendredi soir pour une livraison avant le 24.

Bonjour {{ contact.PRENOM }},

C'est demain, **{{ params.DATE_LIMITE }}**, le dernier jour pour commander avec une livraison prévue avant Noël.

L'emballage de fête est toujours offert.

**[Choisir maintenant]**

Et si tu as déjà tout, merci. Ignore ce message.

### NO-SMS (vendredi 4 décembre, 10 h, opt-in SMS uniquement)

> CHARMED PARIS : aujourd'hui, dernier jour pour une livraison avant Noël. Emballage de fête offert. charmedparis.fr/noel STOP au [numéro STOP]

*(SMS de moins de 160 caractères, sans accent problématique. Mention STOP obligatoire.)*

### NO4. Après la date limite (lundi 7 décembre)

**Objet** : Trop tard pour le 24 ? Pas pour l'offrir
**Pré-header** : Une carte à glisser sous le sapin en attendant.

Bonjour {{ contact.PRENOM }},

La date limite pour une livraison avant Noël est passée. On ne va pas te promettre l'impossible.

Mais tu peux encore offrir une parure :
1. Commande maintenant. Elle arrive en général dans les 4 à 9 jours ouvrés, sans date garantie.
2. Imprime notre carte « **Ton écrin arrive** » et glisse-la sous le sapin le 24.
3. L'écrin suit quelques jours plus tard, avec son emballage de fête si la commande part avant le 24 décembre.

**[Télécharger la carte à imprimer]**   **[Choisir la parure]**

Joyeuses fêtes,
L'équipe CHARMED PARIS

---

## Saint-Valentin 2027

### SV1. Offrir, ou se faire offrir (mardi 19 janvier)

**Objet** : Saint-Valentin : à offrir, ou à te faire offrir
**Pré-header** : Commande avant le {{ params.DATE_LIMITE }} pour le 14 février.

Bonjour {{ contact.PRENOM }},

Le 14 février tombe un dimanche. Pour une livraison à temps, commande au plus tard le **{{ params.DATE_LIMITE }}** (en France : lundi 1er février).

**Pour offrir** : le colis arrive prêt à offrir, avec la boîte à ruban, la pochette en velours, la carte d'entretien et aucun prix. Pas de message possible dans le colis : écris ton mot à part.

**Pour te la faire offrir** : choisis ta parure, puis transfère cet e-mail à la bonne personne. Ou envoie-lui directement le lien de la fiche. On ne dira rien.

[[ bloc 4 produits : Éclat, Couleur précieuse (rose), Joaillerie 925 (cœur) ]]

**[Voir la sélection Saint-Valentin]**

L'équipe CHARMED PARIS

### SV2. Rappel de la date limite (jeudi 28 janvier)

**Objet** : Pour le 14 février : commande avant lundi
**Pré-header** : Après, on ne peut plus garantir la date.

Bonjour {{ contact.PRENOM }},

Un simple rappel : pour une livraison avant la Saint-Valentin, il faut commander au plus tard **{{ params.DATE_LIMITE }}**.

**[Choisir ma parure]**

### SV-SMS (samedi 30 janvier, 11 h)

> CHARMED PARIS : pour une parure livree avant le 14/02, commande jusqu'a lundi 1er fevrier. charmedparis.fr/st-valentin STOP au [numéro STOP]

---

## Fête des mères 2027

France : dimanche 30 mai, date limite **vendredi 14 mai**. Belgique et Suisse : dimanche 9 mai, date limite **lundi 19 avril** (à confirmer). `{{ params.DATE_FETE }}` et `{{ params.DATE_LIMITE }}` sont renseignés selon le `PAYS`.

### FM1. Idées (environ 12 jours avant la date limite)

**Objet** : Fête des mères : une parure, déjà assortie
**Pré-header** : Pour le {{ params.DATE_FETE }}, commande avant le {{ params.DATE_LIMITE }}.

Bonjour {{ contact.PRENOM }},

Cette année, la fête des mères tombe le **{{ params.DATE_FETE }}**. Pour une livraison à temps, commande au plus tard le **{{ params.DATE_LIMITE }}**.

Une parure, c'est pratique à offrir : le collier et les boucles vont ensemble. Tu n'as pas à deviner ce qu'elle portera avec.

**Selon ta maman**
- Classique et discrète → **Sculpture** [[ 2 produits ]]
- Elle aime la couleur → **Couleur précieuse** [[ 2 produits ]]
- Pour marquer le coup → **Joaillerie 925** [[ 2 produits ]]

Livraison possible chez elle. Rien à payer à la réception.

**[Trouver sa parure]**

L'équipe CHARMED PARIS

### FM2. Veille de la date limite

**Objet** : Fête des mères : dernier jour demain
**Pré-header** : Commande avant le {{ params.DATE_LIMITE }} pour le {{ params.DATE_FETE }}.

Bonjour {{ contact.PRENOM }},

C'est demain, **{{ params.DATE_LIMITE }}**, le dernier jour pour commander avec une livraison prévue avant la fête des mères.

**[Choisir sa parure]**

### FM-SMS (jour de la date limite, 10 h, France)

> CHARMED PARIS : fete des meres le 30/05. Dernier jour aujourd'hui pour une livraison a temps. charmedparis.fr/fete-des-meres STOP au [numéro STOP]

---

## Retour en stock

### RS1. Elle est de retour (au retour en stock, un seul envoi)

**Objet** : {{ params.NOM_PRODUIT }} est de nouveau disponible
**Pré-header** : Tu nous avais demandé de te prévenir.

Bonjour {{ contact.PRENOM }},

Tu nous avais demandé de te prévenir : la parure **{{ params.NOM_PRODUIT }}** est de nouveau disponible.

[[ image produit · prix ]]

**[La voir]**

C'était notre seul message à ce sujet. On ne t'écrira plus pour cette parure.

L'équipe CHARMED PARIS

### RS-SMS (opt-in SMS et demande faite par SMS)

> CHARMED PARIS : {{ params.NOM_COURT }} est de nouveau disponible. {{ params.URL_COURTE }} STOP au [numéro STOP]

---

## Le Cercle et parrainage

### C1. Bienvenue dans Le Cercle

**Objet** : Tu fais partie du Cercle
**Pré-header** : Livraison offerte, avant-premières et un cadeau tous les 3 achats.

Bonjour {{ contact.PRENOM }},

Deux parures chez nous [[ ou « une parure Joaillerie 925 » ]] : merci. Tu entres dans **Le Cercle**. Il n'y a rien à faire, tout est déjà actif sur ton adresse e-mail.

**Ce que ça change pour toi**
- **Livraison offerte**, sans minimum, sur toutes tes commandes.
- **Les nouvelles parures 48 h avant tout le monde**, par e-mail.
- **15 € offerts tous les 3 achats**, dès 79 € de commande.
- **Anniversaire** : −15 % au lieu de −10 %, si tu nous donnes ta date. **[Ajouter ma date]**

Connecte-toi avec cette adresse au moment de commander : la livraison offerte s'applique toute seule.

L'équipe CHARMED PARIS

### C2. Tes 15 € (tous les 3 achats)

**Objet** : Tes 15 € sont prêts
**Pré-header** : Valables 60 jours, dès 79 € d'achat.

Bonjour {{ contact.PRENOM }},

Trois parures depuis ton entrée dans Le Cercle : voici **15 €** pour la prochaine.

Ton code : **{{ params.CODE_CERCLE }}**, dès 79 € d'achat, jusqu'au {{ params.DATE_FIN_CODE }}.

**[Choisir ma parure]**

Merci pour ta fidélité,
L'équipe CHARMED PARIS

### PA1. Invitation au parrainage (livraison + 30 jours)

**Objet** : Offre 10 €, reçois 10 €
**Pré-header** : Pour une amie qui aimerait nos parures.

Bonjour {{ contact.PRENOM }},

Si ta parure te plaît, tu connais sûrement quelqu'un à qui elle plairait aussi.

**Comment ça marche**
1. Tu partages ton lien personnel.
2. Ton amie a **10 € de réduction** sur sa première commande, dès 59 €.
3. Quand sa commande est conservée (14 jours après réception), tu reçois **10 €** pour ta prochaine parure, dès 59 €.

Ton lien : **{{ params.LIEN_PARRAINAGE }}**

**[Partager mon lien]**

*Jusqu'à 5 parrainages récompensés par an. Le programme est réservé aux nouvelles clientes. Conditions complètes : [lien].*

L'équipe CHARMED PARIS

### PA2. Récompense de la marraine

**Objet** : Merci, tes 10 € sont là
**Pré-header** : Ton amie a gardé sa parure.

Bonjour {{ contact.PRENOM }},

Ton amie a commandé grâce à toi, et elle a gardé sa parure. Merci !

Tes 10 € : **{{ params.CODE_PARRAIN }}**, dès 59 € d'achat, jusqu'au {{ params.DATE_FIN_CODE }}.

**[Choisir ma parure]**

L'équipe CHARMED PARIS
