#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P162 — detekcija vrstic mrliške 04894, leto 1896 (skeni 55–61).
DETERMINISTIČNI zap-stolpec pristop: vsaka rokopisna zap-številka (band
x 0.045–0.105) = 1 vrstica tabele; veliki markerji (podčrtana letnica) so
VIŠJI in se izločijo po višini. Vrstične meje: yc ± HALF (snap band).
Izhod: /tmp/p162/rows.json + diag PNG."""
from PIL import Image, ImageDraw
import numpy as np, os, json

OUT = "/tmp/p162"
os.makedirs(OUT, exist_ok=True)
SCANS = (55, 56, 57, 58, 59, 60, 61)
HALF = 160          # snap pol-širina vrstice za izreze
TH_DARK = 140       # 0.55 × 255
COV = 0.04          # min delež temnine v bandi (≈5 px črnila iz 130 px)
H_MIN, H_MAX = 15, 110   # višina rokopisne številke (markerji > 110!)


def zap_rows(a, w, h):
    x0, x1 = int(w * 0.045), int(w * 0.105)
    band = a[:, x0:x1]
    frac = (band < TH_DARK).mean(axis=1)
    ys = [y for y in range(h) if frac[y] > COV]
    groups, cur = [], []
    for y in ys:
        if cur and y - cur[-1] <= 15:
            cur.append(y)
        else:
            if cur:
                groups.append((cur[0], cur[-1]))
            cur = [y]
    if cur:
        groups.append((cur[0], cur[-1]))
    rows, markers = [], []
    for (y0, y1) in groups:
        hh = y1 - y0
        rec = {"y0": int(y0), "y1": int(y1), "yc": int((y0 + y1) // 2), "h": int(hh)}
        if H_MIN <= hh <= H_MAX:
            rec["y0"], rec["y1"] = int(max(0, rec["yc"] - HALF)), int(min(h, rec["yc"] + HALF))
            rows.append(rec)
        else:
            markers.append(rec)
    return rows, markers


def main():
    report = {}
    for scan in SCANS:
        im = Image.open(f"{OUT}/s{scan:02d}.jpg")
        w, h = im.size
        a = np.asarray(im.convert("L"), dtype=np.float32)  # 0–255
        rows, markers = zap_rows(a, w, h)
        report[f"s{scan:02d}"] = {"w": int(w), "h": int(h), "rows": rows,
                                  "markers": markers}
        print(f"s{scan:02d}: vrstic={len(rows)} markerjev={len(markers)} "
              f"yc={[r['yc'] for r in rows]}", flush=True)
    json.dump(report, open(f"{OUT}/rows.json", "w"), indent=1)
    # diag PNG: rumene številke vrstic ob zap-stolpcu
    for scan in SCANS:
        rep = report[f"s{scan:02d}"]
        im = Image.open(f"{OUT}/s{scan:02d}.jpg").convert("RGB")
        dr = ImageDraw.Draw(im)
        w, h = im.size
        for i, r in enumerate(rep["rows"]):
            dr.line([(0, r["y0"]), (w, r["y0"])], fill=(255, 0, 0), width=1)
            dr.line([(0, r["y1"]), (w, r["y1"])], fill=(0, 160, 255), width=1)
            dr.text((w - 40, r["yc"] - 6), str(i + 1), fill=(255, 200, 0))
        for m in rep["markers"]:
            dr.line([(0, m["y0"]), (w, m["y0"])], fill=(0, 180, 0), width=2)
            dr.line([(0, m["y1"]), (w, m["y1"])], fill=(0, 180, 0), width=2)
        im.save(f"{OUT}/diag-s{scan:02d}.png")
    print("diag-PNG: shranjeni")


if __name__ == "__main__":
    main()
