#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P95 fix — dokaz JSON: I6 statistika (h58 NI v PT naboru) + P-x labeli v opombah."""
import json

PATH = "research/issue17/parish-baptism-1900.json"
d = json.load(open(PATH, encoding="utf-8"))

# 1) I6 fix: h58 NI v PT verigi (PT_GAP_KNOWN v atlas.ts že vsebuje 58) — ptInNabor 13, gap 45/54/58
d["stats"]["ptInNabor"] = 13
d["stats"]["ptInNaborClean"] = 13
d["stats"]["ptGap"] = ["45", "54", "58"]
d["stats"]["ptGapNote"] = (
    "vsi trije že dokazani prej (45: 1896+97; 54: 1886+97; 58: 1889+90+92+95) "
    "— luknja 42/50/51 NESPREMENJENA (19 dokazanih v 41–60; scopingova h51 ZAVRŽENA: r49 = Primostek 5)"
)

# 2) r29 note: P90 → P91 (1896 = P91) + natančen opis 1896 dvoma (oče ni bil »neberljiv«,
#    ampak MERI dvom »ali drug Janez Brinec?« — 1896 P91 opomba)
for e in d["entries"]:
    if e["row"] == 29:
        for i, n in enumerate(e["notes"]):
            if "REŠUJE P90" in n:
                e["notes"][i] = (
                    "h14 = 2. VPIS; 1896 (P91) oče »Janez Brinec [~]« z MERI dvomom "
                    "(»ali drug Janez Brinec?« — isti priimek+ime kot h69 oče 1888–95); "
                    "1900 forenzika: Janez Brinec → REŠUJE P91 vprašanje očeta [~]"
                )
    # 3) r19 note: P91 → P88 (1893 = P88)
    if e["row"] == 19:
        for i, n in enumerate(e["notes"]):
            if "1893 P91" in n:
                e["notes"][i] = n.replace("1893 P91", "1893 P88")

json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("JSON popravljen: ptInNabor=13, ptGap=45/54/58, r29 P90→P91, r19 P91→P88")
