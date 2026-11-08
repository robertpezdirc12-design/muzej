#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P176 forenzika — crops (ime-traki ×2.2, celice ×3.0).
Y-pasi: band k = 330+135*(k-1) … 330+135*k (P172–P175 recept).
s126 = z1–12 · s127 = z13–24 · s128 = z25–36 · s129 = z37–48 · s130 = z49–54 (1910) + z1–5 (1911)."""
from PIL import Image
import os

OUT = "/tmp/p176/crops"
os.makedirs(OUT, exist_ok=True)

def band(k):
    return (330 + 135 * (k - 1), 330 + 135 * k)

def crop(scan, x0, x1, y0, y1, zoom, name):
    im = Image.open(f"/tmp/p176/s{scan}.jpg")
    c = im.crop((x0, max(0, y0 - 6), x1, y1 + 6))
    c = c.resize((int((x1 - x0) * zoom), int((y1 - y0 + 12) * zoom)), Image.LANCZOS)
    c.save(f"{OUT}/{name}.jpg", quality=93)
    return name

jobs = []
# --- IME-TRAKI ×2.2 (vas+hisa+ime) za 12 GRIBLJE ---
for scan, k, zap in [(126, 3, 3), (126, 9, 9), (126, 10, 10),
                     (127, 1, 13), (127, 11, 23),
                     (129, 2, 38), (129, 4, 40), (129, 5, 41), (129, 9, 45), (129, 10, 46),
                     (130, 3, 51), (130, 5, 53)]:
    y0, y1 = band(k)
    jobs.append(crop(scan, 640, 1290, y0, y1, 2.2, f"ime_z{zap}"))

# --- CELICE ×3.0 ---
# z3: bolezen 'Mrtvo najden'? (lead 'Mrko-najden')
jobs.append(crop(126, 1720, 2160, *band(3), 3.0, "cel_z3_bolezen"))
# z9: starost 86 ali 66? (lead 66!)
jobs.append(crop(126, 1500, 1800, *band(9), 3.0, "cel_z9_starost"))
# z10: ime 'Matija Vambič'? (lead 'Marija-Hanžič?')
jobs.append(crop(126, 1150, 1560, *band(10), 3.0, "cel_z10_ime"))
# z13: hiša h7 ali h4? + starost 70 ali 40? (lead Vötter-h4-40!)
jobs.append(crop(127, 760, 900, *band(1), 3.0, "cel_z13_hisa"))
jobs.append(crop(127, 1500, 1800, *band(1), 3.0, "cel_z13_starost"))
# z38: mesec 24.[~] — September? (kontekst z37-15.Sep / z39-6.Okt)
jobs.append(crop(129, 100, 380, *band(2), 3.0, "cel_z38_datum"))
# z40: hiša h90? (novost — korpus!)
jobs.append(crop(129, 760, 900, *band(4), 3.0, "cel_z40_hisa"))
# z41: ime 'Huc' ali 'Muc'? (h91 = MUC-vez!) + hiša h91
jobs.append(crop(129, 1150, 1560, *band(5), 3.0, "cel_z41_ime"))
jobs.append(crop(129, 760, 900, *band(5), 3.0, "cel_z41_hisa"))
# z45: hiša h6? (mati+sin-dvojica)
jobs.append(crop(129, 760, 900, *band(9), 3.0, "cel_z45_hisa"))
# z51: starost '1/4 ure'! + hiša h16
jobs.append(crop(130, 1500, 1800, *band(3), 3.0, "cel_z51_starost"))
jobs.append(crop(130, 760, 900, *band(3), 3.0, "cel_z51_hisa"))
# z53: ime 'Štrancar'? stan 'hospiter'?
jobs.append(crop(130, 1150, 1560, *band(5), 3.0, "cel_z53_ime"))
# --- PODPISI ×3.0 (nov-duhovnik-check) ---
jobs.append(crop(129, 2020, 2470, *band(9), 3.0, "pod_z45_JosPavic"))
jobs.append(crop(126, 2020, 2470, *band(12), 3.0, "pod_z12_JosPunc_z"))

print(f"crops: {len(jobs)} datotek -> {OUT}")
