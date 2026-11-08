#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P212 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1865 (predzgodovina-21/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1865,', src)
check("I1 bloki 04106/1865-numeric == 13", len(bloki) == 13, f"najdeno {len(bloki)}")
check("I2 hiše-1865-numeric (file-order)", bloki == ["3", "68", "23", "50", "37", "18", "37", "28", "70", "67", "32", "19", "14"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1853 + 04106==433", "HOUSE_VITALS.length !== 1853" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1865-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
cc = json.dumps(d["crossChecks"], ensure_ascii=False)
check("I4 dokaz (66/13-griblje + meja-s46-1865-letnica + 66-vrstic)",
      len(d["entries"]) == 66 and len(grib) == 13
      and "s46" in d["okvir"]["meja_1864_65"] and "1865" in d["okvir"]["meja_1864_65"]
      and "z74" in an and d["statistika"]["vpisov_1865"] == 66,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b 2×-prenoza-9/9 + z74-duel-KROP (crossChecks!)", "9/9" in cc and "74/75/76" in cc)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1853")
check("I5 qa-p212 + števec-1557", "qa-p212-parish-death-1865-04106" in qa and st >= 100, f"1853-številcev={st}")

i0 = src.find("P212: mrliška PREDZGODOVINA 04106, leto 1865")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 66-VPIISOV-ŠTEVJE-IZ-VRSTIC-14.×", "66 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-14.×" in seg)
check("I6b z74-duel-REŠEN + ANOMALIJA-pisar-mota-z13", "z74-duel-REŠEN" in seg and "ANOMALIJA-PISAR-MOTA" in seg)
check("I6c HUSIČ-h37-KLASTER (z13+z18!)", "HUSIČ-h37-KLASTER" in seg)
check("I7a MEJA-s46 (tail-1864-KROP-4-vrstice + ULEDBA-#11!)", "MEJA-1864/65-s46" in seg and "ULEDBA-#11" in seg)
check("I7b 50.-POTRDITEV-invariante ('1865'-VELIKA-LETVICA!)", "50.-POTRDITEV-invariante" in seg)
check("I7c 2×-MARIA-KRIŽAN-v-1-tednu", "2×-MARIA-KRIŽAN" in seg)
check("I8a POŽEK-nit-#2-z36 (h67!)", "POŽEK-nit-#2" in seg and "h67-NOVA-hiša-nit" in seg)
check("I8b BRINC-×2-v-2-hišah (h23+h28!)", "BRINC-×2-2-hiši" in seg)
check("I8c otroška-umrljivost-31%-4/13", "otroška-umrljivost-31%-4/13" in seg)
check("I8d 12-hiš (h37-×2-HUSIČ-klaster!)", "12 hiš" in seg and "h37-×2-HUSIČ-klaster" in seg)
check("I9a qa-p212 (212. kontrola!)", "qa-p212" in qa and "212. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-338/1557", '"vitalsTotal": 1853' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print(f"\n{'VSI-PASS' if ok else 'OBSTAJAJO-FAILI'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
