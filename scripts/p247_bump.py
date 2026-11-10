#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P247 — sanacija zastarelih agregatov: 1985→1990 · 242→247 · sidra 235→240
(1877:5!) · dobe 209→214 (39→44-pred-linijskih! · 47→52!) + sken-range-15–18 +
p80-1877:5-garda + qa-p247 vstavitev."""
import re

ROOT = "/home/z/my-project"
QA = f"{ROOT}/src/lib/qa-parish.ts"
delo = 0

src = open(QA, encoding="utf-8").read()
orig = src

def rep(a, b, label=""):
    global src, delo
    n = src.count(a)
    src = src.replace(a, b)
    delo += n
    print(f"  [{n}] {a[:58]} → {b[:58]} {label}")

# ——— 1. HOUSE_VITALS 1985→1990 ———
rep("HOUSE_VITALS.length !== 1985", "HOUSE_VITALS.length !== 1990")
rep("HOUSE_VITALS ≠ 1985", "HOUSE_VITALS ≠ 1990")

# ——— 2. bloki-04455 242→247 ———
rep("p80Marr.length !== 242", "p80Marr.length !== 247")
rep("p115Marr.length !== 242", "p115Marr.length !== 247")
rep("p116Marr.length !== 242", "p116Marr.length !== 247")
rep('HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 242', 'HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 247')
rep("p152Blocks.length !== 242", "p152Blocks.length !== 247")
rep("bloki 04455 ≠ 242", "bloki 04455 ≠ 247")
rep("bloki-04455 ≠ 242", "bloki-04455 ≠ 247")
rep("poročni vpisi (04455) ≠ 242", "poročni vpisi (04455) ≠ 247")
rep("195 linija (1886–1922) + 47 pred-linijskih", "195 linija (1886–1922) + 52 pred-linijskih (1877×5-P247!+1878×7+1879×9+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)")

# ——— 3. sidra 235→240 + 1877:5 gardo ———
rep("p80MarrAnchors.length !== 235", "p80MarrAnchors.length !== 240")
rep("poročna sidra ≠ 235 (1878:7-P246!", "poročna sidra ≠ 240 (1877:5-P247! · 1878:7-P246!")
a = "  p80MarrAnchors.filter((h) => h.year === 1878).length !== 7 ||"
b = "  p80MarrAnchors.filter((h) => h.year === 1877).length !== 5 ||\n" + a
if a in src and "year === 1877" not in src.split(a)[0][-300:]:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +1877:5-letni-gard")

# ——— 4. sken-range garda 1877 (s15–s18) ———
a = 'if (p80MarrAnchors.some((h) => h.year === 1878 && ((h.scan ?? 0) < 19 || (h.scan ?? 0) > 24)))'
b = ('if (p80MarrAnchors.some((h) => h.year === 1877 && ((h.scan ?? 0) < 15 || (h.scan ?? 0) > 18)))\n'
     '  p80Errors.push(`poročna sidra 1877: skeni izven 15–18 (P247: s15–s18!-najdeno: ${p80MarrAnchors.filter((h) => h.year === 1877).map((h) => h.scan).join(",")})`);\n' + a)
if a in src and "skeni izven 15–18" not in src:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +sken-range-garda-1877-s15–s18")

# ——— 5. dobe 209→214 + pred-linijskih 39→44 / 47→52 ———
rep("p152Pre !== 209 || p152Wwi !== 7 || p152Boom !== 26", "p152Pre !== 214 || p152Wwi !== 7 || p152Boom !== 26")
rep("dobe-bloki ≠ 209/7/26", "dobe-bloki ≠ 214/7/26")
rep("predvojna ≤1913 = 209 blokov", "predvojna ≤1913 = 214 blokov")
rep("39 pred-linijskih 1878-P246×7!+1879-P244×9!+1880-P243×3!+1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!", "44 pred-linijskih 1877-P247×5!+1878-P246×7!+1879-P244×9!+1880-P243×3!+1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!")
rep("47 pred-linijskih (1878×7-P246!+1879×9+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)", "52 pred-linijskih (1877×5-P247!+1878×7+1879×9+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)")

open(QA, "w", encoding="utf-8").write(src)
print(f"P247 bump: {delo} sprememb")
