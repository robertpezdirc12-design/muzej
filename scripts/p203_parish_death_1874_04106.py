#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P203 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1874 (predzgodovina-12/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/muzej"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1874,', src)
check("I1 bloki 04106/1874 == 21", len(bloki) == 21, f"najdeno {len(bloki)}")
check("I2 hiše-1874 (file-order)", bloki == ["11", "24", "28", "69", "55", "64", "72", "86", "39", "69", "21", "48", "6", "33", "72", "36", "64", "38", "57", "19", "29"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1498 + 04106==279", "HOUSE_VITALS.length !== 1498" not in src and skupaj == 279, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1874-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (94/21-griblje/14-anomalij + LEKCIJA-#21 + meja-s119 + 94-vrstic)",
      len(d["entries"]) == 94 and len(grib) == 21 and len(d["anomalije"]) == 14
      and "s119" in d["okvir"]["meja_1873_74"] and "18 74. Jänner" in d["okvir"]["meja_1873_74"]
      and "DOUBLE-SCAN" in an and "s125" in an
      and d["statistika"]["vpisov_1874"] == 94,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1498")
check("I5 qa-p203 + števec-1406", "qa-p203-parish-death-1874-04106" in qa and st >= 100, f"1498-številcev={st}")

i0 = src.find("P203: mrliška PREDZGODOVINA 04106, leto 1874")
seg = src[i0:] if i0 >= 0 else ""
check("I6 KOGEJ-'provisorium'-1874 (NIT-4.-LETO!)", "provisorium KOGEJ" in seg and "KOGEJ-NIT-4.-LETO" in seg)
check("I6b DOVGAN-nit-×6", "DOVGAN-nit" in seg)
check("I7a KRIŽAN-h33-POPRAVEK (ne-h83!)", "h83-VLM-POPRAVEK→h33" in seg)
check("I7b LOGAR-h57-POPRAVEK (ne-h8!)", "h57-POPRAVEK" in seg or "NE-h8" in seg)
check("I7c TILAK-h39 (s123==s124-DVOSCAN!)", "s123==s124-DVOSCAN" in seg)
check("I7d MRTVOROJEN-h72 (Krajnc-vs-Janec!)", "MRTVOROJEN" in seg and "Krajnc-vs-Janec" in seg)
check("I7e BRIME-×2-v-5-TEDNIH (h24/h28!)", "BRIME-1/2-×2-v-5-TEDNIH" in seg)
check("I7f LUNIČ-h11-KUNIĆ-NIT", "h11-KUNIĆ-hiša-NIT" in seg)
check("I8a MEJA-s119 (VELIKA-'18 74. Jänner'-split!)", "MEJA 1873/74 = s119" in seg and "18 74. Jänner" in seg)
check("I8b 45.-46.-POTRDITEV (s122-z1-Mai + s125-z1-September!)", "45.-in-46.-POTRDITEV" in seg)
check("I8c VLM-FALSIFIKACIJE-×3 (s125-'Jänner'-×13 + s122-'1877' + 'Incipit'!)", "VLM-FALSIFIKACIJE-×3" in seg)
check("I8d LEKCIJA-#21 (natisnjene-št.-strani-×7 + DVOSCAN!)", "LEKCIJA-#21" in seg and "pag-118-×2" in seg)
check("I8e 94-VPIISOV-ŠTEVJE-IZ-VRSTIC-5.×", "94 vpisov" in seg and "s123-DUPLIKAT-IZPUŠČEN" in seg)
check("I8f KROP-POPRAVKI-hišnih-št.-×5", "KROP-POPRAVKI-hišnih-št.-×5" in seg)
check("I8g otroška-umrljivost-33% (7/21!)", "33%" in seg)

pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I9 pt-luknja (04106==279, vitals==1406)",
      pt["corpus"]["byBook"]["04106"] == 279 and pt["corpus"]["vitalsTotal"] == 1498,
      f"04106={pt['corpus']['byBook']['04106']} vitals={pt['corpus']['vitalsTotal']}")
bloki94 = re.findall(r'bookSignature:\s*"04894"', src)
check("I10 04894 == 520", len(bloki94) == 520, f"najdeno {len(bloki94)}")
leta = sorted(set(re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d{4})', src)))
check("I10b 04106-leta-{1874,...,1885}", ",".join(leta) == "1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885", ",".join(leta))

if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            prod = json.load(r)
        p203 = next((t for t in prod.get("tests", []) if t.get("id") == "qa-p203-parish-death-1874-04106"), None)
        check("LIVE produkcija /api/qa", prod.get("ok") is True and prod.get("passed") == 203, f"passed={prod.get('passed')}")
        check("LIVE qa-p203-pass", bool(p203 and p203.get("pass")))
    except Exception as e:
        check("LIVE produkcija (dostop)", False, str(e)[:120])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
