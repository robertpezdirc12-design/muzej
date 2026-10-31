#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P167 v2 — celica-podana detekcija vrstic (skeni 81–85).
FIZIKALNA metoda: horizontalne tabela-linije v zap-bandu (x 0.040–0.078)
izolirane s horizontalnim opening (1×30) → celice → zap-cifre (COM
detekcija) preslikane na celice → vrstica-center = celica-center.
Cifre, ki padejo IZVEN celic / manjkajo → roka-sanacija (meja/prazne).
Izhod: /tmp/p167/rows2.json + izpis celic/cifer za agent-eyes."""
from PIL import Image
import numpy as np, json, os
from scipy import ndimage

OUT = "/tmp/p167"
SCANS = (81, 82, 83, 84, 85)
TH_DARK = 140
X0F, X1F = 0.040, 0.078   # zap-band (širši, linije + cifre)
PX0F, PX1F = 0.052, 0.064  # ozek zap-projekcija pas (cifre)


def analyze(scan):
    im = Image.open(f"{OUT}/s{scan:02d}.jpg")
    w, h = im.size
    a = np.asarray(im.convert("L"), dtype=np.float32)
    x0, x1 = int(w * X0F), int(w * X1F)
    px0, px1 = int(w * PX0F), int(w * PX1F)
    band = a[:, x0:x1]
    binv = band < TH_DARK
    # navpične linije odstrani (opening 81×1 — P164-lekcija)
    vlines = ndimage.binary_opening(binv, structure=np.ones((81, 1), bool))
    vlines = ndimage.binary_dilation(vlines, structure=np.ones((5, 11), bool))
    clean = binv & ~vlines
    # horizontalne tabela-linije izoliraj (opening 1×30)
    hlines = ndimage.binary_opening(clean, structure=np.ones((1, 30), bool))
    hproj = hlines.mean(axis=1)
    line_ys = [y for y in range(h) if hproj[y] > 0.35]
    lines = []
    for y in line_ys:
        if lines and y - lines[-1][-1] <= 6:
            lines[-1].append(y)
        else:
            lines.append([y])
    line_c = [int(np.mean(g)) for g in lines if len(g) <= 20]
    # zap-cifre: COM skupine v ozkem pasu
    proj = clean[:, px0 - x0:px1 - x0]
    frac = proj.mean(axis=1)
    cov_ys = [y for y in range(h) if frac[y] > 0.010]
    groups, cur = [], []
    for y in cov_ys:
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
        if merged and g0 - merged[-1][1] <= 55:
            merged[-1] = (merged[-1][0], g1)
        else:
            merged.append((g0, g1))
    cands = [(int((g0 + g1) // 2), g0, g1) for (g0, g1) in merged
             if 12 <= (g1 - g0) <= 145]
    # celice: med zaporednimi linijami
    bounds = [0] + line_c + [h]
    cells = [(bounds[i], bounds[i + 1], (bounds[i] + bounds[i + 1]) // 2)
             for i in range(len(bounds) - 1)
             if (bounds[i + 1] - bounds[i]) >= 60]
    # preslikaj cifre na celice
    cell_map = []
    used = set()
    for (yc, g0, g1) in cands:
        for ci, (c0, c1, cc) in enumerate(cells):
            if c0 - 10 <= yc <= c1 + 10 and ci not in used:
                cell_map.append({"zapyc": yc, "cell": ci, "c0": c0, "c1": c1,
                                 "yc": cc, "cifra": True})
                used.add(ci)
                break
        else:
            cell_map.append({"zapyc": yc, "cell": None, "c0": g0, "c1": g1,
                             "yc": yc, "cifra": True, "orphan": True})
    return {"w": int(w), "h": int(h), "lines": line_c,
            "cells": [{"y0": c0, "y1": c1, "yc": cc}
                      for (c0, c1, cc) in cells],
            "cifre": cell_map}


def main():
    report = {}
    for s in SCANS:
        d = analyze(s)
        report[f"s{s:02d}"] = d
        ok = [c for c in d["cifre"] if not c.get("orphan")]
        orph = [c for c in d["cifre"] if c.get("orphan")]
        print(f"s{s:02d}: linij={len(d['lines'])} celic={len(d['cells'])} "
              f"cifer={len(d['cifre'])} (v celicah={len(ok)}, "
              f"brez={len(orph)})")
        print(f"  linije: {d['lines']}")
        print(f"  cifre-yc (orig COM): {[c['zapyc'] for c in d['cifre']]}")
        print(f"  celica-centri (vrstice): {[c['yc'] for c in ok]}")
        if orph:
            print(f"  ORPHAN: {[(c['zapyc'], c['c0'], c['c1']) for c in orph]}")
    json.dump(report, open(f"{OUT}/rows2.json", "w"), indent=1)
    print("rows2.json: shranjen")


if __name__ == "__main__":
    main()
