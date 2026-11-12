#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — TIEBREAK-crops: r5 datum (10.|19.|26.-Oct) + r1/r2 datumi (12.|19.-Febr)
iz ISTEGA skena (s12), x6 zoom, SIRSI trak (datum + levi rob z robovno stevilko).
Izhod: /tmp/p259/tiebreak/ + kopija v repo p259-work/tiebreak/ (prezivi /tmp wipe)."""
import os
from PIL import Image, ImageDraw

SCAN = '/home/z/my-project/research/issue17/p259-work/s12.jpg'
OUT1 = '/tmp/p259/tiebreak'
OUT2 = '/home/z/my-project/research/issue17/p259-work/tiebreak'
os.makedirs(OUT1, exist_ok=True); os.makedirs(OUT2, exist_ok=True)

ROWS = (12, 280, 1260)  # s12: 12 vrstic

def yc(r):
    n, y0, y1 = ROWS
    pitch = (y1 - y0) / n
    return int(y0 + (r - 0.5) * pitch)

def half():
    n, y0, y1 = ROWS
    return int((y1 - y0) / n * 0.62) + 8

im = Image.open(SCAN)
print('sken:', im.size)

def band(r, x0, x1, zoom, label):
    cy = yc(r); hf = half()
    c = im.crop((x0, max(0, cy - hf), x1, min(im.size[1], cy + hf)))
    c = c.resize((int(c.width * zoom), int(c.height * zoom)), Image.LANCZOS)
    hdr = Image.new('RGB', (c.width, 40), 'white')
    d = ImageDraw.Draw(hdr)
    d.text((10, 10), label, fill='black')
    sep = Image.new('RGB', (c.width, 8), 'gray')
    return [hdr, c, sep]

def composite(name, parts):
    W = max(p.width for p in parts)
    H = sum(p.height for p in parts)
    out = Image.new('RGB', (W, H), 'white')
    y = 0
    for p in parts:
        out.paste(p, (0, y)); y += p.height
    for d in (OUT1, OUT2):
        out.save(os.path.join(d, name + '.jpg'), quality=94)
    print(name, out.size)

# Datumski stolpec sširjenim levim robom: x 10–260 (vključi robovne številke!), x6
parts = []
for r, lab in [(1, 'TRAK A = VRSTICA 1, datum (celoten zapis z letnico)'), (2, 'TRAK B = VRSTICA 2, datum (dito ali poln zapis)'), (5, 'TRAK C = VRSTICA 5, datum (dan + mesec + robovna stevilka ce viden)')]:
    parts += band(r, 10, 260, 6, lab)
composite('s12_tiebreak_dates', parts)

# Samo r5: ultra sirski (rob + datum), x7
parts5 = band(5, 0, 300, 7, 'VRSTICA 5 — ULTRA: levi rob + datumski stolpec')
composite('s12_r5_ultra', parts5)
print('DONE')
