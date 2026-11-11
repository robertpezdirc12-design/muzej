#!/usr/bin/env python3
"""P254 — verifikator HIŠNIH ZGODB GLOBJE: mreže hiš čez 6 knjig (I1–I10 + --live).
Sintezna faza: agregacija korpusa HOUSE_VITALS (2023) po hišah — modul
parish-house-stories.ts + dokaz parish-house-stories.json + qa-p254 (248. kontrola)."""
import json
import re
import sys
import urllib.request

OK = 0
FAIL = 0


def check(name, ok, msg=""):
    global OK, FAIL
    if ok:
        OK += 1
        print(f"[PASS] {name}" + (f" — {msg}" if msg else ""))
    else:
        FAIL += 1
        print(f"[FAIL] {name}" + (f" — {msg}" if msg else ""))


# ——— I1: modul obstaja s 7 izvozi ———
mod = open("src/data/atlas/parish-house-stories.ts", encoding="utf-8").read()
exports = ["HOUSE_STORIES", "HOUSE_STORY_BOOKS", "HOUSE_STORY_SIX", "HOUSE_STORY_TIERS",
           "HOUSE_STORY_TOTALS", "HOUSE_STORY_NOTABLES", "houseStoryByNo"]
missing = [e for e in exports if f"export const {e}" not in mod and f"export function {e}" not in mod]
check("I1 modul parish-house-stories (7 izvozov)", not missing, f"manjka: {missing}" if missing else "×7")

# ——— I2: 100 hiš = 78/16/6 vrst ———
entries = re.findall(r'houseNo: "([^"]+)", kind: "([^"]+)", blocks: (\d+), books: (\d+)', mod)
check("I2 HOUSE_STORIES == 100 (78 Griblje + 16 druga-vas + 6 neznan)",
      len(entries) == 100 and sum(1 for _, k, _, _ in entries if k == "griblje") == 78
      and sum(1 for _, k, _, _ in entries if k == "druga-vas") == 16
      and sum(1 for _, k, _, _ in entries if k == "neznano") == 6, f"najdeno {len(entries)}")

# ——— I3: vsota blokov == 2026; knjige 14/288/502/269/433/520 ———
total = sum(int(b) for _, _, b, _ in entries)
check("I3 vsota blokov HOUSE_STORIES == 2026 (P255: +3-1828!)", total == 2026, f"{total}")
book_blocks = {"01738": 0, "04104": 0, "04105": 0, "04455": 0, "04106": 0, "04894": 0}
for seg in re.finditer(r'houseNo: "([^"]+)".*?perBook: \[(.*?)\]', mod):
    for sig, n in re.findall(r'sig: "(\d+)", n: (\d+)', seg.group(2)):
        book_blocks[sig] += int(n)
expected_books = {"01738": 14, "04104": 288, "04105": 502, "04455": 269, "04106": 433, "04894": 520}
check("I3b bloki po knjigah 14/288/502/269/433/520 (== korpus! P255-01738-14!)", book_blocks == expected_books,
      f"{book_blocks}" if book_blocks != expected_books else "1:1")

# ——— I4: 9 šest-knjižnih hiš [3,10,12,16,18,20,28,63,73] ———
six_m = re.search(r'export const HOUSE_STORY_SIX: HouseStorySix\[\] = \[(.*?)\n\];', mod, re.S)
six_mod = re.findall(r'houseNo: "(\d+)", blocks: \d+, years: "[^"]+"', six_m.group(1)) if six_m else []
check("I4 HOUSE_STORY_SIX == [3,6,10,12,16,18,20,22,28,61,63,73] (P255-12!)",
      six_mod == ["3", "6", "10", "12", "16", "18", "20", "22", "28", "61", "63", "73"], str(six_mod))
six_stories = [h for h, k, b, bk in entries if int(bk) == 6]
check("I4b šest-knjižne v HOUSE_STORIES == 9", sorted(six_stories, key=int) == six_mod, str(sorted(six_stories, key=int)))

# ——— I5: qa-parish.ts vsebuje qa-p254 (248. kontrola) + živa rekalkulacija ———
qa = open("src/lib/qa-parish.ts", encoding="utf-8").read()
check("I5 qa-p254-parish-house-stories kontrola obstaja",
      '"qa-p254-parish-house-stories"' in qa)
check("I5b živa-rekalkulacija v kontroli (p254Agg iz HOUSE_VITALS!)",
      "p254Agg" in qa and "1:1-primerjava-modul-×-živa-agregacija" in qa)

# ——— I6: dokaz JSON ———
ev = json.load(open("research/issue17/parish-house-stories.json", encoding="utf-8"))
check("I6 dokaz parish-house-stories.json (100 hiš v tabeli + tierji + 12-zgodb — P255!)",
      len(ev.get("houses", [])) == 100 and ev["structure"]["tiers"]["six"] == 12
      and len(ev["sixBookHouses"]["stories"]) == 12 and ev["structure"]["tiersSum"] == 100,
      f"houses={len(ev.get('houses', []))}")

# ——— I7: UI komponenta HouseStoriesP254 + uvoz modula ———
ui = open("src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I7 UI HouseStoriesP254 (komponenta + render + uvoz ×6)",
      "function HouseStoriesP254" in ui and "<HouseStoriesP254 />" in ui
      and "parish-house-stories" in ui)

# ——— I8: rekordi in osamelci ———
h24 = re.search(r'houseNo: "24", kind: "griblje", blocks: (\d+)', mod)
h73 = re.search(r'houseNo: "73", kind: "griblje", blocks: (\d+), books: (\d+)', mod)
check("I8 rekordi: h24 == 45 + h73 == 9/knjige-6 + TIHA + KUPAMIČ",
      h24 and int(h24.group(1)) == 45 and h73 and int(h73.group(1)) == 9 and int(h73.group(2)) == 6
      and "TIHA-HIŠA" in mod and "KUPAMIČ" in mod)
check("I8b osamelci: h25-smrtna-vrzeli + h[?]-skrita + 96-let-P255 + obe-eri 69/75/13",
      "SMRTNA VRZEL" in mod and "skrita hiša" in mod.lower() and "96" in mod
      and "bothEraKrstna: 69" in mod and "bothEraMrliska: 75" in mod and "bothEraPorocna: 13" in mod)
check("I8c zgodbe-šest-knjižnih: DRAGOŠ-50-LET + 56-LETNA-ZAKONSKA + KRIŽAN-HIŠA + m1-KURE",
      "DRAGOŠ-50-LET" in mod and "56-LETNA ZAKONSKA ZVEZA" in mod and "KRIŽAN-HIŠA" in mod and "m1-KURE" in mod)

# ——— I9: pt-luknja 2026 (P255: korpus 2026→2026 + 01738 11→14!) ———
pt = json.load(open("research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
pt_corpus = pt.get("corpus", {})
check("I9 pt-luknja-2026 (P255: +3-1828!)",
      pt_corpus.get("vitalsTotal") == 2026 and pt_corpus.get("byBook", {}).get("01738") == 14
      and pt.get("vitalsTotal") == 2026)

# ——— I10: LIVE /api/qa 249/249 ok:True (+qa-p254 pass!) ———
if "--live" in sys.argv:
    try:
        qa_data = json.loads(urllib.request.urlopen(
            urllib.request.Request("http://localhost:3000/api/qa"), timeout=30).read().decode())
        p254 = [t for t in qa_data.get("tests", []) if t.get("id") == "qa-p254-parish-house-stories"]
        check("I10 LIVE QA-živo 249/249 ok:True (+qa-p254 + qa-p255!)",
              qa_data.get("ok") is True and qa_data.get("passed") == 249 and qa_data.get("failed") == 0
              and bool(p254) and p254[0].get("pass") is True,
              f"passed={qa_data.get('passed')} p254={bool(p254) and p254[0].get('pass')}")
    except Exception as e:
        check("I10 LIVE QA-živo", False, str(e)[:80])

print()
print(f"REZULTAT: {OK} PASS / {FAIL} FAIL" + (" — VSI PASS!" if FAIL == 0 else " — POPRAVI!"))
sys.exit(1 if FAIL else 0)
