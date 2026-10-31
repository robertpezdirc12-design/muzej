#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P167 — konsolidacija vrstic mrliške 04894, leto 1901 (skeni 80–85).
v3-celica-metoda (linije + cifre-preslikava) roko potrjena z zapcol
rezinami + zoom (p166-lekcija: yc→zap-preslikavo VEDEJO verificirati
pikselsko!).
  s80 (P166-rows-final REUSE): 1900-rep zap57–61 + MEJA '1901' (@1035) +
       1901 zap1–6 (yc 1174–1848).
  s81: zap7–18 (VLM-'4'=zap7! — γ→7/4-zmeda; cifre @ vrh celic!) ·
  s82: zap19–30 ('Zaporedna štev.'-NASLOV-ostanek @239 IZKLJUČEN!) ·
  s83: zap31–42 · s84: zap43–54 (NASLOV @240 izključen!) ·
  s85: zap55 (VLM-'65' = 5/6-zmeda — zapcol @372 = '55' PRAZNO!) +
       MEJA 1901/02 ('1902.' podčrtana na PRAZNI vrsti @536) + 1902 zap1–10.
1901 = 6+12+12+12+12+1 = 55 VRSTIC (rast 61→55!).
Izhod: /tmp/p167/rows.json + diag-sNN.png (agent-eyes kontrola)."""
from PIL import Image, ImageDraw
import numpy as np, os, json

OUT = "/tmp/p167"
HALF = 160

ROWS = {
    "s80": {"zap1900": [373, 501, 641, 752, 895], "zap1901": [1174, 1318, 1439, 1571, 1711, 1848],
            "markers": [1035]},  # P166 rows-final REUSE (meja 1900/01 @1035)
    "s81": {"zap1901": [375, 513, 650, 787, 924, 1061, 1192, 1324, 1461, 1595, 1731, 1867]},
    "s82": {"zap1901": [395, 533, 672, 810, 947, 1086, 1223, 1360, 1499, 1637, 1774, 1907]},
    "s83": {"zap1901": [391, 529, 665, 799, 934, 1070, 1207, 1343, 1480, 1618, 1756, 1897]},
    "s84": {"zap1901": [395, 531, 667, 803, 939, 1073, 1209, 1344, 1476, 1606, 1737, 1869]},
    "s85": {"zap1901": [395], "meja": [536],
            "zap1902": [676, 807, 937, 1069, 1203, 1339, 1474, 1610, 1748, 1884]},
}


def main():
    report = {}
    for key, d in ROWS.items():
        scan = int(key[1:])
        im = Image.open(f"{OUT}/s{scan:02d}.jpg")
        w, h = im.size
        rows = []
        for tag in ("zap1900", "zap1901", "zap1902"):
            for yc in d.get(tag, []):
                rows.append({"yc": int(yc),
                             "y0": int(max(0, yc - HALF)),
                             "y1": int(min(h, yc + HALF)),
                             "year": int(tag[3:])})
        markers = [{"yc": int(m), "y0": int(m - 60), "y1": int(m + 60)}
                   for m in d.get("meja", []) + d.get("markers", [])]
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
            col = {1900: (255, 0, 0), 1901: (150, 60, 200), 1902: (220, 120, 30)}[r["year"]]
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
