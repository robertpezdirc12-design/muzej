#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P175 forenzika — crops (ime-traki ×2.2, celice ×3.0).
Y-pasi: band k = 330+135*(k-1) … 330+135*k (P172–P174 recept)."""
from PIL import Image
import os

OUT = "/tmp/p175/crops"
os.makedirs(OUT, exist_ok=True)

def band(k):
    return (330 + 135 * (k - 1), 330 + 135 * k)

def crop(scan, x0, x1, y0, y1, zoom, name):
    im = Image.open(f"/tmp/p175/s{scan}.jpg")
    c = im.crop((x0, max(0, y0 - 6), x1, y1 + 6))
    c = c.resize((int((x1 - x0) * zoom), int((y1 - y0 + 12) * zoom)), Image.LANCZOS)
    c.save(f"{OUT}/{name}.jpg", quality=93)
    return name

jobs = []
# --- IME-TRAKI ×2.2 (vas+hisa+ime) za 11 GRIBLJE ---
for scan, k, zap in [(122, 1, 11), (122, 6, 16), (122, 7, 17), (122, 11, 21), (122, 12, 22),
                     (123, 3, 25), (123, 10, 32), (124, 10, 44), (125, 3, 49), (125, 4, 50), (125, 6, 52)]:
    y0, y1 = band(k)
    jobs.append(crop(scan, 640, 1290, y0, y1, 2.2, f"ime_z{zap}"))

# --- CELICE ×3.0 ---
jobs.append(crop(122, 1500, 1800, *band(7), 3.0, "cel_z17_starost"))   # 64 ali 84?
jobs.append(crop(122, 760, 900, *band(7), 3.0, "cel_z17_hisa"))        # 43?
jobs.append(crop(125, 1500, 1800, *band(3), 3.0, "cel_z49_starost"))   # 76 ali 70?
jobs.append(crop(125, 640, 900, *band(6), 3.0, "cel_z52_hisa"))        # 26 ali 86?
jobs.append(crop(125, 1500, 1800, *band(9), 3.0, "cel_z55_starost"))   # 58 ali 50?
# --- ANOMALIJE ---
jobs.append(crop(121, 640, 1290, *band(5), 2.2, "ano_z3_ime"))         # Stublar 92 + ožiglar?
jobs.append(crop(121, 1500, 1800, *band(5), 3.0, "ano_z3_starost"))    # 92 = izenačenje rekorda!
jobs.append(crop(121, 1720, 2160, *band(8), 3.0, "ano_z6_bolezen"))    # 'Mrkvud'?
jobs.append(crop(121, 640, 2160, *band(9), 1.6, "ano_z7_vrsta"))       # mrtvorojen + ——
jobs.append(crop(121, 100, 380, *band(12), 3.0, "ano_z10_smrt"))       # 22/24 izbrisana?
jobs.append(crop(124, 640, 2160, *band(11), 1.6, "ano_z45_vrsta"))     # mrtvorojen VLM-izpuščena!
jobs.append(crop(123, 640, 1290, *band(5), 2.2, "ano_z27_ime"))        # Marija MUC h17!
jobs.append(crop(123, 1500, 1800, *band(4), 3.0, "ano_z26_starost"))   # PRAZNA?
# --- PODPISI ×3.0 ---
jobs.append(crop(125, 2020, 2470, *band(2), 3.0, "pod_Lausin_Bitmar")) # s125-z48
jobs.append(crop(123, 2020, 2470, *band(2), 3.0, "pod_Jos_Pauc_z24"))  # s123-z24 + ž.
jobs.append(crop(121, 2020, 2470, *band(3), 3.0, "pod_Cerar_mg_z1"))   # s121-z1 'm.g.'
jobs.append(crop(124, 2020, 2470, *band(3), 3.0, "pod_Jos_Bucij_z37")) # s124-z37 'Bucij'?
jobs.append(crop(122, 2020, 2470, *band(1), 3.0, "pod_z11"))           # z11 podpis
jobs.append(crop(126, 2020, 2470, *band(3), 3.0, "pod_LB_z3_1910"))    # s126 P176-lead

print(f"crops: {len(jobs)} datotek -> {OUT}")
for j in jobs:
    print(" ", j)
