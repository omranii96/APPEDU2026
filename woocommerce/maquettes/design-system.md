# CHARMED PARIS · design system boutique (WooCommerce)

Source visuelle : `charmed-paris/charmed-site.html` (accueil). Les maquettes `fiche-produit.html`, `collection.html` et `panier-checkout.html` reprennent ses tokens à l'identique. Un seul look, assumé : velours + porcelaine, sans mode sombre.

Contenus : faits de `woocommerce/source/FAITS-BRANVAS.md` et décisions de `woocommerce/BRIEF.md` (prioritaires). Tout le site est bilingue FR / EN.

---

## 1. Tokens

### Couleurs de marque (`:root`, reprises de l'accueil)

| Token | Valeur | Usage |
|---|---|---|
| `--velours` | `#1A1015` | Fonds premium (hero, ticket Noël, footer), texte sur or clair |
| `--velours-2` | `#2a1520` | Centre des dégradés velours |
| `--velours-fg` | `#F2E9EC` | Texte sur velours |
| `--velours-muted` | `#B9A6AE` | Texte secondaire sur velours |
| `--porcelaine` | `#F4F2F5` | Fond de page |
| `--surface` | `#FFFFFF` | Cartes, champs, récap |
| `--encre` | `#1C1519` | Texte, bouton principal |
| `--muted` | `#6B6169` | Texte secondaire |
| `--line` | `#E2DBE0` | Séparateurs (décoratif seulement) |
| `--grenat` | `#7A1F3A` | Bandeau, eyebrows, survol du CTA, remise, barre livraison |
| `--or` | `#A9813F` | Anneau de focus, filets (jamais en texte courant) |
| `--or-clair` | `#E9CB8F` | Accents sur velours, bouton or, compteur panier |
| `--poudre` | `#E8D9DE` | Fonds doux |
| `--ivoire` / `--ivoire-2` | `#FBF8F3` / `#EFE7DC` | Fonds photo, champs carte |

### Tokens fonctionnels (ajoutés, pris dans la palette de l'accueil)

| Token | Valeur | Usage |
|---|---|---|
| `--champ` | `#8E838B` | Bordure des champs, quantité (3,6:1 sur blanc, critère 1.4.11) |
| `--erreur` | `#A3201F` | Messages et bordures d'erreur |
| `--ok` | `#2E6B3A` | Barre « livraison offerte » atteinte, « Sécurisé » |
| `--or-texte` | `#8A672C` | Icônes et petit texte doré sur fond clair (4,65:1) |
| `--shade` | `rgba(26,16,21,.45)` | Voile du tiroir et de la modale |

### Typographie

Google Fonts : `Bodoni Moda` (opsz 6..96, 400–700 + italique), `Jost` (300–600), `DM Mono` (400).

| Rôle | Police | Taille | Notes |
|---|---|---|---|
| Wordmark | Bodoni Moda | 22 px (header), 26 px (footer) | Capitales, interlettrage .16em |
| H1 univers | Bodoni Moda italique | clamp(52px, 8vw, 104px) | Hero Éclat |
| H1 produit | Bodoni Moda | clamp(34px, 4.4vw, 52px) | |
| H2 section | Bodoni Moda | clamp(30px, 4vw, 46px) | `text-wrap: balance` |
| H3 carte | Bodoni Moda | 19 px (16 px mobile) | |
| Prix fiche | Bodoni Moda | 32 px | `tabular-nums` |
| Texte | Jost 400 | 16 px / 1.55 | 16 px minimum dans les champs (pas de zoom iOS) |
| Secondaire | Jost 400 | 13–14 px | `--muted` |
| Bouton | Jost 500 | 13 px, capitales, .12em | |
| Eyebrow, légendes, SKU | DM Mono | 11 px, capitales, .14–.16em | `--grenat` ou `--muted` |

### Espacements et formes

- Gouttière : `max(16px, safe-area)` ; conteneur `.wrap` 1200 px max.
- Sections : 72 px vertical (52 px mobile). Grille produits : 20 px (12 px mobile).
- Rayons : **0** pour boutons, champs et cartes (luxe sobre) ; **999 px** pour chips et pastilles ; 6 px pour les boutons de paiement express (charte Apple/Google).
- Ombres : uniquement sur le ticket et les éléments flottants (tiroir, toast, barre collante).
- Mouvement : `--ease: cubic-bezier(.2,.7,.1,1)`, 0,25 à 0,5 s.

---

## 2. Composants

### Wordmark
`(` HARME `)` : deux parenthèses CSS (`.br.l` / `.br.r`) autour de « HARME », « PARIS » dessous en Jost 9 px interlettré .62em. Parenthèses grenat sur clair, or clair sur velours.

### Header
Bandeau grenat (texte long desktop, version courte mobile), puis header collant porcelaine de 64 px : navigation, logo centré, outils (sélecteur **FR | EN**, recherche, « Écrin » + compteur or clair). Sous 900 px : bouton menu à gauche, navigation déroulante. Le checkout a un header réduit (retour, logo, « Sécurisé », langue), sans navigation.

### Sélecteur de langue
Deux boutons `FR` / `EN` avec `aria-pressed`. Langue mémorisée (`localStorage`), `<html lang>` mis à jour, textes, attributs (`aria-label`, `alt`, `placeholder`, `content`), prix (`69,00 €` / `€69.00`) et dates basculent ensemble. En production : TranslatePress, URL `/en/`, hreflang.

### Boutons
| Variante | Rendu | Usage |
|---|---|---|
| `.btn` | Encre plein, texte porcelaine | CTA principal (« Ajouter à l'écrin », « Commander avec obligation de paiement ») |
| `.btn.ghost` | Contour `currentColor` | Actions secondaires, « Voir plus » |
| `.btn.gold` | Or clair, texte velours | Sur fond velours |
| `.xpay` | Noir (Apple Pay), blanc bordé (Google Pay), jaune (PayPal) | Paiement express, visuels indicatifs |

États : survol grenat, focus anneau or 2 px décalé de 3 px, désactivé à 45 % d'opacité. Hauteur minimale 44 px ; 56 px pour l'ajout au panier, 58 px pour la commande.

### Étiquette « ticket »
Reprise de `.ticket-tag` : fond `#FFFEFB`, œillet, en-tête mono avec wordmark et « Écrin n°10 », code produit encadré (`SOL`) + nom en italique, lignes pointillées pièce / statut, total en Bodoni, code-barres décoratif, pied grenat. Sur la fiche, il sert de bloc « Dans ton colis » (pièces incluses, boîte à bijoux 1 par commande, pochette, chamoisine, carte d'entretien, bordereau sans prix, emballage de Noël).

### Chips (filtres)
Pilule blanche bordée `--line`, 44 px de haut, compteur DM Mono. Sélectionnée : encre pleine + coche, `aria-pressed="true"`. Un chip sans résultat possible est désactivé. Mobile : rangée défilante horizontale avec fondu à droite (le défilement reste dans la rangée, jamais sur la page).

### Carte produit
Visuel 4:5 sur dégradé crème, photo en `multiply`. Au survol (et au focus clavier) : le détourage passe sur velours ; sans détourage disponible, un gros plan de la photo. Titre Bodoni (lien qui couvre toute la carte), prix au-dessus de la matière. Ajout rapide : bouton plein au survol (desktop), bouton rond « + » de 44 px toujours visible sur écran tactile. Variante cross-sell : mention « −15 % en 2e parure », **jamais de prix barré**.

### Badges
DM Mono 10 px capitales. Factuels uniquement :
- `Nouveau` (encre) : selon la date de mise en ligne.
- `Joaillerie 925` (velours / or clair) : argent 925 réel.
Interdits : « Best-seller », « Stock limité », pourcentages, compte à rebours.

### Accordéon
Bouton pleine largeur de 56 px, libellé capitales, icône + / − en CSS, `aria-expanded` + `aria-controls`, panneau `role="region"` animé en `grid-template-rows`, contenu fermé rendu `inert`.

### Barre livraison offerte
Texte + barre de 3 px. Grenat en progression (« Plus que 12,00 € pour la livraison offerte »), vert `--ok` une fois atteinte (« Livraison offerte ✓ »). Seuil **50 €** calculé après la remise 2e parure ; 4,90 € en dessous. Présente sur la fiche, le tiroir et le checkout.

### Quantité
Groupe bordé `--champ`, boutons 44 px (36 px visuels + zone tactile étendue dans le tiroir), valeur en `output` / `aria-live`.

### Tiroir panier et toast
Tiroir à droite (420 px max, plein écran mobile), `role="dialog"`, fermeture par Échap, voile ou bouton, focus rendu au déclencheur. Suggestion de 2e parure quand l'écrin en contient une seule. Toast en bas (au-dessus de la barre collante sur mobile) avec action « Voir l'écrin ».

### Barre d'ajout collante (mobile)
Apparaît quand le bouton d'ajout principal sort de l'écran par le haut : vignette, nom, prix, bouton. Masquée (`visibility:hidden`) sinon, et retirée de l'ordre de tabulation.

### Formulaire de checkout
Labels visibles au-dessus des champs, 50 px de haut, `autocomplete` sur chaque champ, `inputmode` adapté. Champs minimum : e-mail, prénom, nom, adresse (autocomplétion : code postal et ville se remplissent seuls), code postal, ville, téléphone (requis par le transporteur). Complément d'adresse replié derrière un lien. Erreurs sous le champ, bordure `--erreur`, `aria-invalid`, focus sur le premier champ en erreur.

### Bloc avis
Cadre pointillé « Avis clientes vérifiées (avis WooCommerce, à venir) ». Aucune note, aucune étoile, aucun avis tant qu'il n'y a pas de vraies acheteuses.

---

## 3. Règles de contenu (non négociables)

- Matières : « laiton doré » / EN « gold-plated brass » ; « doré à l'or X carats » seulement avec le carat relevé sur la fiche fournisseur. Jamais « plaqué or », « vermeil », « or massif ».
- Pierres : « oxydes de zirconium » / « cubic zirconia » ; « moissanite synthétique » / « lab-grown moissanite ».
- Toujours « à garder au sec ». Jamais « waterproof », « sans nickel », « hypoallergénique », « certifié ».
- Livraison : préparation 1–2 jours ouvrés, France 4–9 jours ouvrés, DHL, un seul mode (pas d'express), droits payés. Noël : « Commande avant le 4 décembre pour une livraison avant Noël (Europe) », emballage de Noël offert jusqu'au 24/12.
- Packaging : une boîte à bijoux par commande (les parures suivantes en sachets scellés), pochette velours, chamoisine, carte d'entretien, bordereau sans prix. Ligne 925 : écrin velours bleu. Pas de message cadeau, pas de gravure.
- Prix TTC en euros, aucun prix barré, remise « 2e parure −15 % » sur la moins chère.
- Checkout : bouton « Commander avec obligation de paiement » / « Order with obligation to pay », lien CGV, rappel du droit de rétractation de 14 jours, lien « Me rétracter » visible.

---

## 4. Accessibilité

- **Contrastes AA mesurés** : encre / porcelaine 16,1:1 ; muted / porcelaine 5,3:1 ; muted / blanc 5,9:1 ; grenat / porcelaine 9,1:1 ; blanc / grenat 10,1:1 ; or clair / velours 11,9:1 ; velours-muted / velours 8,1:1 ; erreur / blanc 7,5:1 ; ok / blanc 6,4:1.
- **À éviter** : `--or` en texte (3,2:1, réservé au focus et aux filets, ≥ 3:1 pour les éléments non textuels) ; `--muted` sur `--poudre` (4,35:1) ; `--line` comme bordure de champ (utiliser `--champ`).
- **Focus** : `:focus-visible` anneau or 2 px, jamais supprimé ; lien d'évitement « Aller au contenu ».
- **Cibles tactiles** : 44 × 44 px minimum (`--tap`) pour boutons, chips, quantités, liens d'action, puces de galerie.
- **Sémantique** : fil d'Ariane `nav` + `aria-current`, galerie au clavier (flèches), filtres `aria-pressed`, résultats `aria-live`, combobox d'adresse (`role="combobox"`, `listbox`, `aria-activedescendant`), tiroir et modale `aria-modal`.
- **Mouvement** : `prefers-reduced-motion` coupe transitions, animations et défilement doux.
- **Responsive** : testé de 360 à 1440 px, sans défilement horizontal de page (les rails défilent dans leur conteneur).

---

## 5. États

| Composant | États |
|---|---|
| Bouton | défaut, survol, focus, actif, désactivé |
| Chip | défaut, survol, sélectionné, désactivé (0 résultat) |
| Carte produit | défaut, survol / focus (détourage), ajout rapide |
| Champ | vide, focus, rempli, autocomplété, erreur |
| Barre livraison | en progression, atteinte |
| Écrin | vide (lien vers Éclat), 1 parure (suggestion −15 %), 2+ (remise affichée) |
| Grille | résultats, aucun résultat (effacer les filtres), « Voir plus » (6 par page), tout affiché |
| Galerie | slide courante (vignette ou puce `aria-current`), début / fin (flèches masquées) |
