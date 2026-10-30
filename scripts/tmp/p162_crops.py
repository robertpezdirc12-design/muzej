#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P162 — max-zoom izrezi spornih celic (agent-oči forenzika, max-zoom > VLM).
Izhod: /tmp/p162/cells/*.png (širina ≤1568 px — Read prikaže 1:1!)."""
from PIL import Image
import os

OUT = "/tmp/p162/cells"
os.makedirs(OUT, exist_ok=True)

# (skan, ime, x0f, x1f, y0, y1, zoom) — y-vrednosti iz diag-agent-oči (h=2000)
CELLS = [
    # A. s55-zap4 — Ana B.? roj. Brinec? h58 (LEVO: datum+vas+hišna+ime; DESNO: starost+vzrok+podpis)
    (55, "s55-zap4-L", 0.03, 0.62, 1810, 1960, 1.6),
    (55, "s55-zap4-R", 0.55, 1.00, 1810, 1960, 1.6),
    # L. s55-marker "1896." (5. STIL 3. potrditev)
    (55, "s55-marker-1896", 0.03, 0.30, 1330, 1480, 2.4),
    # B. s56-zap8 — N. Brinec mrtvorojen h14 (LEVO)
    (56, "s56-zap8-L", 0.03, 0.62, 715, 835, 1.6),
    # C. s56-zap10 — Barbara Strauš ožena Zavrtovč h45 (ime+stan)
    (56, "s56-zap10-L", 0.03, 0.62, 955, 1090, 1.6),
    # D+E. s57 zap20 + zap23 — Podrivec/Pezdirc imena (LEVO vsak)
    (57, "s57-zap20-L", 0.03, 0.62, 725, 865, 1.6),
    (57, "s57-zap23-L", 0.03, 0.62, 1115, 1255, 1.6),
    # F. s58-zap33 — h60 vs h61 (vas+hišna)
    (58, "s58-zap33-vas", 0.13, 0.36, 870, 1010, 2.2),
    # G. s58-zap40 — Hvalešič 56/36 (ime+starost+vzrok)
    (58, "s58-zap40-L", 0.03, 0.62, 1825, 1975, 1.6),
    (58, "s58-zap40-R", 0.55, 0.95, 1825, 1975, 1.6),
    # H. s59-zap43 — Štabijar/kπapπ h46 (LEVO)
    (59, "s59-zap43-L", 0.03, 0.62, 610, 745, 1.6),
    # I. s59-zap50 — Marjeta Mušič? Bule? h41 (LEVO + starost+vzrok)
    (59, "s59-zap50-L", 0.03, 0.62, 1590, 1735, 1.6),
    (59, "s59-zap50-R", 0.55, 0.95, 1590, 1735, 1.6),
    # J. s60-zap54 — Joana Papič h31 (LEVO)
    (60, "s60-zap54-L", 0.03, 0.62, 480, 615, 1.6),
    # K. s60-marker "1897." (meja 1896/97 — 5. STIL 4. potrditev!)
    (60, "s60-marker-1897", 0.03, 0.30, 1440, 1600, 2.4),
    # M+N. s61 zap4 + zap5 (1897-lead)
    (61, "s61-zap4-L", 0.03, 0.62, 455, 600, 1.6),
    (61, "s61-zap5-L", 0.03, 0.62, 595, 730, 1.6),
]

for scan, name, x0f, x1f, y0, y1, z in CELLS:
    im = Image.open(f"/tmp/p162/s{scan:02d}.jpg")
    w, h = im.size
    crop = im.crop((int(w * x0f), y0, int(w * x1f), y1))
    crop = crop.resize((int(crop.width * z), int(crop.height * z)), Image.LANCZOS)
    p = f"{OUT}/{name}.png"
    crop.save(p)
    print(f"{name}: {crop.size}")
print("OK")
