#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P247 — verifikator POROČNE PREDZGOVINE 04455, leto 1877 = 9/13 (I1–I10 + I11-foliacija/glava/re-numbering + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1877,', src)
check("I1 bloki 04455/1877 == 5 (h10+h8+h51+h51+h69!)",
      len(bloki) == 5, f"najdeno {len(bloki)}: {','.join(bloki)}")
check("I1b vrstni-red-5 (10,8,51,51,69!-bloki-po-skenih-s15×3+s16+s18!)",
      bloki == ["10", "8", "51", "51", "69"], ",".join(bloki))
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-2023 + 04455==269", "HOUSE_VITALS.length !== 2011" not in src and skupaj == 269, f"04455={skupaj}")

nove = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1877,\s*scan: (\d+),\s*page: (\d+),', src)
check("I3 skeni+pagi (15/14 ×3 · 16/15 · 18/17 — pag=sken−1!)",
      [b[1] for b in nove] == ["15", "15", "15", "16", "18"]
      and [b[2] for b in nove] == ["14", "14", "14", "15", "17"],
      ";".join(f"s{b[1]}/p{b[2]}" for b in nove))

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1877-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalie"], ensure_ascii=False)
check("I4 dokaz (18-vpisov + 5-Griblje + RESTART-s15-TOP + RE-NUMBERING-s18 + finis-1876 + meje!)",
      d["stats"]["entries"] == 18 and d["stats"]["gribljeMarriages"] == 5
      and "RESTART-1877 = s15-TOP" in d["frame"]["restart_varianta"]
      and "marginalna-'1'-fizično-1:1" in d["frame"]["restart_varianta"]
      and "s14→s15" in d["frame"]["meja_1876_77"]
      and "s18→s19" in d["frame"]["meja_1877_78"]
      and "18-VPISOV-BREZ-PRESKOKOV" in d["frame"]["numbering"]
      and "RE-NUMBERING-s18-+1-×4-PREČRTANIH" in d["frame"]["numbering"]
      and "NE-OBSTAJA" in d["frame"]["glava_1877"]
      and "4/4-1877" in d["frame"]["foliacija"]
      and "f i n i s / 1 8 7 6" in d["frame"]["finis_1876_s14"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']}")
check("I4b MOH-TROJČEK + MOH×BRODARIČ + h51-×2 + firstYear-×3",
      "MOH-TROJČEK-V-1-MESECU" in an and "MOH×BRODARIČ-DVOJNI-SORODSTVENI-ZAKON" in an
      and "h51-1.-04455-BLOK-KADARKOLI" in an
      and "firstYear-DVIG-×3" in an and "h10-1887→1877-ZA-10-LET" in an
      and "h69-1887→1877-ZA-10-LET" in an and "h8-1881→1877-ZA-4-LET" in an)
an2 = json.dumps(d, ensure_ascii=False)
check("I4c h51-1881-PARALELA + BRINC-v16 + PEZDIRC-9.-leto + DOVGAN-9-let + KLOŠTER-v17",
      "h51-1881-krst-MATI-Maria-BRODARIČ" in an2 and "BRINC" in an2
      and "9.-LETU" in an2 and "DOVGAN-CONTINUUM-PODALJŠAN-NA-9-LET" in an2
      and "KLO-ŠTER" in an2)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2023")
check("I5 qa-p247 + števec-2012 (×150!)", "HOUSE_VITALS.length !== 1985" not in qa and st >= 150, f"2012-številcev={st}")
check("I5b sidra-262 + 1877:5-P247 (qa-sidra-message)", "poročna sidra ≠ 262 (1873:4-P251! · 1874:11-P250! · 1875:1-P249! · 1876:6-P248! · 1877:5-P247!" in qa)
check("I5c dobe-214 + 44-pred-linijskih", "dobe-bloki ≠ 236/7/26" in qa and "66 pred-linijskih 1873-P251×4!+1874-P250×11!+1875-P249×1!+1876-P248×6!+1877-P247×5!" in qa)
check("I5d p80-1877:5-garda + sken-range-15–18", 'p80MarrAnchors.filter((h) => h.year === 1877).length !== 5' in qa and "skeni izven 15–18" in qa and "skeni izven 14–18" not in qa)

i0 = src.find("P247: POROČNA PREDZGOVINA 04455, leto 1877")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 18-VPISOV-BREZ-PRESKOKOV + RESTART-s15-TOP + GLAVA-NI-ponovljena",
      "18-VPISOV-BREZ-PRESKOKOV" in seg and "RESTART-1877 = s15-TOP" in seg and "Grubanič" in seg
      and "GLAVA-'1877'-NI-PONOVLJENA-NA-LISTIH" in seg and "POTRJENA-V-2.-LETU" in seg)
check("I6b meja-s14→s15 + finis-3.-instance + RE-NUMBERING",
      "MEJA-1876/77 = s14→s15" in seg and "MEJA-1877/78 = s18→s19" in seg
      and "finis-1876" in seg and "3.-instance" in seg and "RE-NUMBERING-s18-+1-×4-PREČRTANIH" in seg)
check("I6c 5-GRIBLJE-blokov + MOH-TROJČEK + MOH×BRODARIČ + h51-PT-luknja",
      "5-GRIBLJE-blokov" in seg and "MOH-TROJČEK-V-1-MESECU" in seg and "MOH×BRODARIČ-DVOJNI-SORODSTVENI-ZAKON" in seg
      and "h51-PT-LUKNJA-HIŠA" in seg)
check("I6d PEZDIRC-9.-leto + DOVGAN-9-LET + foliacija-4/4-15/15",
      "PEZDIRC-9.-leto-pošteno" in seg and "DOVGAN-CONTINUUM-9-LET" in seg
      and "FOLIACIJA-'Pag-=-sken−1'-4/4-1877" in seg and "15/15" in seg)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1877 (MARRIAGE_1877_*-izvozi!)", all(x in m for x in [
    "MARRIAGE_1877_BLOCKS", "MARRIAGE_1877_GRIBLJE", "MARRIAGE_1877_HOUSES", "MARRIAGE_1877_TOTAL",
    "MARRIAGE_1877_MEJA", "MARRIAGE_1877_NUMBERING", "FOLIACIJA_1877", "GLAVA_1877_INLINE",
    "MOH_1877_TROJCEK", "H51_1877_PT_LUKNJA", "FIRSTYEAR_1877_DVIG", "BRINC_1877_OPOMBA",
    "PEZDIRC_1877_KONTEKST", "DOVGAN_1877_PODALJŠITEV", "MARRIAGE_1877_DUELS", "MARRIAGE_1877_KONTEKST", "MARRIAGE_1877_KORPUS"]))
check("I7b korpus-1877-v-modulu (247/1990/240/214!)",
      "skupaj04455: 247" in m and "skupajVitals: 1990" in m and "sidra: 240" in m and "dobe: 214" in m)
check("I7c FOLIACIJA-4/4 + GLAVA-2.-LETO + MOH-TROJČEK-v-modulu",
      "4/4-1877" in m and "POTRJENA-V-2.-LETU" in m and "MOH-TROJČEK-V-1-MESECU-h51" in m)

pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
h51 = [x for x in pt["gapHouses"] if x["houseNo"] == "51"][0]
h53 = [x for x in pt["gapHouses"] if x["houseNo"] == "53"][0]
check("I8a pt-luknja-2008 + byBook-04455=265 + P247-note",
      pt.get("vitalsTotal") == 2023 and pt.get("corpus", {}).get("byBook", {}).get("04455") == 269
      and "P247" in pt.get("corpus", {}).get("housesNote", ""),
      f"vitalsTotal={pt.get('vitalsTotal')} 04455={pt.get('corpus', {}).get('byBook', {}).get('04455')}")
check("I8b h51-posodobljen (6-blokov/04455=2/firstYear=1877/p247Note!) + h53-intakten (22/4!)",
      h51["blocksTotal"] == 6 and h51["byBook"]["04455"] == 2 and h51["firstYear"] == 1877 and "p247Note" in h51
      and h53["blocksTotal"] == 22 and h53["byBook"]["04455"] == 4)

ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I9 UI-MarriageEarly1877-v-ParishTab + importi + MOH-kartica!",
      "MarriageEarly1877" in ui and "MOH_1877_TROJCEK" in ui
      and "H51_1877_PT_LUKNJA" in ui and "FOLIACIJA_1877" in ui and "GLAVA_1877_INLINE" in ui
      and "MARRIAGE_1877_KONTEKST" in ui and "MARRIAGE_1877_NUMBERING" in ui
      and "P247: poročna predzgodovina 04455 — leto 1877 = 9/13" in ui)
check("I9b worklog-P247-vnos", "## P247" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c stari-verifikatorji-na-živih-številkah",
      "2008" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py", encoding="utf-8").read()
      and "247" in open(f"{ROOT}/scripts/p242_parish_marriage_1881_04455.py", encoding="utf-8").read())

# ——— I10: QA-živo ———
try:
    r = urllib.request.Request("http://localhost:3000/api/qa")
    with urllib.request.urlopen(r, timeout=30) as resp:
        qa_data = json.load(resp)
    check("I10 QA-živo 248/248 ok:True (+qa-p247-id!)",
          qa_data.get("ok") is True and qa_data.get("passed") == 248 and qa_data.get("failed") == 0,
          f"passed={qa_data.get('passed')} failed={qa_data.get('failed')}")
except Exception as e:
    check("I10 QA-živo", False, str(e)[:80])

# ——— --live: Matricula-04455 ———
if "--live" in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                     headers={"User-Agent": "Mozilla/5.0 (p247-verifikator)"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.status
        check("I10b LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10b LIVE matricula-04455", False, str(e)[:60])

n = sum(1 for _, c, _ in results if c)
print(f"\nP247 verifikator: {n}/{len(results)} {'PASS ✓' if ok else 'FAIL ✗'}")
sys.exit(0 if ok else 1)
