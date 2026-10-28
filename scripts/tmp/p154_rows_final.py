#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P154 — KONČNI forenzični izrezi GRIBLJE-vrstic (leto 1888).
Kalibracija po vizualnih sidrih (ser. številke) na vsakem skenu;
centri = linearni fit prva→zadnja vrstica. Izhod: /tmp/p154/fx/."""
from PIL import Image
import os

OUT = "/tmp/p154/fx"
os.makedirs(OUT, exist_ok=True)

# scan -> {serial: center_y}
CAL = {
    14: {6: 312, 7: 418, 10: 736, 13: 1055, 15: 1267},
    15: {20: 434, 21: 538, 22: 642, 23: 746, 24: 850},
    16: {37: 860, 43: 1494, 44: 1599},
    18: {60: 549, 63: 863, 66: 1177, 68: 1386},
    19: {72: 440, 74: 649, 81: 1384, 82: 1489},
    20: {84: 350, 87: 669, 89: 881},
    21: {97: 377, 98: 497, 99: 617, 102: 977},  # 1888
}
S21_1889 = {4: 1575}  # 1889-r4 Griblje h53 (P155-lead, za kontekst)


def crop_row(im, cy, tag, half_h=56):
    w, h = im.size
    c = im.crop((0, max(0, cy - half_h), w, min(h, cy + half_h)))
    lw = int(w * 0.55)
    L = c.crop((0, 0, lw, c.height))
    R = c.crop((int(w * 0.44), 0, w, c.height))
    for half, part in (("L", L), ("R", R)):
        sc = 2.4 if part.width < 1500 else 2.0
        part.resize((int(part.width * sc), int(part.height * sc)), Image.LANCZOS).save(
            f"{OUT}/{tag}{half}.png")


def main():
    for scan, rows in CAL.items():
        im = Image.open(f"/tmp/p154/s{scan:02d}.jpg")
        for serial, cy in sorted(rows.items()):
            crop_row(im, cy, f"s{scan:02d}-n{serial:03d}")
        print(f"s{scan:02d}: {len(rows)}")
    im = Image.open("/tmp/p154/s21.jpg")
    for serial, cy in S21_1889.items():
        crop_row(im, cy, f"s21-p1889-n{serial:03d}")
    print("končano")


if __name__ == "__main__":
    main()
