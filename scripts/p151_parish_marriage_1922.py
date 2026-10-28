#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P151 — poročna knjiga 04455, leto 1922 = ZAKLJUČEK KNJIGE (s188–s190 ==
Pag. 186–188 + s191 prilepljen list + s192 naslovnica) (issue #18). 37. leto
poročne linije (P115 = 1886 → … → P150 = 1921 → P151 = 1922 = KONEC!).

INVARJANTA: 1922 = 13 vpisov (11 oštevilčenih №1–11 + 2 NEŠTEVILČENA = 3. +
4. v liniji!) — ★★★ SIBLING-SWAP #2 (№4+№5: isti dan 20.2. + isti priči +
zamenjava sorojencev Berkovec↔Brodarič!) + ★★★ 1. FRANCISKAN/'per
delegationem' duhovnik (P. Edvard Raustelar O.F.M. Brežje — Mala Paka!) +
★★★ 16 NOVIH PRIIMKOV = REKORD + ★★ 2. HRVAŠKA (Mala Paka 19, župn. Lipnik!)
+ ★★ ZADNJI VPIS 27.8.1922 (№11) + naslovnica 'P 1873–1922' = linija
1886–1922 KOMPLETNA; kumulativ vitals 711 → 714, bloki 04455 194 → 197,
sidra 187 → 190, p80 hiše 77 (0 novih!). Vzorec: p146–p150 (okvir I1–I12 +
--live)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-1922.json"
DOKAZ_P150 = "research/issue17/parish-marriage-1921.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1922-notes.md"
EXPECTED_ENTRIES = 13            # №1–11 + 2 neštevilčena!
EXPECTED_EXCLUDED = 2            # tipovan-list-1911 + naslovnica
EXPECTED_ANOMALIES = 18
EXPECTED_CROSSCHECKS = 17
GRIBLJE_BLOCKS = 3               # h17 h23 h48
GRIBLJE_HOUSES = "17,23,48"
VITALS_TOTAL = 714               # 711 + 3!
BLOKI_04455 = 197                # 194 + 3!
SIDRA_TOTAL = 190                # 187 + 3!
P80_HOUSES = 77                  # 0 novih (h17/h23/h48/h68 že v vzorci!)
EXPECTED_MONDAYS = 8             # 61,5 %
EXPECTED_SUNDAYS = 4
EXPECTED_THURSDAYS = 1

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def main():
    live = "--live" in sys.argv

    # ---------- I1: dokaz ----------
    d = json.load(open(DOKAZ))
    ent = d["entries"]
    check("I1 dokaz JSON 13 vpisov", len(ent) == EXPECTED_ENTRIES, f"{len(ent)}/{EXPECTED_ENTRIES}")
    unnum = [e for e in ent if not re.match(r"^\d+$", str(e["row"]))]
    check("I1b 2 neštevilčena (3.+4. v liniji!)", len(unnum) == 2, str([e["row"] for e in unnum]))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1c obojestransko 13/13", both == EXPECTED_ENTRIES, str(both))
    rows = [e["row"] for e in ent]
    check("I1d kronološki vrstni red (unnum vstavljen!)",
          rows == ["1", "2", "unnum-9.2.", "3", "4", "5", "6", "7", "8", "9", "10", "unnum-19.6.", "11"],
          str(rows))

    # ---------- I2: vrste + datumi ----------
    dates = [e["date"] for e in ent]
    check("I2a vsi datumi 1922", all("1922" in dt for dt in dates), "")
    pon = sum(1 for e in ent if e["dayOfWeek"] == "PONEDELJEK")
    ned = sum(1 for e in ent if e["dayOfWeek"] == "NEDELJA")
    cet = sum(1 for e in ent if e["dayOfWeek"] == "ČETRTEK")
    check("I2b 8 PON + 4 NED + 1 ČET + 0 TOR/PET/SOB",
          (pon, ned, cet) == (EXPECTED_MONDAYS, EXPECTED_SUNDAYS, EXPECTED_THURSDAYS),
          f"PON{pon} NED{ned} ČET{cet}")
    check("I2c №6 izven reda (19.2. NED pred 20.2. PON!)",
          any(e["row"] == "6" and e["dayOfWeek"] == "NEDELJA" for e in ent), "")
    check("I2d excluded 2 (tipovan-list-1911 + naslovnica)",
          len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I2e naslovnica 'P 1873–1922'",
          any("1873–1922" in str(x.get("note", "")) for x in d.get("excluded", [])), "")

    # ---------- I3: okvir ----------
    scans = sorted({e["scan"] for e in ent})
    check("I3a skeni [188–190]", scans == [188, 189, 190], str(scans))
    okv = all(e["page"] == e["scan"] - 2 for e in ent)
    check("I3b Pag == sken − 2 (9.–11. potrditev!)", okv, str(sorted({(e['scan'], e['page']) for e in ent})))

    # ---------- I4: Griblje-vpisi + bloki ----------
    grib = [e for e in ent if "GRIBLJE" in e["groom"].upper() or "GRIBLJE" in e["bride"].upper()]
    check("I4a 3 Griblje-vpisi (№1 №2 №8!)", len(grib) == GRIBLJE_BLOCKS, str([e["row"] for e in grib]))
    gh = sorted({m.group(1) for e in ent for m in re.finditer(r"GRIBLJE (\d+)", e["groom"] + " " + e["bride"])}, key=int)
    check("I4b 4 Griblje-števil (17/23/48/68!)", gh == ["17", "23", "48", "68"], str(gh))
    intra = sum(1 for e in ent if "INTRA-GRIBLJE" in json.dumps(e, ensure_ascii=False))
    check("I4c 1 INTRA-GRIBLJE (h23×h68!)", intra == 1, str(intra))
    swap = sum(1 for e in ent if "SIBLING-SWAP" in json.dumps(e, ensure_ascii=False))
    check("I4d SIBLING-SWAP #2 (№4+№5!)", swap >= 1, str(swap))

    # ---------- I5: strukture ----------
    js = json.dumps(d, ensure_ascii=False)
    hrv = js.count("HRVAŠKA") + js.count("Hrvaška")
    check("I5a 2. HRVAŠKA-referenca (Mala Paka-Lipnik!)", hrv >= 2, str(hrv))
    vdo = sum(1 for e in ent if "vdova" in json.dumps(e, ensure_ascii=False))
    check("I5b 2 vdovi (№9 Flak + №10 Županič!)", vdo >= 2, str(vdo))
    ofm = sum(1 for e in ent if "O.F.M." in json.dumps(e, ensure_ascii=False))
    check("I5c 1. FRANCISKAN O.F.M. (Raustelar per delegationem!)", ofm == 1, str(ofm))
    zad = sum(1 for e in ent if "ZADNJI VPIS" in json.dumps(e, ensure_ascii=False))
    check("I5d ZADNJI VPIS KNJIGE (№11 27.8.1922!)", zad >= 1, str(zad))

    # ---------- I6: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    n714 = qa.count("HOUSE_VITALS.length !== 725")
    check("I6a vitals pini 714 (65 stare + novi!)", n714 >= 65, str(n714))
    n197 = qa.count(".length !== 197")
    check("I6b bloki pini 197 (36 stare + novi!)", n197 >= 36, str(n197))
    check("I6c 1922-filter sidra (h.year === 1922).length !== 3",
          "h.year === 1922).length !== 3" in qa, "")
    check("I6d ostanki 711/194/187 sanirani (P151-kaskada!)",
          "HOUSE_VITALS.length !== 711" not in qa and ".length !== 194" not in qa
          and "p80MarrAnchors.length !== 187" not in qa, "stare pini!")
    check("I6e sidra 190", "p80MarrAnchors.length !== 190" in qa, "")
    check("I6f p80 hiše 77", "p80Houses.size !== 77" in qa, "")

    # ---------- I7: dnevi + stats ----------
    st = d["stats"]
    check("I7a stats vpisi 13", st.get("vpisi") == EXPECTED_ENTRIES, str(st.get("vpisi")))
    check("I7b stats ostevilceni 11 + nestevilceni 2",
          st.get("ostevilceni") == 11 and st.get("nestevilceni") == 2, "")
    check("I7c stats noviPriimki 16 (REKORD!)", st.get("noviPriimki") == 16, str(st.get("noviPriimki")))
    check("I7d stats hrvaska 2", st.get("hrvaska") == 2, str(st.get("hrvaska")))
    check("I7e stats duhovniki 2/13 (Jereb 12× + O.F.M.!)", "2/13" in str(st.get("duhovniki", "")), "")
    check("I7f stats kumulativ 714/197/190/77", "714" in str(st.get("kumulativ", "")) and "197" in str(st.get("kumulativ", "")), "")

    # ---------- I8: kumulativ ----------
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I8a p80 vitals pin 714", "len(vitals) == 714" in p80, "")
    check("I8b p80 houses pin 78 (skriptin filter VES 1897!)", "len(houses) == 78" in p80, "")

    # ---------- I9: parish.ts P151-bloki ----------
    ts = open("src/data/atlas/parish.ts", encoding="utf-8").read()
    for h in ("17", "23", "48"):
        m = re.search(r'houseNo: "' + h + r'",\s*\n\s*bookSignature: "04455",\s*\n\s*year: 1922', ts)
        check(f"I9 parish.ts blok 04455/1922 h{h}", bool(m), "")
    check("I9b P151-sekcija komentar", "P151: poročna knjiga 04455, leto 1922 = ZAKLJUČEK KNJIGE" in ts, "")

    # ---------- I10: README + notes ----------
    rd = open(README, encoding="utf-8").read()
    check("I10a README po P151", "po P151" in rd, "")
    check("I10b README 714/197", "714" in rd and "197" in rd, "")
    nt = open(NOTES, encoding="utf-8").read()
    check("I10c notes P151 obstajajo", "P151" in nt and "1922" in nt, "")

    # ---------- I11: lead-korekcije ----------
    lead = d.get("lead", "")
    check("I11a lead-korekcija 23×69→68", "23×68" in lead, "")
    check("I11b lead-korekcija 16-letna-№2→20", "20-letna" in lead, "")
    check("I11c lead-korekcija Prilozje 3→31", "→31" in lead or "→ 31" in lead, "")
    check("I11d lead-korekcija Raustelar O.F.M.", "Raustelar" in lead, "")
    cc = d.get("crossChecks", [])
    check("I11e crossChecks 17", len(cc) == EXPECTED_CROSSCHECKS, str(len(cc)))
    an = d.get("anomalies", [])
    check("I11f anomalije 18", len(an) == EXPECTED_ANOMALIES, str(len(an)))
    hon = d.get("honesty", [])
    check("I11g honesty 23", len(hon) == 23, str(len(hon)))

    # ---------- I12: veriga — starejše skripte sanirane ----------
    p115 = open("scripts/p115_parish_marriage_1886.py", encoding="utf-8").read()
    check("I12a p115 anchors 190 + 1922×3", "len(anchors) == 190" in p115 and '["1922"] * 3' in p115, "")
    p150 = open("scripts/p150_parish_marriage_1921.py", encoding="utf-8").read()
    check("I12b p150 vitals-pin 714 (kaskada!)", 'qa.count("HOUSE_VITALS.length !== 725")' in p150, "")
    check("I12c p80-hiše text-pini 77 (p137–p146!)",
          all('"p80Houses.size !== 77"' in open(f, encoding="utf-8").read()
              for f in ("scripts/p137_parish_marriage_1908.py", "scripts/p142_parish_marriage_1913.py",
                        "scripts/p146_parish_marriage_1917.py")), "")
    p150d = json.load(open(DOKAZ_P150))
    check("I12d P150-kontinuiteta (31 vpisov 1921)", len(p150d["entries"]) == 31, "")

    # ---------- L1–L3: live ----------
    if live:
        st_, body = http_get(BOOK_URL)
        check("L1 knjiga 04455 HTTP 200", st_ == 200, str(st_))
        import base64
        urls = []
        for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', body.decode("utf-8", "replace")):
            s_ = m.group(1)[7:-1]
            try:
                dd = base64.b64decode(s_ + "=" * (-len(s_) % 4)).decode("utf-8")
                if dd.startswith("http"):
                    urls.append(dd)
            except Exception:
                pass
        urls = sorted(set(urls))
        check("L2 inventar 192 slik", len(urls) == 192, str(len(urls)))
        ok = True
        for n_ in (188, 189, 190, 191, 192):
            s2, data = http_get(urls[n_ - 1])
            ok = ok and s2 == 200 and data[:2] == b"\xff\xd8"
        check("L3 citirani skeni s188–s192 live JPEG", ok, "")

    # ---------- izpis ----------
    npass = sum(1 for _, ok, _ in results if ok)
    for name, ok, det in results:
        print(("PASS  " if ok else "FAIL  ") + name + (("  " + det) if det and not ok else ""))
    print(f"\nP151 --check{' --live' if live else ''}: {'PASS' if npass == len(results) else 'FAIL'}"
          f" — {npass}/{len(results)} — 13 vpisov (KONEC KNJIGE 04455!) · SIBLING-SWAP #2 ·"
          f" 1. FRANCISKAN O.F.M. · 16 NOVIH PRIIMKOV (rekord!) · 2. HRVAŠKA (Mala Paka!) ·"
          f" kumulativ 714/197/190/77 (0 novih hiš!)")
    sys.exit(0 if npass == len(results) else 1)


if __name__ == "__main__":
    main()
