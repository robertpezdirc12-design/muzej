#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P255 — dodatni ciljni izrezi za dueli (vase/imeni/datumi)."""
from PIL import Image

OUT = "/tmp/p255"
s2 = Image.open(f"{OUT}/s2.jpg")
s3 = Image.open(f"{OUT}/s3.jpg")

zooms = [
    (s2, "z_m11_datum", None),
    (s2, "z_m2_datum", (120, 425, 460, 565)),
    (s2, "z_m3_vas", (140, 556, 980, 672)),
    (s2, "z_m4_vas", (140, 660, 760, 774)),
    (s2, "z_m5_vas", (140, 764, 880, 890)),
    (s2, "z_m6_imena", (140, 880, 1500, 996)),
    (s2, "z_m7_vas", (140, 984, 940, 1100)),
    (s2, "z_m8_vas", (140, 1190, 940, 1302)),
    (s3, "z_m10_vas", (140, 418, 940, 524)),
    (s3, "z_m11_vas", (140, 514, 940, 622)),
    (s3, "z_m12_vas", (140, 610, 940, 720)),
    (s3, "z_m14_vas", (140, 806, 940, 920)),
    (s3, "z_m15_vas", (140, 900, 940, 1020)),
    (s3, "z_m13_imena", (240, 700, 1050, 822)),
    (s2, "z_m1_vas", (140, 296, 760, 442)),
    (s3, "z_m9_vas", (140, 318, 760, 430)),
]
for im, name, box in zooms:
    if box is None:
        continue
    c = im.crop(box)
    w, h = c.size
    sc = min(3, max(1, int(1500 / w)))
    c.resize((w * sc, h * sc), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=92)
    print(name, "ok", c.size, "x", sc)

# s3 m11/m12 datumske celice
c = s3.crop((120, 505, 460, 625)); c = c.resize((c.size[0]*3, c.size[1]*3), Image.LANCZOS)
c.save(f"{OUT}/z_m11_datum.jpg", quality=92); print("z_m11_datum ok")
c = s3.crop((120, 600, 460, 720)); c = c.resize((c.size[0]*3, c.size[1]*3), Image.LANCZOS)
c.save(f"{OUT}/z_m12_datum.jpg", quality=92); print("z_m12_datum ok")
