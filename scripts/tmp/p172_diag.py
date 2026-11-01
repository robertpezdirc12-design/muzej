#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P172 — diag gridi (P170-recept): pomanjšan sken + rumene y-črte + oznake.
Vrstice pričakovane @ 330–1950 / ~135px; glava @ 130–290.
Izhod: /tmp/p172/diag-sNN.jpg"""
from PIL import Image, ImageDraw
import os, sys

OUT = "/tmp/p172"
SCANS = sys.argv[1:] or ["s104", "s105", "s106", "s107", "s108", "s109", "s110"]
GRID_STEP = 135
Y0 = 330          # 1. vrstica
YMAX = 2000

for s in SCANS:
    im = Image.open(f"{OUT}/{s}.jpg").convert("RGB")
    w, h = im.size
    tw = 1534
    th = int(h * tw / w)
    im = im.resize((tw, th), Image.LANCZOS)
    dr = ImageDraw.Draw(im)
    scale = th / h
    y = Y0
    while y < YMAX:
        yy = int(y * scale)
        dr.line([(0, yy), (tw, yy)], fill=(255, 200, 0), width=2)
        dr.text((4, yy + 2), f"y={y}", fill=(255, 120, 0))
        y += GRID_STEP
    # glava pas
    dr.rectangle([0, int(130 * scale), 120, int(290 * scale)], outline=(255, 0, 255), width=3)
    im.save(f"{OUT}/diag-{s}.jpg", quality=88)
    print(f"diag-{s}.jpg {im.size}")
