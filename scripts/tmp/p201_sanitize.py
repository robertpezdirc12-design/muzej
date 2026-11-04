#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P201 — sanitizacija: stale-števci 1355→1375 + 04106 136→156 + leta-+1876
(vzorec P200) + krstni-izjeme-RAZŠIRJENE-na-1876 (h53/h12/h18) + INSERT qa-p201 blok +
pt-luknja-regeneracija."""
import glob, json
from pathlib import Path

ROOT = Path("/home/z/muzej")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
orig = src

# ——— A1: total-assertions ———
n1 = src.count("HOUSE_VITALS.length !== 1355")
src = src.replace("HOUSE_VITALS.length !== 1355", "HOUSE_VITALS.length !== 1375")

# ——— A2: 04106-total 136 → 156 ———
n2 = src.count('04106").length !== 136')
src = src.replace('04106").length !== 136', '04106").length !== 156')
n2b = src.count("+ P200: 8 × 1877 = 136!)")
src = src.replace(
    "+ P200: 8 × 1877 = 136!)",
    "+ P200: 8 × 1877 + P201: 20 × 1876 = 156!)",
)

# ——— A3: year-set +1876 ———
OLD_SET = "(h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
NEW_SET = "(h.year ?? 0) !== 1876 && " + OLD_SET
n3 = src.count(OLD_SET)
src = src.replace(OLD_SET, NEW_SET)
OLD_ERR = "04106-bloki izven {1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1876 še nebrani!)"
NEW_ERR = "04106-bloki izven {1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1875 še nebrani!)"
n3b = src.count(OLD_ERR)
src = src.replace(OLD_ERR, NEW_ERR)

# ——— A4: detail-nizi ———
n4 = src.count("vitals 1355 · 04106 136 · 04894 520")
src = src.replace("vitals 1355 · 04106 136 · 04894 520", "vitals 1375 · 04106 156 · 04894 520")

QA.write_text(src, encoding="utf-8")
print(f"qa-parish.ts: total-{n1} | 04106-{n2}+{n2b} | yearset-{n3}+{n3b} | detail-{n4}")

# ——— B: skripte (1355→1375 + 04106-136→156) — p59/p199/p200/p201-IZJEME ———
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True)
                   + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_")
patched = 0
for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    if "1355" not in t and "== 136" not in t and "04106==136" not in t:
        continue
    o = t
    t = t.replace("1355", "1375")
    t = t.replace('.get("04106") == 136', '.get("04106") == 156')
    t = t.replace("04106 == 136", "04106 == 156")
    t = t.replace("04106==136", "04106==156")
    t = t.replace("skupaj == 136", "skupaj == 156")
    t = t.replace('"04106") == 136', '"04106") == 156')
    t = t.replace("(04106, 136)", "(04106, 156)")
    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        patched += 1
print(f"skripte-patched: {patched}")

# ——— C: pt-luknja regeneracija ———
ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1375
pt["corpus"]["byBook"]["04106"] = 156
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P201: +20-blokov-1876 (04106 136→156, vitals 1355→1375)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: vitalsTotal={pt['corpus']['vitalsTotal']} 04106={pt['corpus']['byBook']['04106']}")

# ——— D: krstni-izjeme-RAZŠIRJENE-na-1876 (h53/h12/h18) ———
IZJEME = [
    ('&& !(v.bookSignature === "04106" && v.year === 1877 && hn === "53")))',
     '&& !(v.bookSignature === "04106" && v.year === 1877 && hn === "53") && !(v.bookSignature === "04106" && v.year === 1876 && hn === "53")))',
     " // P201: + mrliška 04106-1876 h53 (z22-Maria-PERDIRE-62J-März — ★★★ PEZDINC-GRAFIA-#8! h53-NIT-babica+dojenček!)",
    ),
    ('&& !(v.bookSignature === "04106" && v.year === 1877 && hn === "12")))',
     '&& !(v.bookSignature === "04106" && v.year === 1877 && hn === "12") && !(v.bookSignature === "04106" && v.year === 1876 && hn === "12")))',
     " // P201: + mrliška 04106-1876 h12 (z36-Anton-DRAGOŠ-¼J-Mai — ★★★ DRAGOŠ-h12-NIT-1876/77! Joanes-otoka-×2!)",
    ),
    ('&& !(v.bookSignature === "04106" && v.year === 1877 && hn === "18")))',
     '&& !(v.bookSignature === "04106" && v.year === 1877 && hn === "18") && !(v.bookSignature === "04106" && v.year === 1876 && hn === "18")))',
     " // P201: + mrliška 04106-1876 h18 (z78-Maria-ŠIMEC-72¾J-Okt — ★h18-ŠIMEC-NIT-3.-LETO! 4-imena-4-leti!)",
    ),
]
n_izj = 0
for old, new, comment in IZJEME:
    if old in src:
        src = src.replace(old, new + comment, 1)
        n_izj += 1
    else:
        print(f"⚠️ izjema-NI-našel: {old[:60]}")
QA.write_text(src, encoding="utf-8")
print(f"krstni-izjeme-1876: {n_izj}/3")
