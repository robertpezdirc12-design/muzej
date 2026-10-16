#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P89 izrezi Griblje vrstic 1894 — frakcijske meje (y0,y1 v dejanskih px ~1500).
Vsak izrez: levo x 55–935 (kraj+hišna+ime), desno x 920–1790 (starši/botra/babica/podpis);
2x upscale; JPEG q92. Večje izrezi 5x za forenziko hišnih števil (x 660–760)."""
import os, sys
from PIL import Image

OUT = "/tmp/p89/crops"
CROPS = {
    # sken: {vrstica: (y0, y1)}
    70: {4: (700, 845)},
}


def main():
    os.makedirs(OUT, exist_ok=True)
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
    for scan, rows in CROPS.items():
        im = Image.open(f"/tmp/p89/scan-{scan}.jpg")
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
            H = im.crop((650, y0, 780, y1))
            H = H.resize((H.width * 5, h * 5), Image.LANCZOS)
            H.save(f"{OUT}/r{row}-H5.jpg", quality=95)
            print(f"r{row}: y {y0}–{y1} (h={h}) → r{row}-L.jpg r{row}-R.jpg r{row}-H5.jpg")


if __name__ == "__main__":
    main()
