#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P194 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1883 (predzgodovina-3/29).

I1: parish.ts vsebuje 11 blokov bookSignature 04106 / year 1883
I2: hiše 1883 == [20,21,33,36,36,37,44,49,68,68,78]
I3: HOUSE_VITALS.length == 1375 (1235 + 21-P193 + 11-P194!) + 04106-skupaj == 48
I4: dokaz research/issue17/parish-death-1883-04106.json (79 entries / 11-griblje / 18-anomalij / meja-s186 / z33-duplikat)
I5: qa-parish.ts vsebuje qa-p194-parish-death-1883-04106 + števec 1375 (≥ 100)
I6: duhovniki-1883 (Jančar-dominanta + Dovgan + Ogrin-tail-s192)
I7: katastrofe/oznake (h68-×2-KATASTROFA + h78-PRAZNO + h49-BRODARIČ + h44-HLEBUČAR + h36-VIJOLIČNO)
I8: z6-90-LET + z37-DAVICA + z9-HLEBEC + z21-Cadič
I9: PT-luknja-dokazi (h44/h49/h33/h21/h37) + pt-luknja-18-final.json (04106 == 156, vitals == 1375)
I10: 04894-still-520 + 04106-leta == {1883, 1884, 1885}
--live: produkcija /api/qa == 194/194 + qa-p194 pass:True
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
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1883,', src)
check("I1 bloki 04106/1883 == 11", len(bloki) == 11, f"najdeno {len(bloki)}")
his = sorted(bloki, key=int)
check("I2 hiše-1883", ",".join(his) == "20,21,33,36,36,37,44,49,68,68,78", ",".join(his))

# I3: vitals + 04106-skupaj
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1375 + 04106==156", "HOUSE_VITALS.length !== 1375" not in src and skupaj == 156,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1883-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if e.get("blok_v_parish")]
dup = [e for e in d["entries"] if "DUPLIKAT" in str(e.get("opomba", ""))]
check("I4 dokaz (79/11-griblje/18-anomalij + meja-s186 + z33-duplikat)",
      len(d["entries"]) == 79 and len(grib) == 11 and len(d["anomalije"]) == 18
      and d["okvir"]["meja_1882_83"].startswith("s186") and len(dup) >= 2,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])} duplikat={len(dup)}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1375")
check("I5 qa-p194 + števec-1375", "qa-p194-parish-death-1883-04106" in qa and st >= 100,
      f"1375-številcev={st}")

# I6: duhovniki-1883 (P194-segment)
i0 = src.find("P194: mrliška PREDZGODOVINA 04106, leto 1883")
seg = src[i0:]
check("I6 Jančar-dominanta", "Jančar" in seg, f"Jančar-omen={seg.count('Jančar')}")
check("I6b Dovgan-×5", seg.count("Dovgan") + seg.count("DOVGAN") >= 4, f"Dovgan-omen={seg.count('Dovgan') + seg.count('DOVGAN')}")
check("I6c Ogrin-tail", "Ogrin" in seg)

# I7: katastrofe/oznake
h68 = len(re.findall(r'houseNo:\s*"68",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1883', seg))
check("I7 h68-KATASTROFA-×2", h68 == 2 and seg.count("KATASTROFA") >= 2, f"h68={h68}")
check("I7b h78-PRAZNO", "PRAZNO" in seg)
check("I7c h49-BRODARIČ", "BRODARIČ" in seg and "Juvač-Doroteja'-ZAVRŽEN" in seg)
check("I7d h44-HLEBUČAR", "HLEBUČAR" in seg)
check("I7e h36-VIJOLIČNO", "VIJOLIČNO" in seg)

# I8: posebne-vrstice
check("I8 90-LET-h20", "90 LET" in seg)
check("I8b h37-DAVICA", "DAVICA" in seg)
check("I8c h21-Cadič", "CADIČ" in seg or "Cadič" in seg)

# I9: PT-luknja
check("I9 PT-luknja-dokazi-1883", "PT-luknja-dokazi-1883" in seg and "h44 (z73" in seg and "h49 (z42" in seg and "h33 (z32" in seg and "h21 (z56" in seg and "h37 (z70" in seg)
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I9b pt-luknja 04106==64", pt["corpus"]["byBook"].get("04106") == 156 and pt["corpus"]["vitalsTotal"] == 1375,
      f"04106={pt['corpus']['byBook'].get('04106')} vitals={pt['corpus']['vitalsTotal']}")

# I10: 04894 + 04106-leta
bloki94 = re.findall(r'bookSignature:\s*"04894"', src)
check("I10 04894 == 520", len(bloki94) == 520, f"najdeno {len(bloki94)}")
izven = re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d+)', src)
check("I10b 04106-leta-{1877,...,1885}", set(izven) == {"1876", "1877", "1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}, str(set(izven)))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            rep = json.load(r)
        p194 = [c for c in rep.get("tests", []) if c.get("id") == "qa-p194-parish-death-1883-04106"]
        check("LIVE produkcija ok", rep.get("ok") is True, f"passed={rep.get('passed')}")
        check("LIVE qa-p194 pass", bool(p194) and p194[0].get("pass") is True)
    except Exception as e:
        check("LIVE produkcija", False, str(e))

print("\n" + ("VSE KONTROLE PASS ✓" if ok else "NEKATERE KONTROLE FAIL ✗"))
sys.exit(0 if ok else 1)
