#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P165 — forenzični izrezi mrliške 04894, leto 1899 (skeni 70–77).
Trakovi ×2.2 (celotne vrstice) + celice ×3.0 (targetirane po Griblje/
meji/mesecih-KAOS/duhovnikih). Izhod: /tmp/p165/crops/*.png
TARGETI (diag-agent-oči + VLM-spori):
  s70: '1899.'-INLINE-meja + zap1-starost (65|68?) + zap7-mesec (Marec?) +
       zap10 Griblje-h20 trak (starost '1 4to'?) + zap11-mesec (Marci 4/6
       PO Mar 26/28 — kronologija?)
  s71: zap12-mesec (Marci 18 po Apr?) + zap13 Griblje-h22-Milek (VLM '91'!)
       + zap17 hišna (21|91?) + zap18 h8 + zap20 h60 + zap21 h65 +
       podpis 'F.Škurmig' (Škurmelj?)
  s72: zap24-mesec (VLM 'Januarj' — Junij?) + zap27-mesec ('Julij') +
       zap29 'je vstrelil' + opomba + zap30/31 pokop ('1.avg') +
       zap32-mesec ('Avgust') + zap33 Griblje-h24 + zap35 (Žugec 34?)
  s73: zap37 (Sep 3|13?) + zap40 Griblje-h28 + zap42 h34 + zap47 h32
       ('Hravc'?) + zap41 podpis 'Jos.Perz coop' (NOVI duhovnik #9?)
  s74: zap49 Griblje-h11 (Zumič) + zap55 h12 (Božjast|Krastelj?) +
       zap57 h33 + zap58 mrtvorojen-brez-podpisa (r53-#14)
  s75: '1900'-DVOJNI-podčrtaj-meja + zap60 mrtvorojena (r53-#15) +
       zap8-1900 Griblje-h32-Marija-URH (P166-lead!)"""
from PIL import Image
import os

OUT = "/tmp/p165/crops"
os.makedirs(OUT, exist_ok=True)

# (ime, sken, x0, y0, x1, y1, zoom)
CROPS = [
    # --- s70: meja-INLINE + starost + meseci + Griblje zap10 ---
    ("s70-meja-INLINE", 70, 100, 130, 900, 420, 2.2),
    ("s70-zap1-starost", 70, 1550, 130, 1860, 420, 3.0),
    ("s70-zap7-mesec", 70, 130, 990, 520, 1180, 3.0),
    ("s70-zap10-trak", 70, 100, 1690, 2450, 1915, 2.2),
    ("s70-zap11-mesec", 70, 130, 1870, 520, 2000, 3.0),
    # --- s71: mesec-zap12 + Griblje zap13/17/18/20/21 + podpis ---
    ("s71-zap12-mesec", 71, 130, 140, 520, 330, 3.0),
    ("s71-zap13-vas-hisna", 71, 520, 290, 900, 470, 3.0),
    ("s71-zap13-ime", 71, 860, 290, 1360, 470, 3.0),
    ("s71-zap13-starost-bolezen", 71, 1550, 290, 2100, 470, 3.0),
    ("s71-zap13-podpis", 71, 2080, 290, 2450, 470, 3.0),
    ("s71-zap17-vas-hisna", 71, 520, 810, 900, 990, 3.0),
    ("s71-zap17-ime-bolezen", 71, 860, 810, 2100, 990, 2.6),
    ("s71-zap18-vas-hisna", 71, 520, 975, 900, 1155, 3.0),
    ("s71-zap18-ime", 71, 860, 975, 1360, 1155, 3.0),
    ("s71-zap20-vas-hisna", 71, 520, 1370, 900, 1550, 3.0),
    ("s71-zap20-ime", 71, 860, 1370, 1360, 1550, 3.0),
    ("s71-zap21-vas-hisna", 71, 520, 1515, 900, 1695, 3.0),
    ("s71-zap21-ime-starost", 71, 860, 1515, 1860, 1695, 2.6),
    # --- s72: meseci-KAOS + suicid + Griblje zap24/33 + zap35 ---
    ("s72-zap24-mesec-vas", 72, 130, 225, 900, 405, 2.6),
    ("s72-zap24-ime", 72, 860, 225, 1360, 405, 3.0),
    ("s72-zap27-mesec", 72, 130, 730, 520, 910, 3.0),
    ("s72-zap29-bolezen-opomba", 72, 1770, 1000, 2560, 1180, 2.6),
    ("s72-zap30-31-pokop", 72, 320, 1110, 520, 1420, 3.0),
    ("s72-zap32-mesec", 72, 130, 1375, 520, 1560, 3.0),
    ("s72-zap33-vas-hisna", 72, 520, 1525, 900, 1700, 3.0),
    ("s72-zap33-ime-bolezen", 72, 860, 1525, 2100, 1700, 2.6),
    ("s72-zap35-vas-hisna-starost", 72, 520, 1850, 1860, 2000, 2.6),
    # --- s73: Griblje zap40/42/47 + Sep-zap37 + podpis Perz ---
    ("s73-zap37-mesec", 73, 130, 440, 520, 620, 3.0),
    ("s73-zap40-vas-hisna", 73, 520, 855, 900, 1035, 3.0),
    ("s73-zap40-ime", 73, 860, 855, 1360, 1035, 3.0),
    ("s73-zap42-vas-hisna", 73, 520, 1130, 900, 1315, 3.0),
    ("s73-zap42-ime-bolezen", 73, 860, 1130, 2100, 1315, 2.6),
    ("s73-zap47-vas-hisna", 73, 520, 1885, 900, 2000, 3.0),
    ("s73-zap47-ime-bolezen", 73, 860, 1885, 2100, 2000, 2.6),
    ("s73-zap41-podpis", 73, 2080, 990, 2450, 1170, 3.0),
    # --- s74: Griblje zap49/55/57 + mrtvorojen zap58 ---
    ("s74-zap49-vas-hisna-ime", 74, 520, 280, 1360, 620, 2.6),
    ("s74-zap55-vas-hisna-ime", 74, 520, 1060, 1360, 1300, 2.6),
    ("s74-zap55-bolezen", 74, 1770, 1060, 2100, 1300, 3.0),
    ("s74-zap57-vas-hisna-ime", 74, 520, 1500, 1360, 1720, 2.6),
    ("s74-zap58-trak", 74, 100, 1660, 2450, 1860, 2.2),
    # --- s75: meja-'1900' + zap60 mrtvorojena + zap8-1900-Urh ---
    ("s75-meja-1900", 75, 100, 640, 900, 1050, 2.2),
    ("s75-zap60-trak", 75, 100, 230, 2450, 500, 2.2),
    ("s75-zap8-1900-vas-hisna", 75, 520, 1770, 900, 2000, 3.0),
    ("s75-zap8-1900-ime", 75, 860, 1770, 1360, 2000, 3.0),
]


def main():
    ok = 0
    for (name, scan, x0, y0, x1, y1, zoom) in CROPS:
        im = Image.open(f"/tmp/p165/s{scan:02d}.jpg")
        crop = im.crop((x0, y0, x1, y1))
        crop = crop.resize((int(crop.width * zoom), int(crop.height * zoom)),
                           Image.LANCZOS)
        dst = f"{OUT}/{name}.png"
        crop.save(dst)
        ok += 1
        print(f"{name}: {crop.size} ✓")
    print(f"crops: {ok}/{len(CROPS)}")


if __name__ == "__main__":
    main()
