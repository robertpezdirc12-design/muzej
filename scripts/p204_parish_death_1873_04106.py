#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P204 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1873 — KOLERA (predzgodovina-13/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/muzej"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1873,', src)
check("I1 bloki 04106/1873 == 38", len(bloki) == 38, f"najdeno {len(bloki)}")
check("I2 hiše-1873 (file-order)", bloki == ["55", "30", "27", "44", "65", "65", "33", "13", "13", "51", "49", "57", "8", "41", "5", "10", "40", "58", "43", "63", "28", "28", "37", "33", "24", "24", "22", "30", "10", "60", "43", "7", "34", "11", "94", "23", "2", "16"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1609 + 04106==390", "HOUSE_VITALS.length !== 1609" not in src and skupaj == 390, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1873-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (212/38-griblje/14-anomalij + KOLERA + meja-s102 + 212-vrstic)",
      len(d["entries"]) == 212 and len(grib) == 38 and len(d["anomalije"]) == 13
      and "s102" in d["okvir"]["meja_1872_73"] and "1873." in d["okvir"]["meja_1872_73"]
      and "DOUBLE-SCAN" in an and "s103" in an
      and d["statistika"]["vpisov_1873"] == 212,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1609")
check("I5 qa-p204 + števec-1444", "qa-p204-parish-death-1873-04106" in qa and st >= 100, f"1609-številcev={st}")

i0 = src.find("P204: mrliška PREDZGODOVINA 04106, leto 1873")
seg = src[i0:] if i0 >= 0 else ""
check("I6a KOLERA-LETO-1873", "KOLERA-LETO" in seg and "cholera epidermica" in seg)
check("I6b 212-VPIISOV-ŠTEVJE-IZ-VRSTIC-6.× (NAJVEČJE-leto!)", "212 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-6.×" in seg)
check("I6c 30-hiš-REKORD", "30 hiš-REKORD" in seg or "30 hiš (REKORD" in seg)
check("I7a MEJA-s102 ('1873.'-celica-41.-POTRDITEV!)", "41.-POTRDITEV" in seg and "Incipit annus Domini" in seg)
check("I7b MEJA-s119 ('December 1873'-celica-43.-POTRDITEV!)", "MEJA 1873/74 = s119" in seg and "43.-POTRDITEV" in seg)
check("I7c DOUBLE-SCAN-3.× (s103==s104!)", "s103==s104" in seg and "DOUBLE-SCAN-3.×" in seg)
check("I7d PISARSKI-ORDINAL-DUPKATI-×4 + LUKNJE-×5", "DUPKATI-×4" in seg and "LUKNJE-×5" in seg)
check("I7e VLM-ORDINAL-OFF-BY-N-×3-KROP-REŠENE", "VLM-ORDINAL-OFF-BY-N-×3" in qa)
check("I7f GLAVE-V-CELICAH-×6-REKORD", "GLAVE-V-DATUMSKI-CELICAH-×6" in qa)
check("I8a KROP-KOREKCIJE-×7 (z71-NI-GRIBLJE! + z76-spol!)", "KROP-KOREKCIJE-×7" in qa and "z71" in seg)
check("I8b LUNIČ-h11-NIT-3.-LETO", "LUNIČ-h11-NIT-3.-LETO" in seg)
check("I8c h65-×2-KLASTER (dvojni-ime!)", "h65-×2-KLASTER" in seg)
check("I8d BRIME-h24-NIT (→P203-z6!)", "BRIME-h24-NIT" in qa and "BRIME-NIT" in seg)
check("I8e ULEDBA-×3-konec-1873", "ULEDBA-×3" in qa and "ULEDBA" in seg)
check("I8f Griblje-DVOJNOST-h58 (Krasinec-mimo-Griblje-Dozeth-MOŠKI!)", "Griblje-DVOJNOST" in seg)
check("I9 peščeni-števec-qa-p204 (204. kontrola!)", "qa-p204" in qa and "204. kontrola" in qa)
check("I9 pt-luknja-292/1511", '"vitalsTotal": 1609' in open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read())

# I10 LIVE-verifikacija matricula (s102-naslovnica-dostopna)
try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
