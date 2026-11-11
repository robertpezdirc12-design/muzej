#!/usr/bin/env python3
"""P256 — doline gostote pisave = meje vrstic (presledki med vpisi)."""
from PIL import Image

def valleys(path, tag, x0, x1, y0=240, y1=1480, thresh=150, smooth=25, cut=0.06):
    im = Image.open(path).convert('L')
    W, H = im.size
    x1 = min(x1, W)
    px = im.load()
    n = x1 - x0
    ink = []
    for y in range(y0, y1):
        d = 0
        for x in range(x0, x1):
            if px[x, y] < thresh: d += 1
        ink.append(d / n)
    # glajenje
    sm = []
    half = smooth // 2
    for i in range(len(ink)):
        a, b = max(0, i-half), min(len(ink), i+half+1)
        sm.append(sum(ink[a:b]) / (b-a))
    # doline: lokalni minimum pod 'cut', med dvema vrhovoma
    out = []
    i = 0
    while i < len(sm):
        if sm[i] < cut:
            j = i
            while j < len(sm) and sm[j] < cut: j += 1
            out.append((y0 + (i+j)//2, round(min(sm[i:j]),3)))
            i = j
        else:
            i += 1
    print(f"=== {tag} x[{x0},{x1}]: {len(out)} dolin ===")
    print([v[0] for v in out])
    return [v[0] for v in out]

for s in [4,5,6,7]:
    im = Image.open(f'/tmp/p256/s{s}.jpg')
    W = im.size[0]
    # cela širina (čez pregib) in leva/desna polovica
    vL = valleys(f'/tmp/p256/s{s}.jpg', f's{s}-LEVO', 260, 1020)
    vR = valleys(f'/tmp/p256/s{s}.jpg', f's{s}-DESNO', 1140, W-60)
