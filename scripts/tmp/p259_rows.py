#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — izrezi vrstic 1833-konec/1834-zacetek iz skenov s11–s13 knjige 01738
(GEOMETRIJA po vzoru P258, kalibrirana z y-grid sidri!):
  s11: 13 vrstic (r1–r8 = 6. Febr-d°-kaskada m7–m14 + r9–r13 = 13. Febr m15–m19), y 285–1400
  s12: 12 vrstic (r1–r6 = 1833-konec: 19. Febr + [12.?] + 21. April + 5. Mai + [10.|26.] Oct + 27. Nov-rob1;
                   r7–r12 = 1834: 22. Jän-rob2 + d°-rob3 + 29. Jän-rob4-7), y 280–1260
  s13: 11 vrstic (rob8–14 = 5. Febr ×7 m1–m7 + rob15 = 9. Febr m8 + rob16–18 = 10. Febr ×3 m9–m11), y 280–1040
(a) polna-širina trakovi (±85px prekrivanja) za VLM branja,
(b) datumski celici (x 70–215, ×3) za dueli-kronologijo,
(c) G/B bloki LEVE strani (ženin x40–640 / nevesta x600–1080; T/B polovici) — za duel-valove,
(d) R bloki DESNE strani (x 1030–2040, T/B) — starši/priči/duhovnik."""
import os
from PIL import Image

OUT = "/tmp/p259/full";    os.makedirs(OUT, exist_ok=True)
OUT2 = "/tmp/p259/dates";  os.makedirs(OUT2, exist_ok=True)
OUT3 = "/tmp/p259/L";      os.makedirs(OUT3, exist_ok=True)
OUT4 = "/tmp/p259/R";      os.makedirs(OUT4, exist_ok=True)

JOBS = [
    ("s11", 13, 285, 1400),
    ("s12", 12, 280, 1260),
    ("s13", 11, 280, 1040),
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
    src = f"/tmp/p259/{tag}.jpg"
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
    # census L/R cele strani
    W, H = im.size
    im.crop((0, 200, 1090, min(1480, H - 20))).save(f"/tmp/p259/{tag}_LEFT.jpg", quality=90)
    im.crop((1030, 200, W - 20, min(1480, H - 20))).save(f"/tmp/p259/{tag}_RIGHT.jpg", quality=90)
print("DONE")
