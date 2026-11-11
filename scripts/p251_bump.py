#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P251 — sanacija zastarelih agregatov v qa-parish.ts:
2008→2012 · 04455 265→269 · sidra 258→262 (1873:4!) · dobe 232→236 (66-pred-linijskih!)
+ garda 1873:4 + sken-garda-1873 (s2!) + p85-izjeme-04455-1873."""
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

# ——— 1. vitals 2008→2012 (global, brez digit-sosedov) ———
repx(r"(?<!\d)2008(?!\d)", "2012", "(vitals-global!)")

# ——— 2. bloki-04455 265→269 ———
rep("bloki 04455 ≠ 265", "bloki 04455 ≠ 269")
rep("bloki-04455 ≠ 265", "bloki-04455 ≠ 269")
rep("p80Marr.length !== 265", "p80Marr.length !== 269")
rep("p115Marr.length !== 265", "p115Marr.length !== 269")
rep("p116Marr.length !== 265", "p116Marr.length !== 269")
rep("p152Blocks.length !== 265", "p152Blocks.length !== 269")
rep('HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 265',
    'HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 269')
rep("poročni vpisi (04455) ≠ 265", "poročni vpisi (04455) ≠ 269")
rep("pt-luknja-265/", "pt-luknja-269/")
rep("04455-265", "04455-269", "(narrativi!)")
rep("04455 265", "04455 269", "(narrativi!)")
rep("265 blokov 04455", "269 blokov 04455", "(narrativi!)")

# ——— 3. linija+pred-linijskih 70→74 ———
rep("195 linija (1886–1922) + 70 pred-linijskih (1874×11-P250!+1875×1-P249!",
    "195 linija (1886–1922) + 74 pred-linijskih (1873×4-P251!+1874×11-P250!+1875×1-P249!")

# ——— 4. sidra 258→262 + 1873:4 garda + sken-garda-1873 (s2!) ———
rep("p80MarrAnchors.length !== 258", "p80MarrAnchors.length !== 262")
rep("poročna sidra ≠ 258 (1874:11-P250!", "poročna sidra ≠ 262 (1873:4-P251! · 1874:11-P250!")
rep("poročna sidra ≠ 258 (${p80MarrAnchors.length} — 258-P250", "poročna sidra ≠ 262 (${p80MarrAnchors.length} — 258-P250")
a = "  p80MarrAnchors.filter((h) => h.year === 1874).length !== 11 ||"
b = "  p80MarrAnchors.filter((h) => h.year === 1873).length !== 4 ||\n" + a
if a in src and "year === 1873" not in src.split(a)[0][-400:]:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +1873:4-letni-gard")
a2 = 'if (p80MarrAnchors.some((h) => h.year === 1874 && ((h.scan ?? 0) < 2 || (h.scan ?? 0) > 7)))'
b2 = ('if (p80MarrAnchors.some((h) => h.year === 1873 && (h.scan ?? 0) !== 2))\n'
      '  p80Errors.push(`poročna sidra 1873: sken ≠ 2 (P251: samo-s2-Pag.-1!-s1-vezalo!-najdeno: ${p80MarrAnchors.filter((h) => h.year === 1873).map((h) => h.scan).join(",")})`);\n' + a2)
if a2 in src and "sken ≠ 2" not in src:
    src = src.replace(a2, b2, 1); delo += 1; print("  [1] +sken-garda-1873-s2")

# ——— 5. dobe 232→236 + pred-linijskih 62→66 ———
rep("p152Pre !== 232 || p152Wwi !== 7 || p152Boom !== 26", "p152Pre !== 236 || p152Wwi !== 7 || p152Boom !== 26")
rep("dobe-bloki ≠ 232/7/26", "dobe-bloki ≠ 236/7/26")
rep("predvojna ≤1913 = 232 blokov", "predvojna ≤1913 = 236 blokov")
rep("predvojna ≤1913 vključuje 62 pred-linijskih 1874-P250×11!+1875-P249×1!",
    "predvojna ≤1913 vključuje 66 pred-linijskih 1873-P251×4!+1874-P250×11!+1875-P249×1!")

# ——— 6. p85-izjeme-04455-1873 (h13/h22/h50/h62 — 6–25 let pred prvencem!) ———
old = '&& !(v.bookSignature === "04455" && v.year === 1874 && (hn === "7" || hn === "30"))'
new = '&& !(v.bookSignature === "04455" && v.year === 1873 && (hn === "13" || hn === "22" || hn === "50" || hn === "62")) && !(v.bookSignature === "04455" && v.year === 1874 && (hn === "7" || hn === "30"))'
rep(old, new, "(p85-izjema-04455-1873!)")
old2 = '&& !(v.bookSignature === "04455" && v.year === 1874 && (hn === "10" || hn === "43"))'
new2 = '&& !(v.bookSignature === "04455" && v.year === 1873 && (hn === "13" || hn === "22" || hn === "50" || hn === "62")) && !(v.bookSignature === "04455" && v.year === 1874 && (hn === "10" || hn === "43"))'
rep(old2, new2, "(p92-izjema-04455-1873!)")

open(QA, "w", encoding="utf-8").write(src)
print(f"P251 bump: {delo} sprememb (dolžina {orig_len}→{len(src)})")
