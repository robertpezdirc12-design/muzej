#!/usr/bin/env python3
"""P256 — sistematični izrezi LEVE STRANI (x 40–1080) za vse skene: ženin-blok + nevesta-blok, zgornja/spodnja polovica, ×3."""
from PIL import Image
import os
OUT = '/tmp/p256/L'
os.makedirs(OUT, exist_ok=True)

JOBS = {
    's4': (300, 1490, 9), 's5': (300, 1370, 8), 's6': (290, 1355, 11), 's7': (300, 1405, 13),
}

for tag, (y0, y1, n) in JOBS.items():
    im = Image.open(f'/tmp/p256/{tag}.jpg')
    W, H = im.size
    # ženin-blok (datum/vas/hiša/ime/številke): x 40–640
    # nevesta-blok (vas/hiša/ime/številke/priče): x 600–1080 (prekrivanje 40px)
    for name, (x0, x1) in {'G': (40, 640), 'B': (600, min(1080, W-30))}.items():
        for half, (a, b) in {'T': (max(240, y0-60), (y0+y1)//2 + 40), 'B': ((y0+y1)//2 - 40, min(1500, y1+60))}.items():
            c = im.crop((x0, a, x1, b))
            c = c.resize((c.width*3, c.height*3), Image.LANCZOS)
            c.save(f'{OUT}/{tag}_{name}{half}.jpg', quality=90)
            print(f'{tag}_{name}{half}: x[{x0},{x1}] y[{a},{b}] -> {c.size}')
