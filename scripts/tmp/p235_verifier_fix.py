#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P235 — verifier-fix: p221–p234 (in p190–p220) stale-I3/I5/I9b → aktualni (288/1940)."""
from pathlib import Path

ROOT = Path("/home/z/my-project")
files = sorted(ROOT.glob("scripts/p2*_parish*.py")) + sorted(ROOT.glob("scripts/p19*.py"))
fixed = []
for f in files:
    if "p235" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    t = t.replace("pt-luknja-271/1923 + byBook-04104", "pt-luknja-288/1940 + byBook-04104")
    t = t.replace('\'"vitalsTotal": 1923\' in pt and \'"04104": 271\' in pt', '\'"vitalsTotal": 1940\' in pt and \'"04104": 288\' in pt')
    t = t.replace("skupaj == 271", "skupaj == 288")
    t = t.replace("04104==271", "04104==288")
    t = t.replace('st = qa.count("HOUSE_VITALS.length !== 1923")', 'st = qa.count("HOUSE_VITALS.length !== 1940")')
    t = t.replace("števec-1923", "števec-1940")
    t = t.replace("1923-številcev", "1940-številcev")
    t = t.replace('check("I3 vitals-1923 + 04104==288"', 'check("I3 vitals-1940 + 04104==288"')
    t = t.replace("1923→1940-sanitizacija", "1923→1940-sanitizacija")
    t = t.replace("1889→1906→1923-sanitizacija", "1889→1940-sanitizacija")
    if t != o:
        f.write_text(t, encoding="utf-8")
        fixed.append(f.name)
print(f"verifier-fix: {len(fixed)} datotek: {fixed}")
