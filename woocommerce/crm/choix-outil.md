# Choix de l'outil CRM : Brevo ou Klaviyo

CHARMED PARIS · boutique WooCommerce bilingue FR + EN · parures en dropshipping Branvas · lancement fin 2026.

> **Prix : à revérifier le jour de la souscription.** Pendant cette session, je n'ai pas pu ouvrir brevo.com ni klaviyo.com (domaines bloqués par le réseau). Les chiffres ci-dessous viennent de la recherche web du 22/11/2026, avec des relevés tiers datés d'octobre à novembre 2026. Les sources sont en bas de page. Les prix Brevo sont en € HT, ceux de Klaviyo en $ US.

---

## 1. Ce dont la boutique a besoin (cahier des charges)

| Besoin | Pourquoi chez CHARMED PARIS |
|---|---|
| Intégration WooCommerce native (contacts, commandes, panier, produits) | Aucun développeur au lancement, et Branvas se connecte déjà à Woo par l'API REST. |
| Automatisations e-commerce : bienvenue, panier abandonné, navigation abandonnée, post-achat, anniversaire, réactivation, retour en stock | Voir `flows.md` (11 flows). |
| Bilingue FR + EN | Chaque flow existe dans les deux langues, avec un aiguillage sur l'attribut `LANGUE`. |
| SMS en France (et au Royaume-Uni et aux États-Unis en anglais) | Usage léger : rappels de Noël, de la Saint-Valentin et de la fête des mères, plus l'avis d'expédition. |
| RGPD, avec les données hébergées si possible dans l'UE | Boutique française, cible française d'abord, et la CNIL est attentive aux transferts hors UE. |
| Coût bas au départ | La marge par parure est d'environ 13 à 17 € sur l'entrée de gamme (voir `segmentation-et-fidelite.md` §7). L'outil ne doit pas la manger. |
| Codes promo uniques | Bienvenue −10 %, anniversaire, Le Cercle et parrainage. |

---

## 2. Comparatif

| Critère | **Brevo** (ex-Sendinblue) | **Klaviyo** |
|---|---|---|
| Société | Française (siège à Paris). | Américaine (Boston). |
| Hébergement des données | **Dans l'UE** : OVHcloud en France et en Allemagne, Google Cloud en Belgique, selon le centre d'aide Brevo. | **Aux États-Unis par défaut** (AWS us-east-1, Virginie). Le transfert repose sur l'adhésion au Data Privacy Framework UE–US et sur les clauses contractuelles types. Le DPA prévoit un hébergement UE « si le client l'a stipulé ». Les conditions (offre, coût) sont à demander à Klaviyo. |
| Interface et support | En français. | Majoritairement en anglais. L'aide existe en français. |
| Intégration WooCommerce | Plugin officiel gratuit « Brevo for WooCommerce » : contacts, commandes et événements panier/commande pour les automatisations, plus un suivi du panier abandonné. **Je n'ai pas trouvé de déclencheur natif « produit consulté »** pour la navigation abandonnée. Il faudra soit le traceur JS Brevo, soit un événement envoyé par l'API. C'est à tester. | Extension officielle Klaviyo for WooCommerce : événements Viewed Product, Added to Cart, Started Checkout, Placed Order, Fulfilled Order, catalogue produits, compatibilité HPOS et blocs Panier/Commande. Modèles prêts pour la navigation abandonnée, la baisse de prix et le retour en stock. **C'est le point fort de Klaviyo.** |
| Segmentation et données | Bonne : attributs, événements, segments dynamiques. Le scoring de contacts n'est disponible qu'en Professional. | Excellente : RFM, prédictions (CLV, date du prochain achat) à partir d'un volume de commandes suffisant, recommandations produits. |
| Mode de facturation | **Au volume d'e-mails envoyés.** Les plafonds de contacts dépendent du palier, les sources se contredisent, à vérifier. | **Au nombre de profils actifs.** Attention : les clientes WooCommerce synchronisées sans consentement marketing comptent aussi, sauf si on les supprime. |
| Prix d'entrée (relevés 2026) | Gratuit : 300 e-mails par jour. Starter : dès **7 € HT/mois** (5 000 e-mails). Standard : dès **15 € HT/mois** (17 € selon le centre d'aide). Professional : dès 499 €. Selon un comparatif, l'automatisation complète commence en **Standard**, à vérifier. | Gratuit : 250 profils, 500 envois par mois, 150 crédits SMS/MMS. Email : dès **20 $/mois** (251 à 500 profils). Email + SMS : dès **35 $/mois** environ. Environ 150 $/mois à 10 000 profils (e-mail seul). |
| SMS France | Crédits prépayés sans expiration, sans abonnement. Environ **0,045 € par SMS vers la France** (4,5 crédits à 0,01 €), selon un relevé tiers de novembre 2026. | France couverte, avec un expéditeur alphanumérique (« CHARMED »). Le tarif par message n'est visible que dans le compte (Billing). Deux petits opérateurs (SYMA, Lebara) reçoivent les SMS par un shortcode à 5 chiffres. Pas de réponse possible avec un expéditeur alphanumérique. |
| SMS Royaume-Uni et États-Unis | Possibles, au tarif par pays, à vérifier. | Possibles. Aux États-Unis, enregistrement obligatoire d'un numéro (10DLC ou toll-free) : comptez des démarches et un délai. |
| Bilingue | Attribut `LANGUE`, puis une condition dans le workflow et un modèle par langue. Simple. | Même logique : propriété de profil, puis un « conditional split ». Simple aussi. |
| Codes promo uniques | Collections de codes importées dans Brevo. Les codes doivent d'abord être créés dans WooCommerce (en masse, par plugin ou WP-CLI). | Klaviyo sait générer des coupons uniques pour certaines plateformes. **Pour WooCommerce, à vérifier**, sinon même méthode que Brevo. |
| Courbe d'apprentissage | Douce. | Plus raide, mais très documentée. |

---

## 3. Coût estimé la première année

Hypothèse : 1 500 contacts à 6 mois, environ 10 000 e-mails par mois (campagnes et flows), 1 500 SMS sur l'année (quatre temps forts).

| | Brevo Standard | Klaviyo Email (+ SMS) |
|---|---|---|
| E-mail | Environ 15 à 30 € HT/mois selon le palier de volume | Environ 45 à 60 $/mois à 1 500–2 500 profils **actifs**, clientes non abonnées comprises |
| SMS (1 500 sur l'an, FR) | Environ 70 € (1 500 × 0,045 €) | Tarif au message, à lire dans le compte |
| **Ordre de grandeur annuel** | **Environ 250 à 430 € HT** | **Environ 550 à 900 $** |

Ce sont des ordres de grandeur, pas des devis. Seuls les configurateurs officiels font foi.

---

## 4. RGPD : ce qui change concrètement

- **Brevo** : les données restent dans l'UE et il n'y a pas d'analyse de transfert hors UE à documenter. Il reste à signer le DPA (accord de sous-traitance), à lister Brevo dans le registre des traitements et à le citer dans la politique de confidentialité.
- **Klaviyo** : c'est légal (DPF et clauses contractuelles types), mais il faut documenter le transfert vers les États-Unis dans le registre et la politique de confidentialité. Le sujet est plus sensible si la CNIL ou une cliente pose la question.
- **Dans les deux cas** :
  - Le traceur JS (navigation abandonnée, pages vues) dépose des cookies. Il ne doit se charger **qu'après consentement** via la bannière cookies (CMP : Complianz, CookieYes…).
  - La navigation abandonnée ne touchera donc que les visiteuses à la fois **identifiées** et **consentantes aux cookies**. Le volume sera faible, et c'est normal.
  - L'authentification du domaine d'envoi est obligatoire : SPF, DKIM, DMARC. Gmail et Yahoo l'exigent depuis 2024 pour les envois en volume, avec en plus un désabonnement en un clic.

---

## 5. Recommandation : **Brevo (offre Standard) au lancement**

**Pourquoi Brevo :**
1. **Données dans l'UE et société française.** C'est l'option la plus simple et la plus rassurante pour une boutique qui vend d'abord en France. C'est aussi un vrai argument dans la politique de confidentialité.
2. **Le coût suit l'activité.** La facturation au volume d'e-mails permet de garder toutes les clientes dans la base (service après-vente, historique) sans payer chaque profil. Les SMS se paient à l'unité, sans abonnement : idéal pour quatre temps forts par an.
3. **Ça suffit pour 9 flows sur 11** : bienvenue, panier (plugin), post-achat, cross-sell, anniversaire, réactivation, saisons, Le Cercle et parrainage, tous en FR et en EN.
4. **Interface en français.** Tu pourras piloter seule, sans prestataire.

**Ce que Brevo fait moins bien (et comment le contourner) :**
- **Navigation abandonnée** : il n'y a pas de déclencheur « produit consulté » confirmé. On teste le traceur Brevo, ou un événement `product_viewed` envoyé par un petit snippet (API « track event »). Si rien ne marche, ce flow attend et on vit sans. C'est le flow qui pèse le moins.
- **Retour en stock** : il n'y a pas d'équivalent natif sûr. On passe par un plugin Woo « préviens-moi » qui alimente une liste Brevo.
- **Pas de prédictif** : on fait un RFM simple, par attributs (voir `segmentation-et-fidelite.md`).

**À vérifier avant de payer (sur un site de préproduction) :**
- [ ] Le plugin Brevo for WooCommerce est compatible avec la version de Woo, le HPOS, les blocs Panier/Commande et le plugin multilingue choisi (WPML, Polylang ou TranslatePress).
- [ ] Les événements panier et commande remontent, avec image, prix, catégorie (= univers) et **langue de la commande**.
- [ ] Le numéro de suivi DHL écrit par Branvas dans la commande est lisible, soit par Brevo, soit par le plugin de suivi (voir `flows.md` §0.4).
- [ ] La création des codes uniques dans Woo et leur import dans une collection Brevo fonctionnent.
- [ ] L'offre Starter inclut-elle les workflows ? Sinon, prendre Standard.
- [ ] Le plafond de contacts du palier choisi.
- [ ] Le tarif SMS France, Royaume-Uni et États-Unis dans le calculateur officiel. L'expéditeur fait **11 caractères maximum** : « CHARMED », car « CHARMEDPARIS » en fait 12.

**Quand passer à Klaviyo (à revoir à 6 mois) :** si **au moins deux** de ces conditions sont réunies.
- Plus de 3 000 profils engagés, et les e-mails pèsent plus de 20 % du chiffre d'affaires.
- La navigation abandonnée et les recommandations produits deviennent un levier clé, et Brevo n'y arrive pas proprement.
- Il faut des prédictions (date du prochain achat, CLV) pour piloter la fidélité.
- Le marché anglophone (Royaume-Uni et États-Unis) dépasse le marché français.

La migration est faisable. Les flows de `flows.md` sont écrits pour être portables : chaque étape indique son équivalent Klaviyo.

**Outil d'avis, en complément :** Judge.me (plugin WooCommerce), ou un équivalent. Il envoie lui-même la demande d'avis, en FR et en EN. Branvas ne fournit **aucun avis** : tous viendront de vraies clientes.

---

## Sources (recherche web du 22/11/2026)

- Brevo, plans et prix : [help.brevo.com, About Brevo's pricing plans](https://help.brevo.com/hc/en-us/articles/208589409) · [getkanal, Brevo prix 2026](https://getkanal.com/fr/blog/brevo-prix) · [getkanal, Brevo SMS 2026](https://getkanal.com/fr/blog/brevo-sms) · [Moosend, Brevo pricing 2026](https://moosend.com/blog/brevo-pricing/) · [Chatarmin, Brevo pricing 2026](https://chatarmin.com/en/blog/brevo-pricing) · [Calculateur SMS Brevo](https://www.brevo.com/tools/ecommerce-tools/sms-whatsapp-cost-calculator/?lang=fr)
- Brevo, hébergement des données : [help.brevo.com, Data storage location](https://help.brevo.com/hc/en-us/articles/360001005510) · [Brevo, Sécurité](https://www.brevo.com/fr/securite/)
- Brevo × WooCommerce : [Brevo for WooCommerce (wordpress.org)](https://wordpress.org/plugins/woocommerce-sendinblue-newsletter-subscription/) · [Brevo, abandoned cart](https://help.brevo.com/hc/en-us/articles/360002368860) · [Brevo plugin Woo](https://www.brevo.com/plugins/woo)
- Klaviyo, prix : [klaviyo.com/pricing](https://klaviyo.com/uk/pricing) · [Omnisend, Klaviyo pricing](https://www.omnisend.com/blog/klaviyo-pricing/) · [MoEngage, Klaviyo pricing 2026](https://www.moengage.com/blog/klaviyo-pricing/) · [Capterra](https://www.capterra.com/p/156699/Klaviyo/pricing)
- Klaviyo × WooCommerce : [Klaviyo WooCommerce integration](https://www.klaviyo.com/platform-integrations/woocommerce) · [Klaviyo for WooCommerce (woocommerce.com)](https://woocommerce.com/products/klaviyo-for-woocommerce/)
- Klaviyo, SMS : [Where is Klaviyo SMS available?](https://help.klaviyo.com/hc/fr-fr/articles/4402914866843) · [Klaviyo, SMS marketing France](https://www.klaviyo.com/uk/blog/sms-marketing-france)
- Klaviyo, RGPD et hébergement : [Klaviyo Privacy FAQs](https://klaviyo.com/legal/privacy-faqs) · [Klaviyo DPA](https://klaviyo.com/legal/dpa) · [Klaviyo GDPR](https://www.klaviyo.com/gdpr)
