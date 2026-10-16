#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P87 izrezi Griblje vrstic 1892 — frakcijske meje (y0,y1 v dejanskih px ~1500).
Vsak izrez: levo x 55–935, desno x 920–1790; 2x upscale; JPEG q92."""
import os, sys
from PIL import Image

OUT = "/tmp/p86/crops87"
CROPS = {
    # sken: {vrstica: (y0, y1)}
    56: {8: (955, 1065), 11: (1265, 1375)},
    57: {13: (240, 355), 17: (650, 765), 20: (955, 1070)},
    60: {50: (340, 455), 54: (785, 900)},
    61: {60: (235, 350), 64: (680, 795), 68: (1125, 1240), 70: (1345, 1460)},
    62: {80: (1240, 1355)},
}


def main():
    os.makedirs(OUT, exist_ok=True)
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
    for scan, rows in CROPS.items():
        im = Image.open(f"/tmp/p86/scan-{scan:02d}.jpg")
        for row, (y0, y1) in rows.items():
            if only and row not in only:
                continue
            h = y1 - y0
            L = im.crop((55, y0, 935, y1))
            L = L.resize((L.width * 2, h * 2), Image.LANCZOS)
            R = im.crop((920, y0, 1790, y1))
            R = R.resize((R.width * 2, h * 2), Image.LANCZOS)
            L.save(f"{OUT}/r{row}-L.jpg", quality=92)
            R.save(f"{OUT}/r{row}-R.jpg", quality=92)
            print(f"r{row}: y {y0}–{y1} (h={h}) → r{row}-L.jpg r{row}-R.jpg")


if __name__ == "__main__":
    main()
