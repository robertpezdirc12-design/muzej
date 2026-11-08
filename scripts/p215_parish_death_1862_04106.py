#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P215 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1862 (predzgodovina-24/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1862,', src)
check("I1 bloki 04106/1862-numeric == 9", len(bloki) == 9, f"najdeno {len(bloki)}")
check("I2 hiše-1862-numeric (file-order)", bloki == ["9", "10", "61", "5", "47", "1", "63", "61", "5"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1759 + 04106==433", "HOUSE_VITALS.length !== 1759" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1862-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
cc = json.dumps(d["crossChecks"], ensure_ascii=False)
check("I4 dokaz (60/9-griblje + meja-s30-1862-letnica + 60-vrstic + vsotna-letnica-marker-3-instance)",
      len(d["entries"]) == 60 and len(grib) == 9
      and "s30" in d["okvir"]["meja_1861_62"] and "1862" in d["okvir"]["meja_1861_62"]
      and "vsotna-letnica-marker-3-instance" in an and d["statistika"]["vpisov_1862"] == 60,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b 2×-prenoza-7/7 + s32-s33-DOUBLE-SCAN + KROP-ADJUDIKACIJE (crossChecks!)",
      "7/7" in cc and "double-scan" in cc.lower() and "ADJUDIKACIJE" in cc)
check("I4c FILAK-mreža-×3 + KUNE-h10-nit + POŽEK-h67-tail (anomalije!)",
      "filak-mreza-1862" in an and "kune-h10-nit" in an and "z54-pozek-tail-1861" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1759")
check("I5 qa-p215 + števec-1590", "qa-p215-parish-death-1862-04106" in qa and st >= 125, f"1759-številcev={st}")

i0 = src.find("P215: mrliška PREDZGODOVINA 04106, leto 1862")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 60-VPIISOV-ŠTEVJE-IZ-VRSTIC-17.×", "60 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-17.×" in seg)
check("I6b NOVA-VARIANTA-brez-rokopisne-glave + vsotna-3.-instance", "NOVA-VARIANTA" in seg and "3.-INSTANCE" in seg)
check("I6c s32=s33-DOUBLE-SCAN-2.-v-knjigi", "DOUBLE-SCAN-2.-v-knjigi" in seg)
check("I7a MEJA-s30 (vsotna-'1862'-marker + restart-z1–z7!)", "MEJA-1861/62-s30" in seg and "1|8|6|2" in seg)
check("I7b KROP-zap-stolpec-DOKAZ ('1861'-glava + '49–54'-misread-korekcija!)", "KROP-zap-stolpec" in seg and "49–54" in seg)
check("I7c FILAK-MREŽA-×3-1862", "FILAK-MREŽA-×3-1862" in seg)
check("I8a KUNE-h10-nit + ŽELKO-h1-nit", "KUNE-h10-nit" in seg and "ŽELKO-h1-nit" in seg)
check("I8b KRIŽAN-h63-nit + POŽEK-h67-nit-4-LETA", "KRIŽAN-h63-nit" in seg and "POŽEK-h67-nit-4-LETA" in seg)
check("I8c otroška-umrljivost-33%-3/9", "otroška-umrljivost-33%-3/9" in seg)
check("I8d h5+h61-×2 (7 hiš!)", "h5+h61-×2" in seg)
check("I9a qa-p215 (215. kontrola!)", "qa-p215" in qa and "215. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-371/1590", '"vitalsTotal": 1759' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
