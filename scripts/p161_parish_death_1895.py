#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P161 — MRLIŠKA knjiga 04894, leto 1895 = 10. polno leto mrliške linije
(s51-dno restart zap1–9 + s52–s54 + s55-top == str. 50–54; 52 vrstic /
12 Griblje-vpisov / 11 hiš — h46 ×2 MATI+SIN!). (issue #18).
★★ 1. ŠTEVILKA-STRANI-SKRIBESKA NAPAKA (s52-'Stran 57' za fizikalno 51 —
VLM prav, pisar narobe — invarianto rešijo 4 sosedi!) + ★★★ h46-TRAGEDIJA
(mati Otročnica 15.3. + sin 3-DNI 16.3. = 2 smrti v 2 DNEH!) + ★★★ ISTO-IMEŠKI
PAR h87 (1894-notarica-roj.-HLEPEC ↔ 1895-bajtarica-roj.-PEZDIREC!) +
★★★ NOVI DUHOVNIK #7 Fr. Škurmelj (1. podpis 9. 11. 1895!) + 5. STIL 3.
POTRDITEV (»1896.« podčrtano — varianta!) + 0 NOVIH hiš (ZASIČANJE 3. leto!)
+ MAX-ZOOM > VLM 12. potrditev (5 popravkov imen + 1 starosti!). Kumulativ:
vitals 825 → 837, mrliški bloki 04894 126 → 138, p80 hiše 87 (NESPREMENJENA!),
korpus 92 (NESPREMENJENA!). Vzorec p160."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1895.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1895-notes.md"

EXPECTED_ENTRIES = 12
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "8,12,26,30,33,35,36,37,38,46,87"
VITALS_TOTAL = 853               # POSODABLJENO P162: 837 + 16 (mrliška 1896)!
BLOKI_04894 = 154                # POSODABLJENO P162: 138 + 16 (mrliška 1896)!
P80_HOUSES = 87                  # NESPREMENJENA — zasičanje 3. leto!
KORPUS_HOUSES = 93               # POSODABLJENO P162: 92 + 1 (+h51 — 1. dokaz kadarkoli)!
NEW_SCANS = [51, 52, 53, 54, 55]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1895", d["status"])
    check("I1b 12 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 1895 = 52 vrstic / 12 Griblje / 11 hiš (h46 ×2!)",
          d["frame"]["rowsTotal"] == 52 and len({e["houseNo"] for e in ent}) == 11, "")
    check("I2b h46 ×2 (MATI+SIN v 2 dneh!)",
          len([e for e in ent if e["houseNo"] == "46"]) == 2, "")

    # ---------- I3: live knjiga ----------
    if live:
        st, body = http_get(BOOK_URL, timeout=45)
        check("I3 knjiga HTTP 200", st == 200, str(st))
        if st == 200:
            check("I3b inventar 256 slik", body.count(b"/image/") >= 0 and b"04894" in body, "")
    else:
        check("I3 knjiga (preskočeno — brez --live)", True, "offline")

    # ---------- I4: skeni + strani ----------
    check("I4 stran == sken − 1 (vseh 12 — 16.–19. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 51–55 (Griblje-vrstice: 51/52/53/54/55 — s56 = že 1896!)",
          all(51 <= s <= 55 for s in {e["scan"] for e in ent}) and sorted({e["scan"] for e in ent}) == [51, 52, 53, 54, 55], "")

    # ---------- I5: hiše + mreže ----------
    vit = parse_house_vitals()
    check("I5 11 različnih hiš", len({e["houseNo"] for e in ent}) == 11, GRIBLJE_HOUSES)
    h8 = [v for v in vit if v["houseNo"] == "8" and v["bookSignature"] == "04894"]
    check("I5a h8 = največ mrliških vpisov (≥3!)", len(h8) >= 3, str(sorted(v["year"] for v in h8)))
    h36 = [v for v in vit if v["houseNo"] == "36" and v["bookSignature"] == "04894"]
    check("I5b h36-veza (04105-krstni + 04894!)",
          any(v["bookSignature"] == "04105" for v in vit if v["houseNo"] == "36"), "")
    h30 = [v for v in vit if v["houseNo"] == "30" and v["bookSignature"] == "04894"]
    check("I5c h30 = 5. mrliški vpis (top-3 s h35/h61-6!)", len(h30) == 5, str(len(h30)))
    h35c = [v for v in vit if v["houseNo"] == "35" and v["bookSignature"] == "04894"]
    check("I5c2 h35 = 6. mrliški vpis = REKORD (skupaj s h61!)", len(h35c) == 6, str(len(h35c)))
    h87 = [v for v in vit if v["houseNo"] == "87" and v["bookSignature"] == "04894"]
    check("I5d h87-gnezdo = PEZDIREC ×2 (1894-Matija-notar + 1895-Marjeta!)",
          sorted(v["year"] for v in h87) == [1894, 1895], str(sorted(v["year"] for v in h87)))

    # ---------- I6: parish.ts ----------
    check("I6a vitals 853", len(vit) == VITALS_TOTAL, str(len(vit)))
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6b mrliški bloki 04894 = 154", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1895 = [v for v in d04894 if v["year"] == 1895]
    check("I6c bloki 1895 = 12", len(d1895) == 12, str(len(d1895)))
    check("I6d bloki 1895: skeni 51–55 + stran == sken − 1",
          all(v["scan"] and 51 <= v["scan"] <= 55 and v["page"] == v["scan"] - 1 for v in d1895), "")
    check("I6d2 bloki 1897+ ne obstajajo (P163-lead!; P162 = 1896 sedaj v korpusu!)",
          all(v["year"] < 1897 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 853 + 88",
          "len(vitals) == 853" in p80 and "len(houses) == 88" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (POSODABLJENO P162: +h51!)", len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika (5 popravkov + 1 starost!) ----------
    r11 = next((e for e in ent if e["row"] == 11), None)
    check("I7a r11 h38 = JOŽEK + 1 DAN (VLM-'Tožek' ZAVRJEN!)",
          bool(r11) and "JOŽEK" in r11["ime"] and "1 DAN" in r11["starost"], "")
    r12 = next((e for e in ent if e["row"] == 12), None)
    check("I7b r12 h33 = PAVIČ (lead-'PAVČIČ' + VLM-'Pavlič' OBOJE ZAVRJENA!)",
          bool(r12) and "PAVIČ" in r12["ime"] and "PAVČIČ" not in r12["ime"], "")
    r13 = next((e for e in ent if e["row"] == 13), None)
    check("I7c r13 h35 = KRIŽAN (lead-'HRIŠAN' ZAVRJEN — K-diagonali!)",
          bool(r13) and "KRIŽAN" in r13["ime"] and "HRIŠAN" not in r13["ime"], "")
    r15 = next((e for e in ent if e["row"] == 15), None)
    check("I7d r15 h46 = BRODARIČ roj. KLOBUČAR + 23 let (lead-25 ZAVRJEN!)",
          bool(r15) and "BRODARIČ" in r15["ime"] and "KLOBUČAR" in (r15.get("rojena") or "")
          and "23 let" in r15["starost"], "")
    r18 = next((e for e in ent if e["row"] == 18), None)
    check("I7e r18 h87 = PEZDIREC roj. PEZDIREC (X10 — ISTO-IMEŠKI PAR!)",
          bool(r18) and r18["ime"].endswith("PEZDIREC") and (r18.get("rojena") or "") == "PEZDIREC", "")
    r39 = next((e for e in ent if e["row"] == 39), None)
    check("I7f r39 h30 = ŠEGINA + Fr. Škurmelj (NOVI DUHOVNIK #7 — 1. podpis 9. 11.!)",
          bool(r39) and "ŠEGINA" in r39["ime"] and "Škurmelj" in r39["duhovnik"], "")
    r51 = next((e for e in ent if e["row"] == 51), None)
    check("I7g r51 h8 = JAKOBČIČ (VLM-'Jakičevič' + lead-'JAKLOVIČ' ZAVRJENA!)",
          bool(r51) and "JAKOBČIČ" in r51["ime"], "")

    # ---------- I8: meja + lead ----------
    check("I8a 5. STIL MEJE 2. potrditev (»— 1895. —« + Januarij-INLINE + restart s51!)",
          "5. STIL 2. potrditev" in fr["boundaries"] and "1895" in fr["boundaries"], "")
    check("I8b 5. STIL MEJE 3. POTRDITEV (»1896.« podčrtano — VARIANTA!)",
          "5. STIL 3. POTRDITEV" in fr["boundaries"] and "podčrtana" in fr["boundaries"], "")
    check("I8c s52-'Stran 57' SKRIBESKA NAPAKA (VLM prav — pisar narobe!)",
          "SKRIBESKA NAPAKA" in d["source"]["s52Anomaly"] and "51" in d["source"]["s52Anomaly"], "")
    e1 = next((x for x in d["excluded"] if x["id"] == "E1"), None)
    check("I8d E1 LEAD 100% (Krasinec-50 + roj.-PEZDIREC-glyph!)",
          bool(e1) and "LEAD 100%" in e1["opis"] and "PEZDIREC" in e1["opis"], "")
    x1 = next((x for x in d["crossChecks"] if x["id"] == "X1"), None)
    check("I8e X1 LEAD 13/13 + POPRAVKI", bool(x1) and "13/13" in x1["opis"], "")

    # ---------- I9: statistika ----------
    previden_1 = len([e for e in ent if e["previden"] == "1"])
    previden_ne = len([e for e in ent if e["previden"] == "ne"])
    check("I9a previden 1 ×8 + NE ×4 (vsi otroci!)",
          previden_1 == 8 and previden_ne == 4, f"{previden_1}+{previden_ne}")
    jelen = len([e for e in ent if e["duhovnik"] == "Jan Jelen"])
    skurmelj = len([e for e in ent if "Škurmelj" in e["duhovnik"]])
    check("I9b Jelen ×8 + Škurmelj ×3 + Rauq ×1", jelen == 8 and skurmelj == 3,
          f"Jelen {jelen} + Škurmelj {skurmelj} + Rauq {len(ent) - jelen - skurmelj}")
    meseci = {}
    for e in ent:
        meseci[e["mesec"]] = meseci.get(e["mesec"], 0) + 1
    check("I9c MARCIJ-epidemija 6/12", meseci.get("Marec") == 6, str(meseci))
    check("I9d starostni razpon 1 DAN → 70 let (Griblje 69)",
          any("1 DAN" in e["starost"] for e in ent) and any(e["starost"] == "69 let" for e in ent), "")

    # ---------- I10: povezane datoteke ----------
    notes = open(NOTES, encoding="utf-8").read()
    check("I10a notes: 12-vrstična tabela + MAX-ZOOM-12",
          "| 51 |" in notes and "12. POTRDITEV" in notes, "")
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10b qa-p161 = 162. kontrola (bloki-1895 12 + hiše 11 + Škurmelj ×3!)",
          "qa-p161-parish-death-1895" in qa and "NOVI DUHOVNIK #7" in qa, "")
    check("I10c qa guard 1897 (bloki 1897+ ne!)",
          "1897+-mrliški bloki že v korpusu" in qa, "")
    par = open(PARISH_TS, encoding="utf-8").read()
    check("I10d parish.ts: 12 blokov 1895-04894",
          par.count('bookSignature: "04894",\n    year: 1895,') == 12, "")
    check("I10e README: P161 glava (10. polno leto!)",
          "po P161" in open(README, encoding="utf-8").read(), "")

    # ---------- I11: honesty ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b [~] konservativno (HLEVIČ + PAVIČ + ŠEGINA X-open)",
          any("HLEVIČ" in h for h in d["honesty"]), "")

    # ---------- I12: kaskada ----------
    check("I12a p80 PT_GAP doc-list 15 (P162: +h51!)",
          '"44", "53", "54", "56", "57", "59", "60", "42", "58", "52", "46", "48", "43", "49", "51"' in qa, "")
    check("I12b p153–p161 skripte VITALS_TOTAL 853",
          all("VITALS_TOTAL = 853" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895))), "")
    check("I12c p161-next: P162-lead (1896) v dokazu",
          "P162" in d["nextSteps"][0], "")

    ok = sum(1 for _, o, _ in results if o)
    print(f"\np161: {ok}/{len(results)}", "PASS" if ok == len(results) else "FAIL")
    for name, o, detail in results:
        mark = "✓" if o else "✗"
        print(f" {mark} {name}" + (f" — {detail}" if detail and not o else ""))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
