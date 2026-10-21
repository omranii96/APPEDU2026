---
description: Produce studio-quality product photography and commercial imagery with lighting inferred from the product type
---

Run the gflow-product-visuals skill. Capture the product brief (category, material, mood, placement), run `gflow doctor`, infer lighting, backdrop, and composition from the product type, generate variations with `gflow image --model imagen-4 --outputs 4` (inheriting `--project <brand>` if a brand exists), let the user select the hero direction, generate the full set (studio, lifestyle, detail, scale), upscale the winners with `--upscale 4k`, export platform-matched crops with `gflow batch`, and run the full quality gate before delivering. Execute every gflow command with one shared `--project <name>` for the run (the brand project if one exists) and `--no-headed`; only `gflow auth login` runs headed.
