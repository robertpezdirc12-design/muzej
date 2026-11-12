#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — worklog-vnos + README-posodobitve (banner + kazalo + tabela + korpus + Zadnje-stanje + Odprto).
CONFIG-DRIVEN: bere scripts/tmp/p259-docs.json (zapiše ga zaključni korak!):
  {"worklogEntry": "## P259 — ...", "banner": "> ...", "bullet": "- **P259 ...",
   "tabelaRow": "| ... |", "korpusNote": "...", "odprtoNew": "...", "evidenceNote": "...",
   "total": N, "byBook01738": M, "sixCount": S, "bothEra": B}
Ankri = P258-besedila (stabilna!). Po vzoru scripts/tmp/p258_docs.py."""
import json
import sys
import os

CFG = "scripts/tmp/p259-docs.json"
if not os.path.exists(CFG):
    print(f"MANJKA {CFG}! Zapiši ga po zaključku P259 (worklogEntry/banner/bullet/tabelaRow/korpusNote/odprtoNew/evidenceNote + števke) in ponovno zaženi.")
    sys.exit(2)
cfg = json.load(open(CFG, encoding="utf-8"))
WL = cfg["worklogEntry"]; BANNER = cfg["banner"]; BULLET = cfg["bullet"]
TAB = cfg["tabelaRow"]; KORPUS = cfg["korpusNote"]; ODPRTO = cfg["odprtoNew"]
EVID = cfg["evidenceNote"]
N = cfg["total"]; M = cfg["byBook01738"]; S = cfg["sixCount"]; B = cfg["bothEra"]

# ——— 1) worklog ———
with open("worklog.md", "a", encoding="utf-8") as f:
    f.write("\n" + WL if not WL.startswith("\n") else WL)
print("worklog P259 dodan")

# ——— 2) README ———
R = "README.md"
r = open(R, encoding="utf-8").read()

# banner: novi P259-banner nad P258
old_banner_marker = "> **11. november 2026 · po P258 ·"
assert old_banner_marker in r, "banner-sidro (po P258) ni najdeno!"
r = r.replace(old_banner_marker, BANNER + "\n" + old_banner_marker, 1)

# kazalo-anchor
r = r.replace("[Zadnje stanje raziskave](#zadnje-stanje-raziskave-po-p258--2026-11-11)",
              "[Zadnje stanje raziskave](#zadnje-stanje-raziskave-po-p259--2026-11-12)")

# tabela-vrstica 01738 (P258 → P259)
OLD_TAB_MARK = "| Poročna PREDHODNIK 01738 | Matricula Online | **leta 1873 + 1828–1833 (notranjost!)"
i = r.find(OLD_TAB_MARK)
assert i >= 0, "tabela-sidro (P258-01738-vrstica) ni najdeno!"
j = r.find("\n", i)
r = r[:i] + TAB + r[j:]

# korpus-vrstica
r = r.replace("**Korpus (po P258):** **2059 vitalov**", f"**Korpus (po P259):** **{N} vitalov**")
OLD_47 = "**47 poročnih blokov 01738-predhodnika (1873-m1–m17 P253 + 1828 P255 + 1829 P256 + 1830/1831 P257 + 1831-konec/1832/1833 P258 — leta 1828–1833+1873!)**"
assert OLD_47 in r, "korpus-47-sidro ni najdeno!"
r = r.replace(OLD_47, KORPUS)
r = r.replace("78 Griblje + 16 druga-vas + 6 neznan — **31 šest-knjiž-hiš po P258 (+8: h2/h8/h35/h36/h42/h46/h47/h48!)**)",
              f"78 Griblje + 16 druga-vas + 6 neznan — **{S} šest-knjiž-hiš po P259!**)")
OLD_VITALS = "(po P258: vitals 2059 · 04455 269 = 74-predzgodovina + 195-linija-1:1 · 01738 47 = 11-1873 + 3-1828 + 6-1829 + 1-1830 + 15-1831 (h3/h33/h50/h54/h56/h26/h27/h65/h1/h11 + h47/h46/h8/h48/h2!) + 9-1832 (h22/h35-×2/h2/h42/h36/h66/h56/h61!) + 2-1833 (h50/h49-PESDIRZ!)"
assert OLD_VITALS in r, "vitals-47-sidro ni najdeno!"
r = r.replace(OLD_VITALS, f"(po P259: vitals {N} · 04455 269 = 74-predzgodovina + 195-linija-1:1 · 01738 {M} = 11-1873 + 3-1828 + 6-1829 + 1-1830 + 15-1831 + 9-1832 + 2-1833 (P258) + {M-47}-1833k/1834 (P259!)")

# dokazi
r = r.replace("+ `research/issue17/parish-marriage-notranjost-1832.json` (P258: 40-vpisov!)",
              "+ `research/issue17/parish-marriage-notranjost-1832.json` (P258: 40-vpisov!)" + (f"\n{EVID}" if EVID else ""))

# Odprto: P258-lead → P259-izveden + P260-lead
OLD_ODP = "nadaljevanje P258: **MEJA-1831/32/33 PREBRANA (P258!)**"
assert OLD_ODP in r, "odprto-sidro ni najdeno!"
r = r.replace(OLD_ODP, ODPRTO)

# Zadnje stanje — naslov + novi bullet
r = r.replace("## Zadnje stanje raziskave (po P258 · 2026-11-11)", "## Zadnje stanje raziskave (po P259 · 2026-11-12)")
old_bullet = "- **P258 (NOTRANJOST-01738: MEJA-1831/32/33!) ZAKLJUČENA**"
assert old_bullet in r, "bullet-sidro (P258) ni najdeno!"
r = r.replace(old_bullet, BULLET + "\n" + old_bullet, 1)

open(R, "w", encoding="utf-8").write(r)
print(f"README posodobljen (banner + kazalo + tabela + korpus {N}/{M}/{S}/{B} + odprto + Zadnje-stanje)")
