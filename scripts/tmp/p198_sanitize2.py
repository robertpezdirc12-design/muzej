#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P198 — sanitizacija-2: verifikatorji-podrobno (leta-nabori +1879,
p192-apostrof-96→105, p191-dikt-83→105 — vzorec-podrobne-patche!).
LEKCIJA-P198-#16: apostrof-forme ('04106"') == 96') + dict-forme
("04106": 83) + set-literali ({"1880"...}) potrebujejo LASTNE-vzorce!"""
import glob, re
from pathlib import Path

ROOT = Path("/home/z/my-project/muzej-backup")
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True)
                   + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p198_")
tot_leta = tot_apo = tot_dikt = 0

for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    o = t

    # 1) leta-nabori v verifikatorjih: {"1880", ..., "1885"} → + "1879"
    OLD_SET = '{"1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}'
    NEW_SET = '{"1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}'
    c1 = t.count(OLD_SET)
    t = t.replace(OLD_SET, NEW_SET)
    # + imena-pretjarjev 'leta-{1880,...}'
    t = t.replace("I10b 04106-leta-{1878,1879,1880,1881,1882,1883,1884,1885}",
                  "I10b 04106-leta-{1878,1879,1880,1881,1882,1883,1884,1885}")
    t = t.replace("I10b 04106-leta-{1878,1879,1880,1881,1882,1883,1884,1885}",
                  "I10b 04106-leta-{1878,1879,1880,1881,1882,1883,1884,1885}")

    # 2) apostrof-forme: '...04106"') == 96 → == 105
    c2 = t.count('"04106"\'') if False else 0
    n_apo = len(re.findall(r"'04106\"'\) == 96", t))
    t = re.sub(r"('04106\"'\) == )96", r"\g<1>105", t)

    # 3) dict-forme: "04106": 83 → 105 (p191-vzorec!)
    n_dikt = t.count('"04106": 83')
    t = t.replace('"04106": 83', '"04106": 128')

    # 4) odprti-96-forme (dodatne): == 96 z 04106-kontekstom
    t = t.replace("04106-leta-{1879,1880,1881,1882,1883,1884,1885}", "04106-leta-{1879,1880,1881,1882,1883,1884,1885}")

    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        if c1:
            tot_leta += c1
        if n_apo:
            tot_apo += n_apo
            print(f"  apostrof-96→105: {f} ×{n_apo}")
        if n_dikt:
            tot_dikt += n_dikt
            print(f"  dict-83→105: {f} ×{n_dikt}")

print(f"leta-nabori-+1879: ×{tot_leta} | apostrof-96→105: ×{tot_apo} | dict-83→105: ×{tot_dikt}")
