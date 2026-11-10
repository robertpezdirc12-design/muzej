#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P243 — pass-3: tight vrstični trakovi (row-panel L+R, P151-metoda).
s36/s37/s38 po 6 vrstic (~200px višine); + 3× number-column izrezi."""
import os
from PIL import Image

OUT = "/tmp/p243/crops3"
os.makedirs(OUT, exist_ok=True)

# layout: glava ~0–310, vrstice ~310–1600 (6 vrstic ≈ 215px), dno ~1600–1800
PAGES = {"s36": 6, "s37": 6, "s38": 6}
ROW_TOP = {"s36": 300, "s37": 280, "s38": 300}
ROW_BOT = {"s36": 1620, "s37": 1620, "s38": 1620}

for page, n in PAGES.items():
    im = Image.open(f"/tmp/p243/{page}.jpg")
    w, h = im.size
    top, bot = ROW_TOP[page], ROW_BOT[page]
    step = (bot - top) / n
    for r in range(n):
        y0 = int(top + r * step) - 12
        y1 = int(top + (r + 1) * step) + 12
        y0 = max(0, y0); y1 = min(h, y1)
        L = im.crop((0, y0, 1230, y1))
        L = L.resize((L.width * 2, L.height * 2), Image.LANCZOS)
        L.save(f"{OUT}/{page}-r{r+1}-L.jpg", quality=92)
        R = im.crop((1180, y0, w, y1))
        R = R.resize((R.width * 2, R.height * 2), Image.LANCZOS)
        R.save(f"{OUT}/{page}-r{r+1}-R.jpg", quality=92)
        print(f"{page}-r{r+1}: y {y0}-{y1} L+R")

# 3× številčni stolpci
for page, x0, x1 in [("s36", 60, 260), ("s37", 60, 260), ("s38", 60, 260)]:
    im = Image.open(f"/tmp/p243/{page}.jpg")
    c = im.crop((x0, 260, x1, 1660))
    c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
    c.save(f"{OUT}/{page}-numcol-3x.jpg", quality=93)
    print(f"{page}-numcol-3x: {c.size}")
print("DONE")
