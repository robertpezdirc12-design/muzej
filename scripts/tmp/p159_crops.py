#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P159 — izrezi: R-trakovi Griblje-vrstic (2.2×) + max-zoom celice spori.
Griblje-1893 = 10 vrstic (zap 5, 7, 19, 25, 41, 44, 45, 52, 57, 67).
Izhod: /tmp/p159/strips/ + /tmp/p159/cells/."""
from PIL import Image
import os

OUT = "/tmp/p159/strips"
CELLS = "/tmp/p159/cells"
for d in (OUT, CELLS):
    os.makedirs(d, exist_ok=True)

# (sken, y0, y1, zap) — L-band meje (gap-vrstice ročno)
ROWS = [
    (41, 1317, 1444, 5),
    (41, 1575, 1712, 7),
    (42, None, None, 19),   # L11 iz lines.json
    (43, None, None, 25),   # L5
    (44, 1272, 1407, 41),   # gap vrstica
    (44, 1671, 1814, 44),
    (44, 1814, 1950, 45),
    (45, 1146, 1282, 52),
    (45, 1822, 1967, 57),
    (46, 1560, 1700, 67),
]

import json
lines = json.load(open("/tmp/p159/lines.json"))
LIDX = {19: ("s42", 11), 25: ("s43", 5), 57: ("s45", 12)}
rows = []
for scan, y0, y1, zap in ROWS:
    if y0 is None:
        key, idx = LIDX[zap]
        r = lines[key]["L"]["rows"][idx]
        y0, y1 = r["y0"], r["y1"]
    rows.append((scan, y0, y1, zap))

def snap_band(a, w, yc, x0f, x1f, half=160, th=0.55):
    """najmočnejši horizontalni črti okoli yc na R-strani"""
    import numpy as np
    band = a[max(0, yc - half):yc + half, int(w * x0f):int(w * x1f)]
    dark = (band < 0.5).mean(axis=1)
    ys = [y for y in range(len(dark)) if dark[y] > 0.5]
    if len(ys) < 2:
        return yc - 68, yc + 68
    groups, cur = [], []
    for y in ys:
        if cur and y - cur[-1] <= 4:
            cur.append(y)
        else:
            if cur:
                groups.append(int(np.mean(cur)) + yc - half)
            cur = [y]
    if cur:
        groups.append(int(np.mean(cur)) + yc - half)
    if len(groups) >= 2:
        return groups[0], groups[-1]
    return yc - 68, yc + 68


import numpy as np
for scan, y0, y1, zap in rows:
    im = Image.open(f"/tmp/p159/s{scan:02d}.jpg")
    w, h = im.size
    a = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
    yc = (y0 + y1) // 2
    # R-trak 2.2× (x 0.47–0.98), y snap na R-strani
    ry0, ry1 = snap_band(a, w, yc, 0.55, 0.95)
    pad = 8
    crop = im.crop((int(w * 0.47), max(0, ry0 - pad), int(w * 0.98), min(h, ry1 + pad)))
    f = 2.2
    crop = crop.resize((int(crop.width * f), int(crop.height * f)), Image.LANCZOS)
    crop.save(f"{OUT}/zap{zap:02d}-R.png")
    # L-trak 2.2× (x 0.04–0.50)
    crop = im.crop((int(w * 0.04), max(0, y0 - pad), int(w * 0.50), min(h, y1 + pad)))
    crop = crop.resize((int(crop.width * f), int(crop.height * f)), Image.LANCZOS)
    crop.save(f"{OUT}/zap{zap:02d}-L.png")
    # max-zoom celice 3.5×
    cells = [
        (0.395, 0.50, "hisna"),    # hišna št.
        (0.545, 0.80, "star-vzrok"),  # starost + bolezen
        (0.76, 0.98, "podpis"),
    ]
    for x0f, x1f, lab in cells:
        cy0, cy1 = (y0 + y1) // 2 - 78, (y0 + y1) // 2 + 78
        if lab == "hisna":
            cy0, cy1 = y0 - 4, y1 + 4
        crop = im.crop((int(w * x0f), max(0, cy0), int(w * x1f), min(h, cy1)))
        f = 3.5 if lab != "hisna" else 4.0
        crop = crop.resize((int(crop.width * f), int(crop.height * f)), Image.LANCZOS)
        crop.save(f"{CELLS}/zap{zap:02d}-{lab}.png")
    print(f"zap {zap}: s{scan} y {y0}-{y1} R-snap {ry0}-{ry1} ✓")
print("STRIPS + CELLS ✓")
