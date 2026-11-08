#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P92 izrezi Griblje vrstic 1897 — pasovne meje (y0,y1 v dejanskih px ~1500).
Vsak izrez: levo x 55–935 (kraj+hišna+ime), desno x 920–1790 (starši/botra/babica/podpis);
2x upscale; JPEG q92. Hišne številke 5x za forenziko (x 640–790).
Griblje vrstice 1897:
  s93 r8 (h12); s94 r12 (h32), r15 (h10), r21 (h23);
  s95 r25 (h37), r26 (h54), r28 (h60), r29 (h2), r31 (h43?);
  s96 r38 (h23), r41 (h46);
  s98 r52 (h31), r53 (h10); s99 r60 (h40), r63 (h20), r65 (h31?), r66 (h11?);
  s100 r79 (h61?), r80 (h65?); s101 r84 (h45)."""
import os, sys
from PIL import Image

OUT = "/tmp/p92/crops"
CROPS = {
    93: {8: (1040, 1145), 11: (1330, 1440)},
    94: {12: (335, 440), 15: (575, 685), 21: (1170, 1285)},
    95: {25: (400, 510), 26: (495, 605), 28: (690, 800), 29: (785, 895), 31: (975, 1085)},
    96: {38: (505, 620), 41: (800, 915)},
    98: {51: (690, 800), 52: (795, 905)},
    99: {60: (290, 400), 63: (575, 685), 65: (760, 870), 66: (850, 960)},
    100: {79: (1070, 1150), 80: (1170, 1270)},
    101: {84: (355, 465)},
}


def main():
    os.makedirs(OUT, exist_ok=True)
    only = [tuple(x.split(":")) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
    only = [(int(a), int(b)) for a, b in only] if only else None
    for scan, rows in CROPS.items():
        im = Image.open(f"/tmp/p92/scan-{scan}.jpg")
        for row, (y0, y1) in rows.items():
            if only and (scan, row) not in only:
                continue
            h = y1 - y0
            L = im.crop((55, y0, 935, y1))
            L = L.resize((L.width * 2, h * 2), Image.LANCZOS)
            R = im.crop((920, y0, 1790, y1))
            R = R.resize((R.width * 2, h * 2), Image.LANCZOS)
            L.save(f"{OUT}/s{scan}-r{row}-L.jpg", quality=92)
            R.save(f"{OUT}/s{scan}-r{row}-R.jpg", quality=92)
            H = im.crop((520, y0, 645, y1))
            H = H.resize((H.width * 5, h * 5), Image.LANCZOS)
            H.save(f"{OUT}/s{scan}-r{row}-H5.jpg", quality=95)
            print(f"s{scan} r{row}: y {y0}-{y1} (h={h})")


if __name__ == "__main__":
    main()
