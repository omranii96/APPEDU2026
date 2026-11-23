# Politique cookies

> **Note interne, à retirer avant publication.** Fondements : article 82 de la loi Informatique et Libertés (transposition de l'article 5.3 de la directive 2002/58/CE, dite « ePrivacy »), lignes directrices CNIL (délibération n° 2020-091) et recommandation CNIL « cookies et autres traceurs » (délibération n° 2020-092), consolidée en janvier 2026 avec la recommandation sur le consentement multi-terminaux. La CNIL sanctionne régulièrement l'absence de bouton de refus et le dépôt de cookies avant consentement.
>
> **Configuration du bandeau (CMP), par exemple Complianz, CookieYes ou Axeptio :**
> 1. Premier écran : **« Tout accepter »**, **« Tout refuser »** et **« Personnaliser »**, au même niveau et dans le même format. Refuser doit être aussi simple qu'accepter. Une croix « Continuer sans accepter » vaut refus si elle est clairement libellée.
> 2. **Aucun traceur soumis à consentement ne doit être déposé ni lu avant le choix.** Pixels Meta et TikTok, GA4 et Google Ads ne se déclenchent qu'après acceptation. Avec Google Consent Mode v2, préférer le mode « basique » (aucune balise avant consentement). Le mode « avancé » envoie des signaux sans cookie avant le choix : [À VÉRIFIER] sa compatibilité avec la position de la CNIL avant de l'activer.
> 3. Finalités présentées séparément (mesure d'audience, publicité, réseaux sociaux), cases décochées par défaut.
> 4. Choix conservé **6 mois**, qu'il s'agisse d'une acceptation ou d'un refus. Pas de nouvelle demande avant ce délai, en cas de refus.
> 5. Lien ou bouton **« Gérer mes cookies »** permanent en pied de page, pour retirer son consentement aussi facilement qu'on l'a donné.
> 6. Preuve du consentement conservée (journal de la CMP).
> 7. Bloquer les vidéos YouTube ou Instagram intégrées jusqu'au consentement, ou utiliser youtube-nocookie avec un clic préalable.
>
> La liste ci-dessous recense les cookies **probables**. **[À VÉRIFIER]** : lancer un scan avec la CMP après installation de tous les outils, et ajuster les noms et les durées. Les durées dépendent souvent du paramétrage de l'outil : les limiter à 13 mois.

**Dernière mise à jour : [À COMPLÉTER : date]**

## Qu'est-ce qu'un cookie ?

Un cookie, ou traceur, est un petit fichier ou identifiant enregistré sur ton appareil quand tu visites un site. Certains sont indispensables au fonctionnement de la boutique, comme le panier ou le paiement. D'autres servent à mesurer l'audience ou à te montrer de la publicité : ceux-là ne sont déposés **que si tu les acceptes**.

## Ton choix

À ta première visite, un bandeau te permet de **tout accepter**, de **tout refuser** ou de **choisir par finalité**. Refuser est aussi simple qu'accepter, et n'empêche pas de commander. Nous gardons ton choix pendant **6 mois**. Tu peux le modifier à tout moment avec le lien **« Gérer mes cookies »** en bas de chaque page.

Tu peux aussi configurer ton navigateur pour bloquer les cookies. Le panier et le paiement risquent alors de ne plus fonctionner.

## Liste des cookies

### 1. Cookies nécessaires (exemptés de consentement)

| Cookie | Fournisseur | Finalité | Durée |
|---|---|---|---|
| `woocommerce_cart_hash` | CHARMED PARIS (WooCommerce) | Détecter les changements du panier | Session |
| `woocommerce_items_in_cart` | CHARMED PARIS (WooCommerce) | Savoir si le panier contient des articles | Session |
| `wp_woocommerce_session_*` | CHARMED PARIS (WooCommerce) | Garder ton panier d'une page à l'autre | 2 jours |
| `woocommerce_recently_viewed` | CHARMED PARIS (WooCommerce) | Afficher les produits récemment consultés (widget) | Session |
| `store_notice*` | CHARMED PARIS (WooCommerce) | Mémoriser la fermeture du bandeau d'information | Session |
| `wordpress_logged_in_*`, `wordpress_sec_*`, `wordpress_test_cookie` | CHARMED PARIS (WordPress) | Connexion au compte client et sécurité | Session, ou 14 jours avec « Se souvenir de moi » |
| `wp-settings-*`, `wp-settings-time-*` | CHARMED PARIS (WordPress) | Préférences d'interface d'une personne connectée | 1 an |
| `__stripe_mid`, `__stripe_sid` | Stripe [À COMPLÉTER : ou votre prestataire] | Sécurité du paiement et prévention de la fraude | 1 an / 30 minutes |
| Cookies PayPal (`ts`, `tsrce`, `x-pp-s`…) | PayPal (si utilisé) | Paiement, sécurité | Session à 3 ans, sur le domaine PayPal [À VÉRIFIER] |
| `[À COMPLÉTER : ex. cmplz_*, cookieyes-consent, axeptio_*]` | CMP | Mémoriser ton choix sur les cookies | 6 mois |

### 2. Attribution des commandes (soumis à consentement)

| Cookie | Fournisseur | Finalité | Durée |
|---|---|---|---|
| `sbjs_migrations`, `sbjs_current_add`, `sbjs_first_add`, `sbjs_current`, `sbjs_first`, `sbjs_udata`, `sbjs_session` | CHARMED PARIS (fonction « Order Attribution » de WooCommerce) | Savoir de quel canal vient une commande (Instagram, Google, newsletter…) | Session à [À VÉRIFIER : environ 6 mois] ; `sbjs_session` : 30 minutes |

> Note interne : soumettre ces cookies au consentement via la WP Consent API, ou désactiver la fonction (*WooCommerce > Réglages > Avancé > Fonctionnalités*).

### 3. Mesure d'audience (soumis à consentement)

| Cookie | Fournisseur | Finalité | Durée |
|---|---|---|---|
| `_ga` | Google Analytics 4 (Google Ireland Ltd, transferts vers les États-Unis encadrés par le DPF) | Distinguer les visiteurs, statistiques de visite | **13 mois** (à configurer : 2 ans par défaut) |
| `_ga_<ID>` | Google Analytics 4 | Maintenir l'état de la session | 13 mois |

> Note interne : pour une mesure d'audience exemptée de consentement, il faut un outil configuré selon les conditions CNIL, par exemple Matomo en mode exempté. GA4 n'en fait pas partie.

### 4. Publicité et réseaux sociaux (soumis à consentement)

| Cookie | Fournisseur | Finalité | Durée |
|---|---|---|---|
| `_fbp` | Meta Platforms Ireland (Pixel Meta) | Mesurer les publicités Facebook et Instagram, créer des audiences | 90 jours |
| `_fbc` | Meta (Pixel Meta) | Mémoriser le clic sur une publicité Meta | 90 jours |
| `fr` | Meta (domaine facebook.com) | Diffusion et mesure de publicités | 90 jours |
| `_ttp` | TikTok (Pixel TikTok, TikTok Technology Ltd, Irlande) | Mesurer les publicités TikTok, créer des audiences | 13 mois |
| `_tt_enable_cookie` | TikTok | Vérifier que les cookies sont acceptés | 13 mois |
| `ttcsid`, `ttcsid_*` | TikTok | Identifier la session pour l'attribution | [À VÉRIFIER : quelques heures à 13 mois] |
| `_gcl_au` | Google Ads | Mesure des conversions publicitaires | 90 jours |
| `IDE`, `test_cookie` | Google (DoubleClick, domaine doubleclick.net) | Publicité et remarketing | 13 mois / 15 minutes |

### 5. E-mail marketing (soumis à consentement)

| Cookie | Fournisseur | Finalité | Durée |
|---|---|---|---|
| `sib_cuid` | Brevo (Sendinblue SAS, France), si utilisé | Associer ta navigation à ton inscription, pour des e-mails pertinents | [À VÉRIFIER : 6 mois] |
| `__kla_id` | Klaviyo (Klaviyo Inc., États-Unis), si utilisé | Associer ta navigation à ton profil e-mail (relances, recommandations) | **13 mois** (à configurer : 2 ans par défaut) |

> Note interne : ne garder que l'outil réellement utilisé (Brevo **ou** Klaviyo) et supprimer l'autre ligne. Le formulaire d'inscription à la newsletter, lui, ne nécessite pas de cookie.

### 6. Avis clientes et contenus intégrés

| Cookie | Fournisseur | Finalité | Durée |
|---|---|---|---|
| [À VÉRIFIER : selon l'outil, ex. Judge.me] | [À COMPLÉTER] | Affichage des avis | [À VÉRIFIER] |
| `YSC`, `VISITOR_INFO1_LIVE` | YouTube (si une vidéo est intégrée) | Lecture vidéo et statistiques | Session / 6 mois |

## Transferts hors de l'Union européenne

Certains fournisseurs (Google, Meta, TikTok, Klaviyo) peuvent transférer des données vers les États-Unis ou d'autres pays tiers. Ces transferts sont encadrés par le Data Privacy Framework UE-États-Unis ou par des clauses contractuelles types. Détails dans notre [Politique de confidentialité](À COMPLÉTER : lien).

## Contact

Pour toute question : **[À COMPLÉTER : e-mail]**. Tu peux aussi adresser une réclamation à la CNIL (www.cnil.fr).
