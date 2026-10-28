#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P154 — izrezi GRIBLJE-vrstic (leto 1888) za VLM forenziko + glave + marker.
s14–s20: uniformna mreža 13 vrstic (vzorec p153_rows.py). s21: po detektiranih
intervalih (6× 1888 + marker 1889 + 6× 1889). Izhod: /tmp/p154/rows3/."""
from PIL import Image
import numpy as np, os

OUT = "/tmp/p154/rows3"
os.makedirs(OUT, exist_ok=True)

# scan -> seznam (page_row_1based, serial) GRIBLJE-vrstic + [nrows za mrežo]
TARGETS = {
    14: [(1, 6), (2, 7), (5, 10), (8, 13), (10, 15)],
    15: [(2, 20), (3, 21), (4, 22), (5, 23), (6, 24)],
    16: [(6, 37), (12, 43), (13, 44)],
    18: [(3, 60), (6, 63), (9, 66), (11, 68)],
    19: [(2, 72), (4, 74), (11, 81), (12, 82)],
    20: [(1, 84), (4, 87), (6, 89)],
}


def find_lines(im, x0, x1, y0, y1, th=0.62, cov=0.12, gap=4):
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


def crop_row(im, scan, y0, y1, tag):
    w, h = im.size
    c = im.crop((0, max(0, y0 - 8), w, min(h, y1 + 8)))
    lw = int(w * 0.55)
    L = c.crop((0, 0, lw, c.height))
    R = c.crop((int(w * 0.44), 0, w, c.height))
    for half, part in (("L", L), ("R", R)):
        sc = 2.4 if part.width < 1500 else 2.0
        part.resize((int(part.width * sc), int(part.height * sc)), Image.LANCZOS).save(
            f"{OUT}/{tag}{half}.png")


def main():
    # — s14–s20: uniformna mreža 13 vrstic —
    for scan, targets in TARGETS.items():
        im = Image.open(f"/tmp/p154/s{scan:02d}.jpg")
        w, h = im.size
        top, bot = int(h * 0.055), int(h * 0.985)
        step = (bot - top) / 13
        for prow, serial in targets:
            y0 = int(top + (prow - 1) * step)
            y1 = int(top + prow * step)
            crop_row(im, scan, y0, y1, f"s{scan:02d}-r{prow:02d}")
        print(f"s{scan:02d}: {len(targets)} izrezov")

    # — s21: detektirani intervali (1888 r97–r102 + marker + 1889 r1–r6) —
    im = Image.open("/tmp/p154/s21.jpg")
    w, h = im.size
    lines = find_lines(im, int(w * 0.05), int(w * 0.45), int(h * 0.04), int(h * 0.985))
    ivals = [(lines[i], lines[i + 1]) for i in range(len(lines) - 1)
             if 42 <= lines[i + 1] - lines[i] <= 130]
    print(f"s21 intervali: {len(ivals)} — {[b - a for a, b in ivals]}")
    # pričakovano 13: 1–6 (1888), 7 = marker, 8–13 (1889)
    griblje_1888 = {1, 2, 3, 6}          # page-rows za ser. 97, 98, 99, 102
    griblje_1889 = {11}                   # page-row 11 = 1889 r4 (h55)
    for i, (a, b) in enumerate(ivals[:13], start=1):
        if i in griblje_1888 or i in griblje_1889:
            crop_row(im, 21, a, b, f"s21-r{i:02d}")
    print("s21: izrezi končani")

    # — glave »Leto 18 ..« s14–s17 (preveriti zadnji cifri!) —
    for scan in (14, 15, 16, 17):
        im = Image.open(f"/tmp/p154/s{scan:02d}.jpg")
        w, h = im.size
        c = im.crop((int(w * 0.06), int(h * 0.045), int(w * 0.30), int(h * 0.10)))
        c.resize((c.width * 4, c.height * 4), Image.LANCZOS).save(
            f"{OUT}/s{scan:02d}-glava.png")
    print("glave shranjene")

    # — marker 1889 na s21 (celota + zadnja cifra) —
    im = Image.open("/tmp/p154/s21.jpg")
    w, h = im.size
    lines = find_lines(im, int(w * 0.05), int(w * 0.45), int(h * 0.04), int(h * 0.985))
    ivals = [(lines[i], lines[i + 1]) for i in range(len(lines) - 1)
             if lines[i + 1] - lines[i] > 90]
    for k, (a, b) in enumerate(ivals):
        c = im.crop((0, a - 8, w, b + 8))
        c.resize((int(c.width * 2.2), int(c.height * 2.2)), Image.LANCZOS).save(
            f"{OUT}/s21-marker{k + 1}-full.png")
        r = im.crop((int(w * 0.5), a - 8, w, b + 8))
        r.resize((int(r.width * 3.5), int(r.height * 3.5)), Image.LANCZOS).save(
            f"{OUT}/s21-marker{k + 1}-right.png")
    print(f"marker-izrezi: {len(ivals)}")


if __name__ == "__main__":
    main()
