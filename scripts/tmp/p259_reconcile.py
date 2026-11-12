#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — usklajevalnik: zbere vrstična brania (full/*.json) + census (census_*.json)
v konsenz-tabelo; izpiše dvoumnosti (duel-kandidati). Pomoč pri integraciji."""
import json, os, sys

D = "/tmp/p259"

def load_json(path):
    raw = open(path).read()
    i, j = raw.find("{"), raw.rfind("}")
    try:
        return json.loads(raw[i:j+1])
    except Exception as e:
        return {"PARSE_ERR": str(e), "raw": raw[:200]}

def load_row(scan, r):
    p = f"{D}/full/{scan}_r{r}.json"
    if not os.path.exists(p):
        return None
    return load_json(p)

def census_rows(sid):
    p = f"{D}/census_{sid}.json"
    if not os.path.exists(p):
        return []
    d = load_json(p)
    return d.get("rows", [])

STRUCT = [
    ("s11", 13, "L11", "R11"),
    ("s12", 12, "L12", "R12"),
    ("s13", 11, "L13", "R13"),
]

out = {}
for scan, n, LID, RID in STRUCT:
    L = census_rows(LID)
    R = census_rows(RID)
    rows = []
    for r in range(1, n + 1):
        row = load_row(scan, r)
        lrow = L[r-1] if r <= len(L) else {}
        rrow = R[r-1] if r <= len(R) else {}
        rows.append({
            "r": r,
            "strip": row,
            "censusL": lrow,
            "censusR": rrow,
        })
    out[scan] = rows

# izpis kompaktne konsenz-tabele
for scan, rows in out.items():
    print("=" * 30, scan, "=" * 30)
    for e in rows:
        s = e["strip"]
        if not s:
            print(f"  r{e['r']}: ?? STRIP MANJKA ?? censusL: {e['censusL'].get('datum','?')} | Z: {str(e['censusL'].get('zenin','?'))[:40]} | N: {str(e['censusL'].get('nevesta','?'))[:40]}")
            continue
        if "PARSE_ERR" in s:
            print(f"  r{e['r']}: PARSE-NAPAKA {s['PARSE_ERR'][:60]}")
            continue
        print(f"  r{e['r']}: {s.get('datum','?')} | Z: {s.get('zenin','?')} [{s.get('vasZenin','?')} {s.get('hisZenin','?')}] {s.get('starZenin','?')}l | N: {s.get('nevesta','?')} [{s.get('vasNevesta','?')} {s.get('hisNevesta','?')}] {s.get('starNevesta','?')}l")
        print(f"        oZ: {str(s.get('oceZenin',''))[:50]} / {str(s.get('mataZenin',''))[:40]} | oN: {str(s.get('oceNevesta',''))[:50]} / {str(s.get('mataNevesta',''))[:40]} | priči: {str(s.get('price',''))[:60]}")
        cl = e["censusL"]
        if cl:
            print(f"        L: {cl.get('datum','?')} | Z: {str(cl.get('zenin','?'))[:44]} | N: {str(cl.get('nevesta','?'))[:44]} | rob: {cl.get('rob','')}")
        xo = s.get("xOpen") or []
        if xo:
            print(f"        xOpen: {xo}")
print("\nMANJKAJOČE STRIPI:", [f"{sc}_r{e['r']}" for sc, rows in out.items() for e in rows if not e["strip"]])
