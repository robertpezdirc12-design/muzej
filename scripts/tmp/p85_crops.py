#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P85 izrezi Griblje vrstic — frakcijske meje (y0,y1 v dejanskih px 1500).
Vsak izrez: levo x 55–935, desno x 920–1790; 2x upscale; JPEG q92."""
import os, sys
from PIL import Image

OUT = "/tmp/p85/crops"
CROPS = {
    # sken: {vrstica: (y0, y1)}
    43: {6: (700, 830)},
    44: {14: (350, 465), 15: (465, 550), 19: (760, 855), 22: (1005, 1095), 23: (1095, 1180)},
    45: {31: (570, 680)},
    46: {42: (500, 650), 44: (765, 880), 47: (995, 1115), 51: (1425, 1500), 52: (1410, 1500)},
    47: {54: (385, 510), 61: (1075, 1185)},
    48: {66: (385, 495), 67: (495, 590), 68: (590, 690), 71: (890, 990), 72: (990, 1090),
         75: (1280, 1370), 76: (1370, 1455), 77: (1455, 1500)},
    49: {79: (385, 495), 85: (910, 1020)},
}


def main():
    os.makedirs(OUT, exist_ok=True)
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
    for scan, rows in CROPS.items():
        im = Image.open(f"/tmp/p85/scan-{scan:02d}.jpg")
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
