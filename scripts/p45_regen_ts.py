#!/usr/bin/env python3
"""P45 — regenerate the TS PS_LEXICON_VERIFIED_P45 families block from the
canonical research/issue17/ps-lexicon-verified.json (deterministic, one-shot).
"""
import json
import re
from pathlib import Path

j = json.load(open("research/issue17/ps-lexicon-verified.json", encoding="utf-8"))


def trunc(s: str, n: int) -> str:
    s = s or ""
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0] + "…"


ORDER = {"NEPOTRJENO": 0, "DELNO": 1, "NEVERIFIKATORNO": 2, "POTRJENO": 3, "BREZ-VIRA": 4}

fam_js: list[str] = []
for f in j["families"]:
    vc = {"POTRJENO": 0, "DELNO": 0, "NEPOTRJENO": 0, "NEVERIFIKATORNO": 0, "BREZ-VIRA": 0}
    for h in f["hypotheses"]:
        vc[h["verification"]["verdict"]] += 1
    # do 3: sortiranje po verdict-prioriteti, deduplikacija po primarni tarči
    # (variante z enakim virom samo enkrat — npr. Öfling ×2 na dwb-oede)
    seen_t: set[str] = set()
    picked = []
    for h in sorted(f["hypotheses"], key=lambda h: ORDER[h["verification"]["verdict"]]):
        prim = h["verification"]["targets"][0]["id"] if h["verification"]["targets"] else "\u0000"
        if prim in seen_t:
            continue
        seen_t.add(prim)
        picked.append(h)
        if len(picked) == 3:
            break
    hyps = picked
    tops = []
    for h in hyps:
        v = h["verification"]
        url = v["targets"][0].get("url") if v["targets"] else None
        tops.append(
            "{ candidate: " + json.dumps(h["candidate"], ensure_ascii=False)
            + ", source: " + json.dumps(trunc(h["source"], 46), ensure_ascii=False)
            + ', verdict: "' + v["verdict"] + '", confidence: "' + v["confidence"] + '"'
            + ", noteSi: " + json.dumps(trunc(v["noteSi"], 235), ensure_ascii=False)
            + ", url: " + (json.dumps(url, ensure_ascii=False) if url else "null")
            + " }"
        )
    vc_js = "{ " + ", ".join(
        ('"BREZ-VIRA": ' + str(c)) if k == "BREZ-VIRA" else (k + ": " + str(c))
        for k, c in vc.items()
    ) + " }"
    fam_js.append(
        '{ id: "' + f["id"] + '", pairs: ' + str(f["pairs"]) + ", verdictCounts: " + vc_js
        + ", topHypotheses: [" + ", ".join(tops) + "] }"
    )

new_block = "  families: [\n    " + ",\n    ".join(fam_js) + ",\n  ],\n"

ts_path = Path("src/data/atlas/research.ts")
ts = ts_path.read_text(encoding="utf-8")
start = ts.index("export const PS_LEXICON_VERIFIED_P45")
end = ts.index("export const PZ_ECONOMY_1825")
seg = ts[start:end]
vi = seg.index("  families: [")
ki = seg.index("  keyFindingsSi: [")
assert vi < ki, "unexpected P45 segment layout"
seg = seg[:vi] + new_block + seg[ki:]
ts = ts[:start] + seg + ts[end:]
ts_path.write_text(ts, encoding="utf-8")
print("TS families block regenerated:", len(fam_js), "families")
