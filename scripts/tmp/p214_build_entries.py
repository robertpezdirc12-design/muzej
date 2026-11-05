#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P214 — agregacija 64 vpisov leta 1863 (ŠTEVJE-IZ-VRSTIC-16.×!).
s35 = MEJA-1862/63: tail-1862 (z55–z60 + vsotna-'1|8|6|3'-'1863'-MARKER!) + RESTART z1–z8!
★★★ arb_s35_glava: rokopisna-'1863'-glava + Jänner + z1 = 52.-POTRDITEV-invariante!
★★★ VSOTNA-VRSTA = LETNICA-MARKER: s35-'1|8|6|3' + s39-'1|8|6|4' (razpeta-čez-stolpce!)
Vrstna aritmetika: 8+15+15+16+10 = 64; ordinali-z1–z64-ČISTO-8.-leto-zapored!
★★★ 7-KROP-VIZUALNIH-ADJUDIKACIJ-SKUPIN (z2-Kune-X-open + z12-h65/unehelich + z18-h32/65J +
z26-h18-ŠIMEC-nit + z27-h11[~71!]-STRAUS + z33-h53 + z38-Rosalia-infans-X-open!)
★★★ z64-ULEDBA-#11-12.×: '31.-Dec-1863' | '2.-Jänner-1864' EKSPLICITNI-LETNICI (@6×!)
s39-tail z55–z64: P213-VLM (/tmp/p213/vlm-page/s39.json vrste 1–10!).
Izhod: /tmp/p214/entries_1863.json"""
import json

TMP = "/tmp/p214"
OLD = "/tmp/p213"
PLAN = [
    (35, list(range(1, 9)), "z1–z8-RESTART-1863 (MEJA-1862/63-s35: tail-1862-z55–z60 + vsotna-'1|8|6|3'-'1863'-MARKER + '1863'-rokopisna-glava = 52.-POTRDITEV!; ★ 1-GRIBLJE: z2-h10-Kune-X-open!)", 8, TMP),
    (36, list(range(9, 24)), "z9–z23 (15; ★ 2-GRIBLJE: z12-h65-BRINC-unehelich! + z18-h32-ULRICH-65J!; ★ z11-Anmerkung-annotacija + h52/32-duel; z53-s38-'außerehelich'-FORMULA-napoved!)", 1, TMP),
    (37, list(range(24, 39)), "z24–z38 (15; ★★★ 4-GRIBLJE: z26-h18-SIMIC-nit! + z27-h11[~71!]-STRAUS-duel! + z33-h53-SIMIC-×2! + z38-h21-Rosalia-infans-X-open!)", 1, TMP),
    (38, list(range(39, 55)), "z39–z54 (16; 0-GRIBLJE; ★★★ z53-'außereheliches-Kind-von'-FORMULA-DOKAZ-za-P213-z6-garble! + z54-FILAK-novorojenček-Grem-h33-nit!)", 1, TMP),
    (39, list(range(55, 65)), "z55–z64-1863-TAIL (10; P213-VLM-s39-vrste-1–10!; ★★★ z64-ULEDBA-#11-12.×-EKSPLICITNI-LETNICI-'31.Dec.1863'-'2.Jän.1864'!; ★ z59-Filak-Grem-h33 + z61-Marentič-doctor-house-nit!)", 1, OLD),
]

KROP = {
    2: {"ime": "Joannes Kune [X-open-duel: 'Kumre'/'Kime'/'Kure' — KURRENT-m/n+u/r-4-NE-SKLADNA-BRANJA!]",
        "stan": "Inwohner [~Inwohnermann?]",
        "bolezen": "Gehirnentzündung [KROP-tight-POTRJENA ('zelo-dolga-besega-čez-stolpec')! duel-'Gichtschmerzen'-FALSIFICIRAN!]",
        "_opomba": "★★★ KROP-VIZUALNI-ADJUDIKACIJI-×2 (ime-4-branja-X-open-HONEST + bolezen-duel!) + h10-nova-hiša (korpus-93-X-open!)"},
    12: {"hisna": "65",
         "stan": "Pächter-Junggesell [~tight-garble]",
         "bolezen": "Lungenentzündung + Magenkrampf [KROP-tight-2-vrstično! duel-full-page-'Wahnsinn[?]/Schlag...'-FALSIFICIRAN!]",
         "opomba": "unehelich [KROP-tight-ANMERKUNG-STOLPEC!]",
         "_opomba": "★★★ KROP-×3 (hisna-'65'-KROP+VIZUALNO! duel-full-page-'68[?]'-FALSIFICIRAN! + bolezen + opomba-'unehelich'!) + ★★★ BRINC-h65-NOVA-HIŠA (3.-BRINC-hiša: cf. P212-z9-Anna-h23-60-J + P212-z20-Jernej-h28-28-J!) + UNEHELICH-opomba-1.-V-GRIBLJE-KORPUSU!"},
    18: {"stan": "Ablöserin [~'Ablaberin'-garble]",
         "starost": "65 J",
         "_opomba": "★★★ h32-TRIJSKOTRJENA (full-page + KROP-full-row + VIZUALNO-s36!) + starost-'65J'-VIZUALNO (duel-KROP-pas-'68'-FALSIFICIRAN!) + ULRICH-nova (cf. 1864-z6-'Ulrich'?-X-open)"},
    26: {"stan": "¼ Güblerssohn",
         "starost": "53 J",
         "bolezen": "Asthma Millari [~miliare? — VIZUALNO-s37-'Millari' + full-page-'Milleri[?]']",
         "_opomba": "★★★ KROP-h18 + VIZUALNO ('18'-2×-neodvisno!) + starost-'53J'-VIZUALNO (duel-pas-'5J'-garble-FALSIFICIRAN!) + ★★★ ŠIMEC-h18-NIT-ČEZ-LETA (1863-z26-Georg-Simic-h18 → 1864-z34-Peter-ŠIMIC-h18-ISTO-HIŠO! + 1864-z10-Mathias-h19! ŠIMEC-2-HIŠI-2-LETI!)"},
    27: {"hisna": "11",
         "ime": "Joannes Straus",
         "stan": "½ Gübler [duel-VIZUALNO-'¼?']",
         "bolezen": "magennahrt [~Magennahrt? ≈Magenkrampf-cf.-z12!]",
         "_opomba": "★★★ HISNA-DUEL-HONEST: KROP-tight-'11' ('ozka-črtica-brez-zanke'!) — ALTERNATIVA-'71' (γ-7-S-PREČKA! cf. P213-z44-h71-γ-7!) + ★★★ STRAUS-mreža-X-open: 1863-z27-'Joannes-Straus' (TRI-branja: full-'Kras'/VIZUALNO-'Graus'/tight-'Straus' — K/G/S!) + 1864-z44-'Anna-Strauž[~Straus?]'-h71 — ČE-h71: POPOLNA-KORELACIJA (isti-γ-7-glyph-2-leta-zapored!) + cf. 1864-z85-PEZDIRC-h11!"},
    33: {"hisna": "53",
         "smrt": "13.",
         "pokop": "15.",
         "stan": "¼ Güblerssohn",
         "_opomba": "★★ h53-2× (KROP-full-row + VIZUALNO-s37!) + datumi-VIZUALNO-'13.|15.' (duel-krop-'15./15.'-garble!) + ★ SIMIC-×2-1863-2-hiši (h18-Georg + h53-Peter — PATTERN-cf.-1864-ŠIMEC-×2-h18/h19!)"},
    38: {"ime": "Rosalia [infans — TRI-branja-duel-X-open: VIZUALNO-'infant-Rosalia-v.-Joh.-Broznič[?]' + KROP-'infant-Rosalia' + full-page-'Josef-Brozik'-FALSIFICIRANA-SINTEZA + tight-'Rojč/Jože'-garble!] — hči-Joh.-Brozič[~Broznik?/Barak?]",
         "starost": "1½ J [~TRAJNI-DUEL: full-page-'3 J.[~]' + KROP-tight-'1 J/1½ J' — X-open!]",
         "bolezen": "Dreinsucht [KROP-tight: dizenterija/krvava-driska!]",
         "_opomba": "★★★ IME-DUEL-X-open-HONEST (4-branja-neskladna!) + h21-nova-hiša (korpus-X-open!) + otroška-2/7"},
    48: {"mesec": "Juli", "pokop": "1. August", "starost": "12 J",
         "_opomba": "★ VIZUALNO-s38: '30.-Jul.|1.-Aug.' + Alter-'12-J' (duel-full-page-'15-let'!; mesec-'Juli/August'-VLM-garble → Juli!)"},
    64: {"mesec": "December", "smrt": "31. Dec 1863",
         "pokop": "2. Jänner 1864",
         "_opomba": "★★★ ULEDBA-#11-12.-INSTANCE-EKSPLICITNO (@6×-KROP + P213-VLM: '31.-Dec-1863' | '2.-Jänner-1864' — LETNICI-ZAPISANI-V-VPISU-čez-mejo!) + hiša-DUEL-h14[P213]-vs-'4'[?VIZUALNO]"},
}

entries = []
for item in PLAN:
    sken, z_list, op, min_vrsta, srcdir = item[0], item[1], item[2], item[3], item[4]
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
        # s35: tail-1862 (vrste 1–7: z55–z60 + vsota) preskoči!
        if sken == 35 and (x.get("vrsta") or 0) < min_vrsta: continue
        # s39: 1864-restart (vrste 11+) preskoči!
        if sken == 39 and (x.get("vrsta") or 0) > 10: continue
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
    "faza": "P214",
    "leto": 1863,
    "knjiga": "04106",
    "okvir": {"skeni": "s033–s039", "pag": "28–34", "pag_formula": "sken−5",
              "meja_1862_63": "s35 (tail-1862-z55–z60 + vsotna-'1|8|6|3'-'1863'-MARKER + RESTART-z1–z8!; '1863'-rokopisna-glava-s35 = 52.-POTRDITEV-invariante — arb_s35_glava-KROP!)",
              "meja_1863_64": "s39-tail (z55–z64-P213-VLM + z64-ULEDBA-#11-EKSPLICITNI-LETNICI + vsotna-'1|8|6|4'-'1864'-MARKER!)",
              "vrstna_aritmetika": "8+15+15+16+10 = 64"},
    "statistika": {"vpisov_1863": len(entries), "griblje": len(grib),
                   "hise": len({e.get("hisna") for e in grib}),
                   "meseci": meseci_all},
    "krop_vizualne": [{"z": z, **{k: v for k, v in k.items() if not k.startswith("_")}} for z, k in sorted(KROP.items())],
    "vsotna_letnica": "★★★ VSOTNA-VRSTA = LETNICA-MARKER-naslednjega-leta: s35-'1|8|6|3'='1863' + s39-'1|8|6|4'='1864' (cifre-razpete-čez-stolpce: zap/Land + ime + Alter + Priester! — 2-NOVI-instance; KROP-s39_vsota_desno: Alter-'6'+Priester-'4'-1:1!)",
    "entries": entries,
    "griblje_entries": grib,
    "leadP215": None,
}
json.dump(out, open(f"{TMP}/entries_1863.json", "w"), ensure_ascii=False, indent=1)
print(f"1863: {len(entries)} vpisov / {len(grib)} Griblje / {len({e.get('hisna') for e in grib})} hiš")
print("meseci:", meseci_all)
print("Griblje z:", [e["z"] for e in grib])
print("Griblje hiše:", [e.get("hisna") for e in grib])
