#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P153 forenzika 2 — ciljni izrezi TROBNIH vrstic (sproženi spori med
celostanskim branjem in VLM-trakovi) + meja-vrsta s13.
Vhodi: (sken, y0_frac, y1_frac, oznaka) — proporcionalne koordinate iz
celostanskih branj (2000 px višine)."""
from PIL import Image
import os

OUT = "/tmp/p153/rows3"
os.makedirs(OUT, exist_ok=True)

CROPS = [
    # s08: vrste 16–26; r24 h65 ≈ 0.72–0.79, r25 h46 ≈ 0.79–0.865
    (8, 0.715, 0.795, "r24-h65"),
    (8, 0.790, 0.868, "r25-h46"),
    # s09: vrste 27–33; r27 h53 ≈ 0.055–0.135, r30 h76 ≈ 0.33–0.42
    (9, 0.052, 0.140, "r27-h53"),
    (9, 0.330, 0.425, "r30-h76"),
    # s11: vrste 40–51; r51 h3 ≈ 0.885–0.975
    (11, 0.880, 0.978, "r51-h3"),
    # s12: vrste 52–64; r55 ≈ 0.335–0.42, r57 ≈ 0.495–0.575, r61 ≈ 0.735–0.81, r63 ≈ 0.875–0.95
    (12, 0.330, 0.425, "r55-h21"),
    (12, 0.490, 0.580, "r57-h13"),
    (12, 0.730, 0.815, "r61-h22"),
    (12, 0.870, 0.955, "r63-h35"),
    # s13: r66 ≈ 0.175–0.26, r71 ≈ 0.50–0.585, meja-vrsta ≈ 0.585–0.675
    (13, 0.170, 0.265, "r66-h53b"),
    (13, 0.495, 0.590, "r71-h43"),
    (13, 0.585, 0.680, "r72-meja"),
    (13, 0.950, 1.000, "r77-lead"),
]

for scan, f0, f1, tag in CROPS:
    im = Image.open(f"/tmp/p153/s{scan:02d}.jpg")
    w, h = im.size
    c = im.crop((0, int(h * f0), w, min(h, int(h * f1))))
    lw = int(w * 0.55)
    L = c.crop((0, 0, lw, c.height))
    R = c.crop((int(w * 0.43), 0, w, c.height))
    for half, part in (("L", L), ("R", R)):
        sc = 2.4
        part.resize((int(part.width * sc), int(part.height * sc)), Image.LANCZOS).save(
            f"{OUT}/s{scan:02d}-{tag}-{half}.png")
print("crops:", len(os.listdir(OUT)) // 2 * 2)
