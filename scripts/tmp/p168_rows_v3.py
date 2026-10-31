#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P168 v3 — konsolidacija: CIFRE (brez linij) + LINIJE (interpolirane).
P167-v1-bug: COM projekcije je mešal linije+cifre. v3-metoda:
 1. horizontalne linije = opening(clean, 1×30) → linija-y (interpolacija
    vrzeli do 2× mediana-razmika)
 2. cifre = clean & ~dilate(hlines) → COM skupine (12–145 px)
 3. celice = med linijami (100–230 px) → preslikava cifra→celica
    (cifra @ vrh celice: cifra-yc v [c0-40, c1+40])
s86–s90: nadaljevanje 1902 (zap 10–61) + MEJA 1902/03 = s90-sredina
('1903' podčrtano + restart zap 1 + Januarj = P167-lead POTRJEN!).
Izhod: /tmp/p168/rows3.json + poročilo za roko-kontrola."""
from PIL import Image
import numpy as np, json
from scipy import ndimage

OUT = "/tmp/p168"
SCANS = (86, 87, 88, 89, 90)
TH_DARK = 140
X0F, X1F = 0.040, 0.078
PX0F, PX1F = 0.052, 0.064


def analyze(scan):
    im = Image.open(f"{OUT}/s{scan:02d}.jpg")
    w, h = im.size
    a = np.asarray(im.convert("L"), dtype=np.float32)
    x0, x1 = int(w * X0F), int(w * X1F)
    px0, px1 = int(w * PX0F), int(w * PX1F)
    band = a[:, x0:x1]
    binv = band < TH_DARK
    vlines = ndimage.binary_opening(binv, structure=np.ones((81, 1), bool))
    vlines = ndimage.binary_dilation(vlines, structure=np.ones((5, 11), bool))
    clean = binv & ~vlines
    # --- linije ---
    hlines = ndimage.binary_opening(clean, structure=np.ones((1, 30), bool))
    hproj = hlines.mean(axis=1)
    raw = []
    for y in range(h):
        if hproj[y] > 0.35:
            if raw and y - raw[-1][-1] <= 6:
                raw[-1].append(y)
            else:
                raw.append([y])
    line_c = [int(np.mean(g)) for g in raw if len(g) <= 20]
    line_c = [y for y in line_c if y > 130]   # glava izključi
    # interpolacija vrzeli (do 2× mediana)
    gaps = [b - a2 for a2, b in zip(line_c, line_c[1:]) if 90 <= b - a2 <= 200]
    med = int(np.median(gaps)) if gaps else 137
    lines = list(line_c)
    for _ in range(3):                     # max 3 prehoda interpolacije
        new = []
        for i in range(len(lines) - 1):
            new.append(lines[i])
            gap = lines[i + 1] - lines[i]
            n = round(gap / med)
            if n == 2 and gap > med * 1.6:
                new.append(lines[i] + gap // 2)
        new.append(lines[-1])
        if new == lines:
            break
        lines = new
    # --- cifre (brez linij) ---
    hl = ndimage.binary_dilation(hlines, structure=np.ones((7, 15), bool))
    cif = clean & ~hl
    proj = cif[:, px0 - x0:px1 - x0]
    frac = proj.mean(axis=1)
    ys = [y for y in range(h) if frac[y] > 0.010]
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
    merged = []
    for (g0, g1) in groups:
        if merged and g0 - merged[-1][1] <= 40:
            merged[-1] = (merged[-1][0], g1)
        else:
            merged.append((g0, g1))
    cifre = [(int((g0 + g1) // 2), g0, g1) for (g0, g1) in merged
             if 12 <= (g1 - g0) <= 145]
    # --- celice: med zaporednimi linijami (+ prva celica nad line[0]) ---
    bounds = [max(150, lines[0] - med)] + lines if lines else []
    cells = []
    for i in range(len(bounds) - 1):
        c0, c1 = bounds[i], bounds[i + 1]
        if 100 <= c1 - c0 <= 230:
            cells.append({"y0": c0, "y1": c1, "yc": (c0 + c1) // 2})
    # preslikava
    rows = []
    used = set()
    for (yc, g0, g1) in cifre:
        best = None
        for ci, c in enumerate(cells):
            if c["y0"] - 40 <= yc <= c["y1"] + 40 and ci not in used:
                if best is None or abs(yc - c["yc"]) < abs(yc - cells[best]["yc"]):
                    best = ci
        if best is not None:
            rows.append({"cell": best, "yc": cells[best]["yc"],
                         "cifra_yc": yc, "c0": g0, "c1": g1})
            used.add(best)
        else:
            rows.append({"cell": None, "yc": yc, "cifra_yc": yc,
                         "c0": g0, "c1": g1, "orphan": True})
    return {"w": int(w), "h": int(h), "med": med,
            "lines": lines, "cells": cells, "rows": rows}


def main():
    report = {}
    for s in SCANS:
        d = analyze(s)
        key = f"s{s:02d}"
        report[key] = d
        inr = [r for r in d["rows"] if not r.get("orphan")]
        orph = [r for r in d["rows"] if r.get("orphan")]
        print(f"{key}: med={d['med']} linij={len(d['lines'])} "
              f"celic={len(d['cells'])} cifer={len(d['rows'])} "
              f"(v={len(inr)}, orph={len(orph)})")
        print(f"  celice-yc: {[c['yc'] for c in d['cells']]}")
        print(f"  cifre→celice: {[(r['cifra_yc'], r['cell']) for r in d['rows']]}")
    json.dump(report, open(f"{OUT}/rows3.json", "w"), indent=1)
    print("rows3.json")


if __name__ == "__main__":
    main()
