#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P161 — izrezi: L/R trakovi Griblje-vrstic (2.2×) + max-zoom celice spori.
Izboljšava P158–P160: vrstične meje iz NAČRTNE ozkopasne detekcije (zap-stolpec
band 0.05–0.10, th 0.60, cov 0.45) — brez snap_band ugibanja. Izrezi:
/tmp/p161/strips + /tmp/p161/cells."""
from PIL import Image
import os, json

OUT = "/tmp/p161/strips"
CELLS = "/tmp/p161/cells"
for d in (OUT, CELLS):
    os.makedirs(d, exist_ok=True)

# natančne vrstične meje (y0, y1) iz ozkopasne detekcije — zap → (y0, y1)
# s51 SANACIJA: zap1 = 670–888 (2-vrstični, Januarj INLINE); marker = 469–670!
ROWS = {
    51: {1: (670, 888), 2: (888, 1031), 3: (1031, 1168), 4: (1168, 1304),
         5: (1304, 1444), 6: (1444, 1583), 7: (1583, 1718), 8: (1718, 1840),
         9: (1840, 1965), 0: (469, 670, "marker-1895")},
    52: {10: (298, 439), 11: (439, 576), 12: (576, 715), 13: (715, 856),
         14: (856, 991), 15: (991, 1132), 16: (1132, 1271), 17: (1271, 1407),
         18: (1407, 1547), 19: (1547, 1681), 20: (1681, 1811), 21: (1811, 1949)},
    53: {22: (314, 450), 23: (450, 584), 24: (584, 718), 25: (718, 851),
         26: (851, 982), 27: (982, 1110), 28: (1110, 1242), 29: (1242, 1382),
         30: (1382, 1517), 31: (1517, 1654), 32: (1654, 1788), 33: (1788, 1930)},
    54: {34: (308, 446), 35: (446, 585), 36: (585, 724), 37: (724, 863),
         38: (863, 1002), 39: (1002, 1141), 40: (1141, 1280), 41: (1280, 1420),
         42: (1420, 1558), 43: (1558, 1700), 44: (1700, 1831), 45: (1831, 1961)},
    55: {46: (307, 449), 47: (449, 589), 48: (589, 724), 49: (724, 866),
         50: (866, 1001), 51: (1001, 1135), 52: (1135, 1273),
         0: (1273, 1532, "marker-1896")},
}

# trakovi: (skan, zap, label)
STRIPS = [
    (51, 1, "r1-jakobcic-lead"), (51, 4, "r4-dragos"),
    (52, 11, "r11-jozek"), (52, 12, "r12-pavcic"), (52, 13, "r13-hrisan"),
    (52, 15, "r15-brodanic-maria"), (52, 16, "r16-brodanic-anton"), (52, 18, "r18-pezdirec"),
    (53, 22, "r22-grinec"), (53, 27, "r27-hottin"), (53, 29, "r29-hlevic"), (53, 33, "r33-zugel"),
    (54, 34, "r34-susmelj"), (54, 36, "r36-mrtvorojena"), (54, 37, "r37-klepec"), (54, 39, "r39-sepina"),
    (55, 49, "r49-krizan"), (55, 50, "r50-simonic"), (55, 51, "r51-jaklovic"),
]

# max-zoom celice: (skan, zap, x0f, x1f, ime)
CELLS_DEF = [
    # s51-r1 LEAD — Krasinec 50/30? + ime/stan PEZDIREC-glyph
    (51, 1, 0.04, 0.24, "s51-r1-datum"),
    (51, 1, 0.19, 0.38, "s51-r1-vas-hisna"),
    (51, 1, 0.25, 0.38, "s51-r1-hisna-wide"),
    (51, 1, 0.30, 0.57, "s51-r1-ime-wide"),
    # s51-r4 Dragoš — Griblje 12 + podpis
    (51, 4, 0.04, 0.38, "s51-r4-vas-hisna"),
    (51, 4, 0.30, 0.57, "s51-r4-ime-wide"),
    # s52 Griblje vrstice
    (52, 11, 0.04, 0.38, "s52-r11-vas-hisna"),
    (52, 11, 0.30, 0.57, "s52-r11-ime-wide"),
    (52, 11, 0.47, 0.80, "s52-r11-starost-vzrok"),
    (52, 12, 0.04, 0.57, "s52-r12-L-hisa-ime"),
    (52, 13, 0.04, 0.57, "s52-r13-L-hisa-ime"),
    (52, 15, 0.04, 0.57, "s52-r15-L-hisa-ime"),
    (52, 15, 0.47, 0.80, "s52-r15-starost-vzrok"),
    (52, 16, 0.04, 0.57, "s52-r16-L-hisa-ime"),
    (52, 18, 0.04, 0.57, "s52-r18-L-hisa-ime"),
    (52, 18, 0.47, 0.80, "s52-r18-starost-vzrok"),
    # s53
    (53, 22, 0.04, 0.57, "s53-r22-L-hisa-ime"),
    (53, 27, 0.47, 0.85, "s53-r27-vzrok-podpis"),
    (53, 29, 0.04, 0.57, "s53-r29-L-hisa-ime"),
    (53, 33, 0.04, 0.30, "s53-r33-datum"),
    # s54
    (54, 34, 0.04, 0.57, "s54-r34-L-hisa-ime"),
    (54, 34, 0.72, 1.00, "s54-r34-podpis"),
    (54, 36, 0.04, 0.57, "s54-r36-L-hisa-ime"),
    (54, 36, 0.72, 1.00, "s54-r36-podpis"),
    (54, 37, 0.04, 0.57, "s54-r37-L-hisa-ime"),
    (54, 39, 0.04, 0.57, "s54-r39-L-hisa-ime"),
    (54, 39, 0.47, 0.80, "s54-r39-starost-vzrok"),
    (54, 39, 0.72, 1.00, "s54-r39-podpis"),
    # s55
    (55, 49, 0.04, 0.57, "s55-r49-L-hisa-ime"),
    (55, 49, 0.26, 0.38, "s55-r49-hisna-wide"),
    (55, 49, 0.47, 0.80, "s55-r49-starost-vzrok"),
    (55, 49, 0.72, 1.00, "s55-r49-podpis"),
    (55, 50, 0.04, 0.26, "s55-r50-datum"),
    (55, 51, 0.04, 0.57, "s55-r51-L-hisa-ime"),
    (55, 51, 0.72, 1.00, "s55-r51-podpis"),
    (55, 0, 0.03, 0.32, "s55-marker-1896"),
]

ZOOM_STRIP, ZOOM_CELL = 2.2, 3.0
PAD = 8  # px čez pravilo (ascender/descender)


def main():
    imgs = {}
    manifest = {"strips": [], "cells": []}
    for scan, zap, label in STRIPS:
        if scan not in imgs:
            imgs[scan] = Image.open(f"/tmp/p161/s{scan:02d}.jpg")
        im = imgs[scan]
        w, h = im.size
        y0, y1 = ROWS[scan][zap if zap in ROWS[scan] else 0][:2]
        for side, (x0f, x1f) in (("L", (0.0, 0.52)), ("R", (0.48, 1.0))):
            crop = im.crop((int(w * x0f), max(0, y0 - PAD), int(w * x1f), min(h, y1 + PAD)))
            crop = crop.resize((int(crop.width * ZOOM_STRIP), int(crop.height * ZOOM_STRIP)), Image.LANCZOS)
            p = f"{OUT}/s{scan:02d}-{label}-{side}.png"
            crop.save(p)
            manifest["strips"].append(p)
    for scan, zap, x0f, x1f, name in CELLS_DEF:
        if scan not in imgs:
            imgs[scan] = Image.open(f"/tmp/p161/s{scan:02d}.jpg")
        im = imgs[scan]
        w, h = im.size
        y0, y1 = ROWS[scan][zap if zap in ROWS[scan] else 0][:2]
        crop = im.crop((int(w * x0f), max(0, y0 - PAD), int(w * x1f), min(h, y1 + PAD)))
        crop = crop.resize((int(crop.width * ZOOM_CELL), int(crop.height * ZOOM_CELL)), Image.LANCZOS)
        p = f"{CELLS}/{name}.png"
        crop.save(p)
        manifest["cells"].append(p)
    json.dump(manifest, open("/tmp/p161/crops-manifest.json", "w"), indent=1)
    print(f"trakovi: {len(manifest['strips'])} · celice: {len(manifest['cells'])}")


if __name__ == "__main__":
    main()
