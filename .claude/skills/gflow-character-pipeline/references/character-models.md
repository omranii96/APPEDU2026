# Character Model Selection

| Model | Use when |
|-------|----------|
| nano-banana-pro | Default. Highest fidelity, best identity consistency. |
| nano-banana-2 | Faster iteration during concept exploration; switch to pro for final. |

## Presets (`--preset`)
- `familiar` - relatable, grounded human characters.
- `eccentric` - stylized, exaggerated features.
- `wicked` - villains, dark archetypes.
- `fantastical` - creatures, non-human, high fantasy.

## Tips
- Provide 1-3 reference images via `--image` for stronger consistency.
- Use `--from-project <name>` to pull existing project assets as references.
- Assign a `--voice` so downstream video skills can use consistent narration.
