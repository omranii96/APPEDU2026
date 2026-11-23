# CHARMED PARIS — Plan de mesure, KPI et tests A/B (FR + EN)

> Version du 23/11/2026. Outils : GA4, Pixel Manager for WooCommerce (Pro), Complianz, Meta Pixel + Conversions API, TikTok Pixel + Events API, tag Pinterest + API, Brevo. Cf. `stack-plugins.md`.

---

## 1. Conventions communes (à respecter sur toutes les plateformes)

| Règle | Valeur |
|---|---|
| `value` envoyée aux plateformes | **CA HT des produits, après remises, hors frais de port** (ex. duo 110,65 € TTC → `value = 92,21`). C'est la base des ROAS seuils « valeur HT produits » de `offres-et-panier-moyen.md` |
| `currency` | Devise réelle de la commande (`EUR`, plus tard `USD`). Ne jamais convertir côté tag |
| `item_id` | **SKU Branvas** (`JSGRQR`…), identique dans GA4, Meta, TikTok, Pinterest et les flux catalogue (pas d'EAN [fait]) |
| `item_category` | Univers : `Sculpture`, `Eclat`, `Couleur precieuse`, `Joaillerie 925`, `Mixte`, `Homme` |
| `item_variant` | Vide (parures = produits simples) |
| `transaction_id` | Numéro de commande WooCommerce. Aussi utilisé comme **`event_id`** pour le dédoublonnage navigateur/serveur |
| Langue | Paramètre `site_language` (`fr` / `en`) sur **tous** les événements + dimension personnalisée GA4 (portée événement) ; propriété utilisateur `langue_preferee` |
| Marché | `market` = pays de livraison (`FR`, `BE`, `US`…) sur `add_shipping_info` et `purchase` |
| Offres | `coupon` (code bienvenue) ; `promotion_id = "2e_parure_15"` quand la remise s'applique |
| Exclusions | Filtrer les IP internes et les commandes test (statut, e-mail interne) ; ne pas compter les commandes en échec/annulées |

---

## 2. GA4 : événements e-commerce (recommandés par Google)

| Événement | Déclencheur | Paramètres clés |
|---|---|---|
| `view_item_list` | Affichage d'une grille univers, de la file des parures, des suggestions | `item_list_id` (`univers_eclat`, `file_parures`, `cross_sell_minipanier`…), `items[]` |
| `select_item` | Clic sur une carte produit | `item_list_id`, `items[0]` |
| `view_item` | Fiche produit | `items[0]`, `value`, `currency`, `site_language` |
| `add_to_cart` | Ajout (fiche, carte rapide, coffret, mini-panier) | `items[]`, `value`, **`source_ajout`** (`fiche`, `carte`, `coffret`, `file`, `minipanier_suggestion`, `sticky`) |
| `remove_from_cart` | Suppression | `items[]` |
| `view_cart` | Ouverture du mini-panier ou de la page panier | `value`, `items[]`, `seuil_atteint` (bool) |
| `view_promotion` / `select_promotion` | Bloc « 2e parure −15 % » vu / cliqué | `promotion_id="2e_parure_15"`, `creative_slot` (`fiche`, `minipanier`) |
| `begin_checkout` | Clic sur « Commander » ou sur un bouton express | `value`, `items[]`, `coupon`, `methode` (`standard`, `apple_pay`, `google_pay`, `paypal`) |
| `add_shipping_info` | Adresse validée | `shipping_tier="DHL standard"`, `market` |
| `add_payment_info` | Moyen de paiement choisi | `payment_type` (`card`, `paypal`, `paypal_4x`, `apple_pay`, `google_pay`) |
| `purchase` | Page merci **+ côté serveur** (Measurement Protocol, Pixel Manager Pro) au passage à « En cours » | `transaction_id`, `value`, `tax`, `shipping`, `currency`, `coupon`, `items[]`, `market`, `site_language` |
| `refund` | Remboursement (rétractation) dans WooCommerce | `transaction_id`, `value` (total ou partiel), `items[]` |
| `sign_up` / `generate_lead` | Inscription newsletter (après double opt-in) | `method` (`popup`, `footer`, `checkout`), `offre` (`livraison_offerte` / `moins_10`) |
| `search` | Recherche FiboSearch | `search_term` |

## 3. GA4 : événements spécifiques CHARMED PARIS

| Événement | Déclencheur | Paramètres | Question à laquelle il répond |
|---|---|---|---|
| `intro_progression` | 25 / 50 / 75 / 100 % du scroll de l'intro | `pourcentage`, `device_category` | Où les visiteuses décrochent-elles dans l'intro ? |
| **`intro_passee`** | Sortie de l'intro | `method` (`bouton`, `cta_voir_parures`, `scroll_fin`, `auto_pub`, `retour_visite`, `reduced_motion`, `connexion_lente`), `pourcentage_vu`, `duree_s` | L'intro aide-t-elle ou freine-t-elle ? (comparer le taux d'ajout au panier par `method`) |
| **`coffret_ouvert`** | Un coffret du carrousel s'ouvre (arrive devant) | `item_id`, `position`, `interaction` (`drag`, `fleche`, `point`, `auto`), `index_session` (n-ième coffret ouvert) | Quels coffrets intriguent ? Après combien d'ouvertures la visiteuse ajoute-t-elle au panier ? |
| `coffret_ajout` | « Ajouter » depuis un coffret ouvert | `item_id`, `position` | (complète `add_to_cart` avec `source_ajout=coffret`) |
| **`vue_file_parures`** | La section `#pieces` entre à 50 % dans l'écran | `vue` (`une`, `file`, `toutes`) | La file est-elle vue ? Quelle vue convertit le mieux ? |
| `file_changement_vue` | Clic sur Une / La file / Toutes | `de`, `vers` | Préférence des visiteuses (test n°8) |
| `file_focus_parure` | Une parure passe au focus avec l'étiquette ticket | `item_id`, `rang` | Intérêt produit sans clic |
| `seuil_livraison_atteint` | Le panier passe à « Livraison offerte » | `value`, `declencheur` (`2_parures`, `montant`) | Efficacité de la règle « dès 2 parures » |
| `delai_affiche` | Ligne de délai estimé visible sur la fiche | `fourchette` (ex. `4-9`), `noel_avant_limite` (bool) | Effet de la transparence sur le délai |
| `langue_changee` | Clic FR ↔ EN | `de`, `vers`, `page_type` | Besoin réel de la version EN |
| `faq_ouverte` | Ouverture d'un accordéon (fiche, FAQ) | `question_id` | Objections principales (alimente les fiches) |
| `retractation_demandee` | Envoi du formulaire / bouton de rétractation | `transaction_id`, `motif` (facultatif) | Taux de rétractation réel par SKU |

**Conversions clés GA4** : `purchase`, `add_to_cart`, `begin_checkout`, `sign_up`.
**Dimensions personnalisées** : `site_language`, `market`, `source_ajout`, `method` (intro), `vue`, `promotion_id`.
**Explorations à créer** : entonnoir (view_item → add_to_cart → begin_checkout → add_shipping_info → add_payment_info → purchase) **séparé par `site_language` et `device_category`** ; chemin accueil `intro_passee` → `coffret_ouvert` → `add_to_cart` ; performance par `item_id` (vues, ajouts, achats, rétractations).

---

## 4. Meta Pixel + Conversions API

| Point | Configuration |
|---|---|
| Outil | Pixel Manager Pro (navigateur + serveur). Pixel de « Meta for WooCommerce » **désactivé** (catalogue seulement) |
| Événements | `PageView`, `ViewContent`, `AddToCart`, `InitiateCheckout`, `AddPaymentInfo`, `Purchase`, `Lead` (newsletter) ; personnalisé : `CoffretOuvert` (audience de reciblage chaud) |
| Dédoublonnage | Même `event_id` côté navigateur et côté serveur (`transaction_id` pour `Purchase`, UUID pour les autres) |
| Correspondance avancée | E-mail, téléphone, prénom, nom, ville, code postal, pays **hachés (SHA-256)**, `fbp`/`fbc`, IP et user agent : **uniquement si consentement marketing** |
| Consentement | **Aucun appel (navigateur ou serveur) sans consentement « marketing »** dans l'UE. Les envois côté serveur restent soumis au consentement (CNIL) : Pixel Manager doit lire le statut Complianz |
| Catalogue | Flux Meta (SKU = `item_id`) ; 2 catalogues ou 1 catalogue avec langue/devise par pays pour l'EN |
| Qualité | Event Match Quality ≥ 6 sur `Purchase` [hyp. : cible] ; écart Meta/WooCommerce ≤ 20 % (sur les commandes consenties) |
| Campagnes | Ensembles de publicités séparés FR / EN ; exclure les acheteuses des 30 derniers jours de la prospection |

## 5. TikTok et Pinterest

| Plateforme | Événements | Notes |
|---|---|---|
| TikTok Pixel + Events API (Pixel Manager Pro) | `ViewContent`, `AddToCart`, `InitiateCheckout`, `AddPaymentInfo`, `CompletePayment` (`event_id` dédoublonné), `Subscribe` | Paramètre `ttclid` conservé. Plugin TikTok officiel : pubs et catalogue seulement (Shop arrêté depuis le 01/06/2026) |
| Pinterest Tag + Conversions API | `pagevisit`, `addtocart`, `checkout`, `signup` | Catalogue via Pinterest for WooCommerce ; `epik` conservé ; audience « Idées cadeaux » |

## 6. Consentement (Consent Mode v2, CNIL)

| Élément | Réglage |
|---|---|
| CMP | Complianz, bannière FR/EN, boutons **« Tout accepter » / « Tout refuser » de même poids** et « Personnaliser » ; aucune case précochée ; refus aussi simple que l'acceptation ; reconsentement à 6 mois [hyp. pratique CNIL courante] |
| Valeurs par défaut (EEE + UK + CH) | `ad_storage=denied`, `ad_user_data=denied`, `ad_personalization=denied`, `analytics_storage=denied`, `functionality_storage=granted`, `security_storage=granted`, `wait_for_update=500` |
| Mode | **Consent Mode v2 avancé** pour Google (pings sans cookie avant consentement, modélisation), ou **basique** si le conseil juridique le préfère [à valider] |
| US (EN) | Région US : opt-out possible (Complianz Premium, géolocalisation) [à vérifier selon les États] |
| Non-Google | Meta, TikTok, Pinterest : **bloqués** tant que le consentement marketing n'est pas donné (pas d'équivalent Consent Mode) |
| Mesure d'audience exemptée | Option : outil configuré selon l'exemption CNIL (ex. Matomo en mode exempté) pour garder une vision des sessions même en cas de refus [à vérifier] |
| Contrôle | Tag Assistant + débogage Consent Mode ; vérifier qu'aucun cookie `_fbp`, `_ttp` ou `_ga` n'est posé avant l'acceptation |
| KPI | Taux d'acceptation (FR / EN) : sert à corriger les chiffres des plateformes |

---

## 7. KPI cibles et seuils d'alerte

> Cibles = **hypothèses de départ** pour une marque nouvelle de bijoux en dropshipping, à recaler après 4 semaines de données réelles. Aucun de ces chiffres ne doit apparaître sur le site.

| KPI | Cible [hyp.] | Alerte | Action si alerte |
|---|---|---|---|
| Taux de conversion session → achat (global) | 1,5 % | < 0,8 % sur 7 j | Vérifier le tracking, puis l'entonnoir étape par étape |
| Ajout au panier / session | 6–8 % | < 4 % | Fiche : photos, prix, délai |
| Checkout commencé / ajout au panier | 45 % | < 30 % | Mini-panier : port, surprise sur le délai |
| Achat / checkout commencé | ≥ 55 % | < 40 % | Champs, paiement, erreurs |
| Sessions accueil qui atteignent `#coffrets` | ≥ 60 % | < 35 % | Raccourcir l'intro (test n°1) |
| Part de paniers à 2 parures ou plus | 20 % (25 % à Noël) | < 10 % | Mini-panier, suggestions |
| Panier moyen TTC | ≥ 85 € (référence actuelle ≈ 72 €) | < 70 € | Offres (§4–6 de `offres-et-panier-moyen.md`) |
| **CPA réel (par plateforme)** | ≤ CPA max du mix vendu (≈ 26–31 €) | > CPA max pendant 3 j avec plus de 10 achats | Couper ou réduire l'ensemble de publicités |
| ROAS (valeur HT produits) | ≥ 2,9 (mix) | < 2,4 | Idem |
| MER (CA total / dépenses pub) | ≥ 3,5 | < 2,8 | Revoir le budget |
| Taux de rétractation | ≤ 8 % | > 12 % sur 30 j, ou > 20 % sur un SKU | Fiche (photos, dimensions), retirer le SKU |
| Réclamations défaut/casse sous 10 j | ≤ 2 % | > 4 % | Remonter à Branvas (photos), suspendre le SKU |
| Délai réel commande → livraison (FR) | ≤ 9 j ouvrés pour 90 % | > 10 % de colis au-delà de 9 j | Mettre à jour le texte de délai (honnêteté) |
| Taux d'échec de paiement | < 5 % | > 10 % | Passerelle, 3-D Secure |
| E-mails : inscription / session | 2–3 % | < 1 % | Offre de bienvenue |
| Panier abandonné récupéré | 5–10 % des paniers relancés | < 3 % | Contenu et timing des relances |
| LCP mobile (fiche) | < 2,5 s | > 3 s | Images, JS |
| Écart achats GA4 / WooCommerce | ≤ 15 % (après consentement) | > 25 %, ou 0 achat GA4 en 24 h avec ≥ 1 commande | **Tracking cassé** : bloquer les décisions pub |
| Écart CA EN / FR | Suivi | — | Arbitrer les budgets par langue |

**Alertes automatiques** : GA4 (Insights personnalisés) sur `purchase = 0` en 24 h, chute de 50 % de `add_to_cart` jour sur jour, hausse des `refund`. Rapport hebdomadaire séparé FR / EN.

---

## 8. Tests A/B : 10 tests priorisés (méthode ICE)

**ICE** = Impact × Confiance × Facilité, chaque critère noté sur 10 ; score = moyenne.

### Taille d'échantillon (calcul)
Formule approchée (risque α = 5 %, puissance 80 %) : `n par variante ≈ 16 × p × (1 − p) / δ²`.
| Métrique de base | p | Effet minimal détectable (relatif) | δ | **n par variante** |
|---|---|---|---|---|
| Achat / session | 1,5 % | +20 % | 0,3 pt | **≈ 26 300 sessions** |
| Ajout au panier / session | 7 % | +20 % | 1,4 pt | **≈ 5 300 sessions** |
| Passage à 2 parures / panier | 15 % | +20 % | 3 pt | **≈ 2 270 paniers** |

→ Au lancement (quelques milliers de sessions par mois [hyp.]), **tester sur des micro-conversions** (ajout au panier, clic, passage à 2 parures), en périodes de 2 semaines minimum, avec 1 test par page à la fois. Les tests de prix et de livraison se font **par périodes successives**, pas en séparant les visiteuses en même temps.

| # | Test | Hypothèse | Métrique principale | Garde-fou | I | C | E | **ICE** |
|---|---|---|---|---|---|---|---|---|
| 1 | **Intro courte (≤ 150vh mobile, « Passer » visible) vs intro actuelle (520vh)** | Moins de scroll avant le produit = plus de visites des coffrets et de la file, sans perte d'image | % des sessions accueil qui atteignent `#coffrets` ; `add_to_cart` / session accueil | Temps passé, `coffret_ouvert` | 8 | 8 | 7 | **7,7** |
| 2 | **Pub vers fiche produit vs pub vers `/lp/ouvre/`** (test A/B dans le gestionnaire de pubs Meta) | La fiche convertit mieux pour les pubs produit ; la LP convertit mieux pour les pubs « univers » | CPA, taux d'achat | Taux de rebond | 9 | 7 | 8 | **8,0** |
| 3 | Bouton **« Ajouter au panier » vs « Ajouter à l'écrin »** | Le libellé standard est plus clair et augmente les ajouts ; « écrin » renforce la marque sans gain | `add_to_cart` / `view_item` | — | 5 | 6 | 10 | **7,0** |
| 4 | **Mini-panier : suggestions « 2e à −15 % » avec prix remisé affiché vs suggestions sans prix remisé** | Montrer « 58,65 € dans ton écrin » augmente le passage à 2 parures | % de paniers à 2 parures ou plus ; marge par session | Taux de checkout | 8 | 7 | 7 | **7,3** |
| 5 | **Livraison offerte dès 2 parures / 89 € vs livraison offerte partout** (périodes successives) | Le seuil augmente le panier moyen davantage qu'il ne fait baisser la conversion | **Marge de contribution par session** | Taux d'achat, abandon au mini-panier | 9 | 6 | 6 | **7,0** |
| 6 | **Ligne « Livraison estimée entre le X et le Y » vs « 4 à 9 jours ouvrés »** | Une date concrète rassure et augmente l'ajout au panier | `add_to_cart` / `view_item` | Contacts SAV « où est ma commande » | 6 | 7 | 8 | **7,0** |
| 7 | **Boutons Apple Pay / Google Pay sur la fiche vs seulement au mini-panier et au checkout** | L'express sur fiche accélère l'achat mobile, mais court-circuite le duo | Taux d'achat mobile | Part de duos, panier moyen | 7 | 5 | 8 | **6,7** |
| 8 | **Vue « Toutes » (grille) par défaut sur mobile vs vue « La file »** | La grille fait comparer plus vite et augmente les clics produit | `select_item` / `vue_file_parures` | `file_focus_parure` | 6 | 6 | 9 | **7,0** |
| 9 | **1re photo de la fiche : portée (mannequin) vs packshot détouré vs coffret ouvert** | La photo portée donne l'échelle et réduit l'incertitude (et les retours) | `add_to_cart` / `view_item` ; taux de rétractation à 30 j | CTR des pubs (mêmes visuels) | 7 | 6 | 7 | **6,7** |
| 10 | **Offre de bienvenue « livraison offerte » vs « −10 % »** (périodes successives) | La livraison offerte coûte moins (−3,57 € contre −5,03 € par commande) pour un taux d'inscription proche | Inscriptions/session × taux d'achat des inscrites × marge | Désinscriptions | 7 | 6 | 8 | **7,0** |

**Ordre de lancement** : 2 (dans Meta, sans outil de test sur le site) → 1 → 4 → 3 → 8 → 6 → 5 → 10 → 9 → 7.
**Règles** : hypothèse écrite avant le lancement, durée fixée à l'avance (au moins 2 cycles hebdomadaires), pas d'arrêt anticipé quand ça « a l'air de gagner », résultats séparés FR / EN et mobile / desktop, et jamais de variante qui enfreint le brief (urgence, rareté ou avis inventés ; case précochée).

---

## 9. Recette du tracking (avant chaque mise en ligne)

1. Mode aperçu GA4 (DebugView) + Meta Test Events + TikTok Test Events.
2. Parcours complet FR **et** EN : refus des cookies → aucun pixel ; acceptation → tous les événements, paramètres `site_language`, `currency`, `item_id` = SKU.
3. Commande test (WooPayments en mode test) : **1 seul** `purchase` dans GA4, 1 seul `Purchase` dédoublonné dans Meta, valeur = HT produits.
4. Rechargement de la page merci : pas de 2e `purchase`.
5. Remboursement test : `refund` remonté.
6. Commande test sur `/en/` : visible dans Branvas, suivi synchronisé, événements avec `site_language=en`.
