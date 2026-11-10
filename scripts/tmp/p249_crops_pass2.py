#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P249 pass-2 — kropi ključnih duelov (iz pass-1 + Read-očesi).
Vsi kropi → /tmp/p249/crops/, upscale z LANCZOS."""
from PIL import Image
import os

D = '/tmp/p249'
O = f'{D}/crops'
os.makedirs(O, exist_ok=True)

# (ime, sken, box(x0,y0,x1,y1), zoom)
CROPS = [
    # S8 — restart-1875
    ('s8_m1_extreme', 8, (0, 95, 330, 345), 6),          # margina '21~1' + datum '1875 16 Jänner'
    ('s8_dates_a', 8, (55, 325, 265, 1020), 2.2),        # datumi vrst 2–5
    ('s8_dates_b', 8, (55, 1015, 265, 1710), 2.2),       # datumi vrst 6–7
    ('s8_row1_names', 8, (140, 95, 1250, 345), 1.7),     # v1 imena (Šolnar × Družamirić?)
    # S9 — vrste 8–12
    ('s9_r1_date_extreme', 9, (55, 95, 330, 425), 5),    # margina '8' + datum DUEL '24 Jän ~ 8 Febr'
    ('s9_r1_wohnorte', 9, (140, 95, 1250, 425), 1.9),    # v8 Wohnort duel Zemelj~Dolenja
    ('s9_r3_bride_griblje', 9, (660, 737, 1250, 1058), 2.6),  # v10 NEVESTA 'Griblje 8' + ime!
    ('s9_r3_h8_extreme', 9, (770, 770, 900, 1055), 8),   # v10 hišna št. mikro 8-vs-6
    ('s9_r5_bride_age', 9, (1020, 1379, 1260, 1700), 6), # v12 starost 17~24
    # S10 — vrste 13–17
    ('s10_r1r2_dates', 10, (55, 95, 330, 745), 2.2),     # v13+v14 datumi (obe 'Februar 8'?)
    ('s10_r3_bride_wohnort', 10, (660, 737, 920, 1058), 5),  # v15 Gradac 26~11
    ('s10_r4_bride_eltern', 10, (1460, 1045, 1740, 1390), 4.5),  # v16 starši neveste 'Anna Bezdir'!
    ('s10_r5_bride_age', 10, (1030, 1379, 1270, 1700), 6),   # v17 starost 19~22
    # S7 — tail-1874
    ('s7_r5_bride', 7, (650, 1180, 1260, 1530), 2.4),    # m32 nevesta Pegdirc + Wohnort Griblje-?
    ('s7_r5_h_extreme', 7, (770, 1210, 900, 1520), 8),   # m32 hišna št. mikro
    ('s7_finis', 7, (80, 1400, 1330, 1800), 1.7),        # finis-ornament + letnica
    # Podpisi (Unterchrift) — Dorgan~Dovgan
    ('s8_podpis_a', 8, (2200, 95, 2467, 950), 2.4),
    ('s8_podpis_b', 8, (2200, 950, 2467, 1750), 2.4),
    ('s9_podpis_a', 9, (2200, 95, 2469, 950), 2.4),
    ('s9_podpis_b', 9, (2200, 950, 2469, 1750), 2.4),
    ('s10_podpis_a', 10, (2200, 95, 2466, 950), 2.4),
    ('s10_podpis_b', 10, (2200, 950, 2466, 1750), 2.4),
]

for name, s, box, z in CROPS:
    im = Image.open(f'{D}/s{s}.jpg')
    c = im.crop(box)
    w, h = c.size
    c = c.resize((int(w * z), int(h * z)), Image.LANCZOS)
    out = f'{O}/{name}.png'
    c.save(out)
    print(f'{name}: box={box} zoom={z} → {c.size}')
print('KROPI KONČANI')
