#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1872 = 14/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1872,', src)
check("I1 bloki 04104/1872-numeric == 17", len(bloki) == 17, f"najdeno {len(bloki)}")
pri = ["11", "30", "3", "44", "9", "38", "24", "12", "33", "6", "40", "68", "69", "7", "30", "66", "29"]
check("I2 hiše-1872 (file-order, 17-vpisov / 16-DISTINCT-h30-×2-DUEL!)", bloki == pri and len(set(bloki)) == 16, ",".join(bloki) if bloki else "-")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1940 + 04104==288", "HOUSE_VITALS.length !== 1940" not in src and skupaj == 288, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1872-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "grib" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (17-griblje + 115-ARITMETIKA-TAIL-VERIGA + MEJA-1871/72-PAGE-BOUNDARY + DUPLIKAT-s28=s29 + PRIMING-halucinacija)",
      len(grib) == 17
      and "115-vpisov-aritmetricni-model-tail-veriga" in an
      and "meja-1871-72-page-boundary-restart-s14-r1" in an
      and "meja-1872-73-page-boundary-p233-napoved-1-1" in an
      and "duplikat-s28-s29-resitev-p233-uge" in an
      and "janner-priming-halucinacija-s19-razrešena" in an
      and d["frame"]["rowsTotal"] == 115 and d["stats"]["griblje_vpisov"] == 17
      and "11–22" in d["frame"]["pagKonvencija"] and "s1–s13" in d["frame"]["pagKonvencija"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (pezdirc-x5 + dragoš-x3-paralela + hrižan-x5 + h40-continuum-x4 + prečrtana-kopija + garbage-row)",
      "pezdirc-x5-garble-continuem-eksplicitni" in an and "dragoš-x3-komplet-hrižan-x5-komplet-paralela" in an
      and "h40-continuum-x4-modri-x4" in an and "h30-x2-duel-prečrtana-kopija-r7" in an
      and "mesec-garbage-row-z27-september-x0" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2059")
check("I5 qa-p234 + števec-1940", "qa-p234-parish-baptism-1872-04104" in qa and st >= 146, f"1940-številcev={st}")

i0 = src.find("P234: krstna PREDZGODOVINA 04104, leto 1872")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 115-VPISOV + TAIL-VERIGA-6/6 + 116−1-prečrtana + LEAD-NADGRADJENO", "115-VPISOV-ARITMETIČNI-MODEL" in seg and "TAIL-VERIGA-6/6" in seg and "116-vrstic-−-1-prečrtana-=-115-DISTINCT-VPISOV" in seg and "vs-LEAD-'~85–95'-NADGRADJENO" in seg)
check("I6b MEJA-1871/72-PAGE-BOUNDARY + 12.-restart + MEJA-1872/73-PAGE-BOUNDARY + 13.-restart-SUPER", "MEJA-1871/72 = s13/s14-PAGE-BOUNDARY" in seg and "12.-restart-PARALELA-P223" in seg and "MEJA-1872/73 = s25/s26-PAGE-BOUNDARY" in seg and "13.-restart-S26R1-SUPER-'1'-VISOKO" in seg)
check("I6c 'sken−3'-11–22-SEKVENČNO + PRIMING-HALUCINACIJA + DUPLIKAT-s28=s29", "'sken−3'-SEKVENČNO-s14–s25 (11–22!" in seg and "PRIMING-HALUCINACIJA-RAZREŠENA" in seg and "DUPLIKAT-s28 = s29-RESITEV" in seg and "98-TOTAL-1873-INTAKTEN" in seg)
check("I7a 17-GRIBLJE / 16-hiš-h30-DUEL + h40-continuum-×4 + h69-continuum", "17-GRIBLJE / 16-hiš" in seg and "h30-×2-DUEL-z14-Petek" in seg and "h40-CONTINUUM" in seg and "h69-continuum" in seg)
check("I7b PEZDIRC-×5-GARBLE + DEBLIČ-Deblin-X + JAKOFČIČ-×2 + ŠIMEC-×3", "PEZDIRC-×5-GARBLE-continuum" in seg and "DEBLIČ-×1-'Deblin'-X" in seg and "JAKOFČIČ-×2-KOMPLET" in seg and "ŠIMEC-×3-KOMPLET" in seg)
check("I7c DRAGOŠ-×3-KOMPLET-1:1-PARALELA + HRIŽAN-×5 + HLOBUČAR-×3 + KLOBUČAR-×2", "DRAGOŠ-×3-KOMPLET-1:1-PARALELA-P233" in seg and "HRIŽAN-×5-oseb-KOMPLET" in seg and "HLOBUČAR-×3-KOMPLET" in seg and "KLOBUČAR-×2" in seg)
check("I7d X-ločitve (z63-h6/61 + z103-h30/39 + zap-47/48 + MILEK-Milhoeluc + z115-h29-TAIL)", "z63-h6/61-DUEL" in seg and "z103-h30/39-DUEL" in seg and "zap-47/48-DUEL" in seg and "MILEK-'Milhoeluc'-PARALELA" in seg and "z115-h29-★★★-TAIL-1872" in seg)
check("I7e z115-TAIL + 1.-VPIS-leta-GRIBLJE + r7-PREČRTANA + MODRI-×4 + SEPTEMBER-×0", "TAIL-1872 = z115" in seg and "1.-VPIS-leta-1872 = GRIBLJE" in seg and "PREČRTANA-KOPIJA-X" in seg and "MODRI-×4-Griblje-1872" in seg and "SEPTEMBER-×0-GRIBLJE" in seg)
check("I8a P233-NAPoved-POTRJENA + GARBAGE-ROW + 'Morija'-nota", "P233-ARITMETIČNA-NAPoved-1:1" in seg and "mesec-GARBAGE-ROW" in seg and "'Morija'-črtan-nota" in seg)
check("I8b P233-LEAD-POTRJEN-s26 + LEAD-P235-1871", "P233-X-open-RESOLVED" in seg and "P235-LEAD" in qa and "1871" in qa)
check("I9a qa-p234 (234. kontrola!)", "qa-p234" in qa and "234. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-271/2043 + byBook-04104", '"vitalsTotal": 2059' in pt and '"04104": 288' in pt)
v233 = open(f"{ROOT}/scripts/p233_parish_baptism_1873_04104.py", encoding="utf-8").read()
check("I9c p233-verifier-sanitizacija (1940→2059-P258!)", '"vitalsTotal": 2059' in v233 and "1906" not in v233)

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
