#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P193 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1884 (predzgodovina-2/29).

I1: parish.ts vsebuje 21 blokov bookSignature 04106 / year 1884
I2: hiše 1884 == [6,8,8,8,10,13,16,17,27,43,44,47,47,49,62,63,63,64,65,69,78]
I3: HOUSE_VITALS.length == 1256 (1235 + 21-P193-1884!) + 04106-skupaj == 37
I4: dokaz research/issue17/parish-death-1884-04106.json (84 entries / 21-griblje / 16-anomalij / meja-s192)
I5: qa-parish.ts vsebuje qa-p193-parish-death-1884-04106 + števec 1256 (≥ 100)
I6: duhovniki-1884 (Peter-Ogrin-coop-dominanta ~24 + Franz-Dovgan + GLIBE-1.-PODPIS z49)
I7: katastrofe (h8-JABLKONIČ-×3 + h47-KLOBUČAR-×2 + h63-KRIŽAN-×2 + MOVRIN-×4)
I8: anomalije-oznake (DAVICA-NIT + MASERN-PRELUDE + FORME-NI-1884/Sterb-Buch + PRAZNI-polji + REWRITE-imena + dvojni-zapis + NOVA-vas-Gorice)
I9: PT-luknja-REGENERACIJA (h43/h44/h47/h49 via 04106 + pt-luknja-18-final.json 04106 == 37)
I10: 04894-still-520 + 04106-leta == {1883, 1884, 1885}
--live: produkcija /api/qa == 193/193 + qa-p193 pass:True
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
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1884,', src)
check("I1 bloki 04106/1884 == 21", len(bloki) == 21, f"najdeno {len(bloki)}")
his = sorted(bloki, key=int)
check("I2 hiše-1884", ",".join(his) == "6,8,8,8,10,13,16,17,27,43,44,47,47,49,62,63,63,64,65,69,78", ",".join(his))

# I3: vitals + 04106-skupaj
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1590 + 04106==371", "HOUSE_VITALS.length !== 1590" not in src and skupaj == 371,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1884-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if e.get("blok_v_parish")]
check("I4 dokaz (84/21-griblje/16-anomalij + meja-s192)",
      len(d["entries"]) == 84 and len(grib) == 21 and len(d["anomalije"]) == 16
      and d["okvir"]["meja_1883_84"].startswith("s192"),
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1590")
check("I5 qa-p193 + števec-1256", "qa-p193-parish-death-1884-04106" in qa and st >= 100,
      f"1256-številcev={st}")

# I6: duhovniki-1884 (samo v P193-segmentu)
i0 = src.find("P193: mrliška PREDZGODOVINA 04106, leto 1884")
seg = src[i0:]
check("I6 Ogrin-dominanta-≥24", seg.count("Peter Ogrin coop") >= 24, f"Ogrin={seg.count('Peter Ogrin coop')}")
check("I6b Franz-Dovgan", seg.count("Dovgan") + seg.count("DOVGAN") >= 10, f"Dovgan-omen={seg.count('Dovgan') + seg.count('DOVGAN')}")
check("I6c GLIBE-1.-PODPIS z49", "GLIBE-1.-PODPIS" in seg)
check("I6d Glibe-kontinuiteta-1885", "kontinuiteta-ČEZ-MEJO" in seg or "kontinuiteta-ČEZ-MEJO-KNJIG" in seg)

# I7: katastrofe
h8 = len(re.findall(r'houseNo:\s*"8",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1884', seg))
h47 = len(re.findall(r'houseNo:\s*"47",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1884', seg))
h63 = len(re.findall(r'houseNo:\s*"63",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1884', seg))
check("I7 h8-JABLKONIČ-×3", h8 == 3, f"h8={h8}")
check("I7b h47-KLOBUČAR-×2", h47 == 2, f"h47={h47}")
check("I7c h63-KRIŽAN-×2-1884", h63 == 2 and "h63 = KRIŽAN-hiša" in seg, f"h63={h63}")
check("I7d MOVRIN-katastrofa-×4", "MOVRIN" in seg)

# I8: anomalije-oznake
check("I8 DAVICA-NIT", "DAVICA-NIT" in seg)
check("I8b MASERN-PRELUDE", "MASERN-PRELUDE" in seg)
check("I8c FORME-NI-1884 (Sterb-Buch)", "FORME-NI-1884" in seg and "Sterb-Buch" in seg)
check("I8d z57-PRAZNI-polji", "PRAZNI-polji" in seg)
check("I8e z52-REWRITE-imena", "REWRITE-imena" in seg)
check("I8f dvojni-zapis-Drugoše", "dvojni-zapis" in seg)
check("I8g NOVA-vas-Gorice", "NOVA-vas" in seg and seg.count("Gorice") >= 3)

# I9: PT-luknja-REGENERACIJA
check("I9 PT-luknja-dokazi-04106", "PT-luknja-dokazi" in seg and "h43 (z46" in seg and "h44 (z48" in seg and "h47 (z27" in seg and "h49 (z62" in seg)
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I9b pt-luknja 04106==64", pt["corpus"]["byBook"].get("04106") == 371 and pt["corpus"]["vitalsTotal"] == 1590,
      f"04106={pt['corpus']['byBook'].get('04106')} vitals={pt['corpus']['vitalsTotal']}")

# I10: 04894 + 04106-leta
bloki94 = re.findall(r'bookSignature:\s*"04894"', src)
check("I10 04894 == 520", len(bloki94) == 520, f"najdeno {len(bloki94)}")
izven = re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d+)', src)
check("I10b 04106-leta-{1877,...,1885}", set(izven) == {"1862", "1863", "1864", "1865", "1866", "1867", "1868", "1869", "1870", "1871", "1872", "1873", "1874", "1875", "1876", "1877", "1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}, str(set(izven)))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            rep = json.load(r)
        p193 = [c for c in rep.get("tests", []) if c.get("id") == "qa-p193-parish-death-1884-04106"]
        check("LIVE produkcija ok", rep.get("ok") is True, f"passed={rep.get('passed')}")
        check("LIVE qa-p193 pass", bool(p193) and p193[0].get("pass") is True)
    except Exception as e:
        check("LIVE produkcija", False, str(e))

print("\n" + ("VSE KONTROLE PASS ✓" if ok else "NEKATERE KONTROLE FAIL ✗"))
sys.exit(0 if ok else 1)
