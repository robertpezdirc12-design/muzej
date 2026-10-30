#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P163 — max-zoom izrezi spornih celic (agent-oči forenzika, max-zoom > VLM).
Izhod: /tmp/p163/cells/*.png (širina ≤1568 px — Read prikaže 1:1!)."""
from PIL import Image
import os

OUT = "/tmp/p163/cells"
os.makedirs(OUT, exist_ok=True)

# (skan, ime, x0f, x1f, y0, y1, zoom) — y-vrednosti iz diag-agent-oči (h=2000)
CELLS = [
    # A. s61-zap5 — Ana Urh?/Mlh? roj. Novosel h51 61 (URH-TRILOGIJA #3!)
    (61, "s61-zap5-L", 0.03, 0.62, 585, 725, 1.6),
    (61, "s61-zap5-R", 0.55, 0.98, 585, 725, 1.6),
    # B. s61-zap11 — Jurij Perdivec/Pezdirc? h42 52 (PEZDIREC-leksikon!)
    (61, "s61-zap11-L", 0.03, 0.62, 1375, 1515, 1.6),
    (61, "s61-zap11-R", 0.55, 0.98, 1375, 1515, 1.6),
    # C. s61-zap14 — Ana Hlebec/Vrobeč? h2 33/53? (γ-3-dvom!)
    (61, "s61-zap14-L", 0.03, 0.62, 1775, 1915, 1.6),
    (61, "s61-zap14-R", 0.55, 0.98, 1775, 1915, 1.6),
    # D. s62-zap16 — Peter Hlebec h2 1 mes (Griblje-potrditev)
    (62, "s62-zap16-L", 0.03, 0.62, 445, 585, 1.6),
    # E. s62-zap21 — Janez Brinec h26 7 let (BRINEC-mreža!)
    (62, "s62-zap21-L", 0.03, 0.62, 1105, 1245, 1.6),
    # F. s62-zap25 — Ana Šimec h54 35 let (starost+vzrok)
    (62, "s62-zap25-L", 0.03, 0.62, 1720, 1860, 1.6),
    (62, "s62-zap25-R", 0.55, 0.98, 1720, 1860, 1.6),
    # G. s62-zap26 — Matijo/Marlo Perdinec/Pezdirc h87 3 mes (ime+stan!)
    (62, "s62-zap26-L", 0.03, 0.62, 1855, 1995, 1.6),
    (62, "s62-zap26-R", 0.55, 0.98, 1855, 1995, 1.6),
    # H+I+J. s63 zap33/34/35 — Griblje VLM-MISS ×3!
    (63, "s63-zap33-L", 0.03, 0.62, 1175, 1315, 1.6),
    (63, "s63-zap34-L", 0.03, 0.62, 1305, 1445, 1.6),
    (63, "s63-zap35-L", 0.03, 0.62, 1435, 1575, 1.6),
    (63, "s63-zap35-R", 0.55, 0.98, 1435, 1575, 1.6),
    # K. s63-zap37 — N. Jakofčič mrtvorojena (r53-vzorec #11 — BREZ imena?)
    (63, "s63-zap37-L", 0.03, 0.62, 1705, 1845, 1.6),
    # L. s64-zap42 — Barbara Padriec/Perdinec? h83/53? 8 mes (ime+hišna!)
    (64, "s64-zap42-L", 0.03, 0.62, 695, 835, 1.6),
    (64, "s64-zap42-R", 0.55, 0.98, 695, 835, 1.6),
    # M. s64-zap45 — Jože Drinovec h14 4 mes (Griblje-potrditev)
    (64, "s64-zap45-L", 0.03, 0.62, 1185, 1325, 1.6),
    # N. s64-glava — 'Leto 1897' prečrtano→1898? (A-scribal anomalija?)
    (64, "s64-glava", 0.03, 0.30, 215, 325, 2.4),
    # O. s65-zap52 — Janez Botek h14 6 tednov (VLM-miss ime!)
    (65, "s65-zap52-L", 0.03, 0.62, 450, 590, 1.6),
    (65, "s65-zap52-R", 0.55, 0.98, 450, 590, 1.6),
    # P. s65-marker '1898.' (meja 1897/98 — 5. STIL 5. POTRDITEV!)
    (65, "s65-marker-1898", 0.03, 0.30, 1385, 1535, 2.4),
]

for scan, name, x0f, x1f, y0, y1, z in CELLS:
    im = Image.open(f"/tmp/p163/s{scan:02d}.jpg")
    w, h = im.size
    crop = im.crop((int(w * x0f), y0, int(w * x1f), y1))
    crop = crop.resize((int(crop.width * z), int(crop.height * z)), Image.LANCZOS)
    p = f"{OUT}/{name}.png"
    crop.save(p)
    print(f"{name}: {crop.size}")
print("OK")
