#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — TAIL-VERIGA: s19 (10-bandov?!) + s24 (11) + s25 (6) — zap-neapolis-končna-resitev.
+ TAIL-št.: 115-vs-116?! + prečrtana-r7-s24-brez-zapa?! + s25-r6-prazna?!"""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p234"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception:
    FONT = ImageFont.load_default()

ZAPL = (0.05, 0.42)

def cropn(scan, r, n, scale=3.0):
    im = Image.open(f"{T}/s{scan}.jpg")
    W, H = im.size
    y0 = 0.125 + (r - 1) * (0.92 - 0.125) / n
    y1 = 0.125 + r * (0.92 - 0.125) / n
    px = (int(ZAPL[0] * W), int(y0 * H), int(ZAPL[1] * W), int(min(1.0, y1) * H))
    c = im.crop(px)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    return c

def sheet(name, items):
    imgs = []
    for label, scan, r, n in items:
        c = cropn(scan, r, n)
        lab = Image.new("RGB", (c.width, 28), (20, 20, 20))
        d = ImageDraw.Draw(lab)
        d.text((8, 3), label, fill=(255, 220, 120), font=FONT)
        imgs += [lab, c, Image.new("RGB", (c.width, 7), (255, 255, 255))]
    W = max(i.width for i in imgs)
    H = sum(i.height for i in imgs)
    out = Image.new("RGB", (W, H), (240, 240, 240))
    y = 0
    for i in imgs:
        out.paste(i, (0, y)); y += i.height
    out.save(f"{OUT}/{name}.png")
    print(f"{name}: {W}x{H} ({len(items)} kropov)")

items = [("s19-r1 (z51? z52? z1?!-JUNI?-kronološko!)", 19, 1, 10),
         ("s19-r5 (z55?!)", 19, 5, 10),
         ("s19-r9 (z59?!-GRIBLJE-h12-Pegdic!)", 19, 9, 10),
         ("s19-r10 (zadnja-band!-z60?-prazna?!)", 19, 10, 10)]
for r in range(1, 12):
    items.append((f"s24-r{r} (z{99+r}?-r7-PREČRTANA!)", 24, r, 11))
for r in range(1, 7):
    items.append((f"s25-r{r} (TAIL!-z110+!)", 25, r, 6))
sheet("TAIL-VERIGA", items)
print("P234-TAIL-VERIGA-GOTOVI")
