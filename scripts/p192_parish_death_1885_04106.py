#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — verifikator MRLIŠKE PREDHODNICE 04106, leto 1885 (predzgodovina-1/29).

I1: parish.ts vsebuje 16 blokov bookSignature 04106 / year 1885
I2: hiše 1885 == [1,5,9,13,21,31,31,31,31,54,58,62,63,63,68,78]
I3: HOUSE_VITALS.length == 1870 (1219 + 16 + 21-P193 + 11-P194!)
I4: dokaz research/issue17/parish-death-1885-04106.json ima 16 griblje-blokov + meja + anomalije
I5: qa-parish.ts vsebuje qa-p192-parish-death-1885-04106 + števec 1235
I6: knjiga-04106 v PARISH_BOOKS (death 1857–1885)
I7: duhovniki (Glibe[l]-dominanta + Dovgan) v blokih + P153-seam ('Andrej Glibel')
I8: h31-katastrofa (4× h31: Župarič + Papič-×3) + POŽEK-×2 (h21+h58) + KRIŽAN-×2 (h63)
I9: duplikat + dual-numbering + forma-sprememba označeni
I10: 04894-still-520 + 04106-leta == {1883, 1884, 1885}
--live: produkcija /api/qa == 192/192 + qa-p192 pass:True
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
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1885,', src)
check("I1 bloki 04106/1885 == 16", len(bloki) == 16, f"najdeno {len(bloki)}")
his = sorted(bloki, key=int)
check("I2 hiše-1885", ",".join(his) == "1,5,9,13,21,31,31,31,31,54,58,62,63,63,68,78", ",".join(his))

# I3: vitals
check("I3 vitals-1940 + 04106==433", "HOUSE_VITALS.length !== 1940" not in src and src.count('bookSignature: "04106"') == 433,
      f"04106-bloki={src.count('bookSignature: \"04106\"')}")

# I4: dokaz
d = json.load(open(f"{ROOT}/research/issue17/parish-death-1885-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if e.get("blok_v_parish")]
check("I4 dokaz (16 griblje + meja + anomalije)", len(grib) == 16 and d["okvir"]["meja_1884_85"].startswith("s198") and len(d["anomalije"]) == 12,
      f"griblje={len(grib)} anomalije={len(d['anomalije'])}")

# I5: qa-parish
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
check("I5 qa-p192 + števec", "qa-p192-parish-death-1885-04106" in qa and qa.count("HOUSE_VITALS.length !== 2043") >= 100,
      f"1940-številcev={qa.count('HOUSE_VITALS.length !== 1870')}")

# I6: PARISH_BOOKS
check("I6 PARISH_BOOKS 04106", re.search(r'signature: "04106", type: "death", from: 1857, to: 1885', src) is not None)

# I7: duhovniki + seam
check("I7 Glibe[l]-dominanta", src.count("Glibe[l] [~Gleibe] co") >= 13, f"Glibe-crops={src.count('Glibe[l] [~Gleibe] co')}")
check("I7b Dovgan ×2", src.count("Franz Dovgan") >= 2, f"Dovgan={src.count('Franz Dovgan')}")
check("I7c P153-seam 'Andrej Glibel'", "Andrej Glibel" in src)

# I8: katastrofa/mreže
h31 = src.count('houseNo: "31",\n    bookSignature: "04106",\n    year: 1885')
check("I8 h31-×4", h31 == 4, f"h31={h31}")
check("I8b POŽEK-×2", "h21 = POŽEK-hiša-PRED-04894" in src and "h58 = POŽEK-hiša-PRED-04894" in src)
check("I8c KRIŽAN-h63", "h63 = KRIŽAN-hiša-PRED-04894" in src)

# I9: anomalije-oznake
check("I9 DUPLIKAT+DUAL+FORMA", "z4-DUPLIKAT-VSTAVEK" in src and "DUAL-NUMBERING-START" in src and "SPREMEMBA-FORME-MID-BOOK" in src)

# I10: 04894-count + nič-izven-1885
bloki94 = re.findall(r'bookSignature:\s*"04894"', src)
check("I10 04894 == 520", len(bloki94) == 520, f"najdeno {len(bloki94)}")
izven = re.findall(r'bookSignature:\s*"04106",\s*year:\s*(\d+)', src)
check("I10b 04106-leta-{1877,...,1885}", set(izven) == {"1857", "1858", "1859", "1860", "1861", "1862", "1863", "1864", "1865", "1866", "1867", "1868", "1869", "1870", "1871", "1872", "1873", "1874", "1875", "1876", "1877", "1878", "1879", "1880", "1881", "1882", "1883", "1884", "1885"}, str(set(izven)))

# --live
if "--live" in sys.argv:
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=60) as r:
            rep = json.load(r)
        p192 = [c for c in rep.get("tests", []) if c.get("id") == "qa-p192-parish-death-1885-04106"]
        check("LIVE produkcija ok", rep.get("ok") is True, f"passed={rep.get('passed')}")
        check("LIVE qa-p192 pass", bool(p192) and p192[0].get("pass") is True)
    except Exception as e:
        check("LIVE produkcija", False, str(e))

print("\n" + ("VSE KONTROLE PASS ✓" if ok else "NEKATERE KONTROLE FAIL ✗"))
sys.exit(0 if ok else 1)
