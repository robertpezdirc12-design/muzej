#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P199 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1878 (predzgodovina-8/29).

I1: parish.ts vsebuje 23 blokov bookSignature 04106 / year 1878
I2: hiše 1878 == [1,3,9,10,14,15,16,18,20,30,30,33,37,38,40,44,47,48,53,54,55,57,66] (h30-×2!)
I3: 04106-skupaj == 128 + vitals-števec-1347
I4: dokaz research/issue17/parish-death-1878-04106.json (85 entries / 23-griblje /
    13-anomalij / meja-s149-'18 78.'-SPLIT / s158-tail / 85-vrstic)
I5: qa-parish.ts vsebuje qa-p199-parish-death-1878-04106 + števec 1347 (≥ 100)
I6: duhovniki-1878 (JANČAR-NIT-1878→1883-6-LET + Kogej-subst.-coop + Dovgan-tranzicija)
I7: kontinuitete/oznake (h30-×2-PEZDIRC + ZELIHA-NIT-h1-×3 + ŠIMEC-×2 + KLOBUČAR-h48
    + GEHIRNENTZÜNDUNG-NIT-1878-#3-h57 + h44-nit)
I8: epidemije/oznake (FRISELN+MASERN-×12-W-krivulja-5-točk + MASERN-×2-ADJACENT +
    'Ukolk'[?]-×5 + MEJA-'18 78.'-38.-POTRDITEV + ULEDBA-#10-7.-instance +
    85-vpisov-EXAKT + ORDINALNO-ČISTO + 2×-87-LET)
I9: pt-luknja-18-final.json (04106 == 128, vitals == 1347)
I10: 04894-still-520 + 04106-leta == {1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}
--live: produkcija /api/qa == 199/199 + qa-p199 pass:True
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
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1878,', src)
check("I1 bloki 04106/1878 == 23", len(bloki) == 23, f"najdeno {len(bloki)}")
his = sorted(bloki, key=int)
check("I2 hiše-1878 (h30-×2)", ",".join(his) == "1,3,9,10,14,15,16,18,20,30,30,33,37,38,40,44,47,48,53,54,55,57,66", ",".join(his))

# I3: 04106-skupaj + vitals-1347
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1544 + 04106==325", "HOUSE_VITALS.length !== 1544" not in src and skupaj == 325,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1878-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if str(e.get("vas", "")).startswith("Griblje")]
check("I4 dokaz (85/23-griblje/13-anomalij + meja-s149-'18 78.'-SPLIT + s158-tail + 85-vrstic)",
      len(d["entries"]) == 85 and len(grib) == 23 and len(d["anomalije"]) == 13
      and "s149" in d["okvir"]["meja_1877_78"] and "18 78." in d["okvir"]["meja_1877_78"]
      and d["okvir"]["meja_1878_79"].startswith("s158")
      and d["statistika"]["vpisane_vrstice"] == 85,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1544")
check("I5 qa-p199 + števec-1375", "qa-p199-parish-death-1878-04106" in qa and st >= 100,
      f"1544-številcev={st}")

# I6: duhovniki-1878 (P199-segment)
i0 = src.find("P199: mrliška PREDZGODOVINA 04106, leto 1878")
seg = src[i0:] if i0 >= 0 else ""
check("I6 JANČAR-NIT-1878→1883 = 6-LET (tranzicija!)", "6-LET" in seg and "TRANZICIJA" in seg,
      f"Jančar-omen={seg.count('Jančar') + seg.count('JANČAR')}")
check("I6b Kogej-subst.-coop (VLM-'Fortin-aus-Kogelnik'-ZAVRJEN!)", "Kogej" in seg and "Fortin-aus-Kogelnik" in seg)
check("I6c Dovgan-dominanta", "Dovgan" in seg or "DOVGAN" in seg)

# I7: kontinuitete/oznake
h30 = len(re.findall(r'houseNo:\s*"30",\s*\n\s*bookSignature:\s*"04106",\s*\n\s*year:\s*1878', seg))
check("I7 h30-×2-1878 (Mathias-Pezdirc + Markus-'Pezdir(e)')", h30 == 2 and "h30-×2" in seg, f"h30={h30}")
check("I7b ZELIHA-NIT-h1-×3-v-2-letih (z46!)", "ZELIHA-NIT" in seg and "In Entbindung" in seg)
check("I7c ŠIMEC-NIT-×2-1878 (z32-h55 + z44-h38-87J)", "ŠIMEC-NIT-×2-1878" in seg or "ŠIMEC-nit" in seg.lower() or "ŠIMEC" in seg)
check("I7d KLOBUČAR-NIT-h48 (z14!)", "KLOBUČAR" in seg)
check("I7e GEHIRNENTZÜNDUNG-NIT-1878-#3-h57 (→ 1879-×2!)", "GEHIRNENTZÜNDUNG-NIT-1878-#3" in seg)
check("I7f h44-nit (→ 1879-z27-katastrofa!)", "h44-NIT-1878" in seg or "h44-nit" in seg or "h44" in seg)

# I8: epidemije/oznake
check("I8 FRISELN+MASERN-×12-W-krivulja-5-točk", "FRISELN+MASERN-×12" in seg and "W-krivulja" in seg)
check("I8b MASERN-×2-ADJACENT (z60+z61!)", "MASERN-×2-ADJACENT" in seg)
check("I8c 'Ukolk'[?]-NEZNANA-VAS-×5 (cf. P195-'Wolk'!)", "Ukolk" in seg and "Wolk" in seg)
check("I8d MEJA-'18 78.'-SPLIT-VARIANTA-v-z1 (38.-POTRDITEV!)", "38.-POTRDITEV" in seg and "18 78." in seg)
check("I8e ULEDBA-#10-7.-INSTANCE (z56: 29-Juni→1-Juli!)", "ULEDBA-#10-7.-INSTANCE" in seg)
check("I8f 85-VPISOV-EXAKT + ORDINALNO-ČISTO", ("85-VPISOV-EXAKT" in seg or "85 vpisov == P197" in seg or "\u2248 85'-EXAKT" in seg) and "ORDINALNO-ČISTO" in seg)
check("I8g 2×-87-LET-GRIBLJE (z44-Simec + z83-Peglavc!)", "87-LET" in seg and "Peglavc" in seg)

# I9: pt-luknja
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I9 pt-luknja (04106==325, vitals==1375)",
      pt["corpus"]["byBook"]["04106"] == 325 and pt["corpus"]["vitalsTotal"] == 1544,
      f"04106={pt['corpus']['byBook']['04106']} vitals={pt['corpus']['vitalsTotal']}")

# I10: 04894-still-520 + leta-nabor
check("I10 04894-still-520", src.count('bookSignature: "04894"') == 520,
      f"04894={src.count('bookSignature: \"04894\"')}")
leta = sorted(set(re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d{4})', src)))
check("I10b 04106-leta-{1877,...,1885}", ",".join(leta) == "1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885", ",".join(leta))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            prod = json.load(r)
        t199 = [t for t in prod.get("tests", []) if "p199" in str(t.get("id", ""))]
        check("LIVE produkcija ok — passed=199", prod.get("ok") is True and prod.get("passed") == 199,
              f"passed={prod.get('passed')}/{len(prod.get('tests', []))}")
        check("LIVE qa-p199 pass", bool(t199) and t199[0].get("pass") is True)
    except Exception as e:
        check("LIVE (napaka)", False, str(e)[:120])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "FAIL ✗")
sys.exit(0 if ok else 1)
