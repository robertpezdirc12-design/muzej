#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — mreža-vsledki za kalibracijo y-koordinat (črta na 50px + oznake)."""
from PIL import Image, ImageDraw
import sys

for scan in sys.argv[1:]:
    im = Image.open(f"/tmp/p192/{scan}.jpg").convert("RGB")
    d = ImageDraw.Draw(im)
    for y in range(0, im.height, 50):
        c = (255, 0, 0) if y % 200 == 0 else (0, 160, 255)
        d.line([(0, y), (im.width, y)], fill=c, width=2)
        d.text((8, y + 3), str(y), fill=(255, 0, 0) if y % 200 == 0 else (0, 100, 255))
        d.text((im.width - 60, y + 3), str(y), fill=(255, 0, 0) if y % 200 == 0 else (0, 100, 255))
    im.save(f"/tmp/p192/grid-{scan}.png")
    print(f"grid-{scan}.png OK")
