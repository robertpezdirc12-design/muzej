#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P160 — MRLIŠKA knjiga 04894, leto 1894 = 9. polno leto mrliške linije
(s47-top + s48–s50 + s51-r50 == str. 46–49; 50 vrstic / 6 Griblje-vpisov /
6 hiš — VSE RAZLIČNE (87,57,49,35,72,24)!). (issue #18). ★★ LEAD 6/6 +
POPRAVKI ×3 (TERDIČEC→PEZDIREC-glyph + roj.-Klepec→HLEPEC + kolarica→
NOTARICA + 62-ne-82 + Fabjan→JAKOPIČ!) + ★★★ datum-forenzika (r20 = 19./20.
jul — Kurrent 2/9 — brez tega KRONOLOGIJA-PLOM!) + ★★ 2 PEZDIREC-hiši isto
leto (h87 + h57!) + Jetika ×14 REKORD LINIJE + Rana-na-nogi NOV vzrok +
2 duhovnika VZPOREDNO (Jelen ×23 + Rauq ×25 + zunanji + brez = 49/50!) +
meja 1894/95 = razporejeni-marker #2 + Jelen-podpis-V-MEJNI-VRSTI +
mrtvorojen-#5 (brez podpisa!) + nezakonska-#2 (Kolar!). Kumulativ:
vitals 819 → 825, mrliški bloki 04894 120 → 126, p80 hiše 86 (0 novih!),
korpus 93 (0 novih!). Vzorec p159."""
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

EXPECTED_ENTRIES = 6
EXPECTED_EXCLUDED = 7
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "24,35,49,57,72,87"
VITALS_TOTAL = 825               # 819 + 6!
BLOKI_04894 = 126                # 120 + 6!
P80_HOUSES = 87                  # 86 → 87 (+h49 EDINA nova — mrliška-1894, 15. dokazana luknja!)
KORPUS_HOUSES = 92               # 0 novih!
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
            mm = re.search(key + r":\s*(\d+)", o)
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
    fr = d["frame"]
    vit = parse_house_vitals()

    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1894", d["status"])
    check("I1b 6 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 7 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")
    check("I2 1894 = 50 vrstic / 6 Griblje / 6 hiš",
          fr["vrstic"] == 50 and len(ent) == 6, f"{fr['vrstic']}/{len(ent)}")
    check("I2b 6 hiš VSE RAZLIČNE (87,57,49,35,72,24 — po 1893-h32×2 spet 0!)",
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)))
    if live:
        st, body = http_get(BOOK_URL)
        check("I3 knjiga HTTP 200", st == 200, str(st))
        if st == 200:
            check("I3b inventar 04894", b"04894" in body, "")
    else:
        check("I3 knjiga (preskočeno — brez --live)", True, "offline")
    check("I4 stran == sken − 1 (vseh 6 — 15. potrditev!)",
          all(int(e["page"]) == int(e["scan"]) - 1 for e in ent), "")
    check("I4b skeni v naboru 47–51",
          all(47 <= int(e["scan"]) <= 51 for e in ent),
          ",".join(str(e["scan"]) for e in ent))
    check("I5 6 različnih hiš", len({e["houseNo"] for e in ent}) == 6, GRIBLJE_HOUSES)
    check("I5b h87 = 1. mrliški vpis (0 blokov 04894-h87 pred P160!)",
          not [v for v in vit if v["bookSignature"] == "04894" and v["houseNo"] == "87" and v["year"] < 1894], "")
    check("I5c h49 = 1. mrliški vpis (0 blokov 04894-h49 pred P160!)",
          not [v for v in vit if v["bookSignature"] == "04894" and v["houseNo"] == "49" and v["year"] < 1894], "")
    check("I5d h57 = 2. mrliški vpis (Rudolf-1892!)",
          len([v for v in vit if v["bookSignature"] == "04894" and v["houseNo"] == "57" and v["year"] <= 1894]) == 2, "")
    check("I5e h35 = 5. mrliški vpis (1887+1888×2+1890+1894 — največ!)",
          len([v for v in vit if v["bookSignature"] == "04894" and v["houseNo"] == "35" and v["year"] <= 1894]) == 5, "")
    check("I5f h72 = 3. + h24 = 3. mrliški vpis",
          len([v for v in vit if v["bookSignature"] == "04894" and v["houseNo"] == "72" and v["year"] <= 1894]) == 3
          and len([v for v in vit if v["bookSignature"] == "04894" and v["houseNo"] == "24" and v["year"] <= 1894]) == 3, "")
    check("I6a vitals 825", len(vit) == VITALS_TOTAL, str(len(vit)))
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6b mrliški bloki 04894 = 126", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1894 = [v for v in d04894 if v["year"] == 1894]
    check("I6c bloki 1894 = 6", len(d1894) == 6, str(len(d1894)))
    check("I6d bloki 1894: skeni 47–51 + stran == sken − 1",
          all(v["scan"] and 47 <= v["scan"] <= 51 and v["page"] == v["scan"] - 1 for v in d1894), "")
    check("I6d2 bloki 1895+ ne obstajajo (P161-lead!; P160 = 1894 v korpusu!)",
          all(v["year"] < 1895 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6e p80-skripta pini 825 + 87 (+h49 EDINA nova!)",
          "len(vitals) == 825" in p80 and "len(houses) == 87" in p80, "")
    check("I6f korpus = 92 hiš (0 novih!)",
          len({v["houseNo"] for v in vit if v["houseNo"].isdigit()}) == KORPUS_HOUSES,
          str(len({v["houseNo"] for v in vit if v["houseNo"].isdigit()})))
    # ——— LEAD + popravki
    r14 = next(e for e in ent if e["houseNo"] == "87")
    r22 = next(e for e in ent if e["houseNo"] == "57")
    r24 = next(e for e in ent if e["houseNo"] == "49")
    r30 = next(e for e in ent if e["houseNo"] == "35")
    r37 = next(e for e in ent if e["houseNo"] == "72")
    r38 = next(e for e in ent if e["houseNo"] == "24")
    check("I7a r14 = PEZDIREC roj. HLEPEC + NOTARICA + 62 (3 LEAD-popravki + 82 ZAVRJEN @8×!)",
          "PEZDIREC" in r14["ime"] and "HLEPEC" in r14["rojena"] and "notarica" in r14["stan"]
          and "62 let" in r14["starost"], f"{r14['ime']} | {r14['rojena']} | {r14['starost']}")
    check("I7b r14 blok-vsebina (whatSi: PEZDIREC + HLEPEC + NOTARICA + 62 let + VLM-'82'-ZAVRJEN)",
          any(v["houseNo"] == "87" and v["year"] == 1894 and "PEZDIREC" in v["whatSi"]
              and "HLEPEC" in v["whatSi"] and "NOTARICA" in v["whatSi"]
              and "62 let" in v["whatSi"] and "82' ZAVRJEN" in v["whatSi"] for v in d1894), "")
    check("I7c r22 = Janez PEZDIREC 1 mesec + pokop 1. 8. ('oktobr' ZAVRJEN @6×!)",
          "Janez PEZDIREC" in r22["ime"] and r22["starost"] == "1 mesec" and "1. 8." in r22["pokop"], "")
    check("I7d r24 = BRODARIČ roj. POGOREVC 53 (LEAD 100%!)",
          "BRODARIČ" in r24["ime"] and "POGOREVC" in r24["rojena"] and r24["starost"] == "53 let", "")
    check("I7e r30 = JAKOPIČ 4 dni (VLM 'Fabjan' ZAVRJEN!)",
          "JAKOPIČ" in r30["ime"] and r30["starost"] == "4 dni", "")
    check("I7f r37 = STRAUV Bele 1 leto (STRAUS-mreža #7!)",
          "STRAUV" in r37["ime"] and "Bele" in r37["bolezen"] and r37["starost"] == "1 leto", "")
    check("I7g r38 = BRINEC 1 leto (BRINEC-hiša 3. mrliški!)",
          "BRINEC" in r38["ime"] and r38["starost"] == "1 leto", "")
    # ——— datum-forenzika + meja
    check("I8a r22 pokop = 1. avg (diag-'oktobr' ZAVRJEN @6× — brez k-glyph!)",
          "avg" in r22["pokop"] and "ZAVRJEN" in r22["pokop"], r22["pokop"])
    check("I8b meja 1894/95 = razporejeni-marker (P158-stil #2) + Januarj + Jelen-V-MEJNI-VRSTI",
          "razporejeni-marker" in fr["meja1894_95"] and "V MEJNI VRSTI" in fr["meja1894_95"], fr["meja1894_95"][:60])
    check("I8c meseci = 50 (Jan2·Feb7·Mar3·Apr4·Jun1·Jul6·Avg3·Sep8·Okt2·Nov9·Dec5)",
          "Jan2·Feb7·Mar3·Apr4·Jun1·Jul6·Avg3·Sep8·Okt2·Nov9·Dec5 = 50" in fr["meseciSmrti"], fr["meseciSmrti"])
    check("I8d X2 datum-forenzika r20 = 19./20. jul (KRONOLOGIJA-PLOM brez!)",
          any("datum-forenzika" in c["name"] and "19./20." in c["detail"] for c in d["crossChecks"]), "")
    # ——— mreže + duhovniki
    check("I9a X7 6-hiš-vse-različne + h35-5.-vpis",
          any("87,57,49,35,72,24" in c["detail"] for c in d["crossChecks"]), "")
    check("I9b 2-PEZDIREC-hiši-isto-leto (A9)",
          any("2 PEZDIREC-hiše isto leto" in a["opis"] for a in d["anomalies"]), "")
    check("I9c duhovniki 49/50 (Jelen ×23 + Rauq ×25 + zunanji + brez)",
          d["stats"]["duhovniki"]["jelen"] == 23 and d["stats"]["duhovniki"]["rauq"] == 25
          and d["stats"]["duhovniki"]["podpisiRazmerje"].startswith("49/50"), "")
    check("I9d X10 max-zoom > VLM 11. potrditev (10 adjudikacij!)",
          any("11. potrditev" in c["detail"] for c in d["crossChecks"]), "")
    # ——— anomalije/honesty/leksikon
    check("I10a JETIKA ×14 = REKORD LINIJE (A6)",
          any("REKORD LINIJE" in a["opis"] and "×14" in a["opis"] for a in d["anomalies"]), "")
    check("I10b Rana-na-nogi = NOV VZROK (A5)",
          any("Rana na nogi" in a["opis"] for a in d["anomalies"]), "")
    check("I10c mrtvorojen-#5 brez podpisa (A7) + nezakonska-#2 Kolar (A8)",
          any("mrtvorojen-#5" in a["opis"] for a in d["anomalies"])
          and any("nezakonska-#2" in a["opis"] for a in d["anomalies"]), "")
    check("I10d rdeče oznake X9-4. leto",
          "X9-4. leto" in d["stats"]["redneOznake"], d["stats"]["redneOznake"])
    check("I10e honesty 10",
          len(d["honesty"]) == 10, str(len(d["honesty"])))
    # ——— parish.ts bloki
    src = open(PARISH_TS, encoding="utf-8").read()
    check("I11 6 blokov P160 v parish.ts (P160-sekcija)",
          src.count("year: 1894,") >= 6 and "P160: MRLIŠKA KNJIGA 04894" in src, "")
    # ——— qa-parish.ts
    qa = open(QA_TS, encoding="utf-8").read()
    check("I12 qa-p160 sekcija (161. kontrola)", "qa-p160-parish-death-1894" in qa, "")
    check("I12b qa-pini 825 (75×) + 126",
          qa.count("HOUSE_VITALS.length !== 825") == 75
          and "p80Death.length !== 126" in qa,
          f"{qa.count('HOUSE_VITALS.length !== 825')}×")
    # ——— README
    rd = open(README, encoding="utf-8").read()
    check("I13 README P160-vnos + glava-161",
          "P160" in rd and "qa-p160" in rd, "")
    # ——— P159-dokaz kontiniteta
    d159 = json.load(open(DOKAZ_P159, encoding="utf-8"))
    check("I14 P159-dokaz kontiniteta (10 vnosov 1893)",
          len(d159["entries"]) == 10, str(len(d159["entries"])))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p160: {ok}/{len(results)}")
    for name, o, det in results:
        mark = "✓" if o else "✗"
        print(f" {mark} {name}" + (f" — {det}" if det and not o else ""))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
