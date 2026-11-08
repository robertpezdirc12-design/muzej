#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P232 — vrstični-krops (polna-širina, ×1.6) za VSAK vpis 1875 + tail-1874 (s45–s64!).
En-sheet-na-sken: vsaka-vrstica = 1 krop s labelo. Izhod: /tmp/p232/krops/R-<scan>.png"""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p232"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

# vrstic-na-sken (iz VLM celostanskih-branj + vizualno!)
ROWS = {37: 8, 38: 8, 39: 9, 40: 11, 41: 9, 42: 9, 43: 9, 44: 9, 45: 8, 46: 8, 47: 8}
Y0, Y1 = 0.13, 0.88

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception:
    FONT = ImageFont.load_default()


def crop(scan, box, scale=1.6):
    im = Image.open(f"{T}/s{scan}.jpg")
    W, H = im.size
    px = (int(box[0] * W), int(box[2] * H), int(box[1] * W), int(box[3] * H))
    c = im.crop(px)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    return c


def sheet(name, items):
    imgs = []
    for label, scan, box in items:
        c = crop(scan, box)
        lab = Image.new("RGB", (c.width, 30), (20, 20, 20))
        d = ImageDraw.Draw(lab)
        d.text((8, 3), label, fill=(255, 220, 120), font=FONT)
        imgs += [lab, c, Image.new("RGB", (c.width, 8), (255, 255, 255))]
    W = max(i.width for i in imgs)
    H = sum(i.height for i in imgs)
    out = Image.new("RGB", (W, H), (240, 240, 240))
    y = 0
    for i in imgs:
        out.paste(i, (0, y)); y += i.height
    p = f"{OUT}/{name}.png"
    out.save(p)
    print(f"{name}: {W}x{H} ({len(items)} kropov)")


FULL = (0.075, 0.995)
ZAPL = (0.075, 0.30)  # zap+mesec+dan

for scan, n in ROWS.items():
    items = []
    for r in range(1, n + 1):
        y_a = Y0 + (r - 1) * (Y1 - Y0) / n - 0.008
        y_b = Y0 + r * (Y1 - Y0) / n + 0.008
        items.append((f"s{scan}-r{r}", scan, (FULL[0], FULL[1], max(0, y_a), min(1.0, y_b))))
    # + zap-krop r1 (kontrola restarta!)
    y_a = Y0 - 0.008
    y_b = Y0 + (Y1 - Y0) / n + 0.008
    items.append((f"s{scan}-r1-ZAP-levo", scan, (ZAPL[0], ZAPL[1], max(0, y_a), min(1.0, y_b))))
    sheet(f"R-{scan}", items)

print("VRSTICNI-KROPS-GOTOVI")
