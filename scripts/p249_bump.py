#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P249 — sanacija zastarelih agregatov: 1996→1997 · 253→254 · sidra 246→247
(1875:1!) · dobe 220→221 (58→59-pred-linijskih!) + sken-range-8–10 + p80-1875:1-garda."""
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

# ——— 1. HOUSE_VITALS 1996→1997 ———
rep("HOUSE_VITALS.length !== 1996", "HOUSE_VITALS.length !== 1997")
rep("HOUSE_VITALS ≠ 1996", "HOUSE_VITALS ≠ 1997")

# ——— 2. bloki-04455 253→254 ———
rep("p80Marr.length !== 253", "p80Marr.length !== 254")
rep("poročni vpisi (04455) ≠ 253", "poročni vpisi (04455) ≠ 254")
rep("p115Marr.length !== 253", "p115Marr.length !== 254")
rep("p116Marr.length !== 253", "p116Marr.length !== 254")
rep('HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 253', 'HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 254')
rep("p152Blocks.length !== 253", "p152Blocks.length !== 254")
rep("bloki 04455 ≠ 253", "bloki 04455 ≠ 254")
rep("bloki-04455 ≠ 253", "bloki-04455 ≠ 254")
rep("195 linija (1886–1922) + 58 pred-linijskih (1876×6-P248!", "195 linija (1886–1922) + 59 pred-linijskih (1875×1-P249!+1876×6-P248!")

# ——— 3. sidra 246→247 + 1875:1 garda ———
rep("p80MarrAnchors.length !== 246", "p80MarrAnchors.length !== 247")
rep("poročna sidra ≠ 246 (1876:6-P248!", "poročna sidra ≠ 247 (1875:1-P249! · 1876:6-P248!")
rep("poročna sidra ≠ 228 (${p80MarrAnchors.length} — 219 + 9-novih-1879-P244!)", "poročna sidra ≠ 247 (${p80MarrAnchors.length} — 246-P248 + 1-h8-1875-P249!)")
a = "  p80MarrAnchors.filter((h) => h.year === 1876).length !== 6 ||"
b = "  p80MarrAnchors.filter((h) => h.year === 1875).length !== 1 ||\n" + a
if a in src and "year === 1875" not in src.split(a)[0][-300:]:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +1875:1-letni-gard")

# ——— 4. sken-range garda 1875 (s8–s10) ———
a = 'if (p80MarrAnchors.some((h) => h.year === 1876 && ((h.scan ?? 0) < 11 || (h.scan ?? 0) > 14)))'
b = ('if (p80MarrAnchors.some((h) => h.year === 1875 && ((h.scan ?? 0) < 8 || (h.scan ?? 0) > 10)))\n'
     '  p80Errors.push(`poročna sidra 1875: skeni izven 8–10 (P249: s8–s10!-najdeno: ${p80MarrAnchors.filter((h) => h.year === 1875).map((h) => h.scan).join(",")})`);\n' + a)
if a in src and "skeni izven 8–10" not in src:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +sken-range-garda-1875-s8–s10")

# ——— 5. dobe 220→221 + pred-linijskih 50→51 / 58→59 ———
rep("p152Pre !== 220 || p152Wwi !== 7 || p152Boom !== 26", "p152Pre !== 221 || p152Wwi !== 7 || p152Boom !== 26")
rep("dobe-bloki ≠ 220/7/26", "dobe-bloki ≠ 221/7/26")
rep("predvojna ≤1913 = 220 blokov", "predvojna ≤1913 = 221 blokov")
rep("predvojna ≤1913 vključuje 50 pred-linijskih 1876-P248×6!", "predvojna ≤1913 vključuje 51 pred-linijskih 1875-P249×1!+1876-P248×6!")
rep("dobe (sinteza 04455): predvojna ≤1913 = 220 blokov", "dobe (sinteza 04455): predvojna ≤1913 = 221 blokov")

open(QA, "w", encoding="utf-8").write(src)
print(f"P249 bump: {delo} sprememb (dolžina {orig_len}→{len(src)})")
