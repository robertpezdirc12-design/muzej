#!/usr/bin/env python3
"""P256 — detekcija črt, nižji prag + profil temnosti (top vrstice)."""
from PIL import Image

def analyze(path, tag, x0=250, x1=2050, y0=230, y1=1490, thresh=150, minfrac=0.30, merge=8):
    im = Image.open(path).convert('L')
    W, H = im.size
    x1 = min(x1, W); y1 = min(y1, H)
    px = im.load()
    prof = []
    for y in range(y0, y1):
        dark = 0
        total = x1 - x0
        for x in range(x0, x1, 2):
            if px[x, y] < thresh:
                dark += 2
        prof.append((y, dark / total))
    lines = []
    for (y, f) in prof:
        if f >= minfrac:
            if lines and y - lines[-1][1] <= merge:
                lines[-1][1] = y; lines[-1][2] = max(lines[-1][2], f)
            else:
                lines.append([y, y, f])
    print(f"=== {tag}: {len(lines)} crt ===")
    print([( (a+b)//2, round(f,2)) for (a,b,f) in lines])
    return lines

for s in [4,5,6,7]:
    analyze(f'/tmp/p256/s{s}.jpg', f's{s}')
