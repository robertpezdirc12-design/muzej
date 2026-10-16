#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P85 — paketni izrezi statusnih celic (½ vs ¼ forenzika)."""
from PIL import Image, ImageOps

JOBS = [
    # (scan, x0, y0, x1, y1, out)
    (44, 920, 1000, 1270, 1100, 'st-r22'),   # r22 oče Janez Pošek
    (44, 920, 1095, 1270, 1195, 'st-r23'),   # r23 oče Jurij Straus
    (45, 920, 700, 1270, 810, 'st-r31'),     # r31 oče Janez Pošek
    (47, 920, 1000, 1270, 1100, 'st-r61'),   # r61 oče Janez Brinec
    (48, 920, 440, 1270, 545, 'st-r67'),     # r67 oče Matija Urh
    (48, 920, 940, 1270, 1040, 'st-r72'),    # r72 oče Matija Hrušič
    (48, 920, 1230, 1270, 1330, 'st-r75'),   # r75 oče Janez Tomc
    (48, 920, 1305, 1270, 1400, 'st-r76'),   # r76 oče Nikolaj Križan
    (49, 920, 915, 1270, 1025, 'st-r85'),    # r85 oče-stolpec Marija Hrižan
    (44, 920, 455, 1270, 560, 'st-r15'),     # r15 oče Peter Klobučar
    (46, 920, 500, 1270, 660, 'st-r42'),     # r42 oče Miha Lozar čevljar
    (46, 920, 940, 1270, 1045, 'st-r47'),    # r47 oče Jurij Pošek bajtar
    (46, 920, 1300, 1270, 1400, 'st-r51'),   # r51 oče Janez Milek
    (47, 920, 300, 1270, 415, 'st-r54'),     # r54 oče Miha Požek mežnar
    (48, 920, 345, 1270, 450, 'st-r66'),     # r66 oče Nikolaj Šimec
    (48, 920, 540, 1270, 645, 'st-r68'),     # r68 oče Matija Zumik
    (48, 920, 845, 1270, 950, 'st-r71'),     # r71 oče Janez Muc bajtar
    (49, 920, 385, 1270, 495, 'st-r79'),     # r79 oče Franc Kopitar učitelj
    (44, 920, 760, 1270, 860, 'st-r19b'),    # r19 oče-stolpec (ponovno širše)
    (43, 920, 700, 1270, 840, 'st-r6b'),     # r6 (ponovno širše)
    (44, 920, 350, 1270, 465, 'st-r14b'),    # r14 (ponovno širše)
    (46, 920, 760, 1270, 880, 'st-r44b'),    # r44 (ponovno širše)
]
for scan, x0, y0, x1, y1, out in JOBS:
    im = Image.open(f'/tmp/p85/scan-{scan:02d}.jpg').convert('L')
    C = im.crop((x0, y0, x1, y1))
    C = ImageOps.autocontrast(C, cutoff=1)
    C = C.resize((C.width * 4, C.height * 4), Image.LANCZOS)
    C.save(f'/tmp/p85/crops/{out}.jpg', quality=95)
    print(out, 'ok')
