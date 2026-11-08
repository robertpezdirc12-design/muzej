#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P225-sanitizacija-3: stari-verifierji-p221/p222/p223/p224 (04104-total 90→107 + pt-luknja-byBook→107!)."""
from pathlib import Path
ROOT = Path("/home/z/my-project")
patched = 0
for name in ["p221_parish_baptism_1885_04104.py", "p222_parish_baptism_1884_04104.py",
             "p223_parish_baptism_1883_04104.py", "p224_parish_baptism_1882_04104.py"]:
    f = ROOT / "scripts" / name
    t = f.read_text(encoding="utf-8"); o = t
    t = t.replace('check("I3 vitals-1781 + 04104==90", "HOUSE_VITALS.length !== 1781" not in src and skupaj == 90, f"04104={skupaj}")',
                  'check("I3 vitals-1781 + 04104==107", "HOUSE_VITALS.length !== 1781" not in src and skupaj == 107, f"04104={skupaj}")')
    t = t.replace('check("I9b pt-luknja-65/1781 + byBook-04104", \'"vitalsTotal": 1781\' in pt and \'"04104": 90\' in pt)',
                  'check("I9b pt-luknja-107/1781 + byBook-04104", \'"vitalsTotal": 1781\' in pt and \'"04104": 107\' in pt)')
    t = t.replace('check("I9b pt-luknja-90/1781 + byBook-04104", \'"vitalsTotal": 1781\' in pt and \'"04104": 90\' in pt)',
                  'check("I9b pt-luknja-107/1781 + byBook-04104", \'"vitalsTotal": 1781\' in pt and \'"04104": 107\' in pt)')
    if t != o:
        f.write_text(t, encoding="utf-8"); patched += 1
print(f"verifierji-patched: {patched} (pričakovano 4)")
