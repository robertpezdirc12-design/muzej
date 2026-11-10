#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P246 — sanacija zastarelih agregatov: 1978→1985 · 235→242 · sidra 228→235
(1878:7!) · dobe 202→209 (32→39-pred-linijskih! · 40→47!) + sken-range-19–24 +
p80-1878:7-garda + qa-p246 vstavitev."""
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

# ——— 1. HOUSE_VITALS 1978→1985 ———
rep("HOUSE_VITALS.length !== 1978", "HOUSE_VITALS.length !== 1985")
rep("HOUSE_VITALS ≠ 1978", "HOUSE_VITALS ≠ 1985")

# ——— 2. bloki-04455 235→242 ———
rep("p80Marr.length !== 235", "p80Marr.length !== 242")
rep("p115Marr.length !== 235", "p115Marr.length !== 242")
rep("p116Marr.length !== 235", "p116Marr.length !== 242")
rep('HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 235', 'HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 242')
rep("p152Blocks.length !== 235", "p152Blocks.length !== 242")
rep("bloki 04455 ≠ 235", "bloki 04455 ≠ 242")
rep("bloki-04455 ≠ 235", "bloki-04455 ≠ 242")
rep("poročni vpisi (04455) ≠ 235", "poročni vpisi (04455) ≠ 242")
rep("195 linija (1886–1922) + 40 pred-linijskih", "195 linija (1886–1922) + 47 pred-linijskih (1878×7-P246!+1879×9+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)")

# ——— 3. sidra 228→235 + 1878:7 gardo ———
rep("p80MarrAnchors.length !== 228", "p80MarrAnchors.length !== 235")
rep("poročna sidra ≠ 228 (1879:9-P244!", "poročna sidra ≠ 235 (1878:7-P246! · 1879:9-P244!")
a = "  p80MarrAnchors.filter((h) => h.year === 1879).length !== 9 ||"
b = "  p80MarrAnchors.filter((h) => h.year === 1878).length !== 7 ||\n" + a
if a in src and "year === 1878" not in src.split(a)[0][-300:]:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +1878:7-letni-gard")

# ——— 4. sken-range garda 1878 (s19–s24) ———
a = 'if (p80MarrAnchors.some((h) => h.year === 1879 && ((h.scan ?? 0) < 26 || (h.scan ?? 0) > 35)))'
b = ('if (p80MarrAnchors.some((h) => h.year === 1878 && ((h.scan ?? 0) < 19 || (h.scan ?? 0) > 24)))\n'
     '  p80Errors.push(`poročna sidra 1878: skeni izven 19–24 (P246: s19–s24!-najdeno: ${p80MarrAnchors.filter((h) => h.year === 1878).map((h) => h.scan).join(",")})`);\n' + a)
if a in src and "skeni izven 19–24" not in src:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +sken-range-garda-1878-s19–s24")

# ——— 5. dobe 202→209 + pred-linijskih 32→39 / 40→47 ———
rep("p152Pre !== 202 || p152Wwi !== 7 || p152Boom !== 26", "p152Pre !== 209 || p152Wwi !== 7 || p152Boom !== 26")
rep("dobe-bloki ≠ 202/7/26", "dobe-bloki ≠ 209/7/26")
rep("predvojna ≤1913 = 202 blokov", "predvojna ≤1913 = 209 blokov")
rep("32 pred-linijskih 1879-P244×9!+1880-P243×3!+1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!", "39 pred-linijskih 1878-P246×7!+1879-P244×9!+1880-P243×3!+1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!")
rep("40 pred-linijskih (1879×9-P244!+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)", "47 pred-linijskih (1878×7-P246!+1879×9+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)")

open(QA, "w", encoding="utf-8").write(src)
print(f"P246 bump: {delo} sprememb")
