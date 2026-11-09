#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P175 fix-round: p80-kaskada-REVERT (93→92 — h86-ŽE-v-p80-prek-04455-1910!)
+ qa-p92/qa-p93 allow-listi (h43/h18-1909) + tekstovne korekcije."""
import io

def patch(path, edits, label):
    src = io.open(path, encoding="utf-8").read()
    orig = src
    miss = []
    for old, new in edits:
        if old not in src:
            miss.append(old[:80])
        src = src.replace(old, new)
    if src != orig:
        io.open(path, "w", encoding="utf-8").write(src)
        print(f"PATCHED {label}: {path}")
    if miss:
        print(f"  ⚠ {label} MANJKA {len(miss)}:")
        for m in miss:
            print("   -", m)

QA = "src/lib/qa-parish.ts"
P175 = "scripts/p175_parish_death_1909.py"
P80S = "scripts/p80_parish_md_books.py"
BLD = "scripts/tmp/p175_build_dokaz.py"
NOTES = "research/issue17/parish-death-1909-notes.md"
PARISH = "src/data/atlas/parish.ts"

# ——— 1. qa-parish.ts ———
patch(QA, [
    # 1a. revert 24× p80-pogoj
    ("p80Houses.size !== 93", "p80Houses.size !== 92"),
    # 1b. qa-p175 komentar (line ~6932)
    ("z17-'84'→64-P174-lead-KOREKCIJA + h86-1.-MRLIŠKI-VPIS-KADARKOLI → p80 93 +",
     "z17-'84'→64-P174-lead-KOREKCIJA + h86-1.-MRLIŠKI-VPIS-KADARKOLI (p80-92-NESPREMENJENO — h86-ŽE-v-filtru!) +"),
    # 1c. qa-p175 check-message (line ~6952)
    ('p175Errors.push("★★★ z52-h86-1.-MRLIŠKI-VPIS-KADARKOLI (31.-PT-kandidat — p80 92→93!) manjka");',
     'p175Errors.push("★★★ z52-h86-1.-MRLIŠKI-VPIS-KADARKOLI (31.-PT-kandidat — p80-92-NESPREMENJENO!) manjka");'),
    # 1d. Si-push — h86-člen
    ("= 31.-PT-kandidat → **p80 92→93 (+h86!)**)",
     "= 31.-PT-kandidat; **p80 92-NESPREMENJENO — h86-ŽE-v-p80-prek-04455-1910-poročna-P139!**)"),
    # 1e. En-push — h86-člen
    ("= the-31st-PT-candidate → **the p80 92→93 (+h86!)**)",
     "= the-31st-PT-candidate; **the p80 92-UNCHANGED — the h86-ALREADY-in-p80-via-the-04455-1910-marriage-P139!**)"),
    # 1f. Si — 11-NOVIH-BLOKOV
    ("mrliški 04894 310 → 321 · p80 92 → 93 (+h86!) · korpus 93 NESPREMENJEN",
     "mrliški 04894 310 → 321 · p80 92-NESPREMENJENO (h86-ŽE-v-filtru!) · korpus 93 NESPREMENJEN"),
    # 1g. En — 11-NEW-BLOCKS
    ("the 04894 310 → 321 · the p80 92 → 93 (+h86!) · the corpus 93 UNCHANGED",
     "the 04894 310 → 321 · the p80 92-UNCHANGED (the h86-ALREADY-in-the-filter!) · the corpus 93 UNCHANGED"),
    # 1h. Si/En — kaskada-p80-skripta
    ("p80-skripta-1020/93", "p80-skripta-1020/92"),
    ("the p80-script-1020/93", "the p80-script-1020/92"),
    # 1i. Si/En — korpus-po-P175
    ("korpus po P175: 1020/197+321/190/93(p80)·93(korpus)", "korpus po P175: 1020/197+321/190/92(p80)·93(korpus)"),
    ("the corpus after P175: 1020/197+321/190/93(p80)·93(corpus)", "the corpus after P175: 1020/197+321/190/92(p80)·93(corpus)"),
    # 1j. success-detail — p80-93 + kumulativ
    ("h86-1.-MRLIŠKI-KADARKOLI (p80 93!)", "h86-1.-MRLIŠKI-KADARKOLI (p80-92-NESPREMENJENO!)"),
    ("kumulativ po P175: 1020/321/93/93 (PT 29)", "kumulativ po P175: 1020/321/92/93 (PT 29)"),
    # 1k. qa-p92 — h43-1909-allow
    ('!(v.bookSignature === "04894" && v.year === 1892 && hn === "43")',
     '!(v.bookSignature === "04894" && v.year === 1892 && hn === "43") && !(v.bookSignature === "04894" && v.year === 1909 && hn === "43")'),
    ("P168: + mrliški blok 04894-1902 h40 (Ana-PEZDIREC-59 — 1. mrliški vpis h40 = 27. PT-vez!)",
     "P168: + mrliški blok 04894-1902 h40 (Ana-PEZDIREC-59 — 1. mrliški vpis h40 = 27. PT-vez!); P175: + mrliški blok 04894-1909 h43 (Marija-LAŠIČ-64 — 3. mrliški vpis!)"),
    # 1l. qa-p93 — h18-1909-allow
    ('!(v.bookSignature === "04894" && v.year === 1940 && hn === "18")',
     '!(v.bookSignature === "04894" && v.year === 1940 && hn === "18") && !(v.bookSignature === "04894" && v.year === 1909 && hn === "18")'),
    ("P172: + mrliški blok 04894-1940 h18 (Alojzij ŠIMEC — 6. mrliški!)",
     "P172: + mrliški blok 04894-1940 h18 (Alojzij ŠIMEC — 6. mrliški!); P175: + mrliški blok 04894-1909 h18 (Peter-ŠIMEC-64 — 7. mrliški vpis!)"),
], "QA")

# ——— 2. parish.ts blok-komentar ———
patch(PARISH, [
    ("// ★★ z52-h86 = 1. MRLIŠKI VPIS KADARKOLI (h86 = 04455-1910/04105-1912+ — vse-kasneje!) → p80 92→93!",
     "// ★★ z52-h86 = 1. MRLIŠKI VPIS KADARKOLI (h86 = 04455-1910/04105-1912+ — vse-kasneje!) → p80 92-NESPREMENJENO (h86-ŽE-v-p80-prek-04455-1910-poročna-P139!)"),
], "PARISH")

# ——— 3. p80-skripta revert ———
patch(P80S, [
    ("and len(houses) == 93  # P175: 92 → 93 (+h86 — mrliška 04894-1909 Marija-KRIŽAN = 1. mrliški vpis h86 = 31.-PT-kandidat!); P174: 92 NESPREMENJENO",
     "and len(houses) == 92  # P175: NESPREMENJENO — h86-ŽE-v-p80-prek-04455-1910-poročna-P139 (mrliška-04894-1909 Marija-KRIŽAN = 1. mrliški vpis h86 = 31.-PT-kandidat, hiša-ŽE-v-filtru!); P174: 92 NESPREMENJENO"),
], "P80-SKRIPTA")

# ——— 4. p175-skripta ———
patch(P175, [
    ("Kumulativ: vitals 1009 → 1020, mrliški bloki 04894 310 → 321, p80 92 → 93\n(+h86!), korpus 93 NESPREMENJEN, PT 29 (h86-31.-kandidat-NE-šteta!).",
     "Kumulativ: vitals 1009 → 1020, mrliški bloki 04894 310 → 321, p80 92\nNESPREMENJENO (h86-ŽE-v-p80-prek-04455-1910!), korpus 93 NESPREMENJEN,\nPT 29 (h86-31.-kandidat-NE-šteta!)."),
    ("P80_HOUSES = 93                 # 92 + h86 (1.-MRLIŠKI-KADARKOLI!)",
     "P80_HOUSES = 92                 # NESPREMENJENO — h86-ŽE-v-p80-prek-04455-1910-poročna-P139!"),
    ('          "1.-MRLIŠKI-VPIS-KADARKOLI" in a5["opis"] and "31.-PT-kandidat" in a5["opis"]\n          and "92→93" in a5["opis"], "")',
     '          "1.-MRLIŠKI-VPIS-KADARKOLI" in a5["opis"] and "31.-PT-kandidat" in a5["opis"]\n          and "92-NESPREMENJENO" in a5["opis"], "")'),
    ('check("I7c A5: h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (31.-PT-kandidat → p80 93!)",',
     'check("I7c A5: h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (31.-PT-kandidat — p80-92-NESPREMENJENO!)",'),
    ('check("I6e p80-skripta pini 1020 + 93 + gap-18 (vitals-P175-kaskada!)",\n          "len(vitals) == 1020" in p80 and "len(houses) == 93" in p80 and "len(gap) == 18" in p80, "")',
     'check("I6e p80-skripta pini 1020 + 92 + gap-18 (vitals-P175-kaskada!)",\n          "len(vitals) == 1020" in p80 and "len(houses) == 92" in p80 and "len(gap) == 18" in p80, "")'),
    ('check("I10d qa-parish p80 = 93 (24× — P175:+h86!)",\n          qa.count("p80Houses.size !== 93") == 24, f"{qa.count(\'p80Houses.size !== 93\')}")',
     'check("I10d qa-parish p80 = 92 (24× — NESPREMENJENO — h86-ŽE-v-filtru!)",\n          qa.count("p80Houses.size !== 92") == 24, f"{qa.count(\'p80Houses.size !== 92\')}")'),
], "P175-SKRIPTA")

# ——— 5. build_dokaz ———
patch(BLD, [
    ('"★★★ h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (korpus-04455-1910 + 04105-1912/1913/1918 — VSE-KASNEJE!) = 31.-PT-kandidat → p80 92→93 (+h86!) — VLM-\'Mišma\'-ZAVRJENO + diag-hišna-\'26\'→86!"',
     '"★★★ h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (korpus-04455-1910 + 04105-1912/1913/1918 — VSE-KASNEJE!) = 31.-PT-kandidat; p80 92-NESPREMENJENO (h86-ŽE-v-p80-prek-04455-1910-poročna-P139!) — VLM-\'Mišma\'-ZAVRJENO + diag-hišna-\'26\'→86!"'),
    ('"★★★ h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (korpus-04455-1910 + 04105-1912/1913/1918 — VSE-KASNEJE! = 31.-PT-kandidat → p80 92→93!) + ★★ VLM-\'Mišma\'-ZAVRJENO→KRIŽAN + diag-hišna-\'26\'→86-KOREKCIJA!"',
     '"★★★ h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (korpus-04455-1910 + 04105-1912/1913/1918 — VSE-KASNEJE! = 31.-PT-kandidat; p80-92-NESPREMENJENO — h86-ŽE-v-filtru!) + ★★ VLM-\'Mišma\'-ZAVRJENO→KRIŽAN + diag-hišna-\'26\'→86-KOREKCIJA!"'),
], "BUILD-DOKAZ")

# ——— 6. notes ———
patch(NOTES, [
    ("4. **z52-hiša = 86** (NE-diag-'26'!) — 1.-MRLIŠKI-VPIS-KADARKOLI-h86 (korpus-04455-1910 + 04105-1912+ — vse-kasneje!) → p80 92→93!",
     "4. **z52-hiša = 86** (NE-diag-'26'!) — 1.-MRLIŠKI-VPIS-KADARKOLI-h86 (korpus-04455-1910 + 04105-1912+ — vse-kasneje!) → p80 92-NESPREMENJENO (h86-ŽE-v-p80-prek-04455-1910-poročna-P139!)"),
    ("- h86 = **1. MRLIŠKI VPIS KADARKOLI** (31.-PT-kandidat → p80 93!)",
     "- h86 = **1. MRLIŠKI VPIS KADARKOLI** (31.-PT-kandidat; p80-92-NESPREMENJENO — hiša-ŽE-v-filtru!)"),
], "NOTES")

print("KONEC.")
