#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P197 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1880 (predzgodovina-6/29).

I1: parish.ts vsebuje 13 blokov bookSignature 04106 / year 1880
I2: hiše 1880 == [2,5,8,10,10,18,20,21,22,27,39,42,47] (h10-×2!)
I3: 04106-skupaj == 279 + vitals-števec-1498 (qa ≥ 100)
I4: dokaz research/issue17/parish-death-1880-04106.json (71 entries / 13-griblje / 14-anomalij / meja-s164 + s171-tail / 71-vrstic)
I5: qa-parish.ts vsebuje qa-p197-parish-death-1880-04106 + števec 1498 (≥ 100)
I6: duhovniki-1880 (Jančar-naslovni-naraščaj coop.→kaplan→VRD/WRD + 12/13-GRIBLJE-92% + Dovgan-z10-izjema + Janežal-glifa)
I7: kontinuitete/oznake (h10-×2 + h2-nit + h21-hot-spot + ŠIMEC/TIMEC-DVOJNICA + KLOBUČAR-nit + PEZDIREC-nit)
I8: epidemije/oznake (FRISELN-EPIDEMIJA-×28-W-krivulja + M/W-NIT-×3-MASERN + z55-PRESKOK + VLM-LETO-MISREAD-×2-KROP + MEJA-'1880'-SPLIT-36.-POTRDITEV + ULEDBA-#10)
I9: pt-luknja-18-final.json (04106 == 279, vitals == 1498)
I10: 04894-still-520 + 04106-leta == {1880, 1881, 1882, 1883, 1884, 1885}
--live: produkcija /api/qa == 197/197 + qa-p197 pass:True
"""
import json, re, sys, urllib.request

ROOT = "/home/z/muzej"
ok = True
def check(name, cond, detail=""):
    global ok
    status = "PASS" if cond else "FAIL"
    if not cond: ok = False
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))

# I1–I2: parish.ts bloki
src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1880,', src)
check("I1 bloki 04106/1880 == 13", len(bloki) == 13, f"najdeno {len(bloki)}")
his = sorted(bloki, key=int)
check("I2 hiše-1880 (h10-×2)", ",".join(his) == "2,5,8,10,10,18,20,21,22,27,39,42,47", ",".join(his))

# I3: 04106-skupaj + vitals-1498 (parish.ts ne sme imeti starega-asserta)
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1498 + 04106==279", "HOUSE_VITALS.length !== 1498" not in src and skupaj == 279,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1880-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if e.get("blok_v_parish")]
check("I4 dokaz (71/13-griblje/14-anomalij + meja-s164 + s171-tail + 71-vrstic)",
      len(d["entries"]) == 71 and len(grib) == 13 and len(d["anomalije"]) == 14
      and d["okvir"]["meja_1879_80"].startswith("s164")
      and d["okvir"]["meja_1880_81"].startswith("s171")
      and d["statistika"]["vpisane_vrstice"] == 71,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1498")
check("I5 qa-p197 + števec-1498", "qa-p197-parish-death-1880-04106" in qa and st >= 100,
      f"1498-številcev={st}")

# I6: duhovniki-1880 (P197-segment)
i0 = src.find("P197: mrliška PREDZGODOVINA 04106, leto 1880")
seg = src[i0:] if i0 >= 0 else ""
check("I6 Jančar-naslovni-naraščaj (coop.→kaplan→VRD/WRD)",
      "JANČAR-NASLOVNI-NARAŠČAJ" in seg and "coop." in seg and "v. kaplan" in seg and "WRD" in seg,
      f"Jančar-omen={seg.count('Jančar') + seg.count('JANČAR')}")
check("I6b GRIBLJE-12/13-92%-Jančar", "12/13" in seg and "92%" in seg)
check("I6c Dovgan-z10-GRIBLJE-izjema", "Dovgan-z10-GRIBLJE-IZJEMA" in seg or "DOVGAN" in seg)
check("I6d Janežal-glifa (KURRENT-j/ž)", "Janežal" in seg)

# I7: kontinuitete/oznake
h10 = len(re.findall(r'houseNo:\s*"10",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1880', seg))
check("I7 h10-×2-1880 (Huore + Kere)", h10 == 2 and "h10-×2" in seg, f"h10={h10}")
check("I7b h2-nit (Klepec → HLEBEC-1881)", "h2-nit" in seg and "HLEBEC" in seg)
check("I7c h21-hot-spot (→ 1881-×2)", "h21-HOT-SPOT" in seg)
check("I7d ŠIMEC/TIMEC-DVOJNICA-×2", seg.count("ŠIMEC/TIMEC-DVOJNICA") >= 2)
check("I7e KLOBUČAR-nit-h47 (→ P193-1884)", "KLOBUČAR-nit" in seg and "h47" in seg)
check("I7f PEZDIREC-nit (z54 + z58)", "PEZDIREC-nit" in seg)

# I8: epidemije/oznake
check("I8 FRISELN-EPIDEMIJA-×28-W-krivulja", "FRISELN-EPIDEMIJA-×28" in seg and "W-krivulja" in seg)
check("I8b M/W-NIT-×3-MASERN (Maschukrankt-z29!)", "M/W-NIT-×3" in seg and "Maschukrankt" in seg)
check("I8c z55-PRESKOK (2.-številčna-anomalija)", "z55-IZPUŠČENA-ŠTEVILKA" in seg and "z55-PRESKOK" in seg)
check("I8d VLM-LETO-MISREAD-×2-KROP ('1859'/'1839')", "VLM-LETO-MISREAD-×2" in seg and "'1880-Novobr'" in seg)
check("I8e MEJA-'1880'-SPLIT-36.-POTRDITEV + restart-63→1", "36.-POTRDITEV-invariante" in seg and "restart-63→1" in seg)
check("I8f ULEDBA-#10 (z63-tail1879-Jänner-1)", "ULEDBA-#10" in seg)
check("I8g 1¾-leta-KROP (z66-ne-VLM)", "1¾" in seg and "KROP" in seg)

# I9: PT-luknja
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
gap_ids = sorted(int(g["houseNo"]) for g in pt["gapHouses"])
check("I9 pt-luknja 04106==279", pt["corpus"]["byBook"].get("04106") == 279 and pt["corpus"]["vitalsTotal"] == 1498,
      f"04106={pt['corpus']['byBook'].get('04106')} vitals={pt['corpus']['vitalsTotal']}")
check("I9b pt-vzorca-kontekst", 42 in gap_ids and 50 not in gap_ids, f"gap={gap_ids[:4]}...{gap_ids[-2:]}")

# I10: 04894 + 04106-leta
bloki94 = re.findall(r'bookSignature:\s*"04894"', src)
check("I10 04894 == 520", len(bloki94) == 520, f"najdeno {len(bloki94)}")
izven = re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d+)', src)
check("I10b 04106-leta-{1877,...,1885}", set(izven) == {"1869", "1870", "1871", "1872", "1873", "1874", "1875", "1876", "1877", "1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}, str(set(izven)))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            rep = json.load(r)
        p197 = [c for c in rep.get("tests", []) if c.get("id") == "qa-p197-parish-death-1880-04106"]
        check("LIVE produkcija ok", rep.get("ok") is True, f"passed={rep.get('passed')}")
        check("LIVE qa-p197 pass", bool(p197) and p197[0].get("pass") is True)
    except Exception as e:
        check("LIVE produkcija (napaka)", False, str(e)[:120])

print()
print(f"SKUPAJ: {'VSI-PASS ✓' if ok else 'OBSTAJAJO-FAIL ✗'}")
sys.exit(0 if ok else 1)
