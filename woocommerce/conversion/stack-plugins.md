# CHARMED PARIS — Stack WordPress / WooCommerce (FR + EN)

> Vérifications faites le 22–23/11/2026 par recherche web (fiches WordPress.org, WooCommerce.com, docs éditeurs). Les numéros de version varient selon les miroirs WordPress.org : **la version installée doit toujours être vérifiée sur la fiche officielle le jour de l'installation**.
> Statuts : ✅ existe et maintenu en 2026 (vérifié) · ⚠️ existe, mais avec un signal négatif · ❌ à ne pas utiliser · 🔎 à vérifier (non confirmé).

## 0. Principes
1. **Un seul outil par fonction** : un seul cache, un seul gestionnaire de pixels, une seule passerelle carte, un seul outil d'e-mail. La plupart des bugs WooCommerce viennent des doublons.
2. **Branvas se connecte par l'API REST, sans plugin** [fait]. Aucun plugin ne doit modifier les produits Branvas (SKU, stock, prix) ni les statuts de commande : Branvas ne traite que les commandes « En cours » (payées).
3. Moins de 25 plugins actifs. Chaque plugin doit avoir un rôle CRO, légal ou de sécurité identifiable.
4. Socle : WordPress et WooCommerce à jour, PHP 8.2 ou plus, **HPOS** (stockage haute performance des commandes) activé, HTTPS (obligatoire pour Branvas [fait]), Checkout et Cart en **blocs** WooCommerce.
5. **Commande test obligatoire après chaque plugin touchant le panier, le checkout, la langue ou la devise**. Elle doit apparaître dans Branvas, recevoir le suivi, et ne pas être comptée 2 fois dans GA4 ni dans Meta.

---

## 1. Paiement

| Rôle | Recommandé | Gratuit / payant | Statut | Alternatives | Notes |
|---|---|---|---|---|---|
| Carte + Apple Pay + Google Pay + multidevise | **WooPayments** (`woocommerce-payments`) | Plugin gratuit, commission par transaction [à vérifier : grille FR en vigueur] | ✅ disponible pour les entreprises établies en France métropolitaine/EEE ; Apple Pay dans tous les pays couverts ; Google Pay activé avec Apple Pay (couverture FR déduite, non explicitement documentée) | **WooCommerce Stripe Payment Gateway** (`woocommerce-gateway-stripe`, ✅ v10.x–11.0 en 2026, Express Checkout = Apple/Google Pay, Klarna) | **Choisir l'un OU l'autre, jamais les 2.** WooPayments a l'avantage d'inclure le **multidevise** (EUR + USD pour la phase EN). Avec Stripe Gateway, il faut un plugin de devises séparé. Signal négatif Stripe : des utilisateurs rapportent que les boutons express se réactivent sur les fiches après chaque mise à jour (à contrôler après mise à jour) |
| PayPal + paiement en 4× | **WooCommerce PayPal Payments** | Gratuit, commission PayPal | ✅ ; PayPal 4X disponible pour les marchands établis en France avec un site orienté France, en EUR | — | Montants éligibles **contradictoires** selon les pages PayPal : 20–3 000 € ou 30–2 000 € [à vérifier dans le compte]. Avis récents mitigés sur la configuration : tester. Le message « Paiement en 4× » est à afficher **seulement sur la Joaillerie 925** (et dans le panier dès 90 €), pas partout |
| Paiement fractionné dédié | **Alma** (`alma-gateway-for-woocommerce`) | Commission marchand **3,6 à 4,8 % HT selon les sources** [à vérifier] | ✅ plugin officiel mis à jour en 2026 (WP 6.6+, PHP 7.4+) ; options 3×/4× **non confirmées sur la fiche** | Klarna (via Stripe/WooPayments) 🔎 | **Pas au lancement** : panier minimum annoncé entre 50 et 100 € selon les sources [à vérifier], frais élevés au regard de la marge (cf. `offres-et-panier-moyen.md`). Phase 2, seulement si la Joaillerie 925 décolle et si PayPal 4X ne suffit pas |
| Marchés EN | Même stack ; PayPal Pay Later (US « Pay in 4 », UK « Pay in 3 ») 🔎 | — | 🔎 éligibilité par pays à vérifier dans PayPal | — | Ne pas ajouter Afterpay/Clearpay au lancement |

**Anti-fraude** : Stripe Radar (inclus dans WooPayments/Stripe) plutôt qu'un captcha visible au checkout.

---

## 2. Checkout, panier, mini-panier

| Rôle | Recommandé | Gratuit / payant | Statut | Alternatives | Notes |
|---|---|---|---|---|---|
| Checkout 1 page | **Checkout Block natif WooCommerce** (personnalisation légère : champs, textes, bouton légal) | Gratuit | ✅ (cœur WooCommerce) | **FunnelKit Funnel Builder** (`funnel-builder`, version Lite gratuite + Pro ; Plus annoncé ≈ 179,50 $/an) ✅ ; **CheckoutWC** (payant, version Lite existante) ✅ | Commencer en natif. Passer à FunnelKit **ou** CheckoutWC (pas les 2) seulement si le taux de finalisation reste sous 50 % après les corrections du `plan-conversion.md`. **Ne pas utiliser les upsells 1 clic post-achat** de FunnelKit (2e commande = 2e frais de 8,99 $ chez Branvas [fait]) |
| Mini-panier (tiroir) | **Celui de la maquette**, reconstruit sur le **Mini-Cart Block** / Store API (barre de progression, 2e parure −15 %, suggestions) | Gratuit (développement) | ✅ | FunnelKit Cart ✅ (inclus dans la suite FunnelKit) | Éviter les vieux plugins de side cart qui utilisent `wc-cart-fragments` : lents et souvent cassés par le cache |
| Remise « 2e parure −15 % » | Règle codée (snippet) ou plugin de règles de prix 🔎 | — | — | — | Un seul moteur de remises. Il doit rester compatible avec le Checkout Block et la multidevise (tester en EUR et en USD) |
| Délai de livraison estimé | **Snippet maison** (jours ouvrés FR, jours fériés, heure de traitement, P90 par pays Branvas [fait]) | Gratuit | — | Plugins « estimated delivery date » 🔎 | Un snippet de 50 lignes évite un plugin lourd et respecte exactement les délais Branvas |
| Téléphone requis hors US/UK | Snippet sur les champs du Checkout Block | Gratuit | — | — | Exigé par le transporteur [fait] |
| E-carte cadeau | **PW WooCommerce Gift Cards** | Gratuit + Pro | ✅ (compatible HPOS ; WP 7.x dans le changelog) ⚠️ des avis fin 2025 se plaignent de renouvellements sans préavis ; compatibilité avec le Checkout Block **contradictoire** selon les avis | WooCommerce Gift Cards (officiel, payant) 🔎 | Utile du 5/12 au 24/12 (après la date limite de Noël en Europe). Désactiver le renouvellement automatique si Pro |

---

## 3. Avis clients vérifiés

> ⚠️ **Correction importante** : **Judge.me n'est plus disponible pour WooCommerce.** La fiche WordPress.org a été fermée le **13/08/2025** à la demande de l'auteur, et le support WooCommerce a pris fin fin 2025 (30/09 ou 31/10 selon les sources). Ne pas le prévoir dans le projet.

| Rôle | Recommandé | Gratuit / payant | Statut | Notes |
|---|---|---|---|---|
| Avis produits au lancement | **Avis natifs WooCommerce** avec « Seuls les propriétaires vérifiés peuvent laisser un avis » + badge « propriétaire vérifié » | Gratuit | ✅ (cœur) | Le plus léger. Les demandes d'avis partent de Brevo/Klaviyo (J+7 après livraison) avec un lien vers la fiche. Conforme si la **méthode de vérification est expliquée** sur le site (`legal-checklist.md`) |
| Photos dans les avis | **Photo Reviews for WooCommerce** (`woo-photo-reviews`) | Gratuit + Pro | ✅ existe 🔎 version 2026 à vérifier | Les photos réelles de clientes : fort levier pour les bijoux |
| Avis + collecte automatisée (si Klaviyo) | **Klaviyo Reviews** | Add-on à partir de 25 $/mois, réservé aux clients Klaviyo Email payants | ✅ WooCommerce supporté depuis juin 2024 | Cohérent si Klaviyo est l'outil d'e-mail |
| Plateforme SaaS d'avis | **WiserReview** (`wiser-review`) | Freemium 🔎 | ✅ sur WordPress.org (éditeur WiserNotify) | Migration Judge.me prévue (inutile ici). Les pages comparatives sont du marketing éditeur |
| À éviter | **Customer Reviews for WooCommerce (CusRev)** ⚠️ | — | La fiche indique « non testé avec les 3 dernières versions majeures » et renvoie vers un autre plugin | Ne pas installer |
| À éviter au lancement | **Trustpilot Reviews** ⚠️ | Gratuit | v3.11.0 (03/2026) mais avis 2026 très négatifs (boucle de connexion, plugin « abandonné ») | Peut-être plus tard, via widget seul |
| 🔎 | Skeepers (ex-Avis Vérifiés) | Payant | Non trouvé lors de la vérification | À vérifier si besoin d'un tiers certificateur français |

**Interdits** : importer des avis AliExpress ou Branvas (Branvas n'en fournit aucun [fait]), avis d'amies non identifiés, filtrage des avis négatifs, avis rémunérés sans mention.

---

## 4. E-mail, SMS, panier abandonné

| Rôle | Recommandé | Gratuit / payant | Statut | Alternatives | Notes |
|---|---|---|---|---|---|
| E-mails marketing + automatisations + SMS | **Brevo for WooCommerce** (`woocommerce-sendinblue-newsletter-subscription`) | Plugin gratuit ; Brevo freemium, paliers payants 🔎 | ✅ plugin officiel Brevo | **Klaviyo for WooCommerce** (`klaviyo`, ✅ v3.8.0 du 27/05/2026 : consentement WhatsApp au checkout, correctif sécurité des identifiants API) | Brevo est **français**, ses tarifs sont accessibles et il gère SMS et transactionnel : **recommandé au lancement**. Klaviyo est plus puissant (segmentation, Reviews) mais plus cher ; avis mitigés sur le support |
| Panier abandonné | **Dans Brevo** (activer le suivi du panier dans les réglages du plugin ; e-mail H+1, H+24, SMS seulement avec opt-in SMS) | Inclus | ✅ (docs Brevo) | CartBoss (SMS, ✅ sur WordPress.org), Abandoned Cart Lite ✅ | **Un seul système** de relance. L'e-mail est capté au 1er champ du checkout ; les relances marketing exigent une base légale (en pratique en France : client existant pour des produits analogues, ou opt-in), cf. `legal-checklist.md` |
| E-mails transactionnels | WooCommerce natif + traduction FR/EN + délivrabilité SMTP (via Brevo) | Gratuit | ✅ | — | Ajouter le délai estimé, le lien de rétractation, les CGV jointes |

**Flux à créer** (FR et EN) : bienvenue (3 e-mails), panier abandonné (2), post-achat (confirmation, envoi, entretien J+1, avis J+7, « un souci ? » J+10, cross-sell J+30), réactivation à 90 jours.

---

## 5. Multilingue et multidevise

| Rôle | Recommandé | Gratuit / payant | Statut | Alternatives | Notes |
|---|---|---|---|---|---|
| Traduction FR → EN | **TranslatePress** (licence avec le module SEO : slugs traduits, hreflang, sitemap) | Gratuit + payant (Business ≈ 199 $/an selon un comparatif éditeur 🔎) | ✅ (comparatifs 2026) | **WPML + WooCommerce Multilingual & Multicurrency** (payant, pas de version gratuite ; multidevise inclus ; e-mails Woo traduits par défaut) ✅ ; **Polylang + Polylang for WooCommerce** (add-on payant, sans multidevise) ✅ | **Argument décisif pour TranslatePress : un seul produit en base.** Branvas crée et met à jour les produits par l'API (prix, stock, images) [fait]. WPML/Polylang dupliquent chaque produit en version EN : le stock et les commandes EN doivent alors être resynchronisés, et la reconnaissance par Branvas des commandes passées sur la copie EN est **non garantie** 🔎. **Test bloquant** avant la mise en ligne EN : commande sur `/en/` → visible et traitée dans Branvas. Point faible de TranslatePress : les e-mails transactionnels demandent une configuration manuelle |
| Devises | **Multidevise de WooPayments** (taux manuels, arrondi, détection géographique) | Inclus | ✅ (doc officielle : taux manuels non mis à jour automatiquement, arrondi) | YayCurrency (`yaycurrency`) ✅ si Stripe Gateway ; WCML si WPML | **Lancement : EUR seulement.** Phase 2 : USD pour les US, prix fixés à la main (59/79/89 $). GBP seulement après la décision TVA UK |
| Sélecteur | Sélecteur de langue de TranslatePress (texte « FR \| EN ») ; **pas de redirection automatique par IP** | — | — | — | cf. `plan-conversion.md` §5 |

---

## 6. Tracking et consentement

| Rôle | Recommandé | Gratuit / payant | Statut | Alternatives | Notes |
|---|---|---|---|---|---|
| Bannière cookies / CMP | **Complianz – GDPR/CCPA Cookie Consent** (`complianz-gdpr`) | Gratuit + Premium (géolocalisation par région, utile pour l'EN/US) | ✅ ; Consent Mode v2 documenté (« Consent Mode for Complianz 7 ») ; intégration IAB TCF (CMP ID 332) ; CMP certifiée Google | **Cookiebot** (`cookiebot`) ✅ : Consent Mode v2 et TCF 2.2 explicitement annoncés | Configurer le bouton **« Tout refuser » au même niveau que « Tout accepter »** (CNIL). Si un autre plugin injecte GTM/GA, désactiver sa propre intégration Complianz (Complianz → Intégrations) pour éviter les doublons |
| GA4 + Google Ads + Meta Pixel + CAPI + TikTok + Pinterest | **Pixel Manager for WooCommerce** (`woocommerce-google-adwords-conversion-tracking-tag`) | Gratuit (GA4 e-commerce, Meta Pixel, Consent Mode v2) ; **Pro** pour Meta CAPI, TikTok Events API, GA4 Measurement Protocol | ✅ ; 19 CMP compatibles, valeurs par défaut Consent Mode v2 par région | GTM + GTM4WP 🔎 (plus flexible, plus technique) | **Outil unique recommandé** pour tous les pixels, avec dédoublonnage navigateur/serveur. Attention : un autre plugin au nom proche (« Pixel Tag Manager for WooCommerce ») existe ; vérifier le slug |
| Catalogue Meta (pubs dynamiques) | **Meta for WooCommerce** (`facebook-for-woocommerce`), **catalogue seulement** | Gratuit | ✅ ⚠️ des avis 2026 signalent des blocages pendant la configuration | — | **Désactiver son pixel** si Pixel Manager envoie déjà les événements (sinon double comptage) |
| Catalogue Pinterest | **Pinterest for WooCommerce** | Gratuit | ✅ mis à jour en 2026 ⚠️ avis mitigés (erreurs de flux, HTTP 429) | Flux produit manuel | Catalogue seulement ; tag via Pixel Manager |
| TikTok | **TikTok for Business / TikTok for WooCommerce** : publicités seulement | Gratuit | ✅ pour les pubs ; ❌ **fonctions TikTok Shop arrêtées le 01/06/2026** sur ce plugin | — | Événements via Pixel Manager Pro ; le plugin TikTok sert au catalogue si nécessaire |
| Google Merchant Center | Google for WooCommerce 🔎 ou flux via Pixel Manager / fichier | Gratuit | 🔎 | — | Pas d'EAN chez Branvas [fait] : `identifier_exists = no`, MPN = SKU JS… |
| Tests A/B | **Nelio A/B Testing** (`nelio-ab-testing`) | Gratuit limité + Premium | ✅ v8.5.x (oct. 2026) ; objectifs WooCommerce (valeur de commande), compatible avec les blocs ; service cloud (déclaré conforme RGPD) | GrowthBook / VWO 🔎 | Avis mitigés sur l'essai gratuit. Ne lancer des tests qu'avec un volume suffisant (`tracking-et-tests.md`) |

---

## 7. Recherche

| Rôle | Recommandé | Statut | Notes |
|---|---|---|---|
| Recherche instantanée | **FiboSearch – Ajax Search for WooCommerce** (`ajax-search-for-woocommerce`), version gratuite | ✅ v1.33 (04/2026) à 1.34.x selon les miroirs ; ≈ 4,9/5 ; plus de 100 000 installations | Avec 30 parures, la version gratuite suffit. Indexer SKU, univers, matières, couleurs de pierre ; traduire via TranslatePress. Optionnel au lancement : la navigation par univers et budget compte plus que la recherche |

---

## 8. Cache, performance, images

| Rôle | Recommandé | Gratuit / payant | Statut | Notes |
|---|---|---|---|---|
| Cache de page + optimisation | **Cache de l'hébergeur** (si hébergement WooCommerce managé) **ou WP Rocket** | WP Rocket payant | ✅ docs à jour : exclut automatiquement panier, checkout, compte et l'API REST WooCommerce | Avec un mini-panier PHP : ajouter le cookie `woocommerce_items_in_cart` en « Never Cache Cookies ». Tester l'intro Three.js avec « Delay JS » (doit rester fluide) |
| Images | WebP/AVIF côté hébergeur/CDN ou plugin de conversion 🔎 | — | 🔎 | Originaux Branvas HD ≥ 1600 px, servis en `srcset` |
| CDN | Cloudflare (gratuit) 🔎 config | — | — | **Ne pas mettre en cache** `/panier`, `/commande`, `/mon-compte`, `/wp-json/` (l'API Branvas passe par là) ; aucune règle WAF qui bloque l'API REST de Branvas |

---

## 9. Sécurité et maintenance

| Rôle | Recommandé | Statut | Notes |
|---|---|---|---|
| Pare-feu + scan + 2FA | **Wordfence Security** (gratuit ; Premium = règles en temps réel, contre 30 jours de délai en gratuit) | ✅ actif en 2026 (alertes sur des compromissions de la chaîne d'approvisionnement, ex. BdThemes, 08/2026) | 2FA obligatoire pour tous les admins. **Ne pas cumuler** avec un 2e pare-feu applicatif (Solid Security, All-In-One WP Security…) |
| Clés API Branvas | Utilisateur WooCommerce dédié, clé REST lecture/écriture limitée à cet usage, rotation si fuite | — | Ne jamais partager la clé par e-mail |
| Sauvegardes | Sauvegarde quotidienne de l'hébergeur + copie externe hebdomadaire (UpdraftPlus 🔎) | — | Tester une restauration |
| Mises à jour | Préproduction (staging) → commande test → production ; mises à jour automatiques **seulement** pour les correctifs de sécurité mineurs | — | — |

---

## 10. Légal

| Rôle | Recommandé | Statut | Notes |
|---|---|---|---|
| Fonction de rétractation en ligne (obligatoire depuis le 19/06/2026) | **WebToffee EU Order Withdrawal Button for WooCommerce** (`wt-eu-withdrawal-button`) | ✅ sur WordPress.org | Alternatives ✅ : WWU Withdrawal Button, EU Withdrawal Button Lite, BeziWorld Withdrawal, BuddyPilot Withdrawal. Choisir **un seul**. Bouton dans « Mon compte » **et** accès sans compte (commande invité : n° de commande + e-mail). Vérifier la traduction FR |
| CGV, mentions légales, confidentialité | **Pages WordPress rédigées** (juriste ou générateur sérieux), **sans plugin** | — | Le plugin ne rend pas conforme ; le contenu, si. Cases et bouton légal via snippets (`legal-checklist.md`) |
| Factures PDF | WooCommerce PDF Invoices & Packing Slips 🔎 ou module de l'outil comptable | 🔎 | Mentions légales des factures (`legal-checklist.md`). **Ne pas** joindre de facture au colis (Branvas envoie un bordereau sans prix [fait]) |
| SEO | Cf. `seo/strategie-seo.md` (un seul plugin SEO) | — | — |

---

## 11. Ce qu'il ne faut PAS installer

| Plugin / type | Pourquoi |
|---|---|
| **Judge.me for WooCommerce** | Fermé sur WordPress.org depuis le 13/08/2025, support WooCommerce terminé |
| Customer Reviews for WooCommerce (ancien CusRev) | Non maintenu selon sa propre fiche |
| Trustpilot Reviews (au lancement) | Avis 2026 très négatifs, compatibilité incertaine |
| Plugins « sales pop » / « X vient d'acheter » / « Y personnes regardent » / compte à rebours / « stock bas » | Dark patterns et pratiques commerciales trompeuses s'ils sont faux ; contraires au brief |
| Plugins d'import AliExpress / dropshipping génériques | Inutiles (Branvas passe par l'API) et risque de conflit sur SKU et stock |
| 2 passerelles carte (WooPayments **et** Stripe Gateway) | Doubles boutons Apple Pay, conflits de webhooks |
| 2 caches (WP Rocket + LiteSpeed Cache + cache hôte…) | Panier vide, prix en mauvaise devise servis depuis le cache |
| 2 pare-feu (Wordfence + Solid Security…) | Conflits, blocages de l'API Branvas |
| Plusieurs plugins de pixels (Meta for WooCommerce avec pixel + Pixel Manager + plugin TikTok avec pixel) | Double comptage des achats, ROAS faux |
| WooCommerce Germanized / German Market | Conçus pour le droit allemand, lourds, ils modifient le checkout |
| Page builders lourds + packs d'add-ons (Elementor + 3 add-ons…) | LCP mobile, conflits avec l'intro Three.js ; la maquette est déjà en HTML/CSS sur mesure |
| Upsell post-achat 1 clic (FunnelKit One Click Upsell…) | Chaque upsell = nouvelle commande Branvas et 8,99 $ de plus [fait] |
| Fonctions TikTok Shop du plugin TikTok | Arrêtées depuis le 01/06/2026 |
| Alma au lancement | Frais élevés pour un panier moyen d'environ 72 € ; PayPal 4X couvre le besoin |
| Traduction automatique publiée sans relecture (DeepL/IA en direct) | Confiance et conformité (CGV EN, matières) |
| Plugins dont l'éditeur a été compromis | Suivre les alertes Wordfence avant d'installer (ex. BdThemes, 08/2026) |

---

## 12. Liste finale (lancement FR, puis EN)

1. WooCommerce (blocs Cart/Checkout, HPOS)
2. WooPayments **ou** Stripe Gateway
3. WooCommerce PayPal Payments (PayPal 4X)
4. Complianz
5. Pixel Manager for WooCommerce (Pro)
6. Meta for WooCommerce (catalogue, pixel désactivé)
7. Pinterest for WooCommerce (catalogue)
8. Brevo for WooCommerce
9. WebToffee EU Order Withdrawal Button (ou équivalent)
10. Photo Reviews for WooCommerce (avec les avis natifs restreints aux propriétaires vérifiés)
11. WP Rocket (si pas de cache hôte)
12. Wordfence
13. FiboSearch (facultatif)
14. PW WooCommerce Gift Cards (avant le 4/12)
15. Plugin SEO (cf. `seo/`)
16. **Phase EN** : TranslatePress + module SEO, multidevise de WooPayments (USD)
17. **Phase 2** : Nelio A/B Testing ; FunnelKit **ou** CheckoutWC si besoin ; Alma si la 925 décolle

## Sources consultées (vérification 2026)
- Alma : https://fr.wordpress.org/plugins/alma-gateway-for-woocommerce/ · tarifs (sources tierces, à vérifier) : https://hackceleration.com/fr/labs/meilleur/paiement-fractionne-e-commercants , https://www.leptidigital.fr/logiciels/alma/
- Judge.me fermé : https://wordpress.org/plugins/judge-me-product-reviews-woocommerce/ · https://wiserreview.com/blog/judge-me-shutdown-alternatives/
- CusRev : https://wordpress.org/plugins/customer-reviews-woocommerce/ · Collector : https://wordpress.org/plugins/customer-reviews-collector-for-woocommerce/
- Klaviyo : https://wordpress.org/plugins/klaviyo/ · Klaviyo Reviews : https://www.klaviyo.com/blog/klaviyo-reviews-for-woocommerce
- Brevo : https://wordpress.org/plugins/woocommerce-sendinblue-newsletter-subscription/ · https://www.brevo.com/blog/woocommerce-abandoned-cart-recovery/
- Complianz : https://wordpress.org/plugins/complianz-gdpr/ · https://complianz.io/consent-mode-for-7-0 · Cookiebot : https://wordpress.org/plugins/cookiebot/
- WooPayments : https://woocommerce.com/document/payments/countries/ · https://woocommerce.com/document/woopayments/payment-methods/apple-pay/ · multidevise : https://woocommerce.com/document/woopayments/currencies/multi-currency-setup/
- Stripe : https://wordpress.org/plugins/woocommerce-gateway-stripe/
- PayPal 4X : https://developer.paypal.com/docs/checkout/pay-later/fr/commerce-platforms/woocommerce/paypal/ · https://woocommerce.com/fr/products/woocommerce-paypal-payments/
- Pixel Manager : https://wordpress.org/plugins/woocommerce-google-adwords-conversion-tracking-tag/ · https://woocommerce.com/products/pixel-manager-pro/
- Meta for WooCommerce : https://wordpress.org/plugin/facebook-for-woocommerce/ · TikTok : https://wordpress.org/plugins/tiktok-for-business/ · Pinterest : https://wordpress.org/plugins/pinterest-for-woocommerce/
- FiboSearch : https://wordpress.org/plugins/ajax-search-for-woocommerce/
- FunnelKit / CheckoutWC : https://funnelkit.com/funnelkit-vs-checkoutwc/ · https://www.checkoutwc.com/funnelkit-vs-checkoutwc
- WP Rocket : https://docs.wp-rocket.me/article/1491-using-wp-rocket-on-your-woocommerce-site
- Wordfence : https://wordpress.org/plugins/wordfence/
- Traduction : https://wpml.org/home/best-wordpress-translation-plugin/ · https://www.businessbloomer.com/choosing-a-multilingual-solution-for-woocommerce-translatepress-vs-polylang/
- Rétractation : https://wordpress.org/plugins/wt-eu-withdrawal-button/
- Cartes cadeaux : https://wordpress.org/plugins/pw-woocommerce-gift-cards/
- Nelio : https://wordpress.org/plugins/nelio-ab-testing/
- Avis photo : https://wordpress.org/plugins/woo-photo-reviews/ · WiserReview : https://wordpress.org/plugins/wiser-review/ · Trustpilot : https://wordpress.org/plugins/trustpilot-reviews
