#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — izrezi za pagcheck (hdr) + datumski stolpec (dates_full + dates_grid z rdečo mrežo)."""
import os
from PIL import Image, ImageDraw

D = "/tmp/p259"
os.makedirs(D, exist_ok=True)

for s in [11, 12, 13]:
    im = Image.open(f"{D}/s{s}.jpg")
    W, H = im.size
    # 1) zgornji rob 130px ×2
    hdr = im.crop((0, 0, W, 130)).resize((int(W * 2), 260), Image.LANCZOS)
    hdr.save(f"{D}/hdr_s{s}.jpg", quality=92)
    # 2) datumski stolpec x 60–240, cela višina ×4
    dc = im.crop((60, 200, 240, H - 20))
    dc = dc.resize((dc.width * 4, dc.height * 4), Image.LANCZOS)
    dc.save(f"{D}/dates_full_s{s}.jpg", quality=92)
    # 3) datumski stolpec z rdečo mrežo vsakih 100px (originalne koordinate!) ×4
    g = im.crop((60, 150, 240, H - 20)).convert("RGB")
    draw = ImageDraw.Draw(g)
    y = 150
    while y < H - 20:
        draw.line([(0, y - 150), (g.width, y - 150)], fill=(255, 0, 0), width=2)
        draw.text((4, y - 150 + 3), f"y{y}", fill=(255, 0, 0))
        y += 50 if y < 400 else 100
    g = g.resize((g.width * 4, g.height * 4), Image.LANCZOS)
    g.save(f"{D}/dates_grid_s{s}.jpg", quality=92)
    print(f"s{s}: hdr + dates_full + dates_grid ({W}x{H})")
print("DONE")
