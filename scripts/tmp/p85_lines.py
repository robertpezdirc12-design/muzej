#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detekcija horizontalnih ločnic tabele na levem listu skena (x∈[120,880])."""
from PIL import Image
import numpy as np
import sys

def lines(scan):
    im = Image.open(f"/tmp/p85/scan-{scan:02d}.jpg").convert("L")
    a = np.asarray(im, dtype=float)
    band = a[:, 120:880]
    darkness = (band < 120).mean(axis=1)
    rows = []
    y = 0
    n = len(darkness)
    while y < n:
        if darkness[y] > 0.5:
            y2 = y
            while y2 + 1 < n and darkness[y2 + 1] > 0.5:
                y2 += 1
            rows.append((y + y2) // 2)
            y = y2 + 1
        else:
            y += 1
    return rows

if __name__ == "__main__":
    for scan in [int(x) for x in sys.argv[1:]]:
        ls = lines(scan)
        print(f"skan {scan}: {len(ls)} črt: {ls}")
