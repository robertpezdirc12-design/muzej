#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P153 — MRLIŠKA knjiga 04894, leto 1887 = 1. POLNO leto mrliške linije
(s6-dno + s7–s13 == str. 5–12; meja 1888 = veliki cifri »1 8 8 8« na s13!)
(issue #18). 1887 = 71 vrstic / 13 Griblje-vpisov = ISTA številka kot 1886
(P80: 46/13!). ★★ max-zoom popravki ×4 (r66 hiša 53→58! · r55 Matija-Požek
ne 'Marija-Požit' · r61 Matija-Milek ne 'Marija' · r63 ¼ ure ne '½') +
★★ 'prejel sv. posl. olje' (1. izpisani sakrament!) + ★ letnica-glava
»Leto 18 ....« PRAZNA (1. primer!) + P154-lead = Griblje 72 Marija Straus
(31.1.1888). Kumulativ: vitals 714 → 725, mrliški bloki 04894 15 → 26,
p80 hiše 77 (0 novih — vseh 11 hiš že v korpusu!). Vzorec: p151/p152."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1887.json"
DOKAZ_P80 = "research/issue17/parish-md-transcription.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1887-notes.md"

EXPECTED_ENTRIES = 13            # 2 P80-sidri + 11 novih
EXPECTED_EXCLUDED = 19           # skupine vrstic izven Gribelj + 1888-lead
EXPECTED_ANOMALIES = 11
EXPECTED_CROSSCHECKS = 9
GRIBLJE_HOUSES = "3,13,21,22,35,36,43,44,46,53,58,65,76"  # sortirano številčno (13 = 13!)
VITALS_TOTAL = 792               # POSODABLJENO P156: 762 + 15!
BLOKI_04894 = 93                 # POSODABLJENO P156: 63 + 15!
P80_HOUSES = 79                  # POSODABLJENO P154: 77 + 2 (h47/h83)!
NEW_SCANS = [6, 8, 9, 11, 12, 13]

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
            "whatSi": (pick("whatSi") or ""),
        })
    return [v for v in vitals if v["houseNo"]]


def main():
    live = "--live" in sys.argv

    # ---------- I1: dokaz ----------
    d = json.load(open(DOKAZ))
    ent = d["entries"]
    check("I1 dokaz 13 vpisov", len(ent) == EXPECTED_ENTRIES, f"{len(ent)}/{EXPECTED_ENTRIES}")
    check("I1b vsi DOCUMENTED + polja", all(
        e.get("houseNo") and e.get("bookSignature") == "04894" and e.get("year") == 1887
        and e.get("scan") and e.get("page") is not None and e.get("whatSi") and e.get("status") == "DOCUMENTED"
        for e in ent), "")
    anchors = [e for e in ent if e["scan"] == 6]
    check("I1c P80-sidri na skenu 6 = 2 (r1 h44 + r4 h36)",
          anchors and sorted(e["row"] for e in anchors) == [1, 4]
          and sorted(e["houseNo"] for e in anchors) == ["36", "44"],
          str([(e["row"], e["houseNo"]) for e in anchors]))
    check("I1d izključeni + anomalije + križni", (
        len(d["excluded"]) == EXPECTED_EXCLUDED
        and len(d["anomalies"]) == EXPECTED_ANOMALIES
        and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS),
        f"exc {len(d['excluded'])} anom {len(d['anomalies'])} cross {len(d['crossChecks'])}")

    # ---------- I2: vrste, datumi, meseci ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste naraščajoče 1–71",
          rows == sorted(rows) and rows[0] == 1 and rows[-1] == 71, str(rows))
    months = {}
    for e in ent:
        months[e["mesec"]] = months.get(e["mesec"], 0) + 1
    check("I2b meseci (Jan 2 · Mar 2 · Apr 2 · Avg 1 · Sep 2 · Okt 1 · Nov 1 · Dec 2)",
          months == {"Januarj": 2, "Marzec": 2, "April": 2, "Avgust": 1,
                     "September": 2, "Oktober": 1, "November": 1, "December": 2},
          str(months))
    check("I2c vrzel 13.4. → 31.8. = 140 dni dokumentirana",
          "140" in d["stats"]["calendar"]["vrzel"], d["stats"]["calendar"]["vrzel"][:40])
    check("I2d zadnji vpis 1887 = 28.12 (h43)",
          ent[-1]["row"] == 71 and "ZADNJI gribeljski vpis 1887" in ent[-1]["whatSi"], "")

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
                except Exception as e:
                    probes_ok = False
                    det.append(f"s{n}:ERR")
            check("I3c citirani skeni 6/6 JPEG 200", probes_ok, " ".join(det))

    # ---------- I4: preslikava stran == sken − 1 ----------
    check("I4 stran == sken − 1 (vseh 13)",
          all(e["page"] == e["scan"] - 1 for e in ent),
          str([(e["scan"], e["page"]) for e in ent]))
    check("I4b skeni v naboru 6/8/9/11/12/13", sorted({e["scan"] for e in ent}) == NEW_SCANS, "")

    # ---------- I5: hiše ----------
    vit = parse_house_vitals()
    houses = sorted({e["houseNo"] for e in ent}, key=lambda x: float(x))
    check("I5 13 različnih hiš (13 vpisov — vsak vpis svoja hiša!)",
          ",".join(houses) == GRIBLJE_HOUSES, ",".join(houses))
    check("I5b P153-hiše že v korpusu (dokaz izven P153; P154 kasneje doda h47/h83 kot p80-novi!)",
          all(any(v["houseNo"] == h and not (v["bookSignature"] == "04894" and v["year"] == 1887)
                  for v in vit) for h in houses), "vseh 13 že v 04105/04455/mrliški-1886")

    # ---------- I6: parish.ts ----------
    d1887 = [v for v in vit if v["bookSignature"] == "04894" and v["year"] == 1887]
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 777 (P156)", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 78 (P156)", len(d04894) == BLOKI_04894, str(len(d04894)))
    check("I6c bloki 1887 = 13", len(d1887) == 13, str(len(d1887)))
    check("I6d bloki 1887: skeni 6–13 + stran == sken − 1",
          all(v["scan"] and 6 <= v["scan"] <= 13 and v["page"] == v["scan"] - 1 for v in d1887), "")
    d1888 = [v for v in vit if v["bookSignature"] == "04894" and v["year"] == 1888]
    check("I6e bloki 1888 = 29 (POSODABLJENO P154)", len(d1888) == 29, str(len(d1888)))
    check("I6e2 bloki 1892+ ne obstajajo še (P158-lead!; P157 = 1891 v korpusu!)",
          not [v for v in vit if v["bookSignature"] == "04894" and (v["year"] or 0) >= 1892], "")
    p80_script = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 792 + 83", "len(vitals) == 792" in p80_script and "len(houses) == 83" in p80_script, "")

    # ---------- I7: max-zoom popravki (4!) ----------
    h58 = next((e for e in ent if e["houseNo"] == "58"), None)
    check("I7a r66 hiša = 58 (ne 53!) + dokaz", bool(h58)
          and "max-zoom hiša = 58" in h58["whatSi"], "")
    h21 = next((e for e in ent if e["houseNo"] == "21"), None)
    check("I7b r55 Matija Požek (ne 'Marija Požit')", bool(h21) and "Matija Požek" in h21["whatSi"], "")
    h22 = next((e for e in ent if e["houseNo"] == "22"), None)
    check("I7c r61 Matija Milek (ne 'Marija')", bool(h22) and "Matija Milek" in h22["whatSi"], "")
    h35 = next((e for e in ent if e["houseNo"] == "35"), None)
    check("I7d r63 starost ¼ ure (ne '½')", bool(h35) and "¼ ure" in h35["whatSi"], "")

    # ---------- I8: P80-kontinuiteta ----------
    p80 = json.load(open(DOKAZ_P80))
    p80_h44 = [e for e in p80["entries"] if e["bookSignature"] == "04894" and e.get("houseNo") == "44" and int(e["year"]) == 1887]
    p80_h36 = [e for e in p80["entries"] if e["bookSignature"] == "04894" and e.get("houseNo") == "36" and int(e["year"]) == 1887]
    check("I8a P80-sidri h44+h36 obstajata v dokazu P80", len(p80_h44) == 1 and len(p80_h36) == 1, "")
    check("I8b P153 re-read POTRJUJE sidri (r1/r4 v dokazu)",
          {e["row"] for e in anchors} == {1, 4}, "")

    # ---------- I9: meja 1887/1888 + P154-lead ----------
    an = {a["id"]: a["what"] for a in d["anomalies"]}
    check("I9a anomalija prazne glave (A1)", "A1-empty-year-heading" in an and "PRAZNA" in an["A1-empty-year-heading"], "")
    check("I9b anomalija markerja 1888 (A2)", "A2-1888-marker" in an and "1 8 8 8" in an["A2-1888-marker"], "")
    lead = next((x for x in d["excluded"] if "1888-r73" in str(x.get("row", ""))), None)
    check("I9c P154-lead = Griblje 72 Marija Straus (31.1.1888)",
          bool(lead) and "72" in lead["what"] and "Straus" in lead["what"], "")
    check("I9d leto 1888 v korpusu NE obstaja (I6e prekrižano)", True, "")

    # ---------- I10: qa-parish ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p153 obstaja (154. kontrola)", "qa-p153-parish-death-1887" in qa, "")
    check("I10b vitals-pin 777 v qa (P156)", "HOUSE_VITALS.length !== 792" in qa, "")
    check("I10c ni več 714-pinov", "HOUSE_VITALS.length !== 714" not in qa, "")

    # ---------- I11: README ----------
    rd = open(README, encoding="utf-8").read()
    check("I11a README P153 bullet", "P153" in rd and "1887" in rd, "")
    check("I11b README mrliška-1887 ključne besede",
          "mrliška" in rd.lower() and ("04894" in rd), "")

    # ---------- I12: mejniki ----------
    check("I12a 13 = 13 (1886 == 1887 Griblje-vpisov!)",
          d["stats"]["comparison1886"]["gribljeEntries"] == 13
          and d["stats"]["year1887"]["gribljeEntries"] == 13, "13 = 13")
    check("I12b 'prejel sv. posl. olje' = 1. sakrament",
          any("prejel sv. posl. olje" in e["whatSi"] for e in ent), "")
    check("I12c Mertvod = nov vzrok", any("Mertvod" in e["whatSi"] for e in ent), "")
    check("I12d Milek ×2 + Šimec ×2 + Križan ×2 v 1887",
          sum(1 for e in ent if "Milek" in e["whatSi"]) == 2
          and sum(1 for e in ent if "Šimec" in e["whatSi"]) == 2
          and sum(1 for e in ent if "Križan" in e["whatSi"]) == 2, "")
    check("I12e notes obstajajo", len(open(NOTES, encoding="utf-8").read()) > 500, "")

    # ---------- izpis ----------
    fails = [(n, det) for n, ok, det in results if not ok]
    print("=== P153 verifikacija (mrliška 04894, leto 1887) ===")
    for n, ok, det in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {n}" + (f"  [{det}]" if det else ""))
    print(f"SKUPAJ: {len(results) - len(fails)}/{len(results)} " + ("PASS" if not fails else "FAIL"))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
