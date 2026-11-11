#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258 — izrezi vrstic 1831-konec/1832/1833-zacetek iz skenov s8–s10 knjige 01738
(ISTA GEOMETRIJA kot P257 — kalibrirana na s6/s7!):
  s8:  11 vrstic (r1–r11 = 1831-konec: 9. Febr-d° + 14. Febr ×2 + 6. Juni + 2.4.?/24.9.? + 24. Aug ×2 + Nov ×4), y 285–1420
  s9:  15 vrstic (r1–r15 = 1832: 18. Jän ×3 + 25. + 29. Jän + 15. Febr ×4 + 22. Febr + 29. Febr ×5), y 285–1400
  s10: 14 vrstic (r1–r8 = 1832-konec: 29. Febr ×4 + 5. März + 28. Mai + 20. Juni + 28. Nov; r9–r14 = 1833: 3./5. Febr + 6. Febr ×5), y 285–1400
(a) polna-širina trakovi (±85px prekrivanja) za VLM branja,
(b) datumski celici (x 70–215, ×3) za dueli-kronologijo,
(c) G/B bloki LEVE strani (ženin x40–640 / nevesta x600–1080; T/B polovici) — za duel-valove,
(d) R bloki DESNE strani (x 1030–2040, T/B) — starši/priči/duhovnik."""
import os
from PIL import Image

OUT = "/tmp/p258/full";    os.makedirs(OUT, exist_ok=True)
OUT2 = "/tmp/p258/dates";  os.makedirs(OUT2, exist_ok=True)
OUT3 = "/tmp/p258/L";      os.makedirs(OUT3, exist_ok=True)
OUT4 = "/tmp/p258/R";      os.makedirs(OUT4, exist_ok=True)

JOBS = [
    ("s8", 11, 285, 1420),
    ("s9", 15, 285, 1400),
    ("s10", 14, 285, 1400),
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


for tag, n, y0, y1 in JOBS:
    src = f"/tmp/p258/{tag}.jpg"
    strips(src, tag, y0, y1, n)
    datecells(src, tag, y0, y1, n)
    gbblocks(src, tag, y0, y1)
    # R bloki
    im = Image.open(src)
    mid = (y0 + y1) // 2
    for half, (a, b) in {"T": (max(240, y0 - 50), mid + 40), "B": (mid - 40, min(1500, y1 + 50))}.items():
        c = im.crop((1030, a, min(im.size[0] - 30, 2050), b))
        c = c.resize((int(c.width * 1.6), int(c.height * 1.6)), Image.LANCZOS)
        c.save(f"{OUT4}/{tag}_{half}.jpg", quality=90)
        print(f"{tag}_R{half}: y[{a},{b}] ×1.6")
print("DONE")
