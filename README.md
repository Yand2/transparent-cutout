# Transparent Cutout

A Codex plugin for removing image backgrounds and returning only verified real-alpha PNG cutouts.

The plugin rejects RGB images, opaque checkerboard patterns, missing alpha-zero pixels, nontransparent corners, fully transparent files, and clipped subjects. A candidate is delivered only after deterministic validation and visual inspection on a solid background.

## Structure

- `.codex-plugin/plugin.json` — plugin manifest
- `skills/transparent-cutout/SKILL.md` — cutout workflow and delivery contract
- `skills/transparent-cutout/scripts/validate_transparency.py` — mandatory PNG/alpha validator
- `skills/transparent-cutout/scripts/test_validator.py` — validator regression tests

## Validate a cutout

```powershell
python skills/transparent-cutout/scripts/validate_transparency.py output.png
```
