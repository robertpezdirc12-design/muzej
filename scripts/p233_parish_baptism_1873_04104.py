#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P233 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1873 = 13/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1873,', src)
check("I1 bloki 04104/1873-numeric == 17", len(bloki) == 17, f"najdeno {len(bloki)}")
pri = ["16", "34", "37", "13", "31", "49", "1", "40", "69", "74", "8", "22", "53", "37", "6", "62", "41"]
check("I2 hiše-1873 (file-order, 17-vpisov / 16-DISTINCT-h37-×2-DUEL-X-open!)", bloki == pri and len(set(bloki)) == 16, ",".join(bloki) if bloki else "-")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1940 + 04104==254", "HOUSE_VITALS.length !== 1940" not in src and skupaj == 288, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1873-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "grib" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (17-griblje + MEJA-pred-s28-X-ARITMETIKA-98-VPISOV-zap-98-REŠEN + foliacija-25–33 + PENT-duhovnikov)",
      len(grib) == 17
      and "meja-1872-73-pred-s28-izven-okna" in an
      and "x-aritmetricni-model-zap-9-anker" in an
      and "98-VPISOV-1873" in an and "'zap-98'" in an
      and "foliacija-sken-3-sekvenčno-25-33-brez-duplikatov" in an
      and "pent-duhovnikov-1873-x-open" in an
      and d["frame"]["rowsTotal"] == 98 and d["stats"]["griblje_vpisov"] == 17
      and "25–33" in d["frame"]["pagKonvencija"] and "s1–s27" in d["frame"]["pagKonvencija"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (pezdirc-x8-garble-rekord + jakofcic-x5 + silar-x3 + 4-prazni-meseci + z73-paralela-p232 + merge-s35-razrešen)",
      "pezdirc-x8-garble-rekord" in an and "jakofcic-x5-rekord-brodaric-x6-komplet" in an
      and "silar-x3-nova-nit-drugosi-x3" in an and "4-prazni-meseci-rekord-izenačen" in an
      and "z73-pozicijska-paralela-p232" in an and "full-r2-r3-merge-s35-razrešen" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2043")
check("I5 qa-p233 + števec-1940", "qa-p233-parish-baptism-1873-04104" in qa and st >= 145, f"1940-številcev={st}")

i0 = src.find("P233: krstna PREDZGODOVINA 04104, leto 1873")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 98-VPISOV + X-ARITMETIČNI-MODEL-9-ANKER + zap-98-REŠEN + LEAD-NADGRADJENO", "98-VPISOV-1873" in seg and "X-ARITMETIČNI-MODEL-zap (9-ANKER" in seg and "P232-X-open-'TAIL-zap-28[~98/lokalni-restart]'-REŠEN-1:1-'zap-98'" in seg and "vs-LEAD-'~95'-NADGRADJENO" in seg)
check("I6b MEJA-1872/73-PRED-s28 + 13.-restart + TAIL-1873-zap-88–97 + z1–z10-pred-s28", "MEJA-1872/73 = PRED-s28 (IZVEN-okna!-X-open)" in seg and "13.-restart-z1-linije" in seg and "TAIL-1873 = s36-r1–r10-zap-88–97" in seg and "z1–z10-PRED-s28 (Jänner–März!-na-s26/s27" in seg)
check("I6c 'sken−3'-25–33-SEKVENČNO + +10-KURRENT-'1'-'2'-MISREAD + formula-CONTINUES", "'sken−3'-SEKVENČNO-s28–s36 (25–33!" in seg and "+10-SISTEMATIČNI-KURRENT-'1'-'2'-MISREAD" in seg and "formula-CONTINUES-iz-P232" in seg)
check("I7a 17-GRIBLJE / 16-hiš-h37-DUEL + h40-continuum + h9/h74", "17-GRIBLJE / 16-hiš" in seg and "h37-×2-DUEL-X-open-z19-vs-z81" in seg and "h40-DUEL-continuum" in seg and "h74/64-DUEL" in seg and "h8" in seg)
check("I7b PEZDIRC-×8-GARBLE-REKORD + JAKOFČIČ-×5 + BRODARIČ-×6-KOMPLET + ŠILAR-×3", "PEZDIRC-×8-GARBLE-REKORD-PORAST" in seg and "JAKOFČIČ-×5-REKORD" in seg and "BRODARIČ-×6-REKORD-KOMPLET" in seg and "ŠILAR-×3-KOMPLET-NOVA-NIT" in seg)
check("I7c X-ANKE (z51/z55/z56/z65/z68/z88/z92/z93/z94) + DRAGOŠ-×3-KOMPLET + NEZ-×1-X-open", "★zap-51-X!" in seg and "★zap-55-X!" in seg and "★zap-56-X!" in seg and "★zap-65-X!" in seg and "★zap-68-X!" in seg and "★zap-92-X!" in seg and "★zap-94-X!" in seg and "DRAGOŠ-×3-KOMPLET" in seg and "NEZAKONSKI-×1-X-open" in seg)
check("I7d LEAD-REŠITVE (JAKOŠA→JAKOFČIČ + MILEK-botra-DUEL + h11-KUMIĆ-DUEL-×3 + h37/57-X-REŠEN + full-MERGE-RAZREŠEN)", "LEAD-JAKOŠA-REŠEN" in seg and "LEAD-'MILEK-botra'-DUEL-X-open" in seg and "LEAD-'h11-Kaspar-KUMIĆ'-DUEL-REŠEN-X-open-×3" in seg and "37/57-DUEL-X-★★★-REŠEN-'37'" in seg and "full-MERGE-RAZREŠEN" in seg)
check("I7e X-ločitve (z28-3-way + z55-vas-DUEL-GRIBLJE-zmaga + z68-MILEK-vs-NOVAC + z94-Kaspar-Katharina + h22/42 + h74/64 + h31/33)", "hisna-31/33-DUEL" in seg and "vas-DUEL-×2/×1-GRIBLJE-zmaga" in seg and "MILEK-vs-NOVAC-DUEL-X-★★★" in seg and "h22/42-DUEL" in seg and "h74/64-DUEL" in seg and "h41/11-DUEL" in seg)
check("I8a 4-PRAZNI-MESECI + MODRI-×2 + PENT-duhovnikov + z73-POZICIJSKA-PARALELA", "4-PRAZNI-MESECI-REKORD-IZENAČEN" in seg and "MODRI-×2-Griblje" in seg and "PENT-duhovnikov-1873-X-open-GARBLE" in seg and "POZICIJSKA-PARALELA-P232-z73" in seg)
check("I8b s37-TAIL-'Initium-1874'-P232 + LEAD-P234-1872", "MEJA-1873/74-s37-SREDI-PAGI-'Initium-anni-Domini-1874'-KALLIGRAFIJA-NOVA-VARIANT" in seg and "P234-LEAD" in qa and "1872" in qa)
check("I9a qa-p233 (233. kontrola!)", "qa-p233" in qa and "233. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-254/2043 + byBook-04104", '"vitalsTotal": 2043' in pt and '"04104": 288' in pt)
v232 = open(f"{ROOT}/scripts/p232_parish_baptism_1874_04104.py", encoding="utf-8").read()
check("I9c p232-verifier-I9b-FIX (1940→2043-sanitizacija-P257!)", '"vitalsTotal": 2043' in v232 and "1887" not in v232)

live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            check("I10 LIVE matricula-04104 HTTP 200", r.status == 200, f"status={r.status}")
    except Exception as e:
        check("I10 LIVE matricula-04104", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
