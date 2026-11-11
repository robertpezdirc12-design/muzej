#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P250 — sanacija zastarelih agregatov v qa-parish.ts:
1997→2008 · 04455 254→265 · sidra 247→258 (1874:11!) · dobe 221→232 (62-pred-linijskih!)
+ gardi 1874:11 + sken-range-2–7."""
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
    print(f"  [{n}] {a[:58]} → {b[:58]} {label}")

def repx(pat, b, label=""):
    global src, delo
    src, n = re.subn(pat, b, src)
    delo += n
    print(f"  [{n}] /{pat[:52]}/ → {b[:52]} {label}")

# ——— 1. vitals 1997→2008 (global, brez digit-sosedov) ———
repx(r"(?<!\d)1997(?!\d)", "2008", "(vitals-global!)")

# ——— 2. bloki-04455 254→265 ———
rep("bloki 04455 ≠ 254", "bloki 04455 ≠ 265")
rep("bloki-04455 ≠ 254", "bloki-04455 ≠ 265")
rep("p80Marr.length !== 254", "p80Marr.length !== 265")
rep("p115Marr.length !== 254", "p115Marr.length !== 265")
rep("p116Marr.length !== 254", "p116Marr.length !== 265")
rep("p152Blocks.length !== 254", "p152Blocks.length !== 265")
rep('HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 254',
    'HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 265')
rep("poročni vpisi (04455) ≠ 254", "poročni vpisi (04455) ≠ 265")
rep("pt-luknja-254/", "pt-luknja-265/")
repx(r"04455(?=[^)\n]{0,40}?)(?=.{0,200}?)", "04455")  # no-op varnost
rep("04455-254", "04455-265", "(narrativi!)")
rep("04455 254", "04455 265", "(narrativi!)")
rep("254 blokov 04455", "265 blokov 04455", "(narrativi!)")

# ——— 3. linija+pred-linijskih 59→70 ———
rep("195 linija (1886–1922) + 59 pred-linijskih (1875×1-P249!",
    "195 linija (1886–1922) + 70 pred-linijskih (1874×11-P250!+1875×1-P249!")

# ——— 4. sidra 247→258 + 1874:11 garda + sken-range-2–7 ———
rep("p80MarrAnchors.length !== 247", "p80MarrAnchors.length !== 258")
rep("poročna sidra ≠ 247 (1875:1-P249!", "poročna sidra ≠ 258 (1874:11-P250! · 1875:1-P249!")
rep("poročna sidra ≠ 247 (${p80MarrAnchors.length} — 246-P248 + 1-h8-1875-P249!)",
    "poročna sidra ≠ 258 (${p80MarrAnchors.length} — 247-P249 + 11-blokov-1874-P250!)")
a = "  p80MarrAnchors.filter((h) => h.year === 1875).length !== 1 ||"
b = "  p80MarrAnchors.filter((h) => h.year === 1874).length !== 11 ||\n" + a
if a in src and "year === 1874" not in src.split(a)[0][-300:]:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +1874:11-letni-gard")
a2 = 'if (p80MarrAnchors.some((h) => h.year === 1875 && ((h.scan ?? 0) < 8 || (h.scan ?? 0) > 10)))'
b2 = ('if (p80MarrAnchors.some((h) => h.year === 1874 && ((h.scan ?? 0) < 2 || (h.scan ?? 0) > 7)))\n'
      '  p80Errors.push(`poročna sidra 1874: skeni izven 2–7 (P250: s2–s7!-s1-vezalo!-najdeno: ${p80MarrAnchors.filter((h) => h.year === 1874).map((h) => h.scan).join(",")})`);\n' + a2)
if a2 in src and "skeni izven 2–7" not in src:
    src = src.replace(a2, b2, 1); delo += 1; print("  [1] +sken-range-garda-1874-s2–s7")

# ——— 5. dobe 221→232 + pred-linijskih 51→62 ———
rep("p152Pre !== 221 || p152Wwi !== 7 || p152Boom !== 26", "p152Pre !== 232 || p152Wwi !== 7 || p152Boom !== 26")
rep("dobe-bloki ≠ 221/7/26", "dobe-bloki ≠ 232/7/26")
rep("predvojna ≤1913 = 221 blokov", "predvojna ≤1913 = 232 blokov")
rep("predvojna ≤1913 vključuje 51 pred-linijskih 1875-P249×1!",
    "predvojna ≤1913 vključuje 62 pred-linijskih 1874-P250×11!+1875-P249×1!")

open(QA, "w", encoding="utf-8").write(src)
print(f"P250 bump: {delo} sprememb (dolžina {orig_len}→{len(src)})")
