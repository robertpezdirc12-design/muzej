#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P257 — detekcija vodoravnih črt tabele na s6–s7 (pikselska analiza, po vzoru P256 lines.py)."""
from PIL import Image

def analyze(path, tag, x0=250, x1=2050, y0=230, y1=1490, thresh=120, minfrac=0.55, merge=6):
    im = Image.open(path).convert('L')
    W, H = im.size
    x1 = min(x1, W); y1 = min(y1, H)
    px = im.load()
    lines = []
    for y in range(y0, y1):
        dark = 0
        total = x1 - x0
        for x in range(x0, x1, 2):
            if px[x, y] < thresh:
                dark += 2
        f = dark / total
        if f >= minfrac:
            if lines and y - lines[-1][1] <= merge:
                lines[-1][1] = y
            else:
                lines.append([y, y])
    centers = [(a + b) // 2 for (a, b) in lines]
    print(f"=== {tag}: {len(centers)} crt (y-sredisca) ===")
    print(centers)
    return centers

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
    sm = []
    half = smooth // 2
    for i in range(len(ink)):
        a, b = max(0, i-half), min(len(ink), i+half+1)
        sm.append(sum(ink[a:b]) / (b-a))
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

for s in [6, 7]:
    p = f'/tmp/p257/s{s}.jpg'
    analyze(p, f's{s}')
    im = Image.open(p)
    W = im.size[0]
    valleys(p, f's{s}-L', 40, 1080)
