#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P160 — izrezi: L/R trakovi + max-zoom celice za 6 Griblje-vrstic 1894
+ meja 1894/95 (marker »— 1895. —« + zap 49/50) + s47 glava/zap1-restart.
Griblje-1894 = 6 vrstic (zap 14, 22, 24, 30, 37, 38).
Izhod: /tmp/p160/strips/ + /tmp/p160/cells/."""
from PIL import Image
import os

STRIPS = "/tmp/p160/strips"
CELLS = "/tmp/p160/cells"
for d in (STRIPS, CELLS):
    os.makedirs(d, exist_ok=True)

# (ime, sken, x0f, x1f, y0, y1, zoom)
CELLS_DEF = [
    # L-stran: zaporedna + mesec + vas + hišna + ime (6 Griblje-vrstic)
    ("s48-r14-L",       48, 0.02, 0.52,  466,  604, 3.0),
    ("s48-r22-L",       48, 0.02, 0.52, 1620, 1770, 3.0),
    ("s48-r24-L",       48, 0.02, 0.52, 1885, 1999, 3.0),
    ("s49-r30-L",       49, 0.02, 0.52, 1018, 1152, 3.0),
    ("s50-r37-L",       50, 0.02, 0.52,  336,  478, 3.0),
    ("s50-r38-L",       50, 0.02, 0.52,  478,  620, 3.0),
    # R-stran: starost + vzrok + previden + podpis (6 × 2.2×)
    ("s48-r14-R",       48, 0.52, 0.98,  466,  604, 2.2),
    ("s48-r22-R",       48, 0.52, 0.98, 1620, 1770, 2.2),
    ("s48-r24-R",       48, 0.52, 0.98, 1885, 1999, 2.2),
    ("s49-r30-R",       49, 0.52, 0.98, 1018, 1152, 2.2),
    ("s50-r37-R",       50, 0.52, 0.98,  336,  478, 2.2),
    ("s50-r38-R",       50, 0.52, 0.98,  478,  620, 2.2),
    # super-zoom imena (5×) — glyphs: Terdinec/Perdinec, Straus, Jakobič, Brinec, Brodanič
    ("s48-r14-ime",     48, 0.29, 0.52,  466,  545, 5.0),
    ("s48-r22-ime",     48, 0.29, 0.52, 1620, 1700, 5.0),
    ("s48-r24-ime",     48, 0.29, 0.52, 1885, 1968, 5.0),
    ("s49-r30-ime",     49, 0.29, 0.52, 1018, 1092, 5.0),
    ("s50-r37-ime",     50, 0.29, 0.52,  336,  412, 5.0),
    ("s50-r38-ime",     50, 0.29, 0.52,  478,  556, 5.0),
    # super-zoom hišnih števil (6×) — γ-7 preverba: 87, 57, 49, 35, 72, 24
    ("s48-r14-h",       48, 0.245, 0.315,  466,  604, 6.0),
    ("s48-r22-h",       48, 0.245, 0.315, 1620, 1770, 6.0),
    ("s48-r24-h",       48, 0.245, 0.315, 1885, 1999, 6.0),
    ("s49-r30-h",       49, 0.245, 0.315, 1018, 1152, 6.0),
    ("s50-r37-h",       50, 0.245, 0.315,  336,  478, 6.0),
    ("s50-r38-h",       50, 0.245, 0.315,  478,  620, 6.0),
    # meja 1894/95: marker + zap 49/50 (December 1894-rep) + restart zap1
    ("s51-marker-1895", 51, 0.02, 0.52,  555,  725, 3.0),
    ("s51-zap49-R",     51, 0.52, 0.98,  280,  435, 2.2),
    ("s51-zap50-R",     51, 0.52, 0.98,  425,  575, 2.2),
    ("s47-glava-zap1",  47, 0.02, 0.52,  130,  420, 2.2),
    ("s51-zap1-1895-L", 51, 0.02, 0.52,  755,  910, 3.0),
]

def main():
    for name, scan, x0f, x1f, y0, y1, z in CELLS_DEF:
        im = Image.open(f"/tmp/p160/s{scan:02d}.jpg")
        x0, x1 = int(im.width * x0f), int(im.width * x1f)
        crop = im.crop((x0, y0, x1, y1))
        crop = crop.resize((int(crop.width * z), int(crop.height * z)), Image.LANCZOS)
        out = f"{CELLS}/{name}.png"
        crop.save(out)
        print(f"{name}: {crop.width}x{crop.height}")

if __name__ == "__main__":
    main()
