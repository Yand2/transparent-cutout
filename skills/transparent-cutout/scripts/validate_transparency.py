#!/usr/bin/env python3
"""Reject fake-transparent or malformed PNG cutouts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


def validate(path: Path, min_padding: int) -> dict:
    errors: list[str] = []
    try:
        image = Image.open(path)
        image.load()
    except Exception as exc:
        return {"ok": False, "errors": [f"cannot open image: {exc}"]}

    if image.format != "PNG":
        errors.append(f"format is {image.format!r}, expected PNG")
    if image.mode != "RGBA":
        errors.append(f"mode is {image.mode!r}, expected RGBA")
        return {"ok": False, "format": image.format, "mode": image.mode, "size": image.size, "errors": errors}

    alpha = image.getchannel("A")
    lo, hi = alpha.getextrema()
    if lo != 0:
        errors.append("no fully transparent background pixels (alpha minimum is not 0)")
    if hi != 255:
        errors.append("no fully opaque subject pixels (alpha maximum is not 255)")

    width, height = image.size
    corners = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
    corner_alpha = [alpha.getpixel(point) for point in corners]
    if any(value != 0 for value in corner_alpha):
        errors.append(f"canvas corners are not fully transparent: {corner_alpha}")

    bbox = alpha.getbbox()
    if bbox is None:
        errors.append("image is fully transparent and contains no subject")
        padding = None
    else:
        left, top, right, bottom = bbox
        padding = [left, top, width - right, height - bottom]
        if min(padding) < min_padding:
            errors.append(f"subject is clipped or lacks required {min_padding}px padding: {padding}")

    histogram = alpha.histogram()
    transparent_ratio = histogram[0] / (width * height)
    if transparent_ratio < 0.01:
        errors.append(f"only {transparent_ratio:.3%} of pixels are fully transparent; likely fake transparency")

    return {
        "ok": not errors,
        "format": image.format,
        "mode": image.mode,
        "size": image.size,
        "alpha_extrema": [lo, hi],
        "corner_alpha": corner_alpha,
        "transparent_ratio": round(transparent_ratio, 6),
        "subject_bbox": bbox,
        "padding": padding,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--min-padding", type=int, default=2)
    args = parser.parse_args()
    report = validate(args.image, max(0, args.min_padding))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
