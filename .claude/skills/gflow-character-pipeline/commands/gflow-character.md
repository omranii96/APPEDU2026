---
description: Design a consistent, reusable character with Google Flow (concept exploration to registered character)
---

Run the gflow-character-pipeline skill. Gather the character brief (name, role, visual traits, personality, voice), explore 4-8 concepts with `gflow image`, let the user select, register with `gflow character create`, validate consistency across test scenes, and deliver a reference sheet plus the reusable character name. Execute every gflow command with one shared `--project <name>` for the run (the brand project if one exists) and `--no-headed`; only `gflow auth login` runs headed.
