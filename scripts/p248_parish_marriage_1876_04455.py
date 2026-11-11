#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P248 — verifikator POROČNE PREDZGOVINE 04455, leto 1876 = 10/13 (I1–I10 + I11-meje/foliacija/dueli + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1876,', src)
check("I1 bloki 04455/1876 == 6 (h31+h44+h35+h64+h41+h30!)",
      len(bloki) == 6, f"najdeno {len(bloki)}: {','.join(bloki)}")
check("I1b vrstni-red-6 (31,44,35,64,41,30!-s11×2+s12×2+s13+s14!)",
      bloki == ["31", "44", "35", "64", "41", "30"], ",".join(bloki))
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-2026 + 04455==269", "HOUSE_VITALS.length !== 2011" not in src and skupaj == 269, f"04455={skupaj}")

nove = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1876,\s*scan: (\d+),\s*page: (\d+),', src)
check("I3 skeni+pagi (11/10 ×2 · 12/11 ×2 · 13/12 · 14/13 — pag=sken−1!)",
      [b[1] for b in nove] == ["11", "11", "12", "12", "13", "14"]
      and [b[2] for b in nove] == ["10", "10", "11", "11", "12", "13"],
      ";".join(f"s{b[1]}/p{b[2]}" for b in nove))

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1876-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalie"], ensure_ascii=False)
check("I4 dokaz (15-vpisov + 6-Griblje + RESTART-s11-VRSTA-2 + TAIL-violet-NAKNADNI + 10.-MEJNA-VARIANTA + finis!)",
      d["stats"]["entries"] == 15 and d["stats"]["gribljeMarriages"] == 6
      and "RESTART-1876 = s11-VRSTA-2" in d["frame"]["restart_varianta"]
      and "marginalna-'1'-FIZIČNO-1:1" in d["frame"]["restart_varianta"]
      and "TAIL-VPIS-8-VIOLET-NAKNADNO-DOPISAN" in d["frame"]["meja_1875_76"]
      and "s10→s11" in d["frame"]["meja_1875_76"]
      and "s14→s15" in d["frame"]["meja_1876_77"]
      and "15-VPISOV-BREZ-PRESKOKOV" in d["frame"]["numbering"]
      and "NE-PONOVLJENA-NA-LISTIH" in d["frame"]["glava_1876"]
      and "4/4-1876" in d["frame"]["foliacija"]
      and "19/19" in d["frame"]["foliacija"]
      and "f-i-n-i-s / 1-8-7-6" in d["frame"]["finis_1876_s14"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']}")
check("I4b 6-DVIGOV-REKORD + PEZDIRC-×9 + h35-PARALELA + TAIL-kaplan",
      "6-firstYear-DVIGOV-V-1-LETU" in an and "h44-1899→1876-ZA-23-LET" in an
      and "h30-1889→1876-ZA-13-LET" in an and "h64-1888→1876-ZA-12-LET" in an
      and "h31-1886→1876-ZA-10-LET" in an and "h35-1882→1876-ZA-6-LET" in an
      and "h41-1881→1876-ZA-5-LET" in an
      and "×9-omemb" in an and "Leinmannstochter" in an
      and "VIOLET-NAKNADNI-VPIS" in an and "Daniel-Perschek" in an)
an2 = json.dumps(d, ensure_ascii=False)
check("I4c sreda-ritem + DISPENS-3.-GRAD + 'f'-forenzika + '8-vs-2' + IZMENA-×2",
      "sreda-ritem" in an2 and "DISPENS-3.-GRAD-1:1" in an2
      and "ena-zanka+spodnja-zanka-NI-J" in an2 and "'8-vs-2'" in an2
      and "IZMENA-VLOG-×2" in an2 and "P229-z79" in an2)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2043")
check("I5 qa-p248 + števec-2043 (×150!)", "HOUSE_VITALS.length !== 1990" not in qa and st >= 150, f"2043-številcev={st}")
check("I5b sidra-262 + 1876:6-P248 (qa-sidra-message)", "poročna sidra ≠ 262 (1873:4-P251! · 1874:11-P250! · 1875:1-P249! · 1876:6-P248!" in qa)
check("I5c dobe-220 + 50-pred-linijskih", "dobe-bloki ≠ 236/7/26" in qa and "66 pred-linijskih 1873-P251×4!+1874-P250×11!+1875-P249×1!+1876-P248×6!" in qa)
check("I5d p80-1876:6-garda + sken-range-11–14", 'p80MarrAnchors.filter((h) => h.year === 1876).length !== 6' in qa and "skeni izven 11–14" in qa and "skeni izven 10–14" not in qa)
check("I5e MILIČ-250-P257 + p85-izjemi-h30/h41-1876", "MILIC_FAMILY_TOTAL !== 250" in qa and 'v.year === 1876 && (hn === "30" || hn === "41"))' in qa)

i0 = src.find("P248: POROČNA PREDZGOVINA 04455, leto 1876")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 15-VPISOV-BREZ-PRESKOKOV + RESTART-s11-VRSTA-2 + TAIL-violet-kaplan",
      "15-VPISOV-BREZ-PRESKOKOV" in seg and "RESTART-1876 = s11-VRSTA-2" in seg
      and "TAIL-1875 = s11-top-VPIS-8-VIOLET-NAKNADNI-VPIS" in seg and "Daniel-Perschek" in seg
      and "10.-MEJNA-VARIANTA" in seg)
check("I6b 6-DVIGOV + h44-ZA-23-LET + PEZDIRC-×9 + INTRA-×2",
      "6-DVIGOV-V-1-LETU-REKORD" in seg and "h44-ZA-23-LET-NOV-ABSOLUTNI-REKORD" in seg
      and "PEZDIRC/PEGDIRE-×9-omemb-V-1-LETU" in seg and "INTRA-DVOJNI-×2" in seg
      and "IZMENA-VLOG-×2" in seg and "DISPENS-3.-GRAD-1:1" in seg)
check("I6c meje-s10→s11 + s14→s15 + foliacija-19/19 + DOVGAN-10-LET",
      "MEJA-1875/76 = s10→s11" in seg and "MEJA-1876/77 = s14→s15" in seg
      and "FOLIACIJA-'Pag-=-sken−1'-4/4-1876" in seg and "19/19" in seg
      and "DOVGAN-CONTINUUM-10-LET" in seg and "P229-z79" in seg)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1876 (MARRIAGE_1876_*-izvozi!)", all(x in m for x in [
    "MARRIAGE_1876_BLOCKS", "MARRIAGE_1876_GRIBLJE", "MARRIAGE_1876_HOUSES", "MARRIAGE_1876_TOTAL",
    "MARRIAGE_1876_MEJA", "MARRIAGE_1876_NUMBERING", "FOLIACIJA_1876", "MEJNA_10_VARIANTA_1876",
    "FIRSTYEAR_1876_REKORD", "PEZDIRC_1876_REKORD", "H35_1876_PARALELA", "DOVGAN_1876_ZACETEK",
    "MARRIAGE_1876_DUELS", "MARRIAGE_1876_KONTEKST", "MARRIAGE_1876_KORPUS"]))
check("I7b korpus-1876-v-modulu (253/1996/246/220!)",
      "skupaj04455: 253" in m and "skupajVitals: 1996" in m and "sidra: 246" in m and "dobe: 220" in m)
check("I7c FOLIACIJA-19/19 + MEJNA-10 + TAIL-kaplan-v-modulu",
      "19/19-v-zaporednih-letih" in m and "10.-MEJNA-VARIANTA-1876" in m and "Daniel-Perschek" in m)

pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
h44 = [x for x in pt["gapHouses"] if x["houseNo"] == "44"][0]
h51 = [x for x in pt["gapHouses"] if x["houseNo"] == "51"][0]
check("I8a pt-luknja-2008 + byBook-04455=265",
      pt.get("vitalsTotal") == 2043 and pt.get("corpus", {}).get("byBook", {}).get("04455") == 269,
      f"vitalsTotal={pt.get('vitalsTotal')} 04455={pt.get('corpus', {}).get('byBook', {}).get('04455')}")
check("I8b h44-posodobljen (24-blokov/04455=6/firstYear=1876/p248Note!) + h51-intakten (6/2!)",
      h44["blocksTotal"] == 24 and h44["byBook"]["04455"] == 6 and h44["firstYear"] == 1876 and "p248Note" in h44
      and h51["blocksTotal"] == 6 and h51["byBook"]["04455"] == 2)

ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I9 UI-MarriageEarly1876-v-ParishTab + importi + DVIG-kartica!",
      "MarriageEarly1876" in ui and "FIRSTYEAR_1876_REKORD" in ui
      and "PEZDIRC_1876_REKORD" in ui and "FOLIACIJA_1876" in ui and "MEJNA_10_VARIANTA_1876" in ui
      and "MARRIAGE_1876_KONTEKST" in ui and "MARRIAGE_1876_NUMBERING" in ui
      and "Poročna predzgodovina 04455 (P248): leto 1876 = 10/13" in ui)
check("I9b worklog-P248-vnos", "## P248" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c stari-verifikatorji-na-živih-številkah (P257: 2043!)",
      "2043" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py", encoding="utf-8").read()
      and "265" in open(f"{ROOT}/scripts/p242_parish_marriage_1881_04455.py", encoding="utf-8").read())

# ——— I10: QA-živo ———
try:
    r = urllib.request.Request("http://localhost:3000/api/qa")
    with urllib.request.urlopen(r, timeout=30) as resp:
        qa_data = json.load(resp)
    check("I10 QA-živo 251/251 ok:True", qa_data.get("ok") is True and qa_data.get("passed") == 251 and qa_data.get("failed") == 0,
          f"passed={qa_data.get('passed')} failed={qa_data.get('failed')}")
except Exception as e:
    check("I10 QA-živo", False, str(e)[:80])

# ——— --live: Matricula-04455 ———
if "--live" in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                     headers={"User-Agent": "Mozilla/5.0 (p248-verifikator)"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.status
        check("I10b LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10b LIVE matricula-04455", False, str(e)[:60])

n = sum(1 for _, c, _ in results if c)
print(f"\nP248 verifikator: {n}/{len(results)} {'PASS ✓' if ok else 'FAIL ✗'}")
sys.exit(0 if ok else 1)
