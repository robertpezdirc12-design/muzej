#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P255 — ciljni izrezi (dueli) + pravilni vrstični izrezi (koordinate meritve ×1,38)."""
import os
from PIL import Image

OUT = "/tmp/p255"
F = f"{OUT}/full"
os.makedirs(F, exist_ok=True)

s2 = Image.open(f"{OUT}/s2.jpg")
s3 = Image.open(f"{OUT}/s3.jpg")

# ——— ciljni zoomi (dvomi) ———
zooms = [
    # (im, ime, box)
    (s2, "z_m1_datum", (120, 290, 620, 450)),      # m1: Jänner 20 vs 30
    (s2, "z_must_row", (20, 1060, 700, 1210)),     # neštevilčena vrstica: marginala + datum
    (s2, "z_datumi_s2", (120, 420, 420, 1310)),    # datumska kolona vseh vrstic s2
    (s3, "z_datumi_s3", (120, 300, 420, 1040)),    # datumska kolona vseh vrstic s3
    (s3, "z_m13_datum", (120, 700, 620, 830)),     # m13: 'Mai 4/5'?
    (s3, "z_sept_nov_marg", (0, 800, 400, 1030)),  # marginali Sept/Nov vrstic (kvačke?)
    (s2, "z_m6_hisa", (0, 870, 760, 1000)),        # m6: 'Tirna 25' + 'Griblje 6'
    (s3, "z_m13_hise", (120, 700, 1000, 830)),     # m13: Griblje 61 × Griblje 22
]
for im, name, box in zooms:
    c = im.crop(box)
    w, h = c.size
    sc = min(3, max(1, int(1600 / w)))
    c.resize((w * sc, h * sc), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=92)
    print(name, box, "->", c.size, "x", sc)

# ——— pravilni vrstični izrezi ———
def rows(im, tag, bounds):
    W, H = im.size
    for i, (a, b) in enumerate(bounds, 1):
        a2, b2 = max(0, a), min(H, b)
        im.crop((0, a2, W, b2)).save(f"{F}/{tag}_r{i}.jpg", quality=92)
    print(tag, len(bounds), "rows")

rows(s2, "s2", [(296, 440), (430, 564), (556, 670), (660, 772), (764, 888),
                (880, 994), (984, 1098), (1088, 1200), (1190, 1300)])
rows(s3, "s3", [(318, 428), (418, 522), (514, 620), (610, 718), (706, 814),
                (806, 918), (900, 1018)])
print("DONE")
