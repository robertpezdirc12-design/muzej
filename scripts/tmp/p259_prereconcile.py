#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — PRE-RECONCILE (brez VLM!): zbere pass1 + census L/R + datcol + hints
v konsenz/konflikt tabelo za vseh 36 vrstic. Priprava na KORAK 3, da bo
uskladitev po prihodu full-strip branj le še potrditev + razrešitev duelov."""
import json, re

D = "/tmp/p259"

def load_json(path):
    raw = open(path).read()
    i, j = raw.find("{"), raw.rfind("}")
    return json.loads(raw[i:j+1])

STRUCT = [
    ("s11", 13, 1, "L11", "R11", "m7"),   # s11 r1..r13 = 1833 m7..m19
    ("s12", 12, 1, "L12", "R12", "m20"),  # s12 r1..r6 = m20..m25; r7..r12 = 1834 m1..m6
    ("s13", 11, 7, "L13", "R13", "m7"),   # s13 r1..r11 = 1834 m7..m17 (rob 8..18)
]

def field(d, *keys):
    for k in keys:
        if d.get(k) not in (None, ""):
            return d[k]
    return ""

def split_entry(s):
    """'Nicolaus Rup Dobroviz 13' -> (ime+priimek, vas, hiša) — groba razčlenitev."""
    if not s: return ("", "", "")
    m = re.search(r"\s(\d+)(?![\d])\s*$", s)
    his = m.group(1) if m else ""
    rest = s[:m.start()] if m else s
    toks = rest.split()
    return (rest, "", his)

hints = json.load(open(f"{D}/hints.json"))

print("#"*100)
print("# P259 PRE-RECONCILE — konsenz/konflikt tabela iz 4 virov (pass1/censusL/censusR/datcol)")
print("# NAMEN: KORAK-3 pospešitev. polja ✓✓ = konsenz, ✗ = konflikt (duel kand.), ? = en sam vir")
print("#"*100)

for scan, n, r0, LID, RID, mtag in STRUCT:
    P = load_json(f"{D}/pass1_{scan}.json")
    L = load_json(f"{D}/census_{LID}.json").get("rows", [])
    R = load_json(f"{D}/census_{RID}.json").get("rows", [])
    DC = load_json(f"{D}/datcol_{scan}.json").get("rows", [])
    prows = P.get("rows", [])
    # pass1_s13 številči po ROBu (r8..r18) → preslikaj na indeks 0..10
    if scan == "s13" and prows and prows[0].get("r", 1) >= 8:
        prows = sorted(prows, key=lambda x: x.get("r", 0))
        prows = [{"r": i + 1, **{k: v for k, v in p.items() if k != "r"}} for i, p in enumerate(prows)]
    print()
    print("="*98)
    print(f"### {scan}  ({len(L)} censusL / {len(R)} censusR / {len(prows)} pass1 / {len(DC)} datcol)")
    print("="*98)
    for idx in range(n):
        r = idx + 1
        lrow = L[idx] if idx < len(L) else {}
        rrow = R[idx] if idx < len(R) else {}
        prow = prows[idx] if idx < len(prows) else {}
        drow = DC[idx] if idx < len(DC) else {}
        rob = lrow.get("rob", "") or prow.get("r", "")
        # --- DATUM: datcol + censusL + pass1
        d_dat = drow.get("datum", "")
        d_cen = lrow.get("datum", "")
        d_pas = prow.get("datum", "")
        dates = {d_dat, d_cen, d_pas} - {""}
        dmark = "✓✓" if len(dates) == 1 else ("✗" if len(dates) > 1 else "?")
        # --- ŽENIN: censusL vs pass1
        z_cen = lrow.get("zenin", "")
        z_pas = prow.get("zenin", "")
        zmark = "✓" if (z_cen and z_pas and z_cen.split()[:1] == z_pas.split()[:1]) else "✗?"
        # --- NEVESTA
        n_cen = lrow.get("nevesta", "")
        n_pas = prow.get("nevesta", "")
        nmark = "✓" if (n_cen and n_pas and n_cen.split()[:1] == n_pas.split()[:1]) else "✗?"
        hint = hints.get(f"{scan}_r{r}", "")
        hq = "H!" if hint else ""
        print(f"-- {scan}_r{r} (rob {rob or '—'}) {hq}")
        print(f"   DATUM[{dmark}]: datcol='{d_dat}' censusL='{d_cen}' pass1='{d_pas}'")
        print(f"   ŽENIN[{zmark}]: censusL='{z_cen}'")
        if z_pas: print(f"              pass1 ='{z_pas}'")
        print(f"   NEVESTA[{nmark}]: censusL='{n_cen}'")
        if n_pas: print(f"              pass1 ='{n_pas}'")
        print(f"   STARŠI/PRIČI (censusR): oZ='{field(rrow,'starsiZenina')}' / oN='{field(rrow,'starsiNeveste')}' | priči='{field(rrow,'price')}'")

print()
print("#"*100)
print("# KRITIČNA POLJA ZA KORPUS (Griblje-bloki — potrditi s full-strip + duel-i):")
print("#"*100)
for k, v in [
    ("s11_r2", "ženin: Pesdirz|Gosling|Gutting? + hiša 33|53|50? · nevesta: Bring|Brinc|Brung h24? → BLOK h53/h33 + h24!"),
    ("s12_r5", "ženin: Šimič|Schmig|Amiz? hiša 60? → BLOK h60 + DATUM-duel 19.|10.|26. Oct"),
    ("s12_r6", "ženin: Bring|Brung h28 → BLOK h28 (ŠIV-hiša! dvig 32!) + KRIŽAN-starši!"),
    ("s13_r6", "ženin: Vrh|Vrb hiša 58|68 + nevesta h51 → BLOKI h58|h68 + h51 (dvig 33?)"),
    ("s13_r11", "nevesta: MARENTIČ h24|29? + DATUM 10.|17. Febr → MARENTIČ-nit!"),
    ("s12_r7", "★RESTART-1834: DATUM 22.|27. Jän + ime Johann|Stephan?"),
    ("s13_r1", "DATUM-duel 5.|8. Febr (post-1834=12.2.-koledar-ne-odloča) + SISTEMATIK-SPOR-rob9-14! + priimka"),
]:
    print(f"  {k}: {v}")
