#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P200 — generični KROP-orožjar: izrez + zoom + kontrast.
Uporaba: p199_crop.py <scan> <x0> <y0> <x1> <y1> <ime> [zoom=2.2] [gamma=1.0]
Koordinate = ULOMKI (0–1) celotnega skena. Izhod: /tmp/p200/crops/<ime>.png"""
import sys
from PIL import Image, ImageEnhance

scan, x0, y0, x1, y1, ime = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
zoom = float(sys.argv[7]) if len(sys.argv) > 7 else 2.2
gamma = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0

im = Image.open(f"/tmp/p200/{scan}.jpg")
W, H = im.size
c = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
c = c.resize((int(c.width * zoom), int(c.height * zoom)), Image.LANCZOS)
if gamma != 1.0:
    c = ImageEnhance.Contrast(c).enhance(gamma)
c.save(f"/tmp/p200/crops/{ime}.png")
print(f"{ime}.png: {c.size}")
