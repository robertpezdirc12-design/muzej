#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P256 — izrezi vrstic 1829/1830/1831 iz skenov s4–s7 knjige 01738.
(a) polna-širina trakovi vrstic (25% prekrivanje) za VLM branje,
(b) datumski celici (prvi stolpec, ×3 povečava) za dueli — kronologija je ključna!
Vrstice (izmerjeno z Read-očesi na 2144×1500 razprti listi):
  s4: 9 vrstic, y 300–1490 · s5: 8 vrstic, y 300–1370 · s6: 11 vrstic, y 290–1355 · s7: 13 vrstic, y 300–1405."""
import os
from PIL import Image

OUT = "/tmp/p256/full"
os.makedirs(OUT, exist_ok=True)
OUT2 = "/tmp/p256/dates"
os.makedirs(OUT2, exist_ok=True)

JOBS = [
    ("s4", 9, 300, 1490),
    ("s5", 8, 300, 1370),
    ("s6", 11, 290, 1355),
    ("s7", 13, 300, 1405),
]


def strips(src, tag, y0, y1, n, half=85):
    im = Image.open(src)
    W, H = im.size
    pitch = (y1 - y0) / n
    for i in range(1, n + 1):
        c = y0 + (i - 0.5) * pitch
        top = max(0, int(c - half))
        bot = min(H, int(c + half))
        im.crop((0, top, W, bot)).save(f"{OUT}/{tag}_r{i}.jpg", quality=92)
        print(f"{tag}_r{i}: y {top}-{bot} ({bot - top}px)")


def datecells(src, tag, y0, y1, n, pad=6):
    im = Image.open(src)
    W, H = im.size
    pitch = (y1 - y0) / n
    for i in range(1, n + 1):
        c = y0 + (i - 0.5) * pitch
        top = max(0, int(c - pitch / 2 - pad))
        bot = min(H, int(c + pitch / 2 + pad))
        cell = im.crop((70, top, 215, bot))
        cell = cell.resize((cell.width * 3, cell.height * 3), Image.LANCZOS)
        cell.save(f"{OUT2}/{tag}_d{i}.jpg", quality=95)
        print(f"{tag}_d{i}: y {top}-{bot}")


for tag, n, y0, y1 in JOBS:
    strips(f"/tmp/p256/{tag}.jpg", tag, y0, y1, n)
    datecells(f"/tmp/p256/{tag}.jpg", tag, y0, y1, n)
print("DONE")
