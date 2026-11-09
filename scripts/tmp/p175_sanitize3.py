#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P175 sanacija-3: končni popravki (p153-I10b, p157-I5d, p165-I12d,
p172/p173-I11d, p174-I5e/I11b) + p175-I5e-bug (Nikolaj-ŠILAK-match!)."""
import io

FIXES = {
    "scripts/p153_parish_death_1887.py": [
        ('check("I10b vitals-pin 996 v qa (P173)", "HOUSE_VITALS.length !== 996" in qa, "")',
         'check("I10b vitals-pin 1020 v qa (P175-kaskada)", "HOUSE_VITALS.length !== 1020" in qa, "")'),
    ],
    "scripts/p157_parish_death_1891.py": [
        ('check("I5d h85 = 1 mrliški (1891) + krstni 1888/1908 izven p80-filtra",\n'
         '          len(h85_mrl) == 1 and h85_mrl[0]["year"] == 1891',
         'check("I5d h85 = 3 mrliški (1891 + 1908-porodna + 1909-dojenček — PEZDIREC-vez!) + krstni 1888/1908 izven p80-filtra",\n'
         '          len(h85_mrl) == 3 and sorted(v["year"] for v in h85_mrl) == [1891, 1908, 1909]'),
    ],
    "scripts/p165_parish_death_1899.py": [
        ('qa.count("04894\\").length !== 297") >= 12, str(qa.count("04894\\").length !== 297"))',
         'qa.count("04894\\").length !== 321") >= 12, str(qa.count("04894\\").length !== 321"))'),
    ],
    "scripts/p172_parish_death_1940.py": [
        ('check("I11d ni-04894-1908-blokov-še (P174-lead!; P173 = 1907 sedaj v korpusu!; 04455-1908-legalno!)",\n'
         '          re.search(r\'bookSignature: "04894",\\s*year: 1908\', src) is None, "")',
         'check("I11d ni-04894-1910-blokov-še (P176-lead!; P175 = 1909 sedaj v korpusu!; 04455-1910-legalno!)",\n'
         '          re.search(r\'bookSignature: "04894",\\s*year: 1910\', src) is None, "")'),
    ],
    "scripts/p173_parish_death_1907.py": [
        ('check("I11d ni-04894-1908-blokov-še (P174-lead!; 04455-1908-legalno!)",\n'
         '          re.search(r\'bookSignature: "04894",\\s*year: 1908\', src) is None, "")',
         'check("I11d ni-04894-1910-blokov-še (P176-lead!; P175 = 1909 sedaj v korpusu!; 04455-1910-legalno!)",\n'
         '          re.search(r\'bookSignature: "04894",\\s*year: 1910\', src) is None, "")'),
    ],
    "scripts/p174_parish_death_1908.py": [
        ('check("I5e h20-Katarina-PERDINEC = VLM-\'Pečnik\'-ZAVRJENA-×3 (z70/z71!)",\n'
         '          "PERDINEC" in e20["whatSi"] and "Pečnik" in e20["whatSi"], "")',
         'check("I5e h20-Katarina-PEZDIREC = P175-KOREKCIJA-×2 (prejšnja-\'PERDINEC\'-\'Pečnik\'-ZAVRJENA — z-DESCENDER!)",\n'
         '          "PEZDIREC" in e20["whatSi"] and "P175-KOREKCIJA" in e20["whatSi"]\n'
         '          and "PERDINEC\' ZAVRJENA" in e20["whatSi"], "")'),
        ('"P173-LEAD-\'81\'-KOREKCIJA", "VLM-\'Alojz-Ožinger\'-ZAVRJENA",\n'
         '                                 "VLM-\'Pečnik\'-ZAVRJENA", "h24-×2-v-1908", "TAPRIČ-vez-h2×h33",',
         '"P173-LEAD-\'81\'-KOREKCIJA", "VLM-\'Alojz-Ožinger\'-ZAVRJENA",\n'
         '                                 "P175-KOREKCIJA", "h24-×2-v-1908", "TAPRIČ-vez-h2×h33",'),
    ],
    "scripts/p175_parish_death_1909.py": [
        ('e34b = next(v for v in d1909 if v["houseNo"] == "34" and "Nikolaj" in v["whatSi"])',
         'e34b = next(v for v in d1909 if v["houseNo"] == "34" and "Nikolaj ŠILAK" in v["whatSi"])'),
    ],
}

for path, edits in FIXES.items():
    src = io.open(path, encoding="utf-8").read()
    orig = src
    for old, new in edits:
        if old not in src:
            print(f"WARN: ni najdeno v {path}: {old[:70]}...")
        src = src.replace(old, new)
    if src != orig:
        io.open(path, "w", encoding="utf-8").write(src)
        print("FIXED:", path)
