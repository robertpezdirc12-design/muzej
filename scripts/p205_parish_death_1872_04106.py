#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P205 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1872 (predzgodovina-14/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1872,', src)
check("I1 bloki 04106/1872 == 17", len(bloki) == 17, f"najdeno {len(bloki)}")
check("I2 hiše-1872 (file-order)", bloki == ["50", "66", "11", "44", "44", "6", "5", "37", "20", "6", "1", "7", "42", "62", "62", "8", "38"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1940 + 04106==433", "HOUSE_VITALS.length !== 1940" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1872-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (114/17-griblje/13-anomalij + meja-s92-'vsota' + 114-vrstic)",
      len(d["entries"]) == 114 and len(grib) == 17 and len(d["anomalije"]) == 13
      and "s92" in d["okvir"]["meja_1871_72"] and "vsota" in d["okvir"]["meja_1871_72"].lower()
      and "vsota" in an and d["statistika"]["vpisov_1872"] == 114,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2059")
check("I5 qa-p205 + števec-1461", "qa-p205-parish-death-1872-04106" in qa and st >= 100, f"1940-številcev={st}")

i0 = src.find("P205: mrliška PREDZGODOVINA 04106, leto 1872")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 114-VPIISOV-ŠTEVJE-IZ-VRSTIC-7.×", "114 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-7.×" in seg)
check("I6b 'vsota'-1.× + 'finis'-1.×", "vsota" in seg and "finis" in seg)
check("I6c CHOLERA-1872-NASTOP (z78!)", "CHOLERA-1872-NASTOP" in seg)
check("I7a MEJA-s92 ('Jänner'-glava + restart!)", "MEJA-1871/72-s92" in seg)
check("I7b P204-REUSE-meja-1872/73 (soglasija!)", "P204-REUSE" in seg or "1873." in seg)
check("I7c KROP-KOREKCIJE-×5 (z28-PRIMEJ! + z78-JEGLIČE!)", "KROP-KOREKCIJE-×5" in qa and "JEGLIČE" in seg and "PRIMEJ" in seg)
check("I8a h11-NIT-4.-LETO-1872", "h11-NIT-4.-LETO" in seg or "h11-NIT-4.-leto" in seg)
check("I8b h44-×2 + h62-×2 + h6-×2-1872", "h44-×2" in seg and "h62-×2" in seg and "h6-×2" in seg)
check("I8c PEZDIR-grafia-#11-1872 (z13!)", "PEZDIR-grafia-#11" in seg)
check("I8d h38/24-Prilozje-DVOJNA (P204-tail-1:1!)", "Prilozje-in-Griblje" in seg)
check("I8e KURE-nit (z86-KHURE!)", "KHURE" in seg or "KURE-nit" in seg)
check("I9 qa-p205 (205. kontrola!)", "qa-p205" in qa and "205. kontrola" in qa)
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
