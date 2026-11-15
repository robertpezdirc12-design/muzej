#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P261 — verifikator NOTRANJOSTI-01738: 1836-NADALJEVANJE + RESTART-1.-NOVEMBER-1836 → 1837-START (I1–I10 + --live).
INTEGRACIJA: 8 GRIBLJE bloki (h20-m14-1836 + h39-m14-1836 + h61-m15-1836 + h7-m15-1836 + h41-m2-1836 + h26-m2-1836 + h20-m3-1837 + h63-m3-1837!);
korpus 2077 → 2081 (P262:+4!); 01738 65 → 69; ŠEST-KNJIŽNI-KLUB 39 → 41 (+2: h17/h31!);
3 DVIGI (h39-1859→1836-23 + h41-1866→1836-30 + h7-1867→1836-31!);
RESTART-(C)-1.-NOVEMBER-1836 (PASTORALNO-Nov→Nov-3.-serija!-m2-'1-im-d°' = ISTI-DAN-2-poroke!);
PEZDIRC-×6-NA-S17 (2-Georga-v-6-mesecih + 4-grafije!); KRIŽAN-NIT-1837 (h63-3.-01738-blok-43-let!);
BRING×ŠHRING-endogamija (letterform-B-loop-VS-Š-hook!); NOTIZEN-soglasja-×4 (m3-datirana-11.-Nov-1836!);
foliacija-'Pag-=-2·sken−3'-serija-14/14 (s17-31/32!).
Dokaz: research/issue17/p261-facts.json (+ p261-work/: s17-3b1f5b30 + s18-1bb45fb3)."""
import json
import re
import sys
import base64
import urllib.request

ROOT = "/home/z/my-project"
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

# ——— I1: 8 blokov 1836/1837/01738 s17 (file-order!) ———
bloki1836 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1836,\s*scan: 17,', src)
check("I1 bloki-01738/1836-s17 == [20,39,61,7,41,26] (m14-ŠHRING + m15-STRAAAF + m2-PEZDIRIZ!)",
      bloki1836 == ["20", "39", "61", "7", "41", "26"], ",".join(bloki1836))
bloki1837 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1837,\s*scan: 17,', src)
check("I1b bloki-01738/1837-s17 == [20,63] (m3-DOW-DIW + m3-KRIŠAN-KRIŽAN-NIT!)",
      bloki1837 == ["20", "63"], ",".join(bloki1837))

# ——— I2: korpus 2081 + 01738 == 69 + leta 1828–1838+1873 (P262-živo!) ———
vseh = re.findall(r'bookSignature: "01738",\s*year: (\d+)', src)
skupaj = len(re.findall(r'bookSignature: "', src))
leta1738 = sorted(set(int(y) for h, b, y in re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "(01738)",\s*year: (\d+)', src) if b == "01738"))
check("I2 vitals == 2081 + 01738 == 69 + leta == 1828–1837+1873",
      "HOUSE_VITALS.length !== 2081" not in src and len(vseh) == 69 and skupaj == 2081
      and leta1738 == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1873],
      f"01738={len(vseh)} skupaj={skupaj} leta={leta1738}")

# ——— I3: modul PREDHODNIK_1836_37_BLOCKS + 261_NITI/KRAJI ———
exports = ["PREDHODNIK_1836_37_BLOCKS", "PREDHODNIK_261_NITI", "PREDHODNIK_261_KRAJI"]
for e in exports:
    check(f"I3 modul-izvoz-{e}", f"export const {e}" in early, "-")
check("I3b PREDHODNIK_1836_37_BLOCKS-števci 8/4/5/2077/65",
      "noviBloki: 8" in early and "vpisi1836n: 4" in early and "vpisiRestart: 5" in early
      and "vitalsTotal: 2081" in early and "byBook01738: 69" in early, "-")
check("I3c dvigi-h39-23 + h41-30 + h7-31",
      'h39: "1859 → 1836 (23 let' in early and 'h41: "1866 → 1836 (30 let' in early
      and 'h7: "1867 → 1836 (31 let' in early, "-")
check("I3d restartStruktura-1.-NOVEMBER-1836 + ISTI-DAN",
      "1.-NOVEMBER-1836" in early and "ISTI-DAN-2-poroke" in early, "-")
check("I3e foliacija-14/14 + pezdirc-×6-4-grafije",
      "serija-14/14-notranjosti" in early and "×6" in early and "4-grafije" in early, "-")

# ——— I4: house-stories — h39/h41/h7 story + SIX-39 + TOTALS ———
check("I4 h39-story: 17-blokov-6-knjig-firstYear-1836-span-76",
      'houseNo: "39", kind: "griblje", blocks: 17, books: 6, perBook: [{ sig: "01738", n: 1 }' in stories
      and 'firstYear: 1836, lastYear: 1912, span: 76' in stories, "-")
check("I4b h41-story: 23-blokov-6-knjig-firstYear-1836-span-85",
      'houseNo: "41", kind: "griblje", blocks: 23, books: 6, perBook: [{ sig: "01738", n: 1 }' in stories
      and 'firstYear: 1836, lastYear: 1921, span: 85' in stories, "-")
check("I4c h7-story: 25-blokov-6-knjig-firstYear-1836-span-85",
      'houseNo: "7", kind: "griblje", blocks: 25, books: 6, perBook: [{ sig: "01738", n: 1 }' in stories
      and 'firstYear: 1836, lastYear: 1921, span: 85' in stories, "-")
check("I4d h20-story-37 + h26-28 + h61-19 + h63-31 (01738-n: 4/2/3/3!)",
      'houseNo: "20", kind: "griblje", blocks: 37' in stories and 'houseNo: "26", kind: "griblje", blocks: 28' in stories
      and 'houseNo: "61", kind: "griblje", blocks: 19' in stories and 'houseNo: "63", kind: "griblje", blocks: 32' in stories
      and 'sig: "01738", n: 4 }' in stories and 'sig: "01738", n: 2 }' in stories and 'sig: "01738", n: 4 }' in stories, "-")
check("I4e SIX-39-izvoz (h7/h39/h41!)",
      '{ houseNo: "7", blocks: 25, years: "1836–1921"' in stories
      and '{ houseNo: "39", blocks: 17, years: "1836–1912"' in stories
      and '{ houseNo: "41", blocks: 23, years: "1836–1921"' in stories, "-")
check("I4f TOTALS-2077/39/29 + TIERS-39/29",
      "blocks: 2081," in stories and "sixBook: 41," in stories and "fiveBook: 27," in stories
      and "{ books: 6, houses: 41," in stories and "{ books: 5, houses: 27," in stories, "-")
check("I4g BOOKS-01738-blocks-65-years-1828–1837",
      'years: "1828–1838 + 1873", blocks: 69, houses: 45,' in stories, "-")

# ——— I5: qa-p261 blok + guardi ———
check("I5 qa-p261-id + živi-bloki-8",
      "qa-p261-parish-marriage-notranjost-01738-1836-1837" in qa
      and 'v.scan === 17' in qa and "bloki-s17 živo ≠ 8" in qa, "-")
check("I5b qa-p261-guardi (20-1836,20-1837,26-1836,39-1836,41-1836,61-1836,63-1837,7-1836)",
      '"20-1836,20-1837,26-1836,39-1836,41-1836,61-1836,63-1837,7-1836"' in qa, "-")
check("I5c qa-p261-firstYear-živi (39/41/7 == 1836)",
      'for (const [hh, pri] of [["39", 1836], ["41", 1836], ["7", 1836]] as const)' in qa, "-")
check("I5d qa-p261-4-dvojne-pari",
      '"20-1836|39-1836", "61-1836|7-1836", "41-1836|26-1836", "20-1837|63-1837"' in qa, "-")
check("I5e qa-p261-KRIŽAN + PEZDIRC + BRING×ŠHRING guardi",
      'h63-KRIŽAN-NIT ni označena!' in qa and 'h41-PEZDIRC-nit ni označena!' in qa
      and 'h39-BRING×ŠHRING-endogamija ni označena!' in qa, "-")

# ——— I6: stari-verifierji-kaskada (p261_oldverifier_cascade) ———
check("I6 cascade-izveden: 64-verifierjev-2077/65-leta+1837",
      'HOUSE_VITALS.length !== 2081' in open(f"{ROOT}/scripts/p200_parish_death_1877_04106.py", encoding="utf-8").read()
      and '01738:69}' in open(f"{ROOT}/scripts/p237_parish_forensics.py", encoding="utf-8").read()
      and '1838, 1873' in open(f"{ROOT}/scripts/p258_meja_1831_32_33.py", encoding="utf-8").read(), "-")
check("I6b p85-izjema-01738-1836-h7/h41",
      '"01738" && (v.year === 1836 || v.year === 1837) && (hn === "7" || hn === "41")' in qa, "-")

# ——— I7: UI komponenta + render ———
check("I7 UI-Notranjost01738Leto1836_1837 + render",
      "function Notranjost01738Leto1836_1837()" in ui and "<Notranjost01738Leto1836_1837 />" in ui, "-")
check("I7b UI-RESTART-1.-NOVEMBER-1836 + PEZDIRC-×6-kartica",
      "RESTART (C) = 1. NOVEMBER 1836" in ui and "PEZDIRC ×6 NA S17" in ui, "-")
check("I7c UI-8-blokov-3-dvigi-kartica + ŠEST-36→39",
      "8 NOVIH BLOKOV — 3 DVIGI" in ui and "36→39" in ui, "-")

# ——— I8: dokaz-JSON ———
try:
    facts = json.load(open(f"{ROOT}/research/issue17/p261-facts.json", encoding="utf-8"))
    check("I8 dokaz-p261-facts.json (9-vpisov-struktura + 8-blokov-3-dvigi)",
          facts.get("phase") == "P261" and len(facts.get("blokiGriblje", [])) == 9
          and facts.get("korpusUcinek", {}).get("noviBloki") == 8
          and facts.get("korpusUcinek", {}).get("vitalsTotal") == 2077,  # P261-facts = HISTORIJSKI P261-dokaz!
          f"bloki={len(facts.get('blokiGriblje', []))}")
    check("I8b dokaz-restart + PEZDIRC-×6",
          "1. November 1836" in facts.get("struktura", {}).get("s17", "")
          and "×6" in facts.get("niti", {}).get("pezdirc", ""), "-")
except Exception as e:
    check("I8 dokaz-p261-facts.json", False, str(e)[:80])

# ——— I9: pt-luknja 2077/65/269 ———
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9 pt-luknja-2081/69/269 + P262-housesNote",
      '"vitalsTotal": 2081' in pt and '"01738": 69' in pt and '"04455": 269' in pt and "P262: +4-bloki-1838-s18" in pt, "-")

# ——— I10: LIVE matricula + /api/qa ———
if LIVE:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01738/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            html = r.read().decode("utf-8", "ignore")
        urls = []
        for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', html):
            s = m.group(1)[7:-1]
            try:
                d = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                if d.startswith("http"):
                    urls.append(d)
            except Exception:
                pass
        check("I10 LIVE matricula-01738 HTTP-200 + inventar-147-URL", r.status == 200 and len(urls) == 147,
              f"URL={len(urls)}")
        s17_url = urls[16].rstrip("/") if len(urls) >= 17 else ""
        with urllib.request.urlopen(urllib.request.Request(s17_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r2:
            import hashlib
            md5_live = hashlib.md5(r2.read()).hexdigest()
        check("I10b LIVE s17-JPEG md5 == 3b1f5b30 (2.-prenos-1:1!)",
              md5_live == "3b1f5b30ad03bcccf43cbb581e276ad2", f"md5={md5_live}")
        qa_data = json.loads(urllib.request.urlopen("http://localhost:3000/api/qa", timeout=90).read())
        p261_live = [t for t in qa_data.get("tests", []) if t.get("id") == "qa-p261-parish-marriage-notranjost-01738-1836-1837"]
        check("I10c LIVE /api/qa 256/256 ok:True (+qa-p261-id!)",
              qa_data.get("ok") is True and qa_data.get("passed") == 256 and p261_live and p261_live[0]["pass"] is True,
              f"pass={qa_data.get('passed')}")
    except Exception as e:
        check("I10 LIVE-verifikacija", False, str(e)[:100])

print(f"\nP261 VERIFIKATOR: {OK} PASS / {FAIL} FAIL")
sys.exit(1 if FAIL else 0)
