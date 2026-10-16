#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P90 — detektor horizontalnih mrežnih črt leve strani (x 120–780) vsakega skena.
Vrne y-pozicije temnih horizontalnih črt = meje vrstic tabele."""
import sys
from PIL import Image

SCANS = [78, 79, 80, 81, 82, 83, 84, 85]

for s in SCANS:
    im = Image.open(f"/tmp/p90/scan-{s}.jpg").convert("L")
    w, h = im.size
    px = im.load()
    bands = []
    for y in range(80, h - 20):
        dark = 0
        for x in range(120, 780, 6):
            if px[x, y] < 150:
                dark += 1
        if dark >= 55:  # dolga temna črta (rjava mreža)
            bands.append(y)
    # zruži sosednje
    lines = []
    for y in bands:
        if lines and y - lines[-1][-1] <= 3:
            lines[-1].append(y)
        else:
            lines.append([y])
    ys = [sum(g) // len(g) for g in lines]
    print(f"scan-{s} ({w}x{h}): {len(ys)} črt")
    print("  ", ys)
