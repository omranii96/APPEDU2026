# Catalogue des skills de motion design et de design web

Installés le 2026-10-21 après audit : licences lues, recherche de commandes réseau ou d'exécution distante, de
télémétrie, d'envoi de données, de caractères invisibles et de consignes cachées. Chaque source est figée sur le
commit audité (colonne « Source »). Ne jamais les mettre à jour par `npx skills add`, un `@latest` ou la pointe d'une
branche : refaire l'audit, puis changer le commit dans `tools/motion-skills/fetch.sh` ou recopier le dossier.

Trois statuts :

- **Versionné** : copié dans `.claude/skills/` et commité (licence MIT).
- **Local** : licence qui autorise l'installation mais pas la redistribution. Récupéré au commit audité par
  `bash tools/motion-skills/fetch.sh skills`, ignoré par Git. À relancer au début d'une nouvelle session cloud.
- **Référence** : à étudier, pas un skill actif. `bash tools/motion-skills/fetch.sh references` les place dans
  `vendor/web-references/`. Sans licence : on s'en inspire, on ne copie pas le code.

## Vidéo et motion design

| Skill | Pour quoi | Source (commit) | Licence | Statut |
|---|---|---|---|---|
| `motion-design-hyperframes` | La méthode de ce dépôt (HyperFrames, film en 5 étapes) | ce dépôt | — | Versionné |
| `lottie-motion-design` | Principes de motion UI : durées, courbes, chorégraphie, principes Disney | LottieFiles/motion-design-skill (f9a8a04) | MIT | Versionné, renommé |
| `howseen-motion-design` | Pipeline 100 % code d'un studio (moteur `seek(t)`, rendu Playwright) | howseen-ai/claude-motion-design (3d90d34) | MIT | Versionné, renommé, en référence |
| `business-motion-film` | Publicités courtes pour une vraie entreprise, boucle de critique indépendante | echris6/motion-video-kit (e4b1c00) | MIT | Versionné |
| `opus-motion` | ~109 motions Remotion paramétrables, 33 transitions, 19 recettes | GovinduSasanka/opus-motion-library (d3876a4) | MIT | Versionné ; bibliothèque en `vendor/` (fetch `libraries`) |
| `kinetic-reel` | Showreels en typographie cinétique, couches three.js | VisualxIntelligence/motion-tools-and-skills (f8cb410) | MIT | Versionné |
| `painted-animation` | Dessin animé aquarelle et encre (p5.brush) | idem | MIT | Versionné |
| `lemo-opuscar` | Courts métrages en code dans des styles nommés (peinture, ukiyo-e…) | idem | MIT | Versionné |
| `3d-product` | Films produit dans Blender, du brief au grading | idem | MIT | Versionné |
| `motion-graphics-music-video` | Clips musicaux à personnages (génération fal.ai, payante) | idem | MIT | Versionné |
| `liam-motion-library` | Bibliothèque d'effets Remotion à codes d'appel | linhaixin45-cmyk/code-liam-motion-library (80e9a09) | Licence Code Liam : **non commercial** | Local |
| `video-talkcraft` | Vidéos « face caméra » en chinois → Remotion | Vincentwei1021/video-talkcraft (a7c29ed) | PolyForm Noncommercial : **usage commercial sur autorisation** | Local (sans `gallery/`) |

## Méthode de production vidéo (VisualxIntelligence, MIT, versionnés)

`video-workflow` (reprendre un projet), `evidence-story-script` (script vérifié), `video-shot-planner` (découpage en
plans), `voice-subtitle-sync` (voix et sous-titres), `explainer-motion` (motion explicative), `generated-broll`
(b-roll généré, budget autorisé), `video-reference-study`, `video-source-index`, `cover-art-direction`,
`cover-independent-review`, `video-release-qa`. Les textes sont en chinois, avec une version anglaise `SKILL.en.md`.

## Sites web et motion d'interface

| Skill | Pour quoi | Source (commit) | Licence | Statut |
|---|---|---|---|---|
| `transitions-dev` | Transitions CSS prêtes pour l'UI (modales, menus, toasts, onglets…) | Jakubantalik/transitions.dev (7ec0b0b) | Transitions.dev : usage libre, pas de redistribution de la collection | Local |
| `transitions-polish` | Recaler le motion existant sur une échelle de tokens | idem | idem | Local |
| `transitions-ui-generation` | Effet « l'IA génère l'interface » (wireframe → UI) | idem | idem | Local |
| `scroll-craft` | Landing pages pilotées par le scroll, vérifiées par captures | nateherkai/scroll-craft (75d81f7) | MIT | Versionné |
| `alive-web` | Expériences immersives à la Lusion (WebGL, physique, scroll) | danielyerushalmi/alive-web (a80b5ee) | MIT | Versionné |
| `claude-club-motion-sites` | 547 recettes de sites animés (héros, pricing, fonds…) | Samin12/claude-club-motion-library-skill (4554656) | MIT (médias tiers non couverts) | Versionné ; catalogue en `vendor/` (fetch `libraries`) |
| `ui-component-sourcing` | Où prendre des composants gratuits, et à quelles conditions | unfoldingdimensions/ui-design-sourcing-skill (e1b7df8) | MIT | Versionné |
| `forge` | Design system React `wss3-forge` | Webba-Creative-Technologies/forge (7572eb8) | MIT | Versionné, déclencheur restreint |
| `hallmark` | Design anti « AI slop » : macrostructures, tokens verrouillés, textes honnêtes sans chiffres inventés | Nutlope/hallmark (13ac0ec) | MIT | Versionné (dossier `skills/hallmark` + LICENSE racine) |

## Génération d'images et de vidéos avec Google Flow (swissmarley/gflow-skills, 9ac3aad, MIT, versionnés)

Préfixés `gflow-` : `gflow-brand-identity` et `gflow-character-pipeline` (fondations), puis `gflow-immersive-web`,
`gflow-motion-graphics`, `gflow-cinema-production`, `gflow-music-video`, `gflow-social-content`,
`gflow-product-visuals`, `gflow-editorial-design`, `gflow-design-docs`, `gflow-game-assets`,
`gflow-architectural-viz`. Ils pilotent la CLI `gflow` (paquet npm `gflow-skills`) et un compte Google Flow,
qui ne sont pas installés ici.

## Références (`vendor/web-references/`, à étudier)

| Dossier | Ce qu'on y apprend | Source (commit) | Licence |
|---|---|---|---|
| `scroll-craft-site` | Site React construit avec scroll-craft | cristianoleamiranda-dotcom/scroll-craft (b9c8e5b) | MIT |
| `web-portfolio` | Portfolio 3D « terminal », glitchs | mscbuild/web-portfolio (fd81ece) | MIT |
| `mctc-website` | Page unique à graphe de nœuds animé | NaeMyoAungKhing/mctc-website (cf94a8d) | aucune : s'inspirer seulement |
| `futureride` | Vitrine de véhicules three.js devant un mot géant | thebuggeddev/futureride (aa6b4c5) | aucune |
| `3d-motion-website` | Parcours 3D au scroll en React Three Fiber | pennyp973/3d--motion-website (c8d5a41) | aucune |
| `animated-website-css-html` | Site animé en HTML et CSS seuls | sukhmandult4-web/Animated_website_CSS_HTML (22655ec) | aucune |
| `immersive-3d-site-skill` | Skill de site 3D au scroll (Three.js + GSAP) | ronniejbotes/claude-skills (266aa8a) | aucune : pas installé comme skill |
| `pluviobyte-video-production-skills` | 4 skills vidéo (direction de motion, réplique de référence…) | Pluviobyte/video-production-skills (e19f1f3) | aucune : pas installé comme skill |
| `full-stack-audit` | Skill d'audit complet d'un site (sécurité, UX, perf, SEO) | jalaalrd/full-stack-audit (78e2a5c) | aucune : pas installé comme skill |
| `seo-blueprint-audit` | Audit SEO de tout un site, note par page | youtube-jono/seo-blueprint-audit (4022368) | aucune : pas installé comme skill |
| `seo-audits-toolkit` | Application web d'outils d'audit SEO (OSAT) | StanGirard/seo-audits-toolkit (c3e95fc) | aucune : ce n'est pas un skill |

## Audit de sites web (lot 3)

| Skill | Pour quoi | Source (commit) | Licence | Statut |
|---|---|---|---|---|
| `extract-design` | Extrait le langage de design d'un site (couleurs, espacements, typo) | Manavarya09/design-extract (a1805d1) | MIT | Versionné ; CLI `designlang` à installer (`npm install -g designlang`) |
| `web-audit` | Audit structuré d'une page : SEO technique, contenu, perf, UX | creativedeals/free-claude-skill-web-audit (6f8adcb) | CreativeDeals (libre, créditer, ne pas revendre) | Versionné |
| `pre-launch-audit` | Checklist avant mise en ligne d'un site | bzsasson/pre-launch-audit-skill (f9ccf06) | MIT | Versionné (nom corrigé en slug) |
| `seo-audit` | Audit SEO/technique/IA via la CLI SEOmator (373 règles) | seo-skills/seo-audit-skill (fac4b75) | MIT | Versionné ; CLI SEOmator à installer à l'usage |
| `website-security-shield` | Audit de sécurité web (OWASP, WSTG) + test d'intrusion autorisé, bridé par un fichier de périmètre signé | DataSpoof/website-security-shield (ba181a8) | MIT | Versionné ; déclencheur resserré sur les demandes de sécurité |

## Collection rampstack (lot 3, 107 skills, MIT, versionnés)

rampstackco/claude-skills (9b90db2), MIT : 107 skills couvrant tout le cycle d'un site (marque, design,
contenu, SEO, dev, ops, croissance, recherche), déclenchés à la demande. Noms conservés, sans préfixe (aucun ne
rentrait en collision avec les skills déjà installés). Seul le dossier `skills/` est repris ; les copies `dist/`
(pour d'autres agents) sont ignorées. Quelques-uns pilotent un MCP Ahrefs, optionnel.

## Outils de sécurité offensive (lot 3, NON installés)

Ces outils ne sont **pas** des skills actifs et **ne sont pas récupérés automatiquement**. À n'utiliser que contre
des cibles pour lesquelles tu as une autorisation écrite. `bash tools/motion-skills/fetch.sh security` les place dans
`vendor/security-tools/` (ignoré par Git) à leur commit audité, uniquement sur demande explicite.

| Dossier | Ce que c'est | Source (commit) | Licence |
|---|---|---|---|
| `recon` | Reconnaissance OSINT / veille concurrentielle (sites, API, domaines, IP, ports) | g-baskin/recon (df6894d) | GPL-3.0 |
| `watchtower` | Automatisation de tests d'intrusion pilotée par des agents LLM (app autonome, pas un skill) | fzn0x/watchtower (a854009) | MIT |

## Écartés

- `transitions-agent` (transitions.dev) : pilote un service payant par `npx transitions-agent@latest` (version non
  figée), envoie le code à `api.transitions.dev`, et sa consigne « ALWAYS use » prendrait la main sur les demandes.
- `refine-live` (transitions.dev) : agent interne de leur application.
- `papermotion` (VisualxIntelligence) : ne fonctionne qu'à l'intérieur de son projet de départ.
- techmonk45/scroll-craft : ancienne copie (0.3.0) de nateherkai/scroll-craft (0.3.1), installé à la place.
- DGILADS/cadife-tour-claude : dépôt vide (un README d'une ligne).

## Modifications apportées (licence MIT : modifications autorisées)

- Renommages pour éviter les doublons de noms : `motion-design` (LottieFiles) → `lottie-motion-design`,
  `motion-design` (Howseen) → `howseen-motion-design`, les 12 skills Google Flow → `gflow-*` (et leurs renvois
  croisés).
- `howseen-motion-design` : description préfixée « Reference only… » (ses chemins, couleurs et faits sont ceux du
  studio Howseen, jamais ceux de ce projet).
- `forge` : déclencheur limité aux projets qui utilisent Forge (au lieu de « toute UI React »).
- `claude-club-motion-sites` et `opus-motion` : chemins pointés vers `vendor/`.
- Les 11 skills de production vidéo sont sortis de leur dossier parent (un dossier par skill) et gardent chacun la
  licence et les notices du parent.

## À savoir avant usage commercial

- `liam-motion-library` et `video-talkcraft` : non commerciaux sans accord de leur auteur.
- `claude-club-motion-sites` : images, vidéos, polices et marques citées dans les recettes gardent leurs droits.
- Les skills qui génèrent (fal.ai, kie.ai, Google Flow, Fish Audio) demandent un compte et une clé d'API, et
  consomment des crédits.
