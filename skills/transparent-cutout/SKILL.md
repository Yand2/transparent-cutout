---
name: transparent-cutout
description: Remove an image background and return an isolated subject as a verified, real-alpha RGBA PNG. Use for cutouts, transparent backgrounds, background removal, isolated subjects, or sticker PNGs. Reject rendered checkerboards and opaque RGB output.
---

# Transparent Cutout

Create a clean cutout from the user's supplied image. Preserve the intended foreground subject and its internal appearance. Remove the full backdrop, background fragments, color spill, cast shadows, floor shadows, halos, and scenery. Keep fine or semi-transparent foreground details when they belong to the subject. Leave transparent padding without clipping.

Do not add an outline, border, drop shadow, reflection, replacement background, gradient, solid fill, or transparency-grid pattern unless the user explicitly requests that separate visual effect.

## Required workflow

1. Use image editing to remove the background. Require a true RGBA PNG with alpha-zero background pixels and explicitly forbid white/black, gray/white, or colored checkerboard patterns.
2. Save the candidate as a `.png` file.
3. Run `python scripts/validate_transparency.py <candidate.png>` from this skill directory.
4. Inspect the candidate visually on at least one solid, contrasting background. A transparency grid displayed by an image viewer is acceptable only when the validator confirms the grid is not stored in opaque pixels.
5. Deliver the PNG only after both deterministic and visual checks pass.

If validation fails, do not present or deliver that candidate. Retry the background-removal edit or use a reliable segmentation method, then validate again. Stop after three failed attempts and explain that no compliant asset was produced; never relabel, rename, or claim an RGB/checkerboard image is transparent.

## Output contract

- PNG format in RGBA mode with an actual alpha channel.
- Background and every canvas corner have alpha 0.
- Subject pixels include alpha 255; anti-aliased subject edges may use partial alpha.
- The canvas includes comfortable transparent padding and does not clip the subject.
- No opaque checkerboard, backdrop, halo, or shadow is baked into the pixels.
- Prefer source resolution; do not upscale unless requested or necessary for visible quality.

Report briefly that deterministic alpha validation passed and provide the final PNG directly.
