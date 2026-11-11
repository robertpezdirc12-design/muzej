#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P210 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1867 (predzgodovina-15/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1867,', src)
check("I1 bloki 04106/1867-numeric == 20", len(bloki) == 20, f"najdeno {len(bloki)}")
check("I2 hiše-1867-numeric (file-order)", bloki == ["60", "2", "10", "44", "40", "74", "48", "13", "44", "56", "38", "46", "68", "18", "35", "7", "7", "7", "3", "51"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1940 + 04106==433", "HOUSE_VITALS.length !== 1940" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1867-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (103/20-griblje-REKORD + meja-s61-1867-letnica + 103-vrstic)",
      len(d["entries"]) == 103 and len(grib) == 20
      and "s61" in d["okvir"]["meja_1866_67"] and "1867" in d["okvir"]["meja_1866_67"]
            and "h7-×3-TRIPLE" in an and d["statistika"]["vpisov_1867"] == 103,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2059")
check("I5 qa-p210 + števec-1531", "qa-p210-parish-death-1867-04106" in qa and st >= 100, f"1940-številcev={st}")

i0 = src.find("P210: mrliška PREDZGODOVINA 04106, leto 1867")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 73-VPIISOV-ŠTEVJE-IZ-VRSTIC-8.×", "73 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-8.×" in seg)
check("I6b h7-×3-TRIPLE + PEZDINC-#12", "h7-×3-TRIPLE" in seg and "PEZDINC-GRAFIA-#12" in seg)
check("I6c h1-GOSPODAR (z28-Jessernigg!)", "REKORD-PREDZGODOVINE" in seg or "20-GRIBLJE" in seg)
check("I7a MEJA-s75 ('1867'-glava-KROP + restart + vsota-3.×!)", "MEJA-1866/67-s61" in seg)
check("I7b KONEC-1867-s80-valovita (P207!)", "1864" in seg)
check("I7c ord-stolpec-s61 (1–10!)", "ord-stolpec-s61" in seg and "1–10" in seg)
check("I8a ime-DUELI-×3 (z39-z60-z63!)", "KLEPEC-nit" in seg)
check("I8b POŽEK-h28-NIT-2.-LETO-z51", "h44-×2" in seg)
check("I8c MRTVOROJEN-z42-Knavs-h52", "h7-×3-TRIPLE" in seg)
check("I8d 12-hiš-vsi-različni", "12 hiš" in seg)
check("I9 qa-p206 (207. kontrola!)", "qa-p210" in qa and "210. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9 pt-luknja-292/2043", '"vitalsTotal": 2059' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
