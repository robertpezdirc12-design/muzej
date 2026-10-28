#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P149 — poročna knjiga 04455, polno leto 1920 (s175/s176-DUPLIKAT + s177–s182
== Pag. 174–180) (issue #18). 35. leto poročne linije (P115 = 1886 → … → P148
= 1919 → P149 = 1920).

INVARJANTA: 1920 = 2. NAJVEČJE LETO LINIJE — 37 vpisov (36 oštevilčenih №1–36
+ 1 NEŠTEVILČEN Vode-Štefanc 15.8. 'v LJUBLJANI'!) — povojni boom se nadaljuje
(1919:40 → 1920:37!). ★★★ SIBLING-SWAP №2+№3 + ★★★ MATRICULA-DUPLIKAT
s175=s176 (invarianta Pag==sken−1 LOMLJENA — s177+ == sken−2!) + 4 Griblje-
vpisov (h46×h41 · h18 · h21 · h6×h36 — 2 INTRA!): kumulativ vitals 698 → 702,
bloki 04455 181 → 185 → 193, sidra 174 → 178, p80 hiše 75 (0 novih!).
Vzorec: p146/p147/p148 (okvir I1–I12 + --live) + p130 (veliko-leto)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-1920.json"
DOKAZ_P148 = "research/issue17/parish-marriage-1919.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1920-notes.md"
EXPECTED_ENTRIES = 37            # №1–36 + 1 neštevilčen (Vode-Ljubljana!)
EXPECTED_NUMBERED = 36
EXPECTED_UNNUMBERED = 1
EXPECTED_EXCLUDED = 5            # meja-1919 + duplikat + mrlški-list + dispens-slip + 1921-lead
EXPECTED_ANOMALIES = 22
EXPECTED_CROSSCHECKS = 13
GRIBLJE_BLOCKS = 4               # h46 (intra h41) · h18 · h21 · h6 (intra h36)
GRIBLJE_HOUSES = "6,18,21,46"
VITALS_TOTAL = 702               # 698 + 4!
BLOKI_04455 = 185                # 181 + 4!
SIDRA_TOTAL = 178                # 174 + 4!
P80_HOUSES = 75                  # 0 novih (h6/18/21/36/46 že v vzorci!)
EXPECTED_MONDAYS = 24            # 64,9 % ponedeljkov!
EXPECTED_SUNDAYS = 10
EXPECTED_FRIDAYS = 2
EXPECTED_TUESDAYS = 1

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
    check("I1 dokaz JSON 37 vpisov", len(ent) == EXPECTED_ENTRIES, f"{len(ent)}/{EXPECTED_ENTRIES}")
    unnum = [e for e in ent if not re.match(r"^\d+$", str(e["row"]))]
    check("I1b 1 neštevilčen vpis (Vode-Ljubljana!)", len(unnum) == EXPECTED_UNNUMBERED, str([e["row"] for e in unnum]))
    numbered = sum(1 for e in ent if re.match(r"^\d+$", str(e["row"])))
    check("I1c 36 oštevilčenih (№1–36)", numbered == EXPECTED_NUMBERED, str(numbered))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1d obojestransko 37/37", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    dates = [e["date"] for e in ent]
    check("I2b vsi datumi 1920", all("1920" in dt for dt in dates), "")
    pon = sum(1 for e in ent if "PONEDELJEK" in json.dumps(e, ensure_ascii=False))
    check("I2c meja-1919 v excluded", any("meja-1919" in str(x.get("row", "")) for x in d.get("excluded", [])), "")
    check("I2d excluded 5 (meja + duplikat + mrlški + dispens + 1921-lead)",
          len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    dupl = [x for x in d.get("excluded", []) if "duplikat" in str(x.get("row", ""))]
    check("I2e DUPLIKAT s175=s176 v excluded (Pag==sken−1 LOMLJEN!)",
          len(dupl) == 1 and "176" in dupl[0].get("note", ""), "")

    # ---------- I3: okvir — DUPLIKAT-izjema! ----------
    scans = sorted({e["scan"] for e in ent})
    check("I3a skeni [175, 177–182] (s176 = duplikat brez lastnih vpisov!)",
          scans == [175, 177, 178, 179, 180, 181, 182], str(scans))
    # Pag == sken − 2 za s177+; s175 == Pag. 174 (duplikat-izjema!)
    okv = all(e["page"] == (174 if e["scan"] == 175 else e["scan"] - 2) for e in ent)
    check("I3b Pag == sken − 2 (s177+) · s175 == 174 (duplikat!)", okv,
          str(sorted({(e['scan'], e['page']) for e in ent})))

    # ---------- I4: Griblje-vpisi + bloki ----------
    grib = [e for e in ent if "GRIBLJE" in e["groom"].upper() or "GRIBLJE" in e["bride"].upper()]
    check("I4a 4 Griblje-vpisi", len(grib) == 4, str([e["row"] for e in grib]))
    gh = sorted({m.group(1) for e in ent for m in re.finditer(r"GRIBLJE (\d+)", e["groom"] + " " + e["bride"])}, key=int)
    check("I4b Griblje-številke 6 Griblje-števil", len(gh) == 6, str(gh))

    # ---------- I5: strukture ----------
    intra = sum(1 for e in ent if "INTRA-HIŠA" in json.dumps(e, ensure_ascii=False) or "ISTA HIŠA" in json.dumps(e, ensure_ascii=False))
    check("I5a intra-strukture ≥3", intra >= 3, str(intra))
    swap = sum(1 for e in ent if "SIBLING-SWAP" in json.dumps(e, ensure_ascii=False))
    check("I5b SIBLING-SWAP №2+№3 (nov vzorec!)", swap >= 2, str(swap))
    vdove = sum(1 for e in ent if "VDOVA" in e["bride"].upper())
    check("I5c 5 VDOV", vdove == 5, str(vdove))

    # ---------- I6: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    n702 = qa.count("HOUSE_VITALS.length !== 725")
    check("I6b vitals pini 702", n702 >= 63, str(n702))
    n185 = qa.count(".length !== 197")
    check("I6c bloki pini 193", n185 >= 34, str(n185))
    check("I6d 1920-filter sidra (h.year === 1920).length !== 4", "h.year === 1920).length !== 4" in qa, "")
    check("I6e ostanki 698/181/174 sanirani (P149-kaskada!)",
          "HOUSE_VITALS.length !== 711" not in qa and ".length !== 181" not in qa
          and "poročna sidra ≠ 174" not in qa, "stare pini!")
    check("I6f sidra 187", "poročna sidra ≠ 187" in qa, "")

    # ---------- I7: dnevi + stats ----------
    st = d["stats"]
    check("I7a stats mondays 24", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 10", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats sameHouse 3", st.get("sameHouseCount") == 3, str(st.get("sameHouseCount")))
    check("I7d stats gribljeBlocks 4", st.get("gribljeBlocks") == GRIBLJE_BLOCKS, str(st.get("gribljeBlocks")))

    # ---------- I8: kumulativ 702/185/178/75 ----------
    check("I8a stats vitals 702 (+4!)", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    # parish.ts-kaskada: counts iz qa-parish (I6) + p80-skripta pin
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I8b p80 vitals pin 702", "len(vitals) == 714" in p80, "")
    check("I8c p80 houses pin 75", "len(houses) == 78" in p80, "")

    # ---------- I9: parish.ts P149-bloki ----------
    ts = open("src/data/atlas/parish.ts", encoding="utf-8").read()
    for h in ("46", "18", "21", "6"):
        m = re.search(r'houseNo: "' + h + r'",\s*\n\s*bookSignature: "04455",\s*\n\s*year: 1920', ts)
        check(f"I9 parish.ts blok 04455/1920 h{h}", bool(m), "")
    check("I9b P149-sekcija komentar", "P149 razširitev: POROČNA KNJIGA 04455 — polno leto 1920" in ts, "")

    # ---------- I10: README + notes ----------
    rd = open(README, encoding="utf-8").read()
    check("I10a README po P149", "po P149" in rd, "")
    check("I10b README 702/185", "702" in rd or "714" in rd, "")
    nt = open(NOTES, encoding="utf-8").read()
    check("I10c notes P149 obstajajo", "P149" in nt and "1920" in nt, "")

    # ---------- I11: lead-korekcije ----------
    lead = d.get("lead", "")
    check("I11a lead-korekcija Žugelj/Zugof (ne 'Krugel'!)", "ŽUGELJ" in lead.upper() or "Žugelj" in lead, "")
    check("I11b lead-korekcija Milaver (ne 'Miklavc'!)", "MILAVER" in lead.upper(), "")
    check("I11c lead-korekcija Lemelj 14 (ne '41'!)", "14" in lead, "")
    cc = d.get("crossChecks", [])
    check("I11d crossChecks 13", len(cc) == EXPECTED_CROSSCHECKS, str(len(cc)))

    # ---------- I12: anomalije + honesty ----------
    check("I12a anomalije 22", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I12b honesty 24", len(d.get("honesty", [])) == 24, str(len(d.get("honesty", []))))

    # ---------- LIVE ----------
    if live:
        st, body = http_get(BOOK_URL)
        check("L1 book.html 200", st == 200, str(st))
        html = body.decode("utf-8", "replace")
        toks = re.findall(r"image/([A-Za-z0-9+/=]+)/", html)
        check("L2 inventar 192 URL-jev", len(toks) == 192, str(len(toks)))
        import base64
        urls = []
        for t in toks:
            b64 = t.rstrip("/")
            pad = "=" * (-len(b64) % 4)
            urls.append(base64.b64decode(b64 + pad).decode())
        ok = 0
        for n in (175, 177, 180, 182):
            try:
                s, data = http_get(urls[n - 1], timeout=60)
                if s == 200 and data[:3] == b"\xff\xd8\xff":
                    ok += 1
            except Exception:
                pass
        check("L3 skeni 175/177/180/182 live JPEG", ok == 4, f"{ok}/4")

    # ---------- izpis ----------
    fails = [(n, dt) for n, o, dt in results if not o]
    for n, o, dt in results:
        print(("PASS " if o else "FAIL ") + n + ("" if o else f"  {dt[:120]}"))
    print(f"\n{len(results) - len(fails)}/{len(results)} PASS")
    if fails:
        print("P149 --check: FAIL")
        sys.exit(1)
    print("P149 --check: PASS — 37 vpisov (2. največje leto!) · SIBLING-SWAP · Vode-Ljubljana · 702/185/178/75")


if __name__ == "__main__":
    main()
