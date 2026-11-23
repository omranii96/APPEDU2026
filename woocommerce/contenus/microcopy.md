# CHARMED PARIS · Microcopy (FR)

Tutoiement partout. Phrases courtes. Variables entre accolades : `{prenom}`, `{numero_commande}`, `{montant}`, `{lien_suivi}`… (à mapper sur les variables WooCommerce ou de l'outil d'e-mails : `{order_number}`, `{site_title}`, etc.). Les notes « À confirmer » sont internes.

---

## 1. Boutons

| Contexte | Texte |
|---|---|
| Ajouter au panier (fiche, carte produit) | Ajouter à l'écrin |
| Ajouter au panier (après ajout, 2 s) | Ajoutée à l'écrin |
| Voir le panier | Voir mon écrin |
| Commander (panier) | Commander |
| Valider le paiement | Payer {montant} |
| Continuer les achats | Continuer à regarder |
| Rupture de stock | Bientôt de retour |
| M'avertir du retour | Préviens-moi |
| Voir toutes les parures | Voir les parures |
| Choisir un coffret (accueil) | Choisir mon coffret |
| Newsletter | Je m'inscris |
| Suivre ma commande | Suivre mon colis |
| Appliquer un code | Appliquer |
| Retirer un article | Retirer |
| Charger plus | Voir plus de parures |
| Filtrer | Filtrer · Effacer les filtres |
| Trier | Trier : prix croissant · prix décroissant · nouveautés |

## 2. Fiche produit

- Sous le prix : **Coffret inclus · Livraison offerte dès 50 € · Droits de douane payés**
- Délai : Livrée en France en 4 à 9 jours ouvrés (9 colis sur 10).
- Noël (jusqu'au 4/12) : Pour Noël en Europe, commande avant le vendredi 4 décembre.
- Noël (5/12 au 24/12) : Emballage de Noël offert jusqu'au 24 décembre. Livraison avant Noël non garantie.
- Bague réglable : Bague réglable : l'anneau s'ajuste légèrement à ton doigt.
- Bague en tailles : Choisis ta taille · Guide des tailles
- Mini-réassurance (accordéon) : Matières · Entretien · Livraison et retours
- Rétractation : 14 jours pour changer d'avis, retour à nos frais.
- Stock épuisé : Cette parure est épuisée pour le moment. Laisse ton e-mail, on te prévient dès qu'elle revient.

## 3. Panier (« Ton écrin »)

**Titre :** Ton écrin
**Panier vide :** Ton écrin est vide. · Bouton : Voir les parures

**Livraison offerte dès 50 € (barre de progression)**
- 0 à 49,99 € : Plus que {reste} pour la livraison offerte.
- ≥ 50 € : La livraison est offerte.
- Panier à 49 € : Une 2e parure et la livraison est offerte, avec −15 % sur la deuxième.

**2e parure −15 %**
- 1 parure dans le panier : Ajoute une 2e parure : −15 % sur la moins chère des deux.
- 2 parures ou plus : −15 % sur ta 2e parure, déjà appliqué.
- Ligne de remise : 2e parure −15 %
- Info colis (à partir de 2 parures) : Tes parures arrivent dans un seul colis : une dans la boîte-tiroir, les autres dans leur sachet scellé. Pour deux cadeaux à deux adresses, passe deux commandes.

**Lignes**
- Sous-total · 2e parure −15 % · Livraison · Total TTC
- Livraison sous 50 € : {frais_livraison} (À confirmer : proposition 4,90 €)
- Mention : Prix TTC, TVA incluse. Droits de douane déjà payés.

**Option cadeau (case à cocher)**
- Libellé : C'est un cadeau
- Aide : Colis prêt à offrir, bordereau sans prix. Mets l'adresse de la personne en livraison, la tienne en facturation.

> À confirmer : la règle « −15 % sur la moins chère » (la maquette applique −15 % sur la parure la moins chère) ; plugin de remise ; frais sous 50 €. L'option « Emballage cadeau et carte Ouvre-moi (offert) » de la maquette est à supprimer : aucune carte personnalisée hors offre VIP.

## 4. Checkout

- Titre : Commande
- Étapes : Coordonnées · Livraison · Paiement
- E-mail : Ton e-mail · Aide : Pour ta confirmation et ton suivi.
- Téléphone (obligatoire) : Téléphone · Aide : Le transporteur peut en avoir besoin pour te livrer.
- Adresse : Adresse · Complément (bâtiment, étage, code) · Aide : Vérifie le numéro de rue : une adresse incomplète bloque l'envoi.
- Livraison à une autre adresse : Livrer à une autre adresse (pour un cadeau, par exemple)
- Mode de livraison (un seul) : **Livraison suivie DHL · 4 à 9 jours ouvrés · {frais ou Offerte}** · sous-ligne : Droits de douane déjà payés. Pas d'option express.
- Noël (jusqu'au 4/12) : Commandée aujourd'hui, ta parure devrait arriver avant Noël en Europe.
- Noël (5/12 au 24/12) : Livraison avant Noël non garantie à partir d'aujourd'hui.
- Code promo : Un code ? · Appliquer
- Paiement : Paiement sécurisé. [À CONFIRMER : Carte, Apple Pay, PayPal selon la passerelle]
- Case CGV : J'ai lu et j'accepte les conditions générales de vente.
- Newsletter (non cochée par défaut) : Je veux recevoir les nouvelles parures et les dates importantes par e-mail.
- Bouton final : Payer {montant}
- Sous le bouton : En payant, tu confirmes ta commande. Tu as 14 jours après réception pour changer d'avis.
- Page de remerciement : Merci {prenom}. Ta commande n° {numero_commande} est confirmée. Tu reçois un e-mail dans quelques minutes, puis un autre avec ton suivi dès l'expédition.

## 5. E-mails transactionnels WooCommerce

### 5.1 Confirmation de commande (« Commande en cours »)
- **Objet :** Ta commande CHARMED PARIS n° {numero_commande} est confirmée
- **Pré-en-tête :** On prépare ton écrin.
- **Corps :**
  Bonjour {prenom},

  Merci pour ta commande. Elle est confirmée et part en préparation.

  Ce qui se passe maintenant :
  - Ta commande est préparée en 1 à 2 jours ouvrés.
  - Tu reçois un e-mail avec ton numéro de suivi DHL dès qu'elle part.
  - En France, compte 4 à 9 jours ouvrés entre ta commande et la livraison.

  Les droits de douane sont déjà payés : tu n'auras rien à régler à la livraison.

  {recapitulatif_commande}

  Une erreur dans l'adresse ? Réponds à cet e-mail tout de suite : on peut la corriger tant que la commande n'est pas partie en préparation.

  À très vite,
  CHARMED PARIS

### 5.2 Expédition (« Commande expédiée », suivi)
- **Objet :** Ta parure est en route
- **Pré-en-tête :** Ton numéro de suivi DHL est dedans.
- **Corps :**
  Bonjour {prenom},

  Ta commande n° {numero_commande} vient de partir.

  Suivi DHL : {numero_suivi}
  [Suivre mon colis]({lien_suivi})

  Le suivi peut mettre 24 à 48 heures à s'afficher. Livraison estimée : entre le {date_min} et le {date_max}.

  Ton numéro de téléphone peut être utilisé par le transporteur pour te livrer.

  CHARMED PARIS

> À confirmer : Branvas écrit le suivi dans la commande Woo ; l'envoi de cet e-mail nécessite un plugin (ex. statut « Expédiée » + e-mail) ou l'e-mail « Note client ». Calcul des dates min/max.

### 5.3 Livraison
- **Objet :** Ton écrin est arrivé
- **Pré-en-tête :** Quelques conseils pour qu'il dure.
- **Corps :**
  Bonjour {prenom},

  D'après le suivi, ta commande n° {numero_commande} a été livrée.

  Avant de la porter :
  - Garde-la au sec : retire-la avant la douche et la baignade.
  - Parfum et crème d'abord, bijoux ensuite.
  - Range-la dans sa pochette en velours.

  Quelque chose ne va pas ? Une pièce abîmée, une erreur de modèle : réponds à cet e-mail avec une photo, le plus tôt possible. On s'en occupe.

  Tu as 14 jours pour changer d'avis. Les frais de retour sont pour nous.

  CHARMED PARIS

> À confirmer : WooCommerce n'a pas de statut « Livrée » natif : plugin de suivi nécessaire. Ensuite, demande d'avis via l'outil d'avis (Judge.me…) à J+7, jamais d'avis inventé.

### 5.4 Commande annulée / remboursée (court)
- Annulation : **Objet :** Ta commande n° {numero_commande} est annulée · Corps : C'est fait, ta commande est annulée. Si tu as payé, le remboursement part aujourd'hui sur ton moyen de paiement. Il apparaît en général sous 3 à 10 jours selon ta banque.
- Remboursement : **Objet :** Ton remboursement est parti · Corps : On t'a remboursé {montant} sur ton moyen de paiement. Selon ta banque, il apparaît sous 3 à 10 jours.

## 6. Relance panier abandonné (3 e-mails)

Règles : pas de fausse urgence, pas de « dernières pièces », pas de compte à rebours. La remise n'arrive qu'au 3e e-mail (facultatif).

### E-mail 1 · 1 heure après
- **Objet :** Ton écrin t'attend
- **Pré-en-tête :** On l'a gardé tel quel.
- **Corps :**
  Bonjour {prenom},

  Tu as laissé {nom_parure} dans ton écrin. On l'a gardée telle quelle.

  {visuel_produit}

  [Reprendre ma commande]({lien_panier})

  Une question sur la matière, la taille ou la livraison ? Réponds simplement à cet e-mail.

### E-mail 2 · 24 heures après
- **Objet :** Ce qu'il y a dans le coffret
- **Pré-en-tête :** Et ce qu'il n'y a pas : aucun prix.
- **Corps :**
  Bonjour {prenom},

  Si tu hésites encore, voici ce que tu recevrais avec {nom_parure} :
  - toutes les pièces de la parure, dans une boîte-tiroir CHARMED PARIS nouée d'un ruban,
  - une pochette en velours et une chamoisine,
  - une carte avec les conseils d'entretien,
  - et aucun prix dans le colis, si c'est un cadeau.

  Livraison en 4 à 9 jours ouvrés en France, droits de douane déjà payés. 14 jours pour changer d'avis.

  [Retrouver mon écrin]({lien_panier})

### E-mail 3 · 72 heures après (facultatif)
- **Objet :** −10 % pour finir ta commande
- **Pré-en-tête :** Valable 7 jours.
- **Corps :**
  Bonjour {prenom},

  Dernier e-mail sur ce sujet, promis.

  Si {nom_parure} te plaît toujours, voici −10 % avec le code {code}, valable 7 jours.

  [Utiliser mon code]({lien_panier})

  Sinon, pas de souci. On ne t'écrira plus à propos de ce panier.

> Noël : remplacer l'e-mail 2 par « Pour Noël en Europe, commande avant le vendredi 4 décembre » jusqu'au 4/12. Ne pas cumuler −10 % et −15 % (à décider).

## 7. Bienvenue newsletter (−10 %)
- **Objet :** Bienvenue dans le cercle, voici tes −10 %
- **Pré-en-tête :** Ton code est dedans.
- **Corps :**
  Bonjour,

  Merci de nous rejoindre. Voici ton code pour ta première commande :

  **{code}** · −10 % · valable [À COMPLÉTER : durée] sur toutes les parures

  Trois choses à savoir sur CHARMED PARIS :
  1. On ne vend que des parures : des pièces assorties, dans un même coffret.
  2. On te dit la vraie matière : laiton doré à l'or fin, argent 925, zircons, moissanites de laboratoire, perles de culture d'eau douce.
  3. La livraison est offerte dès 50 €, et les droits de douane sont déjà payés.

  [Voir les parures]({lien_boutique})

  Tu recevras un e-mail quand une parure arrive ou qu'une date compte. Pas plus.

  CHARMED PARIS · Ouvre. Laisse-toi charmer.

  Lien de désinscription : Ne plus recevoir nos e-mails

## 8. Cadeau : colis prêt à offrir (pas de message cadeau)

Ce qui est possible aujourd'hui : **aucun message imprimé dans le colis** (pas de champ chez le fournisseur ; carte personnalisée réservée à l'offre VIP). Le bordereau n'affiche aucun prix.

Texte de l'option au panier / checkout :
- Case : C'est un cadeau
- Aide : Aucun prix dans le colis. La parure arrive dans sa boîte-tiroir nouée d'un ruban.
- Info : On ne peut pas glisser de mot dans le colis. Tu peux envoyer ton message toi-même le jour de la livraison : ton e-mail d'expédition te donne la date estimée.

Ne proposer aucun champ « message cadeau » au panier ni au checkout. Si une cliente écrit un message dans les notes de commande, réponse type : « Merci pour ton mot. On ne peut pas le glisser dans le colis, mais ta parure part prête à offrir, sans aucun prix. »

## 9. Messages d'erreur

| Situation | Message |
|---|---|
| E-mail invalide | Cette adresse ne semble pas complète. Vérifie l'arobase et le point. |
| Champ obligatoire vide | Il nous manque cette information pour t'envoyer ta parure. |
| Téléphone manquant | Ajoute ton numéro : le transporteur peut en avoir besoin pour te livrer. |
| Adresse incomplète | Il manque le numéro de rue ou le complément. Une adresse incomplète bloque l'envoi. |
| Code postal / pays incohérents | Le code postal ne correspond pas au pays choisi. |
| Code promo invalide | Ce code ne fonctionne pas. Vérifie l'orthographe ou sa date de validité. |
| Code non cumulable | Ce code ne se cumule pas avec la remise 2e parure. On a gardé la plus avantageuse pour toi. |
| Paiement refusé | Le paiement n'est pas passé. Ta banque peut demander une validation : réessaie, ou choisis un autre moyen. |
| Produit épuisé pendant la commande | Cette parure vient d'être épuisée. On l'a retirée de ton écrin. |
| Session expirée | Ta session a expiré. Ton écrin est toujours là, recharge la page. |
| Erreur serveur | Quelque chose a coincé de notre côté. Réessaie dans un instant, ou écris-nous à [À COMPLÉTER : e-mail]. |
| Page 404 | Cette page n'existe pas, ou plus. · Bouton : Voir les parures |
| Pays non desservi | Nous ne livrons pas encore ce pays. |
| Newsletter déjà inscrite | Tu es déjà dans le cercle. Si tu n'as pas reçu ton code, regarde dans tes courriers indésirables. |
