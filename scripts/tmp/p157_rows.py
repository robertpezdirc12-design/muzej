#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P157 — detekcija vrstic + izrezi (L/R serije + max-zoom celice + markerji).
Metoda P155/P156: celostanski VLM pregled je identificiral Griblje-vrstice;
tukaj (1) detektiramo horizontalne črte, (2) ločimo pisane/prazne vrste prek
gostote črnila, (3) izrežemo L/R trake Griblje-vrstic + max-zoom celice za
odprta vprašanja + markerje (meja 1892, številke strani)."""
from PIL import Image
import numpy as np, os, json

OUT = "/tmp/p157/strips"
CELLS = "/tmp/p157/cells"
MARK = "/tmp/p157/markers"
for d in (OUT, CELLS, MARK):
    os.makedirs(d, exist_ok=True)

SCANS = (28, 29, 30, 31, 32, 33, 34)


def find_lines(im, x0, x1, y0, y1, th, cov, gap=4):
    a = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
    band = a[y0:y1, x0:x1]
    dark = (band < th).mean(axis=1)
    ys = [y for y in range(len(dark)) if dark[y] > cov]
    groups, cur = [], []
    for y in ys:
        if cur and y - cur[-1] <= gap:
            cur.append(y)
        else:
            if cur:
                groups.append(int(np.mean(cur)) + y0)
            cur = [y]
    if cur:
        groups.append(int(np.mean(cur)) + y0)
    return groups


def ink_density(im, y0, y1, x0f, x1f, th=0.55):
    a = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
    w = im.size[0]
    band = a[y0 + 3:y1 - 3, int(w * x0f):int(w * x1f)]
    return float((band < th).mean())


def main():
    report = {}
    for scan in SCANS:
        im = Image.open(f"/tmp/p157/s{scan:02d}.jpg")
        w, h = im.size
        th, cov = 0.35, 0.22
        for cand in ((0.35, 0.25), (0.30, 0.18), (0.45, 0.35)):
            lines = find_lines(im, int(w * 0.05), int(w * 0.45), int(h * 0.03), int(h * 0.99), cand[0], cand[1])
            iv = [(lines[i], lines[i + 1]) for i in range(len(lines) - 1)
                  if int(h * 0.032) <= lines[i + 1] - lines[i] <= int(h * 0.10)]
            if len(iv) >= 8:
                th, cov = cand
                break
        rows = []
        for (a, b) in iv:
            dens = ink_density(im, a, b, 0.04, 0.98)
            rows.append({"y0": a, "y1": b, "dens": round(dens, 5), "pisana": dens > 0.008})
        report[f"s{scan:02d}"] = {"th": th, "cov": cov, "n_iv": len(iv),
                                  "pisane": sum(1 for r in rows if r["pisana"]),
                                  "rows": rows}
        print(f"s{scan:02d}: th={th} cov={cov} → intervalov {len(iv)}, pisanih {report[f's{scan:02d}']['pisane']}, "
              f"višine {[b - a for a, b in iv][:14]}")
    json.dump(report, open("/tmp/p157/lines.json", "w"))


if __name__ == "__main__":
    main()
