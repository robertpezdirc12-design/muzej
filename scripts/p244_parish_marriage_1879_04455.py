#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P244 — verifikator POROČNE PREDZGOVINE 04455, leto 1879 = 7/13 (I1–I10 + I11-P245-KOREKCIJA + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1879,', src)
check("I1 bloki 04455/1879 == 9 (h16+h50+h61+h21+h32+h13+h42+h17+h16!)",
      len(bloki) == 9, f"najdeno {len(bloki)}: {','.join(bloki)}")
check("I1b vrstni-red-9 (16,50,61,21,32,13,42,17,16!-h16-×2!)",
      [b.replace(" [~]", "") for b in bloki] == ["16", "50", "61", "21", "32", "13", "42", "17", "16"],
      ",".join(bloki))
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-1997 + 04455==254", "HOUSE_VITALS.length !== 1997" not in src and skupaj == 254, f"04455={skupaj}")

nove = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1879,\s*scan: (\d+),\s*page: (\d+),', src)
check("I3 skeni+pagi (27/26 · 28/27 · 29/28 · 30/29 · 31/30 · 32/31 ×2 · 33/32 ×2 — pag=sken−1!)",
      [b[1] for b in nove] == ["27", "28", "29", "30", "31", "32", "32", "33", "33"]
      and [b[2] for b in nove] == ["26", "27", "28", "29", "30", "31", "31", "32", "32"],
      ";".join(f"s{b[1]}/p{b[2]}" for b in nove))

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1879-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalie"], ensure_ascii=False)
check("I4 dokaz (33-vpisov + 9-Griblje + P245-KOREKCIJA-restart-s26-TOP + GLAVA-ponovljena-ne-restart + meje!)",
      d["stats"]["entries"] == 33 and d["stats"]["gribljeMarriages"] == 9
      and "P245-KOREKCIJA" in d["frame"]["restart_varianta"]
      and "s26-TOP" in d["frame"]["restart_varianta"]
      and "Wilhelm-Fritz" in d["frame"]["restart_varianta"]
      and "LEVI-MARGINI" in d["frame"]["restart_varianta"]
      and "PONOVITEV-leto-na-vsakem-listu" in d["frame"]["restart_varianta"]
      and "s25→s26" in d["frame"]["meja_1878_79"]
      and "finis-pro-anno-1878" in d["frame"]["meja_1878_79"]
      and "s35-mid" in d["frame"]["meja_1879_80"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']}")
check("I4b h50-PT-luknja + h16-×2 + h63-KRIŽAN-2.-leto + FOLIACIJA-4/4-REŠITEV",
      "h50-PT-luknja-hiša-1.-poročni-dokaz-v-predzgodovini" in an
      and "h16-×2-BLOKA-V-1-LETU" in an
      and "h63-KRIŽAN-2.-LETO-ZAPORED" in an
      and "5/5-1879" in d["frame"]["foliacija"] and "Pag. 25" in d["frame"]["foliacija"] and "REŠEN" in d["frame"]["foliacija"])
an2 = json.dumps(d, ensure_ascii=False)
check("I4c PEZDIRC-7.-leto + DOVGAN-7-let + MILEH-križ + TRIPLE-DUEL-v1",
      "7.-LETU" in an2 and "DOVGAN-CONTINUUM-PODALJŠAN-NA-7-LET" in an2
      and "Mileh" in an2 and "TRIPLE-DUEL" in an2)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1997")
check("I5 qa-p244 + števec-1985 (×155!)", "qa-p244-parish-marriage-early-04455-1879" in qa and st >= 150, f"1997-številcev={st}")
check("I5b sidra-235 + 1878:7-P246 + 1879:9-P244 (qa-sidra-message)", "poročna sidra ≠ 247 (1875:1-P249! · 1876:6-P248! · 1877:5-P247! · 1878:7-P246! · 1879:9-P244!" in qa)
check("I5c dobe-209 + 39-pred-linijskih", "dobe-bloki ≠ 221/7/26" in qa and "51 pred-linijskih 1875-P249×1!+1876-P248×6!+1877-P247×5!" in qa)
check("I5d p80-1879:9-garda + sken-range-27–35", 'p80MarrAnchors.filter((h) => h.year === 1879).length !== 9' in qa and "skeni izven 26–35" in qa and "skeni izven 27–35" not in qa)

i0 = src.find("P244+P245-KOREKCIJA: POROČNA PREDZGOVINA 04455, leto 1879")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 33-VPISOV-BREZ-PRESKOKOV + P245-KOREKCIJA-RESTART-s26-top + GLAVA-PONOVLJENA",
      "33-VPISOV-BREZ-PRESKOKOV" in seg and "RESTART-1879 = s26-top" in seg and "Wilhelm-Fritz" in seg
      and "GLAVA-PONOVLJENA-NA-VSAKEM-RAZPRTEM-LISTU" in seg and "PONOVITEV-ne-restart-marker" in seg)
check("I6b meja-s25→s26 + finis-1878 + meja-s35-mid-P243 + NOVA-8.-VARIANTA",
      "MEJA-1878/79 = s25→s26" in seg and "finis-pro-anno-1878" in seg and "MEJA-1879/80 = s35-mid" in seg
      and "NOVA-8.-MEJNA-VARIANTA" in seg)
check("I6c 9-GRIBLJE-blokov + h50-PT + h16-×2 + h63-KRIŽAN-NIT-5-LET",
      "9-GRIBLJE-blokov" in seg and "h50-v7-PT-luknja-hiša-1.-poročni-dokaz" in seg
      and "h16-v4-×2-BLOKA-V-1-LETU" in seg and "NIT-5-LET" in seg)
check("I6d PEZDIRC-7.-leto + DOVGAN-podpis-Dopgan + MILEH-križ + Civil-Beizag",
      "PEZDIRC-×2-ženinov (v7+v21!)" in seg and "DOVGAN-continuum-SE-PODALJŠUJE-NA-7-LET-IN-ŠIRI-OD-v1" in seg
      and "Mileh" in seg and "Civil-Beizag" in seg)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1879 (MARRIAGE_1879_*-izvozi + P245-KOREKCIJA-izvozi!)", all(x in m for x in [
    "MARRIAGE_1879_KOREKCIJA", "MARGINA_1879_STEVILCENJE", "FINIS_1878_S25", "MARRIAGE_1879_KONTEKST",
    "MARRIAGE_1879_BLOCKS", "MARRIAGE_1879_GRIBLJE", "MARRIAGE_1879_HOUSES", "MARRIAGE_1879_TOTAL",
    "MARRIAGE_1879_MEJA", "MARRIAGE_1879_NUMBERING", "FOLIACIJA_1879_REŠITEV", "H50_1879_PT_LUKNJA",
    "H16_1879_DVOJNA", "KRIZAN_1879_NIT", "PEZDIRC_1879_CONTINUUM", "BRINC_1879_NIT",
    "DOVGAN_1879_PODALJŠITEV", "MILEK_1879_KRIZ", "MARRIAGE_1879_DUELS", "MARRIAGE_1879_KORPUS"]))
check("I7b korpus-1879-v-modulu (235/1978/228/202!)",
      "skupaj04455: 235" in m and "skupajVitals: 1978" in m and "sidra: 228" in m and "dobe: 202" in m)
check("I7c FOLIACIJA-REŠITEV-v-modulu + P243-DUEL-zaprt",
      "P243-s38-'Pag. 34.'-X-OPEN-DUEL-REŠEN" in m and "MISREAD-'37'" in m)

pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I8a pt-luknja-1997 + byBook-04455=254", pt.get("vitalsTotal") == 1997 and pt.get("corpus", {}).get("byBook", {}).get("04455") == 254,
      f"vitalsTotal={pt.get('vitalsTotal')} 04455={pt.get('corpus', {}).get('byBook', {}).get('04455')}")

ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I9 UI-MarriageEarly1879-v-ParishTab + importi + P245-KOREKCIJA-kartica!",
      "MarriageEarly1879" in ui and "H50_1879_PT_LUKNJA" in ui
      and "FOLIACIJA-REŠITEV: Pag = sken−1 5/5 v 1879" in ui
      and "P245-KOREKCIJA: P244-napaka razkrita in popravljena" in ui
      and "MARRIAGE_1879_KOREKCIJA" in ui and "MARGINA_1879_STEVILCENJE" in ui
      and "FINIS_1878_S25" in ui and "MARRIAGE_1879_KONTEKST" in ui)
check("I9b worklog-P244-vnos", "## P244" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c stari-verifikatorji-na-živih-številkah",
      "1997" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py", encoding="utf-8").read()
      and "235" in open(f"{ROOT}/scripts/p242_parish_marriage_1881_04455.py", encoding="utf-8").read())

# ——— I11: P245-KOREKCIJA ————
kj = json.dumps(d.get("korekcija", {}), ensure_ascii=False)
check("I11a JSON-korekcija-polje (razkritje + vzrok + dokazi + nespremenjeno)",
      d.get("korekcija", {}).get("faza") == "P245" and "s26 (ne s27!)" in kj
      and "pass-1-na-s26-vrnil-prazno" in kj.replace("PRAZNO", "prazno").replace("vrstic=0", "vrstic=0")
      and "6-VLM-pregledov" in kj and "33-vpisov-skupaj" in kj)
check("I11b bloki-vpis-korigirani (4-7-9-12-16-20-21-24-25!)",
      [b["vpis"] for b in d["bloki"]] == [4, 7, 9, 12, 16, 20, 21, 24, 25],
      ",".join(str(b["vpis"]) for b in d["bloki"]))
check("I11c anomalie-KOREKCIJA-vnosi (21-vnosov!-margina + finis + kontekst + Dovgan)",
      len(d["anomalie"]) == 21 and any("P245-KOREKCIJA-METODA" in a for a in d["anomalie"])
      and any("FINIS-PRO-ANNO-1878" in a for a in d["anomalie"])
      and any("KONTEKST-v1-v2-v3-v5" in a for a in d["anomalie"])
      and any("DOVGAN-od-PRVEGA-VPISA" in a for a in d["anomalie"]))
mk = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I11d modul-KOREKCIJA-vsebine (Fritz + margina + finis + kontekst + Dovgan-×3)",
      "RESTART-1879 = s26 (ne s27!)" in mk and "Wilhelm-Fritz" in mk
      and "natisnjen-Lfd.-stolpec-NE-OBSTAJA" in mk and "finis-pro-anno-1878" in mk
      and "Franz-Dovgan-podpis-×3-NA-s26" in mk and "6-[7]-8" in mk)
check("I11e parish.ts-KOREKCIJA-sekcija (P244+P245-KOREKCIJA-naslov!)",
      "P244+P245-KOREKCIJA: POROČNA PREDZGOVINA 04455" in src and "vpis 4" in src and "vpis 7" in src)

# ——— I10: QA-živo ———
try:
    r = urllib.request.Request("http://localhost:3000/api/qa")
    with urllib.request.urlopen(r, timeout=30) as resp:
        qa_data = json.load(resp)
    check("I10 QA-živo 245/245 ok:True (+qa-p244-id!)",
          qa_data.get("ok") is True and qa_data.get("passed") == 245 and qa_data.get("failed") == 0,
          f"passed={qa_data.get('passed')} failed={qa_data.get('failed')}")
except Exception as e:
    check("I10 QA-živo", False, str(e)[:80])

# ——— --live: Matricula-04455 ———
if "--live" in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            code = r.status
        check("I10b LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10b LIVE matricula-04455", False, str(e)[:60])

f = sum(1 for _, c, _ in results if not c)
print(f"\n{'='*56}\nP244 VERIFIKATOR: {len(results)-f}/{len(results)} PASS" + (" — VSI OK ✓" if f == 0 else f" — {f} FAIL!"))
sys.exit(0 if f == 0 else 1)
