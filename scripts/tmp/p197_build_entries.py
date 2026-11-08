#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P197 — agregacija 9 VLM-branj → 71 vsebinskih vpisov za leto 1880
(mrliška 04106, Pag = sken − 6, md5+vizualno validirano!).

Struktura dokazane preslikave:
  s164: z62,z63 (1879-tail) + MEJA-'1880'-SPLIT-GUTTER (36.-POTRDITEV!) + z1–z7
        (VLM-vrste 3–9 → z1..z7; VLM-VRSTA-3-mel-NULL = z1 Karavanič!)
  s165: z8–z18 (leto-glava '1880 Feber' — VLM-'1859' ZAVRJEN-KROP!)
  s166: z19–z30 · s167: z31–z41 · s168: z42–z52
  s169: z53, z54, z56–z62 — ★ z55 = IZPUŠČENA-ŠTEVILKA (rdeči-margin-KROP:
        53,54,56,57,58,59,60,61,62!) → VLM-vrste 3–9 = +1-shift (z56..z62)
  s170: z63–z71 (leto-glava '1880 Novobr' — VLM-'1839' ZAVRJEN-KROP!)
  s171: z72-tail (reuse P196 s171.json vrsta-1: Valčič-Vranoviče-72J!) + MEJA-1880/81

KROP-izreki (agent-oči, 1.7×-zoom): z10-vas=GRIBLJE (VLM-'Krive' ZAVRJEN),
z66-starost=1¾ (VLM-1½ ZAVRJEN), z52-h47 JASNO, z19-h39[~29], z10-ime=Knuel[~Kuncelj],
z19-ime=Simec[~Timec-VLM], z1-ime=Staravinič[~Karavanič-VLM]."""
import json, re
from pathlib import Path

VLM = Path("/tmp/p197/vlm-page")
P196 = Path("/tmp/p196/vlm-page/s171.json")
OUT = Path("/tmp/p197/entries_raw.json")

KROP = {
    # (sken, zap): {polje: popravek} — agent-oči-izreki s crop-zoomi
    (164, 1): {"ime": "Peter Staravinič [~Karavanič/Maravanič-VLM — KROP: 'St'-ligatura]",
               "krop": "s164-meja-split"},
    (164, 2): {"ime": "Anna Huore [~Huoe/Thure-VLM]", "krop": "s164-griblje-z2-z4 + leva-cela"},
    (165, 10): {"vas": "Griblje", "vas_vlm_zavrnjen": "Krive [~Griblje?] — ZAVRJEN (KROP: 'Griblje.' jasno!)",
                "ime": "Katharina Knuel [~Kuncelj-VLM]", "krop": "s165-z10-kuncelj"},
    (166, 19): {"ime": "Anna Simec [~Timec-VLM — KROP: 'S'-začetnica jasna; ŠIMEC-nit!]",
                "hisna": "39 [~29 — 3/9-KURRENT-zmeda, KROP]", "krop": "s166-z19-z22"},
    (168, 52): {"hisna": "47 (KROP: '47.' jasno)", "krop": "s168-z52-klobucar"},
    (170, 66): {"starost": "1¾ leta (VLM-'1½ [~1J]' ZAVRJEN — KROP: '1¾ Jähr.' jasno)",
                "krop": "s170-griblje-z65-z66"},
}

MONTHS = {"Jänner": 1, "Feber": 2, "Februar": 2, "März": 3, "April": 4, "Mai": 5,
          "Juni": 6, "July": 7, "Juli": 7, "August": 8, "September": 9, "October": 10,
          "November": 11, "Dezember": 12}


def month_no(mes):
    if not mes:
        return None
    m = str(mes).strip()
    for k, v in MONTHS.items():
        if m.lower().startswith(k[:5].lower()):
            return v
    return None


def base(entry_sken, zap, r, leto=1880):
    e = {
        "leto": leto,
        "sken": entry_sken,
        "pag": entry_sken - 6,
        "zap": zap,
        "mesec": (r.get("mesec") or "").strip() or None,
        "mesec_no": month_no(r.get("mesec")),
        "smrt": (r.get("smrt") or "").strip() or None,
        "pokop": (r.get("pokop") or "").strip() or None,
        "vas": (r.get("vas") or "").strip() or None,
        "hisna": (str(r.get("hisna")) if r.get("hisna") is not None else "").strip() or None,
        "ime": (r.get("ime") or "").strip() or None,
        "stan": (r.get("stan") or "").strip() or None,
        "starost": (r.get("starost") or "").strip() or None,
        "bolezen": (r.get("bolezen") or "").strip() or None,
        "previden": (str(r.get("previden")) if r.get("previden") is not None else "").strip() or None,
        "duhovnik": (r.get("duhovnik") or "").strip() or None,
        "opomba": (r.get("opomba") or "").strip() or None,
        "zap_raw": (str(r.get("zaporedna")) if r.get("zaporedna") is not None else "").strip() or None,
        "krop": None,
    }
    return e


entries = []

# ——— s164: VLM-vrste 1–2 = 1879-tail (z62, z63) — NE gredo v 1880-nabor (samo-dokaz)! ———
d = json.load(open(VLM / "s164.json"))
rows = d["vrstice"]
tail_1879 = [base(164, f"z{62 + i}-tail1879", r, leto=1879) for i, r in enumerate(rows[:2])]
tail_1879[1]["opomba"] = "smrt 31.12.1879 → pokop 1.1.1880 (Jänner-vrstica!) — '1879-ima-63-vpisov'"
# VLM-vrsta 3 = zap-null → z1 (Karavanič; VLM jo je spojil z MEJA-markerjem!)
e = base(164, 1, rows[2]); e["zap_raw"] = "null→z1 (VLM-merge-z-MEJA!)"
entries.append(e)
# VLM-vrste 4–9 = z2–z7 (VLM '1[~2]'..'6[~7]' — [~+1]-sumi bili PRAVILNI!)
for i, r in enumerate(rows[3:9]):
    e = base(164, 2 + i, r); e["zap_raw"] = r.get("zaporedna")
    entries.append(e)

# ——— s165: z8–z18 (leto-KROP: '1880 Feber' glava!) ———
d = json.load(open(VLM / "s165.json"))
for r in d["vrstice"]:
    entries.append(base(165, int(r["zaporedna"]), r))

# ——— s166–s168: z19–z30, z31–z41, z42–z52 ———
for s, z0 in [(166, 19), (167, 31), (168, 42)]:
    d = json.load(open(VLM / f"s{s}.json"))
    for i, r in enumerate(d["vrstice"]):
        entries.append(base(s, z0 + i, r))

# ——— s169: z53, z54, potem +1-shift (VLM z55..z61 → realno z56..z62; z55-PRESKOK!) ———
d = json.load(open(VLM / "s169.json"))
rows = d["vrstice"]
for i, r in enumerate(rows[:2]):
    entries.append(base(169, 53 + i, r))
for i, r in enumerate(rows[2:]):
    e = base(169, 56 + i, r)
    e["zap_raw"] = f"{r.get('zaporedna')}→z{56 + i} (+1-shift — z55-PRESKOK!)"
    entries.append(e)

# ——— s170: z63–z71 (leto-KROP: '1880 Novobr' glava!) ———
d = json.load(open(VLM / "s170.json"))
for i, r in enumerate(d["vrstice"]):
    entries.append(base(170, 63 + i, r))

# ——— s171-tail: z72 (P196-reuse!) ———
d = json.load(open(P196))
r72 = d["vrstice"][0]  # vrsta-1 = z72 Dezember Vranoviče Valčič 72J Wassersucht
e = base(171, 72, r72)
e["zap_raw"] = "72 (P196-reuse; KROP-POTRJENO-s171: 72-ne-92 — γ-7!)"
e["opomba"] = "P196-s171-tail; MEJA-1880/81 = '18/81'-SPLIT za to vrstico (35.-POTRDITEV!)"
entries.append(e)

# ——— KROP-injekcija (PREPIŠE glavna polja; zavrnjene-VLM-branje v vlm_zavrnjeno!) ———
for e in entries:
    key = (e["sken"], e["zap"]) if isinstance(e["zap"], int) else None
    if key and key in KROP:
        e.setdefault("vlm_zavrnjeno", {})
        for k, v in KROP[key].items():
            if k.endswith("_zavrnjen"):
                e["vlm_zavrnjeno"][k.replace("_vlm_zavrnjen", "")] = v
                continue
            if k in e and e[k] and e[k] != v:
                e["vlm_zavrnjeno"][k] = e[k]
            e[k] = v

# ——— 1879-tail ločeno (dokaz, ne-vpisi) ———
out = {
    "meta": {
        "leto": 1880,
        "knjiga": "04106",
        "preslikava": "pag = sken − 6 (md5-validirano-s171 + vizualno Pag.158/159/163/164!)",
        "okvir": "s164(Pag.158: z62,z63-1879-tail + MEJA-'1880'-SPLIT-GUTTER + z1–z7) → s171-tail(z72) + MEJA-1880/81",
        "meja_1879_80": "s164 mid-page '1 8'|'8 0' SPLIT-ČEZ-RAZPON = 36.-POTRDITEV-invariante (P194-tehnika-#9!)",
        "restart": "63→1 na s164 (rdeči-margin-KROP: 62,63,1,2,3,4,5,6,7!)",
        "anomalija_številčenja": "★ z55 = IZPUŠČENA-ŠTEVILKA (s169 rdeči-margin: 53,54,56..62 — pisar-preskok; cf. P196-z8-DUPLIKAT!)",
        "leto_popravki": "VLM-'1859'(s165)/'1839'(s170) = KURRENT-misread — KROP: '1880 Feber' + '1880 Novobr' glavi!",
        "krop_izreki": 10,
        "duhovniki_krop": "Jančar (coop.→v.kaplan→VRD-Pfarrer/Priester/Pastor — naraščajoči-naslovi!) + Dovgan (z10-Griblje! + z62?)",
    },
    "tail_1879": tail_1879,
    "entries": entries,
}

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

# ——— statistika ———
n = len(entries)
grib = [e for e in entries if e["vas"] and "gribl" in e["vas"].lower()]
zaps = [e["zap"] for e in entries]
print(f"VPISEK: {n} (pričakovano 71 = z1–z72 minus z55-preskok!)")
print(f"ZAP: min={min(z for z in zaps if isinstance(z, int))} max={max(z for z in zaps if isinstance(z, int))}")
print(f"GRIBLJE: {len(grib)}")
for e in grib:
    print(f"  z{e['zap']}: h{e['hisna']} {e['ime']} | {e['starost']} | {e['bolezen']} | {e['mesec']} {e['smrt']}|{e['pokop']} | {e['duhovnik']}")
from collections import Counter
print("BOLEZNI:", dict(Counter((e["bolezen"] or "?").split()[0].rstrip('.,') for e in entries).most_common(12)))
print("MESeci:", dict(sorted(Counter(e["mesec_no"] for e in entries if e["mesec_no"]).items())))
print(f"OK → {OUT}")
