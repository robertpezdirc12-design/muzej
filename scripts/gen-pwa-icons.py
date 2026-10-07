#!/usr/bin/env python3
"""Generira PWA ikone za Muzej vasi Griblje iz monograma MV (kopia icon.svg)."""
import os
from PIL import Image, ImageDraw, ImageFont

CREAM = (242, 238, 230, 255)      # #F2EEE6
TERRA = (159, 74, 43, 255)        # #9F4A2B
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
OUT = "/home/z/my-project/public/icons"
os.makedirs(OUT, exist_ok=True)


def draw_regular(size: int) -> Image.Image:
    """Ikona po vzoru icon.svg: zaobljen kvadrat, smetana, terakotni rob, monogram MV."""
    scale = size / 64.0
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # zaobljen kvadrat z robom (rect x2 y2 60x60 rx14, stroke 3)
    stroke = max(2, round(3 * scale))
    d.rounded_rectangle(
        [round(2 * scale), round(2 * scale),
         round(62 * scale), round(62 * scale)],
        radius=round(14 * scale),
        fill=CREAM, outline=TERRA, width=stroke,
    )
    # monogram MV (font-size 30, y 41, letter-spacing -1)
    fsize = max(10, round(30 * scale))
    font = ImageFont.truetype(FONT, fsize)
    d.text((size // 2, round(39 * scale)), "MV", font=font,
           fill=TERRA, anchor="mm")
    # spodnja črtica (rect x20 y47 w24 h3)
    d.rounded_rectangle(
        [round(20 * scale), round(47 * scale),
         round(44 * scale), round(50 * scale)],
        radius=round(1.5 * scale), fill=TERRA,
    )
    return img


def draw_maskable(size: int) -> Image.Image:
    """Maskable: polnilo terakota (full-bleed), monogram MV v smetani v varnem območju (~70 %)."""
    img = Image.new("RGBA", (size, size), TERRA)
    d = ImageDraw.Draw(img)
    fsize = round(size * 0.30)
    font = ImageFont.truetype(FONT, fsize)
    d.text((size // 2, round(size * 0.46)), "MV", font=font,
           fill=CREAM, anchor="mm")
    # spodnja črtica
    w, h = round(size * 0.28), round(size * 0.035)
    d.rounded_rectangle(
        [size // 2 - w // 2, round(size * 0.68),
         size // 2 + w // 2, round(size * 0.68) + h],
        radius=max(2, h // 2), fill=CREAM,
    )
    return img


for size in (192, 512):
    draw_regular(size).save(f"{OUT}/icon-{size}.png")
    print(f"icon-{size}.png OK")
draw_maskable(512).save(f"{OUT}/icon-maskable-512.png")
print("icon-maskable-512.png OK")
draw_regular(180).save(f"{OUT}/apple-touch-icon.png")
print("apple-touch-icon.png OK")
print("velikosti:", {f: os.path.getsize(f"{OUT}/{f}") for f in sorted(os.listdir(OUT))})
