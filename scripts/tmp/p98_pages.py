#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P98 — celostranski izrezi (zgornja/spodnja polovica, 1.5×) za prvo branje."""
import os, sys
from PIL import Image

OUT = "/tmp/p98/crops"
os.makedirs(OUT, exist_ok=True)

scans = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [144]
for s in scans:
    im = Image.open(f"/tmp/p98/scan-{s:02d}.jpg")
    w, h = im.size
    for tag, y0, y1 in (("top", 80, 800), ("bot", 780, 1500)):
        c = im.crop((0, y0, w, y1))
        c = c.resize((int(w * 1.5), int((y1 - y0) * 1.5)), Image.LANCZOS)
        c.save(f"{OUT}/s{s}-{tag}.jpg", quality=92)
    print(f"sken {s}: s{s}-top.jpg + s{s}-bot.jpg")
