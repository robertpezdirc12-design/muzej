#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P98 — izrezi glav strani (zgornji pas) za preslikavo sken→stran."""
import os, sys
from PIL import Image

OUT = "/tmp/p98/crops"
os.makedirs(OUT, exist_ok=True)

scans = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(143, 149))
for s in scans:
    im = Image.open(f"/tmp/p98/scan-{s:02d}.jpg")
    w, h = im.size
    # zgornji pas z številko strani (desno zgoraj pri tiskani knjigi) + levi del glave
    top = im.crop((0, 0, w, 150))
    top = top.resize((int(w * 1.6), int(150 * 1.6)), Image.LANCZOS)
    top.save(f"{OUT}/hdr-{s:02d}.jpg", quality=92)
    print(f"sken {s}: hdr-{s:02d}.jpg ({top.size})")
