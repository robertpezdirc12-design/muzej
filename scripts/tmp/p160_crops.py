#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P160 — forenzični izrezi: Griblje-vrstice 1894 (zap 14, 22, 24, 30, 37, 38)
+ s49-r26 opomba (nezakonska Notar-vez) + s50-r41 mrtvorojen (brez podpisa).
Izhod: /tmp/p160/cells/ (sheeti + super-zoomi)."""
from PIL import Image, ImageDraw
import numpy as np, os

OUT = "/tmp/p160/cells"
os.makedirs(OUT, exist_ok=True)

# y-centri vrstic (detekcija + interpolacija ±10)
YC = {
    ("s48", 14): 531, ("s48", 22): 1627, ("s48", 24): 1890,
    ("s49", 30): 1085, ("s49", 26): 535,
    ("s50", 37): 400, ("s50", 38): 538, ("s50", 41): 945,
}
GRIBLJE = [("s48", 14), ("s48", 22), ("s48", 24), ("s49", 30), ("s50", 37), ("s50", 38)]

IM = {}
for s in ("s47", "s48", "s49", "s50", "s51"):
    im = Image.open(f"/tmp/p160/{s}.jpg")
    IM[s] = (im, im.size[0], im.size[1])


def cell(s, yc, x0f, x1f, f, half=64, label=""):
    im, w, h = IM[s]
    crop = im.crop((int(w * x0f), max(0, yc - half), int(w * x1f), min(h, yc + half)))
    crop = crop.resize((int(crop.width * f), int(crop.height * f)), Image.LANCZOS)
    return crop, f"{s}-r{yc}"


def sheet(name, items, tw=2400):
    """items = [(crop, label)]; složi vertikalno z zabeležkami, max širine tw"""
    tiles = []
    for crop, lab in items:
        f = min(1.0, (tw - 90) / crop.width)
        if f < 1.0:
            crop = crop.resize((int(crop.width * f), int(crop.height * f)), Image.LANCZOS)
        tile = Image.new("RGB", (crop.width + 90, crop.height), (255, 250, 220))
        tile.paste(crop, (90, 0))
        d = ImageDraw.Draw(tile)
        d.text((5, 10), lab, fill=(180, 0, 0))
        tiles.append(tile)
    W = max(t.width for t in tiles)
    H = sum(t.height for t in tiles) + 4 * (len(tiles) - 1)
    sh = Image.new("RGB", (W, H), (255, 255, 255))
    y = 0
    for t in tiles:
        sh.paste(t, (0, y))
        y += t.height + 4
    sh.save(f"{OUT}/{name}.png")
    print(f"{name}: {len(items)} celic {W}x{H}")


# --- A: vas + hišna + ime (x 0.20–0.50, @3.2×) — 2 sheeta po 3
items = [cell(s, yc, 0.20, 0.50, 3.2, label=f"{s}-r{zap}")
         for (s, zap), yc in YC.items() if (s, zap) in GRIBLJE]
items = [(c, l) for c, l in items]
for k in range(0, len(items), 3):
    sheet(f"p160-A-L-{k//3+1}", items[k:k+3])

# --- B: starost (x 0.54–0.66 @6×) — γ-7 forenzika
items = [cell(s, yc, 0.54, 0.66, 6.0, label=f"{s}-r{zap}")
         for (s, zap), yc in YC.items() if (s, zap) in GRIBLJE]
for k in range(0, len(items), 3):
    sheet(f"p160-B-starost-{k//3+1}", items[k:k+3])

# --- C: vzrok (x 0.64–0.79 @3.2×)
items = [cell(s, yc, 0.64, 0.79, 3.2, label=f"{s}-r{zap}")
         for (s, zap), yc in YC.items() if (s, zap) in GRIBLJE]
for k in range(0, len(items), 3):
    sheet(f"p160-C-vzrok-{k//3+1}", items[k:k+3])

# --- D: podpis (x 0.82–0.95 @3.2×)
items = [cell(s, yc, 0.82, 0.95, 3.2, label=f"{s}-r{zap}")
         for (s, zap), yc in YC.items() if (s, zap) in GRIBLJE]
for k in range(0, len(items), 3):
    sheet(f"p160-D-podpis-{k//3+1}", items[k:k+3])

# --- super-zoom: s48-r14 ime (Terdičec-glyph) + starost (82/62)
c, l = cell("s48", YC[("s48", 14)], 0.315, 0.50, 6.0, label="s48-r14-ime")
sheet("p160-S-r14-ime", [(c, l)])
c, l = cell("s48", YC[("s48", 14)], 0.545, 0.645, 8.0, label="s48-r14-starost")
sheet("p160-S-r14-starost", [(c, l)])

# --- s49-r26: opomba (x 0.89–1.00 @4×)
c, l = cell("s49", YC[("s49", 26)], 0.89, 1.00, 4.0, label="s49-r26-opomba")
sheet("p160-S-r26-opomba", [(c, l)])

# --- s50-r41 mrtvorojen: vas+hišna+ime + vzrok
c, l = cell("s50", YC[("s50", 41)], 0.20, 0.50, 3.2, label="s50-r41-L")
c2, l2 = cell("s50", YC[("s50", 41)], 0.54, 0.79, 3.2, label="s50-r41-R")
sheet("p160-S-r41-mrtvorojen", [(c, l), (c2, l2)])

print("P160 CELLS ✓")
