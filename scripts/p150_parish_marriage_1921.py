#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P150 — poročna knjiga 04455, polno leto 1921 (s182-dno + s183–s187 == Pag.
180–185) (issue #18). 36. leto poročne linije (P115 = 1886 → … → P149 = 1920 →
P150 = 1921).

INVARJANTA: 1921 = 3. NAJVEČJE LETO LINIJE — 31 vpisov (1919:40 → 1920:37 →
1921:31; P149-lead napovedal 14 — PODCENITEV ×2,2!). ★★★ 2 RAZVEZI-LISTINE
(1. v liniji — škof. ord. LJUBLJANA ×2!) + ★★★ 1. HRVAŠKA (Kaluka 41 (Hrv.) +
potrdilo žup. Lipik/Lipnik!) + ★★ 6 INTRA-HIŠE = REKORD + 5 INTRA-GRIBLJE (13
Griblje-števil!) + ★★ 2 NOVI HIŠI (h92 = 1. dokaz NAJVIŠJE številke — maksimum
po h87! + h72!) + 4 POROKE 21.11. + ŽUPNIK-MENJAVA SREDI LETA (Cerar → P.
Remigi JEREB!) + 113-dnevna poletna vrzel + 1. DATUM-NEOBSTOJI (31. 6.!) +
MATIČAR-PODPIS (1.) + 5 anotacij †1976–81: kumulativ vitals 702 → 710, bloki
04455 185 → 193, sidra 178 → 186, p80 hiše 75 → 77 (+h92/h72).
Vzorec: p146–p149 (okvir I1–I12 + --live) + p130 (veliko-leto)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-1921.json"
DOKAZ_P149 = "research/issue17/parish-marriage-1920.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1921-notes.md"
EXPECTED_ENTRIES = 31            # №1–31 (vse oštevilčene!)
EXPECTED_EXCLUDED = 5            # meja-1920/21 + 3× 1922-lead + tipovan-list-1911
EXPECTED_ANOMALIES = 17
EXPECTED_CROSSCHECKS = 14
GRIBLJE_BLOCKS = 9               # h63 h68 h64 h53 h59 h92 h72 h10 h7
GRIBLJE_HOUSES = "7,10,53,59,63,64,68,72,92"
NEW_HOUSES = ["72", "92"]
VITALS_TOTAL = 711               # 702 + 9!
BLOKI_04455 = 194                # 185 + 9!
SIDRA_TOTAL = 187                # 178 + 9!
P80_HOUSES = 77                  # 75 + h92 + h72!
EXPECTED_MONDAYS = 13            # 41,9 %
EXPECTED_SUNDAYS = 9
EXPECTED_WEDNESDAYS = 4
EXPECTED_TUESDAYS = 2
EXPECTED_FRIDAYS = 3

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
    check("I1 dokaz JSON 31 vpisov", len(ent) == EXPECTED_ENTRIES, f"{len(ent)}/{EXPECTED_ENTRIES}")
    unnum = [e for e in ent if not re.match(r"^\d+$", str(e["row"]))]
    check("I1b 0 neštevilčenih (vsi №1–31!)", len(unnum) == 0, str([e["row"] for e in unnum]))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1c obojestransko 31/31", both == EXPECTED_ENTRIES, str(both))
    rows = [int(e["row"]) for e in ent]
    check("I1d zaporedje №1–31 brez presledkov", rows == list(range(1, 32)), str(rows))

    # ---------- I2: vrste + datumi ----------
    dates = [e["date"] for e in ent]
    check("I2a vsi datumi 1921", all("1921" in dt for dt in dates), "")
    pon = sum(1 for e in ent if e["dayOfWeek"] == "PONEDELJEK")
    ned = sum(1 for e in ent if e["dayOfWeek"] == "NEDELJA")
    sre = sum(1 for e in ent if e["dayOfWeek"] == "SREDA")
    tor = sum(1 for e in ent if e["dayOfWeek"] == "TOREK")
    pet = sum(1 for e in ent if e["dayOfWeek"] == "PETEK")
    check("I2b 13 PON + 9 NED + 4 SRE + 2 TOR + 3 PET + 0 SOB",
          (pon, ned, sre, tor, pet) == (EXPECTED_MONDAYS, EXPECTED_SUNDAYS, EXPECTED_WEDNESDAYS, EXPECTED_TUESDAYS, EXPECTED_FRIDAYS),
          f"PON{pon} NED{ned} SRE{sre} TOR{tor} PET{pet}")
    check("I2c meja-1920/21 v excluded (veliki cifri 20|21!)",
          any("meja-1920/1921" in str(x.get("row", "")) for x in d.get("excluded", [])), "")
    check("I2d excluded 5 (meja + 3× 1922-lead + tipovan-list)",
          len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I2e 1922-lead: ZADNJI VPIS KNJIGE 27.8.1922",
          any("27. 8. 1922" in str(x.get("note", "")) for x in d.get("excluded", [])), "")

    # ---------- I3: okvir ----------
    scans = sorted({e["scan"] for e in ent})
    check("I3a skeni [182–187]", scans == [182, 183, 184, 185, 186, 187], str(scans))
    okv = all(e["page"] == e["scan"] - 2 for e in ent)
    check("I3b Pag == sken − 2 (nova preslikava, 8. potrditev!)", okv, str(sorted({(e['scan'], e['page']) for e in ent})))

    # ---------- I4: Griblje-vpisi + bloki ----------
    grib = [e for e in ent if "GRIBLJE" in e["groom"].upper() or "GRIBLJE" in e["bride"].upper()]
    check("I4a 9 Griblje-vpisov (incl. №27 h7!)", len(grib) == GRIBLJE_BLOCKS, str([e["row"] for e in grib]))
    gh = sorted({m.group(1) for e in ent for m in re.finditer(r"GRIBLJE (\d+)", e["groom"] + " " + e["bride"])}, key=int)
    check("I4b 13 Griblje-števil", len(gh) == 13, str(gh))
    intra = sum(1 for e in ent if "INTRA-GRIBLJE" in json.dumps(e, ensure_ascii=False))
    check("I4c 5 INTRA-GRIBLJE (rekord-serija!)", intra == 5, str(intra))

    # ---------- I5: strukture ----------
    ihis = sum(1 for e in ent if "INTRA-HIŠA" in json.dumps(e, ensure_ascii=False))
    check("I5a 6 INTRA-HIŠE (rekord linije!)", ihis == 6, str(ihis))
    raz = sum(1 for e in ent if "RAZVEZ" in json.dumps(e, ensure_ascii=False))
    check("I5b 2 RAZVEZI (1. v liniji — LJUBLJANA ×2!)", raz == 2, str(raz))
    hrv = sum(1 for e in ent if "HRV" in json.dumps(e, ensure_ascii=False))
    check("I5c 1. HRVAŠKA (№28 Kaluka 41!)", hrv >= 1, str(hrv))

    # ---------- I6: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    n710 = qa.count("HOUSE_VITALS.length !== 711")
    check("I6a vitals pini 711", n710 >= 64, str(n710))
    n193 = qa.count(".length !== 194")
    check("I6b bloki pini 194", n193 >= 35, str(n193))
    check("I6c 1921-filter sidra (h.year === 1921).length !== 9",
          "h.year === 1921).length !== 9" in qa, "")
    check("I6d ostanki 702/185/178/75 sanirani (P150-kaskada!)",
          "HOUSE_VITALS.length !== 702" not in qa and ".length !== 185" not in qa
          and "poročna sidra ≠ 178" not in qa and "p80Houses.size !== 75" not in qa, "stare pini!")
    check("I6e sidra 187", "poročna sidra ≠ 187" in qa, "")
    check("I6f p80 hiše 77", "p80Houses.size !== 77" in qa, "")

    # ---------- I7: dnevi + stats ----------
    st = d["stats"]
    check("I7a stats mondays 13", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 9", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats intraHouse 6", st.get("intraHouseCount") == 6, str(st.get("intraHouseCount")))
    check("I7d stats gribljeBlocks 9", st.get("gribljeBlocks") == GRIBLJE_BLOCKS, str(st.get("gribljeBlocks")))
    check("I7e stats newHouses [72, 92]", st.get("newHouses") == NEW_HOUSES, str(st.get("newHouses")))

    # ---------- I8: kumulativ 710/193/186/77 ----------
    check("I8a stats entries 31", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I8b p80 vitals pin 710", "len(vitals) == 711" in p80, "")
    check("I8c p80 houses pin 78 (skriptin filter VES 1897 = +h45!)", "len(houses) == 78" in p80, "")

    # ---------- I9: parish.ts P150-bloki ----------
    ts = open("src/data/atlas/parish.ts", encoding="utf-8").read()
    for h in ("63", "68", "64", "53", "59", "92", "72", "10", "7"):
        m = re.search(r'houseNo: "' + h + r'",\s*\n\s*bookSignature: "04455",\s*\n\s*year: 1921', ts)
        check(f"I9 parish.ts blok 04455/1921 h{h}", bool(m), "")
    check("I9b P150-sekcija komentar", "P150 razširitev: POROČNA KNJIGA 04455 — polno leto 1921" in ts, "")

    # ---------- I10: README + notes ----------
    rd = open(README, encoding="utf-8").read()
    check("I10a README po P150", "po P150" in rd, "")
    check("I10b README 711/194", "711" in rd and "194" in rd, "")
    nt = open(NOTES, encoding="utf-8").read()
    check("I10c notes P150 obstajajo", "P150" in nt and "1921" in nt, "")

    # ---------- I11: lead-korekcije ----------
    lead = d.get("lead", "")
    check("I11a lead-korekcija Griblje 18→68", "68" in lead, "")
    check("I11b lead-korekcija 4×4→47×47", "47×47" in lead, "")
    check("I11c lead-korekcija 4a→72", "72" in lead, "")
    cc = d.get("crossChecks", [])
    check("I11d crossChecks 14", len(cc) == EXPECTED_CROSSCHECKS, str(len(cc)))
    an = d.get("anomalies", [])
    check("I11e anomalije 17", len(an) == EXPECTED_ANOMALIES, str(len(an)))
    hon = d.get("honesty", [])
    check("I11f honesty 33", len(hon) == 33, str(len(hon)))

    # ---------- I12: veriga — starejše skripte sanirane ----------
    p115 = open("scripts/p115_parish_marriage_1886.py", encoding="utf-8").read()
    check("I12a p115 anchors 186 + 1921×8", "len(anchors) == 187" in p115 and '["1921"] * 9' in p115, "")
    p138 = open("scripts/p138_parish_marriage_1909.py", encoding="utf-8").read()
    check("I12b p138 I6g h46-1920 sanirana (P149-zamuda!)",
          "v.year === 1912 || v.year === 1920))" in p138, "")
    check("I12c p80-hiše text-pini 77 (p137–p146!)",
          all('"p80Houses.size !== 77"' in open(f, encoding="utf-8").read()
              for f in ("scripts/p137_parish_marriage_1908.py", "scripts/p142_parish_marriage_1913.py",
                        "scripts/p146_parish_marriage_1917.py")), "")
    p149 = json.load(open(DOKAZ_P149))
    check("I12d P149-kontinuiteta (37 vpisov 1920)", len(p149["entries"]) == 37, "")

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
        for n_ in (182, 183, 184, 185, 186, 187):
            s2, data = http_get(urls[n_ - 1])
            ok = ok and s2 == 200 and data[:2] == b"\xff\xd8"
        check("L3 citirani skeni s182–s187 live JPEG", ok, "")

    # ---------- izpis ----------
    npass = sum(1 for _, ok, _ in results if ok)
    for name, ok, det in results:
        print(("PASS  " if ok else "FAIL  ") + name + (("  " + det) if det and not ok else ""))
    print(f"\nP150 --check{' --live' if live else ''}: {'PASS' if npass == len(results) else 'FAIL'}"
          f" — {npass}/{len(results)} — 31 vpisov (3. največje leto!) · 2 RAZVEZI (1. v liniji!) ·"
          f" 1. HRVAŠKA · 6 INTRA-HIŠE (rekord!) · župnik-menjava Cerar→Jereb ·"
          f" kumulativ 711/194/187/77 (+h92/h72!)")
    sys.exit(0 if npass == len(results) else 1)


if __name__ == "__main__":
    main()
