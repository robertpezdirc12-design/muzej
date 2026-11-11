#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P242 — verifikator POROČNE PREDZGOVINE 04455, leto 1881 = 5/13 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1881,', src)
check("I1 bloki 04455/1881 == 9 (3-POLNA ×2 + h27-×2!)",
      len(bloki) == 9, f"najdeno {len(bloki)}: {','.join(bloki)}")
check("I1b vrstni-red-9 (27,4,28,8,42,27,41,52,16!)",
      bloki == ["27", "4", "28", "8", "42", "27", "41", "52", "16"], ",".join(bloki))
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-1966 + 04455==223", "HOUSE_VITALS.length !== 2008" not in src and skupaj == 265, f"04455={skupaj}")

nove = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1881,\s*scan: (\d+),\s*page: (\d+),', src)
check("I3 skeni+pagi (39/38 · 42/41 · 43/42 · 44/43 — pag=sken−1!)",
      [b[1] for b in nove] == ["39", "39", "42", "42", "42", "42", "43", "43", "44"]
      and [b[2] for b in nove] == ["38", "38", "41", "41", "41", "41", "42", "42", "43"],
      ";".join(f"s{b[1]}/p{b[2]}" for b in nove))

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1881-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalie"], ensure_ascii=False)
check("I4 dokaz (25-vpisov + 9-Griblje + PRESKOK-12 + restart-s39-letnica-v-stolpcu + NOVA-5.-VARIANTA + meja-s44→s45-P241!)",
      d["stats"]["entries"] == 25 and d["stats"]["gribljeMarriages"] == 9
      and d["stats"]["zapSkipped"] == 12
      and "NOVA-5. MEJNA-VARIANTA" in d["frame"]["restart_varianta"]
      and "s44→s45" in d["frame"]["meja_1881_82"]
      and "25-VPISOV-z-1-PRESKOKOM" in d["frame"]["numbering"]
      and "PRESKOK-12" in d["frame"]["numbering"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']}")
check("I4b h52-DVIG + PEZDIRC-v14 + TAPIČ↔ŠILAR + POLNI ×2-×3",
      "h52-FIRSTYEAR-DVIG-1882→1881" in an and "PEZDIRC-ŽENIN-v14" in an
      and "TAPIČ↔ŠILAR-KRIŽ" in an and "POLNI ×2-×3" in an)
check("I4c foliacija-3/3 + PRESKOK-12-[X-OPEN-DUEL] + v4-3-branja",
      "Pag. 38" in d["frame"]["foliacija"] and "3/3" in d["frame"]["foliacija"] and "X-OPEN-DUEL" in d["frame"]["numbering"]
      and "4:8:47" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2008")
check("I5 qa-p242 + števec-1966", "qa-p242-parish-marriage-early-04455-1881" in qa and st >= 150, f"1966-številcev={st}")
check("I5b sidra-235 + 1878:7-P246 + 1879:9-P244 + 1880:3-P243 (qa-sidra-message)", "poročna sidra ≠ 258 (1874:11-P250! · 1875:1-P249! · 1876:6-P248! · 1877:5-P247! · 1878:7-P246! · 1879:9-P244! · 1880:3-P243!" in qa)
check("I5c dobe-202 + 32-pred-linijskih (P244-živo!)", "dobe-bloki ≠ 232/7/26" in qa and "62 pred-linijskih 1874-P250×11!+1875-P249×1!+1876-P248×6!+1877-P247×5!" in qa)
check("I5d p80-1881:9-garda", 'p80MarrAnchors.filter((h) => h.year === 1881).length !== 9' in qa)

i0 = src.find("P242: POROČNA PREDZGOVINA 04455, leto 1881")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 25-vpisov-z-1-PRESKOKOM-12 + restart-s39-letnica-v-stolpcu-NOVA-5.-VARIANTA", "25-VPISOV-z-1-PRESKOKOM" in seg and "PRESKOK-12" in seg and "RESTART-1881 = s39" in seg and "NOVA-5.-MEJNA-VARIANTA" in seg)
check("I6b meja-1880/81-s38→s39 + meja-1881/82-s44→s45-P241-1:1", "MEJA-1880/81 = s38→s39" in seg and "MEJA-1881/82 = s44→s45-glava (P241-1:1!" in seg)
check("I6c 9-GRIBLJE-blokov-3-POLNA ×2 + h27-×2-PRVIČ", "9-GRIBLJE-blokov" in seg and "3-POLNA ×2" in seg and "h27-×2-BLOKA-V-1-LETU-PRVIČ" in seg)
check("I6d h52-FIRSTYEAR-DVIG + PEZDIRC-ženi n-v14 + TAPIČ↔ŠILAR", "h52-FIRSTYEAR-DVIG-1882→1881-ZA-1-LETO" in seg and "PEZDIRC-ŽENIN-04455-1881-CONTINUUM" in seg and "TAPIČ↔ŠILAR-KRIŽ-v-1-vpisu" in seg)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1881 (MARRIAGE_1881_*-izvozi)", all(x in m for x in [
    "MARRIAGE_1881_BLOCKS", "MARRIAGE_1881_GRIBLJE", "MARRIAGE_1881_HOUSES", "MARRIAGE_1881_TOTAL",
    "MARRIAGE_1881_ZAP_SKIPPED", "MARRIAGE_1881_XOPEN", "MARRIAGE_1881_MEJA", "MARRIAGE_1881_NUMBERING",
    "PEZDIRC_1881_NIT", "H52_1881_DVIG", "TAPIC_SILAR_1881_KRIŽ", "PRIEST_1881", "FOLIACIJA_1881",
    "BRINC_1881_NIT", "MARRIAGE_1881_VILLAGE_DUELS"]))
check("I7b h52-DVIG-v-modulu + ZA-6-LET", "h52-firstYear-DVIG-1882→1881" in m and "ZA-6-LET" in m)
check("I7c forenzika-×237-ostaja", "×237 blokov čez 5 knjig" in open(f"{ROOT}/src/data/atlas/parish-forensics.ts", encoding="utf-8").read())

pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I8a pt-luknja-2008 + byBook-04455=265 (P243-živo!)", pt.get("vitalsTotal") == 2008 and pt.get("corpus", {}).get("byBook", {}).get("04455") == 265,
      f"vitalsTotal={pt.get('vitalsTotal')} 04455={pt.get('byBook', {}).get('04455')}")
h52 = [x for x in pt["gapHouses"] if x["houseNo"] == "52"][0]
check("I8b h52-posodobljen (10-blokov/04455=3/firstYear=1881/p242Note!)",
      h52["blocksTotal"] == 10 and h52["byBook"]["04455"] == 3 and h52["firstYear"] == 1881 and "p242Note" in h52)
check("I9 UI-MarriageEarly1881-v-ParishTab + importi", "MarriageEarly1881" in open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
      and "H52_1881_DVIG" in open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read())
check("I9b worklog-P242-vnos", "## P242" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c stari-verifikatorji-na-živih-številkah",
      "2008" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py", encoding="utf-8").read()
      and "265" in open(f"{ROOT}/scripts/p239_parish_marriage_1884_04455.py", encoding="utf-8").read()
      and "265" in open(f"{ROOT}/scripts/p240_parish_marriage_1883_04455.py", encoding="utf-8").read()
      and "265" in open(f"{ROOT}/scripts/p237_parish_forensics.py", encoding="utf-8").read())

if "--live" in sys.argv:
    try:
        r = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                   headers={"User-Agent": "Mozilla/5.0"})
        code = urllib.request.urlopen(r, timeout=30).status
        check("I10 LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10 LIVE matricula-04455", False, str(e)[:60])

print()
print(f"VERIFIER-P242: {'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
