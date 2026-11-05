#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P217 — agregacija 73 vpisov leta 1860 (ŠTEVJE-IZ-VRSTIC-19.×!).
s20 = MEJA-1859/60: ROKOPISNA-'1860'-GLAVA (KROP-'1860'-POTRJENA — VLM-'1800'-MISREAD-KOREKCIJA!)
+ RESTART-z1–z13 (BREZ-taila-na-s20 — tail-1859-na-s17–s19!). BREZ-vsotne-vidne?! (glava+restart-neposredno!)
★★★ s25-tail = WRITTEN-53–59 (REGISTERJSKA-NAPAKA-P216!) — kronološko-z67–z73!
★★★ VLM-margin-misreadi: s18-'90–101'→'80–91' (+10-tens-8/9-duel-KROP!) + s22-r1-'23'→'27' (KROP-chain!)
★★★ z27-'16.-Mai-1860'-EKSPLICITNA-LETNICA-v-vpisu (KROP!) + POŽEK-h58-nit!
Vrstna aritmetika: 13+13+13+13+14+7 = 73 (kronološko-z1–z73; written-duplikat-53–59-dokumentiran!)
Izhod: /tmp/p217/entries_1860.json"""
import json

TMP = "/tmp/p217"
P216 = "/tmp/p216"
P215 = "/tmp/p216"
PLAN = [
    (20, list(range(1, 14)), "z1–z13-RESTART-1860 (MEJA-1859/60-s20: '1860'-rokopisna-glava-KROP-POTRJENA (VLM-'1800'-misread-KOREKCIJA!) + restart-z1–z13-BREZ-taila (tail-1859-na-s17–s19!); ★ 2-GRIBLJE: z7-h55-Simčič-TRI-DUEL-starost! + z13-h6-Jakofčič-DUEL-starost!)", 1, TMP),
    (21, list(range(14, 27)), "z14–z26 (13; ★ 2-GRIBLJE: z23-h13-Jakošec[~duel!]-59J + z24-h50-ime-TRI-GARBLE-X-open-SPOL-X-open!)", 1, TMP),
    (22, list(range(27, 40)), "z27–z39 (13; VLM-r1-margin-'23'-misread→'27'-KROP-chain!; ★ 1-GRIBLJE: z27-h58-POŽEK-nit-'16.-Mai-1860'-EKSPLICITNA-LETNICA-KROP!-Barbara[~Bartholomä!]-8-mes!)", 1, TMP),
    (23, list(range(40, 53)), "z40–z52 (13; P216-VLM! glava-'1860'-bledo; 0-GRIBLJE; s23-margin-VLM-'41–53'-misread→'40–52'-KROP-P216!)", 1, P216),
    (24, list(range(53, 67)), "z53–z66 (14; P216-VLM! z53-mesec-avgust-nadaljevanje-KROP-P216 (September-glava-šele-z54!); ★ 2-GRIBLJE: z61-h24-Brenc[~duel!] + z65-h30[~40!]-PEZDIRC[?]-duel!)", 1, P216),
    (25, list(range(67, 74)), "z67–z73-TAIL-WRITTEN-53–59 (7; P215-VLM-s25-vrste-1–7! REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA-kronološko-#67–#73!; ★★ 2-GRIBLJE: z69-h57-Valentin-54J + z70-'Prist-57'-Valentin-Struna[?]-37J — VALENTIN-×2-2-dni!)", 1, P215),
]

KROP = {
    7: {"ime": "Miklavž [~Anništ[?]-KROP-duel!] Simčič",
        "starost": "[TRI-DUEL-X-open: 27[VLM]-vs-87[KROP]-vs-37[PAS]!]",
        "bolezen": "Wassersucht [~KROP-opomba]",
        "_opomba": "★★★ KROP-full-row+PAS + ★★★ GRIBLJE-h55-1860-nova + starost-TRI-DUEL-X-open + ime-duel + Jän-29/31-1:1"},
    13: {"ime": "Josip Jakofčič [~Jakobčič-1:1-duel!]",
         "starost": "[TRI-DUEL-X-open: 46-let[VLM]-vs-1-J-1-M[?KROP]-vs-14-J[?PAS]!]",
         "bolezen": "[garble — Brustbräune[?PAS]/Kopfkrankheit[?KROP]]",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ GRIBLJE-h6-1860-nova + starost-TRI-DUEL-X-open + '½[?]-Gütler'-stan-garble + Feb-24/26-1:1"},
    23: {"ime": "Andrej [~Lunbran[?]-KROP-duel-X-open!] Jakošec [~Jakobs[?]-duel!]",
         "bolezen": "Lungenentzündung, Auszehrend [KROP]-vs-Entzündung[PAS]-duel",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ GRIBLJE-h13-1860-nova + 59-J-KROP+PAS-1:1! + Mai-1/2-1:1 + ime-garble-X-open"},
    24: {"hisna": "50 [duel-'30'-KROP-z23-opomba!]",
         "ime": "[TRI-GARBLE-X-open: 'Matija?-Petine?'[VLM]-vs-'Peter-[Mautknecht?]'[KROP]-vs-'Rosalia-Pedire[~]'[KROP2] — SPOL-X-open!]",
         "starost": "64 J [duel-'68-J[?]'KROP2-2:1!]",
         "bolezen": "Lungenentzündung [KROP+PAS-2:1!]",
         "_opomba": "★★★ KROP-full-row+PAS-×2 + ★★★ GRIBLJE-h50-1860-nova + ime-TRI-GARBLE-X-open (SPOL-nejasen!) + '½-Güblerin[?]-vs-Gübler[?]' + Mai-1/2"},
    27: {"ime": "Barbara [~Bartholomä[Bartlome!]-KROP-DUEL-X-open!] Požek [~Pöckl!-duel!]",
         "starost": "8 mesecev [KROP+PAS-1:1!]",
         "bolezen": "[garble — 'Müeman[?Marasmus?]'-KROP]",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ POŽEK-h58-NIT-1860 (z27-otrok-8-mes! — cf.-P211-z90-h58 + P192-h58!) + ★★★ '16.-Mai-1860'-EKSPLICITNA-LETNICA-v-vpisu (KROP! — sredino-letnika! cf.-ULEDBA-pattern!) + ime-DUEL-X-open (Barbara/Bartholomä!)"},
    61: {"ime": "Inocenz [~Lukas!-duel] Brenc [~Brinar?-duel]",
         "starost": "23 J [duel-krop-'1-J-½[?]']",
         "bolezen": "[garble — Zuckfallfluß[?]]",
         "_opomba": "★★★ KROP-full-row-P216 + ★★★ GRIBLJE-h24-1860 (h24-2.-let: cf.-1861-z20-ŽELKO??-ne — Zemelj! + 1864-žé?) + hisna-24-3×-1:1 + datum-duel-10/11"},
    65: {"hisna": "30 [duel-'40'-KROP!]",
         "ime": "Mathias [~Martin?-duel] Pezdirc [?X-open: 'Poschirc'-VLM/'Pestirne'-KROP!]",
         "starost": "34 J [~54!-DUEL-KROP!]",
         "bolezen": "[2-vrstični-GARBLE — Abzehrung-mit-Fieber[?]/Brustfluss[?]]",
         "_opomba": "★★★ KROP-full-row-P216 + ★★★ PEZDIRC-h30[?]-1860-nit (PEZDIRC-MREŽA-×5!) + hisna-DUEL + starost-DUEL-34/54 + ime-TRI-DUEL-X-open"},
    69: {"ime": "Valentin [priimek-NEBERLJIV-X-open]",
         "starost": "54 J",
         "_opomba": "★★★ VALENTIN-×2-h57-1/2 (written-55! — REGISTERJSKA-NAPAKA-kronološko-#69!) + Dez-10/12 + 54-J + Griblje-h57"},
    70: {"ime": "Valentin Struna [?X-open-garble]",
         "hisna": "57 ['Prist'-lokalna-oznaka-X-open!]",
         "starost": "37 J",
         "_opomba": "★★★ VALENTIN-×2-h57-2/2 (written-56! — #70!) + Dez-10/13 + 37-J + 'Griblje-Prist-57'-'Prist'[?]-X-open + oče-sin-hipoteza-54J/37J"},
}

entries = []
for item in PLAN:
    sken, z_list, op, vrsta_filter, srcdir = item[0], item[1], item[2], item[3], item[4]
    d = json.load(open(f"{srcdir}/vlm-page/s{sken}.json"))
    vrste = d.get("vrstice", [])
    realne = []
    for x in vrste:
        ime = (x.get("ime") or "").strip()
        vas = (x.get("vas") or "").strip()
        mes = (x.get("mesec") or "").strip()
        smrt = (x.get("smrt") or "").strip()
        pokop = (x.get("pokop") or "").strip()
        if not ime and not vas: continue
        if not mes and not smrt and not pokop: continue
        if "vsota" in str(x.get("zaporedna", "")).lower() or str(x.get("zaporedna", "")).strip() == "—":
            continue
        if sken == 25 and (x.get("vrsta") or 0) > 7: continue  # s25: samo tail-r1–r7 (written-53–59 = #67–#73!)
        realne.append(x)
    if len(realne) != len(z_list):
        print(f"⚠ s{sken}: pričakovano {len(z_list)}, najdeno {len(realne)} (VLM n={len(vrste)})")
    for i, x in enumerate(realne[:len(z_list)]):
        x = dict(x)
        x["z"] = z_list[i]
        x["sken"] = sken
        x["pag"] = sken - 5
        x["vrsta_sken"] = i + 1
        x["ord_opomba"] = op
        k = KROP.get(x["z"])
        if k:
            for kk, vv in k.items():
                if kk == "_opomba": x["krop_opomba"] = vv
                else: x[kk] = vv
            x["krop"] = True
        entries.append(x)

for e in entries:
    if not e.get("bolezen"): e["bolezen"] = e.get("bolezen") or None

# --- normalizacija (KROP-korekcije) ---
NORM = {
    53: {"mesec": "August [KROP-KOREKCIJA! VLM-'September'-napaka — September-glava-šele-pri-z54!]",
         "smrt": "27.", "pokop": "28.",
         "_n": "z53-mesec-avgust-nadaljevanje (KROP-P216-s24_zap: 'pod-1860-brez-mesečne-glave, September-šele-pred-z54'!)"},
}
for e in entries:
    n = NORM.get(e["z"])
    if n:
        for kk, vv in n.items():
            if kk == "_n": e["mesec_norm_opomba"] = vv
            else: e[kk] = vv

# --- normalizacija ---
import re as _re
for e in entries:
    h = str(e.get("hisna") or "").strip()
    if h and not h.isdigit():
        mfirst = _re.search(r"\d+", h)
        if mfirst:
            e["hisna_duel"] = h; e["hisna"] = mfirst.group(0)
    m = str(e.get("mesec") or "").strip()
    if m.startswith("[") and "]" in m:
        e["mesec"] = m.replace("[", "").replace("]", "").strip()

# --- mesec-zapuščanje ---
prev_mes = None
for e in entries:
    mm = (e.get("mesec") or "").strip()
    if mm and mm != "—" and not mm.startswith("("):
        prev_mes = mm.split()[0]
    elif not mm or mm == "—":
        if prev_mes:
            e["mesec"] = f"{prev_mes} [kontekst-zapuščanje!]"
            e["mesec_deduced"] = True

# --- statistika ---
meseci_all = {}
for e in entries:
    m = (e.get("mesec") or "").strip().split()[0] if (e.get("mesec") or "").strip() else "?"
    m = m.replace("[kontekst-zapuščanje!]", "").strip() or "?"
    m = {"Januar": "J", "Jänner": "J", "Februar": "F", "Feber": "F", "März": "M", "Marec": "M",
         "April": "A", "Mai": "M2", "Maj": "M2", "Juni": "J2", "Junij": "J2", "July": "J3", "Juli": "J3",
         "August": "A2", "Avgust": "A2", "September": "S", "October": "O", "Oktober": "O",
         "November": "N", "December": "D", "Dezember": "D"}.get(m, m)
    meseci_all[m] = meseci_all.get(m, 0) + 1

grib = [e for e in entries if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]

out = {
    "faza": "P217",
    "leto": 1860,
    "knjiga": "04106",
    "okvir": {"skeni": "s017–s025", "pag": "12–20", "pag_formula": "sken−5",
              "meja_1859_60": "s20 ('1860'-rokopisna-glava-KROP-POTRJENA — VLM-'1800'-misread-KOREKCIJA! + RESTART-z1–z13-BREZ-taila-na-s20 — tail-1859-še-3-strani-s17–s19!)",
              "meja_1860_61": "s25 (tail-WRITTEN-53–59 + vsotna-'60'-REGISTERJSKA-NAPAKA + vsotna-'1861'-marker + '1861'-rokopisna-glava — P216!)",
              "vrstna_aritmetika": "13+13+13+13+14+7 = 73 (kronološko-z1–z73!; WRITTEN-duplikat-53–59-dokumentiran!)"},
    "statistika": {"vpisov_1860": len(entries), "griblje": len(grib),
                   "hise": len({e.get("hisna") for e in grib}),
                   "meseci": meseci_all},
    "krop_vizualne": [{"z": z, **{k: v for k, v in k.items() if not k.startswith("_")}} for z, k in sorted(KROP.items())],
    "registerjska_napaka": "★★★ REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA-1860 (P216-dokazana!): s25-tail-WRITTEN-53–59 + vsotna-'60' — kronološko-#67–#73 (prejšnja-s24-že-53–66!) — ordinali-1860-NI-ČISTO (1.-leto-z-napako! — ŠTEVJE-IZ-VRSTIC-še-vedno-EXAKT!)",
    "entries": entries,
    "griblje_entries": grib,
    "leadP218": None,
}
json.dump(out, open(f"{TMP}/entries_1860.json", "w"), ensure_ascii=False, indent=1)
print(f"1860: {len(entries)} vpisov / {len(grib)} Griblje / {len({e.get('hisna') for e in grib})} hiš")
print("meseci:", meseci_all)
print("Griblje z:", [e["z"] for e in grib])
print("Griblje hiše:", [e.get("hisna") for e in grib])
