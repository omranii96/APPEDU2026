# CHARMED PARIS, charte graphique v1

> 23/11/2026 · référence pour le site WooCommerce FR/EN, le packaging Branvas, les réseaux et les e-mails.
> Version visuelle : `charte.html` (ouvrir dans un navigateur, bouton FR/EN). Fichiers : `logos/`.
> La décision sur le nom est dans `decision-nom.md`.

---

## 1. Concept : l'écrin qui s'ouvre

**Le C et le D de CHARMED sont deux parenthèses, les deux parois d'un écrin.** Entre les deux se trouve ce qu'on offre, « HARME ». Fermé, c'est un mot. Ouvert, c'est un cadeau.

Tout découle de ce geste : le logo, l'animation d'ouverture du site, le coffret Branvas qu'on soulève, la signature *« Ouvre. Laisse-toi charmer. »* (EN : *“Open. Be charmed.”*).

Les trois mots de la marque :
- **Écrin** : on encadre, on protège, on révèle. Il y a des marges, du vide autour de l'objet.
- **Velours** : un fond sombre, chaud et profond. Le bijou est la seule lumière.
- **Précision** : le contraste Didone (pleins épais, déliés fins), des chiffres justes et des promesses vraies.

Ton visuel : **luxe accessible**, c'est-à-dire le soin d'une maison de joaillerie sans son prix ni sa froideur. On évite tout ce qui fait « bazar » (rouge promo, badges qui clignotent, faux comptes à rebours).

## 2. Logo

### 2.1 Les éléments
| Élément | Description | Fichiers |
|---|---|---|
| **Logo principal** (empilé) | Les parenthèses ( HARME ) en Bodoni Moda, avec « PARIS » en Jost espacé dessous, centré sur HARME | `logos/principal/` |
| **Logo horizontal** | Le wordmark, un filet vertical, puis PARIS sur une ligne. Pour l'en-tête du site sur mobile, les signatures e-mail et les bandeaux | `logos/horizontal/` |
| **Monogramme** | Les deux parenthèses avec un losange (le bijou dans l'écrin) | `logos/monogramme/` |
| **Favicon / icône d'app** | Monogramme épaissi, or sur carré velours | `logos/favicon/` |
| **Masters impression** | Mêmes dessins, déliés renforcés (Bodoni Moda opsz 6, graisse 600 ; parenthèses déliés ×1,8). Noir pur, une couleur | `logos/impression/` |

Les lettres sont **vectorisées** depuis Bodoni Moda (opsz 18, graisse 500) et Jost (500). Les SVG ne contiennent que des `<path>` et ne dépendent d'aucune police installée. Le script de génération utilise fontTools (instanciation de la police variable, puis contours). Les parenthèses sont dessinées géométriquement : un plein extérieur épais (= fût du H), des déliés haut et bas, et un intérieur elliptique qui reproduit la modulation Didone.

### 2.2 Versions couleur
| Fichier (suffixe) | Usage |
|---|---|
| `-encre` (#1A1015) | Version de référence sur fonds clairs (porcelaine, blanc, poudre) |
| `-grenat` (lettres encre, parenthèses et PARIS grenat) | Sur clair, pour les moments de marque : page d'accueil, carte, étiquettes |
| `-or` (#E9CB8F) | Sur velours ou grenat uniquement |
| `-or-sur-velours` | Fichier avec le fond : avatar, visuels sociaux, écran de chargement |
| `-bicolore` (lettres #F2E9EC, parenthèses or) | En-tête du site et pied de page sur velours (comme la maquette) |
| `-blanc` | Sur photo sombre ou fond grenat |
| `impression/*-noir-impression` | **Noir pur 1 couleur** : dorure à chaud Branvas, tampon, gravure, fax… |
| `impression/*-blanc-impression` | Réserve blanche ou marquage sur fond foncé |

PNG prêts à l'emploi : `logos/png/` (2400 px de large, fond transparent) et `logos/favicon/` (16, 32, 180, 512 px).

### 2.3 Zone de protection
Unité **E** = la largeur d'une parenthèse (environ 9 % de la largeur du logo principal).
- Logo principal et logo horizontal : **1 E de vide sur les quatre côtés.**
- Monogramme : **½ largeur de parenthèse** de vide sur les quatre côtés.
- Aucun texte, aucun bord de page ni pictogramme ne doit entrer dans cette zone.

### 2.4 Tailles minimales
| Version | Écran | Impression couleur / offset | Dorure à chaud Branvas (trait ≥ 0,3 mm) |
|---|---|---|---|
| Principal (master fin) | 140 px de large | 40 mm | à ne pas utiliser |
| Principal **impression** | 110 px | 30 mm | **50 mm de large minimum** (le délié le plus fin, 74/11 648 de la largeur, fait 0,3 mm à 47 mm) |
| Horizontal | 180 px | 50 mm | version impression : 70 mm |
| Monogramme | 24 px (sous 24 px : favicon) | 8 mm | 10 mm |
| Favicon | 16 px | – | – |

Sous ces tailles, on passe à la version suivante : du logo principal au monogramme.

### 2.5 Interdits
- Remplacer les parenthèses par des caractères « ( ) » d'une police, ou par d'autres formes.
- Écrire CHARMED sans PARIS dans la marque (sauf monogramme, et le wordmark seul en très grand, en ouverture d'animation).
- Changer la police, l'approche ou les proportions : on ne déforme pas, on n'étire pas, on ne met pas d'italique.
- Ajouter ombre, dégradé, contour, effet métal 3D ou paillettes (l'or est un **aplat**).
- Mettre l'or sur un fond clair. Il passe sous 3:1 sur blanc pour les petites tailles, donc on prend l'encre ou le grenat.
- Poser le logo sur une photo chargée sans voile ni zone calme.
- Ajouter la signature « Ouvre. Laisse-toi charmer. » **dans** le logo imprimé par Branvas (Branvas déconseille les lignes de base fines).
- Faire référence à la série *Charmed* (triquetra, etc.).

## 3. Couleurs

| Nom | Hex | RVB | Rôle | Part |
|---|---|---|---|---|
| **Velours** | #1A1015 | 26, 16, 21 | Fond signature, texte principal (encre #1C1519 sur le site) | 30 % |
| **Porcelaine** | #F4F2F5 | 244, 242, 245 | Fond clair principal | 45 % |
| **Grenat** | #7A1F3A | 122, 31, 58 | Boutons d'achat, liens forts, bandeaux, accents | 8 % |
| **Or doux** | #A9813F | 169, 129, 63 | Filets, icônes, grands chiffres sur clair (≥ 24 px) | 4 % |
| **Or clair** | #E9CB8F | 233, 203, 143 | Logo et texte sur velours, détails | 5 % |
| **Poudre** | #D9C6CC | 217, 198, 204 | Fonds de sections douces, cartes, étiquettes | 8 % |
| Or texte (accessibilité) | #7D5E2A | 125, 94, 42 | Remplace l'or doux pour le **petit texte** sur clair | – |
| Gris prune (muted) | #6B6169 | 107, 97, 105 | Texte secondaire sur clair | – |

Note : la maquette `charmed-site.html` utilise #E8D9DE pour la poudre. La **référence est #D9C6CC** (BRIEF). #E8D9DE est admis comme teinte de fond très claire (« poudre 50 »).

### Contrastes WCAG vérifiés (calcul de luminance relative WCAG 2.1)
| Texte / fond | Ratio | AA texte normal (4,5) | AA grand texte (3) |
|---|---|---|---|
| Encre #1C1519 / porcelaine | 16,1 | ✔ | ✔ |
| Velours / poudre #D9C6CC | 11,4 | ✔ | ✔ |
| Gris prune #6B6169 / porcelaine | 5,3 | ✔ | ✔ |
| Grenat / porcelaine | 9,1 | ✔ | ✔ |
| Blanc / grenat (bouton) | 10,1 | ✔ | ✔ |
| Grenat / poudre | 6,2 | ✔ | ✔ |
| Or clair #E9CB8F / velours | 11,9 | ✔ | ✔ |
| #F2E9EC / velours | 15,6 | ✔ | ✔ |
| #B9A6AE / velours (texte secondaire) | 8,1 | ✔ | ✔ |
| Or doux #A9813F / velours | 5,2 | ✔ | ✔ |
| Or clair / grenat | 6,4 | ✔ | ✔ |
| **Or doux #A9813F / porcelaine** | **3,2** | ✘ | ✔ (≥ 24 px ou 18,7 px gras seulement) |
| Or doux / blanc | 3,6 | ✘ | ✔ |
| Or texte #7D5E2A / porcelaine | 5,4 | ✔ | ✔ |

Règle : **l'or doux n'est jamais utilisé pour du texte courant sur clair** ; on prend #7D5E2A. Les éléments graphiques non textuels (filets, icônes) doivent atteindre 3:1, ce que fait l'or doux sur porcelaine.

## 4. Typographie

| Police | Rôle | Graisses | Licence |
|---|---|---|---|
| **Bodoni Moda** (Indestructible Type) | Logo, titres, prix, citations en italique | 400, 500 (italique 400). Axe `opsz` actif : `font-optical-sizing:auto` | SIL OFL 1.1 (**confirmée** : fichier OFL.txt du dépôt google/fonts) |
| **Jost** (indestructible type) | Texte courant, boutons, navigation, « PARIS » du logo | 300, 400, 500, 600 | SIL OFL 1.1 (dépôt google/fonts `ofl/jost`), à re-confirmer sur la page Google Fonts au lancement |
| **DM Mono** (Colophon / Google) | Détails : sur-titres, SKU, étiquette « ticket », mentions | 400 | SIL OFL 1.1 (dépôt google/fonts `ofl/dmmono`), à re-confirmer |

OFL : usage commercial, web, impression et logo libres. Seule la revente des fichiers de police seuls est interdite. Pour le site, auto-héberger les WOFF2 (performance + RGPD : pas d'appel à Google Fonts, cf. jurisprudence allemande 2022).

### Échelle (base 16 px, rapport ≈ 1,25 à 1,33)
| Niveau | Police | Taille (mobile → bureau) | Interlignage | Détails |
|---|---|---|---|---|
| Display (hero) | Bodoni Moda 400 | 40 → 72 px | 1,05 | Capitales ou casse normale, approche 0 |
| H1 | Bodoni Moda 400 | 32 → 52 px | 1,1 | |
| H2 | Bodoni Moda 400 | 26 → 40 px | 1,12 | |
| H3 / nom de parure | Bodoni Moda 500 | 20 → 26 px | 1,2 | |
| Citation / signature | Bodoni Moda italique 400 | 20 → 30 px | 1,3 | « Ouvre. Laisse-toi charmer. » |
| Texte | Jost 400 | 16 px (17 px bureau) | 1,55 | 60–72 caractères par ligne |
| Petit texte | Jost 400 | 14 px | 1,5 | |
| Bouton | Jost 500 | 14 px, MAJ, approche 0,12 em | – | |
| Sur-titre (eyebrow) | DM Mono 400 | 11 px, MAJ, approche 0,16 em | – | Grenat sur clair, or clair sur velours |
| Prix | Bodoni Moda 400 | 22 → 28 px, chiffres tabulaires | – | « 69 € », espace insécable |

## 5. Iconographie
- Pictos **au trait 1,5 px**, terminaisons arrondies, grille 24 px, en encre ou or (Lucide, licence ISC, ou Phosphor Light, licence MIT : une seule famille).
- Motifs de marque : la **parenthèse** sert à encadrer un badge ou un chiffre « ( 2e parure −15 % ) », et le **losange** sert de puce ou de séparateur (◆ en or).
- Réassurance (livraison 4–9 jours ouvrés, droits payés, rétractation 14 jours, paiement sécurisé) : un picto + une phrase courte, **jamais** de faux labels ou de faux sceaux de certification.

## 6. Direction photo
1. **Parures détourées sur velours** (#1A1015 ou grenat profond), avec une lumière chaude, latérale et douce, et une ombre portée courte. Le collier et les boucles sont toujours **ensemble** (on vend des parures).
2. **Packshots coffret** : le coffret blanc Branvas entrouvert, la pochette velours, le papier nid d'abeille ; le geste d'ouvrir. Fond porcelaine ou poudre.
3. **Portés : mains, cou, oreille**, en cadrage serré, avec des peaux réelles et variées, en lumière du jour chaude (fenêtre, fin d'après-midi). Les photos mannequins Branvas sont autorisées tant que l'abonnement est actif (on les retire s'il s'arrête).
4. **Interdits** : mannequin généré par IA présenté comme réel, bijou retouché au-delà de la réalité (taille des pierres, éclat ajouté), « or » plus jaune que le produit, mise en scène de luxe trompeuse (faux écrin de grande maison), filtres froids et bleutés.
5. Couleur : balance des blancs chaude (5 000–5 500 K), noirs denses mais pas bouchés, saturation retenue. On garde la même retouche sur tout le catalogue.
6. Formats : fiche produit 1:1 (1 600 px) sur porcelaine ; réseaux 4:5 et 9:16 ; site hero 16:9 et 4:5 en mobile.

## 7. Motion : l'écrin qui s'ouvre
- **Geste unique** : les deux parenthèses s'écartent (ouverture) ou se rapprochent (fermeture) horizontalement, autour du contenu. On ne fait ni rotation ni rebond.
- **Courbe** : `cubic-bezier(.2,.7,.1,1)` (sortie douce, comme un couvercle amorti). Durées : 600–900 ms pour l'ouverture de page, 240–320 ms pour l'interface (panier, menu).
- **Ordre** : les parenthèses s'écartent, le contenu apparaît en fondu et monte de 8 px, puis l'or « respire » une fois (opacité 0,8 → 1). On ne fait jamais de scintillement en boucle.
- **Usages** : intro du site (déjà maquettée), ajout au panier (le losange entre dans l'écrin), chargement (parenthèses qui respirent), stories (ouverture de 1 s en début de vidéo).
- **Accessibilité** : respecter `prefers-reduced-motion` (on affiche l'état ouvert directement), rien ne clignote plus de 3 fois par seconde, et l'animation ne bloque jamais le contenu (on peut la passer).

## 8. Applications

### 8.1 Packaging Branvas (dorure à chaud, une couleur)
Exigences lues dans l'article Branvas 12241060 : marquage **à la feuille d'or, une seule couleur**, avec conversion automatique en monochrome ; **500 × 500 px minimum à 300 DPI** ; monochrome de préférence ; formes pleines et franches ; **épaisseur de trait ≥ 0,3 mm** ; fond propre ou transparent ; PNG, JPG ou WEBP ; **moins de 4 Mo**. Pas de dégradés, pas de multicolore, pas de lignes de base fines.

Fichier à téléverser : **`logos/impression/BRANVAS-logo-principal-noir-2000x2000-300dpi.png`** (2 000 × 2 000 px, 300 DPI, noir pur sur transparent, 37 Ko, master impression aux déliés renforcés, sans signature).
- Alternative si la maquette Branvas montre le logo **à moins de 50 mm de large** : `BRANVAS-monogramme-noir-2000x2000-300dpi.png` (le monogramme tient jusqu'à 10 mm).
- Chemin : Dashboard › Logo Setup › Setup New Logo › fichier › **vérifier l'aperçu de la maquette** (on contrôle que le H et le E gardent leurs déliés), puis Submit. Validation sous 24 h.
- Où va le logo : **à l'intérieur du couvercle du coffret d'envoi blanc** (selon les offres packaging Branvas ; carte insert personnalisée avec l'offre VIP). Le logo n'est jamais sur le bijou.
- Ne pas promettre en ligne un rendu (couleur de dorure, emplacement) qui n'aurait pas été vérifié sur une commande d'échantillon.

### 8.2 Carte de remerciement (VIP Branvas ou impression maison A6 / 105 × 148 mm)
- Recto : fond velours, monogramme or au centre (20 mm), et dessous en Bodoni italique or clair « Ouvre. Laisse-toi charmer. ».
- Verso : fond porcelaine, logo principal encre en haut (40 mm), message en Jost 10 pt (« Merci de nous avoir choisies… »), conseils d'entretien en 3 lignes (« à garder au sec », chamoisine, pochette), le QR code vers la page avis réels, puis `charmedparis.com`.
- On imprime le texte EN au verso d'une seconde version (commandes hors France).

### 8.3 Réseaux sociaux
- **Avatar** : monogramme or sur velours, centré, qui tient dans le cercle (`logos/png/avatar-instagram-1080.png`).
- **Couvertures de stories à la une** (1080 × 1920, motif central dans un cercle de 600 px) : fond velours, un mot en Bodoni italique or clair **entre parenthèses** : ( Parures ), ( Coffrets ), ( Offrir ), ( Avis ), ( Entretien ), ( Noël ). L'EN est géré par des stories à la une séparées si besoin.
- Publications : 4:5, avec une marge intérieure de 64 px ; logo horizontal ou monogramme en bas, petit, jamais au centre de la photo.

### 8.4 Signature e-mail (HTML, 600 px max)
```
Prénom Nom · CHARMED PARIS
Parures & coffrets bijoux
charmedparis.com · @charmedparis
[logo horizontal encre, PNG 2× affiché à 180 px de large]
```
Jost 13 px, gris prune pour la ligne 2. Pas de bannière promo ni de citation animée.

### 8.5 Étiquettes cadeau (60 × 90 mm, trou ⌀ 4 mm)
- Recto : fond grenat ou poudre, monogramme or (ou encre sur poudre), et dessous « Pour toi » (Bodoni italique).
- Verso : 3 lignes manuscrites « De… / Pour… / Un mot… » en DM Mono 7 pt sur filet or.
- L'étiquette est glissée par nos soins seulement si on reconditionne. Avec Branvas, le colis part sans contenu ajouté (hors carte VIP), donc on la propose plutôt **en téléchargement imprimable** après l'achat.

## 9. Fichiers et production
- Les SVG sont générés par script : polices OFL instanciées puis converties en contours (pas de dépendance de police). Pour une retouche manuelle, ouvrir les SVG dans Figma ou Illustrator. Ce sont déjà des contours.
- PNG : rendus par Chromium (Playwright) depuis les SVG, fond transparent. Les fichiers Branvas ont des métadonnées 300 DPI (Pillow).
- `apercu-logos.png` : planche de présentation de toutes les versions.

---

## English summary

**Concept, the opening case.** In CHARMED, the C and the D are drawn as two brackets: the walls of a jewellery case around “HARME”. Every touchpoint repeats this gesture: logo, site intro, the Branvas box you lift open, and the tagline *“Open. Be charmed.”* (FR: *« Ouvre. Laisse-toi charmer. »*). The positioning is accessible luxury: the care of a jewellery house without its price or coldness.

**Logo.** The primary lockup stacks ( HARME ) in Bodoni Moda over a widely tracked Jost “PARIS”. There is also a horizontal lockup, a monogram (the brackets with a lozenge “jewel”) and a favicon. All letters are outlined to SVG paths, with no font dependency. A reinforced **print master** (Bodoni opsz 6/600, thicker hairlines) exists for single-colour pure black use and Branvas gold-foil stamping. Clear space is 1 bracket-width on all sides. Minimum sizes: 140 px on screen, 40 mm in print, **50 mm for foil stamping** (≥ 0.3 mm strokes), and 10 mm for the monogram. Don'ts: no effects or gradients, no gold on light backgrounds for small sizes, no tagline inside the foil logo, and no reference to the *Charmed* TV series.

**Colour.** Velvet #1A1015, Porcelain #F4F2F5, Garnet #7A1F3A, Soft gold #A9813F, Light gold #E9CB8F, Powder #D9C6CC, and Text gold #7D5E2A for small gold text on light backgrounds. All text pairings pass WCAG AA. The exception is soft gold on porcelain (3.2:1), which is for large text and graphics only.

**Type.** Bodoni Moda (display, logo, prices), Jost (body, UI), DM Mono (labels). All three are under the SIL Open Font License, which allows commercial use, web, print and logo work. Bodoni Moda's OFL was confirmed from the google/fonts repository. Self-host the WOFF2 files.

**Photography.** Matching sets cut out on velvet, warm side light, packshots of the half-open box, close crops of hands, neck and ears on real skin. No AI models presented as real, and no retouching beyond reality.

**Motion.** One gesture only: the brackets part (or close) horizontally, with the curve cubic-bezier(.2,.7,.1,1) and 600–900 ms timing. `prefers-reduced-motion` is respected.

**Applications.** Upload `logos/impression/BRANVAS-logo-principal-noir-2000x2000-300dpi.png` to Branvas (Dashboard › Logo Setup). It is printed in gold foil inside the shipping-box lid, and the monogram is the fallback below 50 mm. The guide also specifies the thank-you card, the Instagram avatar and highlight covers ( Sets ), ( Gift )…, the e-mail signature and the gift tags.
