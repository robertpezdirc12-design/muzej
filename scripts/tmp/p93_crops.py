#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P93 izrezi Griblje vrstic 1898 — pasovne meje (y0,y1 v dejanskih px ~1500).
Vsak izrez: levo x 55–935 (kraj+hišna+ime), desno x 920–1880 (starši/botra/babica/podpis);
2x upscale; JPEG q92. Hišne številke 5x za forenziko (x 520–655).
Kandidati Griblje 1898:
  s101 r5 (h39?); s102 r14 (h?), r20 (h61?);
  s103 r22 (h2), r30 (h81/31?);
  s104 r37 (h18), r42 (h32);
  s106 r63 (h56);
  s107 r71 (h33), r72 (h40), r76 (»Sriblje«?), r78 (h63), r79 (h52);
  s108 r89 (h53);
  s109 r96 (h90)."""
import os, sys
from PIL import Image

OUT = "/tmp/p93/crops"
CROPS = {
    101: {5: (1085, 1220)},
    102: {14: (740, 920), 20: (1280, 1460)},
    103: {22: (380, 590), 30: (1340, 1500)},
    104: {37: (750, 910), 42: (1355, 1500)},
    106: {63: (1010, 1190)},
    107: {71: (505, 680), 72: (650, 805), 76: (1040, 1180), 78: (1270, 1400), 79: (1390, 1500)},
    108: {89: (1245, 1405)},
    109: {96: (530, 715)},
}


def main():
    os.makedirs(OUT, exist_ok=True)
    only = [tuple(x.split(":")) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
    only = [(int(a), int(b)) for a, b in only] if only else None
    for scan, rows in CROPS.items():
        im = Image.open(f"/tmp/p93/scan-{scan}.jpg")
        for row, (y0, y1) in rows.items():
            if only and (scan, row) not in only:
                continue
            h = y1 - y0
            L = im.crop((55, y0, 935, y1))
            L = L.resize((L.width * 2, h * 2), Image.LANCZOS)
            R = im.crop((920, y0, 1880, y1))
            R = R.resize((R.width * 2, h * 2), Image.LANCZOS)
            L.save(f"{OUT}/s{scan}-r{row}-L.jpg", quality=92)
            R.save(f"{OUT}/s{scan}-r{row}-R.jpg", quality=92)
            H = im.crop((520, y0, 655, y1))
            H = H.resize((H.width * 5, h * 5), Image.LANCZOS)
            H.save(f"{OUT}/s{scan}-r{row}-H5.jpg", quality=95)
            print(f"s{scan} r{row}: y {y0}-{y1} (h={h})")


if __name__ == "__main__":
    main()
