#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P164 — forenzični izrezi mrliške 04894, leto 1898 (skeni 65–72).
Trakovi ×2.2 (celotne vrstice) + celice ×3.0 (targetirane po Griblje/
meji/γ-kalibraciji). Izhod: /tmp/p164/crops/*.png
TARGETI (diag-agent-oči + VLM-spori):
  s65: meja-'1898.'-marker + zap2-starost (41|77?) + zap3-starost (43|93?)
  s66: zap4 Griblje hišna (32|52?) + ime-Pezdirec + zap10 mesec (Marec|Maj?)
       + hišna-30 + zap14 h64 Ana-Verbičar-roj.-Pezdirec
  s67: zap18 vas (Krasinec|GRIBLJE-h2? — P163-lead ×2!) + zap21 h34 Ana-Filak
  s68: zap37 h64 Matija-Verbičar (ožitek?) + zap39 mrtvorojen-brez-podpisa
  s69: zap46 h60 Ana-Žele + zap48 h22 ime (Mihel|Molk?)
  s70: zap1 '1899.'-INLINE-marker (meja 1898/99)
"""
from PIL import Image
import os

OUT = "/tmp/p164/crops"
os.makedirs(OUT, exist_ok=True)

# (ime, sken, x0, y0, x1, y1, zoom)
CROPS = [
    # --- s65: meja 1897/98 + starosti 1898-zap2/zap3 ---
    ("s65-meja-marker", 65, 100, 1380, 900, 1650, 2.2),
    ("s65-zap2-starost", 65, 1560, 1630, 1850, 1800, 3.0),
    ("s65-zap3-starost", 65, 1560, 1760, 1850, 1930, 3.0),
    ("s65-trak-1898", 65, 100, 1440, 1560, 2000, 2.2),
    # --- s66: Griblje zap4 / zap10 / zap14 ---
    ("s66-zap4-vas-hisna", 66, 520, 300, 880, 450, 3.0),
    ("s66-zap4-ime", 66, 860, 300, 1360, 450, 3.0),
    ("s66-zap10-mesec-vas", 66, 130, 1160, 880, 1330, 2.6),
    ("s66-zap10-ime-starost", 66, 860, 1160, 1830, 1330, 2.6),
    ("s66-zap14-vas-hisna", 66, 520, 1560, 880, 1720, 3.0),
    ("s66-zap14-ime", 66, 860, 1560, 1360, 1720, 3.0),
    # --- s67: zap18 vas-h2? + zap21 h34 ---
    ("s67-zap18-mesec-vas", 67, 130, 565, 880, 735, 3.0),
    ("s67-zap18-ime", 67, 860, 565, 1360, 735, 3.0),
    ("s67-zap21-vas-hisna", 67, 520, 985, 880, 1150, 3.0),
    ("s67-zap21-bolezen", 67, 1770, 985, 2080, 1150, 3.0),
    # --- s68: zap37 h64 + zap39 mrtvorojen ---
    ("s68-zap37-vas-hisna", 68, 520, 1595, 880, 1750, 3.0),
    ("s68-zap37-ime-stan", 68, 860, 1595, 1360, 1750, 3.0),
    ("s68-zap39-podpis", 68, 2100, 1830, 2560, 1990, 3.0),
    # --- s69: zap46 h60 + zap48 h22 ---
    ("s69-zap46-vas-hisna", 69, 520, 1150, 880, 1310, 3.0),
    ("s69-zap46-ime", 69, 860, 1150, 1360, 1310, 3.0),
    ("s69-zap46-starost-bolezen", 69, 1560, 1150, 2080, 1310, 3.0),
    ("s69-zap48-ime", 69, 860, 1420, 1360, 1580, 3.0),
    # --- s70: '1899.'-INLINE-marker (meja 1898/99) ---
    ("s70-meja-marker", 70, 100, 260, 900, 460, 2.2),
]


def main():
    ok = 0
    for (name, scan, x0, y0, x1, y1, zoom) in CROPS:
        im = Image.open(f"/tmp/p164/s{scan:02d}.jpg")
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
