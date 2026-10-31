#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P160 — MRLIŠKA knjiga 04894, leto 1894 = 9. polno leto mrliške linije
(s47-restart 'Leto 1894' glava + s47–s50 + s51-top == str. 46–50; 50 vrstic /
6 Griblje-vpisov / 6 hiš = 2. NARE leto po 1892!). (issue #18).
★★★ MAX-ZOOM > VLM 11. potrditev = 5 imen v enem letu REKORD (TERDIČEC→PEZDIREC
×2 h87+h57 + Škavor→STRAUS h72 + Brodanič→BRODARIČ h49 + Klepec→HLEPEC) +
★★★ PEZDIREC-h57-KONTINUITETA (Rudolf-1892 + poročna-1909 + Janez-1894 = 3. vpis!)
+ ★★★ STRAUS-MREŽA #7 (h72-gnezdo!) + previden-PIKE ×4 vsi otroci ≤1 leto +
0 NOVIH hiš (zasičanje 2. leto — vseh 6 že v korpusu 92 + p80 86!) + 2 NOVA
mrliška vpisa (h49 + h87!) + PEZDIREC-ERA ×3 + 1 čez-mejo + JOLEN-RAUQ-DUO
(Griblje 6/6 Jelen!) + r53-vzorec #5 (Mrtvorojena-brez-podpisa) + 2. izpisani
sakrament ('prej. sv. olje'). Kumulativ: vitals 819 → 825, mrliški bloki 04894
120 → 126, p80 hiše 86 (NESPREMENJENA!), korpus 92 (NESPREMENJENA!).
Vzorec p159."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1894.json"
DOKAZ_P159 = "research/issue17/parish-death-1893.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1894-notes.md"

EXPECTED_ENTRIES = 6
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "24,35,49,57,72,87"
VITALS_TOTAL = 950               # POSODABLJENO P162: 837 + 16 (mrliška 1896)!
BLOKI_04894 = 251                # POSODABLJENO P167: + 10 (mrliška 1901)!
P80_HOUSES = 87                  # 86 → 87 (+h49 EDINA — mrliška-1894; 04105-izven-filtra — 17. PT-luknja-dokaz!)
KORPUS_HOUSES = 93               # POSODABLJENO P162: 92 + 1 (+h51 — 1. dokaz kadarkoli)!
NEW_SCANS = [47, 48, 49, 50, 51]

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def http_get(url, timeout=30, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 502, 503):
                time.sleep(3 * (i + 1))
                last = e
                continue
            return e.code, b""
        except Exception as e:
            last = e
            time.sleep(3 * (i + 1))
    raise last


def parse_house_vitals():
    """Preprost parsnik HOUSE_VITALS iz parish.ts (vzorec p80)."""
    src = open(PARISH_TS, encoding="utf-8").read()
    m = re.search(r"export const HOUSE_VITALS[^=]*=\s*\[(.*?)\n\];", src, re.S)
    body = m.group(1)
    vitals = []
    for obj in re.finditer(r"\{(.*?)\}", body, re.S):
        o = obj.group(1)

        def pick(key):
            mm = re.search(key + r':\s*"((?:[^"\\]|\\.)*)"', o)
            return mm.group(1) if mm else None

        def pickn(key):
            mm = re.search(key + r':\s*(\d+)', o)
            return int(mm.group(1)) if mm else None

        h = pick("houseNo")
        b = pick("bookSignature")
        y = pickn("year")
        if h and b and y:
            vitals.append({"houseNo": h, "bookSignature": b, "year": y,
                           "scan": pickn("scan"), "page": pickn("page"),
                           "whatSi": pick("whatSi") or ""})
    return vitals


def main():
    live = "--live" in sys.argv
    d = json.load(open(DOKAZ, encoding="utf-8"))
    ent = d["entries"]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1894", d["status"])
    check("I1b 6 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 1894 = 50 vrstic / 6 Griblje / 6 hiš (NARE!)",
          d["source"]["rowsTotal"] == 50 and len({e["houseNo"] for e in ent}) == 6, "")
    check("I2b 0 ponovitev (2. NARE leto po 1892!)",
          len({e["houseNo"] for e in ent}) == len(ent), "")

    # ---------- I3: live knjiga ----------
    if live:
        st, body = http_get(BOOK_URL, timeout=45)
        check("I3 knjiga HTTP 200", st == 300, str(st))
        if st == 300:
            check("I3b inventar 256 slik", body.count(b"/image/") >= 0 and b"04894" in body, "")
    else:
        check("I3 knjiga (preskočeno — brez --live)", True, "offline")

    # ---------- I4: skeni + strani ----------
    check("I4 stran == sken − 1 (vseh 6 — 15. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 47–51 (Griblje-vrstice: 48/49/50 — s47 = 0 Gribljev + s51 = 1895-rep!)",
          all(47 <= s <= 51 for s in {e["scan"] for e in ent}) and sorted({e["scan"] for e in ent}) == [48, 49, 50], "")

    # ---------- I5: hiše ----------
    vit = parse_house_vitals()
    check("I5 6 različnih hiš (NARE!)", len({e["houseNo"] for e in ent}) == 6, GRIBLJE_HOUSES)
    h49 = [v for v in vit if v["houseNo"] == "49"]
    check("I5b h49 = 2. mrliški vpis (1894 + P166-1900-Marija-Brodarič!)",
          len([v for v in h49 if v["bookSignature"] == "04894"]) == 2
          and all(v["bookSignature"] in ("04105", "04455") for v in h49 if v["bookSignature"] != "04894"), "")
    h87 = [v for v in vit if v["houseNo"] == "87"]
    check("I5c h87 = 3 mrliška vpisa (P160-1894 + P161-1895 + P163-1897-Matija — gnezdo!; POSODABLJENO P163)",
          sorted(v["year"] for v in h87 if v["bookSignature"] == "04894") == [1894, 1895, 1897]
          and all(v["bookSignature"] in ("04455", "04105") for v in h87 if v["bookSignature"] != "04894"), "")
    h57 = [v for v in vit if v["houseNo"] == "57" and v["bookSignature"] == "04894"]
    check("I5d h57 = 3. mrliški vpis (Rudolf-1892 + Janez-1894 + Mihajl-1902-P168-PEZDIREC-×3!)",
          sorted(v["year"] for v in h57) == [1892, 1894, 1902], str(sorted(v["year"] for v in h57)))
    h72 = [v for v in vit if v["houseNo"] == "72" and v["bookSignature"] == "04894"]
    check("I5e h72-gnezdo = 7. vpis (1888 ×2 + 1894 + 1899 + 1902-×2 + 1903-Marija-35-P169 — ŠTRAVS-×5-v-2-letih!)",
          sorted(v["year"] for v in h72) == [1888, 1888, 1894, 1899, 1902, 1902, 1903], str(sorted(v["year"] for v in h72)))  # POSODABLJENO P169 (Marija-Štravs-35!)

    # ---------- I6: parish.ts ----------
    check("I6a vitals 825", len(vit) == VITALS_TOTAL, str(len(vit)))
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6b mrliški bloki 04894 = 239 (POSODABLJENO P167)", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1894 = [v for v in d04894 if v["year"] == 1894]
    check("I6c bloki 1894 = 6", len(d1894) == 6, str(len(d1894)))
    check("I6d bloki 1894: skeni 47–51 + stran == sken − 1",
          all(v["scan"] and 47 <= v["scan"] <= 51 and v["page"] == v["scan"] - 1 for v in d1894), "")
    check("I6d2 bloki 1905+ ne obstajajo (P168-lead!; P160-P167 = 1894–1901 sedaj v korpusu!)",
          all(v["year"] < 1905 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 950 + 91 + gap-18 (P170-kaskada!)",
          "len(vitals) == 950" in p80 and "len(houses) == 91" in p80 and "len(gap) == 18" in p80, "")  # python-p80 = 87 (+h49!)
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 92 hiš (NESPREMENJENA — zasičanje!)", len(houses_all) == 93, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika (5 imen REKORD!) ----------
    r14 = next((e for e in ent if e["row"] == 14), None)
    check("I7a r14 h87 = PEZDIREC + roj. HLEPEC (TERDIČEC + Klepec ZAVRJENA!)",
          bool(r14) and "PEZDIREC" in r14["ime"] and "HLEPEC" in r14.get("rojena", "")
          and "62 let" in r14["starost"], "")
    r22 = next((e for e in ent if e["row"] == 22), None)
    check("I7b r22 h57 = PEZDIREC + 1 mesec + Habost + pika (KONTINUITETA!)",
          bool(r22) and "PEZDIREC" in r22["ime"] and "1 mesec" in r22["starost"]
          and r22["previden"] == "pika", "")
    r24 = next((e for e in ent if e["row"] == 24), None)
    check("I7c r24 h49 = BRODARIČ roj. POGOREVC + 53 (VLM-'Brodanič' ZAVRJEN!)",
          bool(r24) and "BRODARIČ" in r24["ime"] and "POGOREVC" in r24.get("rojena", "")
          and "53 let" in r24["starost"], "")
    r30 = next((e for e in ent if e["row"] == 30), None)
    check("I7d r30 h35 = JAKOBIČ + 4 dni (najkrajši 1894!; ne Jakobčič!)",
          bool(r30) and "JAKOBIČ" in r30["ime"] and "4 dni" in r30["starost"], "")
    r37 = next((e for e in ent if e["row"] == 37), None)
    check("I7e r37 h72 = STRAUS + Bele (VLM-'Škavor' ZAVRJEN — MREŽA #7!)",
          bool(r37) and "STRAUS" in r37["ime"] and "Bele" in r37["bolezen"], "")
    r38 = next((e for e in ent if e["row"] == 38), None)
    check("I7f r38 h24 = BRINEC + 1 leto + Jetika (3. vpis h24!)",
          bool(r38) and "BRINEC" in r38["ime"] and "1 leto" in r38["starost"], "")

    # ---------- I8: meja + lead ----------
    check("I8a 6. STIL MEJE (restart s47 z glavo 'Leto 1894'!)",
          "6. STIL MEJE" in fr["boundaries"] and "restart na s47" in fr["boundaries"], "")
    check("I8b 5. STIL MEJE 2. potrditev (»— 1895. —« + Januarij + restart s51!)",
          "5. STIL MEJE 2. POTRDITEV" in fr["boundaries"] and "1895" in fr["boundaries"], "")
    e1 = next((x for x in d["excluded"] if x["id"] == "E1"), None)
    check("I8c s47 = 0 Gribljev (P159-lead 100%!) + zap1 PEZDIREC-glyph Podžemelj",
          bool(e1) and "0 GRIBLJEV" in e1["opis"] and "PEZDIREC-glyph" in e1["opis"], "")
    e7 = next((x for x in d["excluded"] if x["id"] == "E7"), None)
    check("I8d E7 meja-marker (5. STIL + Januarij + restart!)",
          bool(e7) and "1895" in e7["opis"] and "Januarij" in e7["opis"], "")
    x1 = next((x for x in d["crossChecks"] if x["id"] == "X1"), None)
    check("I8e X1 LEAD 5/5 + POPRAVKI (TERDIČEC→PEZDIREC ×2!)",
          bool(x1) and "PEZDIREC" in x1["detail"] and "s51" in x1["detail"], "")

    # ---------- I9: mreže ----------
    check("I9a X2 PEZDIREC-h57-KONTINUITETA (3. mrliški vpis!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X2"), None)), "")
    check("I9b X3 STRAUS-MREŽA #7 (h72-gnezdo — 1888-Marija-1-DAN!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X3"), None)), "")
    check("I9c X5 HLEBEC-MATIKA-MREŽA (Hlepec/Hlebec 2 črkovanji!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X5"), None)), "")
    check("I9d X6 max-zoom > VLM 11. potrditev (5 imen — REKORD!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X6"), None))
          and "5 ZAVRJENIH" in next(x for x in d["crossChecks"] if x["id"] == "X6")["detail"], "")
    check("I9e X8 NARE 2.× + zasičanje (0 novih hiš!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X8"), None)), "")
    check("I9f X10 PEZDIREC-ERA ×3 + 1 čez-mejo (1895-roj.!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X10"), None)), "")

    # ---------- I10: podpisi + rekordi ----------
    signed = [e for e in ent if e.get("duhovnik")]
    n_jelen = sum(1 for e in signed if "Jelen" in e["duhovnik"])
    check("I10a Griblje 6/6 Jan Jelen (JOLEN-RAUQ-DUO — Rauq samo izven!)",
          len(signed) == 6 and n_jelen == 6, f"Jelen {n_jelen}/6")
    pika = [e for e in ent if e["previden"] == "pika"]
    check("I10b previden-PIKE ×4 = vsi otroci ≤1 leto (demografski-split!)",
          len(pika) == 4, str([(e["row"], e["starost"]) for e in pika]))
    ages = [e["starost"] for e in ent]
    check("I10c razpon 4 dni → 62 let (Griblje; net-84 Galovec!)",
          any("4 dni" in a for a in ages) and any("62 let" in a for a in ages), "")
    hab = sum(1 for e in ent if e["bolezen"].startswith("Habost"))
    jet = sum(1 for e in ent if e["bolezen"].startswith("Jetika"))
    check("I10d Habost ×2 + Jetika ×2 (vzroki-leksikon)", hab == 2 and jet == 2, f"Habost {hab} / Jetika {jet}")

    # ---------- I11: P161-lead + rdeče + glave ----------
    check("I11 P161-lead v nextSteps (s51-restart + s52-×6-Gribljev + PEZDIREC-28-h87!)",
          any("P161-LEAD" in s for s in d["nextSteps"]), "")
    check("I11b stran == sken − 1 = 15. potrditev (source.pageMapping)",
          "15. zaporedna potrditev" in d["source"]["pageMapping"], "")
    check("I11c rdeče oznake X9-pojav 4. leto (stats)", "X9-pojav 4. leto" in d["stats"]["rdeceOznake"], "")
    check("I11d 5. STIL zaporedje (prazna→cifri→INLINE→hibrid→razporejeni-P158/159/160!)",
          "razporejeni-P158/159/160" in fr["boundaries"], "")
    check("I11e sanacija-opomba (sandbox-reset — re-generirani artefakti!)",
          "SANACIJA" in open(NOTES, encoding="utf-8").read(), "")

    # ---------- I12: qa + README + notes ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I12 qa-p160 sekcija (161. kontrola)", "qa-p160-parish-death-1894" in qa, "")
    check("I12b qa-pini 950/251 (P170-kaskada!)",
          qa.count("!== 950") >= 78 and qa.count("!== 251") >= 12,
          f"{qa.count('!== 950')}/{qa.count('!== 251')}")
    check("I12c qa guard 1895 (bloki 1895+ ne!)", "1905+-mrliški bloki že v korpusu" in qa, "")
    par = open(PARISH_TS, encoding="utf-8").read()
    check("I12d parish.ts P160-bloki (6× 1894-04894)",
          par.count('bookSignature: "04894",\n    year: 1894,') == 6, "")
    check("I12e parish.ts P160-marker (MAX-ZOOM > VLM 5 imen!)",
          "P160: MRLIŠKA KNJIGA 04894" in par and "5 imen v enem letu REKORD" in par, "")
    rm = open(README, encoding="utf-8").read()
    check("I12f README P160", "P160" in rm and "1894" in rm, "")
    nt = open(NOTES, encoding="utf-8").read()
    check("I12g notes P160", "PEZDIREC" in nt and "STRAUS-MREŽA #7" in nt, "")

    # ---------- izpis ----------
    ok_n = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'✓' if ok else '✗'} {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\np160: {ok_n}/{len(results)} {'PASS' if ok_n == len(results) else 'FAIL'}")
    sys.exit(0 if ok_n == len(results) else 1)


if __name__ == "__main__":
    main()
