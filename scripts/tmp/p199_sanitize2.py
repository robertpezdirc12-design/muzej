#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P199 — sanitizacija-2: verifikatorji-podrobno (leta-nabori +1878,
apostrof-105→128, dict-105→128 — vzorec-podrobne-patche P198-#16-lekcije!)."""
import glob, re
from pathlib import Path

ROOT = Path("/home/z/muzej")
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True)
                   + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_")
tot_leta = tot_apo = tot_dikt = 0

OLD_SETS = [
    ('{"1879", "1880", "1881", "1882", "1883", "1884", "1885"}',
     '{"1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}'),
    ('{"1880", "1881", "1882", "1883", "1884", "1885"}',
     '{"1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}'),
    ('{"1882", "1883", "1884", "1885"}',
     '{"1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}'),
]
for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    o = t

    # 1) leta-nabori → + "1878"
    c1 = 0
    for old, new in OLD_SETS:
        c = t.count(old)
        if c:
            t = t.replace(old, new)
            c1 += c
    # + imena-preverjanj 'leta-{...}'
    t = t.replace("I10b 04106-leta-{1879,1880,1881,1882,1883,1884,1885}",
                  "I10b 04106-leta-{1878,1879,1880,1881,1882,1883,1884,1885}")
    t = t.replace("I10b 04106-leta-{1880,1881,1882,1883,1884,1885}",
                  "I10b 04106-leta-{1878,1879,1880,1881,1882,1883,1884,1885}")
    t = t.replace("I10b 04106-leta-{1882,1883,1884,1885}",
                  "I10b 04106-leta-{1878,1879,1880,1881,1882,1883,1884,1885}")

    # 2) apostrof-forme: '04106"') == 105 → == 128
    n_apo = len(re.findall(r"'04106\"'\) == 105", t))
    t = re.sub(r"('04106\"'\) == )105", r"\g<1>128", t)

    # 3) dict-forme: "04106": 105 → 128
    n_dikt = t.count('"04106": 105')
    t = t.replace('"04106": 105', '"04106": 128')

    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        if c1:
            tot_leta += c1
        if n_apo:
            tot_apo += n_apo
            print(f"  apostrof-105→128: {f} ×{n_apo}")
        if n_dikt:
            tot_dikt += n_dikt
            print(f"  dict-105→128: {f} ×{n_dikt}")

print(f"leta-nabori-+1878: ×{tot_leta} | apostrof-105→128: ×{tot_apo} | dict-105→128: ×{tot_dikt}")
