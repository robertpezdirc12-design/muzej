#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P158 — izrezi: L/R trakovi Griblje-vrstic (2.2×) + max-zoom celice spori.
Metoda P157: groba centra iz ruler-diagov → snap_band (pripenjanje na najmočnejši
horizontalni črti ±150px) → natančen (y0,y1). Izrezi: /tmp/p158/strips, /tmp/p158/cells."""
from PIL import Image
import numpy as np, os, json

OUT = "/tmp/p158/strips"
CELLS = "/tmp/p158/cells"
for d in (OUT, CELLS):
    os.makedirs(d, exist_ok=True)

# groba centra vrstic (polna ločljivost y) iz ruler-pregledov
ROW_CENTERS = {
    34: [(1, 410, "lead-r1"), (6, 1090, "r6"), (8, 1370, "r8"), (9, 1510, "r9")],
    35: [(14, 510, "r14"), (21, 1450, "r21"), (24, 1740, "r24-stravs")],
    36: [(27, 675, "r27"), (34, 1645, "r34")],
    37: [(46, 1790, "r46"), (43, 1280, "r43-prezgodaj")],
    38: [(48, 420, "r48"), (50, 700, "r50"), (56, 1620, "r56"), (57, 1770, "r57")],
    39: [(59, 420, "r59"), (61, 700, "r61"), (64, 1190, "r64"), (67, 1680, "r67")],
    40: [(72, 710, "r72")],
    41: [(81, 415, "r81"), (0, 720, "marker-1893")],
}

# max-zoom celice: (skan, y_center, x0f, x1f, ime)
CELLS_DEF = [
    # s34 lead — ime / starost / podpis / datum
    (34, 410, 0.04, 0.24, "s34-r1-L1-datum"),
    (34, 410, 0.20, 0.40, "s34-r1-L2-hisa-ime"),
    (34, 410, 0.47, 0.72, "s34-r1-R1-starost-vzrok"),
    (34, 410, 0.76, 0.97, "s34-r1-R2-podpis"),
    # s38 header page number (37 vs 34!)
    (38, 78, 0.02, 0.20, "s38-header-stran"),
    (39, 78, 0.02, 0.20, "s39-header-stran"),
    # s35 r14 — vas/hisna/ime + podpis
    (35, 510, 0.04, 0.24, "s35-r14-L1-datum"),
    (35, 510, 0.20, 0.42, "s35-r14-L2-hisa-ime"),
    (35, 510, 0.76, 0.97, "s35-r14-R2-podpis"),
    # s35 r21 — hisna/ime/podpis Šašelj
    (35, 1450, 0.20, 0.42, "s35-r21-L2-hisa-ime"),
    (35, 1450, 0.76, 0.97, "s35-r21-R2-podpis"),
    # s36 r27 — starost/vzrok Mertvod + ime
    (36, 675, 0.20, 0.42, "s36-r27-L2-hisa-ime"),
    (36, 675, 0.47, 0.72, "s36-r27-R1-starost-vzrok"),
    # s36 r34 — vas/hisna/ime
    (36, 1645, 0.04, 0.42, "s36-r34-L-hisa-ime"),
    # s37 r46 — hisna/ime/starost
    (37, 1790, 0.04, 0.42, "s37-r46-L-hisa-ime"),
    (37, 1790, 0.47, 0.72, "s37-r46-R1-starost-vzrok"),
    # s38 r48/r50/r56/r57
    (38, 420, 0.04, 0.42, "s38-r48-L-hisa-ime"),
    (38, 420, 0.47, 0.72, "s38-r48-R1-starost-vzrok"),
    (38, 700, 0.04, 0.42, "s38-r50-L-hisa-ime"),
    (38, 700, 0.47, 0.97, "s38-r50-R-vzrok-podpis"),
    (38, 1620, 0.04, 0.42, "s38-r56-L-hisa-ime"),
    (38, 1620, 0.47, 0.72, "s38-r56-R1-starost-vzrok"),
    (38, 1770, 0.04, 0.42, "s38-r57-L-hisa-ime"),
    # s39 r59/r61/r64
    (39, 420, 0.04, 0.42, "s39-r59-L-hisa-ime"),
    (39, 420, 0.47, 0.72, "s39-r59-R1-starost-vzrok"),
    (39, 700, 0.04, 0.42, "s39-r61-L-hisa-ime"),
    (39, 700, 0.47, 0.72, "s39-r61-R1-starost-vzrok"),
    (39, 1190, 0.04, 0.42, "s39-r64-L-hisa-ime"),
    # s40 r72
    (40, 710, 0.04, 0.42, "s40-r72-L-hisa-ime"),
    (40, 710, 0.47, 0.72, "s40-r72-R1-starost-vzrok"),
    # s41 r81 (1892 zadnja) — vas! hisna/ime/vzrok + podpis
    (41, 415, 0.04, 0.42, "s41-r81-L-hisa-ime"),
    (41, 415, 0.47, 0.72, "s41-r81-R1-starost-vzrok"),
    (41, 415, 0.76, 0.97, "s41-r81-R2-podpis"),
    # s41 marker 1893 (boundary style)
    (41, 720, 0.02, 0.45, "s41-marker-1893"),
    # s39 r67 podpis (Rauq+repa)
    (39, 1680, 0.76, 0.97, "s39-r67-R2-podpis"),
]


def snap_band(im, yc, half=160):
    """najmočnejši horizontalni črti okoli yc (±half) → (y0, y1)"""
    a = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
    h, w = a.shape
    band = a[max(0, yc - half):min(h, yc + half), int(w * 0.06):int(w * 0.44)]
    dark = (band < 0.6).mean(axis=1)
    lo = max(0, yc - half)
    idx = np.argsort(dark)[::-1]
    lines = []
    for i in idx:
        y = i + lo
        if all(abs(y - l) > 30 for l in lines):
            lines.append(y)
        if len(lines) >= 2:
            break
    y0, y1 = sorted(lines)
    return y0, y1


def crop_zoom(im, y0, y1, x0f, x1f, zoom, path):
    w = im.size[0]
    c = im.crop((int(w * x0f), max(0, y0 - 6), int(w * x1f), y1 + 6))
    c = c.resize((int(c.width * zoom), int(c.height * zoom)), Image.LANCZOS)
    c.save(path)


def main():
    report = []
    for scan, rows in ROW_CENTERS.items():
        im = Image.open(f"/tmp/p158/s{scan:02d}.jpg")
        w, h = im.size
        for (row, yc, name) in rows:
            y0, y1 = snap_band(im, yc)
            if y1 - y0 < 60:  # snap fail → raw band
                y0, y1 = yc - 85, yc + 85
            crop_zoom(im, y0, y1, 0.045, 0.47, 2.2, f"{OUT}/s{scan:02d}-{name}-L.png")
            crop_zoom(im, y0, y1, 0.47, 0.96, 2.2, f"{OUT}/s{scan:02d}-{name}-R.png")
            report.append({"scan": scan, "row": row, "name": name, "y0": int(y0), "y1": int(y1),
                           "h": int(y1 - y0)})
            print(f"s{scan:02d}-{name}: y {y0}–{y1} (h {y1-y0})")
    for (scan, yc, x0f, x1f, name) in CELLS_DEF:
        im = Image.open(f"/tmp/p158/s{scan:02d}.jpg")
        y0, y1 = snap_band(im, yc)
        if y1 - y0 < 50:
            y0, y1 = yc - 80, yc + 80
        if "header" in name:
            y0, y1 = max(0, yc - 40), yc + 60
        if "marker" in name:
            y0, y1 = yc - 100, yc + 100
        crop_zoom(im, y0, y1, x0f, x1f, 3.0, f"{CELLS}/{name}.png")
        print(f"cell {name}: y {y0}–{y1}")
    json.dump(report, open("/tmp/p158/strips-report.json", "w"), indent=1)


if __name__ == "__main__":
    main()
