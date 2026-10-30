#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P166 — detekcija vrstic mrliške 04894, leto 1900 (skeni 78–80).
P165-metoda (LEKCIJA P164: skeni DVOSTRANSKI razponi + ROTIRANI →
morfološka odstranitev navpičnih črt scipy opening 81×1 + zap-bprojekcija
0.052–0.064 + gap-merge 55). Vrstične meje: yc ± HALF (snap band).
s80 vsebuje MEJO 1900/01 = '1901' velika podčrtana na PRAZNI vrsti
(s80-sredina — VLM: velika podčrtana letnica + restart zap 1 + Januarj!)
→ marker-čeke via diag-PNG agent-oči. Diag PNG → agent-eyes kontrola."""
from PIL import Image, ImageDraw
import numpy as np, os, json
from scipy import ndimage

OUT = "/tmp/p166"
os.makedirs(OUT, exist_ok=True)
SCANS = (78, 79, 80)
HALF = 160          # snap pol-širina vrstice za izreze
TH_DARK = 140       # 0.55 × 255
COV = 0.035         # min delež črnila po odstranitvi črt
MERGE_GAP = 55      # združi fragmente iste vrstice
H_MIN, H_MAX = 12, 145   # višina tekstovne vrstice


def zap_rows(a, w, h):
    # zap-številke @ x 0.052–0.064 (natisnjen navpični naslov
    # 'Zaporedna štev.' + pravili DRSITA z rotacijo!). Širši band
    # 0.040–0.078 za morfološko odstranitev črt, ozek za projekcijo.
    wx0, wx1 = int(w * 0.040), int(w * 0.078)
    px0, px1 = int(w * 0.052), int(w * 0.064)
    band = a[:, wx0:wx1]
    binv = band < TH_DARK
    lines = ndimage.binary_opening(binv, structure=np.ones((81, 1), bool))
    lines = ndimage.binary_dilation(lines, structure=np.ones((5, 11), bool))
    clean = binv & ~lines
    proj = clean[:, px0 - wx0:px1 - wx0]
    frac = proj.mean(axis=1)
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
    merged = []
    for (g0, g1) in groups:
        if merged and g0 - merged[-1][1] <= MERGE_GAP:
            merged[-1] = (merged[-1][0], g1)
        else:
            merged.append((g0, g1))
    rows, markers = [], []
    for (y0, y1) in merged:
        hh = y1 - y0
        rec = {"y0": int(y0), "y1": int(y1), "yc": int((y0 + y1) // 2), "h": int(hh)}
        if H_MIN <= hh <= H_MAX:
            rec["y0"], rec["y1"] = int(max(0, rec["yc"] - HALF)), int(min(h, rec["yc"] + HALF))
            rows.append(rec)
        elif hh > H_MAX and hh < 420:
            # glava-skupina (glava + prva vrstica merged — črta-drifn): vrstica = dno
            yc = y1 - HALF // 2
            rec["yc"] = int(yc)
            rec["head"] = True
            rec["y0"], rec["y1"] = int(max(0, yc - HALF)), int(min(h, yc + HALF))
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
