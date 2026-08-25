from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

from validate_transparency import validate


def main() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        valid = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        ImageDraw.Draw(valid).ellipse((12, 12, 51, 51), fill=(255, 80, 20, 255))
        valid_path = root / "valid.png"
        valid.save(valid_path)
        assert validate(valid_path, 2)["ok"]

        fake = Image.new("RGB", (64, 64), "white")
        draw = ImageDraw.Draw(fake)
        for y in range(0, 64, 8):
            for x in range(0, 64, 8):
                if (x // 8 + y // 8) % 2:
                    draw.rectangle((x, y, x + 7, y + 7), fill=(210, 210, 210))
        fake_path = root / "fake-checkerboard.png"
        fake.save(fake_path)
        report = validate(fake_path, 2)
        assert not report["ok"]
        assert any("expected RGBA" in error for error in report["errors"])

        opaque_rgba = Image.new("RGBA", (64, 64), (240, 240, 240, 255))
        opaque_path = root / "opaque-rgba.png"
        opaque_rgba.save(opaque_path)
        report = validate(opaque_path, 2)
        assert not report["ok"]
        assert any("alpha minimum" in error for error in report["errors"])
    print("validator tests passed")


if __name__ == "__main__":
    main()
