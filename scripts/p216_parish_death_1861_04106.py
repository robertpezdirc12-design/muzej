#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P216 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1861 (predzgodovina-25/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1861,', src)
check("I1 bloki 04106/1861-numeric == 10", len(bloki) == 10, f"najdeno {len(bloki)}")
check("I2 hiše-1861-numeric (file-order)", bloki == ["1", "68", "42", "42", "42", "26", "48", "18", "14", "67"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1853 + 04106==433", "HOUSE_VITALS.length !== 1853" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1861-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
cc = json.dumps(d["crossChecks"], ensure_ascii=False)
check("I4 dokaz (54/10-griblje + meja-s25-1861-letnica + 54-vrstic + vsotna-4-instance)",
      len(d["entries"]) == 54 and len(grib) == 10
      and "s25" in d["okvir"]["meja_1860_61"] and "1861" in d["okvir"]["meja_1860_61"]
      and "vsotna-letnica-marker-4-instance" in an and d["statistika"]["vpisov_1861"] == 54,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b registerjska-napaka + double-scan + KROP-ADJUDIKACIJE (crossChecks/anomalije!)",
      "registerjska-stevilcenjska-napaka-1860" in an and "s27-s26-double-scan" in an and "ADJUDIKACIJE" in cc)
check("I4c h42-klaster + pezdirc-mreza + valentin-×2 (anomalije!)",
      "h42-klaster-druzina" in an and "pezdirc-mreza-1860-1865" in an and "valentin-×2-h57-1860-tail" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1853")
check("I5 qa-p216 + števec-1600", "qa-p216-parish-death-1861-04106" in qa and st >= 125, f"1853-številcev={st}")

i0 = src.find("P216: mrliška PREDZGODOVINA 04106, leto 1861")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 54-VPIISOV-ŠTEVJE-IZ-VRSTIC-18.×", "54 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-18.×" in seg)
check("I6b REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA-NOV-TIP", "REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA" in seg)
check("I6c s27=s26-DOUBLE-SCAN-3.-v-knjigi", "DOUBLE-SCAN-3.-v-knjigi" in seg)
check("I7a MEJA-s25 (vsotna-'1861'-marker-4.-instance + '1861'-rokopisna-glava!)", "MEJA-1860/61-s25" in seg and "54.-POTRDITEV" in seg)
check("I7b VLM-margin-misreadi-KOREKCIJE (s23-+1 + z53-avgust + z20-Zemelj + z18-Mai!)", "VLM-margin-misreadi-KOREKCIJE" in seg and "'Zemelj'" in seg)
check("I7c h42-×3-APR-KLASTER (družina-HIPEZOZA!)", "h42-×3-APR-KLASTER" in seg)
check("I8a PEZDIRC-MREŽA-×5-1860–1865", "PEZDIRC-MREŽA-×5-1860–1865" in seg)
check("I8b ŽELKO-h1-nit-4.-LETO + ŠIMEC-h18-nit-GLOBLJE", "ŽELKO-h1-nit-4.-LETO" in seg and "ŠIMEC-h18-nit-GLOBLJE" in seg)
check("I8c POŽEK-h67-nit-ZADNJI-VNOS + URIH-h68-NOVA", "POŽEK-h67-nit-ZADNJI-VNOS" in seg and "URIH-h68-NOVA" in seg)
check("I8d otroška-umrljivost-50%-5/10 (NAJVIŠJA!)", "otroška-umrljivost-50%-5/10" in seg)
check("I8e VALENTIN-×2-h57-1860-tail", "VALENTIN-×2-h57-1860-tail" in seg)
check("I9a qa-p216 (216. kontrola!)", "qa-p216" in qa and "216. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-381/1600", '"vitalsTotal": 1853' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
