# « La porte unique » : l'importance d'un ITSM / ESM

Film de 36,3 s, 16:9, 1920 × 1080, 30 i/s, voix off d'homme en français (« Ken »), sous-titré mot par mot (lisible
sans le son). Public : direction générale et DSI. Fait avec la méthode de
[motion-design-claude-code](https://github.com/cblain100-prog/motion-design-claude-code) et le moteur
[HyperFrames](https://github.com/heygen-com/hyperframes) 0.8.82 (voir `docs/motion-design/README.md`).

- `la-porte-unique.mp4` : la vidéo (encodage web, 5,6 Mo, -16 LUFS).
- `poster.jpg` : image d'affiche (carte de fin).
- `source/` : le script, le storyboard, le minutage des mots, la composition HTML et les scripts de son.

## Le film

1. **La douleur (0 à 12,2 s)** : un nouvel arrivant, premier jour, sans ordinateur, ni badge, ni accès. L'horloge
   tourne. Sa demande ricoche de porte en porte (Informatique, RH, Finance), chacun la suit dans son propre tableau,
   puis les lumières s'éteignent.
2. **Le pivot (12,2 à 15,4 s)** : « Et si tout passait par une seule porte ? », une porte de lumière qui s'ouvre.
3. **La solution (15,4 à 31,3 s)** : l'ITSM range le service informatique (catalogue, ticket suivi, délai tenu),
   puis l'ESM branche toute l'entreprise sur le même portail. Une seule demande coche la checklist du début, et la
   direction voit où le temps se perd.
4. **La fin** : « Une seule porte pour tous vos services. », un bouton « Lancer votre portail » cliqué.

La vidéo ne porte aucune marque et ne cite aucun chiffre. Le nom, les couleurs et le texte du bouton se changent
dans `source/index.html`, puis on refait le rendu.

## Refaire le rendu

Dans un dossier de projet de la méthode (HyperFrames 0.8.82, polices et GSAP en local, déjà dans `source/assets/`) :

```bash
# 1. Voix, au choix :
#  a. une prise externe du script entier (voix « Ken », Higgsfield) : découpée dans ses silences, chaque morceau
#     transcrit par Whisper et rangé dans les 12 phrases ; une voix rapide demande des coupes plus fines
TAKE_MIN_PAUSE=0.05 TAKE_FLOOR_DB=-34 python3 tools/build_voice_take.py <projet> <prise.wav>
#  b. ou Piper « Tom » (fr_FR-tom-medium) en local via sherpa-onnx, la meilleure de 8 prises par phrase
python3 tools/build_voice.py <projet>
# les deux écrivent assets/audio/voix-raw.wav, onsets.json et la durée du rendu dans index.html ; la composition
# et la musique se calent dessus (gag muet, extinction, flash du pivot, carte de fin)
# 2. Musique originale synthétisée, bruitages media-use calés sur l'image, mixage
python3 tools/build_audio.py <projet> <dossier sfx de media-use>
# puis normalisation à -16 LUFS et -1,5 dBTP max. : assets/audio/mix.wav
# 3. Contrôle et rendu
npx hyperframes check && npx hyperframes render --quality high --output renders/video.mp4
```

Les fichiers audio ne sont pas versionnés (ils se régénèrent avec les deux scripts).

## Crédits

- Voix : « Ken », voix prédéfinie de Higgsfield (modèle Seed Audio), une prise du script entier. La première version
  utilisait le modèle Piper `fr_FR-tom-medium` (sherpa-onnx), généré en local ; elle reste dans l'historique git.
- Musique : composée et synthétisée pour ce film (aucun échantillon externe).
- Bruitages : bibliothèque `media-use` de HyperFrames, Pixabay Content License.
- Polices : Instrument Sans et Space Mono (SIL Open Font License), via Fontsource.
- Animation : GSAP 3.14.2.
