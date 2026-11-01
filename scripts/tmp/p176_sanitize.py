#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P176 kaskada — sanitacija ×4 kroga:
  1) qa-parish.ts: !== 1020→1032 (90×) · !== 321→333 (24×) · >= 1910→1911 (23×)
     · p80Death-message · allow-listi ×4 (h7/h90 @L747, h91 @L1062, h14 @L1377, h49 @L1737)
  2) scripts p153–p175 (23): VITALS_TOTAL 1032 · BLOKI 333 · guardi 1911 · stale 92-fix
  3) scripts/p80: vitals 1032 + P176-komentar
  4) stale-forme: len(houses)==93→92 · p80Houses.size!==93→92 (P175-revert-lekcija!)"""
import io, re, glob

def patch(path, edits, label):
    src = io.open(path, encoding="utf-8").read()
    orig = src
    miss = []
    for old, new in edits:
        if old in src:
            src = src.replace(old, new)
    if src != orig:
        io.open(path, "w", encoding="utf-8").write(src)
        print(f"PATCHED {label}: {path}")
    return src

QA = "src/lib/qa-parish.ts"

# ——— 1. qa-parish.ts ———
qa = io.open(QA, encoding="utf-8").read()
n1020 = qa.count("!== 1020")
n321 = qa.count("!== 321")
n1910 = qa.count(">= 1910")
qa = qa.replace("!== 1020", "!== 1032").replace("!== 321", "!== 333").replace(">= 1910", ">= 1911")
qa = qa.replace(
    "p80Errors.push(`mrliški vpisi (04894) ≠ 333 (${p80Death.length} — P80: 15 + P153–P174: 295 + P175: + 11 blokov 1909 = 321!)`);",
    "p80Errors.push(`mrliški vpisi (04894) ≠ 333 (${p80Death.length} — P80: 15 + P153–P175: 306 + P176: + 12 blokov 1910 = 333!)`);")
qa = qa.replace(
    "p80Errors.push(`mrliški vpisi (04894) ≠ 321 (${p80Death.length} — P80: 15 + P153–P174: 295 + P175: + 11 blokov 1909 = 321!)`);",
    "p80Errors.push(`mrliški vpisi (04894) ≠ 333 (${p80Death.length} — P80: 15 + P153–P175: 306 + P176: + 12 blokov 1910 = 333!)`);")
# allow-listi ×4 (P176: + 12 blokov 04894-1910)
qa = qa.replace(
    '&& !(v.bookSignature === "04894" && v.year === 1908 && hn === "30") ))',
    '&& !(v.bookSignature === "04894" && v.year === 1908 && hn === "30") && !(v.bookSignature === "04894" && v.year === 1910 && (hn === "7" || hn === "90")) ))')
qa = qa.replace(
    '&& !(v.bookSignature === "04894" && v.year === 1907 && hn === "91")))',
    '&& !(v.bookSignature === "04894" && v.year === 1907 && hn === "91") && !(v.bookSignature === "04894" && v.year === 1910 && hn === "91")))')
qa = qa.replace(
    '&& !(v.bookSignature === "04894" && v.year === 1907 && hn === "14")))',
    '&& !(v.bookSignature === "04894" && v.year === 1907 && hn === "14") && !(v.bookSignature === "04894" && v.year === 1910 && hn === "14")))')
qa = qa.replace(
    '&& !(v.bookSignature === "04894" && v.year === 1907 && hn === "49")))',
    '&& !(v.bookSignature === "04894" && v.year === 1907 && hn === "49") && !(v.bookSignature === "04894" && v.year === 1910 && hn === "49")))')
io.open(QA, "w", encoding="utf-8").write(qa)
print(f"QA: 1020→1032 ×{n1020} · 321→333 ×{n321} · 1910→1911 ×{n1910} + allow-listi ×4 + p80Death-msg")

# ——— 2. scripts p153–p175 ———
DEATH_SCRIPTS = sorted(glob.glob("scripts/p15*_parish_death_18*.py") + glob.glob("scripts/p16*_parish_death_19*.py") + glob.glob("scripts/p17*_parish_death_19*.py"))
for sp in DEATH_SCRIPTS:
    s = io.open(sp, encoding="utf-8").read()
    orig = s
    s = re.sub(r"VITALS_TOTAL = 1020[^\n]*", "VITALS_TOTAL = 1032             # 1020 + 12! (P176)", s)
    s = re.sub(r"BLOKI_04894 = 321[^\n]*", "BLOKI_04894 = 333               # 321 + 12! (P176)", s)
    s = s.replace("vitals 1020", "vitals 1032")
    s = s.replace("mrliški bloki 04894 = 321", "mrliški bloki 04894 = 333")
    s = s.replace('"len(vitals) == 1020" in p80', '"len(vitals) == 1032" in p80')
    s = s.replace('"len(houses) == 93" in p80', '"len(houses) == 92" in p80')
    s = s.replace('qa.count("!== 1020") == 90', 'qa.count("!== 1032") == 90')
    s = s.replace("qa.count('!== 1020')", "qa.count('!== 1032')")
    s = s.replace('qa.count("!== 321") == 24', 'qa.count("!== 333") == 24')
    s = s.replace("qa.count('!== 321')", "qa.count('!== 333')")
    s = s.replace('qa.count("p80Houses.size !== 93")', 'qa.count("p80Houses.size !== 92")')
    s = s.replace("qa.count('p80Houses.size !== 93')", "qa.count('p80Houses.size !== 92')")
    s = s.replace(">= 1910", ">= 1911")
    s = s.replace('year"] < 1910 for v in d04894', 'year"] < 1911 for v in d04894')
    s = s.replace('f"1020×', 'f"1032×').replace('}/321×', '}/333×')
    s = s.replace('f"1009×', 'f"1032×').replace('}/310×', '}/333×')
    if s != orig:
        io.open(sp, "w", encoding="utf-8").write(s)
        print(f"PATCHED {sp}")

# ——— 3. p80 skripta ———
P80 = "scripts/p80_parish_md_books.py"
p80 = io.open(P80, encoding="utf-8").read()
p80 = p80.replace(
    "and len(vitals) == 1020  # POSODABLJENO P175:",
    "and len(vitals) == 1032  # POSODABLJENO P176: 1020 → 1032 (+12 blokov mrliške 04894-1910!); POSODABLJENO P175:")
io.open(P80, "w", encoding="utf-8").write(p80)
print("PATCHED p80 vitals 1032")

print("SANITACIJA KONČANA")
