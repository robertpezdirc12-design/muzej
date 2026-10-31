#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P154 — MRLIŠKA knjiga 04894, leto 1888 = 3. polno leto mrliške linije
= REKORDNO leto (s13-dno + s14–s21 == str. 12–20; 102 vrstic / 29 Griblje-vpisov
= ×2.2!). (issue #18). ★★ 2 porodni smrti (r6 h72 'Na porodu' 3 dni po hči +
r23 h83 'Vsled těžkega poroda') + ★★ Željko/Želičo 4 otroci (h1 ×2 + h60 ×2 —
sestri 'Strgjatinka' v 6 dneh!) + ★★ h61 Požek ×3 + ★★ max-zoom popravki ×4
(r20 Janez-Perdinec-h53 ×2-napaka · r84 Matija-Hlusič spol+priimek · r7 PožeK ·
r15 Brinec) + ★ h83/h47 NOVI p80-hiši + ★ 'Starost' kot vzrok (r102, 80 let!) +
★ podpisi-kolaps (8/29!) + celostanska-1889-napaka RAZREŠENA (max-zoom > VLM!).
Kumulativ: vitals 725 → 754, mrliški bloki 04894 26 → 55, p80 hiše 77 → 79.
Vzorec: p153."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1888.json"
DOKAZ_P153 = "research/issue17/parish-death-1887.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1888-notes.md"

EXPECTED_ENTRIES = 29            # 1 P153-lead + 28 novih
EXPECTED_EXCLUDED = 13           # skupine vrstic izven Gribelj + 1889-restart
EXPECTED_ANOMALIES = 12
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "1,1,3,7,8,8,13,21,21,24,25,26,26,35,35,36,41,47,53,60,60,61,61,61,65,69,72,72,83"
VITALS_TOTAL = 938               # POSODABLJENO P162: 837 + 16 (mrliška 1896)!
BLOKI_04894 = 239                # POSODABLJENO P167: + 10 (mrliška 1901)!
P80_HOUSES = 79                  # 77 + 2 (h47/h83)!
NEW_SCANS = [13, 14, 15, 16, 18, 19, 20, 21]

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
        vitals.append({
            "houseNo": pick("houseNo"),
            "bookSignature": pick("bookSignature"),
            "year": pickn("year"),
            "scan": pickn("scan"),
            "page": pickn("page"),
            "whatSi": pick("whatSi") or "",
        })
    return vitals


def main():
    live = "--live" in sys.argv
    d = json.load(open(DOKAZ, encoding="utf-8"))
    ent = d["entries"]

    # ---------- I1: dokaz-structura ----------
    check("I1 dokaz obstaja + status", d.get("status") == "SAMPLE-TRANSCRIPTION-D1888", d.get("status", ""))
    check("I1b št. vpisov = 29", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c izključene skupine = 13",
          len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))
    check("I1d anomalije ×12 + križne ×10 + iskrenost ×10", (
        len(d["anomalies"]) == EXPECTED_ANOMALIES
        and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS
        and len(d["honesty"]) == 10),
        f"anom {len(d['anomalies'])} cross {len(d['crossChecks'])} hon {len(d['honesty'])}")

    # ---------- I2: vrste, hiše, meseci ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste naraščajoče (5,6,7,10,13,15,20,21,22,23,24,37,43,44,60,63,66,68,72,74,81,82,84,87,89,97,98,99,102)",
          rows == sorted(rows) and rows[0] == 5 and rows[-1] == 102, str(rows))
    houses = sorted((e["houseNo"] for e in ent), key=int)
    check("I2b hišna multizbroj = 20 različnih (29 vpisov)",
          ",".join(houses) == GRIBLJE_HOUSES, f"{len(set(houses))} različnih")
    months = {}
    for e in ent:
        months[e["mesec"]] = months.get(e["mesec"], 0) + 1
    check("I2c meseci (Jan 1 · Feb 4 · Mar 1 · Apr 5 · Maj 1 · Jun 2 · Jul 1 · Avg 5 · Sep 3 · Okt 2 · Nov 3 · Dec 1)",
          months == {"Januarj": 1, "Februar": 4, "Marcej": 1, "April": 5, "Maj": 1, "Junij": 2,
                     "Julij": 1, "Avgust": 5, "September": 3, "Oktober": 2, "November": 3, "December": 1},
          str(months))

    # ---------- I3: live viri ----------
    if live:
        st, body = http_get(BOOK_URL)
        ok200 = st == 200
        check("I3a knjiga 04894 HTTP 200", ok200, str(st))
        if ok200:
            html = body.decode("utf-8", "replace")
            inv = re.findall(r'"(/image/[A-Za-z0-9+/=%]+/)"', html)
            urls = set()
            for s in inv:
                import base64
                try:
                    u = base64.b64decode(s[7:-1] + "=" * (-len(s[7:-1]) % 4)).decode()
                    if u.startswith("http"):
                        urls.add(u)
                except Exception:
                    pass
            check("I3b inventar 256", len(urls) == 256, str(len(urls)))
            probes_ok = True
            det = []
            for n in NEW_SCANS:
                try:
                    st2, b2 = http_get(sorted(urls)[n - 1], timeout=60)
                    ok = st2 == 200 and b2[:2] == b"\xff\xd8"
                    probes_ok = probes_ok and ok
                    det.append(f"s{n}:{st2}")
                except Exception:
                    probes_ok = False
                    det.append(f"s{n}:ERR")
            check("I3c citirani skeni 8/8 JPEG 200", probes_ok, " ".join(det))

    # ---------- I4: preslikava stran == sken − 1 ----------
    check("I4 stran == sken − 1 (vseh 29)",
          all(e["page"] == e["scan"] - 1 for e in ent),
          str(sorted({(e["scan"], e["page"]) for e in ent})[:5]) + "...")
    check("I4b skeni v naboru 13+14/15/16/18/19/20/21",
          sorted({e["scan"] for e in ent}) == NEW_SCANS, "")

    # ---------- I5: hiše ----------
    vit = parse_house_vitals()
    uniq = sorted({e["houseNo"] for e in ent}, key=lambda x: float(x))
    check("I5 20 različnih hiš", len(uniq) == 20, ",".join(uniq))
    check("I5b h83 NOVA p80-hiša (dokaz izven P154: ni 04894-1888 prej)",
          any(v["houseNo"] == "83" and v["bookSignature"] == "04894" and v["year"] == 1888 for v in vit),
          "h83 = r23 Radovič")

    # ---------- I6: parish.ts ----------
    d1888 = [v for v in vit if v["bookSignature"] == "04894" and v["year"] == 1888]
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 777 (P156)", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 239 (POSODABLJENO P167)", len(d04894) == BLOKI_04894, str(len(d04894)))
    check("I6c bloki 1888 = 29", len(d1888) == 29, str(len(d1888)))
    check("I6d bloki 1888: skeni 13–21 + stran == sken − 1",
          all(v["scan"] and 13 <= v["scan"] <= 21 and v["page"] == v["scan"] - 1 for v in d1888), "")
    check("I6d2 bloki 1900+ ne obstajajo (P166-lead!; P165 = 1899 sedaj v korpusu!)",
          not [v for v in vit if v["bookSignature"] == "04894" and (v["year"] or 0) >= 1904], "")
    p80_script = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 938 + 90 + gap-18 (POSODABLJENO P164)", "len(vitals) == 938" in p80_script and "len(houses) == 91" in p80_script and "len(gap) == 18" in p80_script, "")

    # ---------- I7: max-zoom popravki (4!) ----------
    r20 = next((e for e in ent if e["row"] == 20), None)
    check("I7a r20 = Janez Perdinec h53 (×2-napaka!) + dokaz", bool(r20)
          and "×2 NAPAČNA" in r20["whatSi"] and "Perdinec" in r20["whatSi"], "")
    r84 = next((e for e in ent if e["row"] == 84), None)
    check("I7b r84 = Matija Hlusič (spol+priimek!)", bool(r84)
          and "Matija Hlusič" in r84["whatSi"] and "Marija Mušič" in r84["whatSi"], "")
    r7 = next((e for e in ent if e["row"] == 7), None)
    check("I7c r7 = PožeK (ne 'Poreht!')", bool(r7) and "PožeK" in r7["whatSi"]
          and "Poreht" in r7["whatSi"], "")
    r15 = next((e for e in ent if e["row"] == 15), None)
    check("I7d r15 = Brinec (ne 'Brune!')", bool(r15) and "Brinec" in r15["whatSi"]
          and "NAPAČNA" in r15["whatSi"], "")

    # ---------- I8: P153-kontinuiteta ----------
    p153 = json.load(open(DOKAZ_P153))
    lead = next((e for e in ent if e["row"] == 5 and e["houseNo"] == "72"), None)
    check("I8a P153-lead r5 h72 potrjen (1 DAN, 31.1.)", bool(lead)
          and lead["whatSi"].startswith("umrla Marija Straus"), "")
    p153_last = [e for e in p153["entries"] if e["row"] == 71]
    check("I8b P153 zadnji 1887 (r71 h43) se nadaljuje z 1888-r1 (s13-dno)",
          bool(p153_last) and lead["scan"] == 13, "s13-dno == P153-s13!")

    # ---------- I9: družinske tragedije ----------
    h61 = [e for e in ent if e["houseNo"] == "61"]
    check("I9a h61 = 3 smrti (Požek-tragedija)", len(h61) == 3
          and {e["row"] for e in h61} == {7, 10, 24}, str([e["row"] for e in h61]))
    zel = [e for e in ent if "Želičo" in e["whatSi"] or "Željko" in e["whatSi"]]
    check("I9b Željko/Želičo = 4 otroci na 2 hišah (h1 ×2 + h60 ×2)",
          len(zel) == 4 and {e["houseNo"] for e in zel} == {"1", "60"},
          str([(e["row"], e["houseNo"]) for e in zel]))
    strg = [e for e in ent if "Strgjatinka [~" in e["whatSi"]]
    check("I9c Strgjatinka ×3 kot vzrok (r43 + r63 + r66 — h60-sestri!)",
          len(strg) == 3 and {e["row"] for e in strg} == {43, 63, 66}, str([e["row"] for e in strg]))
    porod = [e for e in ent if "PORODU" in e["whatSi"] or "PORODA" in e["whatSi"]]
    check("I9d 2 porodni smrti (r6 + r23)", len(porod) == 2
          and {e["row"] for e in porod} == {6, 23}, str([e["row"] for e in porod]))

    # ---------- I10: vzroki + podpisi ----------
    r102 = next((e for e in ent if e["row"] == 102), None)
    check("I10a r102 'STAROST' vzrok (1. primer!) + ZADNJI 1888",
          bool(r102) and "STAROST" in r102["whatSi"] and "ZADNJI gribeljski vpis 1888" in r102["whatSi"], "")
    r89 = next((e for e in ent if e["row"] == 89), None)
    check("I10b r89 '1 URO' + neberljiv vzrok", bool(r89)
          and "1 URO" in r89["whatSi"] and "[?" in r89["whatSi"], "")
    signed = [e for e in ent if any(x in e["whatSi"] for x in ("Glibe coop.", "Romey", "Glibel", "Dovgan"))]
    check("I10c podpisi-kolaps: 9/29 podpisanih", len(signed) == 9,
          str([e["row"] for e in signed]))
    previd = [e for e in ent if "(1)" in e["whatSi"] or "previden (1)" in e["whatSi"] or "previdna (1)" in e["whatSi"]]
    check("I10d previden-oznake ×6", len(previd) == 6, str([e["row"] for e in previd]))

    # ---------- I11: marker 1889 + celostanska napaka ----------
    check("I11 marker-1889 forenzika v frame (9 z repom)",
          "1 8 8 9" in d["frame"]["boundaries"]["1888→1889"], "")
    check("I11b celostanska-1889-napaka = anomalija A1",
          any(a["id"] == "A1-celostanska-1889-napaka" for a in d["anomalies"]), "")
    check("I11c glave s14–s21 izpisane (frame.glave)",
          "18ſſ" in d["frame"].get("glave", ""), "")

    # ---------- I12: qa + README ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I12 qa-p154 obstaja", "qa-p154-parish-death-1888" in qa, "")
    check("I12b qa-p153 1888-prisotnost (posodobljeno)",
          "1888-mrliških blokov ≠ 29" in qa, "")
    readme = open(README, encoding="utf-8").read()
    check("I12c README P154", "P154" in readme and "1888" in readme, "")

    # ---------- izpis ----------
    fails = [r for r in results if not r[1]]
    for name, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\nSKUPAJ: {len(results) - len(fails)}/{len(results)} PASS")
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
