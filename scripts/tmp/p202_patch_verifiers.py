#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P202 — patch starih verifierjev p190–p201 (kumulativni-števci + leta-nabori + 1875).
Vzorec P201-seje: vsaka-faza-patcha-VSE-starе-verifierje-naprej."""
import re
from pathlib import Path

ROOT = Path("/home/z/my-project/scripts")
patched = 0
for f in sorted(ROOT.glob("p19*.py")) + sorted(ROOT.glob("p20[01]_parish*.py")):
    t = f.read_text(encoding="utf-8")
    o = t
    # kumulativni-števci (verifierji + EXPECTED_CORPUS)
    t = t.replace("04106 == 156", "04106 == 166")
    t = t.replace("04106==156", "04106==166")
    t = t.replace("04106\": 156", "04106\": 166")
    t = t.replace("skupaj == 156", "skupaj == 166")
    t = t.replace('"04106") == 156', '"04106") == 166')
    t = t.replace("(04106, 156)", "(04106, 166)")
    t = t.replace("byBook\"][\"04106\"] == 156", "byBook\"][\"04106\"] == 166")
    t = t.replace("vitals == 1375", "vitals == 1385")
    t = t.replace("vitalsTotal == 1375", "vitalsTotal == 1385")
    t = t.replace("!== 1375\"", "!== 1385\"")
    t = t.replace("1375-številcev", "1385-številcev")
    t = t.replace("vitals-števec-1375", "vitals-števec-1385")
    t = t.replace("vitals-1375", "vitals-1385")
    # leta-nabori: set(izven) == {...} — dodaj "1875"
    t = re.sub(r'set\(izven\) == \{"1876"', 'set(izven) == {"1875", "1876"', t)
    # leta-join (p199/p200/p201-forma)
    t = t.replace('",".join(leta) == "1876,1877', '",".join(leta) == "1875,1876,1877')
    t = t.replace('join(leta) == "1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8")
        patched += 1
        print(f"patched: {f.name}")
print(f"SKUPAJ: {patched}")
