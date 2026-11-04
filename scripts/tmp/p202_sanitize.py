#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P202 — sanitizacija: stale-števci 1375→1385 + 04106 156→166 + leta-+1875
(vzorec P201) + pt-luknja-regeneracija + skripte-kaskada."""
import glob, json
from pathlib import Path

ROOT = Path("/home/z/muzej")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")

# ——— A1: total-assertions (qa-p201 + stale bloki) ———
n1 = src.count("HOUSE_VITALS.length !== 1375")
src = src.replace("HOUSE_VITALS.length !== 1375", "HOUSE_VITALS.length !== 1385")

# ——— A2: 04106-total 156 → 166 ———
n2 = src.count('04106").length !== 156')
src = src.replace('04106").length !== 156', '04106").length !== 166')
n2b = src.count("+ P201: 20 × 1876 = 156!)")
src = src.replace(
    "+ P201: 20 × 1876 = 156!)",
    "+ P201: 20 × 1876 + P202: 10 × 1875 = 166!)",
)

# ——— A3: year-set +1875 (qa-p201-blok + stale) ———
OLD_SET = "(h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
NEW_SET = "(h.year ?? 0) !== 1875 && " + OLD_SET
n3 = src.count(OLD_SET)
src = src.replace(OLD_SET, NEW_SET)
OLD_ERR = "04106-bloki izven {1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1875 še nebrani!)"
NEW_ERR = "04106-bloki izven {1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1874 še nebrani!)"
n3b = src.count(OLD_ERR)
src = src.replace(OLD_ERR, NEW_ERR)

# ——— A4: detail-nizi ———
n4 = src.count("vitals 1375 · 04106 156 · 04894 520")
src = src.replace("vitals 1375 · 04106 156 · 04894 520", "vitals 1385 · 04106 166 · 04894 520")

QA.write_text(src, encoding="utf-8")
print(f"qa-parish.ts: total-{n1} | 04106-{n2}+{n2b} | yearset-{n3}+{n3b} | detail-{n4}")

# ——— B: skripte (1375→1385 + 04106-156→166) — p59/p199/p200/p201/p202-IZJEME ———
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True)
                   + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_")
patched = 0
for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    if "1375" not in t and "== 156" not in t and "04106==156" not in t:
        continue
    o = t
    t = t.replace("1375", "1385")
    t = t.replace('.get("04106") == 156', '.get("04106") == 166')
    t = t.replace("04106 == 156", "04106 == 166")
    t = t.replace("04106==156", "04106==166")
    t = t.replace("skupaj == 156", "skupaj == 166")
    t = t.replace('"04106") == 156', '"04106") == 166')
    t = t.replace("(04106, 156)", "(04106, 166)")
    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        patched += 1
print(f"skripte-patched: {patched}")

# ——— C: pt-luknja regeneracija ———
ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1385
pt["corpus"]["byBook"]["04106"] = 166
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P202: +10-blokov-1875 (04106 156→166, vitals 1375→1385, 5-NOVIH-hiš: h11/h35/h45/h59/h72!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: vitalsTotal={pt['corpus']['vitalsTotal']} 04106={pt['corpus']['byBook']['04106']}")
