#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P153 — izrezi vrstic mrliške 04894 (1887) za VLM branje.
Za vsako ključno vrstico: polna širina (L = stolpci št./datum/vas/hiša/ime,
R = starost/bolezen/duhovnik/opomba), 2.2× Lanczos."""
from PIL import Image
import os

OUT = "/tmp/p153/rows"
os.makedirs(OUT, exist_ok=True)

# sken -> (n_vrstic_na_strani, y_vrh_tabele, y_dno_tabele) — ocena iz celostanskih branj
PAGES = {
    6: (12, 0.055, 0.985),   # s06: vrste 41–46 1886 + prelom Januarj 1887 + vrste 1–5
    8: (11, 0.075, 0.985),   # s08: vrste 16–26
    9: (7, 0.055, 0.985),    # s09: vrste 27–33
    11: (12, 0.055, 0.985),  # s11: vrste 40–51
    12: (13, 0.055, 0.985),  # s12: vrste 52–64
    13: (14, 0.055, 0.985),  # s13: vrste 65–71 + meja + vrste 73–77
}

# (sken, indeks_vrstice_od_zgoraj) — ključne vrstice
KEY = [
    (6, 8), (6, 9), (6, 10), (6, 11), (6, 12),   # 1887 r1–r5 (Januarj 1887 blok)
    (8, 9), (8, 10),                              # r24 h65, r25 h46
    (9, 1), (9, 4),                               # r27 h53, r30 h76
    (11, 12),                                     # r51 h3
    (12, 4), (12, 6), (12, 10), (12, 12),         # r55 h21, r57 h13, r61 h22, r63 h35
    (13, 2), (13, 7), (13, 8),                    # r66 h53-Marko, r71 h43, r72 MEJA
]

for scan, nrows, y0, y1 in [(s, *PAGES[s]) for s in PAGES]:
    im = Image.open(f"/tmp/p153/s{scan:02d}.jpg")
    w, h = im.size
    top, bot = int(h * y0), int(h * y1)
    step = (bot - top) / nrows
    for idx in {i for s, i in KEY if s == scan}:
        cy0 = max(0, int(top + idx * step) - 22)
        cy1 = min(h, int(top + (idx + 1) * step) + 34)
        strip = im.crop((0, cy0, w, cy1))
        lw = int(w * 0.55)
        L = strip.crop((0, 0, lw, strip.height))
        R = strip.crop((int(w * 0.45), 0, w, strip.height))
        for half, c in (("L", L), ("R", R)):
            sc = 2.2 if c.width < 1600 else 1.8
            c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS).save(
                f"{OUT}/s{scan:02d}-r{idx+1}{half}.png")

# posebni izrezi: glava s13 (prazno Leto 18) + meja-vrsta 72 celota + vsotna vrsta
im13 = Image.open("/tmp/p153/s13.jpg")
w, h = im13.size
hdr = im13.crop((0, 0, int(w * 0.55), int(h * 0.16)))
hdr.resize((int(hdr.width * 2.0), int(hdr.height * 2.0)), Image.LANCZOS).save(f"{OUT}/s13-heading.png")
print("crops:", len(os.listdir(OUT)))
