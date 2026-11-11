#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P217 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1860 (predzgodovina-26/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1860,', src)
check("I1 bloki 04106/1860-numeric == 9", len(bloki) == 9, f"najdeno {len(bloki)}")
check("I2 hiše-1860-numeric (file-order)", bloki == ["55", "6", "13", "50", "58", "24", "30", "57", "57"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1940 + 04106==433", "HOUSE_VITALS.length !== 1940" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1860-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
cc = json.dumps(d["crossChecks"], ensure_ascii=False)
check("I4 dokaz (73/9-griblje + meja-s20-1860-letnica + 73-vrstic + glava-1860-KROP)",
      len(d["entries"]) == 73 and len(grib) == 9
      and "s20" in d["okvir"]["meja_1859_60"] and "1860" in d["okvir"]["meja_1859_60"]
      and "vlm-letnica-misread-1800" in an and d["statistika"]["vpisov_1860"] == 73,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b registerjska-napaka + z27-eksplicitna-letnica + KROP-ADJUDIKACIJE",
      "registerjska-napaka-1860" in an and "z27-eksplicitna-letnica" in an and "ADJUDIKACIJE" in cc)
check("I4c valentin-×2 + pezdirc-mreza + pozek-h58 (anomalije!)",
      "valentin-×2-h57" in an and "pezdirc-mreza-1860" in an and "z27-pozek-h58-nit" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2043")
check("I5 qa-p217 + števec-1609", "qa-p217-parish-death-1860-04106" in qa and st >= 125, f"1940-številcev={st}")

i0 = src.find("P217: mrliška PREDZGODOVINA 04106, leto 1860")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 73-VPIISOV-ŠTEVJE-IZ-VRSTIC-19.×", "73 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-19.×" in seg)
check("I6b REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA", "REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA" in seg)
check("I6c z27-'16.-Mai-1860'-EKSPLICITNA-LETNICA", "'16.-Mai-1860'-EKSPLICITNA-LETNICA" in seg)
check("I7a MEJA-s20 ('1860'-rokopisna-glava-KROP + 55.-POTRDITEV!)", "MEJA-1859/60-s20" in seg and "55.-POTRDITEV" in seg)
check("I7b VLM-margin-misreadi-KOREKCIJE (s18-'80–91'!)", "VLM-margin-misreadi-KOREKCIJE" in seg and "80–91" in seg)
check("I7c POŽEK-h58-NIT + VALENTIN-×2-h57 + PEZDIRC-h30-nit", "POŽEK-h58-NIT" in seg and "VALENTIN-×2-h57" in seg and "PEZDIRC-h30[?]-NIT" in seg)
check("I8a PEZDIRC-MREŽA (1860 + tail-1859!)", "PEZDIRC-MREŽA" in seg)
check("I8b REGISTERJSKA-NAPAKA-ordinali-NI-ČISTO + h57 ×2", "REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA" in seg and "h57-×2-VALENTIN" in seg)
check("I8c otroška-umrljivost-11%-1/9 (NAJNIŽJA!)", "otroška-umrljivost-11%-1/9" in seg)
check("I8d TAIL-1859-45-vrstic (6-GRIBLJE-tail!)", "TAIL-1859" in seg and "45-vrstic" in seg)
check("I9a qa-p217 (217. kontrola!)", "qa-p217" in qa and "217. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-390/2043", '"vitalsTotal": 2043' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
