#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P213 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1864 (predzgodovina-22/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1864,', src)
check("I1 bloki 04106/1864-numeric == 17", len(bloki) == 17, f"najdeno {len(bloki)}")
check("I2 hiše-1864-numeric (file-order)", bloki == ["63", "62", "19", "2", "45", "14", "3", "1", "16", "34", "18", "1", "67", "71", "5", "27", "11"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1819 + 04106==433", "HOUSE_VITALS.length !== 1819" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1864-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
cc = json.dumps(d["crossChecks"], ensure_ascii=False)
check("I4 dokaz (91/17-griblje + meja-s39-1864-letnica + 91-vrstic)",
      len(d["entries"]) == 91 and len(grib) == 17
      and "s39" in d["okvir"]["meja_1863_64"] and "1864" in d["okvir"]["meja_1863_64"]
      and "s41-shift" in an and d["statistika"]["vpisov_1864"] == 91,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b 2×-prenoza-8/8 + KROP-VIZUALNE-ADJUDIKACIJE (crossChecks!)", "8/8" in cc and "ADJUDIKACIJE" in cc)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1819")
check("I5 qa-p213 + števec-1574", "qa-p213-parish-death-1864-04106" in qa and st >= 120, f"1819-številcev={st}")

i0 = src.find("P213: mrliška PREDZGODOVINA 04106, leto 1864")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 91-VPIISOV-ŠTEVJE-IZ-VRSTIC-15.×", "91 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-15.×" in seg)
check("I6b s41-SHIFT-SANACIJA + ANOMALIJA-ne-kronološki-vnos-z85", "s41-SHIFT-SANACIJA" in seg and "ANOMALIJA-NE-KRONOLOŠKI-VNOS" in seg)
check("I6c PEZDIRC-×2-hiši (h14+h11!)", "PEZDIRC-×2-hiši" in seg)
check("I7a MEJA-s39 (vsotna-vrstica + restart-z1–z2!)", "MEJA-1863/64-s39" in seg and "vsotna-vrstica-1-8-6-4" in seg)
check("I7b 51.-POTRDITEV-invariante ('1864'-VELIKA-LETVICA-s40!)", "51.-POTRDITEV-invariante" in seg)
check("I7c 8-KROP-VIZUALNIH-ADJUDIKACIJ", "8-KROP-VIZUALNIH-ADJUDIKACIJ" in seg)
check("I8a ŽELKO-h1-×2-MAJ-klaster", "ŽELKO-h1-×2" in seg)
check("I8b FILAK-h34-3.-leto + ŠIMEC-×2-hiši", "FILAK-h34" in seg and "ŠIMEC-×2-hiši" in seg)
check("I8c otroška-umrljivost-53%-9/17", "otroška-umrljivost-53%-9/17" in seg)
check("I8d 16-hiš (h1-×2-ŽELKO!)", "16 hiš" in seg and "h1-×2-ŽELKO" in seg)
check("I9a qa-p213 (213. kontrola!)", "qa-p213" in qa and "213. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-355/1574", '"vitalsTotal": 1819' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
