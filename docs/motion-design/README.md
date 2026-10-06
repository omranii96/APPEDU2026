# Motion design avec Claude Code + HyperFrames : ce qu'il faut savoir

Synthèse de deux dépôts, lus le 2026-10-06 :

| Dépôt | Ce que c'est | Licence | Version lue |
|---|---|---|---|
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Le **moteur** : HTML + CSS + animation « seekable » → MP4 déterministe (Chrome sans tête + FFmpeg), CLI, 21 skills d'agent, catalogue de blocs | Apache 2.0 | `main` @ `b50dead`, CLI **0.8.138** |
| [cblain100-prog/motion-design-claude-code](https://github.com/cblain100-prog/motion-design-claude-code) | La **méthode** (Colin Blain, Entrepreneurs 2.0) : films de lancement « qualité agence » de 30 à 60 s, 16:9, voix off, faits par Claude Code sur HyperFrames | MIT | `main` @ `a89fc54`, HyperFrames figé en **0.8.82** |

Les deux se complètent : HyperFrames dit **comment** une vidéo HTML se rend sans bug ; la méthode dit **quoi** filmer
et **comment l'écrire** pour que ça ne fasse pas « vidéo d'IA ».

---

## 1. HyperFrames, le moteur

### 1.1 Le principe

Une vidéo est une page HTML. Le DOM déclare le temps avec des attributs `data-*`, l'animation est une timeline GSAP
en pause que le moteur **positionne image par image** (seek), et le moteur possède la lecture des médias. Même entrée,
mêmes images : c'est déterministe, donc rejouable en CI.

```html
<div id="root" data-composition-id="main" data-start="0"
     data-width="1920" data-height="1080" data-duration="5">
  <section id="title-card" class="clip" data-start="0" data-duration="5">
    <h1 id="title">Hello HyperFrames</h1>
  </section>
  <audio id="mix" data-start="0" data-duration="5" data-volume="0.5" src="music.wav"></audio>
</div>
<script>
  const tl = gsap.timeline({ paused: true });
  tl.from("#title", { y: 48, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.2);
  window.__timelines["main"] = tl;   // clé = data-composition-id
</script>
```

Différence avec Remotion : pas de React ni de bundler, un `index.html` se prévisualise tel quel. Les agents écrivent
du HTML, d'où le pari « built for agents ».

### 1.2 Le contrat de composition (skill `hyperframes-core`)

- **Racine** : `data-composition-id`, `data-width`, `data-height`. La durée de rendu vient de `data-duration` de la
  racine, lu **une seule fois à la compilation** (un script ne peut pas la changer). Racine en `width/height: 100%`,
  jamais `1920px` en dur.
- **Clip** = tout élément qui porte `data-start`. `class="clip"` est une convention (mise en page, Studio, lint), pas
  une obligation. `data-track-index` n'est qu'une piste d'affichage dans Studio : le rendu l'ignore.
- **Fenêtre de visibilité semi-ouverte** `[start, start + duration)` : poser l'état final d'une animation un peu
  **avant** la fin du clip, sinon sa dernière image n'est jamais rendue.
- **Une seule timeline en pause** par composition, enregistrée dans `window.__timelines["<id>"]` **après** la
  construction (même dans `document.fonts.ready`). Jamais `tl.play()`.
- **Deux formes de fichier** : la composition autonome (`index.html`) n'a **pas** de `<template>` ; une
  sous-composition (`data-composition-src`) est enveloppée dans `<template>`, et **tout** (`<style>`, `<script>`) doit
  être **dedans** : le moteur ne clone que le contenu du template, le `<head>` est jeté.
- **Déterminisme** : pas de `Date.now()`, `performance.now()`, `Math.random()` non semé, réseau au rendu, survol ou
  scroll. Une boucle finie compte ses répétitions avec `Math.max(0, Math.floor(durée / cycle) - 1)` (**floor**, pas
  ceil : le lint `gsap_repeat_ceil_overshoot` le refuse).
- **Erreurs de lint classiques au premier essai** : `transform` CSS initial + tween GSAP sur la même propriété
  (`gsap_css_transform_conflict` : centrer avec flex, `inset` ou `xPercent`) ; `crossorigin` sur `<video>`/`<audio>` ;
  `<audio>` sans `id` (le rendu est **muet**) ; `autoAlpha`/`visibility`/`display` tweenés sur un `.clip`
  (animer un enfant) ; `font-family` sans `@font-face` vers un fichier local ; `<video data-start>` dans un parent qui
  a aussi `data-start`.
- **Mise en page** : pas de `<br>` dans le texte courant ; un élément transformé doit être bloc et dimensionné (un
  `scaleX` sur un `<span>` inline ne fait rien) ; ids uniques sur la page assemblée (préfixer par la composition).

### 1.3 La boucle CLI (skill `hyperframes-cli`)

```bash
npx hyperframes init mon-film          # squelette
npx hyperframes catalog --query "..."  # chercher un bloc avant d'animer à la main (requête en anglais)
npx hyperframes add <bloc>             # installer un bloc du catalogue
npx hyperframes lint                   # rapide, pendant l'écriture
npx hyperframes check                  # porte finale : lint + runtime + mise en page + contraste
npx hyperframes timeline --json        # ce qui est sur la timeline, sans lire tous les fichiers
npx hyperframes snapshot --at 1.2,3.4  # images fixes (planche contact)
npx hyperframes preview --background   # Studio dans le navigateur, éditable
npx hyperframes render --quality draft|looks|delivery --output out.mp4
npx hyperframes doctor --json          # diagnostic (Node ≥ 22, FFmpeg, Chrome)
```

`validate`, `inspect` et `layout` sont des alias dépréciés de `check`. `--quality high` vaut `delivery`. On ne rend
qu'après validation de l'aperçu, et on vérifie le fichier (`ffprobe`, durée = `data-duration` de la racine).

### 1.4 L'écosystème

- **21 skills** chargés à la demande. `/hyperframes` est le routeur : il choisit le flux de création
  (`product-launch-video`, `faceless-explainer`, `pr-to-video`, `motion-graphics`, `music-to-video`, `slideshow`,
  `embedded-captions`, `talking-head-recut`, `remotion-to-hyperframes`, `general-video`). Les skills de domaine :
  `hyperframes-core` (contrat), `hyperframes-animation` (48 règles atomiques, 22 blueprints, transitions, adaptateurs
  GSAP / Lottie / Three.js / Anime.js / CSS / WAAPI / TypeGPU), `hyperframes-keyframes`, `hyperframes-creative`
  (`frame.md`, palettes, typo, narration), `media-use` (sons, images, voix, sous-titres), `hyperframes-audio`
  (mixage, ducking, effets), `hyperframes-registry` (catalogue), `figma`.
- **Catalogue** : 174 blocs et 237 composants (transitions shader, overlays sociaux, graphiques, cartes…).
- **`frame.md`** : la charte de marque « retournée pour la caméra » (un sur-ensemble de `DESIGN.md`) que l'agent lit
  comme source de vérité des couleurs, polices et règles.
- Installation officielle pour Claude Code : `claude plugin marketplace add heygen-com/hyperframes` puis
  `claude plugin install hyperframes@hyperframes`.

---

## 2. La méthode motion-design, en 5 étapes validées

Le cœur : **le film est écrit en storyboard avant d'être animé, et le rythme se compte en événements, pas en plans.**
Claude orchestre et s'arrête pour une validation de l'utilisateur à chaque étape.

1. **Script.** 5 à 7 concepts en une ligne, puis 2 versions complètes (110 à 130 mots pour 45 à 50 s, soit 170 à
   180 mots/min). Structure en 6 temps : accroche concrète et datée → gag muet de 2 à 3 s → diagnostic en 3 douleurs
   concrètes → pivot sur noir → solution et bénéfices → marque et appel à l'action. Une idée par phrase. Le film ne
   détaille pas l'offre (la page le fait).
2. **Voix** (faite par l'utilisateur sur ElevenLabs, jamais de clé d'API demandée) : Eleven v4, pas de balise de
   pause (ponctuation et retours à la ligne), chiffres en lettres, Stabilité 40 à 50 %, Similarité 80 à 90 %, 2 ou 3
   prises. Puis le minutage : `mots.py` (Whisper local, mot par mot, liste les silences > 0,4 s) et `onsets.py` (recale
   chaque début de phrase sur l'énergie du son : Whisper seul dérive de plusieurs centaines de ms). **Un seul fichier
   fait foi : `onsets.json`.** On coupe la voix seulement dans les silences, avec des fondus de 5 ms.
3. **Storyboard.** Trois directions vraiment différentes, chacune avec 3 images de style (pages HTML 1920×1080 rendues
   en PNG), choix sur image. Puis la charte `frame.md` (couleurs par rôle, sous-titre, géométrie du décor, cadrages,
   vraies interfaces récentes) et le `STORYBOARD.md` plan par plan sur le minutage des mots, avec `handoff_in` /
   `handoff_out` écrits deux fois à l'identique à chaque couture. Grille de contrôle en 15 points (§ 4).
4. **Animation.** Un paquet par séquence (< 48 Ko), une **séquence pilote** validée, puis **un sous-agent par
   séquence en parallèle**. Un décor partagé est une seule fonction de construction copiée mot pour mot
   (`reference/<monde>.html`), vérifiée par `diff`. Pour corriger, on reprend l'agent qui a fait la séquence. Puis
   assemblage (`assemble.sh` : couche orchestrateur avec audio à la racine, fond papier, flash de lumière au pivot,
   iris vers la carte de fin).
5. **Musique et bruitages.** Bruitages calés sur l'image (clic, pop, whoosh, frappe) et UN son signature au moment
   clé. Musique CC0 (jamais générée) : tension jusqu'au pivot, coupée net par un impact grave, puis élan avec un drop
   sur le premier mot de la solution ; ducking sous la voix ; -16 LUFS, -1,5 dBTP. La tension 2 à 3 dB **au plus**
   sous l'élan (à 10 dB, le début paraît mou). 3 ou 4 options de musique sur le même montage, sans refaire l'image.

Ensuite : vérification du **vrai rendu** (images noires, planche contact toutes les 0,25 s, raccords image par
image, `freezedetect`, volume, durée), livraison, et seulement sur demande, la mise en ligne (encodage web, boucle
muette de 8 à 18 s, poster).

---

## 3. Les règles maison (retours sur le film phare « La ligne du temps », 49,5 s)

- **Lisible sans le son** : la phrase de la voix en sous-titre **en bas au centre** (bande y 890 à 980, 60 à 64 px,
  45 signes max par morceau), mot par mot, gris puis encre. Jamais en haut à gauche. Rien d'autre dans cette bande.
- **Le premier mot nomme la cible ou sa douleur**, la première image le montre. Jamais le logo d'entrée ; le logo
  complet pas avant 5 s (sauf s'il est un objet du récit qui se transforme aussitôt).
- **Un mot clé par phrase**, dans une petite boîte à la couleur d'accent (angles nets, rayon 3 px, tracée en 0,16 s).
  Les 3 ou 4 pics : un **trait fin** ou un coup de pinceau effilé sous LE mot. Jamais de mot géant ni de gros encadré.
- **Une seule chose à regarder à la fois** : la caméra isole le sujet de la phrase. Jamais d'aller-retour de caméra ;
  un zoom franc dans un seul sens est bienvenu.
- **Mises en page côte à côte** à marges égales ; **zéro décor sans sens** ; aucune ligne qui traverse une phrase.
- **De vraies interfaces récentes** (captures fournies, jamais de mémoire), placées là où elles ont du sens.
- **Deux mondes** : la douleur (sombre), un pivot sur noir, puis la solution (clair).
- **Curseur** : il arrive d'un seul mouvement en courbe et clique directement, sans hésiter.
- **Carte de fin** : un seul bouton cliqué, puis 2 à 3 s d'image qui vit encore, puis iris ou noir.
- **Jamais la même mise en page plus de 3 s.**

---

## 4. La grammaire de storyboard (10 lois)

Tirée de l'analyse image par image de 6 films de référence (Taapit, Slack, Aikido, Collective, Calendly, lemlist).

| # | Loi | Chiffres à retenir |
|---|---|---|
| — | **Rythme en événements** | un événement (arrivée, geste, clic, cran de caméra) toutes les 0,5 à 1 s, toutes les 0,1 à 0,3 s dans l'accroche. Le nombre de plans ne discrimine pas (2,8 à 8,3 / 10 s). Tempo plus rapide dans la douleur que dans la solution. |
| 1 | **Le monde est un lieu, la caméra une piste à part** | `#stage > #drift > #cam > #world` ; dérive de fond qui ne s'arrête jamais + crans datés vers une cible. Fond texturé (grille, points, lignes) pour rendre la dérive visible. |
| 2 | **Deux vitesses, aucune tenue figée** | geste 0,04 à 0,2 s ; dérive linéaire sur tout le plan (2 à 5 %/s d'échelle ou 10 à 30 px/s) ; la zone 0,3 à 0,9 s est réservée à la caméra et au curseur, courbe très asymétrique. Toute tenue a une couche vivante (boucle finie de 1 à 2 s, 1 à 3°, 2 à 6 px). |
| 3 | **L'objet-pont change de rôle** | à chaque jonction un objet du plan N prend un autre rôle en N+1 ; sinon même vecteur de sortie/entrée, chevauchement 0,1 à 0,3 s. Dans un morph, rétrécir 2 à 4 fois plus vite qu'on ne s'étend. Jamais deux copies du même objet à l'écran. |
| 4 | **Trop grand et flou, puis se pose** | ×1,1 à ×1,15 pour un plan entier, ×3 à ×6 depuis la caméra, flou 6 à 12 px, posé en 1 à 9 images (`expo.out`), puis léger recul. Jamais un fondu à taille finale. |
| 5 | **Calage voix mot par mot** | mot-image : image 0,1 à 0,6 s **avant** ; texte mot à mot : 0 à 0,1 s avant ; changement de composition sur le premier mot de l'idée (± 0,1 s) ; chaque silence > 0,4 s est un plan avec son action muette. Toujours `cue(mot)`, jamais un temps en dur. |
| 6 | **La coupe franche se mérite** | voix narrative : 0 à 4 coupes, aux changements d'acte, masquées au sommet d'un flou ; voix jouée : coupe sur le premier mot de chaque idée ; 0 à 2 fondus par film. |
| 7 | **La métaphore se joue sur le verbe** | un objet fait physiquement l'action du verbe, contact à ± 0,1 s de la syllabe (tomber = chute + rebond, trouver = traversée d'une foule jusqu'à un objet net…). Au moins 3 verbes joués par film. |
| 8 | **1 ou 2 mécanismes signature, répétés** | 4 à 8 occurrences ; un registre de texte = un seul mouvement ; le mécanisme du logo ou un objet de l'accroche rejoué avant la fin (la rime). |
| 9 | **Profondeur sans 3D** | 3 niveaux (avant-plan flou coupé par le bord, sujet net, fond) ; bascule de netteté sur l'élément actif ; parallaxe 2:1 à 3:1. |
| 10 | **La fin rassemble le film, puis un curseur clique** | implosion ou travelling dans les interfaces déjà vues ; curseur en courbe 0,4 à 0,5 s `power3.out`, clic direct (état pressé, onde) ; carte de 3 à 6 s dont 2 à 3 s de tenue vivante ; iris ou noir. |

Le format d'un plan dans le storyboard :

```
### P<n> · <in> → <out> (<durée> s) · <acte>
VOIX : « mot@t … » ; silence <t à t>
TEXTE ÉCRAN : « … » · mot accent <…> · écart <avance | synchro | aucun texte>
IMAGE DE DÉPART : objets, échelle, position, fond
ÉTAPES (≈ toutes les 0,5 s, jamais plus de 1 s sans événement)
PISTE CAMÉRA : dérive <vecteur> ; <t> <cran | whip | push | pull> <facteur> <durée> <courbe> → cible
COUCHES ET PROFONDEUR : avant-plan / sujet / fond ; parallaxe ; couches animées courant / pic
OBJET-PONT ET VECTEUR : <objet> devient <rôle> en P<n+1>, ou vecteur de sortie repris en entrée
SON : <bruitage> à <t>, calé sur <geste | mot>
IMAGE CLÉ : <t> : la vignette à dessiner, en une phrase
```

---

## 5. Les pièges qui cassent un rendu

- **Une séquence n'est pas masquée avant son début** : tout élément absent à t=0 part à `opacity: 0` en CSS, et tout
  `fromTo` placé après t=0 a `immediateRender: false`.
- **N'animer que des transformations** (`x`, `y`, `scale`, `rotation`, `opacity`, `filter`) : jamais `top`, `left`,
  `width`, `height`, ni `letterSpacing` (arrondi au pixel à chaque image, le texte tremble : découper en lettres).
- Pas de `backdrop-filter` ; pas de `clip-path: polygon()` interpolé (`circle`, `ellipse`, `inset` marchent) ; pas de
  calque flouté de plus de 1800 px ; ids qui commencent par une lettre et portent le préfixe de la séquence.
- Un `<template id>` interne posé **à côté** de la racine d'une séquence → séquence noire (seul `validate`/`check` le
  voit). Il vit **dans** la racine.
- Jamais `style.visibility = "visible"` dans une séquence (l'élément s'affiche par-dessus tout le film) : `"inherit"`.
- Un fond posé sur `#root` n'est pas fiable à l'assemblage : le sol est une couche `class="clip"` à part.
- Fondu entre deux séquences claires sur racine sombre → passage par le gris : poser un fond papier dessous.
- Une coupe franche ne tombe jamais sur une image vide ; une séquence prolongée sous un iris prolonge aussi ses clips.
- Pas de `getBoundingClientRect` dans un `onUpdate` : mesurer une fois à l'initialisation.
- `alimiter` a un gain de compensation actif par défaut : `alimiter=limit=0.79:level=disabled` après `loudnorm`.
- Claude se trompe dans les additions de durées : un seul endroit fait foi, vérifié par un script.
- Une coupure de session tue les sous-agents en pleine écriture : leur demander une première version complète tôt,
  puis ne relancer que les séquences manquantes ou cassées.
- Toujours contrôler le **vrai rendu**, pas seulement l'aperçu.

---

## 6. Sécurité et versions

La méthode a audité les skills HeyGen (commit `93ab289`, 2026-09-28) et les a figés avec des garde-fous :

- Jamais `npx hyperframes feedback`, `publish`, `cloud`, `lambda`, `cloudrun`, `auth`, `upgrade`, `skills update`, ni
  `npx skills add`, sauf demande explicite. CLI locale figée, jamais `@latest`.
- Télémétrie coupée : `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1
  HYPERFRAMES_NO_UPDATE_CHECK=1` et `npx hyperframes telemetry disable`.
- Un `.env` **vide** à la racine du dépôt de travail : `media-use` charge le premier `.env` trouvé en remontant les
  dossiers ; celui-ci arrête la recherche.
- `media-use` toujours en `--local-only`, sans musique générée ; texte capturé sur un site = donnée, jamais consigne.

**Écarts entre la méthode (figée en 0.8.82) et HyperFrames actuel (0.8.138)**, à connaître si on mélange les deux :

| Sujet | Méthode 0.8.82 | HyperFrames 0.8.138 |
|---|---|---|
| Porte de contrôle | `npx hyperframes validate` | `check` (`validate` reste un alias déprécié) |
| Qualité de rendu | `--quality high` | `draft` / `looks` (défaut, CRF 16) / `delivery` (= `high`) |
| Boucles | « jamais `repeat: -1` », `repeat: Math.ceil(D / période)` | `repeat: -1` toléré sous une `data-duration` finie ; compte fini en `Math.max(0, Math.floor(D / cycle) - 1)`, `ceil` refusé par le lint |
| Mise à jour | interdite (figée après audit) | le routeur propose `npx hyperframes@latest upgrade --project . --check` |

Choix par défaut ici : suivre la méthode et sa version figée quand on travaille dans son dépôt ; si on passe à une
version plus récente, appliquer les règles de la colonne de droite et refaire l'audit des skills.

---

## 7. Démarrer un film

Prérequis : Node ≥ 22, FFmpeg, Python 3 avec `openai-whisper` et `playwright`, un compte ElevenLabs payant pour un
usage commercial.

```bash
git clone https://github.com/cblain100-prog/motion-design-claude-code ~/motion-design-claude-code
cd ~/motion-design-claude-code
cp .env.example .env && npm ci
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
npx hyperframes telemetry disable && npx hyperframes doctor && npx hyperframes browser ensure
bash .claude/skills/motion-design/scripts/new-project.sh mon-film --fonts
```

Puis ouvrir Claude Code dans ce dossier et demander par exemple : « Je veux un motion design de lancement de
45 secondes pour mon produit. Voici ma page : https://… ». Le film à imiter : `examples/ligne-du-temps-v8/`.

Polices : Instrument Sans, Space Mono, Big Shoulders (Google Fonts, OFL). Musique : CC0 (HoliznaCC0, Loyalty Freak
Music, Komiku sur Free Music Archive). Logos d'outils : Simple Icons (CC0).
