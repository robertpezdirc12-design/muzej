#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P256 — detekcija vodoravnih črt tabele na s4–s7 (pikselska analiza)."""
from PIL import Image

def analyze(path, tag, x0=250, x1=2050, y0=230, y1=1490, thresh=120, minfrac=0.55, merge=6):
    im = Image.open(path).convert('L')
    W, H = im.size
    x1 = min(x1, W); y1 = min(y1, H)
    px = im.load()
    lines = []
    for y in range(y0, y1):
        dark = 0
        total = x1 - x0
        for x in range(x0, x1, 2):
            if px[x, y] < thresh:
                dark += 2
        f = dark / total
        if f >= minfrac:
            if lines and y - lines[-1][1] <= merge:
                lines[-1][1] = y
            else:
                lines.append([y, y])
    centers = [(a + b) // 2 for (a, b) in lines]
    print(f"=== {tag}: {len(centers)} crt (y-sredisca) ===")
    print(centers)
    return centers

for s in [4, 5, 6, 7]:
    analyze(f'/tmp/p256/s{s}.jpg', f's{s}')
