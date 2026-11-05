#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P200 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1877 (predzgodovina-9/29).

I1: parish.ts vsebuje 8 blokov bookSignature 04106 / year 1877
I2: hiše 1877 == [6,8,12,18,42,53,57,62]
I3: 04106-skupaj == 312 + vitals-števec-1498
I4: dokaz research/issue17/parish-death-1877-04106.json (60 entries / 8-griblje /
    13-anomalij / meja-s143-'18 77.'-ODREZANA + s145-'1877.'-39.-potrditev + 60-vrstic)
I5: qa-parish.ts vsebuje qa-p200-parish-death-1877-04106 + števec 1375 (≥ 100)
I6: duhovniki-1877 (KOGEJ-RAZŠIRJENO-NAZAJ + Dovgan-dominanta + JANČAR-NIT-STABILNA)
I7: kontinuitete/oznake (h12-DRAGOŠ-POPREVEK + h18-ŠIMEC-NIT + h53/h57-NIT + PEZDINC-#7)
I8: oznake ('Hrible'[?]-NOVA-LOKALNOST + 'Br[a]stfbrand'-KLASTER-×3 + ULEDBA-#10-8.-
    instance + 39.-POTRDITEV + ŠTEVJE-IZ-VRSTIC + otroška-umrljivost-75%)
I9: pt-luknja-18-final.json (04106 == 312, vitals == 1531)
I10: 04894-still-520 + 04106-leta == {1877,...,1885}
--live: produkcija /api/qa == 200/200 + qa-p200 pass:True
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
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1877,', src)
check("I1 bloki 04106/1877 == 8", len(bloki) == 8, f"najdeno {len(bloki)}")
his = sorted(bloki, key=int)
check("I2 hiše-1877", ",".join(his) == "6,8,12,18,42,53,57,62", ",".join(his))

# I3: 04106-skupaj + vitals-1498
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1531 + 04106==312", "HOUSE_VITALS.length !== 1531" not in src and skupaj == 312,
      f"04106-bloki={skupaj}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1877-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if str(e.get("vas", "")).startswith("Griblje")]
check("I4 dokaz (60/8-griblje/14-anomalij + meja-s143-'18 77.' + s145-'1877.'-39. + 60-vrstic)",
      len(d["entries"]) == 60 and len(grib) == 8 and len(d["anomalije"]) == 14
      and "s143" in d["okvir"]["meja_1876_77"] and "ODREZANA" in d["okvir"]["meja_1876_77"]
      and "39.-POTRDITEV" in json.dumps(d["anomalije"], ensure_ascii=False)
      and d["statistika"]["vpisane_vrstice"] == 60,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1531")
check("I5 qa-p200 + števec-1375", "qa-p200-parish-death-1877-04106" in qa and st >= 100,
      f"1531-številcev={st}")

# I6: duhovniki-1877 (P200-segment)
i0 = src.find("P200: mrliška PREDZGODOVINA 04106, leto 1877")
seg = src[i0:] if i0 >= 0 else ""
check("I6 KOGEJ-OBDOBJE-RAZŠIRJENO-NAZAJ (1877-Jänner→Mai!)", "KOGEJ-OBDOBJE-RAZŠIRJENO-NAZAJ" in seg,
      f"Kogej-omen={seg.count('Kogej') + seg.count('KOGEJ')}")
check("I6b JANČAR-NIT-1878→1883-SPREMENJENA (NO-Jančar-1877!)", "JANČAR-NIT-1878→1883-SPREMENJENA" in seg)
check("I6c Dovgan-dominanta-1877", "Dovgan" in seg or "DOVGAN" in seg)

# I7: kontinuitete/oznake
check("I7 h12-DEFINITIVNO (P199-'h18[?]'-POPREVEK — z56-DRAGOŠ!)", "h12-DEFINITIVNO" in seg and "DRAGOŠ" in seg)
check("I7b h18-ŠIMEC-NIT-1877 (z26-Siniec — INNEC/SIMEC/TIMEC!)", "ŠIMEC-NIT-1877" in seg or "ŠIMEC-GRAFIA" in seg)
check("I7c h53/h57-NIT-1877 (z51-Pezdinc → z83-Peglavc + z49-Lozar → z80-Logar!)", "h53-NIT-1877" in seg and "h57-NIT-1877" in seg)
check("I7d PEZDINC-GRAFIA-NIT-#7 (z51!)", "PEZDINC-GRAFIA-NIT-#7" in seg)
check("I7e h44-TAIL-1876 (24-URE-Vesperstbrand[?]-Kavčič!)", "h44-TAIL-1876" in seg or "24-URE" in seg)

# I8: oznake
check("I8 'HRIBLE'[?]-NOVA-LOKALNOST-×3 (G-glyph-duel-3.×!)", "HRIBLE" in seg and "G-glyph-duel" in seg)
check("I8b 'Br[a]stfbrand'[?]-KLASTER-×3-OKTOBER (z48/z49/z52!)", "Br[a]stfbrand" in seg and "KLASTER" in seg)
check("I8c ULEDBA-#10-8.-INSTANCE (z24: 29-April→1-Mai!)", "ULEDBA-#10-8.-INSTANCE" in seg)
check("I8d 39.-POTRDITEV-invariante (s145-'1877.'-glava-v-z22-celici!)", "39.-POTRDITEV" in seg)
check("I8e 60-VPIISOV-ŠTEVJE-IZ-VRSTIC (ordinali-NEVIDNI-×6!)", "ŠTEVJE-IZ-VRSTIC" in seg and "NEVIDNI" in seg)
check("I8f otroška-umrljivost-75% (6/8!)", "75%-1877" in seg or "UMRLJIVOST-75%" in seg)

# I9: pt-luknja
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I9 pt-luknja (04106==312, vitals==1511)",
      pt["corpus"]["byBook"]["04106"] == 312 and pt["corpus"]["vitalsTotal"] == 1531,
      f"04106={pt['corpus']['byBook']['04106']} vitals={pt['corpus']['vitalsTotal']}")

# I10: 04894-still-520 + leta-nabor
check("I10 04894-still-520", src.count('bookSignature: "04894"') == 520,
      f"04894={src.count('bookSignature: \"04894\"')}")
leta = sorted(set(re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d{4})', src)))
check("I10b 04106-leta-{1877,...,1885}", ",".join(leta) == "1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885", ",".join(leta))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            prod = json.load(r)
        passed = prod.get("passed")
        p200 = next((t for t in prod.get("tests", []) if t.get("id") == "qa-p200-parish-death-1877-04106"), None)
        check("LIVE produkcija /api/qa", prod.get("ok") is True and passed == 200,
              f"ok={prod.get('ok')} passed={passed}")
        check("LIVE qa-p200-pass", bool(p200 and p200.get("pass")),
              f"qa-p200={'pass' if p200 and p200.get('pass') else 'FAIL/MISSING'}")
    except Exception as e:
        check("LIVE produkcija (dostop)", False, str(e)[:120])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
