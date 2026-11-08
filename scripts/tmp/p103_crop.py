#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P103 delovna faza — zoom izrezi (po vzoru p98_crop). Uporaba:
python3 p103_crop.py <sken> <x0> <y0> <x1> <y1> <ime> [faktor]
Koordinate so na polni sliki skena (1989x1500)."""
import sys
from PIL import Image

scan = int(sys.argv[1])
x0, y0, x1, y1 = map(int, sys.argv[2:6])
ime = sys.argv[6]
fac = float(sys.argv[7]) if len(sys.argv) > 7 else 2.0

im = Image.open(f"/tmp/p103/scan-{scan:02d}.jpg")
c = im.crop((x0, y0, x1, y1))
c = c.resize((int(c.width * fac), int(c.height * fac)), Image.LANCZOS)
c.save(f"/tmp/p103/read/{ime}.png")
print(f"{ime}: {c.size}")
