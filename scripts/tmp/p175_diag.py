#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P175 diag — fiksni grid 330–1950 / 135 px preko skenov s121–s125 (+s126 meja).
Metoda P172–P174: vizualna zaslona z Read-očmi (rows-v3 FAIL — lekcija 3 let)."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/tmp/p175/diag"
os.makedirs(OUT, exist_ok=True)
SCANS = [121, 122, 123, 124, 125, 126]
Y0, Y1, STEP = 330, 1950, 135

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    font_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception:
    font = font_s = ImageFont.load_default()

for s in SCANS:
    im = Image.open(f"/tmp/p175/s{s}.jpg").convert("RGB")
    d = ImageDraw.Draw(im)
    W, H = im.size
    # horizontalne črte + y-oznake
    for y in range(Y0, Y1 + 1, STEP):
        d.line([(0, y), (W, y)], fill=(255, 0, 0), width=3)
        d.text((W - 90, y - 30), str(y), fill=(255, 0, 0), font=font)
    # pasovne oznake (sredina pasu)
    for k in range(12):
        ym = Y0 + STEP * k + STEP // 2
        d.ellipse([(10, ym - 22), (54, ym + 22)], fill=(0, 160, 0))
        d.text((18, ym - 15), str(k + 1), fill=(255, 255, 255), font=font)
    # vertikalne referenčne črte (8 stolpcev)
    for fx in [0.045, 0.135, 0.38, 0.52, 0.62, 0.78, 0.87, 0.93]:
        x = int(W * fx)
        d.line([(x, 0), (x, H)], fill=(0, 120, 255), width=2)
    im.save(f"{OUT}/diag_s{s}.jpg", quality=90)
    print(f"diag s{s}: {im.size} -> {OUT}/diag_s{s}.jpg")
print("DONE")
