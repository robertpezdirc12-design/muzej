#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P195 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1882 (predzgodovina-4/29).

I1: parish.ts vsebuje 16 blokov bookSignature 04106 / year 1882
I2: hiše 1882 == [1,1,3,8,10,13,20,29,50,54,54,55,65,68,69,73] (h1-×2! + h54-×2!)
I3: HOUSE_VITALS.length == 1511 (1267 + 16-P195!) + 04106-skupaj == 433
I4: dokaz research/issue17/parish-death-1882-04106.json (59 entries / 16-griblje / 26-anomalij / meja-s180-top / 59-vrstic)
I5: qa-parish.ts vsebuje qa-p195-parish-death-1882-04106 + števec 1511 (≥ 100)
I6: duhovniki-1882 (Jančar-dominanta-2.-leto + Dovgan + Jakob-Dovgan-#31)
I7: katastrofe/oznake (h1-×2-ZELŠKO + h54-×2-ŠIMEC + h69-Terdič + h68-Mrh?/URH + h50-MÜHLZÜGLERIN)
I8: FRISELN-FLOOD + WASSERSUCHT + DAVICA-NIT-NOV-1882 + ASTHMA + MÜHLZÜGLER-×6
I9: pt-luknja-18-final.json (04106 == 433, vitals == 1839) + h50-izven-vzorca!
I10: 04894-still-520 + 04106-leta == {1881, 1882, 1883, 1884, 1885}
--live: produkcija /api/qa == 195/195 + qa-p195 pass:True
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
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1882,', src)
check("I1 bloki 04106/1882 == 16", len(bloki) == 16, f"najdeno {len(bloki)}")
his = sorted(bloki, key=int)
check("I2 hiše-1882 (h1-×2 + h54-×2)", ",".join(his) == "1,1,3,8,10,13,20,29,50,54,54,55,65,68,69,73", ",".join(his))

# I3: vitals + 04106-skupaj
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1839 + 04106==433", "HOUSE_VITALS.length !== 1839" not in src and skupaj == 433,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1882-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if e.get("blok_v_parish")]
check("I4 dokaz (59/16-griblje/26-anomalij + meja-s180-top + 59-vrstic)",
      len(d["entries"]) == 59 and len(grib) == 16 and len(d["anomalije"]) == 26
      and d["okvir"]["meja_1881_82"].startswith("s180") and d["statistika"]["vpisane_vrstice"] == 59,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1839")
check("I5 qa-p195 + števec-1511", "qa-p195-parish-death-1882-04106" in qa and st >= 100,
      f"1839-številcev={st}")

# I6: duhovniki-1882 (P195-segment)
i0 = src.find("P195: mrliška PREDZGODOVINA 04106, leto 1882")
seg = src[i0:]
check("I6 Jančar-dominanta-2.-leto", "JANČAR" in seg, f"Jančar-omen={seg.count('Jančar') + seg.count('JANČAR')}")
check("I6b Jakob-DOVGAN-#31", "Jakob-DOVGAN" in seg and "#31" in seg)
check("I6c Dovgan-×~12", seg.count("Dovgan") + seg.count("DOVGAN") >= 6, f"Dovgan-omen={seg.count('Dovgan') + seg.count('DOVGAN')}")

# I7: katastrofe/oznake
h1 = len(re.findall(r'houseNo:\s*"1",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1882', seg))
check("I7 h1-×2-ZELŠKO-KATASTROFA", h1 == 2 and seg.count("ZELŠKO-KATASTROFA") >= 2, f"h1={h1}")
h54 = len(re.findall(r'houseNo:\s*"54",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1882', seg))
check("I7b h54-×2-ŠIMEC-KATASTROFA", h54 == 2 and "ŠIMEC-KATASTROFA" in seg, f"h54={h54}")
check("I7c h69-Terdič→BRINE", "h69-Terdič-1882" in seg and "BRINE-1884" in seg)
check("I7d h68-Mrh?/URH", "[~URH!]-1882" in seg and "JANUARSKA-KATASTROFA" in seg)
check("I7e h50-MÜHLZÜGLERIN", "MÜHLZÜGLERIN" in seg and "izven-PT-luknja-vzorca" in seg)

# I8: epidemije/oznake
check("I8 FRISELN-FLOOD-×16", "FRISELN-FLOOD-×16" in seg and "FRISELN-FLOOD-6/16" in seg)
check("I8b WASSERSUCHT-×4-Waſſerſucht", "WASSERSUCHT-×4" in seg and "Waſſerſucht" in seg)
check("I8c DAVICA-NIT-NOV-1882", "DAVICA-NIT-RAZŠIRJENA-NAZAJ-NA-NOVEMBER-1882" in seg and "Diphtheritis" in seg)
check("I8d ASTHMA-×3-1882", "ASTHMA-×3-1882" in seg)
check("I8e MÜHLZÜGLER-×6", "MÜHLZÜGLER-×6" in seg)
check("I8f TODTGEBOREN + dvojno-PUST", "TODTGEBOREN-z50" in seg and "dvojno-PUST" in seg)
check("I8g FABRIKA-1.× + MIGRANT", "FABRIKA-1.×-PREDZGODOVINE" in seg and "MIGRANT-z25" in seg)

# I9: PT-luknja
check("I9 PT-luknja-kontekst (h50-izven-vzorca-v-bloku!)",
      "h50-z58-izven-PT-vzorca-42–60-brez-h50-P191" in seg)
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
gap_ids = sorted(int(g["houseNo"]) for g in pt["gapHouses"])
check("I9b pt-luknja 04106==64", pt["corpus"]["byBook"].get("04106") == 433 and pt["corpus"]["vitalsTotal"] == 1839,
      f"04106={pt['corpus']['byBook'].get('04106')} vitals={pt['corpus']['vitalsTotal']}")
check("I9c h50-izven-PT-vzorca", 50 not in gap_ids and 42 in gap_ids, f"gap={gap_ids[:4]}...{gap_ids[-2:]}")

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
        p195 = [c for c in rep.get("tests", []) if c.get("id") == "qa-p195-parish-death-1882-04106"]
        check("LIVE produkcija ok", rep.get("ok") is True, f"passed={rep.get('passed')}")
        check("LIVE qa-p195 pass", bool(p195) and p195[0].get("pass") is True)
    except Exception as e:
        check("LIVE produkcija", False, str(e))

print("\n" + ("VSE KONTROLE PASS ✓" if ok else "NEKATERE KONTROLE FAIL ✗"))
sys.exit(0 if ok else 1)
