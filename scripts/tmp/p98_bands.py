#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P98 — pasovni izrezi (2x) za transkripcijo vrstic.
Leva polovica = Št/Leto-Mesec-dan/Kraj/Hiša/Ime/Vera-Spola-Stan; desna = Roditelja/Botra/Babica/Podpis."""
import os, sys
from PIL import Image

OUT = "/tmp/p98/crops"
os.makedirs(OUT, exist_ok=True)

scans = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [144]
for s in scans:
    im = Image.open(f"/tmp/p98/scan-{s:02d}.jpg")
    w, h = im.size
    y = 90
    band = 0
    while y < h - 20:
        y1 = min(y + 300, h)
        L = im.crop((60, y, 990, y1))
        L = L.resize((L.width * 2, L.height * 2), Image.LANCZOS)
        L.save(f"{OUT}/s{s}-b{band}-L.jpg", quality=92)
        R = im.crop((950, y, 1890, y1))
        R = R.resize((R.width * 2, R.height * 2), Image.LANCZOS)
        R.save(f"{OUT}/s{s}-b{band}-R.jpg", quality=92)
        print(f"s{s}-b{band}: y {y}-{y1}")
        y += 260  # 40px overlap
        band += 1
