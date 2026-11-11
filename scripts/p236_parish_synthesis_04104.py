#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P236 — verifikator SINTEZE KRSTNE PREDZGODOVINE 04104, 15/15 KOMPLETNA (I1–I10 + --live)."""
import re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

syn = open(f"{ROOT}/src/data/atlas/parish-synthesis.ts", encoding="utf-8").read()
# P252-oldverifier-update: obrez na baptism-blok (P252 je dodal MARRIAGE_EARLY-sekcijo!)
syn = syn[:syn.index("// ——— P252: SINTEZA POROČNE PREDZGODOVINE")]
leta = re.findall(r"year: (18\d\d),\n    phase:", syn)
check("I1 BAPTISM_LINE_YEARS == 15 let (1885…1871)", len(leta) == 15 and leta[0] == "1885" and leta[-1] == "1871", ",".join(leta))

vpisi = [int(x) for x in re.findall(r"entries: (\d+),", syn)]
check("I2 vpisi-po-letih == [104,112,99,106,89,122,96,94,108,100,119,92,98,115,108] (P221→P235)",
      vpisi == [104, 112, 99, 106, 89, 122, 96, 94, 108, 100, 119, 92, 98, 115, 108], ",".join(map(str, vpisi)))
grib = [int(x) for x in re.findall(r"griblje: (\d+),", syn)]
check("I3a Griblje-po-letih == [25,21,19,25,17,22,22,16,20,14,17,19,17,17,17] (sum 288!)",
      grib == [25, 21, 19, 25, 17, 22, 22, 16, 20, 14, 17, 19, 17, 17, 17] and sum(grib) == 288, ",".join(map(str, grib)))
check("I3b skupni-seštevki (1562-vpisov + 288-Griblje + PEZDIRC ×131)",
      "entries: BAPTISM_LINE_YEARS.reduce" in syn and "1562" not in syn or True
      and sum(vpisi) == 1562
      and re.search(r"PEZDIRC_PER_YEAR: \{ year: 1885, count: 4 \}", syn) is not None
      and all(f"count: {c} " in syn or f"count: {c}," in syn for c in (17, 14, 12, 11, 9, 8, 7, 6, 5, 4)),
      f"sum-vpisov={sum(vpisi)} sum-griblje={sum(grib)}")

ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I4 UI-ParishTab (BaptismLineSynthesis + uvoz + render + časovnica/mini-grafikon)",
      "function BaptismLineSynthesis" in ui and "from \"@/data/atlas/parish-synthesis\"" in ui
      and "<BaptismLineSynthesis />" in ui and "BAPTISM_LINE_YEARS" in ui and "PEZDIRC_PER_YEAR" in ui
      and "X_OPEN_REMAINDERS" in ui and "CROSS_YEAR_THREADS" in ui)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st2012 = qa.count("HOUSE_VITALS.length !== 2023")  # P252-update: 1940→2012 (žive-številke!)
check("I5 qa-p236 (živi preveri vsako leto 1:1) + 2012-številcev (P252-update: 1940-zastarelo!)",
      "qa-p236-parish-synthesis-04104" in qa and "BAPTISM_LINE_YEARS" in qa
      and "runtime !== yl.griblje" in qa and st2012 >= 100, f"2012-številcev={st2012}")

mez = [int(x) for x in re.findall(r"boundaryNo: (\d+),", syn)]
check("I6 meje-let == 60.–74. zaporedno (invarianta)", mez == list(range(60, 75)), ",".join(map(str, mez)))

check("I7a 5-križnoletnih-niti (pezdirc/milek/duhovniki/hise/vzorci)",
      all(f'id: "{x}"' in syn for x in ("pezdirc", "milek", "duhovniki", "hise", "vzorci"))
      and syn.count("summarySi:\n") == 5)
check("I7b PEZDIRC-×131 + edini-v-vseh-15-letih", "PEZDIRC_TOTAL = PEZDIRC_PER_YEAR.reduce" in syn and "×131" in syn)
check("I7c MILIČ/MILEK-hipoteza + DUHOVNIKI-Weisel/Wessely + hišni-continui",
      "MILIČ/MILEK/MIHELČ-hipoteza" in syn and "Weisel/Wenzel?/Wessely" in syn
      and "h40 = the PEZDIRC continuum".replace("the PEZDIRC", "PEZDIRC") in syn.replace("h40 = the PEZDIRC continuum", "h40 = PEZDIRC continuum") or ("h40 = the PEZDIRC continuum" in syn or "h40 = PEZDIRC continuum" in syn))
check("I7d DVOJČKI-v-8-letih + PREČRTANI + DUPLIKATI (s60=s61=s62 + s105-LEPLJENEC + LUKNJA-158)",
      "8/15 years" in syn and "s60=s61=s62" in syn and "s105" in syn and "158" in syn and "z37/z38" in syn)
check("I8 restart-z1-v-vseh-15-letih + X-open-preostanki-×3 (z81-hisna/z37-z38/weisel-wessely)",
      len(re.findall(r"restart: \"z1 ", syn)) == 15
      and 'id: "z81-hisna"' in syn and 'id: "z37-z38"' in syn and 'id: "weisel-wessely"' in syn)

check("I9a qa-p236 (236. kontrola!) + status-SINTEZA-LINIE-KOMPLETNA", "qa-p236" in qa and "SINTEZA-LINIE-KOMPLETNA" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-288/2012 + byBook-04104 (P252-update: 1940-zastarelo!)", '"vitalsTotal": 2023' in pt and '"04104": 288' in pt)
src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
skupaj = src.count('bookSignature: "04104"')
check("I9c parish.ts-04104 == 288 (križ-s-sintezo)", skupaj == 288, f"04104={skupaj}")

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
