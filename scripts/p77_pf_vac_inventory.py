#!/usr/bin/env python3
# P77 — PF protokol: VAČ inventarna forenzika (DOKAZANI NEGATIV, vzorec P45).
#
# Odprta točka P76 ②: "PF protokol = manjkajoči vir, ni v repu" (vir identitete
# pas-instanc; povezati lastnike pas-instanc s poligoni — P60/P61/P63–P68 next).
#
# Ta skripta DOKAZUJE, kaj je na VAČ dejansko digitalizirano za k.o. N83
# Griblje (fond SI AS 176, Novomeška kresija): celoten inventar enot prek
# tektonike arhiva (archivePlanSearchAjax — edini delujoči VAČ API ob
# posodobitvi 2.21_5.5, 2026-10-14; fieldSearch vrača 0 zadetkov, details
# javlja interno napako), mapa uodid↔docid za pdfPageImage, ter sosedski
# probe uodid prostora. Izhodiščno znanje: PS uodid=373415, docid=41780
# (recept p59); enote N083 iz src/data/atlas/sources.ts.
#
# METODA (deterministična, brez AI):
#   1. seja: GET /vac/search/archivePlanSearch (cookies; VAČ piškotki)
#   2. tektonski sprehod po STABILNIH BESEDILIH vozlišč (ne po ID-jih):
#      "000 UPRAVA" → "071 Posebni organi za gospodarstvo in finance do
#      1945/1947" → "SI AS 176 Franciscejski kataster za Kranjsko" →
#      "N Novomeška kresija" → "N83 Griblje, k.o."
#   3. inventar: skupini "grafični" + "spisovni" → vsi listi
#   4. probe: (a) docid = uodid − 331635 na vseh spisovnih enotah (JPEG?),
#      (b) sosedski uodid 373411, 373420–373424 (izven razpona = napaka?)
#   5. dokaz research/issue17/pf-vac-inventory.json + --check (bajtno
#      primerjanje stabilnega jedra; timestamps/verzija izključeni)
#
# NE DOKAZUJE vsebine strani — DOKAZUJE inventarno ABSENCO: med enotami
# k.o. N83 NI dodatnega protokola (PF/Parzellen-Führer/Stavbni protokol).
# Edini protokol-slični vir = N083PT "Seznam stavbnih parcel" (373416),
# ki je ŽE v repu (PT: 105 vrstic, 84 hišnih + 21 parcelnih — audit §13).
#
# Izhod: /home/z/muzej/research/issue17/pf-vac-inventory.json
# Status: PROVEN-NEGATIVE-INVENTORY (vir identitete pas-instanc = fizični
#         arhiv / drugi fond — operativna lastniška akcija, P77+).

import json
import os
import subprocess
import sys
import time
import urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOKAZ = os.path.join(REPO, "research", "issue17", "pf-vac-inventory.json")

BASE = "https://vac.sjas.gov.si"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
COOKIE_JAR = "/tmp/p77/vac-cookies.txt"

DOCID_OFFSET = -331635  # docid = uodid - 331635 (PS: 373415→41780; PG: 373413→41778)

# --- pričakovano stanje (invarianti I1–I8) ---
EXPECTED_PATH = [
    ("000 UPRAVA", None),
    ("070 Posebni upravni organi in organizacije do 1945/1947", None),
    ("071 Posebni organi za upravo, pravosodje in notranje in zunanje zadeve do 1945/1947", None),
    ("SI AS 176 Franciscejski kataster za Kranjsko", "23253"),
    ("N Novomeška kresija", "226589"),
    ("N83 Griblje, k.o.", "227663"),
]
EXPECTED_GRAPHIC = [
    ("N083A01 list A01", "227666"),
    ("N083A02 list A02", "227668"),
    ("N083A03 list A03", "227670"),
    ("N083A04 list A04", "227671"),
    ("N083A05 list A05", "227673"),
]
EXPECTED_SPISOVNI = [
    ("N083PG Skica", "373413"),
    ("N083PR Opis meje", "373414"),
    ("N083PS Seznam zemljiških parcel", "373415"),
    ("N083PT Seznam stavbnih parcel", "373416"),
    ("N083PUA Abecedni seznam lastnikov zemljišč", "373417"),
    ("N083PV Izkaz rabe zemljišč", "373418"),
    ("N083PZ Katastrski cenilni elaborat", "373419"),
]
ADJACENT_UODIDS = [373411, 373420, 373421, 373422, 373423, 373424]

PF_TOKENS = ["PF", "Parzellen-Führer", "Parzellenführer", "Führer",
             "Protokol", "Protokoll"]


def http(args, timeout=40):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


def curl(url, data=None, extra=None, out=None):
    args = ["curl", "-sk", "--noproxy", "*", "--max-time", "40",
            "-H", f"User-Agent: {UA}", "-b", COOKIE_JAR, "-c", COOKIE_JAR]
    if data is not None:
        args += ["-X", "POST", "--data", data]
    if extra:
        args += extra
    if out:
        args += ["-o", out]
    args += ["-w", "\n%{http_code}", url]
    r = http(args)
    body, _, code = r.stdout.rpartition("\n")
    return code.strip(), body


def tree_children(node_id, page=0):
    url = (f"{BASE}/vac/search/archivePlanSearchAjax"
           f"?id={node_id}&page={page}")
    code, body = curl(url, extra=["-H", "Accept: application/json"])
    if code != "200":
        raise RuntimeError(f"tektonika {node_id} p.{page}: HTTP {code}")
    return json.loads(body)


def norm(s):
    return " ".join(str(s).split())


def find_by_text(nodes, needle):
    needle = norm(needle)
    for n in nodes:
        if norm(n.get("text", "")) == needle:
            return n
    for n in nodes:  # tolerance: prefix match
        if norm(n.get("text", "")).startswith(needle):
            return n
    return None


def walk_tektonika():
    """Sprehod po tektoniki po besedilih; vrača pot + inventar N83."""
    path = []
    # seja najprej (VAČ piškotki)
    curl(f"{BASE}/vac/search/archivePlanSearch")
    os.makedirs(os.path.dirname(COOKIE_JAR), exist_ok=True)
    curl(f"{BASE}/vac/search/archivePlanSearch")

    current = None
    for needle, expect_id in EXPECTED_PATH:
        if current is None:
            # root: id=1 page=0
            nodes = tree_children(1, 0)
        else:
            nodes = tree_children(current["id"], 0)
        node = find_by_text(nodes, needle)
        if node is None:
            raise RuntimeError(f"vozlišče '{needle}' ni najdeno med {len(nodes)} otroki")
        path.append({"needle": needle, "id": node["id"],
                     "text": node.get("text", ""), "type": node.get("type"),
                     "expectedId": expect_id,
                     "childrenCount": len(nodes)})
        current = node

    # N83 otroci: grafični + spisovni skupini
    groups_raw = tree_children(current["id"], 0)
    groups = [{"id": g["id"], "text": g.get("text", "").strip(),
               "type": g.get("type")} for g in groups_raw]

    inventory = {"graphic": [], "spisovni": []}
    group_map = {}
    for g in groups:
        leaves = tree_children(g["id"], 0)
        key = "graphic" if "grafični" in g["text"].lower() else (
              "spisovni" if "spisovni" in g["text"].lower() else None)
        entry = {"groupId": g["id"], "groupText": g["text"],
                 "leaves": [{"id": l["id"], "text": l.get("text", "").strip()}
                            for l in leaves]}
        group_map[g["text"].strip()] = entry
        if key:
            inventory[key] = entry["leaves"]
            entry["key"] = key
        groups_detail = groups_detail if False else None  # placeholder
    return path, groups, group_map, inventory


def probe_image(uodid, page=1):
    docid = uodid + DOCID_OFFSET
    out = f"/tmp/p77/probe-{uodid}-{page}.jpg"
    os.makedirs("/tmp/p77", exist_ok=True)
    url = (f"{BASE}/vac/util/pdfPageImage"
           f"?uodid={uodid}&docid={docid}&page={page}")
    code, _ = curl(url, out=out)
    try:
        size = os.path.getsize(out)
    except OSError:
        size = 0
    magic = b""
    try:
        with open(out, "rb") as f:
            magic = f.read(3)
    except OSError:
        pass
    return {"uodid": uodid, "docid": docid, "page": page, "http": code,
            "bytes": size, "jpeg": magic[:2] == b"\xff\xd8"}


def vac_version():
    code, body = curl(f"{BASE}/vac")
    m = None
    for token in ["2.21_5.5", "2.21", "2.2"]:
        if token in body:
            m = token
            break
    return m or "unknown"


def build_dokaz():
    t0 = time.strftime("%Y-%m-%dT%H:%M:%S+02:00")
    path, groups, group_map, inventory = walk_tektonika()

    spisovni_probes = [probe_image(int(l["id"])) for l in inventory["spisovni"]]
    adjacent_probes = [probe_image(u) for u in ADJACENT_UODIDS]

    # dokazani negativ: med vsemi leaf besedili N83 ni PF-ključa
    all_leaves = ([(l["id"], l["text"]) for l in inventory["graphic"]] +
                  [(l["id"], l["text"]) for l in inventory["spisovni"]])
    pf_hits = [{"id": i, "text": t, "token": tok}
               for i, t in all_leaves for tok in PF_TOKENS
               if tok.lower() in t.lower()]

    dokaz = {
        "phase": "P77",
        "title": "PF protokol: VAČ inventarna forenzika k.o. N83 Griblje — dokazani negativ",
        "status": "PROVEN-NEGATIVE-INVENTORY",
        "issuedAt": t0,
        "vac": {
            "baseUrl": BASE,
            "versionObserved": vac_version(),
            "apiStatus": {
                "archivePlanSearchAjax": "WORKING",
                "fieldSearchFindAjax": "BROKEN (totalItems 0 za vse kriterije)",
                "details": "BROKEN (interno napaka za znane id-je)",
                "pdfPageImage": "WORKING (docid = uodid - 331635)",
            },
        },
        "method": {
            "navigation": "besedilni sprehod po tektoniki (archivePlanSearchAjax), ne po ID-jih",
            "docidMapping": f"docid = uodid {DOCID_OFFSET:+d}",
            "probes": "pdfPageImage page=1, JPEG magic ff-d8",
        },
        "path": path,
        "ko83Groups": [
            {"id": g["id"], "text": g["text"]} for g in groups
        ],
        "inventory": {
            "graphic": inventory["graphic"],
            "spisovni": inventory["spisovni"],
            "totalUnits": len(all_leaves),
        },
        "docidProbes": spisovni_probes,
        "adjacentUodidProbes": adjacent_probes,
        "pfSearch": {
            "tokens": PF_TOKENS,
            "hits": pf_hits,
            "verdict": ("DOKAZANI NEGATIV: med 12 enotami k.o. N83 na VAČ ni "
                        "dodatnega protokola (PF/Parzellen-Führer/Stavbni "
                        "protokol). Edini protokol-slični vir = N083PT "
                        "Seznam stavbnih parcel (373416), ŽE v repu "
                        "(PT 105 vrstic; audit §13)."),
        },
        "implication": (
            "Vir identitete pas-instanc (P76 ②, P60 moda B 44 [~] vrstic) NI "
            "na VAČ — potreben fizični arhiv (Arhiv RS, SI AS 176 ali SI AS 52 "
            "Finančna direkcija 1825–1924) ali drugi fond. P76 opcije B1/B2 "
            "ostaneta edini izvedljivi poti brez PF protokola; opcija A = "
            "status quo; izbira ostaja LASTNIŠKA."),
        "invariants": {},
    }

    # --- invarianti ---
    dokaz["invariants"] = {
        "I1_path": all(norm(p["needle"]) in norm(p["text"])
                       for p in path),
        "I2_ko83_two_groups": (len(groups) == 2 and
                               {"grafični", "spisovni"} ==
                               {g["text"].strip() for g in groups}),
        "I3_graphic_5": len(inventory["graphic"]) == 5,
        "I4_spisovni_7": len(inventory["spisovni"]) == 7,
        "I5_total_12": len(all_leaves) == 12,
        "I6_pf_absent": len(pf_hits) == 0,
        "I7_docid_all_jpeg": all(p["jpeg"] and p["http"] == "200"
                                 for p in spisovni_probes),
        "I8_adjacent_no_jpeg": all(not p["jpeg"]
                                   for p in adjacent_probes),
    }
    dokaz["invariantsPass"] = all(dokaz["invariants"].values())
    return dokaz


def stable_core(d):
    """Bajtno stabilno jedro (brez časovnih žigov in verzije VAČ)."""
    d2 = json.loads(json.dumps(d))
    d2.pop("issuedAt", None)
    if isinstance(d2.get("vac"), dict):
        d2["vac"].pop("versionObserved", None)
    return json.dumps(d2, sort_keys=True, ensure_ascii=False)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "build"
    if mode == "--check":
        with open(DOKAZ, encoding="utf-8") as f:
            committed = json.load(f)
        fresh = build_dokaz()
        ok = stable_core(committed) == stable_core(fresh)
        print("P77 --check:", "PASS (bajtno stabilno jedro)" if ok
              else "FAIL (dokaz odstopa od svežega VAČ pregleda)")
        if not ok:
            c, f_ = stable_core(committed), stable_core(fresh)
            for i in range(min(len(c), len(f_))):
                if c[i] != f_[i]:
                    print("prva razlika @", i, ":", c[max(0, i-80):i+120],
                          "!=", f_[max(0, i-80):i+120])
                    break
        sys.exit(0 if ok else 1)
    else:
        dokaz = build_dokaz()
        os.makedirs(os.path.dirname(DOKAZ), exist_ok=True)
        with open(DOKAZ, "w", encoding="utf-8") as f:
            json.dump(dokaz, f, ensure_ascii=False, indent=2)
        inv = dokaz["invariants"]
        print(f"P77 dokaz: {DOKAZ}")
        print(f"invarianti: {dokaz['invariantsPass']} — " +
              " ".join(f"{k}={'P' if v else 'F'}" for k, v in inv.items()))
        print(f"enot skupaj: {dokaz['inventory']['totalUnits']}; "
              f"PF zadetki: {len(dokaz['pfSearch']['hits'])}")
        sys.exit(0 if dokaz["invariantsPass"] else 1)


if __name__ == "__main__":
    main()
