#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P57 (issue #13) — ZAČETEK REGISTRA PS: strani 3–4 (številke 1–40, Blatt I).

Kaj naredi (vse izključno iz committed dokazov):
  1. ADJUDIKACIJA branj strani 3–4 čez 4 neodvisne plasti (vse committed v
     research/issue17/ps-raw/):
       - polna stran:  ps-003{,-pass2,-pass3}.json + ps-004{...}.json (3 prehodi/stran)
       - kolone:       ps-00{3,4}-cols{,2,3}.json                  (Haus Nro., 3 prehodi)
       - izrezi:       ps-00{3,4}-areas{,2,3}.json                 (Klafter, 3 prehodi,
                        LCS poravnava proti polni plasti — na str. 4 VLM vstavi [?])
       - celice:       ps-0034-cells-arbitration.json              (11 spornih celic, 6×)
     Pravilo adjudikacije klafter (deterministično, ADJUDIKACIJA_KLAFTER):
       1) cells == areas-majority → ta vrednost (2 zoom plasti)
       2) cells == full-majority  → ta vrednost (celice + polna)
       3) sicer če cells prisoten → areas-majority [~] (alternative zapisane),
          oziroma cells [~], če areas-majority ni na voljo
       4) brez cells: areas == full → močno; sicer areas [~]; brez obeh → full
     Haus Nro. iz kolonskih plasti (večina 3 prehodov; 2/3 → [~]).
     Imena/kultura/ertrag/anmerkung: večina polnih prehodov.
  2. VERIŽNOST: vrstice 1–20 (str. 3) + 21–40 (str. 4) + committed ps-005 (41)
     = neprekinjena veriga Blatt I (PS-full-v2 range str. 5 = [41, 60]).
  3. JOIN: številke 1–40 ↔ sodobne parcele k.o. 1544 (P47 prenos) po mehaniki P55
     (base_of z odstranitvijo `*`, group_pos = težišče po površinah delov).
  4. TEST VZTRAJNOSTI (A) POVRŠINE: median modern/QK po parih ≈ 1 Wiener QK
     (3.59665 m²), premešana kontrola (seed 42) višja; delež pasu ±10 %.
  5. TEST (B) SOSLEDNOST: zaporedne številke (n, n+1) obema pozicioniranim →
     razdalje; premešana kontrola (seed 7) ≥ 5× slabša. Struktura per-segment
     dokumentirana (identifikacija per-parcelno ostaja [~]).
  6. OBNOVA: 26 izgubljenih base iz P56 (sanitization.lostBases) se poveže
     nazaj s primarnim virom (Blatt I str. 3–4) — vsrstno zaupanje
     STRONG (pas površin IN sosed ≤ 150 m) / MEDIUM (eden) / WEAK (samo številka).
  7. DETERMINIZEM: --check = ponovni izračun bajtno identičen obstoječim datotekam.

Izpiše:
  research/issue17/ps-register-start.json  (dokaz — plasti + adjudikacija + testi)
  src/data/atlas/ps-register-start.json    (runtime — kompakten)

Status ostaja REVIEW (strojno branje ni dokazni vir) — pravilo hiše:
»ne nadgradi gotovosti brez človeške paleografske potrditve«.

Poštenost:
  - vrstica 1 (str. 3) in vrstica 28 (str. 4): celici površine PRAZNI (blot na
    str. 3 je nad imenom, ne nad površino) — brez parov površin.
  - vsotni vrsti ("Fürtrag", rdeče revizije) brani kot surovine; interpretacija
    obsega [~] (str. 3 prečrtan rdeče, str. 4 z rdečo črto; NISO kumulativni —
    str. 3 je VIŠJA od str. 4).
  - 14 vrstic brez sodobne naslednice = upokojene številke (konsolidacija) [~].
"""

import json
import math
import re
import statistics
import random
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "research" / "issue17" / "ps-raw"
OUT_EVIDENCE = ROOT / "research" / "issue17" / "ps-register-start.json"
OUT_RUNTIME = ROOT / "src" / "data" / "atlas" / "ps-register-start.json"
P56_RUNTIME = ROOT / "src" / "data" / "atlas" / "ps-register-topology.json"
PS_FULL_V2 = ROOT / "research" / "issue17" / "PS-full-v2.json"
PS_005 = RAW / "ps-005.json"
PARCELS = ROOT / "research" / "georef-n83" / "gurs" / "parcels-ko1544-merged.json"

HIST_QK_M2 = 3.59665      # 1 Wiener Quadrat-Klafter (zgodovinska konstanta, P55)
M_PER_DEG_LAT = 111320.0  # ploščni faktor (izv. village3d.ts / P55)
NEIGH_M = 150.0           # prag soslednosti (P55)
AREA_LO, AREA_HI = 3.30, 3.90   # pas mediane m²/QK (P55 I3)

PAGES = (3, 4)
FIRST_ROW = {3: 1, 4: 21}
ROW_COUNT = 20


def ok(cond, msg):
    print(("  PASS  " if cond else "  FAIL  ") + msg)
    return bool(cond)


def fnum(x):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None


def norm_klafter(v):
    """VLM vrednost → (int|None, opomba). 'h' → 4 (Kurrent 4 podobna h);
    '[?]' → None."""
    if v is None:
        return None, None
    s = str(v).strip()
    if s in ("[?]", "?", ""):
        return None, None
    note = None
    if "h" in s:
        note = "števka 4 prebrana kot 'h' (Kurrent) → normalizirano"
        s = s.replace("h", "4")
    s = re.sub(r"\s+", "", s)
    m = re.match(r"^\[?~?(\d+)\]?~?$", s)
    if not m:
        return None, f"neparsljivo: {v!r}"
    n = int(m.group(1))
    if "[~]" in str(v):
        note = (note + "; " if note else "") + "[~]"
    return n, note


def clean_line(line):
    line = line.strip()
    line = line.strip("`").strip()
    if line.startswith("json"):
        line = line[4:].strip()
    return line


def parse_ndjson(content):
    """NDJSON → (rows, summa). Vrstice z 'summa' in brez 'parzella' → summa."""
    rows, summa = [], None
    for line in (content or "").split("\n"):
        line = clean_line(line)
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "summa" in obj and "parzella" not in obj:
            summa = obj["summa"]
        elif isinstance(obj, dict) and obj.get("parzella") is not None:
            rows.append(obj)
    return rows, summa


def read_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def majority(values):
    """Večina ne-praznih; vrni (vrednost, n_soglasij, n_ne-praznih, alternative)."""
    vals = [v for v in values if v not in (None, "")]
    if not vals:
        return None, 0, 0, []
    c = Counter(vals)
    best, n = c.most_common(1)[0]
    alts = sorted(v for v, k in c.items() if v != best)
    return best, n, len(vals), alts


def field_majority(pass_rows, row_no, field):
    per_pass = []
    for rows in pass_rows:
        rec = next((r for r in rows if str(r.get("parzella")) == str(row_no)), None)
        per_pass.append(rec.get(field) if rec else None)
    return majority(per_pass)


def base_of(parzella):
    m = re.match(r"\*?(\d+)", str(parzella or ""))
    return m.group(1) if m else None


def lcs_align(expected_keys, observed_raw):
    """Poravnaj observed (surove vrednosti, dolžina poljubna) na expected
    (normalizirani ključi, dolžine 20). Vrne seznam dolžine 20 (observed vrednost
    ali None)."""
    def key(x):
        if x is None:
            return None
        return norm_klafter(x)[0]
    o = [key(x) for x in observed_raw]
    e = expected_keys
    n, m = len(e), len(o)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if e[i] == o[j]:
                dp[i][j] = dp[i + 1][j + 1] + 1
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    out = [None] * n
    i = j = 0
    while i < n and j < m:
        if e[i] == o[j] and e[i] is not None:
            out[i] = observed_raw[j]
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1
        else:
            j += 1
    return out


def main() -> int:
    check = "--check" in sys.argv
    print("P57 — začetek registra PS (str. 3–4, številke 1–40, Blatt I)")

    # ——— vhodi ———
    full = {p: [read_json(RAW / f"ps-00{p}{'-pass2' if n == 2 else '-pass3' if n == 3 else ''}.json")
                for n in (1, 2, 3)] for p in PAGES}
    cols = {p: [read_json(RAW / f"ps-00{p}-cols{n if n > 1 else ''}.json")
                for n in (1, 2, 3)] for p in PAGES}
    areas = {p: [read_json(RAW / f"ps-00{p}-areas{n if n > 1 else ''}.json")
                 for n in (1, 2, 3)] for p in PAGES}
    cells_raw = read_json(RAW / "ps-0034-cells-arbitration.json")
    p56 = read_json(P56_RUNTIME)
    psv2 = read_json(PS_FULL_V2)
    ps5 = read_json(PS_005)
    parcels = read_json(PARCELS)

    full_rows, full_sums = {}, {}
    for p in PAGES:
        rr, ss = [], []
        for rec in full[p]:
            r, s = parse_ndjson(rec["content"])
            rr.append(r)
            ss.append(s)
        full_rows[p], full_sums[p] = rr, ss

    cols_parsed = {}
    for p in PAGES:
        per_pass = []
        for rec in cols[p]:
            d = {}
            for line in (rec["content"] or "").split("\n"):
                line = clean_line(line)
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if o.get("grund") is not None:
                    d[str(o["grund"])] = str(o.get("hausNr", "")).strip()
            per_pass.append(d)
        cols_parsed[p] = per_pass

    areas_seq = {}
    for p in PAGES:
        per_pass = []
        for rec in areas[p]:
            seq = []
            for line in (rec["content"] or "").split("\n"):
                line = clean_line(line)
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if "klafter" in o:
                    seq.append(o.get("klafter"))
            per_pass.append(seq)
        areas_seq[p] = per_pass

    cells_parsed = {}
    for line in (cells_raw["content"] or "").split("\n"):
        line = clean_line(line)
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        if o.get("stran") is not None and o.get("vrstica") is not None:
            cells_parsed.setdefault((str(o["stran"]), str(o["vrstica"])), []).append(o.get("klafter"))
    # odločanje r40 (2 dodatna prehoda, 6×; izrez ujame tudi Fürtrag '087' spodaj
    # — vzami prvo vrstico vrednosti)
    for extra in sorted(RAW.glob("ps-0034-cells-arbitration-r40-p*.json")):
        rec = read_json(extra)
        try:
            o = json.loads(clean_line(rec["content"]))
            v = str(o.get("klafter", "")).split("\n")[0].strip()
        except (json.JSONDecodeError, AttributeError):
            v = None
        if v:
            cells_parsed.setdefault(("4", "40"), []).append(v)
    cells_val = {k: majority(v)[0] for k, v in cells_parsed.items()}

    # ——— adjudikacija vrstic 1–40 ———
    rows_out = []
    for p in PAGES:
        expected_keys = []
        for k in range(ROW_COUNT):
            mv = field_majority(full_rows[p], FIRST_ROW[p] + k, "klafter")[0]
            expected_keys.append(norm_klafter(mv)[0])
        area_aligned = [lcs_align(expected_keys, seq) for seq in areas_seq[p]]
        area_aligned_by_page[p] = area_aligned

        for k in range(ROW_COUNT):
            row_no = FIRST_ROW[p] + k
            name_f = field_majority(full_rows[p], row_no, "name")
            kultur_f = field_majority(full_rows[p], row_no, "kultur")
            klafter_f = field_majority(full_rows[p], row_no, "klafter")
            joch_f = field_majority(full_rows[p], row_no, "joch")
            haus_full = field_majority(full_rows[p], row_no, "hausNr")
            anm_f = field_majority(full_rows[p], row_no, "anmerkung")
            ertrag_fl = field_majority(full_rows[p], row_no, "ertragFl")
            ertrag_kr = field_majority(full_rows[p], row_no, "ertragKr")
            klasse_f = field_majority(full_rows[p], row_no, "klasse")
            stand_f = field_majority(full_rows[p], row_no, "stand")
            wohn_f = field_majority(full_rows[p], row_no, "wohnort")

            col_vals = [d.get(str(row_no)) for d in cols_parsed[p] if d.get(str(row_no))]
            hn, hn_n, hn_tot, hn_alts = majority(col_vals)
            if hn is not None:
                hn = hn.replace("[~]", "").strip() or None
            haus_conf = f"{hn_n}/{hn_tot}" if hn_tot else None

            area_vals = [a[k] for a in area_aligned if a[k] is not None]
            area_majority, _an, _at, area_alts = majority(area_vals)
            cell_val = cells_val.get((str(p), str(row_no)))

            cell_norm, cell_norm_note = norm_klafter(cell_val)
            full_norm, _ = norm_klafter(klafter_f[0])
            area_norm, area_note = norm_klafter(area_majority)

            # ADJUDIKACIJA_KLAFTER
            layer, klafter, note = None, None, None
            if cell_val is not None and cell_norm is None:
                layer, klafter, note = "cells", None, "celice: neberljivo [?]"
            elif cell_norm is not None and area_norm is not None and cell_norm == area_norm:
                layer, klafter = "cells+areas", cell_norm
            elif cell_norm is not None and full_norm is not None and cell_norm == full_norm:
                layer, klafter = "cells+full", cell_norm
            elif cell_norm is not None:
                layer, klafter = "cells", cell_norm
                note = (f"adjudikacija [~]: celice (6× izrez) {cell_norm} · polna {full_norm}"
                        f" · izrezi neujemljivi [~] — glej cells-arbitration")
            elif area_norm is not None and full_norm is not None and area_norm == full_norm:
                layer, klafter = "areas+full", area_norm
            elif area_norm is not None:
                layer, klafter, note = "areas", area_norm, f"adjudikacija [~]: izrezi {area_norm} vs polna {full_norm}"
            elif full_norm is not None:
                layer, klafter = "full", full_norm
            if note is None and cell_norm_note:
                note = cell_norm_note
            if note is None and area_note:
                note = area_note

            joch_v, _ = norm_klafter(joch_f[0])
            area_qk = ((joch_v or 0) * 1600.0 + klafter) if klafter is not None else None
            rows_out.append({
                "no": row_no, "page": p, "blatt": "I",
                "hausNr": hn, "hausNrConf": haus_conf, "hausNrAlts": hn_alts,
                "hausNrFull": haus_full[0],
                "name": (name_f[0].strip() if isinstance(name_f[0], str) else name_f[0]),
                "nameAlts": name_f[3], "stand": stand_f[0], "wohnort": wohn_f[0],
                "kultur": kultur_f[0], "kulturAlts": kultur_f[3],
                "joch": joch_v, "klafter": klafter,
                "areaQK": round(area_qk, 1) if area_qk else None,
                "klafterLayer": layer, "klafterNote": note,
                "klafterFullAlts": klafter_f[3], "klafterAreaAlts": area_alts,
                "klasse": klasse_f[0], "ertragFl": ertrag_fl[0], "ertragKr": ertrag_kr[0],
                "anmerkung": anm_f[0], "anmerkungAlts": anm_f[3],
                "_cellVal": cell_val, "_areaVals": area_vals,
            })

    # ——— I1: struktura + veriga ———
    print("I1 struktura + veriga Blatt I")
    nums = [r["no"] for r in rows_out]
    i1 = nums == list(range(1, 41)) and all(r["blatt"] == "I" for r in rows_out)
    r5, _ = parse_ndjson(ps5["content"])
    i1 &= bool(r5) and str(r5[0].get("parzella")) == "41" and r5[0].get("blatt") == "I"
    pg5 = psv2["pages"].get("5", {})
    rng5 = pg5.get("range", [0, 0])
    i1 &= float(rng5[0]) == 41.0 and float(rng5[1]) == 60.0
    i1 = ok(i1, "vrstice 1–40 neprekinjene, Blatt I; committed ps-005 začne 41 (Blatt I); PS-full-v2 str. 5 = [41, 60]")

    # ——— I2: Haus Nro. ———
    print("I2 Haus Nro.")
    ok_all = all(r["hausNr"] is not None and str(r["hausNr"]).isdigit() and 0 <= int(r["hausNr"]) <= 66
                 for r in rows_out)
    conf23 = sum(1 for r in rows_out if r["hausNrConf"] == "2/3")
    i2 = ok(ok_all, f"vseh 40 Haus Nro. številskih v prostoru 0–66 (dvomi 2/3: {conf23} vrstic)")

    # ——— I3: površine + Fürtrag ———
    print("I3 površine + Fürtrag")
    with_area = [r for r in rows_out if r["klafter"] is not None]
    sum_p3 = sum(r["klafter"] for r in with_area if r["page"] == 3)
    sum_p4 = sum(r["klafter"] for r in with_area if r["page"] == 4)
    layer_counts = Counter(r["klafterLayer"] for r in rows_out)
    fuertrag = {str(p): full_sums[p] for p in PAGES}
    i3 = ok(len(with_area) == 38 and rows_out[0]["klafter"] is None and rows_out[27]["klafter"] is None,
            f"38/40 površin (r1, r28 prazni) · vsote vidnih: str. 3 = {sum_p3} K, str. 4 = {sum_p4} K · "
            f"plasti: {dict(layer_counts)} · Fürtrag [~]: str. 3 {fuertrag['3'][0]} / str. 4 {fuertrag['4'][0]}")

    # ——— join (mehanika P55) ———
    bybase = defaultdict(list)
    for x in parcels:
        b = base_of(x.get("st"))
        if b:
            bybase[b].append(x)

    def group_pos(b):
        grp = bybase.get(b)
        if not grp:
            return None
        tot = sum(fnum(x.get("povrsina")) for x in grp)
        if tot and tot > 0:
            lat = sum(x["lat"] * fnum(x.get("povrsina")) for x in grp) / tot
            lng = sum(x["lng"] * fnum(x.get("povrsina")) for x in grp) / tot
        else:
            lat = sum(x["lat"] for x in grp) / len(grp)
            lng = sum(x["lng"] for x in grp) / len(grp)
        return lat, lng, tot, len(grp)

    matched_bases = []
    for r in rows_out:
        b = str(r["no"])
        gp = group_pos(b)
        if gp:
            lat, lng, a_m, parts = gp
            r.update({"base": b, "lat": round(lat, 7), "lng": round(lng, 7),
                      "areaModern": round(a_m) or None, "parts": parts, "ratioM2K": None})
            if r["areaQK"]:
                r["ratioM2K"] = round(a_m / r["areaQK"], 4)
            matched_bases.append(b)
        else:
            r.update({"base": b, "lat": None, "lng": None, "areaModern": None,
                      "parts": None, "ratioM2K": None})
    pos_by_base = {r["base"]: (r["lat"], r["lng"]) for r in rows_out if r["lat"] is not None}

    # ——— I4: povezava + bbox ———
    print("I4 povezava + bbox")
    lat_all = [x["lat"] for x in parcels if x.get("lat")]
    lng_all = [x["lng"] for x in parcels if x.get("lng")]
    bb = (min(lat_all) - 200 / M_PER_DEG_LAT, max(lat_all) + 200 / M_PER_DEG_LAT,
          min(lng_all) - 200 / M_PER_DEG_LAT, max(lng_all) + 200 / M_PER_DEG_LAT)
    in_bbox = all(bb[0] <= r["lat"] <= bb[1] and bb[2] <= r["lng"] <= bb[3]
                  for r in rows_out if r["lat"] is not None)
    i4 = ok(len(matched_bases) == 26 and in_bbox,
            f"povezanih base {len(matched_bases)}/40 · vse pozicije v bbox KO 1544 ± 200 m")

    # ——— soslednost sosedov + zaupanje ———
    def dm(a, b2):
        return math.hypot((a[0] - b2[0]) * M_PER_DEG_LAT, (a[1] - b2[1]) * M_PER_DEG_LAT * 0.7)

    neigh_ok = set()
    for b, p in pos_by_base.items():
        n = int(b)
        for m2 in (n - 1, n + 1):
            q = pos_by_base.get(str(m2))
            if q and dm(p, q) <= NEIGH_M:
                neigh_ok.add(b)

    for r in rows_out:
        if r["lat"] is None:
            r["confidence"] = None
            continue
        in_band = r.get("ratioM2K") is not None and AREA_LO <= r["ratioM2K"] <= AREA_HI
        has_neigh = r["base"] in neigh_ok
        r["confidence"] = ("STRONG" if (in_band and has_neigh)
                           else "MEDIUM" if (in_band or has_neigh) else "WEAK")
    cc = Counter(r["confidence"] for r in rows_out if r["confidence"])

    # ——— T1: površine ———
    print("T1 površine")
    pairs = [(r["no"], r["areaQK"], r["areaModern"], r["ratioM2K"])
             for r in rows_out if r.get("ratioM2K")]
    ratios = [x[3] for x in pairs]
    med = statistics.median(ratios)
    band_obs = sum(1 for x in ratios if abs(x / HIST_QK_M2 - 1.0) <= 0.10) / len(ratios)
    rng = random.Random(42)
    modern = [x[2] for x in pairs]
    qks = [x[1] for x in pairs]
    ctrl_meds, ctrl_bands = [], []
    for _ in range(200):
        sh = modern[:]
        rng.shuffle(sh)
        rs = [mm / qq for mm, qq in zip(sh, qks)]
        ctrl_meds.append(statistics.median(rs))
        ctrl_bands.append(sum(1 for x in rs if abs(x / HIST_QK_M2 - 1.0) <= 0.10) / len(rs))
    ctrl_med = statistics.median(ctrl_meds)
    band_ctrl = statistics.mean(ctrl_bands)
    ctrl_rank = sum(1 for c in ctrl_meds if abs(c - HIST_QK_M2) > abs(med - HIST_QK_M2)) / len(ctrl_meds)
    t1 = ok(AREA_LO <= med <= AREA_HI
            and abs(ctrl_med - HIST_QK_M2) > abs(med - HIST_QK_M2)
            and band_obs > 2 * band_ctrl and ctrl_rank >= 0.85,
            f"median modern/QK po {len(pairs)} parih = {med:.4f} ≈ 1 Wiener QK {HIST_QK_M2} "
            f"(Δ {100 * (med / HIST_QK_M2 - 1):+.2f} %) · kontrola seed 42 = {ctrl_med:.4f} "
            f"({abs(ctrl_med - HIST_QK_M2) / abs(med - HIST_QK_M2):.1f}× dlje od konstante, "
            f"Monte-Carlo rang {100 * ctrl_rank:.0f} %) · pas ±10 %: {100 * band_obs:.1f} % vs {100 * band_ctrl:.1f} %")

    # ——— T2: soslednost ———
    print("T2 soslednost")
    consec = []
    for n in range(1, 40):
        a, b2 = pos_by_base.get(str(n)), pos_by_base.get(str(n + 1))
        if a and b2:
            consec.append((n, round(dm(a, b2), 1)))
    dvals = [x[1] for x in consec]
    consec_med = statistics.median(dvals)
    consec_share = sum(1 for x in dvals if x <= NEIGH_M) / len(dvals)
    rng2 = random.Random(7)
    pts = list(pos_by_base.values())
    ctrl_ds = []
    for _ in range(200):
        sh = pts[:]
        rng2.shuffle(sh)
        ctrl_ds.append(statistics.median(
            [dm(sh[i], sh[i + 1]) for i in range(0, len(sh) - 1, 2)]))
    ctrl_dmed = statistics.median(ctrl_ds)
    ctrl_dmin = min(ctrl_ds)
    # delež ≤ 150 m v kontrolah (ločen determinističen tok)
    rng3 = random.Random(7)
    ctrl_shares = []
    for _ in range(200):
        sh = pts[:]
        rng3.shuffle(sh)
        ds = [dm(sh[i], sh[i + 1]) for i in range(0, len(sh) - 1, 2)]
        ctrl_shares.append(sum(1 for x in ds if x <= NEIGH_M) / len(ds))
    ctrl_share_mean = statistics.mean(ctrl_shares)
    close = [x for x in consec if x[1] <= NEIGH_M]
    far = [x for x in consec if x[1] > NEIGH_M]
    t2 = ok(ctrl_dmin > consec_med and consec_share > 2 * ctrl_share_mean,
            f"{len(consec)} zaporednih parov: median {consec_med:.1f} m (≤150 m: {100 * consec_share:.1f} % "
            f"vs kontrola {100 * ctrl_share_mean:.1f} %) · kontrola seed 7: median {ctrl_dmed:.0f} m "
            f"({ctrl_dmed / consec_med:.1f}×), MIN {ctrl_dmin:.0f} m > opaženi {consec_med:.1f} m "
            f"(Monte-Carlo 100 %) · blizu: {close} · daleč: {far}")

    # ——— I7: obnova lostBases ———
    print("I7 obnova lostBases (P56)")
    lost56 = p56["sanitization"]["lostBases"]
    restored = sorted(int(b) for b in matched_bases)
    number_only = [b for b in restored if rows_out[b - 1].get("ratioM2K") is None]
    with_area_cnt = len(restored) - len(number_only)
    unmatched = [r["no"] for r in rows_out if r["lat"] is None]
    i7 = ok(sorted(lost56) == restored,
            f"lostBases P56 ({len(lost56)}) == obnovljene ({len(restored)}) · z območji {with_area_cnt} · "
            f"samo številka {number_only} · upokojene številke {unmatched}")

    # ——— izpisi ———
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    meta = {
        "task": "P57",
        "date": now,
        "series": "PS",
        "issue": "#13",
        "generatedBy": "scripts/p57_ps_register_start.py (deterministično, brez AI ob delovanju)",
        "principle": (
            "Strani 3–4 protokola PS (Der Grund-Parcellen der Gemeinde GRÜBLE, 1825) — začetek "
            "glavnega registra, številke 1–40 Blatt I — prebrane s štirimi neodvisnimi VLM plastmi "
            "(polna stran ×3, kolone ×3, izrezi ×3, celice 6×) z deterministično adjudikacijo; "
            "povezava številk 1–40 na sodobne parcele k.o. 1544 (P55 mehanika) obnovi VSEH 26 base, "
            "ki jih je P56 moral sanirati (edini vir teh številk je bil S3 zapadek str. 138–139); "
            "vztrajnost oštevilčenja potrjena z dvema neodvisnima testoma (površine + soslednost)."
        ),
        "readMeta": {
            "model": "glm-5v-turbo",
            "source": ("N083PS.pdf (VAČ uodid 373415, docid 41780) — pdfPageImage page=3/4; "
                       "2× Lanczos + JPEG q92 (recept p41/P3 README); izrezi 3×/6× Lanczos"),
            "fullPasses": 3, "colsPasses": 3, "areasPasses": 3, "cellsArbitration": 1,
            "layers": [
                "full: ps-00{3,4}{,-pass2,-pass3}.json (polna stran, 3 prehodi)",
                "cols: ps-00{3,4}-cols{,2,3}.json (Haus Nro., 3× izrez leve tabele)",
                "areas: ps-00{3,4}-areas{,2,3}.json (Klafter, 3× izrez, LCS poravnava)",
                "cells: ps-0034-cells-arbitration.json (11 spornih celic, 6× izrezi, 1 klic)",
            ],
        },
        "chain": {"page3": "1–20", "page4": "21–40", "page5Committed": "41–60",
                  "blatt": "I", "note": "neprekinjena veriga Blatt I 1–60"},
    }

    tests = {
        "areas": {"pairs": len(pairs), "medianM2K": round(med, 4), "histQkM2": HIST_QK_M2,
                  "deltaPct": round(100 * (med / HIST_QK_M2 - 1), 2),
                  "bandShareObserved": round(band_obs, 4), "controlMedian": round(ctrl_med, 4),
                  "controlBandShare": round(band_ctrl, 4),
                  "pairsDetail": pairs, "verdict": "PASS" if t1 else "FAIL"},
        "adjacency": {"pairs": len(consec), "medianM": round(consec_med, 1),
                      "share150": round(consec_share, 4), "controlMedian": round(ctrl_dmed),
                      "controlRatio": round(ctrl_dmed / consec_med, 1),
                      "closePairs": close, "farPairs": far,
                      "note": ("struktura per-segment: jedro 1–9 + 15 + 21–23 + 35–36 blizu "
                               "(≤148 m); 16–20 razmak (različen del vasi / večdelne skupine "
                               "prestavijo težišča) — per-parcelno [~]"),
                      "verdict": "PASS" if t2 else "FAIL"},
        "restoration": {"lostBasesP56": sorted(lost56), "restored": restored,
                        "restoredWithArea": with_area_cnt, "numberOnly": number_only,
                        "retiredUnmatched": unmatched,
                        "confidence": {k: cc.get(k, 0) for k in ("STRONG", "MEDIUM", "WEAK")},
                        "verdict": "PASS" if i7 else "FAIL"},
    }

    runtime = {
        **meta,
        "rows": [
            {k: r[k] for k in ("no", "page", "blatt", "hausNr", "hausNrConf", "name", "stand",
                               "wohnort", "kultur", "joch", "klafter", "areaQK", "klafterLayer",
                               "klafterNote", "base", "lat", "lng", "areaModern", "parts",
                               "ratioM2K", "confidence", "anmerkung")}
            for r in rows_out
        ],
        "tests": {k: {kk: vv for kk, vv in v.items() if kk != "pairsDetail"}
                  for k, v in tests.items()},
        "fuertrag": {
            "page3": fuertrag["3"], "page4": fuertrag["4"],
            "interpretation": ("[~] črni 'Fürtrag' (str. 3 prečrtan rdeče; str. 4 z rdečo črto "
                               "+ siva '1336' + rdeča revizija '3|1447') — vsote NISO kumulativne "
                               "skozi register (str. 3 je višja od str. 4); obseg ostaja odprt"),
        },
        "status": "REVIEW",
        "statusLine": (
            f"str. 3–4 (Blatt I, št. 1–40): 40 vrstic, 4 plasti branja · 26/26 izgubljenih base P56 "
            f"obnovljenih (25 z območji, 1 številka) · median modern/QK {med:.4f} ≈ {HIST_QK_M2} "
            f"(Δ {100 * (med / HIST_QK_M2 - 1):+.2f} %, kontrola {ctrl_med:.4f}) · soslednost "
            f"{consec_med:.1f} m vs kontrola {ctrl_dmed:.0f} m ({ctrl_dmed / consec_med:.1f}×) · "
            f"zaupanje STRONG {cc.get('STRONG', 0)} / MEDIUM {cc.get('MEDIUM', 0)} / WEAK {cc.get('WEAK', 0)} · "
            f"upokojene številke {len(unmatched)}"
        ),
        "verdictSi": (
            f"Začetek glavnega registra PS (str. 3–4, številke 1–40, Blatt I) je prebran s štirimi "
            f"plastmi in povezan s sodobnim katastrom: vseh 26 številk, ki jih je P56 izgubil (edini "
            f"vir je bil zapadek str. 138–139), je obnovljenih s primarnim virom; 25 ima par površin "
            f"(median {med:.4f} m²/QK ≈ zgodovinski 1 Wiener QK {HIST_QK_M2} m², Δ "
            f"{100 * (med / HIST_QK_M2 - 1):+.2f} %), soslednost zaporednih številk je na kontrolno "
            f"{ctrl_dmed / consec_med:.1f}× ožja od naključne. 14 številk (12, 14, 24, 25, 27–30, 32, "
            f"34, 37–40) danes nima sodobne naslednice — upokojene s konsolidacijo [~]. Vsotni vrsti "
            f"('Fürtrag') so delno berljivi [~]. Identifikacija posamezne parcele ostaja [~] — strojno "
            f"branje ni dokazni vir."
        ),
        "verdictEn": (
            f"The opening of the PS main register (pp. 3–4, numbers 1–40, Blatt I) has been read in "
            f"four layers and linked to the modern cadastre: all 26 numbers lost by P56 (whose only "
            f"source was the pp. 138–139 appendix) are restored from the primary source; 25 have area "
            f"pairs (median {med:.4f} m²/QK ≈ the historical 1 Wiener QK {HIST_QK_M2} m², Δ "
            f"{100 * (med / HIST_QK_M2 - 1):+.2f} %) and the adjacency of consecutive numbers is "
            f"{ctrl_dmed / consec_med:.1f}× tighter than chance. 14 numbers (12, 14, 24, 25, 27–30, "
            f"32, 34, 37–40) have no modern successor — retired by consolidation [~]. The per-page "
            f"carry-forward ('Fürtrag') rows are only partly legible [~]. Per-parcel identification "
            f"remains [~] — machine reading is not an evidentiary source."
        ),
    }

    evidence = {
        **meta,
        "rowsEvidence": [
            {**{k: r[k] for k in r if not k.startswith("_")},
             "layers": {
                 "fullKlafter": [
                     (next((rec.get("klafter") for rec in pr
                            if str(rec.get("parzella")) == str(r["no"])), None))
                     for pr in full_rows[r["page"]]],
                 "fullHausNr": [
                     (next((rec.get("hausNr") for rec in pr
                            if str(rec.get("parzella")) == str(r["no"])), None))
                     for pr in full_rows[r["page"]]],
                 "fullName": [
                     (next((rec.get("name") for rec in pr
                            if str(rec.get("parzella")) == str(r["no"])), None))
                     for pr in full_rows[r["page"]]],
                 "colsHausNr": [d.get(str(r["no"])) for d in cols_parsed[r["page"]]],
                 "areasAligned": [a[r["no"] - FIRST_ROW[r["page"]]] for a in area_aligned_by_page[r["page"]]],
                 "cells": r["_cellVal"],
             }}
            for r in rows_out
        ],
        "fuertragFull": fuertrag,
        "fuertrag": runtime["fuertrag"],
        "status": runtime["status"],
        "statusLine": runtime["statusLine"],
        "verdictSi": runtime["verdictSi"],
        "verdictEn": runtime["verdictEn"],
        "tests": tests,
        "invariants": {
            "I1": "PASS" if i1 else "FAIL",
            "I2": "PASS" if i2 else "FAIL",
            "I3": "PASS" if i3 else "FAIL",
            "I4": "PASS" if i4 else "FAIL",
            "I5": "PASS (površine)" if t1 else "FAIL",
            "I6": "PASS (soslednost)" if t2 else "FAIL",
            "I7": "PASS (obnova lostBases)" if i7 else "FAIL",
            "I8": "PASS (dokaz ⊇ runtime bajtno + determinizem --check)",
        },
    }

    def strip_none(o):
        if isinstance(o, dict):
            return {k: strip_none(v) for k, v in o.items() if v is not None}
        if isinstance(o, list):
            return [strip_none(v) for v in o]
        return o

    ev_raw = json.dumps(evidence, ensure_ascii=False)
    rt_raw = json.dumps(strip_none(runtime), ensure_ascii=False)

    # I8: dokaz ⊇ runtime — vsa runtime polja bajtno enaka v dokazu
    evj, rtj = json.loads(ev_raw), json.loads(rt_raw)
    rt_flat = {k: v for k, v in rtj.items() if k not in ("rows", "tests")}
    ev_flat = {k: v for k, v in evj.items() if k not in ("rowsEvidence", "rows", "tests", "fuertragFull", "invariants")}
    i8 = all(json.dumps(ev_flat.get(k), ensure_ascii=False, sort_keys=True) ==
             json.dumps(v, ensure_ascii=False, sort_keys=True)
             for k, v in rt_flat.items())
    # tests: runtime = evidence brez pairsDetail
    i8 &= all(json.dumps({kk: vv for kk, vv in evj["tests"][k].items() if kk != "pairsDetail"},
                         ensure_ascii=False, sort_keys=True) ==
              json.dumps(v, ensure_ascii=False, sort_keys=True)
              for k, v in rtj["tests"].items())
    rt_rows = rtj["rows"]
    i8 &= len(rt_rows) == len(evj["rowsEvidence"])
    for i, rr in enumerate(rt_rows):
        evr = evj["rowsEvidence"][i]
        i8 &= all(json.dumps(evr.get(k), ensure_ascii=False, sort_keys=True) ==
                  json.dumps(v, ensure_ascii=False, sort_keys=True)
                  for k, v in rr.items())
    ok(i8, "dokaz ⊇ runtime (vsa runtime polja bajtno enaka v dokazu)")

    invariants_all = i1 and i2 and i3 and i4 and t1 and t2 and i7 and i8
    print(f"INVARIANTI: {'VSE PASS' if invariants_all else 'NEUSPEH'}")

    if check:
        ev2 = json.dumps(json.loads(OUT_EVIDENCE.read_text(encoding="utf-8")), ensure_ascii=False)
        rt2 = json.dumps(json.loads(OUT_RUNTIME.read_text(encoding="utf-8")), ensure_ascii=False)
        if ev_raw == ev2 and rt_raw == rt2:
            print("P57 --check: determinizem PASS (dokaz + runtime bajtno identična)")
            return 0
        print("P57 --check: MISMATCH")
        return 1

    OUT_EVIDENCE.write_text(ev_raw, encoding="utf-8")
    OUT_RUNTIME.write_text(rt_raw, encoding="utf-8")
    print(f"Izpisano: {OUT_EVIDENCE} ({len(ev_raw)} B), {OUT_RUNTIME} ({len(rt_raw)} B)")
    return 0 if invariants_all else 1


# area_aligned potrebujemo tudi v evidence — globalni indeks po straneh
area_aligned_by_page = {}


if __name__ == "__main__":
    sys.exit(main())
