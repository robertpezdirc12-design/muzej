#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P240 — verifikator POROČNE PREDZGOVINE 04455, leto 1883 = 3/13 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1883,', src)
check("I1 bloki 04455/1883-numeric == 2", len(bloki) == 2, f"najdeno {len(bloki)}")
check("I2 hiše-1883 (vrstni-red 13, 2)", bloki == ["13", "2"], ",".join(bloki))
skupaj = src.count('bookSignature: "04455"')
check("I3 vitals-1985 + 04455==242 (P246-živo!)", "HOUSE_VITALS.length !== 1985" not in src and skupaj == 242, f"04455={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1883-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalies"], ensure_ascii=False)
check("I4 dokaz (12-vpisov + 2-Griblje + BREZ-preskokov + restart-s50-DNO + meja-s50-MID + glava-'1 8 8 3.')",
      d["stats"]["entries"] == 12 and d["stats"]["gribljeMarriages"] == 2
      and d["stats"]["zapSkipped"] == 0
      and "s50" in d["frame"]["meja_1882_83"] and "21. Januar" in d["frame"]["meja_1882_83"]
      and "s52→s53" in d["frame"]["meja_1883_84"]
      and "RAZREŠEN" in d["frame"]["meja_1882_83"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']} anomalies={len(d['anomalies'])}")
check("I4b restart-glava-MISREAD-RAZREŠEN + s51-'2.'-nodat + v5-pripis-Vinica + v6-'nesumnjivo'",
      "RAZREŠEN" in an and "prva-je-2.-ne-1" in an.replace("številka", "").replace("  ", "-") or "prva-je-2" in an
      and "rojstni-kraj" in an and "nesumnjivo" in an)
check("I4c h2-1.-poročni-blok + PEZDIRC-'NI-Pegdirc' + MILEK-izven-korpusa + HROVALJ-brat+sestra",
      "1.-POROČNI-04455-BLOK-KADARKOLI" in an and "NI-'Pegdirc'" in an
      and "MILEK-križ-KANDIDAT" in an and "HROVALJ-brat+sestra" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1985")
check("I5 qa-p240 + števec-1966", "qa-p240-parish-marriage-early-04455-1883" in qa and st >= 145, f"1966-številcev={st}")

i0 = src.find("P240: poročna PREDZGOVINA 04455, leto 1883")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 12-vpisov-BREZ-preskokov + restart-s50-DNO-CRNIČ", "12-vpisov-leta-1883" in seg and "BREZ-PRESKOKOV" in seg and "RESTART-1883 = s50-DNO" in seg and "Jovan-CRNIČ" in seg)
check("I6b števke-'1 8 8 3.'-črez-stolpce + MISREAD-razrešen", "razporejene-črez-stolpce" in seg and "MISREAD-razrešen-2:1" in seg)
check("I6c h2-1.-poročni-04455-blok + HLEBEC-'nesumnjivo'", "1.-POROČNI-04455-BLOK-KADARKOLI" in seg and "HLEBEC" in seg and "nesumnjivo" in seg)
check("I6d h13-RADOVIČ + Segečelo-Vinica-pripis", "RADOVIČ" in seg and "Segečelo" in seg and "NE-hiša" in seg)
check("I7a PEZDIRC-'NI-Pegdirc'-črka-za-črko + CONTINUUM", "NI-Pegdirc" in seg and "črka-za-črko" in seg and "×131→04455" in seg)
check("I7b MILEK-kandidat-IZVEN-korpusa-×237-ostaja", "Milleh" in seg and "IZVEN" in seg and "×237" in seg)
check("I7c HROVALJ-brat+sestra + tail-1882-HRIZAN-h36", "HROVALJ-brat+sestra" in seg and "Mathias-HRIZAN-GRIBLJE-36-tail" in seg)
check("I8a številčenje-modul (MARRIAGE_1883_NUMBERING)", "prva-je-2.-ne-1." in open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read())
m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I8b modul-1883 (MARRIAGE_1883_*-izvozi)", all(x in m for x in [
    "MARRIAGE_1883_BLOCKS", "MARRIAGE_1883_GRIBLJE", "MARRIAGE_1883_HOUSES", "MARRIAGE_1883_TOTAL",
    "MARRIAGE_1883_XOPEN", "MARRIAGE_1883_MEJA", "MARRIAGE_1883_NUMBERING", "PEZDIRC_1883_NIT",
    "MILEK_1883_KANDIDAT", "PRIEST_1883", "HROVALJ_1883_SIBLINGS", "MARRIAGE_1883_VILLAGE_DUELS"]))
check("I8c forenzika-×237-ostaja", "×237 blokov čez 5 knjig" in open(f"{ROOT}/src/data/atlas/parish-forensics.ts", encoding="utf-8").read())
check("I9a pt-luknja-1985 + byBook-04455=242 (P241-živo!)", '"vitalsTotal": 1985' in open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
      and '"04455": 242' in open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read())
check("I9b worklog-P240-vnos", "## P240" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c UI-MarriageEarly1883-v-ParishTab", "MarriageEarly1883" in open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read())
check("I9d sidra-228 + 1879:9-P244! + 1880:3-P243 (qa-sidra-message-P244-živo!)", "poročna sidra ≠ 235 (1878:7-P246! · 1879:9-P244! · 1880:3-P243! · 1881:9-P242! · 1882:7-P241! · 1883:2-P240!" in qa)

if "--live" in sys.argv:
    try:
        r = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                   headers={"User-Agent": "Mozilla/5.0"})
        code = urllib.request.urlopen(r, timeout=30).status
        check("I10 LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10 LIVE matricula-04455", False, str(e)[:60])

print()
print(f"VERIFIER-P240: {'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
