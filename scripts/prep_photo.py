"""Prep a photo for ASCII conversion: grayscale, contrast-boost, white background."""
import sys
from PIL import Image, ImageOps


def prep(src_path: str, dst_path: str = "source-prepped.png") -> None:
    img = Image.open(src_path).convert("RGBA")
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.paste(img, mask=img.split()[3])
    gray = bg.convert("L")
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray.save(dst_path)
    print(f"wrote {dst_path} ({gray.size[0]}x{gray.size[1]})")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.png"
    prep(src)
