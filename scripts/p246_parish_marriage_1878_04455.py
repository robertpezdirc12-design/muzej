#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P246 — verifikator POROČNE PREDZGOVINE 04455, leto 1878 = 8/13 (I1–I10 + I11-foliacija/glava/margine + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1878,', src)
check("I1 bloki 04455/1878 == 7 (h2+h47+h63+h18+h23+h1+h36!)",
      len(bloki) == 7, f"najdeno {len(bloki)}: {','.join(bloki)}")
check("I1b vrstni-red-7 (2,47,63,18,23,1,36!-bloki-po-skenih-s20×4+s21+s23+s24!)",
      bloki == ["2", "47", "63", "18", "23", "1", "36"], ",".join(bloki))
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-1997 + 04455==254", "HOUSE_VITALS.length !== 1997" not in src and skupaj == 254, f"04455={skupaj}")

nove = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1878,\s*scan: (\d+),\s*page: (\d+),', src)
check("I3 skeni+pagi (20/19 ×4 · 21/20 · 23/22 · 24/23 — pag=sken−1!)",
      [b[1] for b in nove] == ["20", "20", "20", "20", "21", "23", "24"]
      and [b[2] for b in nove] == ["19", "19", "19", "19", "20", "22", "23"],
      ";".join(f"s{b[1]}/p{b[2]}" for b in nove))

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1878-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalie"], ensure_ascii=False)
check("I4 dokaz (23-vpisov + 7-Griblje + RESTART-s19-TOP-marginal-1-fizično + GLAVA-NI-ponovljena + meje!)",
      d["stats"]["entries"] == 23 and d["stats"]["gribljeMarriages"] == 7
      and "RESTART-1878 = s19-TOP" in d["frame"]["restart_varianta"]
      and "marginalna-številka-'1'-fizično-1:1" in d["frame"]["restart_varianta"]
      and "DISPENS-super-mixta-ac-prima" in d["frame"]["restart_varianta"]
      and "s18→s19" in d["frame"]["meja_1877_78"]
      and "s25→s26" in d["frame"]["meja_1878_79"]
      and "23-VPISOV-BREZ-PRESKOKOV" in d["frame"]["numbering"]
      and "NI-PONOVLJENA" in d["frame"]["glava_1878"]
      and "6/6-1878" in d["frame"]["foliacija"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']}")
check("I4b HRIŽAN-×3 + INTRA-×3 + h47-NOVA + hišna-sinhronizacija-9/10",
      "HRIŽAN-×3-BLOKI-V-1-LETU" in an
      and "INTRA-DVOJNI-BLOKI-×3" in an
      and "h47-NOVA-hiša-v-korpusu" in an
      and "9-od-10-hiš" in json.dumps(d.get("hišnaSinhronizacija", {}), ensure_ascii=False))
an2 = json.dumps(d, ensure_ascii=False)
check("I4c PEZDIRC-8.-leto-×2 + DOVGAN-8-let + MILEK-h65 + KELCHO-continuum + h43-BRULA",
      "8.-LETU" in an2 and "DOVGAN-CONTINUUM-PODALJŠAN-NA-8-LET" in an2
      and "MILEK-družina-h65-1.-POROČNI-DOKAZ" in an2.replace("h65-MILEK-družina-1.-POROČNI-DOKAZ", "MILEK-družina-h65-1.-POROČNI-DOKAZ")
      and "Kelcho" in an2 and "BRULA" in an2)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1997")
check("I5 qa-p246 + števec-1985 (×155!)", "HOUSE_VITALS.length !== 1978" not in qa and st >= 150, f"1997-številcev={st}")
check("I5b sidra-235 + 1878:7-P246 (qa-sidra-message)", "poročna sidra ≠ 247 (1875:1-P249! · 1876:6-P248! · 1877:5-P247! · 1878:7-P246!" in qa)
check("I5c dobe-209 + 39-pred-linijskih", "dobe-bloki ≠ 221/7/26" in qa and "51 pred-linijskih 1875-P249×1!+1876-P248×6!+1877-P247×5!" in qa)
check("I5d p80-1878:7-garda + sken-range-19–24", 'p80MarrAnchors.filter((h) => h.year === 1878).length !== 7' in qa and "skeni izven 19–24" in qa and "skeni izven 18–24" not in qa)

i0 = src.find("P246: POROČNA PREDZGOVINA 04455, leto 1878")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 23-VPISOV-BREZ-PRESKOKOV + RESTART-s19-TOP-marginal-1 + GLAVA-NI-ponovljena",
      "23-VPISOV-BREZ-PRESKOKOV" in seg and "RESTART-1878 = s19-TOP" in seg and "Šelah" in seg
      and "GLAVA-'1878'-NI-PONOVLJENA-NA-LISTIH" in seg and "9.-MEJNA-VARIANTA" in seg)
check("I6b meja-s18→s19 + meja-s25→s26-P245 + finis-2.-instance",
      "MEJA-1877/78 = s18→s19" in seg and "MEJA-1878/79 = s25→s26" in seg
      and "finis-pro-anno-1878" in seg and "2.-instance" in seg)
check("I6c 7-GRIBLJE-blokov + HRIŽAN-×3 + INTRA-×3 + hišna-sinhronizacija-9/10",
      "7-GRIBLJE-blokov" in seg and "HRIŽAN-×3-BLOKI-V-1-LETU" in seg and "×3-INTRA-DVOJNI-BLOKI" in seg
      and "hišna-sinhronizacija-9/10" in seg)
check("I6d PEZDIRC-8.-leto + DOVGAN-8-LET + foliacija-6/6-11/11",
      "PEZDIRC-×2-garble-v-8.-letu" in seg and "DOVGAN-CONTINUUM-8-LET" in seg
      and "FOLIACIJA-'Pag-=-sken−1'-6/6-1878" in seg and "11/11" in seg)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1878 (MARRIAGE_1878_*-izvozi!)", all(x in m for x in [
    "MARRIAGE_1878_BLOCKS", "MARRIAGE_1878_GRIBLJE", "MARRIAGE_1878_HOUSES", "MARRIAGE_1878_TOTAL",
    "MARRIAGE_1878_MEJA", "MARRIAGE_1878_NUMBERING", "FOLIACIJA_1878", "GLAVA_1878_NI",
    "HRIZAN_1878_TROJNA", "MILEK_1878_H65", "PEZDIRC_1878_KONTEKST", "DOVGAN_1878_PODALJŠITEV",
    "MARRIAGE_1878_DUELS", "MARRIAGE_1878_KONTEKST", "MARRIAGE_1878_KORPUS"]))
check("I7b korpus-1878-v-modulu (242/1985/235/209!)",
      "skupaj04455: 242" in m and "skupajVitals: 1985" in m and "sidra: 235" in m and "dobe: 209" in m)
check("I7c FOLIACIJA-6/6 + GLAVA-9.-VARIANTA-v-modulu",
      "6/6-1878" in m and "9.-MEJNA-VARIANTA" in m and "11/11-v-zaporednih-letih" in m)

pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I8a pt-luknja-1997 + byBook-04455=254 + P246-note",
      pt.get("vitalsTotal") == 1997 and pt.get("corpus", {}).get("byBook", {}).get("04455") == 254
      and "P246" in pt.get("corpus", {}).get("housesNote", ""),
      f"vitalsTotal={pt.get('vitalsTotal')} 04455={pt.get('corpus', {}).get('byBook', {}).get('04455')}")

ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I9 UI-MarriageEarly1878-v-ParishTab + importi + HRIŽAN-kartica!",
      "MarriageEarly1878" in ui and "HRIZAN_1878_TROJNA" in ui
      and "MILEK_1878_H65" in ui and "FOLIACIJA_1878" in ui and "GLAVA_1878_NI" in ui
      and "MARRIAGE_1878_KONTEKST" in ui and "MARRIAGE_1878_NUMBERING" in ui
      and "P246: poročna predzgodovina 04455 — leto 1878 = 8/13" in ui)
check("I9b worklog-P246-vnos", "## P246" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c stari-verifikatorji-na-živih-številkah",
      "1997" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py", encoding="utf-8").read()
      and "242" in open(f"{ROOT}/scripts/p242_parish_marriage_1881_04455.py", encoding="utf-8").read())

# ——— I11: foliacija/margine/glava-dokazi ————
check("I11a margine-fizično-Read-očesa-×6-strani (s19-1/2/3-s20-4/5/6/7-s21-8/9/10/11-s22-12/13/14-s23-15/16/17-s24-18/19/20/21!)",
      "s19-1/2/3" in an and "4/5/6/7" in an and "8/9/10/11" in an
      and "12/13/14" in an and "15/16/17" in an and "18/19/20/21" in an
      and "ŠTEVILČENJE-v-LEVI-MARGINI-POTRJENO-2.-LETO" in an)
check("I11b foliacija-VLM-misreadi-KOREKCIJA (s21-'21'-→-'20' + s24-'25'-→-'23'-10×!)",
      "s21-'21'-→-'20'" in an and "s24-'25'-→-'23'" in an and "10×" in an)
gl = json.dumps(d["frame"]["glava_1878"], ensure_ascii=False)
check("I11c glava-INLINE-v-1.-vpisu-vsakega-lista (s19-r1-s20-r4-s21-r8-s22-r12-s23-r15-s24-r18!)",
      "s19-r1-'1878-Jänner-16'" in gl and "s20-r4-'1878-Febr-20'" in gl and "s21-r8-'1878-Februar-24'" in gl
      and "s22-r12-'1878-Februar-27'" in gl and "s23-r15-'1878-Mai-26" in gl and "s24-r18-'1878-Juni-23'" in gl)
check("I11d 10×-hišne-številke-1:1 (m5-'47'-m6-'63'-m7-'18'/'65'-m11-'23'-m17-'35'-m21-'36'!)",
      "m5-'47'" in json.dumps(d["metoda"], ensure_ascii=False) and "m6-'63'" in json.dumps(d["metoda"], ensure_ascii=False)
      and "m17-'35'" in json.dumps(d["metoda"], ensure_ascii=False) and "m21-'36'" in json.dumps(d["metoda"], ensure_ascii=False))
check("I11e NODAT-0 + datumski-dueli + mladoletnica-v16",
      d.get("nodat") == 0 and "DATUMSKI-DUELI-1878" in an and "16-l-MLADOLETNICA" in an)

# ——— I10: QA-živo ———
try:
    r = urllib.request.Request("http://localhost:3000/api/qa")
    with urllib.request.urlopen(r, timeout=30) as resp:
        qa_data = json.load(resp)
    check("I10 QA-živo 245/245 ok:True (+qa-p246-id!)",
          qa_data.get("ok") is True and qa_data.get("passed") == 245 and qa_data.get("failed") == 0,
          f"passed={qa_data.get('passed')} failed={qa_data.get('failed')}")
except Exception as e:
    check("I10 QA-živo", False, str(e)[:80])

# ——— --live: Matricula-04455 ———
if "--live" in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                     headers={"User-Agent": "Mozilla/5.0 (p246-verifikator)"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.status
        check("I10b LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10b LIVE matricula-04455", False, str(e)[:60])

n = sum(1 for _, c, _ in results if c)
print(f"\nP246 verifikator: {n}/{len(results)} {'PASS ✓' if ok else 'FAIL ✗'}")
sys.exit(0 if ok else 1)
