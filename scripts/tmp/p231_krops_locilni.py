#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P231 — ločilni-krops (×2.4): kritične Griblje-vrstice + DUELI (hisna/imesa/datumi/meja!)."""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p231"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception:
    FONT = ImageFont.load_default()

# (label, scan, x0, x1, y0, y1)  — frakcije
L = (0.075, 0.56)   # datumi+vas+hisna+ime
R = (0.50, 0.995)   # starši+botra+duhovnik
F = (0.075, 0.995)  # polno
HIS = (0.24, 0.36)  # hisna-stolpec

def rowy(scan, r, n, pad=0.010):
    y_a = 0.13 + (r - 1) * (0.88 - 0.13) / n - pad
    y_b = 0.13 + r * (0.88 - 0.13) / n + pad
    return max(0.0, y_a), min(1.0, y_b)

# vrstic-na-sken
N = {47: 8, 48: 9, 49: 8, 50: 9, 52: 9, 53: 9, 54: 9, 59: 8, 63: 8, 64: 4}

ITEMS = {
 "X1": [
  ("s48-r1 LEVO (13/13!-hisna-48/18-DUEL!-Mathias)", 48, L, 1),
  ("s48-r1 DESNO (stari-dvoumni!)", 48, R, 1),
  ("s48-r1 HISNA-zoom", 48, HIS, 1),
  ("s49-r2 LEVO (Feber?-7/8-Griblje-h34-Catharina)", 49, L, 2),
  ("s49-r2 DESNO (Felah/Dehlic!)", 49, R, 2),
  ("s49-r3 LEVO (Feber-11/12-h37-Michael)", 49, L, 3),
  ("s49-r3 DESNO (Husic/Hambic!)", 49, R, 3),
  ("s49-r4 LEVO (Feber-12/12-h94/37?-Maria)", 49, L, 4),
  ("s49-r4 DESNO (Hambic/Princ + Milek-botra!)", 49, R, 4),
  ("s50-r9 POLNO (Griblje-h33-Johann-stari?!-März-24)", 50, F, 9),
 ],
 "X2": [
  ("s52-r6 LEVO (Mai-22/23-Griblje-h64/6?-Katharina)", 52, L, 6),
  ("s52-r6 DESNO (Verbicar?+Anna-PEZDIRC!)", 52, R, 6),
  ("s53-r4 LEVO (Juni-14/15-Griblje-h72/42?-Johann)", 53, L, 4),
  ("s53-r4 DESNO (Stranc/Dragos!)", 53, R, 4),
  ("s54-r1 LEVO (Juni23-vs-Juli22-DUEL!-Griblje-h38-Margareth)", 54, L, 1),
  ("s54-r1 DESNO (Klinec/Krizan-vs-SIMEC/HRIŽAN-DUEL!)", 54, R, 1),
  ("s54-r3 POLNO (Griblje-h57-Johann-28/28?)", 54, F, 3),
  ("s54-r4 POLNO (Griblje-h57-DUP?-29/29?)", 54, F, 4),
 ],
 "X3": [
  ("s59-r1 LEVO (Oct-18/18-Griblje-h48-Katarina!)", 59, L, 1),
  ("s59-r1 DESNO (Klobucar+Podirec/PEZDIRC!-†28.11.1940!)", 59, R, 1),
  ("s59-r6 LEVO (Oct-28/28-Griblje-h68-Nikolaus)", 59, L, 6),
  ("s59-r6 DESNO (Urh/Cozek!)", 59, R, 6),
  ("s63-r6 LEVO (Nov-26/26-Griblje-h1-Josef)", 63, L, 6),
  ("s63-r6 DESNO (Kelcic/Jarofic-vs-Stefko/Jakofcic-DUEL!)", 63, R, 6),
  ("s64-r4 LEVO (Dez-14-vs-18-DUEL!-Gradac-h55)", 64, L, 4),
  ("s48-r8+9 PRELOM (Feber-1-veliki!+Gradac-Anton)", 48, F, 9),
 ],
}

def crop(scan, xr, yr, scale=2.4):
    im = Image.open(f"{T}/s{scan}.jpg")
    W, H = im.size
    px = (int(xr[0] * W), int(yr[0] * H), int(xr[1] * W), int(yr[1] * H))
    c = im.crop(px)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    return c

for name, items in ITEMS.items():
    imgs = []
    for label, scan, xr, r in items:
        if len(xr) == 4:
            yr = (xr[2], xr[3])
            xr = (xr[0], xr[1])
        else:
            yr = rowy(scan, r, N[scan])
        c = crop(scan, xr, yr)
        lab = Image.new("RGB", (c.width, 30), (20, 20, 20))
        d = ImageDraw.Draw(lab)
        d.text((8, 3), label, fill=(255, 220, 120), font=FONT)
        imgs += [lab, c, Image.new("RGB", (c.width, 8), (255, 255, 255))]
    W = max(i.width for i in imgs)
    H = sum(i.height for i in imgs)
    out = Image.new("RGB", (W, H), (240, 240, 240))
    y = 0
    for i in imgs:
        out.paste(i, (0, y)); y += i.height
    out.save(f"{OUT}/sheet-{name}.png")
    print(f"sheet-{name}: {W}x{H} ({len(items)})")

print("LOCILNI-KROPS-GOTOVI")
