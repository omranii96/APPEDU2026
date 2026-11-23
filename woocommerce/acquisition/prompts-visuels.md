# CHARMED PARIS — Prompts visuels IA (Higgsfield / GPT Image)

> Objectif : produire vite des visuels de pub et d'organique **sans jamais trahir le bijou**.
> Les prompts sont en anglais (meilleurs résultats sur les modèles) ; chaque bloc a sa note en français. Textes à l'écran : FR + EN (marché UK).
> Palette : velours `#1A1015`, grenat `#7A1F3A`, or doux `#A9813F`, or clair `#E9CB8F`, porcelaine `#F4F2F5`, poudre `#D9C6CC`.

---

## 1. Règles non négociables

1. **Le bijou n'est jamais généré ni modifié.** Forme, nombre de pierres, couleur des pierres, type de chaîne, teinte du métal, proportions, fermoirs : identiques à la photo produit. Un visuel où le bijou a changé (même un maillon) est **rejeté**, pas « corrigé ».
2. **Toujours partir de la photo produit réelle comme référence** : détourés `charmed-paris/cut/{SKU}.webp`, photos `charmed-paris/img/{SKU}.webp`, photos de la fiche Branvas, ou (dès réception) photos de l'échantillon.
3. **Méthode par défaut = composition** : on génère la scène **vide** (fond, mains, cou, décor), puis on pose le **détouré réel** par-dessus (Photopea / Photoshop / Canva), avec ombre portée et reflets ajoutés à la main. L'IA ne touche jamais les pixels du bijou.
4. **Méthode avec référence (porté sur cou/oreille)** : autorisée seulement si le résultat passe la **check-list §2** à 100 %. Sinon : composition.
5. **Échelle honnête** : la taille du pendentif et des boucles par rapport au cou/à l'oreille doit correspondre aux dimensions de la fiche Branvas (à relever : hauteur du pendentif, longueur de chaîne, hauteur des boucles). Les photos sur mannequin peuvent tromper sur la taille [FAIT Branvas] : en cas de doute, comparer avec l'échantillon porté.
6. **Couleur du métal** : pas d'étalonnage qui rend le doré plus jaune/plus rose qu'en réalité ; pas de saturation des zircons.
7. **Mentions** :
   - Visuel montrant une **personne générée par IA** (y compris les mannequins Branvas, qui sont générés par IA [FAIT]) : mention **« Image virtuelle »** (EN : *AI-generated image*) dans le visuel ou la légende, et étiquette IA de la plateforme (Meta « Informations sur l'IA », TikTok « contenu généré par IA »). Obligatoire pour les créatrices (loi n° 2023-451 du 9 juin 2023), recommandé par prudence pour la marque (transparence IA, AI Act art. 50).
   - Photo de personne réelle dont la **silhouette ou le visage** est modifié : mention **« Photographie retouchée »** (décret n° 2017-738) / « Image retouchée » pour les créatrices.
   - Simple changement de fond autour du bijou : pas de mention obligatoire, mais **interdit** si cela crée une fausse impression (taille, matière, contexte).
8. **Droits** : les médias Branvas (photos, mannequins, vidéos) sont utilisables et modifiables en pub **tant que l'abonnement est actif** (essai compris), uniquement pour les produits réellement vendus, **sans jamais citer Branvas** [FAIT]. À retirer si l'abonnement s'arrête → archiver la liste des visuels qui en dépendent (colonne « source » du tableau §6).
9. **Textes dans l'image** : jamais générés par l'IA (fautes, lettres déformées). Ajoutés ensuite en Bodoni Moda / Jost / DM Mono.
10. **Logo** : uniquement le vrai fichier logo, ajouté en post-production. Jamais de logo généré, jamais de logo sur le bijou (il n'y en a pas [FAIT]).

## 2. Check-list de validation (chaque visuel)

| Contrôle | OK ? |
|---|---|
| Forme du pendentif et des boucles identique à la référence | ☐ |
| Nombre, forme et couleur des pierres identiques | ☐ |
| Type et finesse de chaîne identiques (ex. Molten Art : double chaîne à maillons trombone) | ☐ |
| Teinte du métal fidèle (comparée côte à côte avec la photo produit) | ☐ |
| Échelle cohérente avec les dimensions de la fiche | ☐ |
| Pas de pièce ajoutée (bague, bracelet) absente de la parure | ☐ |
| Pas de texte/logo parasite généré | ☐ |
| Mains/cou anatomiquement corrects (5 doigts, pas d'oreille déformée) | ☐ |
| Mention « Image virtuelle » / « Photographie retouchée » ajoutée si nécessaire | ☐ |
| Pour la ligne 925 : écrin velours **bleu** (pas l'écrin à ruban marqué) | ☐ |

## 3. Réglages des outils

### GPT Image (ChatGPT ou API, mode édition)
- **Scène vide** : génération simple, format 1024×1536 (2:3) ou 1024×1024, puis recadrage 4:5 / 9:16.
- **Avec référence** : importer la photo produit + écrire « keep the jewellery exactly as in the reference image, do not redraw it ». Utiliser l'édition avec **masque** : masquer uniquement la zone hors bijou.
- Générer 4 variantes, garder celle qui passe la check-list.

### Higgsfield
- Importer la photo produit comme **image de référence** (Media → upload) ; utiliser un modèle image qui accepte une référence produit (choix selon l'abonnement, ex. GPT Image via Higgsfield).
- Pour les vidéos (animation de lumière, mouvement de caméra autour de l'écrin) : partir d'une **image validée**, demander un mouvement de caméra lent sans transformation d'objet ; **refuser** toute vidéo où le bijou se déforme entre deux images (vérifier image par image au ralenti).
- Ne pas utiliser de génération « produit dans la main » animée si le bijou bouge : préférer un panoramique sur une image fixe composée.

### Agrandissement
- Les photos du dossier `branvas-photos/` font 400×400 : trop petites pour du 1080×1350. Récupérer les photos HD de la fiche produit synchronisée sur le site, ou utiliser un agrandissement **non génératif** (bicubique / Real-ESRGAN en réglage conservateur) puis vérifier la check-list. Pas d'agrandissement « créatif ».

---

## 4. Bibliothèque de prompts

Variables : `{SKU}` (ex. JSGRQR), `{PIECE}` (ex. « sculptural gold-tone necklace and earrings »), `{BG}` (couleur de fond).

### 4.1 Fonds vides pour composition (le détouré est posé ensuite)

**F1 — Velours grenat, lumière rasante** (Note : fond signature des pubs catalogue)
```
Empty product photography backdrop: deep garnet red velvet (#7A1F3A) gently draped, soft directional window light from the upper left, warm highlights, subtle shadow falloff, shallow depth of field, top-down 45-degree angle, generous empty space in the centre for a jewellery set to be placed later. No jewellery, no objects, no text, no logo. Photorealistic, editorial, 4:5.
```

**F2 — Porcelaine et poudre, minimal** (Note : statiques prix / C16)
```
Minimal studio surface in porcelain white (#F4F2F5) with a soft powder pink (#D9C6CC) curved backdrop, diffused daylight, very soft contact shadows, clean negative space in the centre. No objects, no jewellery, no text. Photorealistic, high-end catalogue style, square format.
```

**F3 — Marbre clair et soie** (Note : univers Éclat / Couleur précieuse)
```
Light Calacatta marble slab with a fold of champagne silk fabric on one side, morning light, delicate reflections on the marble, empty area in the lower centre for a jewellery piece. No jewellery, no text. Photorealistic, luxury editorial, 4:5.
```

**F4 — Velours noir, faisceau de lumière** (Note : C09, animation de lumière en post-prod)
```
Black velvet background (#1A1015), a single narrow beam of warm light crossing diagonally, dust particles barely visible in the beam, rest of the frame in deep shadow, empty centre. No objects, no jewellery, no text. Photorealistic, cinematic, 1:1.
```

**F5 — Écrin ouvert vide** (Note : uniquement pour un plan « avant » ; pour le vrai écrin, utiliser `box-open.webp` ou la photo de l'échantillon)
```
Use the reference image of the open jewellery box exactly as it is (same shape, same ribbon, same colour, same logo placement). Place it on deep garnet velvet with soft warm side light and a gentle glow coming from inside the box. Do not change the box. No jewellery inside. No added text. Photorealistic, 4:5.
```

### 4.2 Mains (scènes vides puis composition, ou référence + check-list)

**M1 — Mains qui tiennent l'écrin fermé** (Note : hook C01 / C14)
```
Close-up of two elegant female hands with natural short nails in a nude polish, holding a closed white jewellery box tied with a chocolate-brown ribbon with small gold hearts, as in the reference image (do not change the box or ribbon). Background: blurred garnet velvet. Soft warm light from the left. Natural skin texture, realistic fingers. No rings on the fingers. No text. Photorealistic, 4:5.
```

**M2 — Main ouverte, paume vers le haut, vide** (Note : on pose ensuite les boucles détourées dans la paume)
```
A single female hand, palm facing up, relaxed fingers, natural skin texture, neutral manicure, resting on a porcelain linen cloth, soft daylight, shallow depth of field, empty palm ready for small earrings to be added later. No jewellery, no rings, no text. Photorealistic, macro editorial, 4:5.
```

**M3 — Mains de deux générations** (Note : fête des mères / Mothering Sunday ; personnes générées = « Image virtuelle »)
```
Two pairs of hands, one older woman's hands with visible natural lines and one younger woman's hands, both holding the same closed jewellery box from the reference image, warm kitchen window light, cream knit sleeves, intimate and calm. Keep the box exactly as in the reference. No jewellery on the hands. No text. Photorealistic, documentary style, 9:16.
```

### 4.3 Cou et décolleté (porté)

**C1 — Cou nu pour composition du collier** (Note : la plus sûre ; poser le collier détouré, ajuster l'ombre)
```
Close-up of a woman's neck and collarbones, three-quarter view, head slightly turned away, hair tied up in a loose low bun, black fine-knit V-neck top, soft warm window light, natural skin texture with slight freckles, no jewellery at all, empty neckline ready for a necklace to be added. No face above the lips. No text. Photorealistic, editorial, 4:5.
```

**C2 — Porté avec référence (à valider par check-list)** (Note : « Image virtuelle » obligatoire)
```
Use the reference product image of {PIECE} (SKU {SKU}). Show the exact same necklace worn on a woman's neck and the exact same earrings on her ears. Do not redesign, simplify or add any element to the jewellery: same shapes, same number of stones, same chain, same gold tone, same proportions relative to a real human neck. Woman in a simple black top, hair tied back, cropped from lips to chest, soft warm daylight, neutral background in powder pink (#D9C6CC). No other jewellery. No text. Photorealistic, 4:5.
```

**C3 — Oreille en macro, vide** (Note : composition des boucles)
```
Macro photograph of a woman's ear and jawline in profile, hair tucked behind the ear, pierced earlobe with no earring, soft warm light, natural skin texture, blurred background in deep garnet. No jewellery. No text. Photorealistic, 4:5.
```

**C4 — Avant/après (paire d'images identiques)** (Note : C04 ; générer UNE image sans bijou, dupliquer, composer la parure sur la 2e)
```
Mirror-free front-facing portrait from shoulders up, woman in a plain black V-neck jumper, hair loose, neutral expression, soft daylight, beige wall background, no jewellery. Keep framing centred with space around the neck. No text. Photorealistic, 9:16.
```

### 4.4 Lumière et ambiance

**L1 — Lueur sortant de l'écrin** (Note : concept « l'écrin qui s'ouvre »)
```
Use the reference image of the open jewellery box. Add a warm golden glow (#E9CB8F) softly emanating from inside the box onto the surrounding dark velvet, as if light was coming out when opened. Do not alter the box shape, ribbon or logo. Nothing inside the box. No text. Photorealistic, cinematic, 9:16.
```

**L2 — Golden hour sur table** (Note : univers Sculpture)
```
Wooden café table at golden hour, a linen napkin, a ceramic espresso cup, long warm shadows from a window, empty space in the foreground for a jewellery set to be placed. No jewellery, no text, no brands. Photorealistic, lifestyle, 4:5.
```

**L3 — Soirée, bokeh** (Note : réveillon / Nouvel An)
```
Dark evening background with warm out-of-focus bokeh lights, a black satin fabric surface in the foreground with a soft spotlight, empty centre for a jewellery set. No jewellery, no text. Photorealistic, 4:5.
```

### 4.5 Saisonniers

**S1 — Noël (cohérent avec l'emballage de fête réel)** (Note : utiliser `pack-noel-f.webp` en référence ; ne pas inventer un autre emballage)
```
Use the reference image of the Christmas packaging exactly as it is. Extend the scene to a 9:16 vertical frame: more of the red knitted blanket, a few out-of-focus fairy lights at the top, a small pine branch. Do not change the box, the cards, the ribbon or the logo. No added text. Photorealistic.
```

**S2 — Saint-Valentin**
```
Overhead view of a powder pink (#D9C6CC) silk surface with a few scattered dark red rose petals and a folded handwritten-looking blank note card (no writing), soft daylight, empty centre for a jewellery box and set to be composited later. No jewellery, no text. Photorealistic, 4:5.
```

**S3 — Fête des mères / Mothering Sunday**
```
Spring kitchen table near a window, a small vase of white tulips, a linen tablecloth, a teapot slightly out of focus, morning light, empty foreground space for a jewellery box. No jewellery, no text, no people. Photorealistic, 4:5.
```

**S4 — Pour lui** (Note : packaging homme `pack-h.webp` en référence)
```
Use the reference image of the black men's packaging exactly as it is. Place it on a dark walnut desk with a leather notebook and a fountain pen slightly out of focus, cool evening light. Do not change the packaging. No added text. Photorealistic, 4:5.
```

### 4.6 Négatif (à ajouter si l'outil le permet)
```
Avoid: altered jewellery design, extra stones, extra chains, added rings or bracelets, melted or warped metal, text, letters, watermarks, logos, deformed hands, extra fingers, deformed ears, plastic skin, over-saturated gold, cartoon style.
```

---

## 5. Textes à poser en post-production (FR / EN)

| Usage | FR | EN |
|---|---|---|
| Signature | Ouvre. Laisse-toi charmer. | Open to be charmed. |
| Produit | Le collier et ses boucles, dans un seul écrin. | The necklace and its earrings, in one box. |
| Inclus | Écrin, pochette velours et chamoisine inclus. | Box, velvet pouch and polishing cloth included. |
| Taxes | Droits et taxes déjà payés. | Duties and taxes already paid. (UK : à confirmer) |
| Entretien | Dorée à l'or fin · à garder au sec. | Gold-plated · keep it dry. |
| Noël | Commande avant le vendredi 4 décembre pour Noël (Europe). | Order by Tuesday 8 December for Christmas (UK). |
| Emballage | Emballage de fête offert jusqu'au 24 décembre. | Festive wrapping until 24 December. |
| Mention IA | Image virtuelle | AI-generated image |
| Mention retouche | Photographie retouchée | Retouched image |

---

## 6. Les 10 premiers visuels à produire (vague du 24 au 27 novembre)

| # | Visuel | Produit (SKU) | Méthode | Prompt(s) | Format | Usage | Mention | Source des médias |
|---|---|---|---|---|---|---|---|---|
| 1 | Parure sur velours grenat, lumière rasante | Solar Sphere (JS1AQ5) | Composition | F1 + `cut/JS1AQ5.webp` | 4:5, 1:1 | Meta C1, catalogue, C09 | — | Branvas (abonnement) |
| 2 | Parure sur velours grenat | Golden Luxe (JSJB3S) | Composition | F1 + `cut/JSJB3S.webp` | 4:5, 1:1 | Meta C1, C09 | — | Branvas |
| 3 | Parure sur porcelaine + bloc infos prix | Molten Art (JSGRQR) | Composition | F2 + `cut/JSGRQR.webp` | 4:5 | C16 FR + EN | — | Branvas |
| 4 | Écran partagé « dépareillé vs assorti » | Emerald Square (JS3GGZ) | Composition | F2 ×2 + détouré + pièces neutres sans marque | 1:1, 9:16 | C05 | — | Branvas + photo propre |
| 5 | Écrin qui s'ouvre, lueur | Écrin (box-open) | Référence + vidéo Higgsfield caméra lente | L1, F5 | 9:16 | C01 hook | — | Maquette logo (Branvas) |
| 6 | Emballage de Noël étendu en 9:16 | pack-noel-f | Référence (outpaint) | S1 | 9:16, 4:5 | C03, C11 | — | Branvas |
| 7 | Collier porté, cou nu composé | Molten Art (JSGRQR) | Composition | C1 + détouré | 4:5 | C04 « après », Meta | « Image virtuelle » | IA + Branvas |
| 8 | Boucles dans la paume | Golden Hour (JS63VP) | Composition | M2 + détouré | 4:5 | Carrousel C08, Pinterest | « Image virtuelle » | IA + Branvas |
| 9 | Carrousel 8 parures fonds palette | 8 hero (cut/) | Composition | F1, F2, F3, F4 | 1:1 | C08 | — | Branvas |
| 10 | Packaging homme étendu | pack-h + Cosmic Circle (JSVKMZ) | Référence | S4 + photo produit | 4:5 | C18 | — | Branvas |

**Dès réception des échantillons** : refaire les visuels 1, 2, 3, 5 et 7 en **photo réelle** (téléphone, lumière du jour, fonds en tissu) : ils remplaceront progressivement les visuels IA et ne dépendront plus de l'abonnement Branvas.
