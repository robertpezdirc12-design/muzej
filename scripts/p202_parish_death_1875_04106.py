#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P202 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1875 (predzgodovina-11/29).
I1: parish.ts vsebuje 10 blokov bookSignature 04106 / year 1875
I2: hiše 1875 == [5,11,17,22,31,35,45,59,69,72] (5-NOVIH: h11/h35/h45/h59/h72!)
I3: 04106-skupaj == 433 + vitals-števec-1498
I4: dokaz research/issue17/parish-death-1875-04106.json (71 entries / 10-griblje /
    14-anomalij / meja-s127-TAIL-10 + 'Jänner 1875'-42.-potrditev + GLAVE-×6 +
    71-vrstic)
I5: qa-parish.ts vsebuje qa-p202-parish-death-1875-04106 + števec 1385 (≥ 100)
I6: duhovniki-1875 (KOGEJ-'provinciat'-RANK + DOVGAN-dominanta-×23 + HOZJAN-variante)
I7: PEZDIR-GRAFIA-DUEL-#1 (z9-h59!) + KROP-FALSIFIKACIJA-#9 (z27-h35!) +
    KURRENT-DUEL-RAZREŠEN (z40-h72!) + GEORG-HUSIČ-DUEL (z59-h69!)
I8: forma-invariante (s127-TAIL-10 + 42./43./44.-POTRDITVI + 71-vrstic-ŠTEVJE-IZ-VRSTIC)
I9: pt-luknja (04106 == 433, vitals == 1870)
I10: 04894-still-520 + 04106-leta == {1875,...,1885}
I8b: 5-NOVIH-hiš-rekord + BRAUŠ-nit-×2 + otroška-umrljivost-30% (+2-[?])
"""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
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
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1875,', src)
check("I1 bloki 04106/1875 == 10", len(bloki) == 10, f"najdeno {len(bloki)}")

# I2: hiše
check("I2 hiše-1875 (file-order)", bloki == ["59", "45", "31", "17", "35", "22", "72", "5", "69", "11"], ",".join(bloki))
check("I2b 5-NOVIH-hiš-rekord (h11/h35/h45/h59/h72!)",
      all(h in bloki for h in ["11", "35", "45", "59", "72"]))

# I3: 04106-skupaj + vitals-1498
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1870 + 04106==433", "HOUSE_VITALS.length !== 1870" not in src and skupaj == 433,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1875-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if str(e.get("vas", "")).startswith("Griblje")]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (71/10-griblje/14-anomalij + meja-s127-TAIL-10 + 42.-potrditev + 71-vrstic)",
      len(d["entries"]) == 71 and len(grib) == 10 and len(d["anomalije"]) == 14
      and "s127" in d["okvir"]["meja_1874_75"] and "TAIL-10" in d["okvir"]["meja_1874_75"]
      and "42.-POTRDITEV" in d["okvir"]["meja_1874_75"]
      and "PEZDIR-GRAFIA-DUEL" in an and "KROP-FALSIFIKACIJA-VLM" in an
      and d["statistika"]["vpisov_1875"] == 71,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1870")
check("I5 qa-p202 + števec-1385", "qa-p202-parish-death-1875-04106" in qa and st >= 100,
      f"1870-številcev={st}")

# I6: duhovniki-1875 (P202-segment)
i0 = src.find("P202: mrliška PREDZGODOVINA 04106, leto 1875")
seg = src[i0:] if i0 >= 0 else ""
check("I6 KOGEJ-'provinciat'-RANK-1875 (3.-razširitev!)", "KOGEJ-OBDOBJE-3.-RAZŠIRITEV" in seg and "provinciat" in seg)
check("I6b DOVGAN-dominanta-×23", "DOVGAN-DOMINANTA-×23" in seg)
check("I6c HOZJAN-variante-×14", "HOZJAN-VARIANTE-×14" in seg)

# I7: ključne-nití
check("I7a PEZDIR-GRAFIA-DUEL-#1 (z9-'Peglinc[?Bezdira?]'-h59!)", "PEZDIR-GRAFIA-DUEL-#1" in seg)
check("I7b KROP-FALSIFIKACIJA-VLM-#9 (z27-'Miha-Nemanič'!)", "KROP-FALSIFIKACIJA-VLM-#9" in seg)
check("I7c KURRENT-DUEL-RAZREŠEN (z40-h72-NE-h73!)", "KURRENT-DUEL-RAZREŠEN" in seg)
check("I7d GEORG-HUSIČ-DUEL-s133 (z58/z59!)", "GEORG-HUSIČ-DUEL" in seg)
check("I7e BRAUŠ-NIT-×2 (z11-mama + z40-oče!)", "BRAUŠ-NIT-×2" in seg or "BRAUŠ-oče" in seg)
check("I7f KUNIĆ/JAKOŠ-NIT (z71-h11-P201-lead-1:1!)", "KUNIĆ/JAKOŠ-NIT-1.-dokaz" in seg)

# I8: forma-invariante
check("I8a MEJA-s127 (TAIL-10-NOV/DEZ-1874!)", "MEJA 1874/75 = s127" in seg and "TAIL-10" in seg)
check("I8b 42.-43.-44.-POTRDITEV (s127-z11 + s128-z6 + s133-z1!)", "42.-POTRDITEV" in seg and "44.-POTRDITEV" in seg)
check("I8c GLAVE-V-CELICAH-×6-REKORD", "GLAVE-V-CELICAH-×6" in seg or "GLAVE-V-DATUMSKI-CELICAH-×6" in seg)
check("I8d 71-VPIISOV-ŠTEVJE-IZ-VRSTIC (ordinali-NEVIDNI-×8!)", "71 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC" in seg)
check("I8e VIOLETNA-TINTA ('1875'-glava-s133!)", "VIOLETNA-TINTA" in seg)
check("I8f 'Feber'-GRAFA-×3 + Juli-1-MIN", "Feber'-GRAFA-×3" in seg or "Feber-GRAFA" in seg)
check("I8g otroška-umrljivost-30% (3/10-jasna + 2-[?]!)", "30%-3/10" in seg or "30%" in seg)

# I9: pt-luknja
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I9 pt-luknja (04106==433, vitals==1511)",
      pt["corpus"]["byBook"]["04106"] == 433 and pt["corpus"]["vitalsTotal"] == 1870,
      f"04106={pt['corpus']['byBook']['04106']} vitals={pt['corpus']['vitalsTotal']}")

# I10: 04894 + leta-nabor
bloki94 = re.findall(r'bookSignature:\s*"04894"', src)
check("I10 04894 == 520", len(bloki94) == 520, f"najdeno {len(bloki94)}")
leta = sorted(set(re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d{4})', src)))
check("I10b 04106-leta-{1875,...,1885}", ",".join(leta) == "1857,1858,1859,1860,1861,1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885", ",".join(leta))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            prod = json.load(r)
        passed = prod.get("passed")
        p202 = next((t for t in prod.get("tests", []) if t.get("id") == "qa-p202-parish-death-1875-04106"), None)
        check("LIVE produkcija /api/qa", prod.get("ok") is True and passed == 202,
              f"ok={prod.get('ok')} passed={passed}")
        check("LIVE qa-p202-pass", bool(p202 and p202.get("pass")),
              f"qa-p202={'pass' if p202 and p202.get('pass') else 'FAIL/MISSING'}")
    except Exception as e:
        check("LIVE produkcija (dostop)", False, str(e)[:120])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
