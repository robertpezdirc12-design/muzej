#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P90 izrezi Griblje vrstic 1895 — pasovne meje (y0,y1 v dejanskih px ~1500).
Vsak izrez: levo x 55–935 (kraj+hišna+ime), desno x 920–1790 (starši/botra/babica/podpis);
2x upscale; JPEG q92. Hišne številke 5x za forenziko (x 640–790).
Griblje vrstice 1895: r15 (s79), r18/r19/r22/r26/r27 (s80),
r40/r43/r45/r48/r49 (s82), r53/r54/r55 (s83), r66 (s84)."""
import os, sys
from PIL import Image

OUT = "/tmp/p90/crops"
CROPS = {
    # sken: {vrstica: (y0, y1)}
    79: {15: (1235, 1335)},
    80: {18: (400, 500), 19: (490, 590), 22: (760, 860), 26: (1120, 1220), 27: (1210, 1310)},
    82: {40: (220, 320), 43: (505, 610), 45: (695, 800), 48: (980, 1085), 49: (1075, 1180)},
    83: {53: (305, 410), 54: (400, 505), 55: (495, 600)},
    84: {66: (410, 515)},
}


def main():
    os.makedirs(OUT, exist_ok=True)
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
    for scan, rows in CROPS.items():
        im = Image.open(f"/tmp/p90/scan-{scan}.jpg")
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
            # forenzika hišne številke 5x
            H = im.crop((640, y0, 790, y1))
            H = H.resize((H.width * 5, h * 5), Image.LANCZOS)
            H.save(f"{OUT}/r{row}-H5.jpg", quality=95)
            print(f"r{row}: y {y0}–{y1} (h={h}) → r{row}-L.jpg r{row}-R.jpg r{row}-H5.jpg")


if __name__ == "__main__":
    main()
