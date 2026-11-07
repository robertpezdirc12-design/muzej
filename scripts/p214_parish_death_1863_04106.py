#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P214 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1863 (predzgodovina-23/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1863,', src)
check("I1 bloki 04106/1863-numeric == 7", len(bloki) == 7, f"najdeno {len(bloki)}")
check("I2 hiše-1863-numeric (file-order)", bloki == ["10", "65", "32", "18", "11", "53", "21"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1742 + 04106==433", "HOUSE_VITALS.length !== 1742" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1863-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
cc = json.dumps(d["crossChecks"], ensure_ascii=False)
check("I4 dokaz (64/7-griblje + meja-s35-1863-letnica + 64-vrstic + vsotna-letnica-marker)",
      len(d["entries"]) == 64 and len(grib) == 7
      and "s35" in d["okvir"]["meja_1862_63"] and "1863" in d["okvir"]["meja_1862_63"]
      and "vsotna-letnica-marker" in an and d["statistika"]["vpisov_1863"] == 64,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b 2×-prenoza-7/7 + KROP-VIZUALNE-ADJUDIKACIJE (crossChecks!)", "7/7" in cc and "ADJUDIKACIJE" in cc)
check("I4c z64-ULEDBA-12.×-EKSPLICITNO (anomalije!)", "z64-uledba-eksplicitno" in an and "31.-Dec-1863" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1742")
check("I5 qa-p214 + števec-1581", "qa-p214-parish-death-1863-04106" in qa and st >= 120, f"1742-številcev={st}")

i0 = src.find("P214: mrliška PREDZGODOVINA 04106, leto 1863")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 64-VPIISOV-ŠTEVJE-IZ-VRSTIC-16.×", "64 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-16.×" in seg)
check("I6b NOV-INVARIANTA-TIP-vsotna-LETNICA-MARKER + ULEDBA-EKSPLICITNO", "VSOTNA-VRSTA = LETNICA-MARKER" in seg and "EKSPLICITNI-LETNICI" in seg)
check("I6c ŠIMEC-h18-NIT-ČEZ-LETA", "ŠIMEC-h18-NIT-ČEZ-LETA" in seg)
check("I7a MEJA-s35 (vsotna-'1863'-marker + restart-z1–z8!)", "MEJA-1862/63-s35" in seg and "1|8|6|3" in seg)
check("I7b 52.-POTRDITEV-invariante ('1863'-rokopisna-glava!)", "52.-POTRDITEV-invariante" in seg)
check("I7c 7-KROP-VIZUALNIH-ADJUDIKACIJSKIH-SKUPIN", "7-KROP-VIZUALNIH-ADJUDIKACIJSKIH-SKUPIN" in seg)
check("I8a BRINC-h65-NOVA-HIŠA + unehelich", "BRINC-h65-NOVA" in seg and "unehelich" in seg)
check("I8b STRAUS-h71-korelacija + FILAK-Grem-h33", "STRAUS-h71" in seg and "FILAK-Grem-h33" in seg)
check("I8c otroška-umrljivost-29%-2/7", "otroška-umrljivost-29%-2/7" in seg)
check("I8d 7-hiš (NAJMANJ-v-predzgodovini!)", "7 hiš" in seg and "NAJMANJ-v-predzgodovini" in seg)
check("I9a qa-p214 (214. kontrola!)", "qa-p214" in qa and "214. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-362/1581", '"vitalsTotal": 1742' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
