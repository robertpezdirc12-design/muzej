#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P244 — sanacija zastarelih agregatov: 1969→1978 · 226→235 · sidra 219→228
(1879:9!) · dobe 193→202 (23→32-pred-linijskih! · 31→40!) + sken-range-27–35 +
qa-p244 vstavitev + 1886-garda-gujf."""
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

# ——— 1. HOUSE_VITALS 1969→1978 ———
rep("HOUSE_VITALS.length !== 1969", "HOUSE_VITALS.length !== 1978")
rep("HOUSE_VITALS ≠ 1969", "HOUSE_VITALS ≠ 1978")

# ——— 2. bloki-04455 226→235 ———
rep("p80Marr.length !== 226", "p80Marr.length !== 235")
rep("p115Marr.length !== 226", "p115Marr.length !== 235")
rep("p116Marr.length !== 226", "p116Marr.length !== 235")
rep('HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 226', 'HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 235')
rep("p152Blocks.length !== 226", "p152Blocks.length !== 235")
rep("bloki 04455 ≠ 226", "bloki 04455 ≠ 235")
rep("bloki-04455 ≠ 226", "bloki-04455 ≠ 235")
rep("poročni vpisi (04455) ≠ 226", "poročni vpisi (04455) ≠ 235")
rep("195 linija (1886–1922) + 31 pred-linijskih", "195 linija (1886–1922) + 40 pred-linijskih (1879×9-P244!+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)")

# ——— 3. sidra 219→228 + 1879:9 gardo ———
rep("p80MarrAnchors.length !== 219", "p80MarrAnchors.length !== 228")
rep("poročna sidra ≠ 219 (1880:3-P243!", "poročna sidra ≠ 228 (1879:9-P244! · 1880:3-P243!")
rep("poročna sidra ≠ 219 (${p80MarrAnchors.length} — 216 + 3-novih-1880-P243!)", "poročna sidra ≠ 228 (${p80MarrAnchors.length} — 219 + 9-novih-1879-P244!)")
a = "  p80MarrAnchors.filter((h) => h.year === 1880).length !== 3 ||"
b = "  p80MarrAnchors.filter((h) => h.year === 1879).length !== 9 ||\n" + a
if a in src and "year === 1879" not in src.split(a)[0][-300:]:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +1879:9-letni-gard")

# ——— 4. sken-range garda 1879 (s27–s35) ———
a = 'if (p80MarrAnchors.some((h) => h.year === 1880 && ((h.scan ?? 0) < 35 || (h.scan ?? 0) > 38)))'
b = ('if (p80MarrAnchors.some((h) => h.year === 1879 && ((h.scan ?? 0) < 27 || (h.scan ?? 0) > 35)))\n'
     '  p80Errors.push(`poročna sidra 1879: skeni izven 27–35 (P244: s27–s35!-najdeno: ${p80MarrAnchors.filter((h) => h.year === 1879).map((h) => h.scan).join(",")})`);\n' + a)
if a in src and "skeni izven 27–35" not in src:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +sken-range-garda-1879-s27–s35")

# ——— 5. dobe 193→202 + pred-linijskih 23→32 / 31→40 ———
rep("p152Pre !== 193 || p152Wwi !== 7 || p152Boom !== 26", "p152Pre !== 202 || p152Wwi !== 7 || p152Boom !== 26")
rep("dobe-bloki ≠ 193/7/26", "dobe-bloki ≠ 202/7/26")
rep("predvojna ≤1913 = 193 blokov", "predvojna ≤1913 = 202 blokov")
rep("23 pred-linijskih 1880-P243×3!+1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!", "32 pred-linijskih 1879-P244×9!+1880-P243×3!+1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!")
rep("31 pred-linijskih (1880×3-P243!+1881×9-P242!+1882×7-P241!+1883×2+1884×3+1885×7)", "40 pred-linijskih (1879×9-P244!+1880×3+1881×9+1882×7+1883×2+1884×3+1885×7)")

open(QA, "w", encoding="utf-8").write(src)
print(f"\np244_bump QA: {delo} zamenjav ✓")
