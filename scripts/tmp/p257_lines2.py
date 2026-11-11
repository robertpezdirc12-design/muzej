#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P257 — detekcija črt tabele na s6/s7 z NIŽJIM pragom (P256 lines.py je s 0.55
našel 0-1 črt — tabele na teh straneh so svetlejše/prekinjene)."""
from PIL import Image

def analyze(path, tag, x0=250, x1=2050, y0=230, y1=1480, thresh=150, minfrac=0.35, merge=8):
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
    print(f"=== {tag}: {len(centers)} crt ===")
    print(centers)
    return centers

for s in [6, 7]:
    analyze(f'/tmp/p257/s{s}.jpg', f's{s}')
