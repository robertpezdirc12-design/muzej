#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P261 — izrezi s17 (Pag 31/32, 1836-nadaljevanje + 1836/37-restart!).
Metoda P259-PREDPIS: agent-vizija (Read tool), L+R-celotne-vrstice 1:1 + zoom ×3–5
za dvomljive dele. Izrez: levo-margina+datum+Wohnort + desno-starši/priče/duhovnik."""
from PIL import Image
import os

SRC = "research/issue17/p261-work/s17.jpg"
OUT = "/tmp/p261"
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC)
W, H = im.size  # 2139 x 1500

# --- 9 vrstic (ocena y-obsegov iz celotne strani ~1500px) ---
# vrstice pribl.: r14 ~150-255, r15 ~255-350, r16 ~350-430, r17 ~430-505,
# r18 ~505-580, r19 ~580-660, r20 ~660-745, r21 ~745-820, r22 ~820-900
rows = {
    "r14": (140, 258),
    "r15": (258, 352),
    "r16": (352, 432),
    "r17": (432, 506),
    "r18": (506, 582),
    "r19": (582, 662),
    "r20": (662, 748),
    "r21": (748, 824),
    "r22": (824, 910),
}
# levi del (margina+datum+Wohnort+ženin) do x~1070; desni del (nevesta+starši+priče) od x~1000
for name, (y0, y1) in rows.items():
    # cela vrstica L (ženin stran)
    im.crop((80, y0, 1080, y1)).resize((2000, (y1 - y0) * 2), Image.LANCZOS).save(f"{OUT}/s17_{name}_L.png")
    # cela vrstica R (nevesta + starši + priče + duhovnik)
    im.crop((1000, y0, 2100, y1)).resize((2200, (y1 - y0) * 2), Image.LANCZOS).save(f"{OUT}/s17_{name}_R.png")

# --- margina+datum stolpec (cel, ×2) ---
im.crop((80, 140, 420, 910)).resize((680, 1540), Image.LANCZOS).save(f"{OUT}/s17_margins.png")
print("izrezi:", len(os.listdir(OUT)))
