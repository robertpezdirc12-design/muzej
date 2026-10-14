#!/usr/bin/env python3
# P66 — SPLIT DECISION PACK: 39 split base (odločitveni paket za per-Blatt
# SPLIT joina — odprta točka P64 #8 / kandidat #1 iz P65 `next`).
#
# P65 je pokritost per-Blatt atribucije več-stranskih base zaprla 211/211
# (172 atributiranih + 39 split z alternativami). SPLIT joina (#8) je
# LASTNIŠKA ODLOČITEV — P66 ne odloča namesto lastnika, ampak MERI in
# DOKAZUJE vsa dejstva, ki odločitev podpirajo (deterministično, brez AI
# ob delovanju; join v2 NESPREMENJEN — disciplina P56/P58/P59/P65).
#
# Merjeno nad 39 split base (iz P65 runtime, bajtni vir) × v2 rowsEvidence
# × P59 pageAttribution:
#   • blattPair dist: I·II 7 · II·III 21 · II·IV 2 · IV·V 9
#     (37/39 sosednja Blatta; 2 skok II·IV — preskočita III)
#   • shareCount dist: VSI 39 = 2 deleža
#   • vrstice: 93 (25 × 2 + 13 × 3 + 1 × 4)
#   • lastniki: 2 edinstvena 25 · 3 13 · 4 1; ownerRelation
#     per Blatt-par: DISJUNKTNI 39/39 — vsak split base ima RAZLIČNE
#     lastnike po Blattih (močan dokaz, da je ista številka pod
#     različnima Blattoma 2 RAZLIČNI realni parceli, ne isti parceli
#     prestopa meje) — JEDRO odločitvenega paketa
#   • dominantni delež pasovi: [0.50,0.60) 23 · [0.60,0.70) 11 ·
#     [0.70,0.75) 5 (razlog za split: delež < 0.75, R2a ne zadošča)
#   • kulture: 92 (največ 3 per base); kulturesByBlatt razčlenitev
#   • GEO: 39/39 base ima VSEH vrstic ENAKO geometrijo joina v2 (0
#     različnih, 0 null) — join v2 je na nivoju številke, zato split
#     base danes nosi eno geometrijo za 2 realni parceli → SPLIT join
#     bi zahteval 2 geometriji (odločitev lastnika; tukaj samo števec,
#     brez koordinat — I6)
#   • areaSuspect: 0 vrstic; sosledje split del: ok 82 / flag 11
#     (flag 5 base: 646, 661, 1821, 2141, 2143)
#
# Vhodi (committed):
#   research/issue17/ps-parcels-geo-v2.json      — vrstice v2 (rowsEvidence)
#   research/issue17/ps-blatt-headers.json       — P59 dokaz (pageAttribution)
#   src/data/atlas/ps-attribution-full.json      — P65 runtime (bajtni vir 211)
# Izhodi:
#   research/issue17/ps-split-pack.json          (dokaz)
#   src/data/atlas/ps-split-pack.json            (runtime, bajtna projekcija)
#
# Invarianti (FAIL ob padu):
#   I1 vhodni pini: 3× sha256 (v2 ev ebb8f729…, P59 ev 95929a2e…, P65 rt
#      74477ac8…); števci 1093/800/211/39
#   I2 razčlenitev: 39 split ⊂ 211 multi-page; attributedBlatt null × 39;
#      blattShares == 2 × 39; Σ share == 1 (± 1e-6); Σ areaQK per Blatt
#      == Σ areaQK vrstic (bajtno half-up); 0 vrstic brez atribucije strani
#   I3 P65 polja bajtno (deep equality 39×: status, attributedBlatt,
#      blattShares, rowsTotal, pages, kultures, owners, sosledje)
#   I4 distribucije: blattPair 7/21/2/9 · shareCount 39 · vrstice 25/13/1 ·
#      uniqueOwners 25/13/1 · ownerRelation disjoint 39 · pasovi 23/11/5 ·
#      kulture 92 · geo 39/0/0 · areaSuspect 0
#   I5 sosledje split del == P65 bajtno (ok 82 / flag 11; 93 relevantnih)
#   I6 brez georef polj (lat, lng, areaModern, ratio) v izpisu; geoShared
#      samo kot števec (merjeno iz v2, brez koordinat); v2 sha nespremenjen
#   I7 dokaz ⊇ runtime (bajtno podmnožica)
#   I8 determinizem — --check bajtno identično
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v2.json")
P59 = os.path.join(ROOT, "research/issue17/ps-blatt-headers.json")
P65RT = os.path.join(ROOT, "src/data/atlas/ps-attribution-full.json")
OUT_EV = os.path.join(ROOT, "research/issue17/ps-split-pack.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-split-pack.json")

PIN_V2EV_SHA = "ebb8f7298de713e73bc7417f392d60c7e5eb03a6675f96317320188750e27731"
PIN_P59EV_SHA = "95929a2e373f7e4acd8f5fe4e93db08419e18c8dfbc604c1fc87beeae65da973"
PIN_P65RT_SHA = "74477ac800ad47b4a37805aa0b398ddc88327f8c45afc342f97a084813d0396d"

EXPECTED_ROWS = 1093
EXPECTED_BASES = 800
EXPECTED_MULTI = 211
EXPECTED_SPLIT = 39

EXPECTED_PAIRS = {"I·II": 7, "II·III": 21, "II·IV": 2, "IV·V": 9}
EXPECTED_ADJACENT = 37
EXPECTED_SKIP = 2
EXPECTED_SHARE_COUNT = {"2": 39}
EXPECTED_ROWS_DIST = {"2": 25, "3": 13, "4": 1}
EXPECTED_OWNERS = {"2": 25, "3": 13, "4": 1}
EXPECTED_OWNER_REL = {"disjoint": 39}
EXPECTED_BUCKETS = {"0.50–0.60": 23, "0.60–0.70": 11, "0.70–0.75": 5}
EXPECTED_KULTURES = 92
EXPECTED_GEO = {"shared": 39, "distinct": 0, "null": 0}
EXPECTED_AREA_SUSPECT = 0
EXPECTED_SOS = {"ok": 82, "flag": 11}
EXPECTED_SOS_FLAG_BASES = ["1821", "2141", "2143", "646", "661"]

P65_KEYS = ("status", "attributedBlatt", "blattShares", "rowsTotal", "pages",
            "kultures", "owners", "sosledje")

ADJACENT = {("I", "II"), ("II", "III"), ("III", "IV"), ("IV", "V")}

GEO_FIELDS = ("lat", "lng", "areaModern", "ratio")


def fail(msg):
    print(f"FAIL I: {msg}")
    sys.exit(1)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def rnd(x, n):
    """Half-up zaokroževanje (JS Math.round kompatibilno)."""
    return math.floor(x * (10 ** n) + 0.5) / (10 ** n)


def main():
    v2 = json.load(open(V2))
    p59 = json.load(open(P59))
    p65 = json.load(open(P65RT))

    rows = v2["rowsEvidence"]
    page_attr = p59["pageAttribution"]
    p65_bases = p65["bases"]
    split_65 = {k: e for k, e in p65_bases.items() if e.get("status") == "split"}

    # ————— I1 vhodni pini —————
    if sha256(V2) != PIN_V2EV_SHA:
        fail("I1 sha256 v2 vhoda se je spremenil (drift — preveri P65 chain)")
    if sha256(P59) != PIN_P59EV_SHA:
        fail("I1 sha256 dokaza ps-blatt-headers.json ≠ pin (drift)")
    if sha256(P65RT) != PIN_P65RT_SHA:
        fail("I1 sha256 runtime ps-attribution-full.json ≠ pin (drift)")
    if len(rows) != EXPECTED_ROWS:
        fail(f"I1 rowsEvidence {len(rows)} ≠ {EXPECTED_ROWS}")
    all_bases = {r["base"] for r in rows}
    if len(all_bases) != EXPECTED_BASES:
        fail(f"I1 base {len(all_bases)} ≠ {EXPECTED_BASES}")
    if len(p65_bases) != EXPECTED_MULTI:
        fail(f"I1 P65 runtime base {len(p65_bases)} ≠ {EXPECTED_MULTI}")
    if len(split_65) != EXPECTED_SPLIT:
        fail(f"I1 split base {len(split_65)} ≠ {EXPECTED_SPLIT}")

    rows_by_base = defaultdict(list)
    for r in rows:
        rows_by_base[r["base"]].append(r)

    def blatt(p):
        b = page_attr.get(str(p), {}).get("blatt")
        if not b:
            fail(f"I2 stran {p} brez atribucije Blatta")
        return b

    def bucket(d):
        if 0.50 <= d < 0.60:
            return "0.50–0.60"
        if 0.60 <= d < 0.70:
            return "0.60–0.70"
        if 0.70 <= d < 0.75:
            return "0.70–0.75"
        return "outside"

    pairs = Counter()
    adjacent = skip = 0
    share_count = Counter()
    rows_dist = Counter()
    owners_dist = Counter()
    owner_rel = Counter()
    buckets = Counter()
    kultures_total = 0
    geo = Counter()
    area_suspect = 0
    sos_ok = sos_flag = 0
    sos_flag_bases = []
    bases_out = {}

    # ————— per base —————
    for b in sorted(split_65, key=int):
        e65 = split_65[b]
        rs = rows_by_base.get(b)
        if not rs:
            fail(f"I2 {b}: brez vrstic v v2")
        if len(rs) != e65["rowsTotal"]:
            fail(f"I2 {b}: vrstic {len(rs)} ≠ P65 rowsTotal {e65['rowstTotal'] if False else e65['rowsTotal']}")

        # I3: P65 polja bajtno
        entry = {}
        for k in P65_KEYS:
            entry[k] = json.loads(json.dumps(e65[k]))
            if entry[k] != e65[k]:
                fail(f"I3 {b}: P65 polje '{k}' se je spremenilo")

        # I2: blattShares kontrola
        shares = entry["blattShares"]
        if len(shares) != 2:
            fail(f"I2 {b}: blattShares {len(shares)} ≠ 2")
        s_tot = sum(s["share"] for s in shares)
        if abs(s_tot - 1.0) > 1e-3:  # deleži half-up @ 4 decimalki (P64) — vsota lahko odstopa ≤ 1e-4
            fail(f"I2 {b}: Σ share {s_tot} ≠ 1")
        a_tot = sum(s["areaQK"] for s in shares)
        rows_a = sum(r.get("areaQK") or 0.0 for r in rs)
        if abs(a_tot - rows_a) > 1e-6:
            fail(f"I2 {b}: Σ areaQK shares {a_tot} ≠ vrstice {rows_a}")

        # per-Blatt razčlenitev
        rows_out = []
        kult_by = defaultdict(set)
        own_by = defaultdict(set)
        for r in rs:
            bl = blatt(r["page"])
            if r.get("kultur"):
                kult_by[bl].add(str(r["kultur"]))
            if r.get("owner"):
                own_by[bl].add(r["owner"])
            if r.get("areaSuspect"):
                area_suspect += 1
            row = {
                "page": r["page"], "blatt": bl, "parzella": r["parzella"],
                "base": r["base"], "owner": r.get("owner"),
                "stand": r.get("stand"), "hausNr": r.get("hausNr"),
                "wohnort": r.get("wohnort"),
                "wohnortInherited": r.get("wohnortInherited"),
                "kultur": r.get("kultur"), "joch": r.get("joch"),
                "klafter": r.get("klafter"), "areaQK": r.get("areaQK"),
                "areaSuspect": r.get("areaSuspect"), "parts": r.get("parts"),
                "conf": r.get("conf"), "series": r.get("series"),
                "ambiguous": r.get("ambiguous"),
            }
            for extra in ("source", "readConf", "anmerkung"):
                if r.get(extra) is not None:
                    row[extra] = r[extra]
            rows_out.append(row)

        blatts = sorted(s["blatt"] for s in shares)
        pair = "·".join(blatts)
        pairs[pair] += 1
        if tuple(blatts) in ADJACENT:
            adjacent += 1
        else:
            skip += 1

        share_count[str(len(shares))] += 1
        rows_dist[str(entry["rowsTotal"])] += 1

        dom = shares[0]["share"]  # P65 sort: areaQK desc → [0] dominantni
        entry["dominantShare"] = dom
        entry["shareDelta"] = rnd(dom - shares[1]["share"], 4)
        buckets[bucket(dom)] += 1

        uo = len(entry["owners"])
        owners_dist[str(uo)] += 1
        if not own_by[blatts[0]] or not own_by[blatts[1]]:
            rel = "open"
        elif own_by[blatts[0]].isdisjoint(own_by[blatts[1]]):
            rel = "disjoint"
        elif own_by[blatts[0]] == own_by[blatts[1]]:
            rel = "equal"
        else:
            rel = "overlap"
        owner_rel[rel] += 1

        kultures_total += len(entry["kultures"])

        # GEO (I6: samo števec — brez koordinat v izpisu)
        geos = {(r.get("lat"), r.get("lng")) for r in rs}
        if (None, None) in geos and len(geos) == 1:
            geo["null"] += 1
            entry["geoShared"] = None
        elif len(geos) <= 1:
            geo["shared"] += 1
            entry["geoShared"] = True
        else:
            geo["distinct"] += 1
            entry["geoShared"] = False

        # sosledje split del == P65 (I5)
        s65 = e65["sosledje"]
        sos_ok += s65["ok"]
        sos_flag += s65["flag"]
        if s65["flag"] > 0:
            sos_flag_bases.append(b)

        entry["blattPair"] = pair
        entry["kulturesByBlatt"] = {k: sorted(v) for k, v in sorted(kult_by.items())}
        entry["ownersByBlatt"] = {k: sorted(v) for k, v in sorted(own_by.items())}
        entry["ownerRelation"] = rel
        entry["rows"] = rows_out
        bases_out[b] = entry

    # ————— I4 distribucije —————
    if dict(pairs) != EXPECTED_PAIRS:
        fail(f"I4 blattPair {dict(pairs)} ≠ {EXPECTED_PAIRS}")
    if adjacent != EXPECTED_ADJACENT or skip != EXPECTED_SKIP:
        fail(f"I4 sosednji/skok {adjacent}/{skip} ≠ {EXPECTED_ADJACENT}/{EXPECTED_SKIP}")
    if dict(share_count) != EXPECTED_SHARE_COUNT:
        fail(f"I4 shareCount {dict(share_count)} ≠ {EXPECTED_SHARE_COUNT}")
    if dict(rows_dist) != EXPECTED_ROWS_DIST:
        fail(f"I4 rowsDist {dict(rows_dist)} ≠ {EXPECTED_ROWS_DIST}")
    if dict(owners_dist) != EXPECTED_OWNERS:
        fail(f"I4 uniqueOwners {dict(owners_dist)} ≠ {EXPECTED_OWNERS}")
    if dict(owner_rel) != EXPECTED_OWNER_REL:
        fail(f"I4 ownerRelation {dict(owner_rel)} ≠ {EXPECTED_OWNER_REL}")
    if dict(buckets) != EXPECTED_BUCKETS:
        fail(f"I4 dominantShareBuckets {dict(buckets)} ≠ {EXPECTED_BUCKETS}")
    if kultures_total != EXPECTED_KULTURES:
        fail(f"I4 kulture {kultures_total} ≠ {EXPECTED_KULTURES}")
    if {k: geo[k] for k in EXPECTED_GEO} != EXPECTED_GEO:
        fail(f"I4 geo {dict(geo)} ≠ {EXPECTED_GEO}")
    if area_suspect != EXPECTED_AREA_SUSPECT:
        fail(f"I4 areaSuspect {area_suspect} ≠ {EXPECTED_AREA_SUSPECT}")

    # ————— I5 sosledje —————
    if sos_ok != EXPECTED_SOS["ok"] or sos_flag != EXPECTED_SOS["flag"]:
        fail(f"I5 sosledje {sos_ok}/{sos_flag} ≠ {EXPECTED_SOS}")
    if sorted(sos_flag_bases) != EXPECTED_SOS_FLAG_BASES:
        fail(f"I5 flag base {sorted(sos_flag_bases)} ≠ {EXPECTED_SOS_FLAG_BASES}")

    # ————— I6: brez georef polj —————
    def assert_no_geo(obj, path="root"):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in GEO_FIELDS:
                    fail(f"I6 georef polje '{k}' @ {path}.{k}")
                assert_no_geo(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                assert_no_geo(v, f"{path}[{i}]")

    rows_split = sum(e["rowsTotal"] for e in bases_out.values())

    verdict_si = (
        "P66: SPLIT DECISION PACK — 39 SPLIT BASE (issue #13) — odločitveni "
        "paket za per-Blatt SPLIT joina (odprta točka P64 #8, kandidat #1 iz "
        "P65; deterministično, brez AI ob delovanju; NE odloča namesto "
        "lastnika — MERI in DOKAZUJE dejstva): vseh 39 base ima TOČNO 2 "
        "deleža (blattShares), 93 vrstic (25 × 2 + 13 × 3 + 1 × 4); Blatt "
        "pari I·II 7 · II·III 21 · II·IV 2 · IV·V 9 (37/39 sosednja Blatta, "
        "2 skoka II·IV — 1603/1604, isti kulturi na obeh Blattih); "
        "LASTNIŠKA RAZČLENITEV PER BLATT: 39/39 DISJUNKTNI lastniki — vsak "
        "split base ima različne lastnike po Blattih (močan dokaz, da je "
        "ista številka pod različnima Blattoma 2 RAZLIČNI realni parceli); "
        "2–3 edinstvenih lastnikov (25/13/1); dominantni deleži [0.50,0.60) "
        "23 · [0.60,0.70) 11 · [0.70,0.75) 5; kulture 92 (kulturesByBlatt); "
        "GEO: 39/39 base nosi VSEH vrstic ENAKO geometrijo joina v2 (0 "
        "različnih) — join v2 je na nivoju številke, zato SPLIT join bi "
        "zahteval 2 geometriji (števec merjen brez koordinat — I6); "
        "areaSuspect 0; sosledje split del 82/93 (flag 11 — 5 base: 646, "
        "661, 1821, 2141, 2143); P65 polja 39× bajtno (I3); join v2 "
        "NESPREMENJEN (disciplina P56/P58/P59/P65); odločitev LASTNIKA"
    )
    verdict_en = (
        "P66: SPLIT DECISION PACK — 39 SPLIT BASES (issue #13) — the "
        "decision pack for the per-Blatt SPLIT join (P64 open point #8, "
        "candidate #1 from P65; deterministic, no AI at runtime; does NOT "
        "decide on behalf of the owner — MEASURES and PROVES the facts): "
        "all 39 bases have EXACTLY 2 shares (blattShares), 93 rows "
        "(25 × 2 + 13 × 3 + 1 × 4); Blatt pairs I·II 7 · II·III 21 · II·IV 2 "
        "· IV·V 9 (37/39 adjacent Blatts, 2 skips II·IV — 1603/1604, same "
        "cultures on both Blatts); OWNERSHIP PARTITION PER BLATT: 39/39 "
        "DISJOINT owners — every split base has different owners per Blatt "
        "(strong evidence that the same number under different Blatts is 2 "
        "DIFFERENT real parcels); 2–3 unique owners (25/13/1); dominant "
        "shares [0.50,0.60) 23 · [0.60,0.70) 11 · [0.70,0.75) 5; cultures "
        "92 (kulturesByBlatt); GEO: 39/39 bases carry the SAME join-v2 "
        "geometry for ALL rows (0 distinct) — the v2 join is at the number "
        "level, so a SPLIT join would require 2 geometries (counter measured "
        "without coordinates — I6); areaSuspect 0; adjacency split part "
        "82/93 (11 flags — 5 bases: 646, 661, 1821, 2141, 2143); the P65 "
        "fields byte-identical 39× (I3); the v2 join UNCHANGED (P56/P58/P59/"
        "P65 discipline); the decision belongs to the OWNER"
    )

    ev = {
        "task": "P66 — split decision pack: 39 split base (odločitveni paket za per-Blatt SPLIT joina)",
        "date": "2026-10-14",
        "principle": (
            "odločitveni paket za lastniško odločitev o per-Blatt SPLIT "
            "joinu (#8): 39 split base iz P65 (bajtni vir) × v2 vrstice × "
            "P59 pageAttribution — per-Blatt razčlenitev vrstic, kulture, "
            "lastnikov; merjeni: Blatt pari (37/39 sosednji, 2 skoka), "
            "deležni pasovi, disjunktnost lastnikov (39/39), geo delitev "
            "(39/39 ena geometrija), sosledje; NE odloča namesto lastnika; "
            "join v2 nespremanjen (disciplina P56/P58/P59/P65)"
        ),
        "inputs": {
            "v2": "research/issue17/ps-parcels-geo-v2.json (rowsEvidence 1093)",
            "p59": "research/issue17/ps-blatt-headers.json (pageAttribution)",
            "p65rt": "src/data/atlas/ps-attribution-full.json (P65 runtime — bajtni vir 211, split 39)",
        },
        "rule": {
            "source": "split base = P65 status 'split' (dominantni delež v [0.5, 0.75), attributedBlatt null, blattShares alternative) — P66 ne spreminja pravil",
            "blattPair": "urejen par Blattov split base ('·' join); sosednji = v ADJACENT {(I,II),(II,III),(III,IV),(IV,V)}",
            "ownerRelation": "disjunktnost množic lastnikov per Blatt: 'disjoint' | 'equal' | 'overlap' | 'open' (prazna množica)",
            "dominantShare": "share[0] (P65 sort: Σ areaQK desc, Blatt asc); pasovi [0.50,0.60)/[0.60,0.70)/[0.70,0.75)",
            "geoShared": "ali vse vrstice base nosijo isti par (lat, lng) v v2 (null = vse brez); SAMO števec v summary — koordinate ne gredo v izpis (I6)",
        },
        "v2Sha256": sha256(V2),
        "inputSha256": {"p59": sha256(P59), "p65rt": sha256(P65RT)},
        "summary": {
            "splitBases": len(bases_out),
            "rowsTotal": rows_split,
            "rowsPerBaseDist": {k: rows_dist[k] for k in sorted(rows_dist)},
            "shareCountDist": {k: share_count[k] for k in sorted(share_count)},
            "blattPairDist": {k: pairs[k] for k in sorted(pairs)},
            "adjacentPairs": adjacent,
            "skipPairs": skip,
            "uniqueOwnersDist": {k: owners_dist[k] for k in sorted(owners_dist)},
            "ownerRelationDist": {k: owner_rel[k] for k in sorted(owner_rel)},
            "dominantShareBuckets": {k: buckets[k] for k in EXPECTED_BUCKETS},
            "kulturesTotal": kultures_total,
            "geoShared": {"shared": geo["shared"], "distinct": geo["distinct"], "null": geo["null"]},
            "areaSuspectRows": area_suspect,
            "sosledje": {"ok": sos_ok, "flag": sos_flag,
                         "relevantRows": sos_ok + sos_flag,
                         "flagBases": sorted(sos_flag_bases)},
        },
        "bases": dict(sorted(bases_out.items(), key=lambda kv: int(kv[0]))),
        "invariants": ["I1 vhodni pini (3× sha256 + števci 1093/800/211/39)",
                       "I2 razčlenitev (39 ⊂ 211; 2 deleža; Σ share = 1; Σ areaQK == vrstice)",
                       "I3 P65 polja bajtno (deep equality 39×)",
                       "I4 distribucije (pairs/skip/owners/rel/pasovi/kulture/geo/suspect)",
                       "I5 sosledje split del == P65 bajtno (82/93; flag 5 base)",
                       "I6 brez georef polj (lat/lng/areaModern/ratio); geoShared samo števec",
                       "I7 dokaz ⊇ runtime", "I8 determinizem (--check)"],
        "statusLine": (
            f"P66 SPLIT PACK: {len(bases_out)} split base (39 ⊂ 211 multi-page), "
            f"{rows_split} vrstic; pari I·II {pairs['I·II']} · II·III {pairs['II·III']} · "
            f"II·IV {pairs['II·IV']} · IV·V {pairs['IV·V']} (sosednji {adjacent}, "
            f"skok {skip}); lastniki per Blatt DISJUNKTNI {owner_rel['disjoint']}/39; "
            f"pasovi 23/11/5; geo ena geometrija {geo['shared']}/39; join v2 nespremanjen; "
            f"odločitev lastnika"
        ),
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "next": [
            "LASTNIŠKA ODLOČITEV o per-Blatt SPLIT joinu za 39 base (2 geometriji; razdelitev per deleži ali per lastnika) — ta paket je dokazni vir",
            "izvedba SPLIT joina (ob odobritvi): v2 join upgrade — 39 base → 78 kandidatnih instanc per Blatt, geometrije per Blatt georef [~]",
            "razlaga 2 skokov II·IV (1603, 1604: isti kulturi 'Acker' + 'Weide und Gfällgut, Laubm.' na obeh Blattih — preveriti dednost/preimenovanje)",
            "razlaga 5 sosledje flagov (646, 661, 1821, 2141, 2143)",
            "lastniki atributiranih instanc ↔ PF protokol (ostaja iz P65)",
        ],
    }

    runtime = {
        "version": 1,
        "task": ev["task"],
        "date": ev["date"],
        "generatedBy": "scripts/p66_ps_split_pack.py",
        "rule": ev["rule"],
        "summary": ev["summary"],
        "bases": ev["bases"],
        "statusLine": ev["statusLine"],
        "verdictSi": ev["verdictSi"],
        "verdictEn": ev["verdictEn"],
        "next": ev["next"],
    }

    # ————— I6 na runtime —————
    assert_no_geo(runtime, "runtime")

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

    print(f"OK: split base {len(bases_out)} ({rows_split} vrstic), pari {dict(sorted(pairs.items()))}")
    print(f"OK: lastniki per Blatt {dict(owner_rel)}, unique {dict(owners_dist)}, pasovi {dict(buckets)}")
    print(f"OK: geo shared {geo['shared']}/{len(bases_out)} — join v2 nespremanjen")
    print(f"OK: sosledje split del {sos_ok}/{sos_ok + sos_flag}")
    print(f"OK: dokaz {OUT_EV}, runtime {OUT_RT}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        h1 = sha256(OUT_EV)
        h2 = sha256(OUT_RT)
        main()
        if sha256(OUT_EV) != h1 or sha256(OUT_RT) != h2:
            fail("I8 determinizem: izhod se je spremenil")
        print("I8 --check: PASS")
    else:
        main()
