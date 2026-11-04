#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P201 — patch starih verifierjev p191–p200 (kumulativni-števci + leta-nabori + 1876).
Vzorec P200-seje: vsaka-faza-patcha-VSE-starе-verifierje-naprej."""
import re
from pathlib import Path

ROOT = Path("/home/z/muzej/scripts")
patched = 0
for f in sorted(ROOT.glob("p19*.py")) + sorted(ROOT.glob("p200_parish*.py")):
    t = f.read_text(encoding="utf-8")
    o = t
    # kumulativni-števci (p199/p200-verifier + p191 EXPECTED_CORPUS)
    t = t.replace("04106 == 136", "04106 == 156")
    t = t.replace("04106==136", "04106==156")
    t = t.replace("04106\": 136", "04106\": 156")
    t = t.replace("skupaj == 136", "skupaj == 156")
    t = t.replace('"04106") == 136', '"04106") == 156')
    t = t.replace("(04106, 136)", "(04106, 156)")
    t = t.replace("byBook\"][\"04106\"] == 136", "byBook\"][\"04106\"] == 156")
    t = t.replace("vitals == 1355", "vitals == 1375")
    t = t.replace("vitalsTotal == 1355", "vitalsTotal == 1375")
    t = t.replace("!== 1355\"", "!== 1375\"")
    t = t.replace("1355-številcev", "1375-številcev")
    t = t.replace("vitals-števec-1355", "vitals-števec-1375")
    t = t.replace("vitals-1355", "vitals-1375")
    # leta-nabori: set(izven) == {...} — dodaj "1876"
    t = re.sub(r'set\(izven\) == \{"1877"', 'set(izven) == {"1876", "1877"', t)
    # leta-join (p199/p200-forma)
    t = t.replace('",".join(leta) == "1877,1878', '",".join(leta) == "1876,1877,1878')
    t = t.replace('join(leta) == "1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8")
        patched += 1
        print(f"patched: {f.name}")
print(f"SKUPAJ: {patched}")
