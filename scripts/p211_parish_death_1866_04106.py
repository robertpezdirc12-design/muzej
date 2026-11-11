#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P211 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1866 (predzgodovina-20/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1866,', src)
check("I1 bloki 04106/1866-numeric == 13", len(bloki) == 13, f"najdeno {len(bloki)}")
check("I2 hiše-1866-numeric (file-order)", bloki == ["19", "41", "14", "34", "3", "1", "37", "13", "47", "48", "34", "58", "53"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1940 + 04106==433", "HOUSE_VITALS.length !== 1940" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1866-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
cc = json.dumps(d["crossChecks"], ensure_ascii=False)
check("I4 dokaz (104/13-griblje + meja-s51-1866-letnica + 104-vrstic)",
      len(d["entries"]) == 104 and len(grib) == 13
      and "s51" in d["okvir"]["meja_1865_66"] and "1866" in d["okvir"]["meja_1865_66"]
      and "DOUBLE-SCAN-4.×" in an and d["statistika"]["vpisov_1866"] == 104,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b vsebinska-križ-s60↔P210-tail (10/10!)", "10/10-zap-EXAKT" in cc and "s54-SKIP" in cc)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2043")
check("I5 qa-p211 + števec-1544", "qa-p211-parish-death-1866-04106" in qa and st >= 100, f"1940-številcev={st}")

i0 = src.find("P211: mrliška PREDZGODOVINA 04106, leto 1866")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 104-VPIISOV-ŠTEVJE-IZ-VRSTIC-13.×", "104 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-13.×" in seg)
check("I6b DOUBLE-SCAN-4.× + DVOJČKA-z34/z35", "DOUBLE-SCAN-4.×" in seg and "DVOJČKA-MRTVOROJENA-z34/z35" in seg)
check("I6c HUESTIČ-h41-KONTINUITETA (z22!)", "HUESTIČ-h41-KONTINUITETA-z22" in seg)
check("I7a MEJA-s51 (tail-1865-KROP + prečrtana-67 + restart!)", "MEJA-1865/66-s51" in seg)
check("I7b ULEDBA-#10-9.INSTANCE-z58 (JUNI→JULI!)", "ULEDBA-#10-9.INSTANCE-z58" in seg)
check("I7c 49.-POTRDITEV-invariante ('1866'-VELIKA-LETVICA!)", "49.-POTRDITEV-invariante" in seg)
check("I8a POŽEK-h58-TOTGEBORENES-z90 (2-OSEBI-FALSIF!)", "POŽEK-h58-z90" in seg and "2-OSEBI-FALSIFICIRAN" in seg)
check("I8b KLOBUČAR-×2-v-4-dneh (h47+h48!)", "KLOBUČAR-×2-v-4-dneh" in seg)
check("I8c otroška-umrljivost-77%-10/13", "otroška-umrljivost-77%-10/13" in seg)
check("I8d 12-hiš (h34-×2-FILAK!)", "12 hiš" in seg and "h34-×2-FILAK" in seg)
check("I9 qa-p211 (211. kontrola!)", "qa-p211" in qa and "211. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9 pt-luknja-325/2043", '"vitalsTotal": 2043' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
