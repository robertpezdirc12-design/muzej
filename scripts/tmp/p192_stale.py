#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — stale-sanacija: VITALS 1219→1235 v 40 skriptah (p80 + p153–p191).
LEKCIJA-3 (P187): spremeni CILJE (pričakovane vrednosti), ne virov (komentarje zgodovine)."""
import re, py_compile, sys

files = [
    "scripts/p80_parish_md_books.py",
] + [f"scripts/p{n}_parish_death_{y}.py" for n, y in [
    (153,1887),(154,1888),(155,1889),(156,1890),(157,1891),(158,1892),(159,1893),(160,1894),
    (161,1895),(162,1896),(163,1897),(164,1898),(165,1899),(166,1900),(167,1901),(168,1902),
    (169,1903),(170,1904),(171,1905),(172,1923),(173,1907),(174,1908),(175,1909),(176,1910),
    (177,1911),(178,1912),(179,1913),(180,1914),(181,1915),(182,1916),(183,1917),(184,1918),
    (185,1919),(186,1920),(187,1921),(188,1922),(189,1923),(190,1924)]] + [
    "scripts/p191_pt_luknja_final.py",
]

changed = 0
for f in files:
    src = open(f, encoding="utf-8").read()
    orig = src
    # 1) VITALS_TOTAL = 1219 → 1235
    src = src.replace("VITALS_TOTAL = 1219", "VITALS_TOTAL = 1235")
    # 2) len(vitals) == 1219 → 1235 (p80-skripta + verifikatorji)
    src = src.replace("len(vitals) == 1219", "len(vitals) == 1235")
    # 3) "== 1219" preostanek (npr. vitals==1219)
    src = re.sub(r"(vitals\s*==\s*)1219\b", r"\g<1>1235", src)
    # 4) qa.count("!== 1219") → 1235
    src = src.replace('qa.count("!== 1219")', 'qa.count("!== 1235")')
    # 5) pini 1219 → 1235 (p80-skripta-pini)
    src = src.replace("pini 1219", "pini 1235")
    # 6) 'vitals 1219' v pričakovanjih-stringih I-checkov (ne v zgodovinskih komentarjih!)
    src = src.replace("vitals 1219 ·", "vitals 1235 ·").replace("vitals 1219 (", "vitals 1235 (")
    if src != orig:
        open(f, "w", encoding="utf-8").write(src)
        changed += 1

print(f"spremenjenih: {changed}/{len(files)}")
# py_compile vseh
bad = 0
for f in files:
    try:
        py_compile.compile(f, doraise=True)
    except Exception as e:
        print(f"COMPILE-FAIL {f}: {e}")
        bad += 1
print(f"py_compile: {len(files)-bad}/{len(files)}")
sys.exit(1 if bad else 0)
