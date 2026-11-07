#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P191 — PT-luknja-18 FINALNI verifikator (po zaključku mrliške linije 39/39).

Vse tri knjige so popolnoma prebrane (krstna 04105: 1887–1919 · poročna
04455: 1886–1922 · mrliška 04894: 1886–1924), zato je korpus FINALEN.
Ta verifikator potrjuje dokaz research/issue17/pt-luknja-18-final.json
(generira ga scripts/tmp/p191-pt-luknja.ts iz src/data/atlas/parish.ts):

  I1  datoteka obstaja, phase == P191, definicija gap = 18 hiš (42–60 brez h41/h50)
  I2  korpus FINALNO: vitals 1511 · 04105=502 · 04455=197 · 04106=312 · 04894=520
  I3  gap-status: 18/18 hiš Z dokazi — pravih lukenj (0 blokov) = 0
  I4  konsistentnost na hišo: blocksTotal == vsota po knjigah == len(years)
      in firstYear <= lastYear
  I5  dokaz-via: natanko 13/18 v VSEH TREH knjigah; h51 = edina samo-mrliška;
      nič ne-zaprtih prek poročne-samo
  I6  ekstremi: min blokov = 4 (h51!) · max blokov = 30 (h46)

--live: preveri produkcijo https://griblje-museum.vercel.app/api/qa
        (ok:True in passed >= 191).

Zagon:  python3 scripts/p191_pt_luknja_final.py --check [--live]
"""
import argparse
import json
import os
import sys
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOKAZ = os.path.join(REPO, "research", "issue17", "pt-luknja-18-final.json")
LIVE_URL = "https://griblje-museum.vercel.app/api/qa"

EXPECTED_GAP = ["42", "43", "44", "45", "46", "47", "48", "49",
                "51", "52", "53", "54", "55", "56", "57", "58", "59", "60"]
EXPECTED_CORPUS = {"04105": 502, "04455": 197, "04106": 433, "04894": 520, "04104": 65}  # POSODABLJENO P223: + krstna-04104 = 65 (25×1885-P221 + 21×1884-P222 + 19×1883-P223!)
VITALS_TOTAL = 1717


def load():
    if not os.path.exists(DOKAZ):
        print(f"I1 FAIL: manjka {DOKAZ} (zaženi bun scripts/tmp/p191-pt-luknja.ts)")
        sys.exit(1)
    return json.load(open(DOKAZ, encoding="utf-8"))


def check(report):
    issues = []

    def ok(label, cond, detail=""):
        print(f"  {'✓' if cond else '✗'} {label}{(' — ' + detail) if detail else ''}")
        if not cond:
            issues.append(label)

    gap_houses = [g["houseNo"] for g in report["gapHouses"]]

    # I1
    ok("I1 faza + definicija 18 hiš (42–60 brez h41/h50)",
       report.get("phase") == "P191" and sorted(gap_houses) == sorted(EXPECTED_GAP),
       f"{len(gap_houses)} hiš")

    # I2
    corpus = report["corpus"]
    ok("I2 korpus FINALNO (vitals 1717 · 04105=502 · 04455=197 · 04106=433 · 04894=520 · 04104=65)",
       corpus["vitalsTotal"] == VITALS_TOTAL
       and {k: v for k, v in corpus["byBook"].items()} == EXPECTED_CORPUS,
       str(corpus["byBook"]))

    # I3
    gs = report["gapStatus"]
    ok("I3 PT-luknja ZAKLJUČENA — 18/18 z dokazi, pravih lukenj 0",
       gs["total"] == 18 and gs["withDokaz"] == 18 and gs["trueHoles"] == [])

    # I4
    bad = []
    for g in report["gapHouses"]:
        s = g["byBook"]["04105"] + g["byBook"]["04455"] + g["byBook"].get("04106", 0) + g["byBook"]["04894"]
        if g["blocksTotal"] != s or g["blocksTotal"] != len(g["years"]):
            bad.append(f"h{g['houseNo']}-vsota")
        if g["firstYear"] is None or g["firstYear"] > g["lastYear"]:
            bad.append(f"h{g['houseNo']}-leta")
    ok("I4 konsistentnost na hišo (vsota po knjigah == bloki == leta)",
       not bad, ", ".join(bad) or "18/18 OK")

    # I5
    all_three = [g["houseNo"] for g in report["gapHouses"]
                 if g["byBook"]["04105"] > 0 and g["byBook"]["04455"] > 0 and g["byBook"]["04894"] > 0]
    ok("I5 dokaz-via: 13/18 v vseh treh knjigah · h51 edina samo-mrliška · poročna-samo = nič",
       len(all_three) == 13
       and gs["dokazOnlyMrliška"] == ["51"]
       and gs["dokazOnlyPoročna"] == [],
       f"vse-tri: {len(all_three)}")

    # I6
    totals = {g["houseNo"]: g["blocksTotal"] for g in report["gapHouses"]}
    mn = min(totals, key=totals.get)
    mx = max(totals, key=totals.get)
    ok("I6 ekstremi: min h51=4 · max h46=30",
       totals[mn] == 4 and mn == "51" and totals[mx] == 30 and mx == "46",
       f"min h{mn}={totals[mn]} · max h{mx}={totals[mx]}")

    print(f"\nP191 --check: {'PASS' if not issues else 'FAIL (' + str(len(issues)) + ')'}")
    return not issues


def live():
    req = urllib.request.Request(LIVE_URL, headers={"User-Agent": "p191-verifier"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    good = bool(d.get("ok")) and int(d.get("passed", 0)) >= 191
    print(f"  {'✓' if good else '✗'} --live produkcija: ok={d.get('ok')} · passed={d.get('passed')}/{d.get('tests') and len(d['tests'])}")
    return good


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--live", action="store_true")
    args = ap.parse_args()
    if not (args.check or args.live):
        args.check = True
    good = True
    if args.check:
        good = check(load()) and good
    if args.live:
        good = live() and good
    sys.exit(0 if good else 1)


if __name__ == "__main__":
    main()
