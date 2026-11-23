# CHARMED PARIS — spécification d'installation (WordPress + WooCommerce + Branvas)

Version du 23/11/2026. Sources : `woocommerce/BRIEF.md` (décisions arrêtées), `woocommerce/source/FAITS-BRANVAS.md`
(prioritaire sur le brief), FAQ Branvas (`woocommerce/source/branvas-faq/`, articles 13284375, 18510887, 18321590,
12241419, 12241434, 12872188, 16207436, 18511443, 16207660), `woocommerce/legal/`, `woocommerce/contenus/notes.md`.
Tout ce qui n'est pas vérifié est marqué **À CONFIRMER**.

Thème : `woocommerce/theme/charmed-paris/` (README du thème pour le détail des blocs et réglages).

---

## 1. Hébergement recommandé

**Exigences**

| Poste | Exigence | Pourquoi |
|---|---|---|
| Localisation | Serveurs en **France ou UE**, contrat de sous-traitance RGPD (DPA) | RGPD, latence FR |
| PHP | **8.2 ou 8.3**, OPcache activé, `memory_limit` ≥ 256M, `max_execution_time` ≥ 120 s | Woo 9+/10, imports |
| Base | MySQL 8 ou MariaDB ≥ 10.6 | HPOS (tables de commandes) |
| HTTPS | Certificat (Let's Encrypt suffit), HTTP/2 ou HTTP/3, redirection 301 http→https, HSTS | **Obligatoire pour Branvas** (API REST) et le paiement |
| Cache objet | **Redis** (ou Memcached) persistant + plugin « Redis Object Cache » | panier, sessions, requêtes produits |
| Cache de page | Cache serveur (LiteSpeed, Nginx FastCGI, Varnish) avec exclusions Woo (§ 9) | TTFB |
| Cron | WP-Cron désactivé (`DISABLE_WP_CRON`) + vraie tâche cron toutes les 5 min | e-mails, Action Scheduler Woo, synchro |
| Outils | SSH + WP-CLI, préproduction en un clic, sauvegardes quotidiennes hors site (UE) | § 7–8 |
| E-mail | Ne pas envoyer depuis le serveur web : SMTP transactionnel (Brevo, FR) | délivrabilité du suivi colis |

**Hébergeurs adaptés (à comparer, tarifs non vérifiés)** : o2switch (FR, mutualisé performant, LiteSpeed + Redis),
OVHcloud Web Cloud « Performance » ou VPS managé (FR), Kinsta ou Cloudways sur datacenter Paris / Francfort
(Google Cloud europe-west9, AWS eu-west-3) si budget plus élevé. Éviter les offres mutualisées d'entrée de gamme sans
Redis ni SSH.

---

## 2. Installation pas à pas

### 2.1 WordPress
1. Créer la base (utf8mb4), installer WordPress **en français**, compte admin nominatif (pas « admin »), e-mail du domaine.
2. **Réglages > Général** : titre « CHARMED PARIS », slogan « Ouvre. Laisse-toi charmer. », **fuseau horaire Europe/Paris**
   (les dates de Noël du thème en dépendent), format de date `j F Y`.
3. **Réglages > Permaliens** : « Titre de la publication » (`/%postname%/`). Obligatoire : l'API REST utilisée par
   Branvas ne fonctionne pas avec les permaliens « simples ». Base produit : `/parure/` ; base catégorie : `/parures/`
   (cohérent avec `woocommerce/seo/architecture.md` — **à aligner** avec le SEO s'il a fixé autre chose).
4. **Réglages > Lecture** : « Demander aux moteurs de ne pas indexer » **coché jusqu'au lancement**, décoché le jour J.
5. `wp-config.php` : `define('DISALLOW_FILE_EDIT', true); define('WP_POST_REVISIONS', 10); define('DISABLE_WP_CRON', true);`
   + clés de sel régénérées.

### 2.2 WooCommerce
Installer WooCommerce (dernière 9.x/10.x), passer l'assistant sans installer les extensions proposées. Activer
**HPOS** (Woo > Réglages > Avancé > Fonctionnalités, par défaut sur une installation neuve).

**Général**
- Adresse de la boutique : **ton adresse professionnelle** (jamais celle de Branvas, FAQ 16207417).
- Vendre : **à des pays spécifiques → France** au lancement. Livrer : vers les pays de vente.
  Extension UE plus tard uniquement vers des pays de la liste Branvas (FAQ 12241419 : Monaco, Guadeloupe, Guyane,
  Mayotte ne sont **pas** desservis ; La Réunion et la Martinique le sont). Royaume-Uni : **ne pas ouvrir** avant
  immatriculation TVA UK (et la ligne 925 y est exclue, poinçon obligatoire).
- Devise **Euro (€)**, position « Droite avec espace », séparateur des milliers espace, décimal virgule, 2 décimales.
  EUR uniquement au lancement (décision du 23/11).

**Taxes** (cocher « Activer les taxes » dans Général)
- « Oui, je saisirai les prix **TTC** ». Calcul selon l'**adresse de livraison**. Classe d'expédition : selon les articles.
- Arrondi au niveau du sous-total : oui. Afficher les prix **TTC** en boutique et au panier, suffixe « TTC ».
  Totaux : « en tant que total unique ».
- Taux standard : FR, 20 %, nom « TVA », **Livraison cochée** (la livraison suit le taux du bien).
- Ventes UE > 10 000 €/an : guichet **OSS** et taux de chaque pays (import CSV des taux) — **à valider avec le comptable**.
  Import (droits + TVA import) payé par Branvas (DDP), pas d'IOSS à fournir.

**Expédition** (un seul service Branvas : **pas d'express, pas de date garantie**)
- Zone « France » (FR ; ajouter « Réunion » et « Martinique » seulement si vous les ouvrez à la vente).
  1. Méthode **Forfait** : libellé « Livraison suivie », statut fiscal « Taxable », coût **4.0833** (HT, saisi HT par
     WooCommerce) → **4,90 € TTC** affiché (décision du 23/11, configurable).
  2. Méthode **Livraison gratuite** : libellé « Livraison offerte », « Nécessite… » = **Un montant minimum de commande**,
     **50 €**, « Appliquer le minimum avant remise du coupon » décoché.
- Zone « Reste du monde » : **aucune méthode** (les pays non desservis ne peuvent pas commander).
- Le thème (WooCommerce > Réglages > Produits > CHARMED PARIS) : recalcule le seuil **après la remise 2e parure**,
  **masque le forfait** quand la livraison est offerte, lit le seuil pour les textes (bandeau, fiches, réassurance) et
  affiche le délai réel **4–9 jours ouvrés** (France, 90 % des colis, commande → livraison).
- Coût réel Branvas : 8,99 $ par commande (y compris DDP et packaging), deux commandes = deux colis.
  Règle Branvas : seuil 20–30 % au-dessus du panier moyen → **réévaluer le seuil après 4 semaines de ventes**.

**Paiements** : WooPayments ou Stripe (CB, Apple Pay, Google Pay) + PayPal Payments. Mode test pendant la recette.
Vérifier en préproduction que la remise « 2e parure » (frais négatif) est bien transmise à PayPal (lignes de commande)
et que la commande passe en **En cours** (seules les commandes payées « En cours » partent chez Branvas).
Pas de virement / chèque au lancement (statut « En attente » non synchronisé tant qu'on ne le change pas à la main).

**Comptes et confidentialité** : commande sans compte autorisée ; création de compte au paiement facultative ; page
de confidentialité = `woocommerce/legal/politique-confidentialite.md` ; conservation des commandes 10 ans (comptabilité).

**E-mails** : expéditeur « CHARMED PARIS », adresse du domaine (ex. `bonjour@…`), SMTP Brevo (plugin WP Mail SMTP ou
Brevo), enregistrements **SPF, DKIM, DMARC**. Couleurs : base #7A1F3A, fond #F4F2F5. Vérifier les modèles :
« Commande en cours », « Commande terminée » (= « ta commande est en route » : Branvas passe la commande en Terminée
avec le suivi), « Note client » (utilisée par Branvas pour le suivi si aucun plugin de suivi), « Remboursement ».

**Avancé** : pages Panier / Commande / Mon compte / **Conditions générales** (CGV de `woocommerce/legal/cgv.md`).
Dans le bloc Paiement, activer la case « J'accepte les CGV » ; vérifier que le bouton final affiche
« **Commander avec obligation de paiement** » (le thème le force ; le libellé du bloc peut aussi être saisi dans
l'éditeur par sécurité). Téléphone : **obligatoire** (forcé par le thème, exigence Branvas hors US/UK).

**Produits** : unités g / cm ; **avis activés, réservés aux « propriétaires vérifiés »**, libellé « acheteuse vérifiée »
(forcé par le thème ; demande d'avis post-livraison envoyée par Brevo ; pas de Judge.me). **Gestion du stock activée**
(Branvas synchronise : **ne jamais modifier les quantités**, valeur fictive type 1000, rupture = 0) ; affichage du
stock « Ne jamais afficher la quantité » (forcé par le thème) ; « Masquer les articles en rupture » : oui.
Aucun prix promo au lancement (pas de prix barré : thème + règle L112-1-1). Pas d'EAN/GTIN (Branvas n'en fournit pas) :
laisser le champ GTIN vide.

### 2.3 Thème et extensions
1. Téléverser et activer le thème `charmed-paris` (voir son README). Copier `inc/withdrawal.php` en mu-plugin.
2. Réglages du thème : WooCommerce > Réglages > Produits > **CHARMED PARIS** ; Avancé > **Rétractation** → « Créer la page ».
3. Extensions minimales :
   - **TranslatePress** (Personal, SEO Pack) — § 3 ;
   - **Advanced Shipment Tracking** (gratuit) — Branvas y écrit le suivi (FAQ 18321590), sinon note client ;
   - Redis Object Cache, plugin de cache du serveur (LiteSpeed Cache si LiteSpeed) ;
   - WP Mail SMTP ou Brevo (SMTP + formulaires) ; brancher la newsletter du thème sur l'action
     `charmed_newsletter_subscribe` (double opt-in, listes FR/EN) ;
   - bannière cookies conforme CNIL (refus aussi simple que l'acceptation) ; SEO (Yoast / Rank Math, cf. `woocommerce/seo/`) ;
   - sécurité : 2FA (WP 2FA ou équivalent).
   Rien d'autre sans besoin précis (chaque extension coûte en performance).

---

## 3. Bilingue FR / EN — TranslatePress (décision arrêtée)

**Pourquoi TranslatePress et pas WPML / Polylang** : WPML et Polylang créent **un produit WooCommerce par langue**
(IDs différents). Branvas lie ses commandes à **ses** produits : une commande passée sur le doublon anglais risque de ne
jamais remonter (la FAQ 16207660 : dupliquer un produit casse le lien de synchro) et le stock synchronisé ne
s'appliquerait qu'à l'original. TranslatePress traduit **le même produit** (un seul ID, un seul stock), slugs et
métadonnées compris (SEO Pack), et gère hreflang + sitemap multilingue.

1. Installer TranslatePress + licence Personal (SEO Pack inclus, ≈ 99 €/an, **tarif à confirmer**).
2. Langue par défaut **Français**, langue secondaire **English (en_US ou en_GB)**, sous-répertoire `/en/`,
   « Utiliser un sous-répertoire pour la langue par défaut » : non.
3. SEO Pack : traduire les slugs (produits, catégories, pages), vérifier les balises `hreflang` (fr, en, x-default → fr)
   et le sitemap.
4. Le thème est traduit par gettext (`languages/en_US.mo`, `en_GB.mo`) ; le sélecteur FR · EN est déjà dans l'en-tête
   (bloc `charmed/language-switcher`, il appelle `trp_custom_language_switcher()`).
5. Traduire les contenus dans l'éditeur visuel TranslatePress à partir de `woocommerce/contenus/*-en.*`
   (fiches, pages, microcopy). **Ne pas importer `produits-woocommerce-en.csv` avec l'importateur Woo** (même SKU : il
   écraserait le français).
6. **Test obligatoire** : passer une commande depuis `/en/` (mode test + Auto-Fulfillment Branvas coupé, § 4.4) et
   vérifier qu'elle remonte dans Branvas « Customer Orders » avec le bon produit. Vérifier aussi la langue des e-mails
   Woo envoyés à une cliente anglophone (**à confirmer** selon l'offre TranslatePress).

---

## 4. Connexion Branvas

### 4.1 Prérequis
- Offre Branvas **payante** (Growth 29 $/mois ≥ 75 produits ; la publication vers une boutique connectée exige une offre
  payante ; la fin d'essai **dépublie** les produits, FAQ 16207498).
- Logo téléversé et **approuvé** (sinon colis neutres).
- Site en **HTTPS**, permaliens jolis, API REST joignable : `https://ton-domaine/wp-json/wc/v3/` ne doit pas être bloquée
  par un pare-feu, Cloudflare (règle « skip » pour `/wp-json/wc/`), un plugin de sécurité ou une protection par mot de
  passe du site. En préproduction protégée par mot de passe HTTP, la connexion échouera.

### 4.2 Connecter (FAQ 18510887 — étapes exactes)
1. Se connecter sur **branvas.com**.
2. Ouvrir l'onglet **Connect Store**.
3. Choisir **WooCommerce** et suivre les instructions pour connecter la boutique. Intégration par **clé API REST
   (lecture/écriture)**, **aucun plugin à installer**, aucune validation à attendre.
   - Si Branvas demande de saisir des clés : WooCommerce > Réglages > Avancé > **API REST** > Ajouter une clé :
     description « Branvas », utilisateur **dédié** (compte `branvas-api`, rôle Gestionnaire de boutique), droits
     **Lecture/Écriture** ; copier Consumer key / Consumer secret dans Branvas (ils ne sont affichés qu'une fois).
   - Si Branvas redirige vers l'écran d'autorisation WooCommerce : se connecter avec ce même compte dédié et approuver.
   - (Le mode exact — saisie ou redirection — est **à confirmer** à la connexion.)
4. Succès = statut **« Connected » vert**. S'il ne passe pas au vert : cliquer à nouveau Connect (inutile de déconnecter),
   puis support Branvas (FAQ 16207570).

### 4.3 Produits (FAQ 13284375)
1. **Catalog** → « Add to My Products » sur les **30 SKU** sélectionnés (`branvas-photos/bundles.csv`, `selection_charmed = oui`).
2. **Product Listing** (FAQ 15606591) : langue **français**, devise **EUR**, style de description, SEO (désactiver les
   méta Branvas si le SEO fournit les siennes), fond **ivoire**.
3. **My Products** → « Edit Listing » : prix de vente (`woocommerce/contenus/notes.md`, **après contrôle de marge**),
   titre, description, matières, images → bouton **sync**.
4. Toggle **Publish to Store** (ou sélection multiple → Actions → Publish).
5. Dans WooCommerce, vérifier : produits créés en natif (simples ou variables), **SKU = SKU Branvas `JS…`**, images,
   poids, stock. **Ne jamais dupliquer ni recréer un produit Branvas dans Woo** (casse la synchro des commandes).

### 4.4 Commandes, suivi, test
- Seules les commandes **payées** (statut **En cours**) partent chez Branvas ; elles y apparaissent en « Payment needed »
  puis sont payées par toi (ou automatiquement si **Auto-Fulfillment** est actif).
- **Test avant lancement (FAQ 18511443)** : couper **Auto-Fulfillment** (Customer Orders) → passer une commande test
  payée → vérifier qu'elle apparaît dans Branvas (produit, quantité, adresse, **téléphone**) → l'annuler dans Woo,
  ne pas la payer dans Branvas. Puis commander **un échantillon à ton adresse** pour juger le packaging réel.
- Suivi : avec Advanced Shipment Tracking, Branvas écrit le transporteur + numéro dans la commande et passe la commande en
  **Terminée** (= « en route ») ; l'e-mail « Commande terminée » contient le suivi. Sans plugin : note client (e-mail).
- Retours : **gérés par toi** (Branvas ne couvre que colis endommagé / défaut / erreur, réclamation sous 10 jours avec
  photos). Rétractation 14 jours et garantie légale 2 ans à ta charge : prévoir une **adresse de retour en France**.
  Le formulaire de rétractation en ligne du thème (L221-21) envoie la demande, horodate l'accusé de réception et l'inscrit
  en note de commande ; **libellés exacts à vérifier dans le décret 2026-3** (réglages Avancé > Rétractation).

### 4.5 Expédition côté Branvas
Branvas facture 8,99 $ par commande quel que soit le tarif client. Le réglage « Connect Store → Change (shipping rate) »
est documenté pour Shopify ; pour WooCommerce, **à confirmer** s'il crée ou modifie des zones Woo. Si oui, le
remplacer par la configuration du § 2.2 et revérifier après chaque « Save and publish to store ».

---

## 5. Import et enrichissement des produits

Ordre impératif :
1. **Branvas crée les produits** (§ 4.3) — jamais l'inverse.
2. Contrôler les SKU et créer les catégories univers selon `woocommerce/seo/architecture.md` (base de catégorie
   `parures`) : slugs `sculpture`, `eclat`, `couleur-precieuse`, `joaillerie-argent-925`, `mixte` (lus par le bloc
   Univers ; images de catégorie à téléverser, sinon images de repli du thème) + catégories cadeaux. Écart à trancher :
   `contenus/notes.md` prévoit une catégorie parente « Parures > … » ; le bloc fonctionne dans les deux cas.
3. **Titres et descriptions FR** depuis `woocommerce/contenus/` (fiches-produits.md, produits-woocommerce.csv).
   **Attention** : la FAQ Branvas (13284375, 16207660) indique que les données produit vont **dans un seul sens**,
   Branvas → boutique, et **écrasent** les modifications faites côté boutique. Deux options :
   - **A (recommandée, sans risque)** : coller titres, descriptions et SEO dans Branvas « Edit Listing », puis sync ;
   - **B** : import CSV Woo « Mettre à jour les produits existants » (correspondance SKU, colonne Images = « Ne pas
     importer »), comme décrit dans `contenus/notes.md` — **uniquement après un test en préproduction** : modifier un
     produit dans Woo, relancer une sync Branvas, vérifier ce qui est écrasé (titre, description, catégories, champs
     `_charmed_*`). **À CONFIRMER** avant de généraliser.
4. Champs du thème par produit (onglet Général) : image détourée (téléverser `charmed-paris/cut/*.webp`, noter l'ID),
   ligne courte, code étiquette, composition. Ces métadonnées ne sont pas gérées par Branvas : survie à la sync **à
   confirmer** au même test.
5. Anglais : TranslatePress (§ 3). 6. Contrôle légal des textes (dorure, oxyde de zirconium, moissanite synthétique,
   « à garder au sec », aucun « waterproof », aucun « sans nickel » sans rapport) : `woocommerce/legal/points-de-vigilance.md`.
7. Google Merchant Center : marque « CHARMED PARIS » + MPN = SKU (le thème les ajoute au JSON-LD), pas de GTIN
   (« identifier_exists = no » pour la marque propre) ; délai de livraison FR 4–9 jours ouvrés, livraison 4,90 € / offerte
   dès 50 €, retours conformes aux CGV.

---

## 6. Accueil et pages

- L'accueil utilise `templates/front-page.html` (sections de la maquette, intro 260vh desktop / 170vh mobile avec
  « Passer l'intro », pas d'intro pour le trafic publicitaire `utm_* / gclid / fbclid`, ni pour « réduire les animations »).
- Pages à créer (slugs utilisés par le pied de page) : `livraison`, `retours-et-retractation`, `entretien`, `contact`,
  `cgv`, `mentions-legales`, `cookies`, politique de confidentialité (réglage WP), `retractation` (créée par le thème).
  Textes : `woocommerce/legal/` et `woocommerce/contenus/pages.md`. Mentions GPSR : opérateur responsable UE = toi.

---

## 7. Sauvegardes

- Quotidienne complète (fichiers + base) **hors site, dans l'UE**, rétention 30 jours ; base **toutes les heures** en
  période de forte vente (novembre–décembre) : les commandes vivent dans la base.
- Avant chaque mise à jour WooCommerce / thème / extension : sauvegarde manuelle.
- **Test de restauration mensuel en préproduction.** Ne jamais restaurer une base de production plus ancienne sans
  exporter d'abord les commandes postérieures (sinon commandes perdues, et Branvas aura expédié des commandes que la
  boutique ne connaît plus).

## 8. Préproduction (staging)

- Copie à une adresse séparée, `noindex`, protégée (mot de passe HTTP ou IP).
- Désactiver l'envoi d'e-mails (WP Mail SMTP « Disable emails ») et passer les paiements en mode test.
- **Ne pas connecter Branvas à la préproduction** (risque de commandes doublées / expédiées) — sauf session de test
  dédiée Auto-Fulfillment coupé, et dans ce cas déconnecter ensuite. Nombre de boutiques connectables par compte : **à confirmer**.
- Déploiement : pousser **fichiers** (thème, mu-plugins) de la préproduction vers la production ; **jamais la base**
  (écraserait commandes, clientes, stock synchronisé).
- Mises à jour : d'abord en préproduction (WooCommerce 7 jours après sa sortie), test du parcours d'achat, puis production.

## 9. Cache et sécurité

**Cache de page** : exclure `/panier/`, `/commande/`, `/mon-compte/`, `/retractation/`, toute URL avec `add-to-cart`,
`wc-ajax`, `/wp-json/` (Store API et API REST Branvas), et les cookies `woocommerce_items_in_cart`, `wp_woocommerce_session_*`.
Le thème est conçu pour le cache : boutons d'ajout compatibles (nonce Store API rafraîchi), newsletter et rétractation
sans nonce (anti-spam par champ piège). **Purger le cache** le 5 décembre à 0 h (fin de la date limite de Noël) et le
25 décembre (fin de l'emballage de Noël) : les messages sont calculés au rendu.

**Sécurité**
- Mises à jour automatiques mineures ; extensions abandonnées proscrites.
- 2FA pour tous les comptes admin / gestionnaire ; 2 administrateurs maximum ; mots de passe forts ; limitation des
  tentatives de connexion ; XML-RPC désactivé.
- Clé API Branvas : utilisateur dédié, droits Lecture/Écriture **seulement pour lui**, révoquer / régénérer si fuite ou
  fin de collaboration (WooCommerce > Avancé > API REST).
- Pare-feu applicatif (hébergeur, Cloudflare ou Wordfence) avec exception pour `/wp-json/wc/v3/` (Branvas).
- En-têtes : HSTS, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`,
  `Permissions-Policy` minimale ; `DISALLOW_FILE_EDIT`.
- Scan de logiciels malveillants hebdomadaire ; journal d'activité admin.
- Conformité : bannière cookies CNIL, mentions légales, CGV, médiateur de la consommation, rétractation en ligne,
  RGPD (registre, DPA hébergeur / Brevo / passerelles de paiement).

## 10. Recette avant lancement (checklist)

- [ ] Commande test FR et `/en/` : remise 2e parure correcte (ex. 79 € + 49 € → −7,35 €), forfait 4,90 € sous 50 €
      (après remise), livraison offerte au-delà, TVA 20 % dans la commande et la facture, téléphone exigé.
- [ ] Bouton « Commander avec obligation de paiement » (FR) / « Order with obligation to pay » (EN).
- [ ] Commande visible dans Branvas, annulée ; échantillon reçu.
- [ ] Formulaire de rétractation : e-mail marchand, accusé horodaté cliente, note de commande, entrée « Rétractations ».
- [ ] Bandeau Noël : « commande avant le vendredi 4 décembre » (jusqu'au 4/12 inclus).
- [ ] Aucune quantité de stock, aucun prix barré, aucun avis inventé visible.
- [ ] PageSpeed mobile : objectifs de `tech/performance.md`.
- [ ] Désindexation retirée, sitemap soumis, Search Console + Merchant Center.
