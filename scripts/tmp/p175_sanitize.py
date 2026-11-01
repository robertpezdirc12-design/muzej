#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P175 stale-sanacija: p153–p174 (22 skript) + p80-skripta.
VITALS_TOTAL 1009→1020 · BLOKI_04894 310→321 · guardi 1909→1910 ·
qa-pini '!== 1009'→'!== 1020' · '!== 310'→'!== 321' · '>= 1909'→'>= 1910' ·
p80-pin 92→93 + p80-skripta 1009/92→1020/93."""
import glob, re, io

changed = []
for path in sorted(glob.glob("scripts/p1*_parish_death_*.py")):
    num = re.match(r"scripts/p(\d+)_", path)
    if not num or not (153 <= int(num.group(1)) <= 174):
        continue
    src = io.open(path, encoding="utf-8").read()
    orig = src
    # 1. konstanti
    src = src.replace("VITALS_TOTAL = 1009", "VITALS_TOTAL = 1020")
    src = src.replace("BLOKI_04894 = 310", "BLOKI_04894 = 321")
    # 2. qa-pin-nizi (count-checki)
    src = src.replace('qa.count("!== 1009")', 'qa.count("!== 1020")')
    src = src.replace("qa.count('!== 1009')", "qa.count('!== 1020')")
    src = src.replace('qa.count("!== 310")', 'qa.count("!== 321")')
    src = src.replace("qa.count('!== 310')", "qa.count('!== 321')")
    src = src.replace('qa.count(">= 1909")', 'qa.count(">= 1910")')
    src = src.replace("qa.count('>= 1909')", "qa.count('>= 1910')")
    src = src.replace('qa.count("p80Houses.size !== 92")', 'qa.count("p80Houses.size !== 93")')
    src = src.replace("qa.count('p80Houses.size !== 92')", "qa.count('p80Houses.size !== 93')")
    # 3. p80-skripta-check-nizi (I6e)
    src = src.replace('"len(vitals) == 1009" in p80', '"len(vitals) == 1020" in p80')
    src = src.replace('"len(houses) == 92" in p80', '"len(houses) == 93" in p80')
    # 4. filter-guardi (04894-leto-meja)
    src = src.replace('(v["year"] or 0) >= 1909', '(v["year"] or 0) >= 1910')
    src = src.replace('(v["year"] or 0) < 1909', '(v["year"] or 0) < 1910')
    src = src.replace('v["year"] < 1909', 'v["year"] < 1910')
    src = src.replace('(h.year ?? 0) >= 1909', '(h.year ?? 0) >= 1910')
    # 5. trde-enakosti v count-checkih (p172/p173/p174)
    src = src.replace('qa.count("!== 1020") == 88', 'qa.count("!== 1020") == 90')
    src = src.replace('qa.count("!== 1020") == 89', 'qa.count("!== 1020") == 90')
    src = src.replace('qa.count("!== 321") == 22', 'qa.count("!== 321") == 24')
    src = src.replace('qa.count("!== 321") == 23', 'qa.count("!== 321") == 24')
    src = src.replace('qa.count(">= 1910") == 21', 'qa.count(">= 1910") == 23')
    src = src.replace('qa.count(">= 1910") == 22', 'qa.count(">= 1910") == 23')
    # 6. display f-stringi
    src = src.replace("1009×{qa.count('!== 1009')}", "1020×{qa.count('!== 1020')}")
    src = src.replace("310×{qa.count('!== 310')}", "321×{qa.count('!== 321')}")
    src = src.replace("{qa.count('>= 1909')}", "{qa.count('>= 1910')}")
    src = src.replace("{qa.count('p80Houses.size !== 92')}", "{qa.count('p80Houses.size !== 93')}")
    # 7. check-imena (I6d2/I11d — lead-skoščki)
    src = src.replace("I6d2 bloki 1909+ ne obstajajo (P175-lead!; P174 = 1908 sedaj v korpusu!)",
                      "I6d2 bloki 1910+ ne obstajajo (P176-lead!; P175 = 1909 sedaj v korpusu!)")
    src = src.replace("I11d ni-04894-1909-blokov-še (P175-lead!; 04455/04105-1909-legalno!)",
                      "I11d ni-04894-1910-blokov-še (P176-lead!; 04455/04105-1910-legalno!)")
    src = src.replace('bookSignature: "04894",\\s*year: 1909', 'bookSignature: "04894",\\s*year: 1910')
    src = src.replace("I8c P175-lead v dokazu (1909 + Stublar-92 + ŠILAK-dvojčki!)",
                      "I8c P175-lead v dokazu (1909 + Stublar-92 + ŠILAK-dvojčki!) [P175-zgodovinska]")
    if src != orig:
        io.open(path, "w", encoding="utf-8").write(src)
        changed.append(path)

# ——— p80-skripta ———
p80 = "scripts/p80_parish_md_books.py"
src = io.open(p80, encoding="utf-8").read()
orig = src
src = src.replace("and len(vitals) == 1009  # POSODABLJENO P174:",
                  "and len(vitals) == 1020  # POSODABLJENO P175: 1009 → 1020 (+11 blokov mrliške 04894-1909!); POSODABLJENO P174:")
src = src.replace("and len(houses) == 92  # P174: 92 NESPREMENJENO",
                  "and len(houses) == 93  # P175: 92 → 93 (+h86 — mrliška 04894-1909 Marija-KRIŽAN = 1. mrliški vpis h86 = 31.-PT-kandidat!); P174: 92 NESPREMENJENO")
if src != orig:
    io.open(p80, "w", encoding="utf-8").write(src)
    changed.append(p80)

print("SANACIRANO:", len(changed), "skript")
for c in changed:
    print(" -", c)
