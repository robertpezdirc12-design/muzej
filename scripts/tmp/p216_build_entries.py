#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P216 — agregacija 54 vpisov leta 1861 (ŠTEVJE-IZ-VRSTIC-18.×!).
s25 = MEJA-1860/61: tail-1860 (WRITTEN-53–59 + vsotna-'60' — REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA!
prejšnja-stran-s24-že-ima-53–66! kronološko-#67–#73!) + VSOTNA-'1|8|...|1'-'1861'-MARKER-4.-INSTANCE
+ ROKOPISNA-'1861'-GLAVA (OBOJE — cf.-s35-pattern!) = 54.-POTRDITEV-invariante! + RESTART-z1–z5!
★★★ s27 = s26 DOUBLE-SCAN (3.-v-knjigi!) — 2×-NEODVISNA-VLM-z6–z18!
★★★ KROP-korekcije: z20-vas-'Griblje'→'Zemelj'! + z18-mesec-'April'→'Mai'! (kronološka-veriga-ČISTA!)
★★★ PERDIU/PEZDIRC[?]-h42-×3-APR-KLASTER (družina-hipoteza!) + URIH-h68 + MALEŠIČ-h26 + KLOBUČAR-h48!
Vrstna aritmetika: 5+13+14+16+6 = 54; ordinali-z1–z54-ČISTO-10.-leto-zapored!
Izhod: /tmp/p216/entries_1861.json"""
import json

TMP = "/tmp/p216"
OLD = "/tmp/p215"
PLAN = [
    (25, list(range(1, 6)), "z1–z5-RESTART-1861 (MEJA-1860/61-s25: tail-1860-WRITTEN-53–59 + vsotna-'60'-REGISTERJSKA-NAPAKA + vsotna-'1|8'-letnica-marker + '1861'-rokopisna-glava = 54.-POTRDITEV!; ★ z1-DUELI-hisna-34/54/56-starost-25/65-ime-Kampšar/Stampehar!)", 9, TMP),
    (26, list(range(6, 19)), "z6–z18 (13; s26-PRIMARY (s27=double-scan-križ!); ★★★ 5-GRIBLJE: z7-h1-ŽELKO-nit-TRI-branja-ime-DUEL! + z11-h68-URIH-4-branja-ime-DUEL! + z14/z15/z17-h42-×3-APR-KLASTER (družina-hipoteza — ime-garble!); ★ z18-mesec-KOREKCIJA-'April'→'Mai'-KROP!)", 1, TMP),
    (28, list(range(19, 33)), "z19–z32 (14; ★ 2-GRIBLJE: z30-h26-MALEŠIČ-NOVA-59J-duel! + z32-h48-KLOBUČAR-NOVA-15J-TRAJNI-DUEL!; ★ z20-vas-KOREKCIJA-'Griblje'→'Zemelj'-KROP! — GRIBLJE-7-ne-8!)", 1, TMP),
    (29, list(range(33, 49)), "z33–z48 (16; P215-VLM-s29! glava-'1861'-bledo; 0-GRIBLJE; tail-1861-kontekst)", 1, OLD),
    (30, list(range(49, 55)), "z49–z54-1861-TAIL (6; P215-VLM-s30-vrste-1–6! ordinali-iz-CHAIN (VLM-margin-'29–34'-misread-KOREKCIJA-P215!); ★ z54-GRIBLJE-tail-NI (z54=Dobravce! — z54-1860-Požek-bil-na-s30-WRITTEN-53–59!))", 1, OLD),
]

KROP = {
    7: {"ime": "Grozj [TRI-branja-DUEL-X-open: 'Jurkič'[VLM]-vs-'Franc'[KROP]-vs-'Šumič/Gunkiè'[vizualno]!]",
        "stan": "¼ [~½!-duel] Gübler",
        "starost": "47 J [KROP+PAS-2:1-vs-VLM-44!]",
        "bolezen": "Wassersucht [~KROP-PAS-duel-'Magenkrank[?]']",
        "_opomba": "★★★ KROP-full-row+PAS + ★★★ ŽELKO-h1-NIT-1861 (h1-4.-LETO-GLOBOKO: 1861-z7-[?]-47J → 1862-z41-Maria-½J → 1864-×2!) + ime-TRI-branja-DUEL-X-open + datum-duel-13/15"},
    11: {"ime": "Markus [4-BRANJA-DUEL-X-open: 'Marko'[s26]-vs-'Mariša/Marša'[s27]-vs-'Martha[~Utrich]'-KROP — SPOL-X-open!] Urih",
         "stan": "¼ [~½] Gübler",
         "bolezen": "Lungenentzündung [PAS+vizualno-2:1-vs-KROP-'Lungensucht']",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ URIH-h68-NOVA-HIŠA (cf. P212-'URIH-ne-Urik'-1865!) + ime-4-BRANJA-DUEL-X-open (Kurrent-M-zmeda!) + 46-J-3×-1:1!"},
    14: {"ime": "[GARBLE-X-open: 'Perdiu[?]'-VLM-vs-'Mariana-Kerdivc[~]'-KROP-vs-'[Marina?]-Ivan-Peždinc'-vizualno!]",
         "starost": "[TRI-DUEL-X-open: 45-J[VLM]-vs-4½-J[vizualno]-vs-7½-J[PAS]!]",
         "bolezen": "[garble — Albrandefluss[?KROP]/Alten-und-Schwachheit[?PAS]]",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ h42-×3-APR-KLASTER-1/3 (ime-GARBLE-X-open — spol-nejasen!) + starost-TRI-DUEL + stan-garble-'Ablöserin-Kind[?]'"},
    15: {"ime": "Anžal [~Miklav[?]-KROP-duel] [PEZDIRC[?]-priimek-garble-X-open: 'Perdiu[?]'-vs-'Kerdivc[?]'-'Peždinc'-vizualno!]",
         "starost": "2 leti [3×-1:1: VLM+PAS+vizualno!]",
         "bolezen": "Steckfluß [KROP+PAS-1:1!]",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ h42-×3-APR-KLASTER-2/3 + 2-J-3×-1:1 + '¼-Gütlertsohn' + PEZDIRC-družina-hipoteza!"},
    17: {"ime": "Marija [~garble: 'Mai-Pe'-VLM-'Mariša-Bezgorič/Degde'-s27-'Marija-Hržica'-KROP!]",
         "starost": "5 tednov [VLM+PAS-2×!]",
         "bolezen": "[garble — 'Vifal'šfn[?]'-KROP-X-open]",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ h42-×3-APR-KLASTER-3/3 (dojenček-5-tednov!) + ½-Güblers-tochter + PERDIU/PEZDIRC-družina-hipoteza (starš+2-otroci-v-6-dnih!)"},
    18: {"mesec": "Mai [KROP-KOREKCIJA! VLM-'April'-×2-NAPAČNO — '1. Mai 3.'-jasno!]", "smrt": "1.", "pokop": "3.",
         "starost": "[TRI-DUEL-X-open: 42-J[VLM]-vs-12-J[PAS]-vs-1½-J[KROP]!]",
         "bolezen": "Zopfkrämpfe [~KROP]",
         "_opomba": "★★★ KROP-MESEC-KOREKCIJA ('Mai'! — kronološka-veriga-ČISTA: Apr-23/24→Mai-1/3→Mai-4!) + ne-Griblje (Cerkovše-2-Anna-Jakopič-'Güblerstochter-unvereh.') + starost-TRI-DUEL"},
    20: {"vas": "Zemelj [KROP-KOREKCIJA! VLM-napaka — Z-forma-jasna!]",
         "starost": "2 leti [~duel-krop-'48-J[?]'-vs-PAS-'2-Tage[?]']",
         "bolezen": "Wassersucht [~Wasserbrust?-duel]",
         "_opomba": "★★★ KROP-VAS-KOREKCIJA (VLM-je-bral-G-vas-NAPAČNO — Z-forma-jasna-vs-G-forma-z61/z65-komparacija!) — GRIBLJE-ŠTEVJE-BREZ-tega-vpisa! + MUC-nit (Zemelj-h24-Johanna-2J — cf.-1862-s32/s33-Muc-×4!) + ime-duel-'Johanna-Muc[?]'",
         "hisna": "24"},
    30: {"stan": "Ablöser [duel-KROP-'Ackerer[?]']",
         "starost": "59 J [duel-KROP-PAS-'54-J[~ali-57]'-vs-VLM+vizualno-59-2×!]",
         "bolezen": "Abzehrung [TRI-branja-1:1!]",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ MALEŠIČ-h26-NOVA-HIŠA + ime-TRI-branja-1:1 (Mathias-Malesič!) + starost-DUEL + Abzehrung-3×-1:1!"},
    32: {"ime": "Katharina Klobučar [~Hlobučar-S/H-duel-KROP!]",
         "starost": "15 J [TRAJNI-DUEL-X-open: 15[VLM+vizualno]-vs-65[KROP-PAS]-vs-1[KROP-grib]!]",
         "bolezen": "Abzehrung [~duel-KROP-'Bräbsfloss[?]'-garble]",
         "_opomba": "★★★ KROP-full-row+PAS + ★★★ KLOBUČAR-h48-NOVA-HIŠA + starost-TRAJNI-DUEL-X-open + '¼-Güblerkind' + 15-J-otrok!"},
    54: {"hisna": "67 [~69-VLM-duel!-\u03b3-forma-KROP!-PO\u017dEK-nit-korelacija-z-1865-h67!]",
         "ime": "Mathias Po\u017eek [~Po\u017eekh-garble]",
         "stan": "\u00bc G\u00fctler in Griblje [~garble]",
         "starost": "2 J [~duel-krop-'2-J-1-M[?]']",
         "bolezen": "Kr\u00e4mpfe [~'Gnaifan'/'Kreuzflu\u00df'-garble-duel]",
         "_opomba": "\u2605\u2605\u2605 PO\u017dEK-h67-NIT-ZADNJI-1861-VNOS (z54-Dez-16/18! KROP-P215: \u03b3-forma-'67'-vs-VLM-'69'-duel!) \u2192 1865-P212-z36-Mathias-36J-ISTO-HI\u0160A-h67 (o\u010de-sin-hipezoza-X-open!) + h67 = 9.-GRIBLJE-hi\u0161a-1861"},
    35: {"hisna": "18 [duel-'19[?]-VLM!']",
         "ime": "Anna Goric [~Goričan[?]-garble]",
         "starost": "1½ J",
         "bolezen": "Abzehrung [~VLM-garble]",
         "_opomba": "★★★ GRIBLJE-1861 (P215-VLM-s29-r3!) + ★★★ ŠIMEC-h18-NIT-GLOBLJE (1861-Anna-Goric-1½J-h18 → 1863-z26-Georg-Simic-h18 + 1864-z34-Peter!) + hisna-duel-18/19"},
    44: {"hisna": "14 [duel-'44[?]-VLM!']",
         "ime": "Anna Hrance [?garble]",
         "starost": "3 J",
         "bolezen": "Krämpfe [~VLM-garble]",
         "_opomba": "★★★ GRIBLJE-1861 (P215-VLM-s29-r12!) + ★★★ PEZDIRC-h14-NIT-GLOBLJE (1861-Anna-Hrance[?]-3J-h14 → 1864-z18-Michael-Pezdirc-h14 + 1865-z41!) + hisna-duel-14/44 + cf.-h42-×3-klaster (PEZDIRC-mreža!)"},
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
        # s25: tail-1860 (vrste 1–8: WRITTEN-53–59 + vsota) preskoči!
        if sken == 25 and (x.get("vrsta") or 0) < vrsta_filter: continue
        # s30: 1862-restart (vrste 7+) preskoči!
        if sken == 30 and (x.get("vrsta") or 0) > 6: continue
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

# --- normalizacija ---
NORM = {}
for e in entries:
    n = NORM.get(e["z"])
    if n:
        for kk, vv in n.items():
            if kk == "_n": e["mesec_norm_opomba"] = vv
            else: e[kk] = vv
    h = str(e.get("hisna") or "").strip()
    if h and not h.isdigit():
        import re as _re
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
    "faza": "P216",
    "leto": 1861,
    "knjiga": "04106",
    "okvir": {"skeni": "s023–s030", "pag": "18–25", "pag_formula": "sken−5",
              "meja_1860_61": "s25 (tail-1860-WRITTEN-53–59 + VSOTNA-'60'-margin-REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA + VSOTNA-'1|8'-letnica-marker-4.-INSTANCE + ROKOPISNA-'1861'-GLAVA = 54.-POTRDITEV! + RESTART-z1–z5!)",
              "meja_1861_62": "s30 (tail-1861-z49–z54 + vsotna-'1|8|6|2'-'1862'-MARKER-3.-instance + RESTART-BREZ-rokopisne-glave — P215!)",
              "vrstna_aritmetika": "5+13+14+16+6 = 54"},
    "statistika": {"vpisov_1861": len(entries), "griblje": len(grib),
                   "hise": len({e.get("hisna") for e in grib}),
                   "meseci": meseci_all},
    "krop_vizualne": [{"z": z, **{k: v for k, v in k.items() if not k.startswith("_")}} for z, k in sorted(KROP.items())],
    "vsotna_letnica": "★★★ VSOTNA-VRSTA = LETNICA-MARKER-4.-INSTANCE: s25-'1|8|...|1'='1861' (KROP-'1|8'-levo + ROKOPISNA-'1861'-glava-pod-njo = 54.-POTRDITEV-invariante! — cf. s30-'1862' + s35-'1863' + s39-'1864'!)",
    "registerjska_napaka": "★★★ NOV-TIP-ANOMALIJE: REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA-1860 (s25-tail-WRITTEN-53–59 + vsotna-margin-'60' — prejšnja-stran-s24-že-ima-53–66! kronološko-#67–#73! KROP-s25_zap_tight-1:1!)",
    "entries": entries,
    "griblje_entries": grib,
    "leadP217": None,
}
json.dump(out, open(f"{TMP}/entries_1861.json", "w"), ensure_ascii=False, indent=1)
print(f"1861: {len(entries)} vpisov / {len(grib)} Griblje / {len({e.get('hisna') for e in grib})} hiš")
print("meseci:", meseci_all)
print("Griblje z:", [e["z"] for e in grib])
print("Griblje hiše:", [e.get("hisna") for e in grib])
