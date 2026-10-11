#!/usr/bin/env python3
"""P44: agregacija 1. kroga — kulture, razredi, površine, vsote; uskladitev s PV."""
import json, re, glob, collections

RAW_DIR = "research/issue11/pz-raw"

# PV cilji (research.ts PV_LAND_USE_1825)
PV = {
    "Gemüse Gärten": (2, 123),
    "Wein Gärten": (7, 665),
    "Wiesen": (76, 1480),
    "Wiesen mit Obstbäumen": (12, 328),
    "Weiden": (636, 263),
    "Aecker": (413, 870),
    "Oedungen": (1, 476),
    "Flüsse oder Bäche": (21, 142),
    "Weg Parzellen": (46, 1127),
    "Bau Parzellen": (4, 889),
}

def norm_culture(c):
    if not c:
        return "?"
    c = c.lower()
    if "acker" in c or "äcker" in c: return "Ackerland"
    if "wiese" in c: return "Wiesen"
    if "wein" in c: return "Weingärten"
    if "gemü" in c or "gemus" in c or "müß" in c or "muß" in c: return "Gärten (Gemüse)"
    if "garten" in c or "gärten" in c: return "Gärten (ostalo)"
    if "hutweide" in c or "weide" in c: return "Weiden/Hutweide"
    if "bau" in c: return "Bau-Area"
    if "unbenütz" in c or "unbenutz" in c or "unbebaubar" in c or "oed" in c or "öd" in c: return "Unbenützte"
    if "fluss" in c or "bach" in c: return "Flüsse"
    if "weg" in c: return "Wege"
    if "vieh" in c or "titelblatt" in c or "naslovn" in c: return "(neco kulture)" if "vieh" in c else "_meta"
    return f"_drugo:{c[:30]}"

def parse_num(v):
    if v is None: return None
    s = str(v).strip().replace(",", ".")
    if s in ("", "null", "[?]", "?"): return None
    m = re.match(r"^-?\d+(?:\.\d+)?$", s)
    return float(s) if m else None

files = sorted(glob.glob(f"{RAW_DIR}/pz-*.json"))
by_culture = collections.defaultdict(list)   # culture -> list of row dicts
page_rows = {}
for f in files:
    d = json.load(open(f))
    page = d["page"]
    rows_n = 0
    if not d["parseOk"]:
        continue
    for sec in (d["structured"].get("sections") or []):
        cult = norm_culture(sec.get("culture"))
        for r in (sec.get("rows") or []):
            rows_n += 1
            j = parse_num(r.get("areaJoch"))
            k = parse_num(r.get("areaKlafter"))
            if j is None and k is None:
                continue
            by_culture[cult].append({
                "page": page, "label": r.get("label"), "joch": j, "klafter": k,
                "values": r.get("values"), "conf": r.get("confidence"),
            })
    page_rows[page] = rows_n

print("=== VRSTICE S POVRSINO po kulturah (1. krog) ===")
for cult in sorted(by_culture):
    rows = by_culture[cult]
    sj = sum(r["joch"] for r in rows if r["joch"])
    sk = sum(r["klafter"] for r in rows if r["klafter"])
    print(f"\n{cult}: {len(rows)} vrstic s površino, vsota {sj:.0f} j {sk:.0f} kl")
    for r in rows[:8]:
        print(f"   p{r['page']:>2} {str(r['label'])[:28]:28} {r['joch']} j {r['klafter']} kl  [{r['conf']}] {str(r['values'])[:50]}")

print("\n=== PRIMERJAVA S PV (kjer ima PZ ekvivalent) ===")
map_pv = {
    "Ackerland": "Aecker", "Wiesen": "Wiesen", "Weiden/Hutweide": "Weiden",
    "Weingärten": "Wein Gärten", "Gärten (Gemüse)": "Gemüse Gärten", "Bau-Area": "Bau Parzellen",
    "Unbenützte": "Oedungen", "Flüsse": "Flüsse oder Bäche", "Wege": "Weg Parzellen",
}
for cult, pv_name in map_pv.items():
    rows = by_culture.get(cult, [])
    sj = sum(r["joch"] for r in rows if r["joch"])
    sk = sum(r["klafter"] for r in rows if r["klafter"])
    pj, pk = PV[pv_name]
    dj = sj - pj
    print(f"  {cult:18} PZ vsota {sj:6.0f} j {sk:5.0f} kl  |  PV {pv_name}: {pj} j {pk} kl  |  Δ {dj:+.0f} joch")

print("\n=== STRANI Z NAJVEČ VRSTICAMI ===")
for p, n in sorted(page_rows.items(), key=lambda x: -x[1])[:12]:
    print(f"  p{p}: {n} vrstic")
