#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P166 — rule-detekcija (natisnjene horizontalne črte tabele) s78–s80.
LEKCIJA P162: zap-projekcija spusti vrstice s bledimi ciframi. Pravila
tabele so OSTRA in POPOLNA (vsaka meja vrstice ima črto) → vrstice =
razponi med sosednjimi pravili (x-band 0.25–0.40 čez levo tabelo).
Izhod: /tmp/p166/rules.json (nadomesti vrstice v rows.json) + diag PNG."""
from PIL import Image, ImageDraw
import numpy as np, os, json

OUT = "/tmp/p166"
SCANS = (78, 79, 80)
XB0, XB1 = 0.25, 0.40   # band čez levo tabelo (mesec+vas+ime)
RULE_FRAC = 0.55        # min delež temnih px v vrsti = pravilo
GLAVA_Y = 240           # vrstice nad tem = glava tabele


def rules(a, w, h):
    band = a[:, int(w * XB0):int(w * XB1)]
    dark = (band < 150)
    frac = dark.mean(axis=1)
    ys = [y for y in range(h) if frac[y] > RULE_FRAC]
    groups, cur = [], []
    for y in ys:
        if cur and y - cur[-1] <= 3:
            cur.append(y)
        else:
            if cur:
                groups.append((cur[0], cur[-1]))
            cur = [y]
    if cur:
        groups.append((cur[0], cur[-1]))
    return groups


def main():
    report = {}
    for scan in SCANS:
        im = Image.open(f"{OUT}/s{scan:02d}.jpg")
        w, h = im.size
        a = np.asarray(im.convert("L"), dtype=np.float32)
        rs = rules(a, w, h)
        # pravila pod glavo → meje vrstic
        bounds = [g0 for (g0, g1) in rs if g0 > GLAVA_Y]
        rows = []
        for i in range(len(bounds) - 1):
            y0, y1 = bounds[i], bounds[i + 1]
            if y1 - y0 < 60:
                continue  # preozka (dvojni pravil / marker podčrtaj)
            rows.append({"y0": int(y0), "y1": int(y1),
                         "yc": int((y0 + y1) // 2), "h": int(y1 - y0)})
        report[f"s{scan:02d}"] = {"w": int(w), "h": int(h),
                                  "rules": [int(g0) for (g0, g1) in rs],
                                  "rows": rows}
        print(f"s{scan:02d}: pravil={len(rs)} vrstic={len(rows)} "
              f"yc={[r['yc'] for r in rows]}", flush=True)
    json.dump(report, open(f"{OUT}/rules.json", "w"), indent=1)
    # diag PNG: zelena pravila + rumene številke
    for scan in SCANS:
        rep = report[f"s{scan:02d}"]
        im = Image.open(f"{OUT}/s{scan:02d}.jpg").convert("RGB")
        dr = ImageDraw.Draw(im)
        w, h = im.size
        for i, r in enumerate(rep["rows"]):
            dr.line([(0, r["y0"]), (w, r["y0"])], fill=(255, 0, 0), width=1)
            dr.line([(0, r["y1"]), (w, r["y1"])], fill=(0, 160, 255), width=1)
            dr.text((w - 40, r["yc"] - 6), str(i + 1), fill=(255, 200, 0))
        for g in rep["rules"]:
            dr.line([(0, g), (30, g)], fill=(0, 200, 0), width=2)
        im.save(f"{OUT}/diag-rule-s{scan:02d}.png")
    print("diag-rule-PNG: shranjeni")


if __name__ == "__main__":
    main()
