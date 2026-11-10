#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P248 — sanacija zastarelih agregatov: 1990→1996 · 247→253 · sidra 240→246
(1876:6!) · dobe 214→220 (44→50 / 52→58-pred-linijskih!) + sken-range-11–14 +
p80-1876:6-garda + narrativi."""
import re

ROOT = "/home/z/my-project"
QA = f"{ROOT}/src/lib/qa-parish.ts"
delo = 0

src = open(QA, encoding="utf-8").read()
orig_len = len(src)

def rep(a, b, label=""):
    global src, delo
    n = src.count(a)
    src = src.replace(a, b)
    delo += n
    print(f"  [{n}] {a[:56]} → {b[:56]} {label}")

# ——— 1. HOUSE_VITALS 1990→1996 ———
rep("HOUSE_VITALS.length !== 1990", "HOUSE_VITALS.length !== 1996")
rep("HOUSE_VITALS ≠ 1990", "HOUSE_VITALS ≠ 1996")

# ——— 2. bloki-04455 247→253 ———
rep("p80Marr.length !== 247", "p80Marr.length !== 253")
rep("p115Marr.length !== 247", "p115Marr.length !== 253")
rep("p116Marr.length !== 247", "p116Marr.length !== 253")
rep('HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 247', 'HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 253')
rep("p152Blocks.length !== 247", "p152Blocks.length !== 253")
rep("bloki 04455 ≠ 247", "bloki 04455 ≠ 253")
rep("bloki-04455 ≠ 247", "bloki-04455 ≠ 253")
rep("poročni vpisi (04455) ≠ 247", "poročni vpisi (04455) ≠ 253")
rep("195 linija (1886–1922) + 52 pred-linijskih", "195 linija (1886–1922) + 58 pred-linijskih (1876×6-P248!+1877×5-P247!+1878×7+1879×9+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)")

# ——— 3. sidra 240→246 + 1876:6 gardo ———
rep("p80MarrAnchors.length !== 240", "p80MarrAnchors.length !== 246")
rep("poročna sidra ≠ 240 (1877:5-P247!", "poročna sidra ≠ 246 (1876:6-P248! · 1877:5-P247!")
a = "  p80MarrAnchors.filter((h) => h.year === 1877).length !== 5 ||"
b = "  p80MarrAnchors.filter((h) => h.year === 1876).length !== 6 ||\n" + a
if a in src and "year === 1876" not in src.split(a)[0][-300:]:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +1876:6-letni-gard")

# ——— 4. sken-range garda 1876 (s11–s14) ———
a = 'if (p80MarrAnchors.some((h) => h.year === 1877 && ((h.scan ?? 0) < 15 || (h.scan ?? 0) > 18)))'
b = ('if (p80MarrAnchors.some((h) => h.year === 1876 && ((h.scan ?? 0) < 11 || (h.scan ?? 0) > 14)))\n'
     '  p80Errors.push(`poročna sidra 1876: skeni izven 11–14 (P248: s11–s14!-najdeno: ${p80MarrAnchors.filter((h) => h.year === 1876).map((h) => h.scan).join(",")})`);\n' + a)
if a in src and "skeni izven 11–14" not in src:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +sken-range-garda-1876-s11–s14")

# ——— 5. dobe 214→220 + pred-linijskih 44→50 / 52→58 ———
rep("p152Pre !== 214 || p152Wwi !== 7 || p152Boom !== 26", "p152Pre !== 220 || p152Wwi !== 7 || p152Boom !== 26")
rep("dobe-bloki ≠ 214/7/26", "dobe-bloki ≠ 220/7/26")
rep("predvojna ≤1913 = 214 blokov", "predvojna ≤1913 = 220 blokov")
rep("44 pred-linijskih 1877-P247×5!+1878-P246×7!+1879-P244×9!+1880-P243×3!+1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!", "50 pred-linijskih 1876-P248×6!+1877-P247×5!+1878-P246×7!+1879-P244×9!+1880-P243×3!+1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!")
rep("52 pred-linijskih (1877×5-P247!+1878×7+1879×9+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)", "58 pred-linijskih (1876×6-P248!+1877×5-P247!+1878×7+1879×9+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)")

# ——— 6. h-izjeme: h44-gap-posodobitev (p152-gapa-izjema-če-obstaja) ————
# h44 je v PT-luknji 41–60 — preveri morebitno h44-gardo:
if "h44" in src and "p248" not in src:
    pass  # h44-guardi se preverijo živo prek QA

open(QA, "w", encoding="utf-8").write(src)
print(f"P248 bump: {delo} sprememb (dolžina {orig_len}→{len(src)})")
