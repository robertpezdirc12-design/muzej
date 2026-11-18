#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — verifikator NOTRANJOSTI-01738: 1834-NADALJEVANJE + 1835 + 1836-RESTART (I1–I10 + --live).
INTEGRACIJA: 4 GRIBLJE bloki (h4-m14-1835 + h6-m15-1835 + h9-m6-1836 + h63-m7-1836!);
korpus 2065 → 2069 (+4); 01738 53 → 57; šest-knjižne 34 → 36 (+2: h4/h9!); bothEra-poročna 39 → 41;
h4-DVIG-39 = NOV-ABSOLUTNI-REKORD-ČEZ-VSE-POROČNE-KNJIGE (prej h43-34-P250!);
SIBLING-SWAP-h9×h63 (brat+sestra × brat+sestra — 1. te vrste v 01738!); DUEL-63-vs-68-RAZREŠEN;
KRIŽAN-NIT-42-let (1836→04455-1878!); 1.-VELIKA-GLAVA-'1836'-v-notranjosti;
številčenje = serije restartov (A-rob-19/20 + B-pastoralno-Nov→Nov + C-koledarsko-1836!).
Dokaz: research/issue17/p260-facts.json (+ p260-work/: s14-dc2f13e0 + s15-b130fa71 + s16-eef17788)."""
import json
import os
import re
import sys
import base64
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = os.environ.get("MUZEJ_URL", "http://localhost:3000")
OK = 0
FAIL = 0
LIVE = "--live" in sys.argv


def check(name, ok, msg=""):
    global OK, FAIL
    if ok:
        OK += 1
        print(f"[PASS] {name}" + (f" — {msg}" if msg else ""))
    else:
        FAIL += 1
        print(f"[FAIL] {name}" + (f" — {msg}" if msg else ""))


src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
early = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
stories = open(f"{ROOT}/src/data/atlas/parish-house-stories.ts", encoding="utf-8").read()
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()

# ——— I1: 4 bloki 1835/1836/01738 (file-order!) ———
bloki1835 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1835,\s*scan: 15,', src)
check("I1 bloki-01738/1835-s15 == [4,6] (m14-KRAUG×TOLLER + m15-AHOFZHIG×KLEMERG!)",
      bloki1835 == ["4", "6"], ",".join(bloki1835))
bloki1836 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1836,\s*scan: 16,', src)
check("I1b bloki-01738/1836-s16 == [9,63] (m6-ZAHOFZHIG×KRIŽAN + m7-SIBLING-SWAP!)",
      bloki1836 == ["9", "63"], ",".join(bloki1836))
check("I1c foliacija: Pag. 27/27/29/29 (2·sken−3 ×4 — svinčnik 25/26-27/28-29/30!)",
      len(re.findall(r'year: 1835,\s*scan: 15,\s*page: 27,', src)) == 2
      and len(re.findall(r'year: 1836,\s*scan: 16,\s*page: 29,', src)) == 2, "-")

# ——— I2: korpus 2069 + 01738 == 57 + leta 1828–1836+1873 ———
vseh = re.findall(r'bookSignature: "01738"', src)
skupaj = len(re.findall(r'bookSignature: "', src))
leta1738 = sorted(set(int(y) for h, b, y in re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "(01738)",\s*year: (\d+)', src) if b == "01738"))
check("I2 vitals == 2085 + 01738 == 69 + leta == 1828–1836+1873",
      "HOUSE_VITALS.length !== 2085" in qa and len(vseh) == 73 and skupaj == 2085
      and leta1738 == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1873],
      f"01738={len(vseh)} skupaj={skupaj} leta={leta1738}")

# ——— I3: modul PREDHODNIK_183536_BLOCKS + 260_NITI + 260_KRAJI ———
exports = ["PREDHODNIK_183536_BLOCKS", "PREDHODNIK_260_NITI", "PREDHODNIK_260_KRAJI"]
check("I3 modul: 3 izvoza P260 prisotni", all(f"export const {e}" in early for e in exports), ",".join(exports))
check("I3b števci: noviBloki-4 + vpisi 3/18/13 + vitalsTotal-2069 + byBook01738-57",
      "noviBloki: 4," in early and "vpisi1834n: 3," in early and "vpisi1835: 18," in early
      and "vpisi1836: 13," in early and "vitalsTotal: 2069," in early and "byBook01738: 57," in early, "-")

# ——— I4: dvigi h4-39-REKORD/h9-~49/h63-42/h6-2.-blok + siblingSwap + duel ———
check("I4 dvig-h4-39-NOV-ABSOLUTNI-REKORD (prej-h43-34-P250!)",
      'h4: "1874 → 1835 (39 let' in early and "NOV-ABSOLUTNI-REKORD-DVIGA-ČEZ-VSE-POROČNE-KNJIGE" in early, "-")
check("I4b dvig-h9-~49-kand.-1885 + h63-42-KRIŽAN-NIT + h6-2.-blok",
      '"kand. 1885 → 1836 (~49 let' in early and 'h63: "1878 → 1836 (42 let' in early
      and 'h6: "2.-01738-blok' in early, "-")
check("I4c siblingSwap-ISTI-DAN-ISTI-PRIČI + duelRazresen-63-vs-68 + VELIKA-GLAVA-'1836'",
      "siblingSwap:" in early and "ISTI-DAN-ISTI-PRIČI" in early
      and "63-vs-68-RAZREŠEN-letterform" in early and "1.-VELIKA-GLAVA-'1836'-PRED-vrstico-1" in early, "-")

# ——— I5: house-stories h4/h6/h9/h63 + SIX-42 + TIERS-42/26 + BOOKS-01738-73/46 ———
check("I5 h4 vrsta: 8-blokov/6-knjig/01738-1/firstYear-1835/span-71",
      re.search(r'houseNo: "4", kind: "griblje", blocks: 8, books: 6, perBook: \[\{ sig: "01738", n: 1 \}.*firstYear: 1835, lastYear: 1906, span: 71', stories) is not None, "-")
check("I5b h6 vrsta: 37-blokov/01738-2 + h9 vrsta: 24-blokov/6-knjig/01738-1/firstYear-1836/span-86",
      'houseNo: "6", kind: "griblje", blocks: 37, books: 6, perBook: [{ sig: "01738", n: 2 }' in stories
      and re.search(r'houseNo: "9", kind: "griblje", blocks: 24, books: 6, perBook: \[\{ sig: "01738", n: 1 \}.*firstYear: 1836, lastYear: 1922, span: 86', stories) is not None, "-")
check("I5c h63 vrsta: 31-blokov/01738-3/firstYear-1836/span-85 (P261: +1-m3-1837!)",
      'houseNo: "63", kind: "griblje", blocks: 32, books: 6, perBook: [{ sig: "01738", n: 4 }' in stories
      and re.search(r'houseNo: "63", kind: "griblje", blocks: 32.*firstYear: 1836, lastYear: 1921, span: 85', stories) is not None, "-")
check("I5d SIX-42 (P263: +h29!) + TIERS-42/26 + TOTALS-2085/42/26/42 + p260Dvigi",
      'houseNo: "4", blocks: 8, years: "1835–1906"' in stories and 'houseNo: "9", blocks: 24, years: "1836–1922"' in stories
      and "{ books: 6, houses: 42," in stories and "{ books: 5, houses: 26," in stories
      and "blocks: 2085," in stories and "sixBook: 42," in stories and "fiveBook: 26," in stories
      and "bothEraPorocna: 42," in stories and "p260Dvigi:" in stories, "-")
check("I5e BOOKS-01738: blocks-65/houses-43/years-1828–1837 (P261!)",
      'years: "1828–1838 + 1873", blocks: 73, houses: 46,' in stories, "-")

# ——— I6: QA-p260 blok + importi + žive kontrole ———
check("I6 qa-p260-id + importi-3 + živi-števci-4/57/2069",
      "qa-p260-parish-marriage-notranjost-01738-1835-1836" in qa
      and "PREDHODNIK_183536_BLOCKS," in qa and "PREDHODNIK_260_NITI," in qa and "PREDHODNIK_260_KRAJI," in qa
      and "HOUSE_VITALS.length !== 2085" in qa, "-")
check("I6b QA-bumpi: šest-seznam-vsebuje-'4'-'9' + tierji-36 + bothEra-41 + p91-izjema-01738-1836-h9",
      '"1", "2", "3", "4", "5", "6", "7", "8", "9", "10",' in qa and "tierji ≠ 41/27/8/8/8/8=100 (P261: 39 → P262: +2-h17/h31!)" in qa
      and "obe-eri-pokritje ≠ 69/75/41" in qa and '"01738" && v.year === 1836 && hn === "9"' in qa, "-")

# ——— I7: UI komponenta + render ———
check("I7 UI: Notranjost01738Leto1835_1836 definicija + import + render",
      "function Notranjost01738Leto1835_1836()" in ui and "PREDHODNIK_183536_BLOCKS," in ui
      and "<Notranjost01738Leto1835_1836 />" in ui, "-")

# ——— I8: parish.ts P260-komentar — strukturno odkritje + h4-rekord + sibling-swap ———
check("I8 parish.ts P260-komentar: ŠTEVILČENJE-=-SERIJE-PONOVNIH-ZAČETKOV + h4-39-REKORD + SIBLING-SWAP",
      "ŠTEVILČENJE-=-SERIJE-PONOVNIH-ZAČETKOV" in src and "NOV-ABSOLUTNI-REKORD-DVIGA-ČEZ-VSE-POROČNE-KNJIGE" in src
      and "POLNI-DVOJNI-SIBLING-SWAP" in src and "KRIŽAN-NIT-42-LET" in src, "-")

# ——— I9: dokaz p260-facts.json ———
try:
    d = json.load(open(f"{ROOT}/research/issue17/p260-facts.json", encoding="utf-8"))
    ids = [b["id"] for b in d["gribljeBloki"]]
    check("I9 dokaz: 4-bloki-[m14-s15,m15-s15,m6-s16,m7-s16] + scope-s14–s16",
          ids == ["m14-s15", "m15-s15", "m6-s16", "m7-s16"] and "s14–s16" in d["scope"], ",".join(ids))
    check("I9b dokaz-korpusUcinek: 4-bloki + 2069 + 57 + dvig-h4-39",
          "4" in d["korpusUcinek"]["noviBloki"] and "2065 → 2069" in d["korpusUcinek"]["korpus"]
          and "53 → 57" in d["korpusUcinek"]["korpus"] and "h4" in d["korpusUcinek"]["dvigi"], "-")
    check("I9c dokaz-pushStatus: žeton-mrtev + postopek-nov-ghp_",
          "MRTEV" in d["pushStatus"]["stanje"] and "nov-ghp_" in d["pushStatus"]["postopek"], "-")
except Exception as e:
    check("I9 dokaz p260-facts.json", False, str(e)[:80])

# ——— I10: LIVE ———
if LIVE:
    # I10: matricula HTTP 200 + inventar 147
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01738/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
        urls = []
        for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', html):
            s = m.group(1)[7:-1]
            try:
                dd = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                if dd.startswith("http"):
                    urls.append(dd)
            except Exception:
                pass
        check("I10 LIVE matricula-01738 HTTP-200 + inventar-147-URL", len(urls) == 147, f"URL={len(urls)}")
    except Exception as e:
        check("I10 LIVE matricula-01738", False, str(e)[:80])
    # I10b: /api/qa 254/254
    try:
        qaResp = json.load(urllib.request.urlopen(f"{BASE_URL}/api/qa", timeout=120))
        check("I10b LIVE /api/qa == 254/254 ok:True",
              qaResp.get("ok") is True and qaResp.get("passed") == 254 and qaResp.get("failed") == 0,
              f"{qaResp.get('passed')}/{qaResp.get('passed', 0) + qaResp.get('failed', 0)}")
    except Exception as e:
        check("I10b LIVE /api/qa", False, str(e)[:80])
    # I10c: qa-p260-id prisoten
    check("I10c LIVE qa-p260-id v /api/qa",
          "qa-p260-parish-marriage-notranjost-01738-1835-1836" in qa, "-")

print(f"\n=== P260: {OK} PASS / {FAIL} FAIL ===")
sys.exit(1 if FAIL else 0)
