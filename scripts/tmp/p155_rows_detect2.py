#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P155 — natančna detekcija vrstic (nižji prag — črte so svetlejše kot v 1888)
+ izrez max-zoom celic za 8 GRIBLJE-vrstic (hišna št. + ime + vzrok + datum)."""
from PIL import Image
import numpy as np, os, json

OUT = "/tmp/p155/cells"
os.makedirs(OUT, exist_ok=True)
SCANS = (21, 22, 23, 24)


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


def intervals(im, th, cov, minh, maxh):
    w, h = im.size
    lines = find_lines(im, int(w * 0.05), int(w * 0.45), int(h * 0.04), int(h * 0.985), th, cov)
    return [(lines[i], lines[i + 1]) for i in range(len(lines) - 1)
            if minh <= lines[i + 1] - lines[i] <= maxh], lines


def main():
    report = {}
    for scan in SCANS:
        im = Image.open(f"/tmp/p155/s{scan:02d}.jpg")
        w, h = im.size
        for th, cov in ((0.35, 0.25), (0.30, 0.18), (0.45, 0.35)):
            iv, lines = intervals(im, th, cov, int(h * 0.035), int(h * 0.09))
            if len(iv) >= 6:
                break
        report[f"s{scan:02d}"] = {"th": th, "cov": cov, "lines": lines, "ivals": iv}
        print(f"s{scan:02d}: th={th} cov={cov} → črt {len(lines)}, intervalov {len(iv)}, "
              f"višine {[b - a for a, b in iv]}")
    json.dump(report, open("/tmp/p155/lines2.json", "w"))


if __name__ == "__main__":
    main()
