#!/usr/bin/env python3
"""P256 — duel-izrezi (×5): hišne celice korpusnih vrstic + datumskie celice."""
from PIL import Image
import os
OUT = '/tmp/p256/D'
os.makedirs(OUT, exist_ok=True)

# (ime, scan, x0, x1, y0, y1)
GH = (150, 285)   # vas+hiša ženina
BH = (555, 790)   # vas+hiša neveste (z ženinovim imenom v ozadju)
DT = (35, 255)    # datumski celici (široka: letnica+dan+mesec)

JOBS = [
    # hišni dueli — korpusne vrstice 1829
    ('s4r2_gh', 's4', GH, 360, 530), ('s4r2_bh', 's4', BH, 360, 530),
    ('s5r1_gh', 's5', GH, 230, 380), ('s5r1_bh', 's5', BH, 230, 380),
    ('s6r1_gh', 's6', GH, 295, 415), ('s6r1_bh', 's6', BH, 295, 415),
    # datumski dueli — spodnje vrstice s4 (17? 9to? Febr?)
    ('s4r6_dt', 's4', DT, 845, 985), ('s4r7_dt', 's4', DT, 950, 1090),
    ('s4r8_dt', 's4', DT, 1065, 1205), ('s4r9_dt', 's4', DT, 1180, 1330),
    # s5 vrstice 1–2 (11? 14? 27?)
    ('s5r1_dt', 's5', DT, 230, 380), ('s5r2_dt', 's5', DT, 355, 505),
    # s6 vrstica 1 (März 1 ali 15?) + meja 1830 (r4)
    ('s6r1_dt', 's6', DT, 295, 415), ('s6r4_dt', 's6', DT, 590, 720),
    # s4 r6 semel-hisa (13?) + s5 r3 hiši (10? 15?)
    ('s4r6_gh', 's4', GH, 845, 985), ('s5r3_gh', 's5', GH, 480, 640), ('s5r3_bh', 's5', BH, 480, 640),
]
for name, tag, (x0, x1), y0, y1 in JOBS:
    im = Image.open(f'/tmp/p256/{tag}.jpg')
    W, H = im.size
    c = im.crop((x0, y0, min(x1, W), min(y1, H)))
    c = c.resize((c.width*5, c.height*5), Image.LANCZOS)
    c.save(f'{OUT}/{name}.jpg', quality=92)
    print(name, c.size)
