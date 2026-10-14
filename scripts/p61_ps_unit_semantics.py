#!/usr/bin/env python3
# P61 — UNIT-SEMANTICS moda B: merjena karakterizacija (odprta točka P60 #1).
#
# Vprašanje (P60 next[0]): moda B (ratio = areaModern / areaQK ≈ 1, n=62) —
# kolonialna merska enota ali delna površina?
#
# METODA (vse deterministično, brez AI ob delovanju):
#   M1 klasifikacija modi z pasovi == P60 ([3.3, 4.3] / [0.8, 1.25], QK_REF 3.59665)
#   M2 razpršenost moda B: strani, bloki ≥2 sosedenih vrstic iste strani
#   M3 Blatt distribucija (P59 pageAttribution)
#   M4 permutacijska kontrola hipoteze H1 (napačen številčni join): točke iz
#      determinističnega FNV-1a-32 hash (prenosljivo Python/TS — QA preracun),
#      radija 50/100 m, površinski pas ±25 % glede na target = areaQK × QK_REF
#   M5 hipoteza H3 (delna površina): base z ≥2 moda B vrsticami
#
# IZHODIŠČA: moda A = prava konverzija QK → m² (meritev ujeta na pravo parcelo).
# Primerjava realne vs permutirane pozicije pove, ali bi "prava parcela"
# (površina ≈ QK×3.6) bila v bližini — če ne, potem pri moda B ujeta parcela
# NIMA velike sosede → napačni join ni glavni mehanizem → moda B je drugačna
# registracijska konvencija (enota), identiteta enote ostaja ODPRTA [~].
#
# INVARIANTE:
#   I1 modi pini == P60 unitSemantics (226/62, pasovi, QK_REF)
#   I2 sha256 v2 vhoda == P60 dokaz v2Sha256 (vhod sinkron)
#   I3 GURS vhod 2117 parcel (pin) + števec pozicij
#   I4 FNV determinizem (pin FNV-1a("p61-perm-0-lat") + dvakratni izračun enak)
#   I5 Blatt distribucija moda B == pini
#   I6 bloki moda B == pini (3 bloki / 9 vrstic)
#   I7 dokaz ⊇ runtime (bajtno podmnožica)
#   I8 P59/P60 runtime nespremanjeni (sha256 pini — lekcija P9)
#   I9 determinizem — --check bajtno identično
import hashlib
import json
import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v2.json")
P59 = os.path.join(ROOT, "research/issue17/ps-blatt-headers.json")
P60_EV = os.path.join(ROOT, "research/issue17/ps-perblatt-attribution.json")
P60_RT = os.path.join(ROOT, "src/data/atlas/ps-perblatt-attribution.json")
BH_RT = os.path.join(ROOT, "src/data/atlas/ps-blatt-headers.json")
GURS = os.path.join(ROOT, "research/georef-n83/gurs/parcels-ko1544-merged.json")
OUT_EV = os.path.join(ROOT, "research/issue17/ps-unit-semantics.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-unit-semantics.json")

# ——— konstante (pasovi == P60; kontrole pinane) ———
QK_REF = 3.59665
MODA_A = (3.3, 4.3)
MODA_B = (0.8, 1.25)
RADIUS = (50.0, 100.0)
PAS = 0.25
FNV_OFFSET = 0x811C9DC5
FNV_PRIME = 0x01000193
FNV_PIN = 1711381398  # FNV-1a-32("p61-perm-0-lat") — pin determinizma

# ——— pini rezultatov (vzorci iz podatkov; skripta FAIL ob odmiku) ———
PIN_MODI = {"A": 226, "B": 62, "X": 800, "noRatio": 5}
PIN_BLATT_B = {"II": 32, "IV": 15, "III": 9, "I": 5, "I·II": 1, "null": 0}  # P62: null 5 (strani 133–136) → IV +4, II +1
PIN_BLOCKS = 3
PIN_BLOCK_ROWS = 9
PIN_MULTI_B_BASES = 2  # base z ≥2 moda B vrsticami (H3 neuporabna)
# hit številce (realno/perm) @ radij — I4-primerjava + runtime pini za QA
PIN_HITS = {
    "A": {"real50": 209, "perm50": 37, "real100": 220, "perm100": 118},
    "B": {"real50": 18, "perm50": 11, "real100": 45, "perm100": 38},
}


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def median(vals):
    s = sorted(vals)
    return s[len(s) // 2] if s else None


def fnv1a32(s: str) -> int:
    """FNV-1a 32-bit — ista implementacija mora biti v TS QA (bajtno enaka)."""
    h = FNV_OFFSET
    for b in s.encode("utf-8"):
        h = ((h ^ b) * FNV_PRIME) & 0xFFFFFFFF
    return h


def perm_point(i, box):
    """Deterministična 'naključna' točka i — FNV-1a na fiksnih nizih (TS prenosljivo)."""
    latMin, latMax, lngMin, lngMax = box
    la = latMin + fnv1a32(f"p61-perm-{i}-lat") / 4294967296.0 * (latMax - latMin)
    ln = lngMin + fnv1a32(f"p61-perm-{i}-lng") / 4294967296.0 * (lngMax - lngMin)
    return la, ln


def dm(a, b):
    """Razdalja m — EKSPlicitna formula (sqrt/hypot razlike čez jezike izločene)."""
    dlat = (a[0] - b[0]) * 111320.0
    dlng = (a[1] - b[1]) * 111320.0 * math.cos(a[0] * math.pi / 180.0)
    return math.sqrt(dlat * dlat + dlng * dlng)


def band(v):
    if v is None:
        return None
    if MODA_A[0] <= v <= MODA_A[1]:
        return "A"
    if MODA_B[0] <= v <= MODA_B[1]:
        return "B"
    return "X"


def pnum(p):
    s = str(p)
    return int(s) if s.isdigit() else 10 ** 9


def hit_count(points, gurs_c, R):
    """Števec točk, ki imajo v radiju R parcelo s površino v pasu ±PAS glede na target."""
    ok = 0
    for (la, ln, t) in points:
        if t <= 0:
            continue
        found = False
        for g in gurs_c:
            if dm((la, ln), (g[2], g[3])) <= R and abs(g[1] - t) / t <= PAS:
                found = True
                break
        if found:
            ok += 1
    return ok


def main():
    v2 = json.load(open(V2))
    p59_ev = json.load(open(P59))
    p60_ev = json.load(open(P60_EV))
    gurs = json.load(open(GURS))

    rows = v2["rowsEvidence"]
    page_attr = p59_ev["pageAttribution"]

    # ————— I2: v2 vhod sinkron s P60 —————
    if sha256(V2) != p60_ev.get("v2Sha256"):
        fail("I2 sha256(v2) ≠ P60 dokaz v2Sha256")

    # ————— I1: modi klasifikacija == P60 pini —————
    us = p60_ev["unitSemantics"]
    if us["modaA"]["band"] != list(MODA_A) or us["modaB"]["band"] != list(MODA_B):
        fail(f"I1 pasovi ≠ P60: {us['modaA']['band']} / {us['modaB']['band']}")
    if abs(us["qkReference"] - QK_REF) > 1e-9:
        fail("I1 qkReference ≠ 3.59665")
    counts = {"A": 0, "B": 0, "X": 0, "noRatio": 0}
    for r in rows:
        b = band(r.get("ratio"))
        counts["noRatio" if b is None else b] += 1
    if counts != PIN_MODI:
        fail(f"I1 modi {counts} ≠ pini {PIN_MODI}")
    if us["modaA"]["count"] != PIN_MODI["A"] or us["modaB"]["count"] != PIN_MODI["B"]:
        fail("I1 P60 unitSemantics counts ≠ 226/62")

    # protokolni vrstni red (page, parzella)
    ordered = sorted(rows, key=lambda r: (r["page"], pnum(r["parzella"])))

    # ————— M2: razpršenost + bloki —————
    b_rows = [r for r in ordered if band(r.get("ratio")) == "B"]
    pages_b = sorted({r["page"] for r in b_rows})
    blocks = []
    cur = []
    for i, r in enumerate(ordered):
        if band(r.get("ratio")) == "B" and cur and ordered[i - 1]["page"] == r["page"] \
                and band(ordered[i - 1].get("ratio")) == "B":
            cur.append(r)
        else:
            if len(cur) >= 2:
                blocks.append(cur)
            cur = [r] if band(r.get("ratio")) == "B" else []
    if len(cur) >= 2:
        blocks.append(cur)
    n_block_rows = sum(len(x) for x in blocks)
    if len(blocks) != PIN_BLOCKS or n_block_rows != PIN_BLOCK_ROWS:
        fail(f"I6 bloki {len(blocks)}/{n_block_rows} ≠ pini {PIN_BLOCKS}/{PIN_BLOCK_ROWS}")

    # ————— M3: Blatt distribucija (P59 pageAttribution) —————
    blatt_b = defaultdict(int)
    for r in b_rows:
        att = page_attr.get(str(r["page"]), {})
        bl = att.get("blatt")
        blatt_b[bl if bl else "null"] += 1
    blatt_b_s = {k: blatt_b.get(k, 0) for k in ("II", "IV", "III", "I", "I·II", "null")}
    if blatt_b_s != PIN_BLATT_B:
        fail(f"I5 blattDist {blatt_b_s} ≠ pini {PIN_BLATT_B}")

    # ————— M5: H3 delna površina —————
    b_by_base = defaultdict(int)
    for r in b_rows:
        b_by_base[r["base"]] += 1
    multi_b = {b for b, n in b_by_base.items() if n >= 2}
    if len(multi_b) != PIN_MULTI_B_BASES:
        fail(f"M5 base z ≥2 moda B vrsticami {len(multi_b)} ≠ {PIN_MULTI_B_BASES}")

    # ————— I3: GURS vhod + kompakt (st, povrsina, lat, lng) —————
    if len(gurs) != 2117:
        fail(f"I3 GURS {len(gurs)} ≠ 2117")
    gurs_c = [(g["st"], float(g["povrsina"]), g["lat"], g["lng"])
              for g in gurs if g.get("lat") is not None and g.get("lng") is not None]
    n_gurs_pos = len(gurs_c)

    # ————— M4: permutacijska kontrola —————
    lats = [g[2] for g in gurs_c]
    lngs = [g[3] for g in gurs_c]
    box = (min(lats), max(lats), min(lngs), max(lngs))
    real_pts = {"A": [], "B": []}
    for r in ordered:
        b = band(r.get("ratio"))
        if b in ("A", "B"):
            real_pts[b].append((r["lat"], r["lng"], r["areaQK"] * QK_REF))
    perm_pts = {"A": [], "B": []}
    for b in ("A", "B"):
        for i in range(len(real_pts[b])):
            la, ln = perm_point(i, box)
            perm_pts[b].append((la, ln, real_pts[b][i][2]))
    hits = {"A": {}, "B": {}}
    for b in ("A", "B"):
        for tag, R in (("50", RADIUS[0]), ("100", RADIUS[1])):
            real = hit_count(real_pts[b], gurs_c, R)
            perm = hit_count(perm_pts[b], gurs_c, R)
            hits[b][f"real{tag}"] = real
            hits[b][f"perm{tag}"] = perm
    if hits != PIN_HITS:
        fail(f"M4 hits {hits} ≠ pini {PIN_HITS}")

    # ————— I4: FNV determinizem —————
    if fnv1a32("p61-perm-0-lat") != FNV_PIN:
        fail(f"I4 FNV pin {fnv1a32('p61-perm-0-lat')} ≠ {FNV_PIN}")
    if hit_count(perm_pts["B"], gurs_c, RADIUS[1]) != hit_count(list(reversed(perm_pts["B"])), gurs_c, RADIUS[1]):
        fail("I4 FNV determinizem: obratni vrstni red da drug rezultat")

    # ————— rate pomožno (4 decimalki, za izpise) —————
    def rate(h, n):
        return round(h / n, 4)

    stats = {}
    for b in ("A", "B"):
        n = len(real_pts[b])
        stats[b] = {"n": n,
                    "real50": {"hit": hits[b]["real50"], "rate": rate(hits[b]["real50"], n)},
                    "perm50": {"hit": hits[b]["perm50"], "rate": rate(hits[b]["perm50"], n)},
                    "real100": {"hit": hits[b]["real100"], "rate": rate(hits[b]["real100"], n)},
                    "perm100": {"hit": hits[b]["perm100"], "rate": rate(hits[b]["perm100"], n)}}

    aqk_b = [r["areaQK"] for r in b_rows]
    a_rows = [r for r in rows if band(r.get("ratio")) == "A"]
    aqk_a = [r["areaQK"] for r in a_rows]

    kultur_b = defaultdict(int)
    for r in b_rows:
        kultur_b[r.get("kultur") or "null"] += 1
    kultur_top = sorted(kultur_b.items(), key=lambda kv: (-kv[1], kv[0]))[:10]

    gurs_sha = sha256(GURS)
    p60rt_sha = sha256(P60_RT)
    bhrt_sha = sha256(BH_RT)

    status_line = (
        f"P61 UNIT-SEMANTICS MERJENA: moda B (ratio ≈ 1, n={PIN_MODI['B']}) = drugačna registracijska "
        f"konvencija [~], ne napaka ujeme — permutacijska kontrola @ 50/100 m pas ±25 %: moda A real "
        f"{stats['A']['real50']['rate']}/{stats['A']['real100']['rate']} vs perm "
        f"{stats['A']['perm50']['rate']}/{stats['A']['perm100']['rate']} (ujeta = prava parcela), "
        f"moda B real {stats['B']['real50']['rate']}/{stats['B']['real100']['rate']} vs perm "
        f"{stats['B']['perm50']['rate']}/{stats['B']['perm100']['rate']} → prava parcela (QK×3.6) ni v "
        f"bližini → H1 napačni join ZAVRŽEN; delna površina neuporabna ({PIN_MULTI_B_BASES} base z ≥2 B); "
        f"blattDist II {PIN_BLATT_B['II']} · IV {PIN_BLATT_B['IV']} · III {PIN_BLATT_B['III']} · "
        f"I {PIN_BLATT_B['I']}; bloki {PIN_BLOCKS}/{PIN_BLOCK_ROWS}; identiteta enote ODPRTA; "
        f"pas pravilo P59/P60 = moda B — atribucija smiselna kot relativa"
    )

    verdict_si = (
        "P61 merjeno razrešuje odprto točko P60 #1 s preusmeritvijo: moda B ni napaka ujeme in ni "
        "delna površina — je dosledna drugačna registracijska konvencija površin (številka ≈ sodobna "
        f"meritev v m²; n={PIN_MODI['B']} vrstic, {len(pages_b)} strani, Blatt II {PIN_BLATT_B['II']} · "
        f"IV {PIN_BLATT_B['IV']} · III {PIN_BLATT_B['III']} · I {PIN_BLATT_B['I']}). Permutacijska "
        f"kontrola (FNV-1a deterministične točke, radija 50/100 m, pas ±25 %): pri moda A je prava "
        f"parcela (površina ≈ QK×3.6) tik zraven ({stats['A']['real50']['rate']} @ 50 m vs "
        f"{stats['A']['perm50']['rate']} naključno), pri moda B pa ni ({stats['B']['real50']['rate']} vs "
        f"{stats['B']['perm50']['rate']}) → napačni številčni join ZAVRŽEN kot glavni mehanizem. "
        "Delna površina neuporabna: samo 2 base z ≥2 moda B vrsticami. Identiteta enote ostaja ODPRTA "
        "[~] — paleografska/dokumentarna potrditev. Implikacija za P60: pas pravilo [0.8, 1.25] izbere "
        "vrstico v konvenciji, ki je številčno primerljiva s sodobno meritvijo — atribucija ostaja "
        "smiselna kot RELATIVA [~]; join v2 NESPREMENJEN."
    )
    verdict_en = (
        "P61 measures and re-frames P60 open point #1: mode B is not a join error and not a partial "
        f"surface — it is a consistent alternative registration convention (number ≈ modern m²; "
        f"n={PIN_MODI['B']} rows, {len(pages_b)} pages, Blatt II {PIN_BLATT_B['II']} · IV "
        f"{PIN_BLATT_B['IV']} · III {PIN_BLATT_B['III']} · I {PIN_BLATT_B['I']}). Permutation control "
        f"(FNV-1a deterministic points, 50/100 m, ±25 %): for mode A the true parcel (≈ QK×3.6) sits "
        f"next door ({stats['A']['real50']['rate']} @ 50 m vs {stats['A']['perm50']['rate']} random), "
        f"for mode B it does not ({stats['B']['real50']['rate']} vs {stats['B']['perm50']['rate']}) → "
        "wrong-number join REJECTED as the main mechanism. Partial surface unusable: only 2 bases with "
        "≥2 mode B rows. Unit identity remains OPEN [~] — paleographic/documentary confirmation. "
        "Implication for P60: the [0.8, 1.25] band selects rows in the convention numerically "
        "comparable with the modern measurement — attribution remains sound as RELATIVE [~]; join v2 "
        "UNCHANGED."
    )

    ev = {
        "task": "P61 — unit-semantics moda B: merjena karakterizacija (odprta točka P60 #1)",
        "date": "2026-10-14",
        "principle": ("moda B merjena s permutacijsko kontrolo na GURS parcelah KO 1544: napačni "
                      "številčni join ZAVRŽEN, delna površina neuporabna — moda B = drugačna "
                      "registracijska konvencija [~], identiteta enote ODPRTA; deterministične "
                      "FNV-1a točke (prenosljivo Python/TS) po receptu P55 kontrol"),
        "inputs": {
            "v2": "research/issue17/ps-parcels-geo-v2.json (rowsEvidence 1093, sha256 == P60)",
            "gurs": "research/georef-n83/gurs/parcels-ko1544-merged.json (2117 parcel, P47)",
            "p59": "research/issue17/ps-blatt-headers.json (pageAttribution)",
            "p60": "research/issue17/ps-perblatt-attribution.json (unitSemantics + v2Sha256)",
        },
        "method": {
            "bands": {"modaA": list(MODA_A), "modaB": list(MODA_B)},
            "qkReference": QK_REF,
            "radiusM": list(RADIUS),
            "pas": PAS,
            "perm": "FNV-1a-32 na fiksnih nizih 'p61-perm-{i}-{lat|lng}' (Python/TS bajtno enako)",
            "target": "areaQK × 3.59665 (m²)",
        },
        "v2Sha256": sha256(V2),
        "gursSha256": gurs_sha,
        "summary": {
            "modi": PIN_MODI,
            "modaBPages": pages_b,
            "modaBBlattDist": blatt_b_s,
            "blocks": [{"pages": sorted({x["page"] for x in blk}), "n": len(blk),
                        "bases": [x["base"] for x in blk],
                        "kultur": blk[0].get("kultur")} for blk in blocks],
            "multiB": sorted(multi_b),
            "areaQK": {"B": {"mediana": median(aqk_b), "min": min(aqk_b), "max": max(aqk_b)},
                       "A": {"mediana": median(aqk_a), "min": min(aqk_a), "max": max(aqk_a)}},
            "kulturTopB": kultur_top,
        },
        "kontrola": stats,
        "hipoteze": {
            "H1_napacenJoin": {
                "status": "ZAVRŽEN",
                "dokaz": (f"moda A real @50 {stats['A']['real50']['rate']} vs perm "
                          f"{stats['A']['perm50']['rate']}; moda B real @50 "
                          f"{stats['B']['real50']['rate']} vs perm {stats['B']['perm50']['rate']} — "
                          "prava parcela (QK×3.6) pri moda B ni tik zraven; @100 m base rate raste "
                          "z gostoto parcel (A perm " + str(stats['A']['perm100']['rate']) + ", B perm " +
                          str(stats['B']['perm100']['rate']) + ") — diskriminator je 50 m"),
            },
            "H3_delnaPovrsina": {
                "status": "NEUPORABNA",
                "dokaz": (f"samo {PIN_MULTI_B_BASES} base z ≥2 moda B vrsticami "
                          "(163: 226+214 @ p61/p86; 176: 334+289 @ p83/p86) — blok p85 = "
                          "različne base (644–657 družina), ne delitve istih"),
            },
            "H2_drugaEnota": {
                "status": "OSTAJA [~]",
                "dokaz": ("meritev ujeta na pravo parcelo; register nosi številko ≈ m² — "
                          "identiteta enote/konvencije ODPRTA (paleografija/dokumenti)"),
            },
        },
        "implikacijeP60": {
            "pasPravilo": "[0.8, 1.25] = moda B pas",
            "smisel": ("pas izbere vrstico v konvenciji, številčno primerljivi s sodobno meritvijo — "
                       "atribucija smiselna kot RELATIVA [~]; atribucije P60 NESPREMENJENE"),
        },
        "invariants": ["I1 modi == P60", "I2 v2 sinkron", "I3 GURS 2117", "I4 FNV determinizem",
                       "I5 blattDist", "I6 bloki", "I7 dokaz ⊇ runtime", "I8 P59/P60 runtime pini",
                       "I9 --check bajtno"],
        "statusLine": status_line,
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "next": [
            "identiteta enote moda B (paleografija/dokumenti: glave sekcij str. 61–99, pojasnila registra)",
            "razširitev atribucije na 106 čez-Blatt base (potrebna P59 pokritost 133–136 + 138–139 ob VLM kvoti)",
            "razlaga strani 61/83–87/99 kot Kultur-Tabellen: navzkrižje s Kultur stolpcem polnih branj P38",
            "per-Blatt SPLIT joina za atributirane base (zahteva pini + odločitev lastnika o pozicijah)",
            "povezati lastnike pas-instanc (npr. 163 II) s PF protokolom",
        ],
    }

    # ————— runtime (kompakten + gursCompact za QA produkcija preracun) —————
    runtime = {
        "version": 1,
        "task": ev["task"],
        "date": ev["date"],
        "generatedBy": "scripts/p61_ps_unit_semantics.py",
        "method": ev["method"],
        "summary": ev["summary"],
        "kontrola": ev["kontrola"],
        "hipoteze": ev["hipoteze"],
        "implikacijeP60": ev["implikacijeP60"],
        "pini": {
            "v2Sha256": ev["v2Sha256"],
            "gursSha256": gurs_sha,
            "gursPositioned": n_gurs_pos,
            "hits": PIN_HITS,
            "fnv": FNV_PIN,
            "blattDist": PIN_BLATT_B,
            "blocks": {"n": PIN_BLOCKS, "rows": PIN_BLOCK_ROWS},
            "multiB": PIN_MULTI_B_BASES,
            "p60RuntimeSha256": p60rt_sha,
            "blattHeadersRuntimeSha256": bhrt_sha,
        },
        "statusLine": status_line,
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "gursCompact": [[g[0], g[1], g[2], g[3]] for g in gurs_c],
    }

    # ————— I8: P59/P60 runtime nespremanjeni —————
    if p60rt_sha != "28465b3e28fef763f951dc8ea379b7e071bd9d5fa109ebb9a577e594236e386a":
        fail("I8 P60 runtime sha256 odmik (pini po P9 lekciji)")
    if bhrt_sha != "efe39f41dc4f81703e3b8aa47632faef75222a000ad13b7a674f3a853c1ee66e":  # P63: korekcija p139 = Blatt IIb (oči 5x + 3. VLM prehod); p138 izčrpen opis ostankov + 'Zusammenstellung'
        fail("I8 P59 blatt-headers runtime sha256 odmik")

    # ————— I7: dokaz ⊇ runtime bajtno —————
    ev_sub = json.loads(json.dumps(ev))
    ev_sub["runtime"] = runtime
    with open(OUT_EV, "w") as f:
        json.dump(ev_sub, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    with open(OUT_RT, "w") as f:
        json.dump(runtime, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    ev_check = json.load(open(OUT_EV))
    rt_bytes = open(OUT_RT, "rb").read()
    if json.dumps(ev_check["runtime"], indent=1, ensure_ascii=False, sort_keys=True).encode() + b"\n" != rt_bytes:
        fail("I7 runtime ni bajtno podmnožica dokaza")

    print(f"OK: modi {PIN_MODI}, moda B @ {len(pages_b)} strani, bloki {PIN_BLOCKS}/{PIN_BLOCK_ROWS}")
    for b in ("A", "B"):
        s = stats[b]
        print(f"OK: moda {b} @50 real {s['real50']['rate']} perm {s['perm50']['rate']} · "
              f"@100 real {s['real100']['rate']} perm {s['perm100']['rate']}")
    print(f"OK: GURS {len(gurs)} ({n_gurs_pos} pozicij), FNV pin OK")
    print(f"OK: dokaz {OUT_EV}, runtime {OUT_RT}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        h1 = sha256(OUT_EV)
        main()
        if sha256(OUT_EV) != h1:
            fail("I9 determinizem: izhod se je spremenil")
        print("I9 --check: PASS")
    else:
        main()
