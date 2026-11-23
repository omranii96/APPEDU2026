# Données structurées JSON-LD — mode d'emploi

| Fichier | Où | Comment l'injecter |
|---|---|---|
| `organization-website.jsonld` | Toutes les pages (Organization + WebSite) | Rank Math → Titres & métas → Local SEO / Knowledge Graph : renseigner nom, logo, e-mail. Rank Math génère déjà Organization + WebSite : **comparer, compléter, ne pas doubler**. Pour `hasMerchantReturnPolicy` au niveau Organization : snippet dans `functions.php` (filtre `rank_math/json_ld`) ou Rank Math Pro |
| `product-solar-sphere-fr.jsonld` / `-en.jsonld` | Fiches produits | Rank Math (module WooCommerce) génère Product + Offer automatiquement. Ce fichier est la **cible à atteindre** : ajouter `brand`, `material`, `color`, `shippingDetails`, `hasMerchantReturnPolicy` via le filtre `rank_math/snippet/rich_snippet_product_entity` ou Rank Math Pro. Ne pas coller ce JSON en dur sur 30 fiches (prix et stock doivent rester dynamiques) |
| `breadcrumb-produit.jsonld`, `breadcrumb-page-cadeau.jsonld` | Produits, catégories, pages | Généré par le fil d'Ariane Rank Math (catégorie principale = univers). Ces fichiers servent de référence pour vérifier le résultat |
| `faqpage-fr.jsonld` | `/faq/` (et une FAQ courte sur chaque page cadeau) | Bloc « FAQ by Rank Math » dans l'éditeur : il génère le schéma depuis le texte visible. Le texte affiché et le JSON-LD doivent être **identiques** |
| `itemlist-univers-eclat.jsonld` | Pages univers et cadeaux | Rank Math sort un ItemList sur les archives produits si l'option n'est pas désactivée ; sinon snippet. Modèle valable pour les 5 univers |

## Valeurs d'exemple à remplacer (non vérifiées)

- Domaine `charmedparis.com` (achat **à confirmer**), e-mail `bonjour@`, logo, **adresse postale** (champs « À REMPLIR » ; c'est ton adresse, jamais celle du fournisseur).
- `price` : 69,00 € (fourchette maquette Éclat 59–79 €) et 79,00 $ : **exemples à valider**.
- `shippingRate` 0,00 : valable seulement si la livraison est offerte pour ce prix (seuil « dès 50 € » **à valider**). Sinon, mettre le tarif réel affiché au checkout.
- `returnFees` = frais de retour à la charge de la cliente : **à confirmer**. Si les retours sont offerts, mettre `https://schema.org/FreeReturn`. `returnPolicyCountry` = pays de l'adresse de retour (FR supposé, **à confirmer**).
- `sku` : le SKU synchronisé (préfixe JS). Il apparaît publiquement ; un SKU maison est possible si la synchro Branvas le permet (**à confirmer**).

## Délais utilisés (faits Branvas)

Préparation 1–2 jours ouvrés. Délai total (9 colis sur 10) : France 4–9 jours ouvrés → `handlingTime` 1–2 + `transitTime` 3–7. US 3–8 → 1–2 + 2–6. UK 3–7 → 1–2 + 2–5. Canada 4–8 → 1–2 + 3–6. Un `shippingDetails` par pays dans le schéma EN, ou mieux : renseigner les délais dans **Merchant Center**, qui fait foi pour Google Shopping.

## Version EN : devise

Le prix du schéma doit être celui **affiché** sur la page. Avec WCML (devise selon le pays), Googlebot, qui crawle surtout depuis les États-Unis, verra probablement l'USD : définir l'USD comme devise par défaut de `/en/` et donner les prix GBP / CAD à Google via les flux Merchant Center par pays (**à valider**).

## aggregateRating / review : NE PAS AJOUTER maintenant

Aucun avis réel n'existe. Ajouter un `aggregateRating` sans avis visibles et vérifiables est contraire aux consignes Google (action manuelle possible) et constitue une pratique commerciale trompeuse.

L'ajouter seulement quand :
1. un outil d'avis vérifiés est en place (Judge.me, Trustpilot, avis Google Merchant, etc.) et collecte des avis de vraies clientes après livraison ;
2. les avis sont **affichés sur la fiche produit** elle-même ;
3. le produit a au moins quelques avis (aucun minimum chez Google ; viser ≥ 3–5 pour que la note ait du sens) ;
4. le balisage est généré **par l'outil d'avis ou Rank Math depuis les avis réels** (jamais saisi à la main), avec un seul `aggregateRating` par produit.

L'information obligatoire (directive Omnibus / art. L111-7-2 du Code de la consommation) sur la façon dont les avis sont contrôlés doit être affichée près des avis.

## Notes Google (à jour de mes connaissances, à revérifier)

- **FAQPage** : depuis 2023, Google n'affiche plus les résultats enrichis FAQ que pour les sites gouvernementaux et de santé. On garde le balisage parce qu'il structure le contenu pour les autres moteurs et les IA, sans attendre d'affichage enrichi.
- **SearchAction** (champ de recherche de liens annexes) : Google ne l'affiche plus depuis fin 2024. Balisage inoffensif, gardé pour les autres moteurs.
- **ItemList** sur une catégorie produit : aucun résultat enrichi garanti ; utile à la compréhension de la page.
- Tester chaque modèle avec le Test des résultats enrichis de Google et le Schema Markup Validator avant la mise en ligne, puis surveiller les rapports « Fiches de marchand » et « Extraits de produits » de Search Console.
