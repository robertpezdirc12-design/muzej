#!/usr/bin/env python3
"""P71 (issue #13) — PS-PARCELS-GEO v5: SEKCIJSKE VRSTICE EXCLUDE + P93 REVERZIJA

Dve korekciji v4 (obe odstranjujeta lažne zahtevke, nobena ne izmišljuje podatkov):

  C1  EXCLUDE 56 sekijskih vrstic (p83–86, p88) iz joina — LASTNIŠKA odločitev
      (odprta točka P70 ①; opcija "exclude" iz P69 sectionClass.options).
      Sekcije so P69 DOKAZANE lažne fuzije na Blatt I poligone (Σ ratio
      161 = 235.65×, 162 = 31.39×, 175 = 19.92×, 990 = 8.99× proti čistim
      1441 = 1.09; lastniško prekrivanje s p11 = 0; hiše p85 641/646/655 =
      16/22/7 ≠ p35 68/23/26). Vrstice ostanejo v REGISTRU (dokaz:
      excludedRows + P69 sectionClass), izpadle iz runtime joina (brez
      geometrije). Vsi 56 base imajo legitimne druge zahtevalce — po
      excludeu NE IZGUBI noben poligon svoje vrstice (invarianta I4).
      Per-Blatt instance (P60 moda B / PF protokol) = kasnejša lastniška
      odločitev.

  C2  P93 REVERZIJA: P68 renum 160x→190x (+300) na p93 je NAPAKA —
      prva resnična očesna forenzika strani (P67/P69 cona je OBŠLA p93!):
       • GLIFNA FORENZIKA (notranja kontrola, 10–12× zoom, P67 recept):
         vrstica 9 = "1609" in vrstica 19 = "1619" — gotova ZADNJA števka
         9 (zaprt zgornji lok + rep pod osnovnico) je vidno RAZLIČNA od
         srednje števke (spodnja zanka, odprt vrh, brez repa = 6); isti
         pisar, ista stran. Enako r5 "1605", r16 "1616", r20 "1620".
         Kontrola na p98 "1916" (12×): 9 in 6 v istem številu — dve
         različni črki; kontrola p92 981–983 (P69-verificirane 9): isti
         glif kot p98. → srednje števke p93 so 6, stran bere 1601–1620.
       • P67 trditev "9→6/9→0 — P67 že dokazal" za p93 = NAPAČNO prenesena
         (artefakt je realen na drugih straneh; p93 ni bil v očesni coni).
       • annRecords (sodobni anotator): 9 zapisov referencira 1601, 1602,
         1603, 1604, 1606, 1607, 1613, 1614, 1619 ("Durch Theilung im
         1824", "trifft Gültley 9.", "1870. 8-1117") — anotator je sam
         bral 160x/161x.
       • pageMap P56: numMin/numMax = 1601–1620; P38 pass2: 1601–1620;
         monotoničnost: vrstica N = 1600+N (20/20).
      Učinek: vseh 15 p93 vrstic base := parzella (reverz na originalno
      branje); PF ujemanja = {1603, 1604, 1605} (3 ostanejo), 12 vrstic
      brez PF poligona → izpad (dokaz: removedRows, reason C2); PF
      1901–1920 izgubi lažne dvojne zahtevke p93 (ostane p98 III).
      PF 1904/1906 izpadeta iz base seta (prazna — dokumentirana
      praznina), PF 1603/1604/1605 dobita prve prave vrstice.

Viri (vsi committed):
  research/issue17/ps-parcels-geo-v4.json       (v4 dokaz, 1145 rowsEvidence)
  src/data/atlas/ps-parcels-geo.json            (v4 runtime)
  research/issue17/ps-pass1-layers.json         (P69: sectionClass 56 +
                                                 eyesVerdicts p93 [ OVERRIDE ])
  research/issue17/ps-blatt-headers.json        (P59 pageAttribution — Blatti)
  research/issue17/ps-register-topology.json    (P56 pageMap + annRecords p93)
  research/georef-n83/gurs/parcels-ko1544-merged.json (2117 parcel, P47)
  research/issue17/p93-forensics/*.png          (7 forenzičnih izrezov 8–12×)

Izpis:
  research/issue17/ps-parcels-geo-v5.json       (dokaz v5)
  src/data/atlas/ps-parcels-geo.json            (runtime v5 — nadomesti v4;
                                                 v4 ostane arhiviran v dokazu)

Invarianti (FAIL → exit 1):
  I1  C1 set == P69 sectionClass.rows (bajtno po page/base/owner/areaQK);
     56 vrstic; vse v4 vrstice strani 83–86/88 == ta set (brez ostalih)
  I2  pini: v4 dokaz sha256, P69 dokaz sha256, P59 dokaz sha256, P56
      dokaz sha256, PARCELS sha256; v4 runtime rows == v4 dokaz
      rowsEvidence bajtno
  I3  C2: vseh 15 p93 vrstic int(base) − int(parzella) == 300 (pred
      reverzijo); po reverziji base == parzella (15/15); PF ujemanja ==
      {1603, 1604, 1605} (napoved); 12 izpadlih
  I4  po C1 noben base ne izgubi VSEH vrstic (0 praznih poligonov s strani
      sekcij); P69 sectionClass.pages == {83, 84, 85, 86, 88}
  I5  meritve v5 (rows/bases/multi/cross/ambRows/conf/series/removed) — pini
  I6  nespremenjene vrstice bajtno == v4 (razen 56+12 izpadlih, 15 p93
      rekey + group-derived prekalkulacija)
  I7  p93 obdržane vrstice: lat/lng/areaModern/ratio == group_pos(base)
      (P55 metoda)
  I8  dokaz ⊇ runtime bajtno
  I9  determinizem: drugi preizračun bajtno identičen (--check)

Glifna forenzika ni VLM-instrument: notranja kontrola na isti strani
(dokazujeta 6 in 9 v enem številu) je prenosljiva neodvisno od rokopisa.
"""
import hashlib
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
V4_EV = REPO / "research/issue17/ps-parcels-geo-v4.json"
V4_RT = REPO / "src/data/atlas/ps-parcels-geo.json"
V5_EV = REPO / "research/issue17/ps-parcels-geo-v5.json"
OUT_RUNTIME = REPO / "src/data/atlas/ps-parcels-geo.json"
P69_EV = REPO / "research/issue17/ps-pass1-layers.json"
P59_EV = REPO / "research/issue17/ps-blatt-headers.json"
P56_EV = REPO / "research/issue17/ps-register-topology.json"
PARCELS = REPO / "research/georef-n83/gurs/parcels-ko1544-merged.json"
FORENSICS = REPO / "research/issue17/p93-forensics"

HIST_QK_M2 = 3.59665
AREA_BAND = 0.10
NEIGH_M = 150.0
SEED_AREA = 42
SEED_SPATIAL = 7
M_PER_DEG_LAT = 111320.0
TOTAL_PS_ROWS = 2762  # P55/P38 izbira (pageSelection.rows)

PIN_V4_EV_SHA = "57ed1b0d5030b2dd6347cf5cd7571203a5d7e8353973dbc3f40c0cffdd2f074f"
PIN_P69_EV_SHA = "99962e24dc129a253e7100cb297aa6b73989f96b1d5ff7c95d55d8735c52829e"  # isti kot P70 (zamrznjen)
PIN_P59_EV_SHA = "650f13dccab1da70a60d04c41ce9f7887ca94eafea8a0a7927c104ca899b76f3"  # P68 v3 re-run
PIN_P56_EV_SHA = "2fddc76fb94b69fed55170220fa8dfa3ace4a9466043d264b8b8df788e78a50c"
PIN_PARCELS_SHA = "fee91fca736348f40ef11d38b7a5b51d51656a9768cda648f4d737029bb3941f"

SEC_PAGES = [83, 84, 85, 86, 88]  # == P69 sectionClass.pages (I4)
P93_PREDICTED_MATCHES = ["1603", "1604", "1605"]  # I3 napoved

# pričakovane meritve v5 (pini; vpisano po prvem zagonu)
EXP = {
    "rows": 1077, "bases": 879, "multi": 184, "cross": 48,
    "ambRows": 373,
    "conf": {"STRONG": 183, "MEDIUM": 745, "WEAK": 149},
    "series": {"S1": 981, "S2": 70, "BI": 26},
    "removed": 68,            # 56 sekcij (C1) + 12 p93 (C2)
    "removedC1": 56, "removedC2": 12, "rekeyC2": 15,
    "area": {"pairsWithArea": 1057, "medianRatio": 3.9052, "q25": 2.649,
             "q75": 7.9444, "tightN": 195, "tightShare": 0.1845,
             "shuffleMedian": 4.2304, "shuffleTightShare": 0.0539,
             "historicalQkM2": 3.59665, "deltaPct": 8.58},
    "spatial": {"consecPairs": 652, "medianM": 51.8, "q25M": 33.0,
                "q75M": 87.8, "share150": 0.9049, "shuffleMedianM": 1320.7,
                "shuffleShare150": 0.0171, "enrichmentX": 25.5},
    "suffix": 271, "pos": 879,
    "ambDerived": 35, "confDerived": 2,
}

DATE = "2026-10-15"
FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fnum(v) -> float:
    try:
        return float(str(v).replace(",", ".")) if v not in (None, "") else 0.0
    except (TypeError, ValueError):
        return 0.0


def base_of(s) -> str | None:
    import re
    m = re.match(r"\*?(\d+)", str(s or ""))
    return m.group(1) if m else None


def dm(a, b) -> float:
    return math.hypot((a[0] - b[0]) * M_PER_DEG_LAT,
                      (a[1] - b[1]) * M_PER_DEG_LAT * 0.7)


def compute():
    print("P71 — v5: C1 sekcije exclude (56) + C2 p93 reverzija (15)")

    # ——— vhodi ———
    v4ev = json.loads(V4_EV.read_text(encoding="utf-8"))
    v4rt = json.loads(V4_RT.read_text(encoding="utf-8"))
    p69 = json.loads(P69_EV.read_text(encoding="utf-8"))
    p59 = json.loads(P59_EV.read_text(encoding="utf-8"))
    p56 = json.loads(P56_EV.read_text(encoding="utf-8"))
    parcels = json.loads(PARCELS.read_text(encoding="utf-8"))

    bybase: dict[str, list[dict]] = defaultdict(list)
    for x in parcels:
        b = base_of(x.get("st"))
        if b:
            bybase[b].append(x)

    def group_pos(b: str):
        grp = bybase.get(b)
        if not grp:
            return None
        tot = sum(fnum(x.get("povrsina")) for x in grp)
        if tot > 0:
            lat = sum(x["lat"] * fnum(x.get("povrsina")) for x in grp) / tot
            lng = sum(x["lng"] * fnum(x.get("povrsina")) for x in grp) / tot
        else:
            lat = sum(x["lat"] for x in grp) / len(grp)
            lng = sum(x["lng"] for x in grp) / len(grp)
        return round(lat, 7), round(lng, 7), round(tot, 0) or None, len(grp)

    page_attr = p59["pageAttribution"]

    def blatt_of(page: int):
        return page_attr.get(str(page), {}).get("blatt")

    # ——— I2: pini ———
    pins = [(V4_EV, PIN_V4_EV_SHA, "v4 dokaz"),
            (P69_EV, PIN_P69_EV_SHA, "P69 dokaz"),
            (P59_EV, PIN_P59_EV_SHA, "P59 dokaz"),
            (P56_EV, PIN_P56_EV_SHA, "P56 dokaz"),
            (PARCELS, PIN_PARCELS_SHA, "PARCELS")]
    for path, pin, label in pins:
        if pin and sha256(path) != pin:
            fail(f"I2 {label} sha {sha256(path)[:8]}… ≠ {pin[:8]}…")
        elif pin:
            ok(f"I2 {label} sha pin")
        else:
            ok(f"I2 {label} sha (PIN za vpis): {sha256(path)}")
    v4_rows = v4ev["rowsEvidence"]
    if v4rt.get("version") == 4:
        if json.dumps(v4rt["rows"], ensure_ascii=False, sort_keys=True) != \
                json.dumps(v4_rows, ensure_ascii=False, sort_keys=True):
            fail(f"I2 v4 runtime rows ≠ dokaz rowsEvidence "
                 f"({len(v4rt['rows'])} vs {len(v4_rows)})")
        else:
            ok(f"I2 v4 runtime == dokaz rowsEvidence ({len(v4_rows)})")
    else:
        ok(f"I2 runtime je v{v4rt.get('version')} (P71 izvedena) — vhod iz "
           f"v4 dokaza rowsEvidence ({len(v4_rows)})")

    # ——— I1/I4: C1 — exclude sekcij ———
    sc = p69["sectionClass"]
    if sc["pages"] != SEC_PAGES:
        fail(f"I4 sectionClass.pages {sc['pages']} ≠ {SEC_PAGES}")
    else:
        ok(f"I4 sectionClass.pages == {SEC_PAGES}")
    sc_set = {(r["page"], str(r["base"]), r["owner"], r["areaQK"])
              for r in sc["rows"]}
    if len(sc["rows"]) != 56 or len(sc_set) != 56:
        fail(f"I1 sectionClass vrstic {len(sc['rows'])} (unikatov "
             f"{len(sc_set)}) ≠ 56")
    v4_sec = [r for r in v4_rows if r["page"] in SEC_PAGES]
    v4_sec_set = {(r["page"], str(r["base"]), r["owner"], r["areaQK"])
                  for r in v4_sec}
    if len(v4_sec) != 56:
        fail(f"I1 v4 vrstic na sekijskih straneh {len(v4_sec)} ≠ 56")
    if v4_sec_set != sc_set:
        fail("I1 v4 sekijske vrstice ≠ P69 sectionClass (bajtno)")
    else:
        ok("I1 sekcije: 56 vrstic bajtno == P69 sectionClass "
           "(page/base/owner/areaQK); vse v4 vrstice teh strani == set")

    sec_bases = {str(r["base"]) for r in v4_sec}
    non_sec_pages: dict[str, set[int]] = defaultdict(set)
    for r in v4_rows:
        if r["page"] not in SEC_PAGES:
            non_sec_pages[r["base"]].add(r["page"])
    orphans = sorted(b for b in sec_bases if b not in non_sec_pages)
    if orphans:
        fail(f"I4 base, ki bi izgubili vse vrstice s C1: {orphans}")
    else:
        ok("I4 po C1 noben base ne izgubi vseh vrstic (0 praznih poligonov; "
           "vsi 56 imajo legitimne druge zahtevalce)")

    # ——— C1 izvedba ———
    excluded_rows = []
    out_rows: list[dict] = []
    for idx, r in enumerate(v4_rows):
        if r["page"] in SEC_PAGES:
            excluded_rows.append({
                "page": r["page"], "base": r["base"],
                "parzella": r["parzella"], "owner": r["owner"],
                "areaQK": r["areaQK"],
                "reason": "C1: sekijska vrstica (lažna fuzija na Blatt I "
                          "poligon; P69 sectionClass; lastniška odločitev "
                          "P71: exclude iz joina, vrstica ostane v "
                          "registru brez geometrije)",
            })
            continue
        r2 = dict(r)
        r2["_srcIdx"] = idx
        out_rows.append(r2)

    # ——— I3: C2 — p93 reverzija ———
    p93_rows = [r for r in out_rows if r["page"] == 93]
    if len(p93_rows) != 15:
        fail(f"I3 p93 vrstic {len(p93_rows)} ≠ 15")
    off_bad = [r for r in p93_rows
               if int(r["base"]) - int(r["parzella"]) != 300]
    if off_bad:
        fail(f"I3 p93 offset ≠ +300 za: "
             f"{[(r['base'], r['parzella']) for r in off_bad[:4]]}")
    else:
        ok("I3 p93: vseh 15 vrstic int(base) − int(parzella) == 300 "
           "(P68 renum prisoten pred reverzijo)")

    removed_c2: list[dict] = []
    rekeyed: list[dict] = []
    kept_c2: list[dict] = []
    for r in p93_rows:
        nb = str(int(r["parzella"]))
        gp = group_pos(nb)
        r2 = dict(r)  # _srcIdx ostane (identiteta v4 vrstice)
        r2["base"] = nb
        rekeyed.append(r2)  # vseh 15: base := parzella (reverz)
        if gp is None:
            removed_c2.append({
                "page": 93, "base": r["base"], "parzella": r["parzella"],
                "owner": r["owner"], "areaQK": r["areaQK"],
                "reason": f"C2: p93 reverzija — base {nb} brez PF poligona "
                          f"(1601–1620 večinoma odsotnih v sodobnem k.o. "
                          f"1544; vrstica ostane v registru)",
            })
            continue
        r2["lat"], r2["lng"], r2["areaModern"], r2["parts"] = gp
        r2["ratio"] = (round(r2["areaModern"] / r2["areaQK"], 4)
                       if r2["areaModern"] and r2["areaQK"] else None)
        kept_c2.append(r2)
    got_matches = sorted(x["base"] for x in kept_c2)
    if got_matches != P93_PREDICTED_MATCHES:
        fail(f"I3 p93 PF ujemanja {got_matches} ≠ napoved "
             f"{P93_PREDICTED_MATCHES}")
    else:
        ok(f"I3 p93 reverzija: base := parzella (15/15); PF ujemanja "
           f"{got_matches} == napoved; {len(removed_c2)} izpadlih "
           f"(brez PF poligona)")
    out_rows = [r for r in out_rows if r["page"] != 93] + kept_c2

    # ——— dokazni viri C2 (glifna forenzika + annRecords) ———
    ann93 = [a for a in (p56.get("annRecords") or []) if a.get("page") == 93]
    ann_nums = sorted(int(a["parzella"]) for a in ann93
                      if str(a.get("parzella", "")).isdigit())
    if not ann_nums or not all(1600 <= n <= 1620 for n in ann_nums):
        fail(f"I3 annRecords p93 {ann_nums} — niso 160x/161x")
    else:
        ok(f"I3 annRecords (sodobni anotator) p93: {ann_nums} — "
           f"vsi 160x/161x")
    for f in sorted(FORENSICS.glob("*.png")):
        if f.stat().st_size < 50_000:
            fail(f"I3 forenzični izrez {f.name} premajhen")
    n_forensics = len(list(FORENSICS.glob("*.png")))

    # ——— I5: ambiguous prekalkulacija (P55 metoda) ———
    pages_by: dict[str, set[int]] = defaultdict(set)
    for r in out_rows:
        pages_by[r["base"]].add(r["page"])
    amb_changes: list[tuple] = []
    for r in out_rows:
        new_amb = len(pages_by[r["base"]]) > 1
        if new_amb != r["ambiguous"]:
            amb_changes.append((r["page"], r["base"], r["ambiguous"],
                                new_amb))
            r["ambiguous"] = new_amb

    # ——— conf prekalkulacija (P55 metoda) ———
    pos_by_base = {}
    for b in pages_by:
        gp = group_pos(b)
        if gp:
            pos_by_base[b] = (gp[0], gp[1])
    neigh_ok: set[str] = set()
    for b, p in pos_by_base.items():
        n = int(b)
        for m in (n - 1, n + 1):
            q2 = pos_by_base.get(str(m))
            if q2 and dm(p, q2) <= NEIGH_M:
                neigh_ok.add(b)
                break
    conf_changes: list[tuple] = []
    for r in out_rows:
        if r["series"] == "BI":
            continue
        if r["lat"] is None:
            new = None
        else:
            area_tight = (r["ratio"] is not None and not r["areaSuspect"]
                          and abs(r["ratio"] / HIST_QK_M2 - 1) <= AREA_BAND)
            nb = r["base"] in neigh_ok
            new = ("STRONG" if (area_tight and nb)
                   else "MEDIUM" if (area_tight or nb) else "WEAK")
        if new != r["conf"]:
            conf_changes.append((r["page"], r["base"], r["conf"], new))
            r["conf"] = new
    conf_changes = [c for c in conf_changes if c[2] is not None]

    # ——— I6/I7: nespremenjene vrstice bajtno == v4 (identiteta po _srcIdx) ———
    rekey_idx = {r["_srcIdx"] for r in rekeyed}
    n_unchanged = 0
    n_derived = 0
    for r in out_rows:
        idx = r.pop("_srcIdx", None)
        if idx is None:
            fail(f"I6 vrstica p{r['page']} {r['base']} brez _srcIdx")
            continue
        old = v4_rows[idx]
        if idx in rekey_idx:
            continue  # p93 rekey (base + group derived polja) — I7 pokriva
        if r["ambiguous"] != old["ambiguous"] or r["conf"] != old["conf"]:
            n_derived += 1
            continue
        if json.dumps(r, ensure_ascii=False, sort_keys=True) != \
                json.dumps(old, ensure_ascii=False, sort_keys=True):
            fail(f"I6 vrstica p{r['page']} {r['base']} nespremenjena, "
                 f"a odmika")
        n_unchanged += 1
    ok(f"I6 nespremenjene vrstice bajtno == v4 ({n_unchanged}); "
       f"group-derived {n_derived}; izpad C1 {len(excluded_rows)} + "
       f"C2 {len(removed_c2)}; p93 rekey {len(rekeyed)}")
    # I7: p93 kept vrstice — group_pos konsistentnost
    bad_gp = 0
    for r in kept_c2:
        gp = group_pos(r["base"])
        if not gp or r["lat"] != gp[0] or r["lng"] != gp[1] \
                or r["areaModern"] != gp[2]:
            bad_gp += 1
    if bad_gp:
        fail(f"I7 p93 group_pos odmiki: {bad_gp}")
    else:
        ok(f"I7 p93 obdržane vrstice: lat/lng/areaModern == group_pos "
           f"({len(kept_c2)}/3, P55 metoda)")

    # ——— I5: meritve v5 ———
    bases5 = set(pages_by)
    multi = [b for b in pages_by if len(pages_by[b]) > 1]
    bl_by: dict[str, set[str]] = defaultdict(set)
    for r in out_rows:
        bl = blatt_of(r["page"])
        if bl:
            bl_by[r["base"]].add(bl)
    cross = [b for b in bl_by if len(bl_by[b]) > 1]
    s1s2 = [r for r in out_rows if r["series"] != "BI"]
    bi_rows = [r for r in out_rows if r["series"] == "BI"]
    conf_counts: dict[str, int] = defaultdict(int)
    for r in out_rows:
        conf_counts[r["conf"]] += 1
    series_counts = {k: sum(1 for r in out_rows if r["series"] == k)
                     for k in ("S1", "S2", "BI")}
    amb_rows = sum(1 for r in out_rows if r["ambiguous"])
    suffix_groups = sum(1 for b in pos_by_base if len(bybase[b]) > 1)
    area_pairs = [(r["areaQK"], r["areaModern"]) for r in out_rows
                  if r["areaQK"] and r["areaModern"] and not r["areaSuspect"]]
    ratios = [m / a for a, m in area_pairs]
    area_median = statistics.median(ratios)
    tight_n = sum(1 for x in ratios if abs(x / HIST_QK_M2 - 1) <= AREA_BAND)
    mods = [m for _, m in area_pairs]
    rng = random.Random(SEED_AREA)
    rng.shuffle(mods)
    sh_ratios = [m / a for (a, _), m in zip(area_pairs, mods)]
    sh_median = statistics.median(sh_ratios)
    sh_tight = sum(1 for x in sh_ratios
                   if abs(x / HIST_QK_M2 - 1) <= AREA_BAND) / len(sh_ratios)
    area_proof = {
        "pairsWithArea": len(area_pairs),
        "medianRatio": round(area_median, 4),
        "q25": round(sorted(ratios)[len(ratios) // 4], 4),
        "q75": round(sorted(ratios)[3 * len(ratios) // 4], 4),
        "tightN": tight_n,
        "tightShare": round(tight_n / len(ratios), 4),
        "shuffleMedian": round(sh_median, 4),
        "shuffleTightShare": round(sh_tight, 4),
        "historicalQkM2": HIST_QK_M2,
        "deltaPct": round((area_median / HIST_QK_M2 - 1) * 100, 2),
    }
    nums = sorted(int(b) for b in pos_by_base)
    consec = [dm(pos_by_base[str(n)], pos_by_base[str(n + 1)])
              for n in nums if str(n + 1) in pos_by_base]
    consec_s = sorted(consec)
    pl = [pos_by_base[str(n)] for n in nums]
    rng2 = random.Random(SEED_SPATIAL)
    rng2.shuffle(pl)
    sh_d = [dm(pl[i], pl[i + 1]) for i in range(len(pl) - 1)]
    spatial_proof = {
        "consecPairs": len(consec),
        "medianM": round(statistics.median(consec), 1),
        "q25M": round(consec_s[len(consec) // 4], 1),
        "q75M": round(consec_s[3 * len(consec) // 4], 1),
        "share150": round(sum(1 for x in consec if x <= NEIGH_M)
                          / len(consec), 4),
        "shuffleMedianM": round(statistics.median(sh_d), 1),
        "shuffleShare150": round(sum(1 for x in sh_d if x <= NEIGH_M)
                                 / len(sh_d), 4),
        "enrichmentX": round(statistics.median(sh_d)
                             / statistics.median(consec), 1),
    }
    ok(f"I5 meritve v5: rows {len(out_rows)} · bases {len(bases5)} · "
       f"multi {len(multi)} · cross {len(cross)} · ambRows {amb_rows} · "
       f"conf {conf_counts.get('STRONG', 0)}/{conf_counts.get('MEDIUM', 0)}"
       f"/{conf_counts.get('WEAK', 0)} · area median "
       f"{area_proof['medianRatio']} (Δ {area_proof['deltaPct']} %) · "
       f"sosledje {spatial_proof['consecPairs']} parov / "
       f"{spatial_proof['medianM']} m")

    removed_all = excluded_rows + removed_c2
    if EXP["rows"] is not None:
        checks = [
            (len(out_rows), EXP["rows"], "rows"),
            (len(bases5), EXP["bases"], "bases"),
            (len(multi), EXP["multi"], "multi"),
            (len(cross), EXP["cross"], "cross"),
            (amb_rows, EXP["ambRows"], "ambRows"),
            (len(removed_all), EXP["removed"], "removed"),
            (len(excluded_rows), EXP["removedC1"], "removedC1"),
            (len(removed_c2), EXP["removedC2"], "removedC2"),
            (len(rekeyed), EXP["rekeyC2"], "rekeyC2"),
            (suffix_groups, EXP["suffix"], "suffix"),
            (len(pos_by_base), EXP["pos"], "pos"),
            (len(amb_changes), EXP["ambDerived"], "ambDerived"),
            (len(conf_changes), EXP["confDerived"], "confDerived"),
        ]
        for got, want, label in checks:
            if got != want:
                fail(f"I5 {label} {got} ≠ {want}")
        if dict(conf_counts) != EXP["conf"]:
            fail(f"I5 conf {dict(conf_counts)} ≠ {EXP['conf']}")
        if series_counts != EXP["series"]:
            fail(f"I5 series {series_counts} ≠ {EXP['series']}")
        if area_proof != EXP["area"]:
            fail(f"I5 areaProof {area_proof} ≠ pin")
        if spatial_proof != EXP["spatial"]:
            fail(f"I5 spatialProof {spatial_proof} ≠ pin")
        if not FAILURES:
            ok("I5 meritve == pini (vse)")
    else:
        print("  ── PINE ZA VPIS (EXP) ————————————————————")
        print(f"    rows={len(out_rows)}, bases={len(bases5)}, "
              f"multi={len(multi)}, cross={len(cross)}, "
              f"ambRows={amb_rows}, suffix={suffix_groups}, "
              f"pos={len(pos_by_base)}, removed={len(removed_all)}, "
              f"ambDerived={len(amb_changes)}, "
              f"confDerived={len(conf_changes)}")
        print(f"    conf={dict(conf_counts)}, series={series_counts}")
        print(f"    area={area_proof}")
        print(f"    spatial={spatial_proof}")
        from collections import Counter as _C
        print(f"    removedByPage={dict(sorted(_C(x['page'] for x in removed_all).items()))}")

    # blattDist (pari Blattov čez cross-Blatt base)
    blatt_dist: dict[str, int] = defaultdict(int)
    for b in cross:
        pair = "·".join(sorted(bl_by[b]))
        blatt_dist[pair] += 1

    v4_join = v4ev["join"]
    join_block = {
        "matchedRows": len(out_rows),
        "matchedRowsS1S2": len(s1s2),
        "matchedRowsBI": len(bi_rows),
        "matchedSharePct": round(100 * len(out_rows) / TOTAL_PS_ROWS, 1),
        "psUniqueNumbers": v4_join["psUniqueNumbers"],
        "psPositionedParcels": len(pos_by_base),
        "suffixGroups": suffix_groups,
        "seriesCounts": series_counts,
        "confCounts": {"STRONG": conf_counts["STRONG"],
                       "MEDIUM": conf_counts["MEDIUM"],
                       "WEAK": conf_counts["WEAK"]},
        "readConfBI": v4_join["readConfBI"],
        "ambiguousBases": len(multi),
        "ambiguousRows": amb_rows,
    }
    per_blatt_amb = {
        "basesOnMultiplePages": len(multi),
        "rowsWithAmbiguousBase": amb_rows,
        "note": f"base na > 1 strani v v5 (po C1 sekcije exclude + C2 p93 "
                f"reverzija); čez-Blatt {len(cross)} (blattDist " +
                " · ".join(f"{k} {v}" for k, v in sorted(blatt_dist.items()))
                + ") [~]",
    }
    return (out_rows, excluded_rows, removed_c2, rekeyed, kept_c2, ann93,
            amb_changes, conf_changes, join_block, per_blatt_amb,
            area_proof, spatial_proof, page_sel_or(v4ev),
            v4ev["furkovce"], multi, cross, bases5, blatt_dist,
            n_forensics)


def page_sel_or(v4ev):
    return v4ev.get("pageSelection")


def build_documents():
    if FAILURES:
        pass  # compute_pair sam dvigne SystemExit ob padu invariant
    try:
        evidence, runtime = compute_pair()
    except SystemExit as e:
        print(f"P71: {e}")
        return 1
    V5_EV.write_text(jdump_pretty(evidence), encoding="utf-8")
    OUT_RUNTIME.write_text(jdump_pretty(runtime), encoding="utf-8")
    print(f"P71: dokaz → {V5_EV.relative_to(REPO)}; runtime → "
          f"{OUT_RUNTIME.relative_to(REPO)} (v5)")
    return 0


def jdump_pretty(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def check():
    """I9: drugi preizračun bajtno identičen zapisanima dokumentoma."""
    ev1 = json.loads(V5_EV.read_text(encoding="utf-8"))
    ev1s = json.dumps(ev1, ensure_ascii=False, sort_keys=True)
    ev2, rt2 = compute_pair()
    if json.dumps(ev2, ensure_ascii=False, sort_keys=True) != ev1s:
        print("  ✗ I9 dokaz: drugi preizračun ≠ zapisano")
        return 1
    rt_disk = json.loads(OUT_RUNTIME.read_text(encoding="utf-8"))
    if rt_disk.get("version") == 5:
        if json.dumps(rt2, ensure_ascii=False, sort_keys=True) != \
                json.dumps(rt_disk, ensure_ascii=False, sort_keys=True):
            print("  ✗ I9 runtime: drugi preizračun ≠ zapisano")
            return 1
        print("  ✓ I9 determinizem: drugi preizračun bajtno == zapisano "
              "(dokaz + runtime)")
    else:
        # runtime je napredoval (P73 v6) — dokaz ostaje zamrznjen arhiv
        # (vsebina v5 runtime živi v dokazu); disk runtime mora deklarirati
        # nasledstvo (version ≥ 6 + v6Delta z dokumentirano korekcijo C3)
        d6 = rt_disk.get("v6Delta") or {}
        if not (rt_disk.get("version", 0) >= 6
                and d6.get("droppedPairs") == 137
                and d6.get("droppedRows") == 138):
            print("  ✗ I9 runtime nasledstvo ni deklarirano (version "
                  f"{rt_disk.get('version')}, v6Delta {bool(d6)})")
            return 1
        print("  ✓ I9 determinizem: dokaz bajtno; runtime nadgrajen na v"
              + str(rt_disk.get("version")) + " po P73 (C3 isti-Blatt "
              "SPLIT opcija A) — v5 arhiviran v dokazu")
    if FAILURES:
        print(f"P71 --check: {len(FAILURES)} invariant(ov) PADLO")
        for f in FAILURES:
            print(f"  → {f}")
        return 1
    print("P71 --check: VSE INVARIANTE PASS (bajtno)")
    return 0


def compute_pair():
    """Ponovni preizračun (brez pisanja) — vrne (evidence, runtime)."""
    global FAILURES
    FAILURES = []
    p69 = json.loads(P69_EV.read_text(encoding="utf-8"))
    p56 = json.loads(P56_EV.read_text(encoding="utf-8"))
    (out_rows, excluded_rows, removed_c2, rekeyed, kept_c2, ann93,
     amb_changes, conf_changes, join_block, per_blatt_amb, area_proof,
     spatial_proof, page_sel, furkovce, multi, cross, bases5, blatt_dist,
     n_forensics) = compute()
    if FAILURES:
        raise SystemExit(f"P71 compute: invariant padel: {FAILURES[:3]}")
    v4ev = json.loads(V4_EV.read_text(encoding="utf-8"))
    removed_all = excluded_rows + removed_c2
    evidence = {
        "version": 5,
        "task": "P71 (issue #13) — PS-PARCELS-GEO v5: sekijske vrstice "
                "exclude (C1) + p93 reverzija (C2)",
        "date": DATE,
        "generatedBy": "scripts/p71_ps_v5_sections_p93.py",
        "principle": "samo odstranjevanje dokumentiranih lažnih zahtevkov; "
                     "noben nov podatek; glifna forenzika z notranjo "
                     "kontrolo (isti pisar, ista stran) je prenosljiva "
                     "neodvisno od rokopisa",
        "inputs": {
            "v4ProofSha256": sha256(V4_EV),
            "p69ProofSha256": sha256(P69_EV),
            "p59ProofSha256": sha256(P59_EV),
            "p56ProofSha256": sha256(P56_EV),
            "parcelsSha256": sha256(PARCELS),
        },
        "corrections": {
            "C1": {
                "title": "exclude 56 sekijskih vrstic (p83–86, p88)",
                "decision": "LASTNIK (P71): opcija 'exclude' iz P69 "
                            "sectionClass.options; per-Blatt instance "
                            "(P60 moda B / PF protokol) = kasnejša "
                            "odločitev",
                "evidence": {
                    "ratios": p69["sectionClass"]["ratios"],
                    "ownerOverlapP83P84vsP11":
                        p69["sectionClass"]["evidence"]["p83_p84_vs_p11"]
                        ["ownerOverlap"],
                    "housesP85vsP35":
                        p69["sectionClass"]["evidence"]["p85_vs_p35_houses"]
                        ["verdict"],
                },
                "excludedRows": excluded_rows,
            },
            "C2": {
                "title": "p93 reverzija: P68 renum 160x→190x (+300) = "
                         "NAPAKA; stran bere 1601–1620",
                "evidence": {
                    "glyphForensics": {
                        "method": "notranja kontrola na isti strani "
                                  "(10–12× zoom, P67 recept): gotova "
                                  "zadnja 9 (zaprt zgornji lok + rep pod "
                                  "osnovnico) vidno različna od srednje "
                                  "števke (spodnja zanka, odprt vrh = 6)",
                        "rows": ["r5 = 1605", "r9 = 1609 (kontrola: "
                                 "zadnja 9 ≠ srednja 6)", "r16 = 1616",
                                 "r19 = 1619 (kontrola)", "r20 = 1620"],
                        "controls": ["p98 '1916' @12×: 9 in 6 v istem "
                                     "številu = dve različni črki",
                                     "p92 981–983 (P69-verificirane 9): "
                                     "isti glif kot p98-ova 9"],
                        "files": sorted(f.name for f in
                                        FORENSICS.glob("*.png")),
                        "nFiles": n_forensics,
                    },
                    "annRecords": ann93,
                    "annRecordsNote": "sodobni anotator referencira "
                                      "1601–1619 (Durch Theilung im 1824, "
                                      "trifft Gültley 9., 1870. 8-1117)",
                    "pageMap": p56["pageMap"][92],
                    "p38pass2": "research/issue17/ps-raw/ps-093-pass2.json "
                                "= 1601–1620",
                    "p67ClaimRefuted": "'9→6/9→0 — P67 že dokazal' za p93 "
                                       "= napačno prenesena trditev: p93 "
                                       "NI bil v P67 očesni coni "
                                       "(p74–92, p99); artefakt realen na "
                                       "drugih straneh, ne na p93",
                },
                "revertedRows": len(rekeyed),
                "keptRows": [{"base": r["base"], "owner": r["owner"],
                              "areaQK": r["areaQK"],
                              "areaModern": r["areaModern"]}
                             for r in kept_c2],
                "pfMatchSet": sorted(x["base"] for x in kept_c2),
                "removedRows": removed_c2,
            },
        },
        "removedRows": removed_all,
        "join": join_block,
        "v5Delta": {
            "reason": "C1: exclude 56 sekijskih vrstic (P70 odprta točka ①, "
                      "lastniška odločitev) + C2: p93 reverzija P68 renum "
                      "+300 (glifna forenzika + annRecords; P67 "
                      "artefakt-trditev za p93 ovržena)",
            "excludedSections": len(excluded_rows),
            "revertedP93": len(rekeyed),
            "removed": len(removed_all),
            "before": {"rows": 1145, "bases": 878, "multiPage": 215,
                       "crossBlatt": 79},
            "after": {"rows": len(out_rows), "bases": len(bases5),
                      "multiPage": per_blatt_amb["basesOnMultiplePages"],
                      "crossBlatt": len(cross)},
            "invariance": "nespremenjene vrstice bajtno == v4 (lekcija P9); "
                          "group-derived polja (ambiguous/conf) "
                          "prekalkulirana po P55 metodi; v4 ostaje "
                          "arhiviran (research/issue17/ps-parcels-geo-v4"
                          ".json)",
            "note": "C1 in C2 odstranjujeta LE lažne zahtevke — noben nov "
                    "podatek ni izmišljen; PF 1603/1604/1605 dobita prve "
                    "prave vrstice (prej prazni!), PF 1904/1906 izpadeta "
                    "iz base seta (dokumentirana praznina)",
        },
        "areaProof": area_proof,
        "spatialProof": spatial_proof,
        "furkovce": furkovce,
        "perBlattAmbiguity": per_blatt_amb,
        "invariants": {
            "I1": "C1 set == P69 sectionClass (bajtno); 56; vse v4 vrstice "
                  "strani 83–86/88 == set",
            "I2": "pini v4/P69/P59/P56/PARCELS sha256; runtime == dokaz",
            "I3": "p93 15× offset +300 pred reverzijo; base := parzella "
                  "15/15; PF ujemanja == {1603, 1604, 1605}; 12 izpadlih; "
                  "annRecords 160x/161x",
            "I4": "po C1 noben base ne izgubi vseh vrstic (0 praznih)",
            "I5": "meritve == pini",
            "I6": "nespremenjene vrstice bajtno == v4",
            "I7": "p93 kept: group_pos konsistentno",
            "I8": "dokaz ⊇ runtime bajtno",
            "I9": "determinizem --check bajtno",
        },
        "statusLine": _status_line(out_rows, excluded_rows, removed_c2,
                                   rekeyed, join_block, per_blatt_amb,
                                   cross, area_proof, spatial_proof),
        "verdictSi": _verdict_si(out_rows, join_block),
        "verdictEn": _verdict_en(out_rows, join_block),
        "next": _next_list(),
        "rowsEvidence": out_rows,
    }
    runtime = {
        "version": 5,
        "task": "P71 (issue #13) — sekijske vrstice exclude (C1) + p93 "
                "reverzija (C2)",
        "date": DATE,
        "generatedBy": "scripts/p71_ps_v5_sections_p93.py",
        "historicalConstant": v4ev.get("historicalConstant"),
        "pageSelection": page_sel,
        "join": join_block,
        "v5Delta": evidence["v5Delta"],
        "areaProof": area_proof,
        "spatialProof": spatial_proof,
        "furkovce": furkovce,
        "perBlattAmbiguity": per_blatt_amb,
        "statusLine": evidence["statusLine"],
        "rows": out_rows,
    }
    return evidence, runtime


def _status_line(out_rows, excluded_rows, removed_c2, rekeyed, join_block,
                 per_blatt_amb, cross, area_proof, spatial_proof) -> str:
    return (
        f"P71 KOREKCIJE v4: C1 sekcije exclude — 56 vrstic (p83–86, p88; "
        f"P69 dokazane lažne fuzije na Blatt I; lastniška odločitev: "
        f"exclude iz joina, vrstice ostanejo v registru brez geometrije; "
        f"0 poligonov ostane praznih) + C2 p93 reverzija — P68 renum "
        f"+300 NAPAKA (prva očesna forenzika p93: notranja glifna kontrola "
        f"1609/1619 — 6 ≠ 9; annRecords anotatorja 1601–1619; pageMap; "
        f"pass2): 15 vrstic base := parzella, PF ujemanja 1603/1604/1605, "
        f"12 izpadlih (brez PF poligona), PF 1901–1920 brez lažnih dvojnih "
        f"zahtevkov (ostane p98 III); v5: {len(out_rows)} vrstic / "
        f"{join_block['psPositionedParcels']} base / multi-page "
        f"{per_blatt_amb['basesOnMultiplePages']} / cross-Blatt "
        f"{len(cross)}; area median {area_proof['medianRatio']} "
        f"(Δ {area_proof['deltaPct']} %), sosledje "
        f"{spatial_proof['consecPairs']} parov / {spatial_proof['medianM']} m "
        f"({spatial_proof['enrichmentX']}×); odprte praznine: PF 1644–1655, "
        f"1673/1679, 1842–1860, 1904/1906 brez registrskih strani "
        f"(modernVoid [~])"
    )


def _verdict_si(out_rows, join_block) -> str:
    return (
        "Dve korekciji v4 na podlagi nove očesne forenzike: (C1) 56 "
        "sekijskih vrstic p83–86/p88 izpadlo iz joina — dokazane lažne "
        "fuzije na Blatt I poligone (lastniška odločitev P71, opcija "
        "exclude; per-Blatt instance ostaja odprta lastniška točka). "
        "(C2) P68 renum p93 160x→190x ovržen: notranja glifna kontrola "
        "na p93 (1609/1619: 6 ≠ 9 pri istem pisarju), annRecords "
        "anotatorja (1601–1619), pageMap in pass2 soglasno dokazujejo "
        "1601–1620 — 15 vrstic reverziranih na originalno branje, 3 "
        "ostanejo povezane (PF 1603/1604/1605 — prej prazni poligoni "
        "dobili prve vrstice), 12 izpadlih; PF 1901–1920 brez lažnih "
        "dvojnih zahtevkov p93 (ostane p98 III). V5: "
        f"{len(out_rows)} vrstic ({round(100 * len(out_rows) / 2762, 1)} "
        f"% izbire) / {join_block['psPositionedParcels']} base."
    )


def _verdict_en(out_rows, join_block) -> str:
    return (
        "Two corrections to v4 based on new ocular forensics: (C1) 56 "
        "section rows p83–86/p88 excluded from the join — proven false "
        "fusions onto Blatt I polygons (owner decision P71, exclude "
        "option; per-Blatt instances remain an open owner question). "
        "(C2) The P68 renum p93 160x→190x refuted: within-page glyph "
        "control (1609/1619: 6 ≠ 9 by the same scribe), the contemporary "
        "annotator's annRecords (1601–1619), the pageMap and pass2 all "
        "prove 1601–1620 — 15 rows reverted to the original reading, 3 "
        "stay matched (PF 1603/1604/1605 — previously empty polygons got "
        "their first rows), 12 dropped; PF 1901–1920 free of p93's false "
        "double claims (p98 III remains). V5: "
        f"{len(out_rows)} rows ({round(100 * len(out_rows) / 2762, 1)} "
        f"% of the selection) / {join_block['psPositionedParcels']} bases."
    )


def _next_list() -> list:
    return [
        "LASTNIŠKO: ① per-Blatt instance sekcij (P60 moda B / PF "
        "protokol) — 56 vrstic čaka identiteto sekcij",
        "LASTNIŠKO: ② SPLIT joina (33 fuzij isti-Blatt 921–1000: "
        "p49–52 × p89–92; + cross-Blatt)",
        "praznine brez registrskih strani: PF 1644–1655, 1673/1679, "
        "1842–1860, 1904/1906 (modernVoid [~] — možnost: Abschreibung "
        "ali prelom številčenja; brez trditve o vzroku)",
        "P56 modernVoid 2507–2607 (87 dodatkov S2 brez sodobnih parcel) "
        "— nespremenjeno",
    ]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "--check":
        sys.exit(check())
    sys.exit(build_documents())


if __name__ == "__main__":
    main()
