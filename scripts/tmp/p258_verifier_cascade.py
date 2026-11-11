#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258 — kaskadna posodobitev starih VERIFIKATORJEV .py (p230–p257 → živo-stanje P258:
2043→2059 · 01738 31→47 · SIX 23→31 · bothEra 26→34 · MILIČ 250→252 · h50-12→13 · h22-35→36)."""
import glob
import re

REPL = [
    # splošni živi števci (vsi verifikatorji)
    ('qa.count("HOUSE_VITALS.length !== 2043")', 'qa.count("HOUSE_VITALS.length !== 2059")'),
    ('števec-2043 (P254-sanacija!)', 'števec-2059 (P258-kaskada!)'),
    ('f"2043-številcev={st}"', 'f"2059-številcev={st}"'),
    ("len(bloki) == 2043", "len(bloki) == 2059"),
    ("skupaj == 2043", "skupaj == 2059"),
    ('"vitalsTotal": 2043', '"vitalsTotal": 2059'),
    ("pt-luknja-288/2043", "pt-luknja-288/2059"),
    ("pt-luknja-2043", "pt-luknja-2059"),
    ("pt-luknja-20438:31", "pt-luknja-2059/01738:47"),
    ("1940→2043-P257", "1940→2059-P258"),
    ("korpus == 2043", "korpus == 2059"),
    ("== 2043 blokov", "== 2059 blokov"),
    ("vitals == 2043", "vitals == 2059"),
    ("I2 vitals == 2043 + 01738 == 31", "I2 vitals == 2059 + 01738 == 47"),
    ("(P257: +11-1830/31!)", "(P258: +16-1831k/32/33!)"),
    # byBook 01738 31→47
    ('"01738": 31', '"01738": 47'),
    ("01738 == 31", "01738 == 47"),
    ("bloki-01738 ≠ 31", "bloki-01738 ≠ 47"),
    ("31/288/502/269/433/520", "47/288/502/269/433/520"),
    ("P257-01738-31", "P258-01738-47"),
    # MILIČ 250→252 (p237 + p239–p242)
    ("MILIC_FAMILY_TOTAL !== 250", "MILIC_FAMILY_TOTAL !== 252"),
    ("živi preverja 250/53-78-20-36-60-3", "živi preverja 252/53-78-20-36-60-5"),
    ("skupaj 250 (Python-križ", "skupaj 252 (Python-križ"),
    ("MILIČ-family-total == 250", "MILIČ-family-total == 252"),
    ("milič == 250", "milič == 252"),
    ("MILIČ == 250", "MILIČ == 252"),
    ("family == 250", "family == 252"),
    ("total == 250", "total == 252"),
    ("250 (53+78", "252 (53+78"),
    # SIX 23→31 + bothEra 26→34 + tierji (p254/255/256/257)
    ('["1", "3", "5", "6", "10", "11", "12", "16", "18", "19", "20", "22", "26", "27", "28", "32", "33", "56", "61", "62", "63", "65", "73"]',
     '["1", "2", "3", "5", "6", "8", "10", "11", "12", "16", "18", "19", "20", "22", "26", "27", "28", "32", "33", "35", "36", "42", "46", "47", "48", "56", "61", "62", "63", "65", "73"]'),
    ('["1","3","5","6","10","11","12","16","18","19","20","22","26","27","28","32","33","56","61","62","63","65","73"]',
     '["1","2","3","5","6","8","10","11","12","16","18","19","20","22","26","27","28","32","33","35","36","42","46","47","48","56","61","62","63","65","73"]'),
    ("(P257-23!)", "(P258-31!)"),
    ("SIX-×23", "SIX-×31"),
    ("sixBook == 23", "sixBook == 31"),
    ("tiers-six-23", "tiers-six-31"),
    ("stories-23 (P257!)", "stories-31 (P258!)"),
    ("23-zgodb — P257!", "31-zgodb — P258!"),
    ("23 ZGODB (P257!)", "31 ZGODB (P258!)"),
    ("bothEraPorocna-26", "bothEraPorocna-34"),
    ("bothEraPorocna == 26", "bothEraPorocna == 34"),
    ("bothEraPorocna !== 26", "bothEraPorocna !== 34"),
    ("bothEra-26 (P257!)", "bothEra-34 (P258!)"),
    ("bothEra == 26", "bothEra == 34"),
    ("obe-eri 69/75/26", "obe-eri 69/75/34"),
    ("69/75/26", "69/75/34"),
    ("tierji-23/41", "tierji-31/35"),
    ("tiers[6] == 23", "tiers[6] == 31"),
    ('"sixBook": 23', '"sixBook": 31'),
    ('"sixBook": 31', '"sixBook": 31'),
    # p254: h50-12→13-blokov + h22-35→36 + h2-66→93
    ("h50-story: 12-blokov-1831–1924-span-93", "h50-story: 13-blokov-1831–1924-span-93"),
    ("12-blokov-1831", "13-blokov-1831"),
    ("h50-12-blokov", "h50-13-blokov"),
    ("h22-35-blokov", "h22-36-blokov"),
    # p257 specifično: 1831-bloki scan-7 + h22-perBook-3→4
    ("bloki1831 = re.findall(r'houseNo: \"([^\"]+)\",\\s*bookSignature: \"01738\",\\s*year: 1831,', src)",
     "bloki1831 = re.findall(r'houseNo: \"([^\"]+)\",\\s*bookSignature: \"01738\",\\s*year: 1831,\\s*scan: 7,', src)  # P258: +scan-7!"),
    ("h22st.perBook[0]?.n !== 3", "h22st.perBook[0]?.n !== 4"),
    ("/35-blokov/01738×3", "/36-blokov/01738×4"),
    ("h22 ≠ firstYear-1828/span-93/35-blokov", "h22 ≠ firstYear-1828/span-93/36-blokov"),
]

changed = 0
for f in sorted(glob.glob("scripts/p2*.py")):
    name = f.split("/")[-1]
    if any(x in name for x in ("oldverifier", "_update", "insert", "korekcija", "docs", "restore", "fix", "worklog", "readme", "_gen", "build", "kompozit", "crops", "sanacija", "bump", "guards", "module_append", "p258")):
        continue
    try:
        s = open(f, encoding="utf-8").read()
    except Exception:
        continue
    s0 = s
    for a, b in REPL:
        s = s.replace(a, b)
    if s != s0:
        open(f, "w", encoding="utf-8").write(s)
        changed += 1
        print(f"posodobljen: {name}")
print(f"\nskupaj: {changed} verifikatorjev")
