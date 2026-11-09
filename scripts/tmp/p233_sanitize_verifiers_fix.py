#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P233-fiks — CILJNE zamenjave v verifierjih (BREZ blanket-replace!-P232-lekcija!):
1889→1923 (samo števci/pt-checks), 237→254 (04104-totals), p232-stale-1887→1923, p80-stale-1870→1923."""
from pathlib import Path
import glob

ROOT = Path("/home/z/my-project")

# --- verifierji p19x/p2xx (targeted!) ---
vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p233" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    # 1) qa-števec reference (narekovajski-kontekst!)
    t = t.replace('qa.count("HOUSE_VITALS.length !== 1889")', 'qa.count("HOUSE_VITALS.length !== 1923")')
    t = t.replace('qa.count("HOUSE_VITALS.length !== 1887")', 'qa.count("HOUSE_VITALS.length !== 1923")')
    t = t.replace('!== 1889"', '!== 1923"')
    t = t.replace('!== 1887"', '!== 1923"')
    # 2) pt-luknja vitalsTotal checks
    t = t.replace('\'"vitalsTotal": 1889\'', '\'"vitalsTotal": 1923\'')
    t = t.replace('\'"vitalsTotal": 1887\'', '\'"vitalsTotal": 1923\'')
    t = t.replace('\\"vitalsTotal\\": 1889', '\\"vitalsTotal\\": 1923')
    # 3) 04104-totals (obe formi!)
    t = t.replace('== 237', '== 254')
    t = t.replace('\'"04104": 237\'', '\'"04104": 254\'')
    # 4) detail/imena-checkov
    t = t.replace('f"1889-številcev', 'f"1923-številcev')
    t = t.replace('f"1887-številcev', 'f"1923-številcev')
    t = t.replace('števec-1889"', 'števec-1923"')
    t = t.replace('števec-1887"', 'števec-1923"')
    t = t.replace('vitals-1889', 'vitals-1923')
    t = t.replace('vitals-1887', 'vitals-1923')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-targeted-patched: {vpatched}")

# --- p80 stale-literal: len(vitals) == 1870 → 1923 ---
p80 = ROOT / "scripts/p80_parish_md_books.py"
t = p80.read_text(encoding="utf-8"); o = t
t = t.replace("and len(vitals) == 1870  # POSODABLJENO P218: 1597 (P216-stale!) → 1870",
              "and len(vitals) == 1923  # POSODABLJENO P233: 1889 (P232-stale-literal!) → 1923 (+17 blokov 04104-1873-predzgodovina — X-ARITMETIČNI-MODEL-98-VPISOV!)  # POSODABLJENO P218: 1597 (P216-stale!) → 1870")
if t != o:
    p80.write_text(t, encoding="utf-8"); print("p80-stale-literal-FIX: 1870→1923")

# --- kontrola: NIKJER več blanket-pokvarjenih '1923' na mestih-letnic ---
bad = []
for f in sorted(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True)):
    if "p233_" in f: continue
    t = Path(f).read_text(encoding="utf-8")
    for pat in ("P155-1923", "1923-okvir", "do-1923-", "†1923-", "umrl-1923"):
        if pat in t:
            bad.append((f, pat))
print("pokvarjeni-vzorci:", bad if bad else "NIČ ✓")
