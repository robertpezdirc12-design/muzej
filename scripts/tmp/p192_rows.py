#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — avtomatska detekcija vrstic v2 (občutljivejši prag)."""
from PIL import Image
import numpy as np
import sys

def detect_rows(scan, x0=180, x1=760, thr=170, frac=0.30):
    im = Image.open(f"/tmp/p192/{scan}.jpg").convert("L")
    a = np.array(im)
    band = a[:, x0:x1].astype(float)
    dark = (band < thr).sum(axis=1)
    t = (x1 - x0) * frac
    lines = []
    y = 0
    H = a.shape[0]
    while y < H:
        if dark[y] > t:
            y2 = y
            while y2 < H - 1 and dark[y2 + 1] > t:
                y2 += 1
            lines.append((y + y2) // 2)
            y = y2 + 1
        else:
            y += 1
    return lines

for scan in sys.argv[1:]:
    ls = detect_rows(scan)
    merged = []
    for l in ls:
        if merged and l - merged[-1] < 22:
            merged[-1] = (merged[-1] + l) // 2
        else:
            merged.append(l)
    gaps = [(merged[i], merged[i+1]) for i in range(len(merged) - 1)]
    rows = [g for g in gaps if 55 < g[1] - g[0] < 130]
    print(f"{scan}: črte={len(merged)} vrstic={len(rows)}")
    print("  " + " ".join(f"{a}-{b}" for a, b in rows))
