#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P257 — točna segmentacija vrstic na s6/s7: profil črnila po y (pasovi besedila)
+ detekcija navpičnih črt tabele po x. Leva stran razprtega lista = x 40–1030."""
from PIL import Image

def rowbands(path, tag, x0=40, x1=1030, y0=250, y1=1480, thresh=150, gap=14, minrun=28):
    im = Image.open(path).convert('L')
    W, H = im.size
    x1 = min(x1, W)
    px = im.load()
    n = x1 - x0
    ink = []
    for y in range(y0, y1):
        d = sum(1 for x in range(x0, x1) if px[x, y] < thresh)
        ink.append(d / n)
    # pasovi: sklenjeni nizi y z gostoto > 0.045, spojeni če presledek < gap
    bands = []
    on = False
    start = 0
    lastink = -99
    for i, v in enumerate(ink):
        if v > 0.045:
            if not on:
                on = True; start = i
            lastink = i
        else:
            if on and i - lastink >= gap:
                if lastink - start + 1 >= minrun:
                    bands.append((y0 + start, y0 + lastink))
                on = False
    if on and lastink - start + 1 >= minrun:
        bands.append((y0 + start, y0 + lastink))
    print(f"=== {tag}: {len(bands)} pasov besedila (y-robovi) ===")
    for b in bands:
        print(f"  y {b[0]}–{b[1]}  (vis {b[1]-b[0]+1}px)")
    return bands


def vrules(path, tag, y0=300, y1=1450, x0=40, x1=2040, thresh=120, minfrac=0.30):
    im = Image.open(path).convert('L')
    W, H = im.size
    x1 = min(x1, W)
    px = im.load()
    rows = y1 - y0
    cols = []
    for x in range(x0, x1):
        d = sum(1 for y in range(y0, y1, 2) if px[x, y] < thresh)
        if d / (rows / 2) >= minfrac:
            cols.append(x)
    # grupiraj
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
    centers = [int(sum(g)/len(g)) for g in groups]
    print(f"=== {tag}: navpične črte (x-središča) ===")
    print(centers)
    return centers

for s in [6, 7]:
    p = f'/tmp/p257/s{s}.jpg'
    rowbands(p, f's{s}-LEVO')
    vrules(p, f's{s}')
