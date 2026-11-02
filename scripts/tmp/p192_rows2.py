#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — detekcija vrstic v2b: prazen stolpec Pos.Nr (x95–155)."""
from PIL import Image
import numpy as np
import sys, json

def detect(scan):
    im = Image.open(f"/tmp/p192/{scan}.jpg").convert("L")
    a = np.array(im)
    band = a[:, 95:155].astype(float)
    dark = (band < 150).sum(axis=1)
    t = 60 * 0.45
    lines, y, H = [], 0, a.shape[0]
    while y < H:
        if dark[y] > t:
            y2 = y
            while y2 < H - 1 and dark[y2 + 1] > t: y2 += 1
            lines.append((y + y2) // 2); y = y2 + 1
        else: y += 1
    merged = []
    for l in lines:
        if merged and l - merged[-1] < 18: merged[-1] = (merged[-1] + l) // 2
        else: merged.append(l)
    return merged

out = {}
for scan in sys.argv[1:]:
    m = detect(scan)
    out[scan] = m
    print(f"{scan}: {m}")
json.dump(out, open("/tmp/p192/rows.json", "w"))
