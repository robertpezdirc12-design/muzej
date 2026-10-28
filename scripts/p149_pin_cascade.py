#!/usr/bin/env python3
# P149 — pin-kaskada: vitals 698→702 · bloki 04455 181→185 · sidra 174→178
# (+ sanacija P148-zamud: p140–p147 tekoči I6 + p115 anchors/I8/I8c/I9c!)
import re
import sys

QA = "src/lib/qa-parish.ts"
changes = []


def sub_file(path, pairs, regex=False):
    src = open(path, encoding="utf-8").read()
    orig = src
    for old, new in pairs:
        if regex:
            src, n = re.subn(old, new, src)
        else:
            n = src.count(old)
            src = src.replace(old, new)
        if n:
            changes.append(f"{path}: {old[:60]!r} ×{n}")
    if src != orig:
        open(path, "w", encoding="utf-8").write(src)
    return src


# ---------- 1. qa-parish.ts ----------
qa = open(QA, encoding="utf-8").read()
n698 = qa.count("HOUSE_VITALS.length !== 698")
n181 = qa.count(".length !== 181")
n174 = qa.count("poročna sidra ≠ 174")
qa = qa.replace("HOUSE_VITALS.length !== 698", "HOUSE_VITALS.length !== 702")
qa = qa.replace("HOUSE_VITALS ≠ 698", "HOUSE_VITALS ≠ 702")
qa = qa.replace(".length !== 181", ".length !== 185")
qa = qa.replace("bloki 04455 ≠ 181", "bloki 04455 ≠ 185")
qa = qa.replace("poročna sidra ≠ 174", "poročna sidra ≠ 178")
# p148-specifični message-repi
qa = qa.replace("P147: 688; P148: + 10 blokov 1919 = 698!", "P148: 698; P149: + 4 blokov 1920 = 702!")
qa = qa.replace("P147: 171; P148: + 10 = 181!", "P148: 181; P149: + 4 = 185!")
qa = qa.replace("P147: 171; P148: + 10 = 181)", "P148: 181; P149: + 4 = 185)")
# 1920-filter v sidra-pogoju + razširitev sporočila
qa = qa.replace(
    "  p80MarrAnchors.filter((h) => h.year === 1917).length !== 1\n)",
    "  p80MarrAnchors.filter((h) => h.year === 1917).length !== 1 ||\n"
    "  p80MarrAnchors.filter((h) => h.year === 1920).length !== 4\n)",
)
qa = qa.replace(
    " · P148 +10 blokov (1919 = REKORD LINIJE 40 vpisov — 10 Griblje: №3 h22[~] · №6 h77×87 · №13 h12×30 · №18 h2×58 · №20 h41×64[~] · №21 h20×13 · №27 h48 · №33 h61 · №34 h26×24 · №35 h15!))",
    " · P148 +10 blokov (1919 = REKORD LINIJE 40 vpisov — 10 Griblje: №3 h22[~] · №6 h77×87 · №13 h12×30 · №18 h2×58 · №20 h41×64[~] · №21 h20×13 · №27 h48 · №33 h61 · №34 h26×24 · №35 h15!) · P149 +4 blokov (1920 = 2. največje leto 37 vpisov — №10 h46×h41 INTRA · №27 h18 · №28 h21 · №34 h6×h36 INTRA!))",
)
# p80Houses-zgodovina
qa = qa.replace(
    "; P145–P147: 0 novih; P148: +h2/h12/h77 (poročna 1919 — 3 NOVE hiše v 04455: h2 1. poročni dokaz NAJNIŽJE aktivne številke! · h12 1. poročni dokaz! · h77 1. poročni dokaz!; h15/20/22/26/41/48/61/87 že v 04455!) → 75`",
    "; P145–P147: 0 novih; P148: +h2/h12/h77 (poročna 1919 — 3 NOVE hiše v 04455: h2 1. poročni dokaz NAJNIŽJE aktivne številke! · h12 1. poročni dokaz! · h77 1. poročni dokaz!; h15/20/22/26/41/48/61/87 že v 04455!) → 75; P149: 0 novih (h6/18/21/36/46 že v vzorci!) → 75`",
)
changes.append(f"qa-parish.ts: 698-pini {n698} → 702 · 181-pini {n181} → 185 · sidra-174 {n174} → 178")
open(QA, "w", encoding="utf-8").write(qa)

# ---------- 2. p80 ----------
sub_file("scripts/p80_parish_md_books.py",
         [("len(vitals) == 688  # POSODABLJENO P144: 578 (era P126) → 670 (P140) → 675 (P141) → 681 (P142) → 685 (P143) → 686 (živi korpus!; P127–P144: poročna linija 1898–1915)",
           "len(vitals) == 702  # POSODABLJENO P149: 578 (era P126) → 686 (P144) → 688 (P146) → 698 (P148: +10 blokov 1919!) → 702 (P149: +4 blokov 1920!)")])

# ---------- 3. p115 (anchors + BLOCKS + I9c) ----------
p115 = "scripts/p115_parish_marriage_1886.py"
src = open(p115, encoding="utf-8").read()
src = src.replace("BLOCKS_04455 = 185                # POSODABLJENO P144: 164 (P142-era) → 168 (P143: +4 — ZAMUDA SANIRANA!) → 169 (P144: +1 h82!)",
                  "BLOCKS_04455 = 185                # POSODABLJENO P149: 164 (P142-era) → 169 (P144) → 171 (P146) → 181 (P148: +10 REKORD!) → 185 (P149: +4 blokov 1920!)")
src = src.replace('len(anchors) == 164 and', 'len(anchors) == 178 and')
src = src.replace('+ ["1915", "1916", "1917"]', '+ ["1915", "1916", "1917"] + ["1919"] * 10 + ["1920"] * 4')
src = src.replace('check("I9c vitals 637 zaščita (P129)", "HOUSE_VITALS.length !== 688" in qa',
                  'check("I9c vitals 702 zaščita (P149)", "HOUSE_VITALS.length !== 702" in qa')
open(p115, "w", encoding="utf-8").write(src)
changes.append(f"{p115}: BLOCKS 171→185 · anchors 164→178 (+1919×10 +1920×4) · I9c 688→702")

# ---------- 4. BLOCKS_04455 = 185 v ostalih skriptah ----------
import glob
for f in glob.glob("scripts/p1*.py"):
    if "p115" in f:
        continue
    src = open(f, encoding="utf-8").read()
    if "BLOCKS_04455 = 185" in src:
        src = src.replace("BLOCKS_04455 = 185", "BLOCKS_04455 = 185")
        # dopolni komentar, če obstaja enovrstični
        src = re.sub(r"(BLOCKS_04455 = 185[^\n]*?)(\n)", r"\1 → 185 (P149: +4!)\2" if "P149" not in src.split("BLOCKS_04455 = 185")[0][-200:] else r"\1\2", src, count=1)
        open(f, "w", encoding="utf-8").write(src)
        changes.append(f"{f}: BLOCKS_04455 171 → 185")

# ---------- 5. tekoči I6 v p140–p148 ----------
i6_map = [
    ('qa.count("HOUSE_VITALS.length !== 688")', 'qa.count("HOUSE_VITALS.length !== 702")'),
    ('qa.count("HOUSE_VITALS.length !== 698")', 'qa.count("HOUSE_VITALS.length !== 702")'),
    ("qa.count('.length !== 171')", "qa.count('.length !== 185')"),
    ('qa.count(".length !== 171")', 'qa.count(".length !== 185")'),
    ('qa.count(".length !== 181")', 'qa.count(".length !== 185")'),
    ('"poročna sidra ≠ 164" in qa', '"poročna sidra ≠ 178" in qa'),
    ('"poročna sidra ≠ 174" in qa', '"poročna sidra ≠ 178" in qa'),
]
for f in sorted(glob.glob("scripts/p14*_parish_marriage_*.py")):
    src = open(f, encoding="utf-8").read()
    orig = src
    for old, new in i6_map:
        src = src.replace(old, new)
    # razširi stale-sete z 698/181/174 (P149-zamude)
    src = re.sub(
        r'check\("I6e ostanki ([^"]*)",\s*"HOUSE_VITALS\.length !== (687|688|698)" not in qa and "\.length !== (170|171|181)" not in qa',
        r'check("I6e ostanki \1 + P149-sanacija", "HOUSE_VITALS.length !== \2" not in qa and ".length !== \3" not in qa\n          and "HOUSE_VITALS.length !== 698" not in qa and ".length !== 181" not in qa',
        src,
    )
    if src != orig:
        open(f, "w", encoding="utf-8").write(src)
        changes.append(f"{f}: tekoči I6 → 702/185/178 + stale-seti")

print("P149-KASKADA:")
for c in changes:
    print(" •", c)
