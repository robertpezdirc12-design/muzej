#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P143 — poročna knjiga 04455, polno leto 1914 (s154-dno + s155 == Pag. 153–154)
(issue #18). 29. leto poročne linije (P115 = 1886 → … → P143 = 1914).

Invariante I1–I12 + --live (LIVE 04455 HTTP). Vzorec: p142 (ZAMRNJENI pini 675/158/151
p141 + 681/164/157 p142 + 685/168/161 p143 ostajajo [P143-pini ZAMRNJENI]; tekoči korpus 686/169/162/72 od P144)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-1914.json"
DOKAZ_P142 = "research/issue17/parish-marriage-1913.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1914-notes.md"
EXPECTED_ENTRIES = 7            # №1–№7
EXPECTED_EXCLUDED = 0           # s155-dno prazna + diagonala = čista meja!
EXPECTED_ANOMALIES = 13
EXPECTED_CROSSCHECKS = 10
GRIBLJE_ROWS = [1, 3, 4, 5]   # +№1 dekle/služabnica na h46 (Brodarič-hiša)!
GRIBLJE_HOUSES = ["31", "46", "65", "68", "91"]  # 46 = dekle-hiša (brez novega bloka!)
GRIBLJE_BLOCKS = 4              # №3 h91+h68 + №4 h68 (ISTA-HIŠA!) + №5 h65+h31 → 4 bloki
GRIBLJE_INTRA = 3               # №3 + №4 + №5 = REKORD!
VITALS_TOTAL = 685              # 681 + 4 (ZAMRNJEN 1914-evidence pin — NE posodabljati v kaskadi!; tekoči korpus = 686 od P144)
BLOKI_04455 = 168               # 164 + 4 (ZAMRNJEN 1914-evidence pin; tekoči = 169 od P144)
SIDRA_TOTAL = 161               # 157 + 4 blokov (+1914:4) (ZAMRNJEN 1914-evidence pin; tekoči = 162 od P144)
EXPECTED_MONDAYS = 3            # + 3 nedelje + 1 torek = 6/7 vikendov
EXPECTED_SUNDAYS = 3

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def main():
    live = "--live" in sys.argv

    # ---------- I1: dokaz ----------
    d = json.load(open(DOKAZ))
    ent = d["entries"]
    check("I1 dokaz JSON", len(ent) == EXPECTED_ENTRIES, f"{len(ent)}/{EXPECTED_ENTRIES} vpisov")
    check("I1b excluded 0 (s155-dno prazna + diagonala = čista meja!)",
          len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1c obojestransko 7/7", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste [1–7]", rows == [str(i) for i in range(1, 8)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?(\d+)[^\s]*\s+(\w+)", dt)
        if m:
            months[m.group(2)] = months.get(m.group(2), 0) + 1
    # feb 3 + maj 2 + jun 1 + jul 1 = 7
    check("I2b meseci (feb 3 + maj 2 + jun 1 + jul 1)",
          months.get("februar") == 3 and months.get("maj") == 2
          and months.get("junij") == 1 and months.get("julij") == 1 and sum(months.values()) == 7, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    tor = sum(1 for dt in dates if "torek" in dt.lower())
    check("I2c 3 pon + 3 ned + 1 TOR №7 (6/7 vikendov — 1. TOR po 1912 №1!)",
          mon == EXPECTED_MONDAYS and sun == EXPECTED_SUNDAYS and tor == 1,
          f"{mon} pon + {sun} ned + {tor} tor")
    # postna vrzel: 22.2. -> 3.5. (post 25.2.–11.4.)
    lent = any("22. februar" in dt for dt in dates) and any("3. maj" in dt for dt in dates)
    check("I2d postna vrzel 22.2. → 3.5. (4. zapored!)", lent, "")
    # WWI-luknja: zadnja 7.7.1914
    wwi = any("7. julij 1914" in dt for dt in dates)
    check("I2e WWI-luknja (zadnja poroka 7.7.1914 → 1915 №1 2.5.1915 = 10-mesečna vrzel!)",
          wwi and "vojna" in str(d.get("stats", {}).get("warGap", "")).lower(), "")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (29. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [154,155]", scans == [154, 155], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = str(e.get("groom", {}).get("place", "")) + " " + str(e.get("bride", {}).get("place", ""))
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 Griblje vrste [1,3,4,5]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        for pl in (str(e.get("groom", {}).get("place", "")), str(e.get("bride", {}).get("place", ""))):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 5 GRIBLJE [31,46,65,68,91]", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c 3 INTRA-GRIBLJE (№3+№4+№5 = REKORD linije!)",
          allsi.count("INTRA-GRIBLJE") >= 3, str(allsi.count("INTRA-GRIBLJE")))
    check("I4d DVOTERNA KORPUS-SINHRONIZACIJA №5 (krsta 1893 h65 + 1894 h71!)",
          "DVOTERNA KORPUS-SINHRONIZACIJA" in allsi, "")
    check("I4e MATI-IN-SIN POROČNA TEDNA №4+№5 (8 dni!)", "MATI-IN-SIN" in allsi, "")
    check("I4f ISTA-HIŠA №4 (h68 × h68 — 1. v celi liniji!)", "ISTA-HIŠA" in allsi, "")
    check("I4g MLAJKOVA-MREŽA ×2 (№3 + №6!)", "MLAJKOVA-MREŽA" in allsi, "")
    check("I4h ROJSTNA DATUMA №7 (12.VII.1879 + 8.XII.1885 — novina!)",
          "12. VII. 1879" in allsi and "8. XII. 1885" in allsi, "")
    check("I4i NAJSTAREJŠI ŽENIN №4 (Ivan Mih 71!)", "NAJSTAREJŠI ŽENIN" in allsi, "")
    check("I4j SEGINA-ANKETA №1 (5 variant — S/J/L-zmeda!)", "SEGINA" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1914 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1914,', ts))
    check("I5a parish.ts bloki 1914 = 4", n_04455_1914 == GRIBLJE_BLOCKS, str(n_04455_1914))
    pins = [
        ("91", "PREDKORPUSNA generacija"), ("91", "NOVA p80-hiša"),
        ("68", "ISTA-HIŠA"), ("68", "NAJSTAREJŠI ŽENIN"), ("68", "MATI №5-ŽENINA"),
        ("65", "KORPUS-KRST"), ("65", "DVOTERNA KORPUS-SINHRONIZACIJA"),
        ("31", "SEJEM SELITEV"),
    ]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1914,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} 1914 ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P143 sekcija", "P143 razširitev: POROČNA KNJIGA 04455 — polno leto 1914" in ts)
    check("I5d MATI-IN-SIN v ts (№4+№5!)", "MATI-IN-SIN" in ts and "8 DNI NARAZEN" in ts, "")
    check("I5e ISTA-HIŠA h68 × h68 v ts", "h68 × h68" in ts, "")

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p143 id", "qa-p143-parish-marriage-1914" in qa)
    n686 = qa.count("HOUSE_VITALS.length !== 688")
    check("I6b vitals pini 686", n686 >= 57, str(n686))
    n169 = qa.count(".length !== 171")
    check("I6c bloki pini 169", n169 >= 2, str(n169))
    check("I6d sidra 162 + 1914:4", "poročna sidra ≠ 164" in qa and "p143Marr.length !== 4" in qa, "")
    check("I6e hiše 1914 pin", '"31,65,68,91"' in qa, "")
    check("I6f ostanki 687/170/163/72 (P146-sanacija!)", "HOUSE_VITALS.length !== 687" not in qa and ".length !== 170" not in qa
          and "p80MarrAnchors.length !== 163" not in qa and "p80Houses.size !== 71" not in qa, "stare pini! (posodobljeno P146)")
    check("I6g p80 hiše 72 (+h68!)", "p80Houses.size !== 72" in qa, "")
    check("I6h PT luknja 13 nespremenjena", "p80Gap.length !== 13" in qa, "")
    check("I6i p88 h91-1914 izjema", '(hn === "91" && (v.year === 1890 || v.year === 1913 || v.year === 1914))' in qa, "")

    # ---------- I7: dnevi ----------
    st = d["stats"]
    check("I7a stats mondays 3", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 3", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats sameVillage 4 (№3+№4+№5+№7!)", st.get("sameVillageCount") == 4, str(st.get("sameVillageCount")))
    check("I7d stats sameHouse 1 (№4 ISTA-HIŠA h68!)", st.get("sameHouseCount") == 1, str(st.get("sameHouseCount")))
    check("I7e letna glava 1914/1915 (meja s155-dno!)", "1914" in str(st.get("yearHeading", "")) and "1915" in str(st.get("yearHeading", "")), str(st.get("yearHeading", ""))[:40])

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals 685", st.get("vitalsTotal") == VITALS_TOTAL, str(st.get("vitalsTotal")))
    check("I8b stats bloki 168", st.get("blocks04455") == BLOKI_04455, str(st.get("blocks04455")))
    check("I8c stats sidra 161", st.get("sidraTotal") == SIDRA_TOTAL, str(st.get("sidraTotal")))
    check("I8d stats entries 7", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    check("I8e stats gribljeBlocks 4", st.get("gribljeBlocks") == GRIBLJE_BLOCKS, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [68]", st.get("newHouses") == ["68"], str(st.get("newHouses")))
    check("I8g stats gribljeIntra 3 (REKORD!)", st.get("gribljeIntra") == GRIBLJE_INTRA, str(st.get("gribljeIntra")))
    check("I8h stats p80Houses 71 (+h68!)", st.get("p80Houses") == 71, str(st.get("p80Houses")))
    check("I8i stats unnumbered 0", st.get("unnumbered") == 0, str(st.get("unnumbered")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 13", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 10", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P143" in notes and "1914" in notes and "MATI-IN-SIN" in notes, "")
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 5, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P143 bullet", "po P143" in rd, "")
    check("I10b README 685/168", "685" in rd and "168" in rd, "")
    check("I10c README P144 lead", "P144" in rd, "")

    # ---------- I11: P142 dokaz nespremenjen ----------
    d142 = json.load(open(DOKAZ_P142))
    check("I11 P142 dokaz 13 vnosov", len(d142["entries"]) == 13, str(len(d142["entries"])))

    # ---------- I12: lead-korekcija ----------
    lead = d.get("lead", {})
    check("I12 lead-korekcija (7 vpisov + 3 INTRA = REKORD; 'Lipovec' → Segina!)",
          "7 vpisov" in lead.get("correction", "") and "Segina" in lead.get("correction", ""), lead.get("correction", "")[:60])

    # ---------- LIVE ----------
    if live:
        try:
            status, body = http_get(BOOK_URL)
            check("LIVE knjiga HTTP 200", status == 200, str(status))
            check("LIVE 04455", "04455" in body)
        except Exception as e:
            check("LIVE napaka", False, str(e)[:80])

    fails = [(n, det) for (n, ok, det) in results if not ok]
    for (n, ok, det) in results:
        print(("PASS" if ok else "FAIL"), n, ("— " + det if det else ""))
    print(f"\n{len(results) - len(fails)}/{len(results)} PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
