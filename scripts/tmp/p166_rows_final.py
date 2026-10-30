#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P166 — konsolidacija vrstic mrliške 04894, leto 1900 (skeni 75–80).
Zap-stolpčna projekcija COV=0.010 (morfološka odstranitev črt 81×1).
s75: 1899-rep (zap60–61) + MEJA '1900' (~y660–740, PRAZNA vrsta + velika
     podčrtana letnica) + 1900 zap1–8 (yc 848–1787).
s76: zap9–20 · s77: zap21–32 (merge 1326/1380→1353) · s78: zap33–44 ·
s79: zap45–56 · s80: zap57–61 + MEJA '1901' (~y1035) + 1901 zap1–6.
Izhod: /tmp/p166/rows.json + diag-sNN.png (agent-eyes kontrola)."""
from PIL import Image, ImageDraw
import numpy as np, os, json

OUT = "/tmp/p166"
HALF = 160

# zap-rows po skenu (yc vrednosti iz COV=0.010 projekcije, ročno potrjene
# z diag/zapcol rezinami; 1900 vrstice označene)
ROWS = {
    "s75": {"zap1899": [383, 520], "zap1900": [848, 991, 1112, 1247, 1376, 1507, 1644, 1787],
            "markers": [660]},   # '1900' velika podčrtana — PRAZNA vrsta
    "s76": {"zap1900": [399, 525, 650, 800, 927, 1071, 1204, 1333, 1483, 1617, 1750, 1886]},
    "s77": {"zap1900": [391, 533, 670, 804, 938, 1056, 1202, 1353, 1465, 1593, 1724, 1861]},
    "s78": {"zap1900": [389, 521, 659, 791, 933, 1058, 1195, 1320, 1454, 1592, 1724, 1853]},
    "s79": {"zap1900": [383, 526, 663, 793, 935, 1058, 1196, 1329, 1474, 1619, 1731, 1870]},
    "s80": {"zap1900": [373, 501, 641, 752, 895], "zap1901": [1174, 1318, 1439, 1571, 1711, 1848],
            "markers": [1035]},  # '1901' velika podčrtana — PRAZNA vrsta
}


def main():
    report = {}
    for key, d in ROWS.items():
        scan = int(key[1:])
        im = Image.open(f"{OUT}/s{scan:02d}.jpg")
        w, h = im.size
        rows = []
        for tag in ("zap1899", "zap1900", "zap1901"):
            for yc in d.get(tag, []):
                rows.append({"yc": int(yc),
                             "y0": int(max(0, yc - HALF)),
                             "y1": int(min(h, yc + HALF)),
                             "year": int(tag[3:])})
        markers = [{"yc": int(m), "y0": int(m - 60), "y1": int(m + 60)}
                   for m in d.get("markers", [])]
        report[key] = {"w": int(w), "h": int(h), "rows": rows, "markers": markers}
        print(f"{key}: vrstic={len(rows)} markerjev={len(markers)}")
    json.dump(report, open(f"{OUT}/rows.json", "w"), indent=1)
    # diag PNG
    for key, rep in report.items():
        scan = int(key[1:])
        im = Image.open(f"{OUT}/s{scan:02d}.jpg").convert("RGB")
        dr = ImageDraw.Draw(im)
        w, h = im.size
        for i, r in enumerate(rep["rows"]):
            col = (255, 0, 0) if r["year"] == 1900 else (150, 60, 200)
            dr.line([(0, r["y0"]), (w, r["y0"])], fill=col, width=1)
            dr.line([(0, r["y1"]), (w, r["y1"])], fill=(0, 160, 255), width=1)
            dr.text((w - 40, r["yc"] - 6), str(i + 1), fill=(255, 200, 0))
        for m in rep["markers"]:
            dr.line([(0, m["y0"]), (w, m["y0"])], fill=(0, 190, 0), width=2)
            dr.line([(0, m["y1"]), (w, m["y1"])], fill=(0, 190, 0), width=2)
        im.save(f"{OUT}/diag-{key}.png")
    print("diag-PNG: shranjeni")


if __name__ == "__main__":
    main()
