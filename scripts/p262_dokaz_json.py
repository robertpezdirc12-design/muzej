#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — kirurška posodobitev dokaz-JSON datotek (json-indent-1 = forma-intakt! cf. P261-lekcija):
parish-house-stories.json (six 39→41 + h17/h31-stories!) + pt-luknja-18-final.json (vitals 2077→2081, 01738 65→69)."""
import json

ROOT = "/home/z/my-project"

# ——— 1. parish-house-stories.json ———
P1 = f"{ROOT}/research/issue17/parish-house-stories.json"
pt = json.load(open(P1, encoding="utf-8"))
st = pt["structure"]
st["sixBook"] = 41
st["fiveBook"] = 27
sb = pt["sixBookHouses"]
sb["count"] = 41
sb["note"] = sb["note"].replace(
    "| P261: +3-h7/h39/h41 (vsi-5→6-knjig-prek-s17-01738-blokov!)",
    "| P261: +3-h7/h39/h41 (vsi-5→6-knjig-prek-s17-01738-blokov!) | P262: +2-h17/h31 (vsi-5→6-knjig-prek-s18-01738-blokov-1838!-h17-DVIG-37-2.-NAJVEČJI-NOTRANJOSTI!-h31-DVIG-19!)",
)
houses = sorted({int(x) for x in sb["houses"]} | {17, 31})
sb["houses"] = [str(n) for n in houses]
sb["stories"]["17"] = "★★★★★★ P262-hiša-DVIG-37-2.-NAJVEČJI-NOTRANJOSTI: m10-1838 (1. Februar d°!-proklamacija-6-Nov-1837!-s18-Pag. 33) — NEVESTA-Maria-KRAL-24-l-GRABLJE-17-×-ženin-Martin-PAPIGH-33-l-'Gerzhich-33'-[~X-OPEN!] = h17-1.-01738-BLOK — POROČNA-firstYear-1875→1838-DVIG-ZA-37-LET (2.-NAJVEČJI-DVIG-NOTRANJOSTI-po-h22-41-P255!-NAJVEČJI-P262!) — ŠEST-KNJIŽNA-5→6-knjig!"
sb["stories"]["31"] = "★★★★★★ P262-hiša-DVIG-19: m8-1838 (1. Februar d°!-proklamacija-1-Nov-1837!-s18-Pag. 33) — NEVESTA-Anna-TILAH-18-l-GRABLJE-31-×-ženin-Johann-KRISCHAN-20-l-GRABLJE-63-POLNI-DVOJNI-ALL-GRABLJE = h31-1.-01738-BLOK — POROČNA-firstYear-1857→1838-DVIG-ZA-19-LET — ŠEST-KNJIŽNA-5→6-knjig! + mladoletni-par-18l×20l-NAJMLAJŠI-01738-ženin!"
json.dump(pt, open(P1, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"[OK] house-stories.json: six-41/five-27/count-41/stories-{len(sb['stories'])} (+h17/h31!)")

# ——— 2. pt-luknja-18-final.json ———
P2 = f"{ROOT}/research/issue17/pt-luknja-18-final.json"
pt2 = json.load(open(P2, encoding="utf-8"))
pt2["generatedAt"] = "2026-11-15 (P262-posodobitev)"
corpus = pt2["corpus"]
corpus["vitalsTotal"] = 2081
corpus["byBook"]["01738"] = 69
note = corpus.get("housesNote", "")
if "P262: +4-bloki-1838-s18" not in note:
    corpus["housesNote"] = note + (" | P262: +4-bloki-1838-s18 (vitals 2077→2081, 01738 65→69!-h36-m6-nevesta-Anna-KRISCHAN "
                                   "+ h63-m8-ženin-Johann-KRISCHAN-4.-blok + h31-m8-nevesta-Anna-TILAH-DVIG-19 + h17-m10-nevesta-Maria-KRAL-DVIG-37-2.-NAJVEČJI-NOTRANJOSTI! "
                                   "- POLNI-DVOJNI-h63×h31-ALL-GRABLJE!-RESTART-(D)-1.-FEBRUAR-1838-7-porok-VSI-d°-PROKLAMACIJE-1-Nov/6-Nov-1837!-leta-01738-1828–1838-11-let-notranjosti!-ŠEST-KNJIŽNI-39→41!)")
json.dump(pt2, open(P2, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"[OK] pt-luknja-18-final.json: vitals-{corpus['vitalsTotal']}/01738-{corpus['byBook']['01738']}/housesNote-P262")
