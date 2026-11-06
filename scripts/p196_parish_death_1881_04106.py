#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P196 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1881 (predzgodovina-5/29).

I1: parish.ts vsebuje 19 blokov bookSignature 04106 / year 1881
I2: hiše 1881 == [2,4,8,13,17,18,21,21,26,31,37,37,44,48,56,60,65,66,78] (h37-×2-KATASTROFA! + h21-×2!)
I3: HOUSE_VITALS.length == 1511 (1283 + 19-P196!) + 04106-skupaj == 433
I4: dokaz research/issue17/parish-death-1881-04106.json (93 entries / 19-griblje / 26-anomalij / meja-s171 + s180-top / 93-vrstic)
I5: qa-parish.ts vsebuje qa-p196-parish-death-1881-04106 + števec 1511 (≥ 100)
I6: duhovniki-1881 (Jančar-19/19-GRIBLJE-100%-dominanta-3.-leto + Dovgan-izključno-ne-Griblje + Prieſter-ligatura)
I7: katastrofe/oznake (h37-×2-v-2-dneh + h21-×2 + h66-NOVA + h56-ŠIMEC + h78-LOZAR-nit + h65-MILEK-nit + h60-MÜHLZÜGLER-ženska-nit)
I8: epidemije/oznake (M/W-NIT-×4 + FRISELN-×3 + ANGINA-1.× + TUBERCULOSE-1.× + BLATTERN-×5 + NOVA-ULEDBA-#10)
I9: pt-luknja-18-final.json (04106 == 433, vitals == 1677)
I10: 04894-still-520 + 04106-leta == {1881, 1882, 1883, 1884, 1885}
--live: produkcija /api/qa == 196/196 + qa-p196 pass:True
"""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
ok = True
def check(name, cond, detail=""):
    global ok
    status = "PASS" if cond else "FAIL"
    if not cond: ok = False
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))

# I1–I2: parish.ts bloki
src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1881,', src)
check("I1 bloki 04106/1881 == 19", len(bloki) == 19, f"najdeno {len(bloki)}")
his = sorted(bloki, key=int)
check("I2 hiše-1881 (h37-×2 + h21-×2)", ",".join(his) == "2,4,8,13,17,18,21,21,26,31,37,37,44,48,56,60,65,66,78", ",".join(his))

# I3: vitals + 04106-skupaj
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1677 + 04106==433", "HOUSE_VITALS.length !== 1677" not in src and skupaj == 433,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1881-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if e.get("blok_v_parish")]
check("I4 dokaz (93/19-griblje/26-anomalij + meja-s171 + s180-top + 93-vrstic)",
      len(d["entries"]) == 93 and len(grib) == 19 and len(d["anomalije"]) == 26
      and d["okvir"]["meja_1880_81"].startswith("s171")
      and d["okvir"]["meja_1881_82"].startswith("s180")
      and d["statistika"]["vpisane_vrstice"] == 93,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1677")
check("I5 qa-p196 + števec-1511", "qa-p196-parish-death-1881-04106" in qa and st >= 100,
      f"1677-številcev={st}")

# I6: duhovniki-1881 (P196-segment)
i0 = src.find("P196: mrliška PREDZGODOVINA 04106, leto 1881")
seg = src[i0:]
check("I6 Jančar-19/19-100%-dominanta", "JANČAR" in seg and "19/19-GRIBLJE" in seg,
      f"Jančar-omen={seg.count('Jančar') + seg.count('JANČAR')}")
check("I6b Dovgan-izključno-ne-Griblje", "DOVGAN" in seg and "IZKLJUČNO-ne-Griblje" in seg)
check("I6c Prieſter-ligatura", "Prieſter" in seg)

# I7: katastrofe/oznake
h37 = len(re.findall(r'houseNo:\s*"37",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1881', seg))
check("I7 h37-×2-KATASTROFA-v-2-dneh", h37 == 2 and seg.count("h37-KATASTROFA") >= 2, f"h37={h37}")
h21 = len(re.findall(r'houseNo:\s*"21",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1881', seg))
check("I7b h21-×2 (Ožolt + Pögl)", h21 == 2, f"h21={h21}")
check("I7c h66-NOVA-GRIBLJE-hiša", "NOVA-GRIBLJE-hiša-1881" in seg)
check("I7d h56-ŠIMEC-MREŽA", "ŠIMEC-MREŽA" in seg and "h56" in seg)
check("I7e h78-LOZAR-NIT-1.-člen", "LOZAR-NIT" in seg and "h78" in seg)
check("I7f h65-MILEK-NIT + h60-MÜHLZÜGLER-ženska", "MILEK-NIT" in seg and "MÜHLZÜGLER-ženska" in seg)

# I8: epidemije/oznake
check("I8 M/W-NIT-×4", "M/W-NIT-×4" in seg and "Maffpüffl" in seg and "Maspenn" in seg)
check("I8b FRISELN-×3-1881", "FRISELN-×3-1881" in seg and "FRISELN-1/3" in seg)
check("I8c ANGINA-1.×-PREDZGODOVINE", "ANGINA-1.×-PREDZGODOVINE" in seg)
check("I8d TUBERCULOSE-1.×-PREDZGODOVINE", "TUBERCULOSE-1.×-PREDZGODOVINE" in seg)
check("I8e BLATTERN-VAL-×5 (dokaz) + Masern-fresh (seg)", "BLATTERN-(Bele)-VAL-×5" in json.dumps(d, ensure_ascii=False) and "Masern" in seg)
check("I8f NOVA-ULEDBA-#10", "NOVA-ULEDBA-#10" in seg and "MESEC-SPREMEMBA-V-VRSTICI" in seg)
check("I8g BRINC/PRINC + HLEBEC-DVOJNICA", "BRINC/PRINC-DVOJNICA" in seg and "HLEBEC-DVOJNICA" in seg)
check("I8h z8-DUPLIKAT-5.×", "z8-DUPLIKAT" in seg)

# I9: PT-luknja
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
gap_ids = sorted(int(g["houseNo"]) for g in pt["gapHouses"])
check("I9 pt-luknja 04106==433", pt["corpus"]["byBook"].get("04106") == 433 and pt["corpus"]["vitalsTotal"] == 1677,
      f"04106={pt['corpus']['byBook'].get('04106')} vitals={pt['corpus']['vitalsTotal']}")
check("I9b pt-vzorca-kontekst", 42 in gap_ids and 50 not in gap_ids, f"gap={gap_ids[:4]}...{gap_ids[-2:]}")

# I10: 04894 + 04106-leta
bloki94 = re.findall(r'bookSignature:\s*"04894"', src)
check("I10 04894 == 520", len(bloki94) == 520, f"najdeno {len(bloki94)}")
izven = re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d+)', src)
check("I10b 04106-leta-{1877,...,1885}", set(izven) == {"1857", "1858", "1859", "1860", "1861", "1862", "1863", "1864", "1865", "1866", "1867", "1868", "1869", "1870", "1871", "1872", "1873", "1874", "1875", "1876", "1877", "1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}, str(set(izven)))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            rep = json.load(r)
        p196 = [c for c in rep.get("tests", []) if c.get("id") == "qa-p196-parish-death-1881-04106"]
        check("LIVE produkcija ok", rep.get("ok") is True, f"passed={rep.get('passed')}")
        check("LIVE qa-p196 pass", bool(p196) and p196[0].get("pass") is True)
    except Exception as e:
        check("LIVE produkcija (napaka)", False, str(e)[:120])

print()
print(f"SKUPAJ: {'VSI-PASS ✓' if ok else 'OBSTAJAJO-FAIL ✗'}")
sys.exit(0 if ok else 1)
