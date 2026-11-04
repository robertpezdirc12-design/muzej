#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P205 — MERGE KROP-forenzike v entries_1872.json (ročna-tabela iz vizualnih-Readov + krop-log)."""
import json, glob, os

TMP = "/tmp/p205"
ent = json.load(open(f"{TMP}/entries_1872.json"))

MANUAL = {
    13: {"ime": "Barbara Kerdise [~ Perdise/Pecdiac — PEZDIR-grafia!]", "opomba": "PEZDIR-grafia-#11-1872 + otrok-½-J-Krampje! + h50-NOVA-hiša"},
    16: {"ime": "Anna KRIŽAN [~ Vrižan-VLM-ZAVRJEN]", "opomba": "KRIŽAN-korekcija (KROP!); 66-J-Typhöse-Lungenentzündung; h66-NOVA"},
    23: {"ime": "Matthias Žunec [~ Ferič/Furič-KROP-DUEL]", "starost": "2 meseca [~ 4 tednov?]", "opomba": "★ h11-NIT-4.-LETO-1872 (→ 1873-z177-63J → P203-16dni → P202-KUNIĆ-1875!) + ime/starost-DUEL"},
    26: {"ime": "Johann Bakorić", "opomba": "'Prümml und Son Pfarre' [?] + h44"},
    28: {"ime": "Margaretha PRIMEJ [~ Žunec-VLM-ZAVRJEN]", "starost": "2 dni", "bolezen": "Brechruhr [griža]", "opomba": "KROP-KOREKCIJA-ime! + otrok-2-DNI + h44-×2-1872!"},
    35: {"ime": "Johann Jakofitsch [~ Zaupšek-VLM-ZAVRJEN]", "starost": "1 leto", "opomba": "KROP-KOREKCIJA-ime! + otrok + h6-nit (→ z67! → 1877-h6!)"},
    36: {"ime": "Joseph Strohec [~ Štönec-VLM-DUEL]", "starost": "1½ let", "opomba": "h5-nit"},
    43: {"hisna": "37 [~ 38?]", "ime": "Catharina Husič", "opomba": "hisna-DUEL 37-vs-38 (Kurent!)"},
    65: {"ime": "Johann LEGAT [~ Pegdirec-VLM-ZAVRJEN]", "starost": "1 teden [~ 1 mes?]", "opomba": "KROP-KOREKCIJA-ime-#3! + otrok-Frisen + h20-nit (cf. 1878-h20-×2!)"},
    67: {"ime": "Maria Jakofčič", "opomba": "JAKOFČIČ-nit (cf. 1877-z39 + P199-×3!) + otrok-8-Mon + h6-×2-1872!"},
    70: {"ime": "Johann Feliko [~ Felikša]", "starost": "¼ leta [~ 3 mes?]", "opomba": "otrok + h1-nit (ZELIHA/ZELE-h1-×2-1878!)"},
    74: {"hisna": "7 [~ 3?]", "ime": "Andreas Toster [~ Toško-VLM]", "opomba": "hisna-DUEL 7-vs-3! + otrok-3½-J"},
    78: {"ime": "Mathias JEGLIČE [~ Jeglič — Dejak-VLM-ZAVRJEN]", "opomba": "KROP-KOREKCIJA-ime-#4! + 83-J + ★ CHOLERA-1872-nastop! + h42-nit (cf. P203-h42!)"},
    85: {"ime": "Marija (Dutzbandl...-Kind) — NEPOZNAN-ime [?]", "opomba": "otrok + h62-×2-KLASTER!"},
    86: {"ime": "Anna KHURE [~ Kure]", "opomba": "KURE-nit! + h62-×2-#2"},
    89: {"hisna": "8 [~ 9? / 5-VLM]", "ime": "Maria [?]", "opomba": "hisna-DUEL 8/9-vs-5! + otrok-1½-J-Frisen"},
    111: {"opomba": "h38/24-'Prilozje-in-Griblje'-DVOJNA (KROP-neučinkovit — P204-s101-tail-1:1!) + Nervenfieber"},
}

krops = {}
for f in glob.glob(f"{TMP}/krop-grib/z*.json"):
    d = json.load(open(f))
    try:
        z = int(os.path.basename(f).split("_")[0][1:])
        krops[z] = d
    except Exception:
        pass

fixed = 0
for e in ent["entries"]:
    z = e.get("z")
    if z in MANUAL:
        e.update(MANUAL[z])
        fixed += 1
    k = krops.get(z)
    if k and z != 111:
        if k.get("duhovnik") and not e.get("duhovnik"):
            e["duhovnik"] = k["duhovnik"]
        if k.get("bolezen") and e.get("bolezen") and k["bolezen"][:12].lower() not in (e["bolezen"] or "").lower():
            e["bolezen_krop"] = k["bolezen"]

griblje = [e for e in ent["entries"] if any(w in (e.get("vas") or "").lower() for w in ("gribl", "grible", "hrible"))]
ent["griblje"] = len(griblje)
ent["griblje_entries"] = griblje
ent["korekcije"] = {"manual": sorted(MANUAL.keys()), "n_fixed": fixed}
json.dump(ent, open(f"{TMP}/entries_1872.json", "w"), ensure_ascii=False, indent=1)
print(f"MERGE: {fixed} ročnih; Griblje-FINAL: {len(griblje)}")
print("Griblje-z:", [e["z"] for e in griblje])
