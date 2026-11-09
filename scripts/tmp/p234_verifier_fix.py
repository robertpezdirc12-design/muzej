#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — verifier-fix: p221–p233 (in p190–p220) stale-I3/I5/I9b/I9c → aktualni (271/1923)."""
from pathlib import Path

ROOT = Path("/home/z/my-project")
files = sorted(ROOT.glob("scripts/p2*_parish*.py")) + sorted(ROOT.glob("scripts/p19*.py"))
fixed = []
for f in files:
    t = f.read_text(encoding="utf-8"); o = t
    t = t.replace("pt-luknja-201/1870 + byBook-04104", "pt-luknja-271/1923 + byBook-04104")
    t = t.replace("pt-luknja-237/1887 + byBook-04104", "pt-luknja-271/1923 + byBook-04104")
    t = t.replace("pt-luknja-254/1906 + byBook-04104", "pt-luknja-271/1923 + byBook-04104")
    t = t.replace('\'"vitalsTotal": 1870\' in pt and \'"04104": 201\' in pt', '\'"vitalsTotal": 1923\' in pt and \'"04104": 271\' in pt')
    t = t.replace('\'"vitalsTotal": 1887\' in pt and \'"04104": 237\' in pt', '\'"vitalsTotal": 1923\' in pt and \'"04104": 271\' in pt')
    t = t.replace('\'"vitalsTotal": 1889\' in pt and \'"04104": 201\' in pt', '\'"vitalsTotal": 1923\' in pt and \'"04104": 271\' in pt')
    t = t.replace('\'"vitalsTotal": 1889\' in pt and \'"04104": 254\' in pt', '\'"vitalsTotal": 1923\' in pt and \'"04104": 271\' in pt')
    t = t.replace('\'"vitalsTotal": 1906\' in pt and \'"04104": 254\' in pt', '\'"vitalsTotal": 1923\' in pt and \'"04104": 271\' in pt')
    t = t.replace("skupaj == 201", "skupaj == 271")
    t = t.replace("skupaj == 237", "skupaj == 271")
    t = t.replace("skupaj == 218", "skupaj == 271")
    t = t.replace("skupaj == 190", "skupaj == 271")
    t = t.replace("04104==201", "04104==271")
    t = t.replace("04104==237", "04104==271")
    t = t.replace("04104==218", "04104==271")
    t = t.replace('st = qa.count("HOUSE_VITALS.length !== 1870")', 'st = qa.count("HOUSE_VITALS.length !== 1923")')
    t = t.replace('st = qa.count("HOUSE_VITALS.length !== 1887")', 'st = qa.count("HOUSE_VITALS.length !== 1923")')
    t = t.replace('st = qa.count("HOUSE_VITALS.length !== 1889")', 'st = qa.count("HOUSE_VITALS.length !== 1923")')
    t = t.replace('st = qa.count("HOUSE_VITALS.length !== 1906")', 'st = qa.count("HOUSE_VITALS.length !== 1923")')
    t = t.replace("števec-1870", "števec-1923")
    t = t.replace("števec-1887", "števec-1923")
    t = t.replace("števec-1889", "števec-1923")
    t = t.replace("števec-1906", "števec-1923")
    t = t.replace("1870-številcev", "1923-številcev")
    t = t.replace("1887-številcev", "1923-številcev")
    t = t.replace("1889-številcev", "1923-številcev")
    t = t.replace("1906-številcev", "1923-številcev")
    t = t.replace('check("I3 vitals-1889 + 04104==271"', 'check("I3 vitals-1923 + 04104==271"')
    t = t.replace('check("I3 vitals-1870 + 04104==271"', 'check("I3 vitals-1923 + 04104==271"')
    t = t.replace("1887→1889→1923-sanitizacija", "1887→1923-sanitizacija")
    if t != o:
        f.write_text(t, encoding="utf-8")
        fixed.append(f.name)
print(f"verifier-fix: {len(fixed)} datotek: {fixed}")
