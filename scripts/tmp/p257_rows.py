#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P257 — izrezi vrstic 1830/1831 iz skenov s6–s7 knjige 01738 (ISTA GEOMETRIJA kot P256
— kalibrirana na teh istih straneh!):
  s6: 11 vrstic (r1–r3 = 1829 P256; r4–r11 = 1830 P257!), y 290–1355
  s7: 13 vrstic (r1–r13 = 1831 P257!), y 300–1405
(a) polna-širina trakovi (±85px prekrivanje) za VLM branja,
(b) datumski celici (x 70–215, ×3) za dueli-kronologijo,
(c) G/B bloki LEVE strani (3×; ženin x40–640 / nevesta x600–1080; T/B polovici),
(d) R bloki DESNE strani razprtega lista (x 1030–2040, T/B, ×2) — starši/priči/duhovnik."""
import os
from PIL import Image

OUT = "/tmp/p257/full";    os.makedirs(OUT, exist_ok=True)
OUT2 = "/tmp/p257/dates";  os.makedirs(OUT2, exist_ok=True)
OUT3 = "/tmp/p257/L";      os.makedirs(OUT3, exist_ok=True)
OUT4 = "/tmp/p257/R";      os.makedirs(OUT4, exist_ok=True)

JOBS = [
    ("s6", 11, 290, 1355),
    ("s7", 13, 300, 1405),
]


def strips(src, tag, y0, y1, n, half=85):
    im = Image.open(src)
    W, H = im.size
    pitch = (y1 - y0) / n
    for i in range(1, n + 1):
        c = y0 + (i - 0.5) * pitch
        top = max(0, int(c - half)); bot = min(H, int(c + half))
        im.crop((0, top, W, bot)).save(f"{OUT}/{tag}_r{i}.jpg", quality=92)
        print(f"{tag}_r{i}: y {top}-{bot}")


def datecells(src, tag, y0, y1, n, pad=8):
    im = Image.open(src)
    W, H = im.size
    pitch = (y1 - y0) / n
    for i in range(1, n + 1):
        c = y0 + (i - 0.5) * pitch
        top = max(0, int(c - pitch / 2 - pad)); bot = min(H, int(c + pitch / 2 + pad))
        cell = im.crop((70, top, 215, bot))
        cell = cell.resize((cell.width * 3, cell.height * 3), Image.LANCZOS)
        cell.save(f"{OUT2}/{tag}_d{i}.jpg", quality=95)
        print(f"{tag}_d{i}: y {top}-{bot} ×3")


def gbblocks(src, tag, y0, y1):
    im = Image.open(src)
    W, H = im.size
    mid = (y0 + y1) // 2
    for name, (x0, x1) in {"G": (40, 640), "B": (600, 1080)}.items():
        for half, (a, b) in {"T": (max(240, y0 - 50), mid + 40), "B": (mid - 40, min(1500, y1 + 50))}.items():
            c = im.crop((x0, a, x1, b))
            c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
            c.save(f"{OUT3}/{tag}_{name}{half}.jpg", quality=90)
            print(f"{tag}_{name}{half}: x[{x0},{x1}] y[{a},{b}] ×3")


def rightblocks(src, tag, y0, y1):
    im = Image.open(src)
    W, H = im.size
    mid = (y0 + y1) // 2
    for half, (a, b) in {"T": (max(240, y0 - 50), mid + 40), "B": (mid - 40, min(1500, y1 + 50))}.items():
        c = im.crop((1030, a, min(2040, W), b))
        c = c.resize((int(c.width * 2), int(c.height * 2)), Image.LANCZOS)
        c.save(f"{OUT4}/{tag}_{half}.jpg", quality=90)
        print(f"{tag}_R{half}: ×2")


for tag, n, y0, y1 in JOBS:
    src = f"/tmp/p257/{tag}.jpg"
    strips(src, tag, y0, y1, n)
    datecells(src, tag, y0, y1, n)
    gbblocks(src, tag, y0, y1)
    rightblocks(src, tag, y0, y1)
print("DONE")
