#!/usr/bin/env python3
"""Generate all icons for the Keeper app from the source avatar."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("/home/nigga/Рабочий стол/киппер.jpg")
WWW = ROOT / "www" / "icons"
IOS = ROOT / "Resources" / "Assets.xcassets" / "AppIcon.appiconset"

for d in (WWW, IOS):
    d.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC).convert("RGB")
w, h = img.size
s = min(w, h)
img = img.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
base = img.resize((1024, 1024), Image.LANCZOS)


def save(folder, size, name):
    out = base.resize((size, size), Image.LANCZOS)
    out.save(folder / name, "PNG", optimize=True)
    print(f"{folder.name}/{name}: {size}x{size}")


# --- PWA / web icons ---
for size in (64, 180, 192, 512, 1024):
    save(WWW, size, f"icon-{size}.png")
base.save(WWW / "apple-touch-icon.png", "PNG", optimize=True)

# --- iOS AppIcon.appiconset ---
ios_sizes = {
    "Icon-20@2x.png": 40,
    "Icon-20@3x.png": 60,
    "Icon-29@2x.png": 58,
    "Icon-29@3x.png": 87,
    "Icon-40@2x.png": 80,
    "Icon-40@3x.png": 120,
    "Icon-60@2x.png": 120,
    "Icon-60@3x.png": 180,
    "Icon-76@2x.png": 152,
    "Icon-83.5@2x.png": 167,
    "Icon-1024.png": 1024,
}
for name, size in ios_sizes.items():
    save(IOS, size, name)

entries = [
    ("Icon-20@2x.png", "20x20", "2x", "iphone"),
    ("Icon-20@3x.png", "20x20", "3x", "iphone"),
    ("Icon-29@2x.png", "29x29", "2x", "iphone"),
    ("Icon-29@3x.png", "29x29", "3x", "iphone"),
    ("Icon-40@2x.png", "40x40", "2x", "iphone"),
    ("Icon-40@3x.png", "40x40", "3x", "iphone"),
    ("Icon-60@2x.png", "60x60", "2x", "iphone"),
    ("Icon-60@3x.png", "60x60", "3x", "iphone"),
    ("Icon-76@2x.png", "76x76", "2x", "ipad"),
    ("Icon-83.5@2x.png", "83.5x83.5", "2x", "ipad"),
    ("Icon-1024.png", "1024x1024", "1x", "ios-marketing"),
]
contents = {
    "images": [
        {"filename": f, "idiom": idi, "scale": sc,
         "size": sz} for f, sz, sc, idi in entries
    ],
    "info": {"author": "xcode", "version": 1},
}
import json
(IOS / "Contents.json").write_text(json.dumps(contents, indent=2) + "\n")
print("Wrote Contents.json")
