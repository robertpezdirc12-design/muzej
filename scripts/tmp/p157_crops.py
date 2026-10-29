#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P157 — izrezi: L/R trakovi 17 GRIBLJE-vrstic (1891) + max-zoom celice
za odprta vprašanja + markerji. Koordinate iz diag-pregledov (ročno kalibrirane)."""
from PIL import Image
import os

OUT = "/tmp/p157/strips"
CELLS = "/tmp/p157/cells"
MARK = "/tmp/p157/markers"
for d in (OUT, CELLS, MARK):
    os.makedirs(d, exist_ok=True)

# (sken, y0, y1, oznaka) — Griblje-vrstice 1891 (iz diag pregledov)
ROWS = [
    (29, 1373, 1511, "s29-13-h64"),
    (30, 456, 586, "s30-17-h56"),
    (30, 1720, 1838, "s30-27-h46"),
    (31, 448, 577, "s31-30-h68"),
    (31, 828, 951, "s31-33-h16"),
    (31, 951, 1080, "s31-34-h9"),
    (31, 1569, 1689, "s31-39-h6"),
    (31, 1826, 1963, "s31-41-h61"),
    (32, 329, 465, "s32-42-h62"),
    (32, 465, 600, "s32-43-h55"),
    (33, 464, 607, "s33-55-h30"),
    (33, 607, 741, "s33-56-h23"),
    (33, 1029, 1157, "s33-59-h35"),
    (33, 1157, 1291, "s33-60-h35"),
    (33, 1429, 1570, "s33-62-h85"),
    (33, 1570, 1717, "s33-63-h71"),
    (33, 1717, 1845, "s33-64-h6"),
    # lead vrstice (kontekst)
    (28, 1640, 1801, "s28-91r1-h11V"),
    (28, 1801, 1946, "s28-91r2-h18O"),
    (34, 331, 464, "s34-92r1-h57"),
]

# max-zoom celice: (sken, y0, y1, x0, x1, zoom, oznaka) — x/y frakcije ABS (px)
CELL_DEFS = [
    # ime+stan+starost (L)
    (29, 1373, 1511, 0.03, 0.53, 3.2, "s29-13-L"),
    (29, 1373, 1511, 0.50, 0.99, 3.2, "s29-13-R"),
    (30, 456, 586, 0.10, 0.35, 4.5, "s30-17-hisa"),
    (30, 456, 586, 0.28, 0.53, 3.6, "s30-17-ime"),
    (30, 1720, 1838, 0.28, 0.53, 3.6, "s30-27-ime"),
    (30, 1838, 1961, 0.50, 0.99, 3.2, "s30-28-R"),
    (31, 448, 577, 0.62, 0.99, 3.6, "s31-30-podpis"),
    (31, 828, 951, 0.62, 0.99, 3.6, "s31-33-podpis"),
    (31, 1826, 1963, 0.03, 0.53, 3.2, "s31-41-L"),
    (31, 1826, 1963, 0.50, 0.99, 3.2, "s31-41-R"),
    (31, 1327, 1447, 0.50, 0.99, 3.6, "s31-37-R"),
    (32, 465, 600, 0.62, 0.99, 3.6, "s32-43-podpis"),
    (32, 329, 465, 0.62, 0.99, 3.6, "s32-42-podpis"),
    (33, 1029, 1291, 0.03, 0.35, 4.0, "s33-59-60-vas-hisa"),
    (33, 1570, 1717, 0.28, 0.53, 3.6, "s33-63-ime"),
    (33, 1570, 1717, 0.50, 0.80, 4.0, "s33-63-starost"),
    (33, 1429, 1570, 0.28, 0.53, 3.6, "s33-62-ime"),
    (33, 1717, 1845, 0.03, 0.53, 3.6, "s33-64-L"),
    (28, 1640, 1801, 0.28, 0.53, 3.6, "s28-91r1-ime"),
    (28, 1640, 1801, 0.03, 0.30, 4.0, "s28-91r1-dat-vas"),
    (28, 1801, 1946, 0.28, 0.53, 3.6, "s28-91r2-ime"),
    # markerji
    (28, 1407, 1650, 0.02, 0.30, 2.5, "s28-marker-1891"),
    (34, 83, 340, 0.02, 0.35, 2.5, "s34-marker-1892"),
    (29, 75, 140, 0.00, 0.14, 5.0, "s29-stran"),
    (32, 75, 140, 0.00, 0.14, 5.0, "s32-stran"),
    (33, 75, 140, 0.00, 0.14, 5.0, "s33-stran"),
]

# L/R trakovi (x frakcije) iz ABS vrstic
def main():
    n = 0
    for scan, y0, y1, tag in ROWS:
        im = Image.open(f"/tmp/p157/s{scan:02d}.jpg")
        w, h = im.size
        L = im.crop((0, max(0, y0 - 6), int(w * 0.53), min(h, y1 + 6)))
        L.resize((int(L.width * 2.2), int(L.height * 2.2)), Image.LANCZOS).save(f"{OUT}/{tag}-L.png")
        R = im.crop((int(w * 0.50), max(0, y0 - 6), w, min(h, y1 + 6)))
        R.resize((int(R.width * 2.2), int(R.height * 2.2)), Image.LANCZOS).save(f"{OUT}/{tag}-R.png")
        n += 2
    for scan, y0, y1, g0, g1, z, tag in CELL_DEFS:
        im = Image.open(f"/tmp/p157/s{scan:02d}.jpg")
        w, h = im.size
        c = im.crop((int(w * g0), y0, int(w * g1), min(h, y1)))
        c.resize((int(c.width * z), int(c.height * z)), Image.LANCZOS).save(f"{CELLS}/{tag}.png")
        n += 1
    print(f"izrezi: {n}")

if __name__ == "__main__":
    main()
