#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P153 forenzika 3 — MAX-ZOOM celice (3.6×) za 11 odprtih vprašanj.
Vhod: (sken, y0, y1, x0, x1, oznaka) — proporcionalne koordinate."""
from PIL import Image
import os

OUT = "/tmp/p153/cells"
os.makedirs(OUT, exist_ok=True)

# (sken, y0, y1, x0, x1, tag)  — frakcije širine/višine
C = [
    # r24 h65: ime+stan (0.29–0.50) + starost+bolezen (0.54–0.75)
    (8, 0.715, 0.800, 0.28, 0.51, "r24-ime"),
    (8, 0.715, 0.800, 0.53, 0.78, "r24-star-bolez"),
    # r25 h46: starost+bolezen
    (8, 0.790, 0.875, 0.53, 0.78, "r25-star-bolez"),
    # r27 h53: datumi+ime
    (9, 0.140, 0.235, 0.04, 0.51, "r27-dat-ime"),
    (9, 0.140, 0.235, 0.53, 0.78, "r27-star-bolez"),
    # r30 h76: celotna vrsta (prej zamaknjeno)
    (9, 0.235, 0.330, 0.00, 0.52, "r30-ime"),
    (9, 0.235, 0.330, 0.53, 0.80, "r30-star-bolez"),
    # r51 h3: stan
    (11, 0.880, 0.985, 0.28, 0.51, "r51-ime-stan"),
    # r55 h21: ime+stan + spol-tick
    (12, 0.330, 0.425, 0.26, 0.58, "r55-ime-spol"),
    # r57 h13: datumi + ime
    (12, 0.490, 0.585, 0.04, 0.58, "r57-dat-ime"),
    # r61 h22: ime+stan + spol
    (12, 0.730, 0.820, 0.26, 0.58, "r61-ime-spol"),
    # r63 h35: vas+hisa + starost
    (12, 0.870, 0.960, 0.10, 0.32, "r63-vas-hisa"),
    (12, 0.870, 0.960, 0.53, 0.78, "r63-star-bolez"),
    # r66 h53b: vas+hiša (53-vs-58!) + ime/stan + bolezen
    (13, 0.175, 0.270, 0.10, 0.32, "r66-vas-hisa"),
    (13, 0.175, 0.270, 0.28, 0.55, "r66-ime-stan"),
    (13, 0.175, 0.270, 0.53, 0.80, "r66-star-bolez"),
    # r71 h43: ime+stan
    (13, 0.500, 0.595, 0.26, 0.55, "r71-ime-stan"),
]

for scan, f0, f1, g0, g1, tag in C:
    im = Image.open(f"/tmp/p153/s{scan:02d}.jpg")
    w, h = im.size
    c = im.crop((int(w * g0), int(h * f0), int(w * g1), min(h, int(h * f1))))
    c.resize((int(c.width * 3.6), int(c.height * 3.6)), Image.LANCZOS).save(f"{OUT}/{tag}.png")
print("cells:", len(os.listdir(OUT)))
