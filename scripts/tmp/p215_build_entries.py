#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P215 — agregacija 60 vpisov leta 1862 (ŠTEVJE-IZ-VRSTIC-17.×!).
s30 = MEJA-1861/62: tail-1861-z49–z54 (KROP-zap-stolpec: VLM-misread-'29–34'→'49–54'-KOREKCIJA!)
+ VSOTNA-'1|8|6|2'-'1862'-MARKER (3.-instance-invariante — levo-'1|8'-KROP + desno-'6|2'-KROP!)
+ RESTART-z1–z7 (BREZ-rokopisne-'1862'-glave — NOVA-VARIANTA: vsotna=edini-marker!)
★★★ s32 = s33 DOUBLE-SCAN (2.-v-knjizi: cf.-s53/s54-P211!) — 2×-NEODVISNA-VLM-branja-z24–z39!
★★★ FILAK-mreža-×3-1862 (z11-Katharina-h61 + z14-Nicolaus-h5-'Kind-von-Anna-Filak' + Anna!)
★★★ KUNE-h10-nit (z10-1862-'Kure' → 1863-z2-'Kune'-X-open!) + POŽEK-h67-tail-1861 (z54!)
Vrstna aritmetika: 7+16+16+15+6 = 60; ordinali-z1–z60-ČISTO-9.-leto-zapored!
Izhod: /tmp/p215/entries_1862.json"""
import json

TMP = "/tmp/p215"
OLD = "/tmp/p214"
PLAN = [
    (30, list(range(1, 8)), "z1–z7-RESTART-1862 (MEJA-1861/62-s30: tail-1861-z49–z54-KROP-zap-DOKAZ + vsotna-'1|8|6|2'-'1862'-MARKER-3.-instance + RESTART-BREZ-rokopisne-glave-NOVA-VARIANTA!; ★ z1-PEZDIRC-Andreas-36J-Podzemelj-h10-'von-Griblje[?]'!)", 8, TMP),
    (31, list(range(8, 24)), "z8–z23 (16; ★★★ 4-GRIBLJE: z10-h10-KURE→KUNE-nit! + z11-h61-Katharina-FILAK! + z14-h5-Nicolaus-FILAK-'Kind-von-Anna'! + z17-h47-Anna-Skobucar!)", 1, TMP),
    (32, list(range(24, 40)), "z24–z39 (16; s32=s33-DOUBLE-SCAN-2.-v-knjizi! — s32-fresh-ČISTEJŠA-foto (s33-obscured!) — 2×-NEODVISNA-VLM!; ★ z30-'Mrtvogrobnik[?]'-pokop-brez-smrti!)", 1, TMP),
    (34, list(range(40, 55)), "z40–z54 (15; robna-'410–424'-prefixacija→ordinali-40–54-iz-CHAIN!; ★★★ 4-GRIBLJE: z41-h1-ŽELKO-nit-Zuckfall! + z43-h63-POTOČAR-Typhus-TRI-branja-1:1! + z48-h61-2.-instance-'—'/'—'! + z50-h5-2.-instance-Graucek-duel!)", 1, OLD),
    (35, list(range(55, 61)), "z55–z60-1862-TAIL (6; P214-VLM-s35-vrste-1–6!; ★ z57-Gradac-h60-DOCTOR-HOUSE-Marentič-nit-cf.-1863-z61!)", 1, OLD),
]

KROP = {
    1: {"stan": "¼ Güblerssohn [+ 'von Griblje'[?]-KROP!]",
        "_opomba": "★★★ z1-RESTART-1862-PEZDIRC-NIT: Andreas-Pezdirc-36J-Podzemelj-h10-'von-Griblje[?]' — cf. 1864-z18-Michael-h14-¼-Güblers-Kind + 1864-z85-Anna-h11 + 1865-z41-Mathias-unehelich-h14! (PEZDIRC-mreža-globlje-v-1862!) + Lungenentzündung"},
    4: {"ime": "Markus [~Mathias!-duel] Križan",
        "stan": "Gutsler [~duel-full-page-garble]",
        "bolezen": "Marasmus senilis [KROP+PAS-1:1!]",
        "_opomba": "★★★ KROP-full-row+PAS (hisna-'9'-γ/9-duel-rešen-9! + ime-Markus/Mathias-duel + stan-garble!) + ★★★ KRIŽAN-h9-NOVA-HIŠA (Griblje-h9! soseda-h10-KUNE! cf. 1862-tail-z56-Krasinec-h9-Krijžan!) + 72-J + Marasmus-senilis"},
    10: {"ime": "Simon [~Vinanz?-Ehefrau-duel-X-open!] Kure",
         "stan": "¼ Güblerssohn [~Ehefrau?-duel]",
         "bolezen": "Ohnmacht[sucht?] [~garble-duel-'-sucht'-končnica]",
         "starost": "2 J",
         "_opomba": "★★★ KROP-full-row+PAS-×2 (ime-DUEL: full-'Simon'-vs-krop-'Maria/Vinanz-Ehefrau'-X-open!) + ★★★ KUNE-h10-NIT: z10-1862-'Simon-Kure'-h10 → 1863-z2-'Joannes-Kune'-h10 (X-open-4-branja-'Kumre/Kime/Kure' — 1862-'Kure'-reading-PODPORA — 5.-branja!) + 2-J"},
    11: {"ime": "Katharina Filak [DUEL: 'Kolak'-full-vs-'Tilak'-vizualno-vs-'Filak'-KROP — F/T/K!]",
         "stan": "[garble — ~Hausfrau?]",
         "starost": "34 J [duel-krop-37-J — 2×-vs-1×!]",
         "bolezen": "Lungenentzündung [KROP+PAS-1:1!]",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ FILAK-h61-1862! (DUEL-F/T/K-rešen-FILAK-z-z14-korelacijo!) + ★★★ KATARINA-FILAK-age-match: 1862-z11-34J → 1866-P211-z48-Katarina-Filak-38J — MOŽNO-ISTA-OSEBA (hiša-h61-vs-h34-sprememba-možna — HIPEZOZA-X-open!) + h61-1.-instance"},
    14: {"ime": "Nicolaus Filak [DUEL: 'Kolak'-full-vs-'Silak'-KROP-vs-'Filak'-vizualno!]",
         "opomba": "unehelich[?] Kind von Anna Filak [garble-2-vrstično — 'uneheliches'/'verwaisetes'-X-open!]",
         "bolezen": "[garble — Zufallfluß[?]/Zopfkrankheit[?]-X-open]",
         "_opomba": "★★★ KROP-full-row + ★★★ FILAK-h5-1862-'Kind-von-ANNA-FILAK' (FORMULA-cf.-P214-z53-'außereheliches-Kind-von'-FORMULA-DOKAZ!) + ★★★ ANNA-FILAK-nova-oseba (mati!) — FILAK-mreža-×3-v-1862 (Katharina-h61 + Nicolaus-h5 + Anna!) → FILAK-h34-1864/65/66 (P213-z33-Mathias-63J + P211-z48-Katarina + z80-Josip!) + 10-J + h5-duel-krop-'3'"},
    17: {"ime": "Anna Skobucar [~Hlobucar-duel-S/H]",
         "bolezen": "Lungensucht [KROP]-vs-Masern [PAS-'ošpice!']-DUEL-X-open",
         "_opomba": "★★★ KROP-full-row+PAS + bolezen-DUEL-X-open (Masern=ošpice-epidemija-hipoteza?) + h47-NOVA-hiša (duel-krop-'17'-vs-full-'47'-2×!) + 1½-J + '¼-Gütlerskind'"},
    41: {"ime": "Maria Zeljko [~Šeljko-Ž/Z-duel]",
         "stan": "¼ Güblerskind",
         "bolezen": "Zuckfall [~Kaßfall/Unfall-duel — cf.-1863-z39/z40-'Zaugfall≈Zuckfall'!]",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ ŽELKO-h1-NIT: z41-1862-Maria-½J-Griblje-h1 → 1864-z30-Anna-22J + z35-Peter-1J (h1-×2!) — h1-3.-LETO-GLOBOKO! + ½-J + Zuckfall-duel"},
    43: {"ime": "Thomas Potočar [KROP+FULL-1:1!]",
         "stan": "[2-vrstični-garble — ~Ehemann-von-Agnes[?]/Amts...-X-open]",
         "bolezen": "Typhus [TRI-branja-1:1: KROP+PAS+FULL!]",
         "_opomba": "★★★ KROP-full-row+PAS + Typhus-TRI-branja-1:1 (izjemno!) + ★★★ KRIŽAN-h63-NIT-2-LETI: z43-1862-Thomas-Potočar-h63 → 1864-z63-'?ollganerischb'-Kind-von-Johann-Križan-h63! + h63-duel-krop-'68'-vs-'63'-2× + 28-J"},
    48: {"ime": "Mathias Jerlicar [~Seliscar-duel-J/S! + garble-vrstica-'Müllerssohn[?]']",
         "starost": "— [duel-krop-'1 J[?]'-vs-'—'-2×!]",
         "bolezen": "—",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ h61-2.-INSTANCE-v-1-LETU (z11-Katharina-Filak-März + z48-Okt!) + ★★★ ANOMALIJA: starost-'—' + bolezen-'—' (PRAZNI-STOLPCI! cf.-doctor-house-pattern) + ime-garble-2-vrstici-'Müllerssohn[?]'-mlinarjev-sin-X-open"},
    50: {"ime": "Joseph Graucek [DUEL: 'Strucelj'-KROP-vs-'Gartner[?]'-full — G/S/K-cf.-1863-z27-STRAUS-K/G/S!]",
         "stan": "½ Gübler",
         "starost": "61 J [~TRAJNI-DUEL: pas-'61-let?-ali-6-tednov?' + krop-'1[?]' + full-'61-fufa[?]' — X-open!]",
         "bolezen": "Abzehrung [~pas-'Abgang[?]']",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ h5-2.-INSTANCE-v-1-LETU (z14-Nicolaus-Filak-Apr + z50-Okt!) + ime-TRI-branja-DUEL-X-open (Graucek/Strucelj/Gartner!) + starost-TRAJNI-duel + mesec-duel-krop-'Xbr'-vs-'October'"},
    54: {"hisna": "67 [duel-krop-'6?'-vs-vizualno-'67'-γ-forma!]",
         "starost": "2 J [~duel-krop-'2-J-1-M[?]']",
         "bolezen": "Krämpfe [~'Gnaifan'-garble]",
         "_opomba": "★★★ TAIL-1861-GRIBLJE: z54-Mathias-POŽEK-h67-2J-Dez-16/18! — ★★★ POŽEK-h67-NIT-4-LETA-GLOBOKO: 1861-z54-Mathias-2J → 1865-P212-z36-Mathias-36J-ISTO-HIŠA-h67 (oče-sin-hipezoza-X-open!) + h69[full-VLM]-vs-h67[KROP-γ!]"},
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
            continue  # vsotna-vrstica (letnica-marker) — ne-je-vpis!
        # s30: tail-1861 (vrste 1–7: z49–z54 + vsota) preskoči!
        if sken == 30 and (x.get("vrsta") or 0) < vrsta_filter: continue
        # s35: 1863-restart (vrste 7+) preskoči!
        if sken == 35 and (x.get("vrsta") or 0) > 6: continue
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

# --- normalizacija (KROP-adjudicirane-vrednosti; dueli-v-opombah) ---
NORM = {
    27: {"mesec": "Mai", "smrt": "31.", "pokop": "2. Juni", "_n": "duel-Mai/Juni-pokop-VIZUALNO-s32/s33!"},
    34: {"mesec": "Juli", "smrt": "30.", "pokop": "1. August", "_n": "duel-Juli/August-pokop (cf.-1863-z48-'30.Jul|1.Aug'!)"},
}
for e in entries:
    n = NORM.get(e["z"])
    if n:
        for kk, vv in n.items():
            if kk == "_n": e["mesec_norm_opomba"] = vv
            else: e[kk] = vv
    # hisna-čistilka: '61 [~]' → '61' (dueli-ostanejo-v-krop_opomba)
    h = str(e.get("hisna") or "").strip()
    if h and not h.isdigit():
        digits = "".join(c for c in h if c.isdigit())
        if digits: e["hisna_duel"] = h; e["hisna"] = digits
    # mesec-čistilka: '[Dezember]' → 'Dezember'
    m = str(e.get("mesec") or "").strip()
    if m.startswith("[") and "]" in m:
        e["mesec"] = m.replace("[", "").replace("]", "").strip()

# --- mesec-zapuščanje (kontekst-dedukcija) ---
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
    "faza": "P215",
    "leto": 1862,
    "knjiga": "04106",
    "okvir": {"skeni": "s029–s035", "pag": "24–30", "pag_formula": "sken−5",
              "meja_1861_62": "s30 (tail-1861-z49–z54 + VSOTNA-'1|8|6|2'-'1862'-MARKER-3.-instance + RESTART-z1–z7-BREZ-rokopisne-glave — NOVA-VARIANTA: vsotna=edini-letnica-marker!; KROP-zap-stolpec: glava-'1861'-bledo + '49–54'-jasno — VLM-misread-'29–34'-KOREKCIJA!)",
              "meja_1862_63": "s35 (tail-1862-z55–z60 + vsotna-'1|8|6|3'-'1863'-MARKER + RESTART-z1–z8 + '1863'-rokopisna-glava = 52.-POTRDITEV — P214!)",
              "vrstna_aritmetika": "7+16+16+15+6 = 60"},
    "statistika": {"vpisov_1862": len(entries), "griblje": len(grib),
                   "hise": len({e.get("hisna") for e in grib}),
                   "meseci": meseci_all},
    "krop_vizualne": [{"z": z, **{k: v for k, v in k.items() if not k.startswith("_")}} for z, k in sorted(KROP.items())],
    "vsotna_letnica": "★★★ VSOTNA-VRSTA = LETNICA-MARKER-3.-INSTANCE: s30-'1|8|6|2'='1862' (KROP-levo-'1|8' + KROP-desno-'6|2'!) + NOVA-VARIANTA: s30-RESTART-BREZ-rokopisne-'1862'-glave — vsotna=EDINI-marker (cf. s35-'1863'-glava+vsota-OBOJE!)",
    "entries": entries,
    "griblje_entries": grib,
    "leadP216": None,
}
json.dump(out, open(f"{TMP}/entries_1862.json", "w"), ensure_ascii=False, indent=1)
print(f"1862: {len(entries)} vpisov / {len(grib)} Griblje / {len({e.get('hisna') for e in grib})} hiš")
print("meseci:", meseci_all)
print("Griblje z:", [e["z"] for e in grib])
print("Griblje hiše:", [e.get("hisna") for e in grib])
