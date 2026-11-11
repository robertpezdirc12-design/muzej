#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P252 — verifikator SINTEZE POROČNE PREDZGODOVINE 04455, 13/13 KOMPLETNA (I1–I10 + --live).

Sinteza IZKLJUČNO meri obstoječe faze P238–P251 (NI novih branj/skenov!) — korpus 2012/269
NESPREMENJEN; razcep 74 (predzgodovina 1873–1885) + 195 (linija 1886–1922) = 269 — pt-luknja 1:1.
"""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

syn_full = open(f"{ROOT}/src/data/atlas/parish-synthesis.ts", encoding="utf-8").read()
src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
# P252-sekcija (za BaptismYear-razdelkom P236!) — vsi regexi za sintezo so omejeni nanno!
syn = syn_full[syn_full.index("// ——— P252: SINTEZA POROČNE PREDZGODOVINE"):]

# ——— I1: MARRIAGE_EARLY_LINE_YEARS — 13 let 1885→1873, griblje 1:1 z runtime parish.ts ———
leta = [int(y) for y in re.findall(r"year: (18[78]\d),\s*\n\s*phase:", syn) if 1873 <= int(y) <= 1885]
check("I1a MARRIAGE_EARLY_LINE_YEARS == 13 let 1885→1873 (descending-kot-04104!)",
      len(leta) == 13 and leta[0] == 1885 and leta[-1] == 1873, ",".join(map(str, leta)))
pri = {int(y): int(g) for y, g in re.findall(
    r'year: (\d+),\s*\n\s*phase: "P[^"]*",\s*\n\s*progress: "[^"]*",\s*\n\s*entries: \d+,\s*\n\s*griblje: (\d+),', syn) if 1873 <= int(y) <= 1885}
run = {}
for y in range(1873, 1886):
    run[y] = len(re.findall(r'bookSignature: "04455",\s*year: %d,' % y, src))
razcep_ok = all(pri.get(y) == run[y] for y in run) and sum(run.values()) == 74
check("I1b griblje-po-letih 1:1-z-runtime (7+3+2+7+9+3+9+7+5+6+1+11+4 = 74!)",
      razcep_ok and run.get(1874) == 11 and run.get(1873) == 4 and run.get(1885) == 7,
      " ".join(f"{y}:{run[y]}" for y in sorted(run)))

# ——— I2: razcep korpusa 74 + 195 = 269 — pt-luknja 1:1 (vitals 2012 NESPREMENJEN!) ———
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-2012 + 04455==269 + razcep-74/195 (NI novih branj — MERI!)",
      "HOUSE_VITALS.length !== 2012" not in src and skupaj == 269 and sum(run.values()) == 74
      and skupaj - 74 == 195, f"04455={skupaj} predzgodovina={sum(run.values())}")

# ——— I3: dokaz research/issue17/parish-marriage-synthesis-early.json ———
d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-synthesis-early.json", encoding="utf-8"))
st = d["stats"]
check("I3 dokaz (266-vpisov + 74-blokov + PEZDIRC-×35/13-13 + FOLIACIJA-29/29 + FINIS-SODA-×4 + KNIŽNO-ODPIRANJE + 26-DVIGOV)",
      st["vpisi"] == 266 and st["blokiGriblje"] == 74 and st["pezdircSkupaj"] == 35
      and st["pezdircPoLetih"].startswith("3+4+1+5+1+2+2+2+1+9")
      and "29/29" in st["foliacija"] and st["finisSODA"] == 4
      and "m1–m17" in st["knjiznoOdpiranje"] and "VEZALO" in st["knjiznoOdpiranje"]
      and st["firstYearDvigi"] == 26 and "+34" in st["dvigiRekordi"],
      f"vpisi={st['vpisi']} bloki={st['blokiGriblje']} pezdirc={st['pezdircSkupaj']}")
check("I3b niti-6 + xOpen + honesty + lead-P253+",
      len(d["niti"]) == 6 and len(d["xOpen"]) >= 5 and len(d["honesty"]) >= 5
      and "predhodnik" in d["lead"] and "m1–m17" in d["lead"],
      f"niti={len(d['niti'])} xOpen={len(d['xOpen'])}")

# ——— I4: PEZDIRC_MARRIAGE_PER_YEAR v P252-sekciji modula (×35 = 3+4+1+5+1+2+2+2+1+9+3+1+1) ———
pez_pairs = re.findall(r"\{ year: (18[78]\d), count: (\d+) \},", syn)
pez_mar = [(int(y), int(c)) for y, c in pez_pairs if 1873 <= int(y) <= 1885]
check("I4 PEZDIRC_MARRIAGE_PER_YEAR ×35/13-let (vrh-1876-×9-REKORD!-dno-1877/1883-×1!)",
      len(pez_mar) == 13 and sum(c for _, c in pez_mar) == 35
      and dict(pez_mar).get(1876) == 9 and dict(pez_mar).get(1877) == 1 and dict(pez_mar).get(1883) == 1
      and all(c >= 1 for _, c in pez_mar),
      " ".join(f"{y}:{c}" for y, c in pez_mar))

# ——— I5: UI MarriageLineSynthesis v museum-atlas.tsx ———
ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I5 UI-MarriageLineSynthesis (importi + komponenta + render + 13-stolpcev + PEZDIRC-grafikon + niti + X-open)",
      "MARRIAGE_EARLY_LINE_YEARS" in ui and "function MarriageLineSynthesis()" in ui
      and "<MarriageLineSynthesis />" in ui and "PEZDIRC_MARRIAGE_PER_YEAR" in ui
      and "MARRIAGE_EARLY_THREADS" in ui and "MARRIAGE_EARLY_X_OPEN" in ui
      and "sinteza 13 let (1873–1885)" in ui and "X-open preostanki (P251-LEAD)" in ui,
      "render+imports OK")

# ——— I6: mejne variante 13 + FINIS-SODA + knjižno odpiranje v letnih karticah ———
variante = re.findall(r'boundaryVariant: "([^"]+)"', syn)
check("I6 13-boundaryVariant + FINIS-SODA-4-instance + 1873-KNIŽNO-ODPIRANJE",
      len(variante) == 13 and any("13. vrsta" in v for v in variante)
      and any("8. vrsta" in v for v in variante) and any("10. vrsta" in v for v in variante)
      and syn.count("1-8-7-4") + syn.count("1-8-7-6") >= 2
      and "KONČNA-POTRDITEV-KNIŽNEGA-ODPIRANJA" in syn
      and "m1–m17" in syn and "SAMO m18–m21" in syn,
      f"variante={len(variante)}")
restarti = re.findall(r'restart: "[^"]*"', syn)
check("I6b restart-vpis-1 dokumentiran 13/13 + FOLIACIJA-29/29-na-odprtanj",
      len(restarti) == 13 and "29/29! (pravilo-drži-NA-ODPIRANJU-knjige!)" in syn
      and "s2-'Pag. 1' NA ODPRTANJU" in syn,
      f"restarti={len(restarti)}")

# ——— I7: qa-parish.ts — qa-p252 sekcija + živi preveri vsako leto 1:1 ———
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st2012 = qa.count("HOUSE_VITALS.length !== 2012")
check("I7 qa-p252 (živi preveri vsako leto 1:1) + 2012-številcev + FINIS + 74/195-razcep",
      "qa-p252-parish-synthesis-04455-early" in qa and "MARRIAGE_EARLY_LINE_YEARS" in qa
      and "runtime !== yl.griblje" in qa and st2012 >= 100
      and 'p252Pre !== 74 || p252Line !== 195' in qa
      and "PEZDIRC_MARRIAGE_TOTAL !== 35" in qa and "SINTEZA-PREDZGODOVINE-KOMPLETNA" in qa,
      f"2012-številcev={st2012}")

# ——— I8: pt-luknja-18-final.json NESPREMENJEN (2012/269 — vsota 1:1!) ———
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I8 pt-luknja-2012/269 vsota-1:1 (korpus-NESPREMENJEN!)",
      '"vitalsTotal": 2012' in pt and '"04455": 269' in pt, "2012/269")

# ——— I9: README + worklog P252 vnos ———
rd = open(f"{ROOT}/README.md", encoding="utf-8").read()
wl = open(f"{ROOT}/worklog.md", encoding="utf-8").read()
check("I9 README (TOC-po-p252 + povzetek + tabela + korpus + odprto) + worklog-P252",
      "po-p252" in rd and "P252" in rd and "SINTEZA POROČNE PREDZGODOVINE" in rd
      and "266 vpisov" in rd and "74 blokov" in rd
      and "## P252 — SINTEZA POROČNE PREDZGODOVINE 04455" in wl
      and "13/13 KOMPLETNA" in wl,
      "README+worklog P252")

live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    try:
        with urllib.request.urlopen("http://localhost:3000/api/qa", timeout=60) as r:
            qa_live = json.load(r)
        p252_live = [t for t in qa_live["tests"] if t["id"] == "qa-p252-parish-synthesis-04455-early"]
        check("I10 LIVE /api/qa ok=True — pass=246 + p252-pass",
              qa_live.get("ok") is True and qa_live.get("passed") == 246 and p252_live and p252_live[0]["pass"] is True,
              f"pass={qa_live.get('passed')}")
    except Exception as e:
        check("I10 LIVE /api/qa", False, str(e)[:80])
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            check("I10b LIVE matricula-04455 HTTP 200 (križ-knjige!)", r.status == 200, f"status={r.status}")
    except Exception as e:
        check("I10b LIVE matricula-04455", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
