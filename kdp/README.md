# KDP Kids — TOP 3 livres enfants prêts à publier (EN + FR)

Trois livres complets, **6 éditions** (anglais pour Amazon.com/.co.uk, français pour Amazon.fr), générés par un moteur de production Python 100 % reproductible : intérieurs, couvertures complètes (dos + tranche + face), fichiers Kindle, fiches KDP copier-coller, et un contrôle qualité automatique (preflight) sur chaque fichier.

| # | Livre | Format KDP | Pages | Pourquoi il vend |
|---|---|---|---|---|
| 1 | **Dino Quest Activity Book (4-8 ans)** / *Cahier d'activités Dinosaures* | Broché 8,5×11 in, noir & blanc, sans fond perdu | 108 | La niche la plus constante de KDP jeunesse (cahier d'activités + dinosaures, 4-8 ans). 86 activités variées à difficulté progressive, solutions, diplôme. Pic de ventes à Noël → à publier **maintenant**. |
| 2 | **Dino Quest ABC (3-5 ans)** / *J'apprends à écrire* | Broché 8,5×11 in, noir & blanc | 82 | Les cahiers d'écriture sont une demande « evergreen » (pics en janvier et août). **Différenciation unique : traits numérotés + flèches de sens** pour chaque lettre et chiffre, ce que les cahiers à pointillés n'offrent pas. Même univers que le #1 → effet série. |
| 3 | **Nova's Calm Glow** / *La lumière douce de Nova* | Broché 8,5×8,5 in, **Premium Color**, fond perdu + eBook Kindle | 32 | Combine les 2 niches d'album les plus stables : **histoire du soir** + **émotions/apprentissage socio-émotionnel**. 3 outils de calme concrets, pages bonus interactives. |

> Les fichiers sont dans `kdp/out/` — tous ont passé le **PREFLIGHT PASS** (voir plus bas).

---

## 1. Étude de marché (résumé)

* Bande d'âge la plus porteuse sur KDP : **3-7 ans**. Formats les plus réguliers : cahiers d'activités thématiques, cahiers d'écriture, albums « émotions » et « coucher ».
* Les activités doivent être **nichées** (thème fort : dinosaures) et les albums doivent enseigner **une compétence précise** (ici : se calmer par la respiration), pas un message vague.
* Les livres d'émotions (« big feelings ») sont en tête des ventes jeunesse en 2026 ; les cahiers de vacances/maternelle dominent les meilleures ventes françaises.
* Contrôle d'originalité effectué : un album « Luma's Little Light » (luciole nommée Luma) existait déjà → **personnage et titre renommés en Nova** avant publication. « Dino Quest » : aucun livre ni marque trouvé (à re-vérifier sur Amazon et l'INPI/USPTO avant publication).

Sources : [Book Bolt – niches enfants](https://bookbolt.io/kdp-books-for-children/), [KDP Builder – niches 2026](https://kdpbuilder.com/blog/best-childrens-book-niches), [Neolemon – niches enfants](https://www.neolemon.com/guides/profitable-childrens-book-niches-amazon-kdp/), [KDPeasy – activity books](https://www.kdpeasy.com/blog/kids-activity-book-kdp-guide), [Common Sense Media – best-sellers Amazon](https://www.commonsensemedia.org/lists/bestselling-new-books-on-amazon-for-kids-and-teens), [ActuaLitté – meilleures ventes cahiers](https://actualitte.com/article/132461/meilleures-ventes/quels-cahiers-de-vacances-choisir-pour-oublier-sa-la-prof).

## 2. Analyse des 18 dépôts fournis → ce qui a été installé

| Dépôt | Ce que c'est | Verdict |
|---|---|---|
| wendy5062/KDP-PUBLISHING-SKILL | Skill Claude « album jeunesse KDP » (specs, marges, tranche, preflight) | ✅ **Installé** → `.claude/skills/kdp-childrens-book-publishing` (MIT). Ses règles sont appliquées (marge texte couverture 0,5 in, vérif. programmatique, pas de texte « placeholder », zone code-barres vide). |
| nikmcfly/kindle-book-skill | Skill Markdown → EPUB3 + PDF KDP (pandoc/XeLaTeX) | ✅ **Installé** → `.claude/skills/kindle-book` (MIT). Utile pour de futurs livres texte (romans, guides parents). |
| beyondtahir/beyondwords | Skill complet recherche → écriture → couverture → pub | ✅ **Installé** → `.claude/skills/beyondwords` (MIT, 1,8 Mo sans la vidéo). |
| rxpelle/kdp-scout | CLI mots-clés (autocomplétion Amazon, BSR, Ads) | ✅ **Installé** dans `.venv-kdp` (non versionné ; réinstaller avec `python3 -m venv .venv-kdp && .venv-kdp/bin/pip install git+https://github.com/rxpelle/kdp-scout`). Amazon est bloqué dans ce conteneur cloud → à lancer sur votre machine pour valider les mots-clés. |
| joshyattridge/amazon-kdp-skill | Automatisation KDP (Playwright : publier, prix, rapports) | ⚠️ **Pas de licence** → non copié dans le dépôt. Installation sur votre machine : `git clone https://github.com/joshyattridge/amazon-kdp-skill` (exige votre connexion KDP). |
| ekr0/auto-kdp | Upload KDP en masse (Puppeteer + CSV) | Référence (MIT). Utile seulement à partir de dizaines de titres. |
| vpuna/markdown-to-book | Markdown → PDF/EPUB KDP (pandoc) | Référence (MIT) ; doublon de kindle-book. |
| b7011343/kdp-gpt | Générateur de livres via OpenAI | Écarté : génère du texte générique, ne fait pas la mise en page. |
| wesleyscholl/book-generator | Scripts bash multi-IA + études de marché | Écarté (pas de licence, orienté non-fiction). |
| BrahimAkar/Amazon-KDP-Automater (×3 dans la liste) | Scraper KDP | Écarté (pas de licence, scraping). |
| sparkle666/amazon-profitable-keyword-generator | Extension Chrome mots-clés | Écarté (pas de licence) ; kdp-scout fait mieux. |
| digistoremaster/bookcoverly | Publicité pour un logiciel payant (README seul) | Écarté ; le calcul tranche/fond perdu est intégré à `kdpkit`. |
| TheLittleEngineers/Generic-eBook… | Modèle Word | Écarté (pas de licence ; nos PDF sont générés). |
| ahsaantariq12-at/e-Book-Formatter | Une page HTML | Écarté. |
| pbs/Canvas-Drawing-Tool, ashislaha/DrawingCanvas | Outils de dessin JS / iOS | Écartés (pas pour le print). Les illustrations sont dessinées en vectoriel par code. |
| Akylas/conty | Appli d'histoires audio pour enfants | Hors sujet KDP (piste future : version audio de Nova). |
| kyverno/KDP | « Kyverno Design Proposals » (Kubernetes) | Hors sujet (homonyme « KDP »). |
| Kilo-Projects-AtlasRearden8/ | Profil GitHub, pas un dépôt | — |

## 3. Livrables (`kdp/out/`)

```
01_dino_quest/{en,fr}/  DinoQuest_XX_Interior_8.5x11.pdf      intérieur 108 p.
                         DinoQuest_XX_Cover_Paperback.pdf      couverture complète 17,493 x 11,25 in
                         DinoQuest_XX_Front_Cover.jpg          face avant 300 dpi (A+ content, réseaux)
02_dino_abc/{en,fr}/    DinoQuestABC_XX_Interior_8.5x11.pdf   intérieur 82 p.
                         DinoQuestABC_XX_Cover_Paperback.pdf   17,435 x 11,25 in
03_nova/{en,fr}/        Nova_XX_Interior_8.5x8.5_bleed.pdf    intérieur 32 p. avec fond perdu (8,625 x 8,75 in)
                         Nova_XX_Cover_Paperback.pdf           17,325 x 8,75 in
                         Nova_XX_eBook_KKBC.pdf                eBook (import Kindle Kids' Book Creator)
                         Nova_XX_Kindle_Cover_2560.jpg         couverture Kindle 2560 x 2560
*/KDP_LISTING_EN.md, KDP_LISTING_FR.md                         fiche KDP prête à copier-coller
```

## 4. Qualité « au moindre détail »

* **Preflight automatique** (`python3 -m lib.qa`) : taille exacte de chaque page, nombre de pages, **toutes les polices incorporées**, et **distance mesurée de chaque caractère** au bord de coupe (intérieur ≥ 0,25 in, petit fond ≥ 0,375 in ; couverture ≥ 0,5 in, plus strict que KDP), **zone code-barres** vide. Résultat : PASS sur les 12 fichiers.
* **Tranche** calculée au millième selon l'encre et le papier (N&B blanc 0,002252 in/page ; couleur 0,002347 in/page). Texte de tranche seulement au-delà de 79 pages (#1 oui ; #2 et #3 non, normal).
* Pages de **coloriage imprimées au recto seul** (le verso est volontairement blanc, sans pastilles de test qui traverseraient).
* Les doubles pages lettre/mot du #2 tombent **en vis-à-vis** (page de gauche paire).
* Intérieurs N&B **sans aucune couleur** (flèches en gris foncé) ; album en **Premium Color** (obligatoire : en Standard Color, 8,5×8,5 exige 72 pages minimum).
* Polices **SIL Open Font License** (Lilita One, Fredoka, Nunito, Andika — Andika est conçue pour les lecteurs débutants), licences dans `kdp/fonts/`.
* Illustrations **100 % originales**, dessinées en vectoriel par le code (`lib/art.py`, `lib/icons.py`, `lib/night.py`) : netteté parfaite à toute taille, aucun problème de droits d'images.
* Mots-clés et titres **validés automatiquement** (`listings.py`) : ≤ 50 caractères/case, titre + sous-titre ≤ 200, pas de termes interdits (« free », « bestseller »…), pas de répétition inutile des mots du titre.
* PDF **reproductibles** (même source → même fichier, octet pour octet).

## 5. Publier sur KDP — pas à pas

1. **Compte** : kdp.amazon.com → infos fiscales + bancaires complètes.
2. **Créer → Livre broché** pour chaque titre/langue. Copier-coller depuis `KDP_LISTING_XX.md` : titre, sous-titre, série, auteur, description (HTML), 7 mots-clés, 3 catégories, âge.
3. **ISBN** : « Obtenir un ISBN KDP gratuit ».
4. **Paramètres d'impression** :
   * #1 et #2 : *Encre noire, papier blanc* · 8,5 × 11 in · **Sans fond perdu** · finition brillante.
   * #3 : ***Premium Color*, papier blanc** · 8,5 × 8,5 in · **Avec fond perdu** · finition brillante.
5. **Fichiers** : intérieur = `*_Interior_*.pdf` ; couverture = « Télécharger une couverture prête à imprimer » → `*_Cover_Paperback.pdf`.
6. **Contenu IA** : KDP demande si le texte/les images sont générés par IA. Ici texte et illustrations ont été produits avec l'IA → **répondez « Oui » honnêtement** (cela n'affecte pas la mise en vente, la non-déclaration peut entraîner un retrait).
7. **Aperçu** : lancer le Previewer en ligne, vérifier, puis **commander une épreuve** (proof) avant la mise en vente.
8. **Prix** : voir ci-dessous → Publier (validation sous ~72 h).
9. **eBook Nova** : *Créer → eBook Kindle* → Kindle Kids' Book Creator → importer `Nova_XX_eBook_KKBC.pdf` → couverture `Nova_XX_Kindle_Cover_2560.jpg`. Les cahiers #1 et #2 n'ont volontairement **pas** de version Kindle (on n'écrit pas sur une liseuse).
10. **Série** : créer la série « Dino Quest » et y lier #1 et #2 (page série Amazon = ventes croisées).

## 6. Prix & royalties (estimations à confirmer dans le calculateur KDP)

| Livre | Prix conseillé | Impression estimée | Royalty estimée |
|---|---|---|---|
| #1 Dino Quest | 9,99 $ / 9,99 € | ~2,84 $ | ~3,15 $ par vente (60 %) |
| #2 Dino Quest ABC | 9,99 $ (option lancement 7,99 $) / 8,99 € | ~2,84 $ | ~3,15 $ (60 %) · ~1,16 $ à 7,99 $ (50 %) |
| #3 Nova (broché) | 12,99 $ / 12,99 € | ~4,10 $ | ~3,70 $ (60 %) |
| #3 Nova (eBook) | 3,99 $ | — | ~2,60 $ (70 % moins frais de livraison du fichier) |

Clé : sur Amazon.com un broché **sous 9,99 $ ne touche que 50 %** → 9,99 $ est le point d'équilibre pour #1 et #2.

## 7. Plan de lancement

* **Timing** : publier #1 et #2 **dès maintenant** pour la fenêtre de Noël (KDP : jusqu'à 72 h de validation + délais de livraison). #2 a un second pic en janvier (bonnes résolutions/rentrée de janvier) et en août (rentrée).
* **Contenu A+** (gratuit) : utiliser les `*_Front_Cover.jpg` et des captures d'intérieur ; montrer le « avant/après » des flèches de traçage du #2.
* **Amazon Ads** : campagne automatique 5 $/jour par livre pendant 2 semaines, enchères basses (0,30–0,45 $), puis campagnes manuelles « exact » sur les termes qui convertissent ; couper les termes à ACOS > 60 %.
* **Avis** : uniquement des avis spontanés (la page finale de chaque livre invite à laisser un avis honnête) ; jamais d'avis échangés ou rémunérés (interdit par Amazon).
* **Vérifier les mots-clés** sur votre ordinateur avec `kdp-scout mine "dinosaur activity book"` (installé dans `.venv-kdp`).

## 8. Personnaliser / reconstruire

```bash
cd kdp
sed -i 's/Dino Quest Kids Press/Votre Maison/g' books/*/*.py listings.py   # votre nom d'éditeur / de plume
python3 build_all.py          # reconstruit les 6 éditions + fiches + preflight (~30 s)
```

Dépendances : `pip install reportlab pypdf pypdfium2 pillow shapely fonttools`.

Architecture :
* `lib/kdpkit.py` — géométrie KDP (tranche, fond perdu, zone code-barres), polices, rendu des traits d'écriture, constructeur de couverture, rendu/aperçus.
* `lib/strokes.py` — alphabet pédagogique à **ordre et sens des traits encodés** (majuscules, minuscules, chiffres, accents français).
* `lib/puzzles.py` — labyrinthes (avec solveur), mots mêlés (avec solutions), points à relier.
* `lib/art.py`, `lib/icons.py`, `lib/night.py` — illustrations vectorielles originales.
* `lib/qa.py` — preflight KDP · `listings.py` — fiches + validation · `build_all.py` — pipeline complet.

## 9. Suite logique (le moteur est prêt)

1. **Dino Quest Coloring** et **Dino Quest Math (K-1)** : réutilisent 90 % du code (série de 4 = coffret).
2. **Édition française en écriture cursive** (GS-CP) du #2 : très forte demande en France.
3. **Nova #2** (la rentrée, la peur du noir, l'arrivée d'un petit frère) → série « Petites Lumières ».
4. Éditions **espagnol / allemand** : il suffit d'ajouter une langue dans les dictionnaires de texte.
