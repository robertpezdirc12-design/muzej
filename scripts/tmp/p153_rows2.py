#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P153 — natančna forenzika: detekcija horizontalnih črt tabele na skenih
mrliške 04894, izrez VSAKE vrstice (levo+desno polovico) z 2.4× povečavo.
Izhod: /tmp/p153/rows2/sNN-rRR{L,R}.png + /tmp/p153/lines-sNN.json"""
from PIL import Image
import numpy as np, os, json, sys

OUT = "/tmp/p153/rows2"
os.makedirs(OUT, exist_ok=True)


def find_lines(im, x0, x1, y0, y1):
    """Vrni y-pozicije horizontalnih črnih črt (povprečna temnost > 0.45)."""
    a = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
    band = a[y0:y1, x0:x1]
    dark = (band < 0.45).mean(axis=1)
    ys = [y for y in range(band.shape[0]) if dark[y] > 0.45]
    # združi sosednje
    groups, cur = [], []
    for y in ys:
        if cur and y - cur[-1] <= 3:
            cur.append(y)
        else:
            if cur:
                groups.append(int(np.mean(cur)) + y0)
            cur = [y]
    if cur:
        groups.append(int(np.mean(cur)) + y0)
    return groups


def main():
    report = {}
    for scan in [6, 8, 9, 11, 12, 13]:
        im = Image.open(f"/tmp/p153/s{scan:02d}.jpg")
        w, h = im.size
        # leva stran razpeta od ~2 % do ~49 % širine; tabela od ~3.5 % do ~98.5 % višine
        lx0, lx1 = int(w * 0.03), int(w * 0.47)
        y0, y1 = int(h * 0.035), int(h * 0.985)
        lines = find_lines(im, lx0, lx1, y0, y1)
        # izloči glavne veje (glava tabele) — zanimajo nas vrstične črtice med njimi
        rows = []
        for i in range(len(lines) - 1):
            a, b = lines[i], lines[i + 1]
            if b - a > int(h * 0.035):  # vrstica = vsaj 3.5 % višine
                rows.append((a, b))
        report[f"s{scan:02d}"] = {"lines": lines, "rows": rows}
        for j, (a, b) in enumerate(rows):
            pad_top = 14 if j == 0 else 6
            c = im.crop((0, max(0, a - pad_top), w, min(h, b + 6)))
            lw = int(w * 0.55)
            L = c.crop((0, 0, lw, c.height))
            R = c.crop((int(w * 0.44), 0, w, c.height))
            for half, part in (("L", L), ("R", R)):
                sc = 2.4 if part.width < 1500 else 2.0
                part.resize((int(part.width * sc), int(part.height * sc)), Image.LANCZOS).save(
                    f"{OUT}/s{scan:02d}-R{j+1:02d}{half}.png")
        print(f"s{scan:02d}: črt {len(lines)}, vrstic {len(rows)}")
    json.dump(report, open("/tmp/p153/lines.json", "w"))


if __name__ == "__main__":
    main()
