#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P162 — detekcija vrstic mrliške 04894, leto 1896 (skeni 55–61).
Zap-pasu pristop: rokopisne grupe (TH 140, COV 0.04, band x 0.045–0.105,
group-gap 30) = kandidati vrstic. Spodnji rob vezave (y0 > 0.965h) = šum.
MARKERJI (velike podčrtane letnice 1896./1897.) se izločijo po DROP_MARKERS
— položaje je vizualno potrdil izrez zap-stolpca (glej zapcol-s55/s60.png).
Izhod: /tmp/p162/rows.json + diag PNG."""
from PIL import Image, ImageDraw
import numpy as np, os, json

OUT = "/tmp/p162"
os.makedirs(OUT, exist_ok=True)
SCANS = (55, 56, 57, 58, 59, 60, 61)
TH, COV = 140, 0.04
BAND = (0.045, 0.105)
RAW_GAP = 6        # surove grupe (crte ostanejo tanke)
INK_H = 14         # min visina za rokopis (plastinke/crte h<=10 odpadejo)
MERGE_GAP = 55     # zdruzevanje rokopisnih grup iste vrstice (rezultat <= 100 px)
MAX_H = 100        # max visina zdruzenega rokopisa (marker+vrstica se ne zlijeta)
TOP_ZONE = 330     # y-center < TOP_ZONE = stran-glava/tabela-glava
BOT_ZONE_FRAC = 0.965
HALF = 72          # snap pol-višina vrstice za izreze
# markerji (velike letnice med vrsticami) — vizualno potrjeno:
#   s55: "1896." na y≈1315–1377 (med zap 52 in zap 1)
#   s60: "1897." na y≈1485–1545 (med zap 60 in zap 1)
DROP_MARKERS = {"s55": [(1315, 1377)], "s60": [(1485, 1545)]}


def raw_groups(a, w, h):
    x0, x1 = int(w * BAND[0]), int(w * BAND[1])
    frac = (a[:, x0:x1] < TH).mean(axis=1)
    ys = [y for y in range(h) if frac[y] > COV]
    groups, cur = [], []
    for y in ys:
        if cur and y - cur[-1] <= RAW_GAP:
            cur.append(y)
        else:
            if cur:
                groups.append((cur[0], cur[-1]))
            cur = [y]
    if cur:
        groups.append((cur[0], cur[-1]))
    return groups


def ink_rows(raw):
    """Surove grupe -> trim glave (g0 < TOP_ZONE < g1 -> prizay na 330)
    -> rokopis (h>=INK_H) -> merge iste vrstice."""
    ink = []
    for (g0, g1) in raw:
        if g1 <= TOP_ZONE:            # cela v glavi
            continue
        if g0 < TOP_ZONE < g1:        # seka mejo: prizay
            g0 = TOP_ZONE
        ink.append((g0, g1))
    ink = [(g0, g1) for (g0, g1) in ink if (g1 - g0 + 1) >= INK_H]
    merged = []
    for (g0, g1) in ink:
        if merged:
            p0, p1 = merged[-1]
            if g0 - p1 <= MERGE_GAP and (g1 - p0 + 1) <= 100:
                merged[-1] = (p0, g1)
                continue
        merged.append((g0, g1))
    return merged


def main():
    report = {}
    for scan in SCANS:
        key = f"s{scan:02d}"
        im = Image.open(f"{OUT}/s{scan:02d}.jpg")
        w, h = im.size
        a = np.asarray(im.convert("L"), dtype=np.float32)
        groups = ink_rows(raw_groups(a, w, h))
        cand = []
        for (g0, g1) in groups:
            yc = int((g0 + g1) // 2)
            if yc < TOP_ZONE:             # stran-glava / tabela-glava
                continue
            if g0 > BOT_ZONE_FRAC * h:    # vez/shadow na spodnjem robu
                continue
            cand.append({"y0": int(g0), "y1": int(g1),
                         "yc": yc, "h": int(g1 - g0 + 1)})
        drops = DROP_MARKERS.get(key, [])
        rows, markers = [], []
        for c in cand:
            hit = any(not (c["y1"] < m0 or c["y0"] > m1) for (m0, m1) in drops)
            (markers if hit else rows).append(c)
        report[key] = {"w": int(w), "h": int(h), "rows": rows,
                       "markers": markers, "dropped_groups": len(cand) - len(rows) - len(markers)}
        print(f"{key}: kandidatov={len(cand)} vrstic={len(rows)} "
              f"markerjev={len(markers)} "
              f"yc={[r['yc'] for r in rows]}", flush=True)
    json.dump(report, open(f"{OUT}/rows.json", "w"), indent=1)
    # diag PNG
    for scan in SCANS:
        rep = report[f"s{scan:02d}"]
        im = Image.open(f"{OUT}/s{scan:02d}.jpg").convert("RGB")
        dr = ImageDraw.Draw(im)
        w, h = im.size
        for i, r in enumerate(rep["rows"]):
            dr.line([(0, r["yc"] - HALF), (w, r["yc"] - HALF)], fill=(255, 0, 0), width=1)
            dr.line([(0, r["yc"] + HALF), (w, r["yc"] + HALF)], fill=(0, 160, 255), width=1)
            dr.text((w - 46, r["yc"] - 6), str(i + 1), fill=(255, 210, 0))
        for m in rep["markers"]:
            dr.line([(0, m["y0"]), (w, m["y0"])], fill=(0, 190, 0), width=2)
            dr.line([(0, m["y1"]), (w, m["y1"])], fill=(0, 190, 0), width=2)
            dr.text((w - 46, m["yc"] - 6), "M", fill=(0, 220, 0))
        im.save(f"{OUT}/diag-s{scan:02d}.png")
    print("diag-PNG: shranjeni")


if __name__ == "__main__":
    main()
