#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P158 — detekcija vrstic mrliške 04894, leto 1892 (skeni 34–42).
Metoda P157: (1) detektiramo horizontalne črte (x-band 5–45 %, th/cov kaskada),
(2) ločimo pisane/prazne vrste prek gostote črnila, (3) diag-PNG za vizualno
kalibracijo. Izhod: /tmp/p158/lines.json + /tmp/p158/diag-sNN.png."""
from PIL import Image, ImageDraw
import numpy as np, os, json

OUT = "/tmp/p158"
os.makedirs(OUT, exist_ok=True)

SCANS = (34, 35, 36, 37, 38, 39, 40, 41, 42)


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
        im = Image.open(f"{OUT}/s{scan:02d}.jpg")
        w, h = im.size
        th, cov = 0.35, 0.22
        for cand in ((0.35, 0.25), (0.30, 0.18), (0.45, 0.35), (0.65, 0.30)):
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
        # diag-PNG
        d = ImageDraw.Draw(im.convert("RGB"))
        for i, (a, b) in enumerate(iv):
            col = (255, 0, 0) if rows[i]["pisana"] else (0, 160, 0)
            d.line([(0, a), (w, a)], fill=col, width=4)
            d.line([(0, b), (w, b)], fill=(255, 160, 0), width=2)
            d.text((30, (a + b) // 2), f"R{i}", fill=(0, 0, 255))
        im.convert("RGB").resize((w // 2, h // 2)).save(f"{OUT}/diag-s{scan:02d}.png")
    json.dump(report, open(f"{OUT}/lines.json", "w"))


if __name__ == "__main__":
    main()
