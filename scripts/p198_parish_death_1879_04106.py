#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P198 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1879 (predzgodovina-7/29;
SANACIJA-RE-RUN-usklajen!).

I1: parish.ts vsebuje 9 blokov bookSignature 04106 / year 1879
I2: hiše 1879 == [1,20,20,30,32,40,44,53,56] (h20-×2!)
I3: 04106-skupaj == 292 + vitals-števec-1511 (qa ≥ 100)
I4: dokaz research/issue17/parish-death-1879-04106.json (64 entries / 9-griblje /
    14-anomalij / meja-s158-Incipit-annus + s164-tail / 64-vrstic / sanacija!)
I5: qa-parish.ts vsebuje qa-p198-parish-death-1879-04106 + števec 1511 (≥ 100)
I6: duhovniki-1879 (Jančar-9/9-GRIBLJE-100%-5.-leto-nit + Dovžan/Dovgan-ne-Griblje)
I7: kontinuitete/oznake (h20-×2 + h56-ŠIMEC-nit + h1-nit + h53-nit + GEHIRN-×2-
    KATASTROFA-h44+h40)
I8: epidemije/oznake (FRISELN-×14-W-krivulja + z28-DUPLIKAT-3.-anomalija +
    97-LET-KORPUS-REKORD + MEJA-'Incipit-annus'-'1 8|7 9'-37.-POTRDITEV +
    ULEDBA-#10-ARBITRAŽA-A1 + KRONOLOŠKI-PRESKOKI-×2 + ARBITRAŽE-A1–A5 +
    s157-ordinali-73–82-KROP)
I9: pt-luknja-18-final.json (04106 == 292, vitals == 1511)
I10: 04894-still-520 + 04106-leta == {1879, 1880, 1881, 1882, 1883, 1884, 1885}
--live: produkcija /api/qa == 198/198 + qa-p198 pass:True
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
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1879,', src)
check("I1 bloki 04106/1879 == 9", len(bloki) == 9, f"najdeno {len(bloki)}")
his = sorted(bloki, key=int)
check("I2 hiše-1879 (h20-×2)", ",".join(his) == "1,20,20,30,32,40,44,53,56", ",".join(his))

# I3: 04106-skupaj + vitals-1511
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1511 + 04106==292", "HOUSE_VITALS.length !== 1511" not in src and skupaj == 292,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1879-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if str(e.get("vas", "")).startswith("Griblje")]
check("I4 dokaz (64/9-griblje/14-anomalij + meja-s158-Incipit + s164-tail + 64-vrstic + sanacija)",
      len(d["entries"]) == 64 and len(grib) == 9 and len(d["anomalije"]) == 14
      and "s158" in d["okvir"]["meja_1878_79"] and "Incipit annus" in d["okvir"]["meja_1878_79"]
      and d["okvir"]["meja_1879_80"].startswith("s164")
      and d["statistika"]["vpisane_vrstice"] == 64
      and "sanacija" in d and "re-clone" in d["sanacija"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1511")
check("I5 qa-p198 + števec-1511", "qa-p198-parish-death-1879-04106" in qa and st >= 100,
      f"1511-številcev={st}")

# I6: duhovniki-1879 (P198-segment)
i0 = src.find("P198: mrliška PREDZGODOVINA 04106, leto 1879")
seg = src[i0:] if i0 >= 0 else ""
check("I6 Jančar-9/9-GRIBLJE-100% (5.-leto-nit)", "9/9" in seg and "100%" in seg and "5.-leto-nit" in seg,
      f"Jančar-omen={seg.count('Jančar') + seg.count('JANČAR')}")
check("I6b Dovžan/Dovgan-ne-Griblje", "Dovžan/Dovgan" in seg or "DOVGAN" in seg or "Dovgan" in seg)

# I7: kontinuitete/oznake
h20 = len(re.findall(r'houseNo:\s*"20",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1879', seg))
check("I7 h20-×2-1879 (Pezdirc-Juni + Abramšek-Okt)", h20 == 2 and "h20-×2" in seg, f"h20={h20}")
check("I7b h56-ŠIMEC-nit (→ 1880-z19 + 1881-h18)", "ŠIMEC-nit" in seg)
check("I7c h1-nit (→ ZELŠKO-1882-P195)", "h1-nit" in seg and "ZELŠKO" in seg)
check("I7d h53-nit (z15 + tail-1878-z83-Peglavc)", "h53-nit" in seg and "Peglavc" in seg)
check("I7e GEHIRN-KATASTROFA-×2-istega-dna (h44+h40)", "GEHIRNENTZÜNDUNG-KATASTROFA-×2-ISTEGA-DNA" in seg)

# I8: epidemije/oznake
check("I8 FRISELN-×14-W-krivulja", "FRISELN-×14" in seg and "W-krivulja" in seg)
check("I8b z28-DUPLIKAT (3.-številčna-anomalija)", "z28-DUPLIKAT-1/2" in seg and "z28-DUPLIKAT-2/2" in seg
      and "3.-številčna-anomalija" in seg)
check("I8c 97-LET-KORPUS-REKORD (KROP + RE-READ)", "97 LET" in seg and "KORPUS-REKORD" in seg)
check("I8d MEJA-'Incipit-annus'+'1 8|7 9'-37.-POTRDITEV", "Incipit annus" in seg and "37.-POTRDITEV" in seg)
check("I8e ULEDBA-#10-6.-instance (ARBITRAŽA-A1)", "ULEDBA-#10-6.-INSTANCE" in seg and "Junii" in seg)
check("I8f KRONOLOŠKI-PRESKOKI-×2", "KRONOLOŠKI-PRESKOKI-×2" in seg)
check("I8g ARBITRAŽE-A1–A5 (max-zoom > VLM)", "ARBITRAŽE-A1" in seg and "max-zoom > VLM" in seg)
check("I8h s157-ordinali-73–82-KROP (1878 ≈ 85)", "73–82" in seg and "85-vpisov" in seg)
check("I8i RE-READ-SOGLASJA (tail-83/84/85 + z28-DUP)", "RE-READ-SOGLASJE" in seg)
check("I8j SANACIJA-RE-RUN (deterministična-reprodukcija)", "SANACIJA-RE-RUN" in seg and "195b4e1" in seg)

# I9: PT-luknja
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
gap_ids = sorted(int(g["houseNo"]) for g in pt["gapHouses"])
check("I9 pt-luknja 04106==292", pt["corpus"]["byBook"].get("04106") == 292 and pt["corpus"]["vitalsTotal"] == 1511,
      f"04106={pt['corpus']['byBook'].get('04106')} vitals={pt['corpus']['vitalsTotal']}")
check("I9b pt-vzorca-kontekst", 42 in gap_ids and 50 not in gap_ids, f"gap={gap_ids[:4]}...{gap_ids[-2:]}")

# I10: 04894 + 04106-leta
bloki94 = re.findall(r'bookSignature:\s*"04894"', src)
check("I10 04894 == 520", len(bloki94) == 520, f"najdeno {len(bloki94)}")
izven = re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d+)', src)
check("I10b 04106-leta-{1877,...,1885}",
      set(izven) == {"1868", "1869", "1870", "1871", "1872", "1873", "1874", "1875", "1876", "1877", "1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}, str(sorted(set(izven))))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            rep = json.load(r)
        p198 = [c for c in rep.get("tests", []) if c.get("id") == "qa-p198-parish-death-1879-04106"]
        check("LIVE produkcija ok", rep.get("ok") is True, f"passed={rep.get('passed')}")
        check("LIVE qa-p198 pass", bool(p198) and p198[0].get("pass") is True)
    except Exception as e:
        check("LIVE produkcija (napaka)", False, str(e)[:120])

print()
print(f"SKUPAJ: {'VSI-PASS ✓' if ok else 'OBSTAJAJO-FAIL ✗'}")
sys.exit(0 if ok else 1)
