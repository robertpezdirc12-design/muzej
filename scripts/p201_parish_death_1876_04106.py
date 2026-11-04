#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P201 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1876 (predzgodovina-10/29).
I1: parish.ts vsebuje 20 blokov bookSignature 04106 / year 1876
I2: hiše 1876 == [7,8,12,16,18,20,23,26,34,41,44,46,46,49,52,53,55,64,70,75] (h46-×2!)
I3: 04106-skupaj == 156 + vitals-števec-1375
I4: dokaz research/issue17/parish-death-1876-04106.json (89 entries / 20-griblje /
    16-anomalij / meja-s134-velika-'1876 Jänner' + NOVEMBER-falsifikacija + s136/s142-
    40./41.-potrditvi + December-0 + 89-vrstic)
I5: qa-parish.ts vsebuje qa-p201-parish-death-1876-04106 + števec 1375 (≥ 100)
I6: duhovniki-1876 (KOGEJ-RAZŠIRJENO-V-1876 + Dovgan-×3 + Hozjan-Capp.)
I7: PEZDINC-#8 (z22-'Perdire'-h53!) + DRAGOŠ-h12-NIT (z36!) + ŠIMEC-h18-3.-LETO (z78!)
I8: forma-invariante (s134-velika-glava + s136-z1-celica-40. + s142-z1-celica-41.)
I9: pt-luknja (04106 == 156, vitals == 1375)
I10: 04894-still-520 + 04106-leta == {1876,...,1885}
I8b: otroška-umrljivost-55% (11/20) + KRONOLOŠKA-NAPAKA-pisarja (z83-Nov-24-pred-z85-Nov-12!)
"""
import json, re, sys, urllib.request

ROOT = "/home/z/muzej"
results = []
ok = True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond:
        ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

# I1: parish.ts bloki
src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1876,', src)
check("I1 bloki 04106/1876 == 20", len(bloki) == 20, f"najdeno {len(bloki)}")

# I2: hiše
his = bloki
check("I2 hiše-1876 (file-order, h46-×2)", his == ["7", "41", "53", "46", "23", "34", "70", "26", "46", "12", "49", "20", "64", "55", "52", "18", "8", "44", "75", "16"], ",".join(his))

# I3: 04106-skupaj + vitals-1375
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1375 + 04106==156", "HOUSE_VITALS.length !== 1375" not in src and skupaj == 156,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1876-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if str(e.get("vas", "")).startswith("Griblje")]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (89/20-griblje/16-anomalij + meja-s134 + NOVEMBER-falsifikacija + December-0 + 89-vrstic)",
      len(d["entries"]) == 89 and len(grib) == 20 and len(d["anomalije"]) == 16
      and "s134" in d["okvir"]["meja_1875_76"] and "1876 Jänner" in d["okvir"]["meja_1875_76"]
      and "NOVEMBER-FALSIFIKACIJA" in an and "DECEMBER-1876 = 0" in an
      and d["statistika"]["vpisov_1876"] == 89,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1375")
check("I5 qa-p201 + števec-1375", "qa-p201-parish-death-1876-04106" in qa and st >= 100,
      f"1375-številcev={st}")

# I6: duhovniki-1876 (P201-segment)
i0 = src.find("P201: mrliška PREDZGODOVINA 04106, leto 1876")
seg = src[i0:] if i0 >= 0 else ""
check("I6 KOGEJ-OBDOBJE-RAZŠIRJENO-V-1876", "KOGEJ-OBDOBJE-RAZŠIRJENO-V-1876" in seg)
check("I6b Dovgan-×3 + Hozjan-Capp.-×2", "DOVGAN-×3" in seg and "HOZJAN" in seg)

# I7: ključne-nití
check("I7a PEZDINC-GRAFIA-#8 (z22-'Perdire'-h53!)", "PEZDINC-GRAFIA-#8" in seg)
check("I7b DRAGOŠ-h12-NIT (z36-Anton-¼J!)", "DRAGOŠ-h12-NIT" in seg)
check("I7c ŠIMEC-h18-NIT-3.-LETO (z78-'Simec'!)", "ŠIMEC-NIT-3.-LETO" in seg or "ŠIMEC-h18-NIT-3.-LETO" in seg)

# I8: forma-invariante
check("I8a MEJA-s134 (velika-'1876 Jänner'-glava + 'Jahr'-beseda!)", "1876 Jänner" in seg and "MEJA 1875/76 = s134" in seg)
check("I8b 40.-in-41.-POTRDITEV (s136-z1 + s142-z1-celici!)", "40.-in-41.-POTRDITEV" in seg)
check("I8c NOVEMBER-FALSIFIKACIJA (VLM-'Dezember'-KROP-FALSIFICIRAN!)", "NOVEMBER-FALSIFIKACIJA" in seg)
check("I8d DECEMBER-1876 = 0 (31-dnevna-vrzel!)", "DECEMBER-1876 = 0" in seg)
check("I8e 89-VPIISOV-ŠTEVJE-IZ-VRSTIC (ordinali-NEVIDNI-×9!)", "89 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC" in seg)
check("I8f otroška-umrljivost-55% (11/20!)", "55%" in seg)
check("I8g KRONOLOŠKA-NAPAKA-PISARJA (Nov-24-pred-Nov-12!)", "KRONOLOŠKA-NAPAKA-PISARJA" in seg)

# I9: pt-luknja
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I9 pt-luknja (04106==156, vitals==1375)",
      pt["corpus"]["byBook"]["04106"] == 156 and pt["corpus"]["vitalsTotal"] == 1375,
      f"04106={pt['corpus']['byBook']['04106']} vitals={pt['corpus']['vitalsTotal']}")

# I10: 04894 + leta-nabor
bloki94 = re.findall(r'bookSignature:\s*"04894"', src)
check("I10 04894 == 520", len(bloki94) == 520, f"najdeno {len(bloki94)}")
leta = sorted(set(re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d{4})', src)))
check("I10b 04106-leta-{1876,...,1885}", ",".join(leta) == "1876,1877,1878,1879,1880,1881,1882,1883,1884,1885", ",".join(leta))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            prod = json.load(r)
        passed = prod.get("passed")
        p201 = next((t for t in prod.get("tests", []) if t.get("id") == "qa-p201-parish-death-1876-04106"), None)
        check("LIVE produkcija /api/qa", prod.get("ok") is True and passed == 201,
              f"ok={prod.get('ok')} passed={passed}")
        check("LIVE qa-p201-pass", bool(p201 and p201.get("pass")),
              f"qa-p201={'pass' if p201 and p201.get('pass') else 'FAIL/MISSING'}")
    except Exception as e:
        check("LIVE produkcija (dostop)", False, str(e)[:120])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
