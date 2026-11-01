#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P175 stale-sanacija-2. krog: preostali stale-vzorci, ki jih P174-sanacija
ni zajela (996-p80-pini + < 1908-guardi + >= 1906 + 297-qa-pini)."""
import glob, re, io

changed = []
for path in sorted(glob.glob("scripts/p1*_parish_death_*.py")):
    num = re.match(r"scripts/p(\d+)_", path)
    if not num or not (153 <= int(num.group(1)) <= 174):
        continue
    src = io.open(path, encoding="utf-8").read()
    orig = src
    # 1. p80-pin-checki (I6f + I12b) — vsi-stari-vitali-pini → 1020
    src = re.sub(r'"len\(vitals\) == \d+" in p80', '"len(vitals) == 1020" in p80', src)
    src = re.sub(r'"len\(vitals\) == \d+" in p80_script', '"len(vitals) == 1020" in p80_script', src)
    # 2. I6d2-guardi — < 1908 → < 1910
    src = src.replace('all(v["year"] < 1908 for v in d04894)',
                      'all(v["year"] < 1910 for v in d04894)')
    src = src.replace('(v["year"] or 0) >= 1906', '(v["year"] or 0) >= 1910')
    # 3. I12d qa-pini — 04894").length !== 297 → !== 321
    src = src.replace("qa.count('04894\").length !== 297')",
                      "qa.count('04894\").length !== 321')")
    if src != orig:
        io.open(path, "w", encoding="utf-8").write(src)
        changed.append(path)

print("SANACIJA-2:", len(changed), "skript")
for c in changed:
    print(" -", c)
