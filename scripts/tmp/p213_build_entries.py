#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P213 — agregacija 91 vpisov leta 1864 (ŠTEVJE-IZ-VRSTIC-15.×!).
s39 = MEJA-1863/64: tail-1863 (z55–z64 + vsotna-vrstica 1-8-6-4!) + RESTART z1–z2!
'1864'-VELIKA-LETVICA na s40-glavi = 51.-POTRDITEV-invariante (arb_s40_glava-KROP!).
Vrstna aritmetika: 2+14+14+14+15+14+14+4 = 91; ordinali-1–91 ČISTO-7.-leto-zapored!
★★★ s41-SHIFT-SANACIJA: VLM-zap +1-pomik razkrit (margin-17–30 KROP-stripi + VIZUALNI-dokaz!)
★★★ KROP-VIZUALNE-ADJUDIKACIJE (računalniško-vodene-izrezi + direktni-vpogled):
  z18-h14 (4-Z-ZANKO!) + z18-PEZDIRC (glyph-comparacija-z85!) + z33-FILAK ('-ilak' + h34-nit!)
  + z34-ŠIMIC + z35-ŽELKO + z36-POŽEK + z44-h71 (γ-7!) + z61-h5 (CALIBRACIJA z60-'1'/z62-'8'!)
  + z85-PEZDIRC-h11 (dve-ozki-1!) + z85-DATUMI-Dec-2./4. (ANOMALIJA-NE-KRONOLOŠKI-VNOS!)
s46-tail z88–z91: P212-KROP-dokaz (arb_s46_tail; sveža-križ-3/4-EXAKT + z89-duel-HONEST!).
Izhod: /tmp/p213/entries_1864.json"""
import json

TMP = "/tmp/p213"
PLAN = [
    (39, list(range(1, 3)), "z1–z2-RESTART-1864 (MEJA-1863/64-s39: tail-1863-z55–z64 + vsotna-vrstica-1-8-6-4!; '1864'-glava-na-s40 = 51.-POTRDITEV!)", 11),
    (40, list(range(3, 17)), "z3–z16 (14; ★ 5-GRIBLJE: z6,z9,z10,z12,z13!)",
     ),
    (41, list(range(17, 31)), "z17–z30 (14; ★★★ s41-SHIFT-SANACIJA: VLM-zap-+1-pomik! margin-17–30-KROP-VIZUALNO!; 3-GRIBLJE: z18,z27,z30)"),
    (42, list(range(31, 45)), "z31–z44 (14; ★★★ 6-GRIBLJE-MAJ-klaster: z31,z33,z34,z35,z36 + z44-h71!; z33-FILAK + z34-ŠIMIC-KROP!)"),
    (43, list(range(45, 60)), "z45–z59 (15; 0-GRIBLJE — Juli/Avgust-luknja!)"),
    (44, list(range(60, 74)), "z60–z73 (14; 2-GRIBLJE: z61-h5-CALIBRACIJA! + z64)"),
    (45, list(range(74, 88)), "z74–z87 (14; 1-GRIBLJE: z85-PEZDIRC-h11 + ANOMALIJA-NE-KRONOLOŠKI-VNOS!)"),
]

# KROP-korekcije (VIZUALNO-adjudicirane za reproducibilnost!) — ključ: z
KROP = {
    6: {"ime": "[?≈'Mollganerischb'-garble-X-open] Kind von Johann Križan (½ Gübler)",
        "_opomba": "★★★ X-open-garble: ime-celica-1.-vrstica '?ollganerischb-Kind von' (ultra-zoom-6×: VLM-'Malijschehibsb'/'Wolfgang-Khür'-obe-FALSIFICIRANI!) + 2.-vrstica '½ gübler Johan Križān' — FORMULA-hipoteza: ≈'uneheliches/außereheliches-Kind-von' (cf. z80+z84-ISTI-'Mastgutlinstleht-Kind-von'-formula!) — starost-bolezen-PRAZNI (dojenček!)"},
    9: {"stan": "¼ Güblerin [~garble: VLM-'Gürlichanderuib'/KROP-vizual-'güblasbonil']",
        "_opomba": "★ KRIŽAN-nit (Maria-87-J-h62 — NAJSTAREJŠA-1864! cf. z1-1865-Maria-Križan-h3-81-J + 2×-Maria-Križan-P212!)"},
    10: {"ime": "Mathias Simic", "stan": "Ablöser [~Altlöbler?]",
         "_opomba": "★ ŠIMEC-grafia-#1 (cf. z34-Peter-ŠIMIC-h18! h19-nit)"},
    12: {"vas": "Griblje (weiler Pragovi [~])", "ime": "Maria Klepec", "stan": "½ Güblerstochter",
         "_opomba": "★ KLEPEC-nit (h2-weiler-Pragovi[~] — cf. h45-Georg-Obrawos + KLEPEC-velika-nit-korpusa!)"},
    17: {"hisna": "11 [KROP-vizual: morda-14? duel-VLM-'11']",
         "_opomba": "★ Zemelj-h11/14-duel (ne-Griblje — HONEST-dvoboj; Kurrent-1/4!)"},
    18: {"hisna": "14", "ime": "Michael Pezdirc [KROP-glyph-comparacija-z85!]",
         "stan": "¼ Güblers-Kind", "starost": "6 mesecev",
         "_opomba": "★★★ KROP-VIZUALNA-ADJUDIKACIJA (3-fazna): (1) hisna-'14'-4-IMA-ZANKO (z18_hisa2@5× — duel-VLM-'11' + KROP-VLM-'11'-FALSIFICIRANA!) (2) ime-'Feydrie'[KROP-VLM]/'Poždrie'[VLM] → PEZDIRC via IDENTIČNA-glyph-veriga-z-z85-'Anna-Pezdirc' (P-cap-e-z-d-r-c!) (3) starost-'6mg'=6-mesecev (KROP-'1J'-row-bleed-z19-FALSIFICIRAN!) — ★★★ PEZDIRC-h14-NIT-1864 (z18-6-M → 1865-z41-Mathias-unehelich-h14 → 1865-tail-z66-Maria-66J-h14! 3-LETA-GLOBOKO!)"},
    27: {"hisna": "3", "ime": "Georg Dragos [~DRAGOŠ-glyph!]", "stan": "Ablassen [~Ablöser?]",
         "_opomba": "★★★ KROP-VIZUALNA-ADJUDIKACIJA (z27_hisa@5×: '3'-dvoja-izboklina ≠5≠8!) + DRAGOŠ-glyph ('Dragos' — cf. P200-DRAGOŠ-h12-nit-15-let-pred-prvenci! h3 = KRIŽAN-h3-nit-1865-z1!) — h3-družina-1864: Dragos-70-J + (z61→h5-NE!)"},
    30: {"ime": "Anna Želko [KROP!]", "hisna": "1",
         "_opomba": "★★★ ŽELKO-nit-#1 (½-Gütlens-Witwe-22-J — cf. z35-Peter-ŽELKO-h1-ISTE-HIŠE-×2-MAJ-klaster!)"},
    31: {"ime": "Matthias Kitah [~Kotar?]", "stan": "½ Gübler [~'Gütlbler'-garble]",
         "_opomba": "★ 'Kitah'-grafia (cf. z32-Grem-Michael-Kitah — brata? X-open!)"},
    33: {"ime": "Mathias Filak [KROP-VIZUAL!]", "stan": "Ablöser [~'Altabler'-garble]",
         "_opomba": "★★★ KROP-VIZUALNA-ADJUDIKACIJA (z33_ime@4.5×: '-ilak'-dolgi-rez → FILAK! duels: VLM-'Kitah'/KROP-VLM-'Šilak'-obe-FALSIFICIRANI!) + ★★★ FILAK-h34-NIT-1864 (cf. P211-h34-×2: z48-Katarina-6½-J + z80-Josip-1-J! 3.-leto-zapored-h34!)"},
    34: {"ime": "Peter Šimic [KROP-VIZUAL!]", "stan": "Ablöser [~'Altabler'-garble]",
         "_opomba": "★★★ KROP-VIZUALNA-ADJUDIKACIJA (z34_ime2@4.5×: 'Peter-Šimic'-haček-S! duel-VLM-'Jinnie/Zinnig'-FALSIFICIRAN!) + ★★★ ŠIMEC-h18-NIT-1864 (cf. z10-h19-Mathias-Simic-×2-leta! + P200-h18-ŠIMEC-NIT-1877!)"},
    35: {"ime": "Peter Želko [KROP!]", "stan": "¼ Gütlner-kind",
         "_opomba": "★★★ ŽELKO-h1-×2-MAJ-KLASTER (z30-Anna-22-J-½-Witwe + z35-Peter-1-J — mati+sin?! 8-DNI-razlike! cf. P212-HUSIČ-h37-klaster!)"},
    36: {"ime": "Maria Požek [KROP-'Požeh'!]", "stan": "¼ Gütlner-kind",
         "_opomba": "★★★ POŽEK-h67-NIT-1864 (duel-VLM-'Pogach[~Pogorevc?]'-FALSIFICIRAN-KROP!) — h67-veriga: 1864-z36-Maria-6-M → 1865-z36-Mathias-36-J → (P192-1885-h58-Požek!?)"},
    44: {"hisna": "71", "ime": "Anna Strauž [~Straus?]", "stan": "¼ Gübler [?]",
         "_opomba": "★★★ KROP-VIZUALNA-ADJUDIKACIJA (z44_hisa@5×: '71' = γ-7-S-PREČKO + ozka-1! duels: VLM-'11[~71?]'-delno + KROP-VLM-'7'-FALSIFICIRAN!) + ★★★ h71-DUEL-KONTINUITETA (cf. P210-z26-'h74[~71?]-Brinc-DUEL'!) + STRAUS-mreža? (h72-gnezdo-sosedi! X-open)"},
    61: {"hisna": "5", "stan": "¼ Gübler", "ime": "Johannes Hruscel [~Hrušec?]",
         "_opomba": "★★★ KROP-VIZUALNA-ADJUDIKACIJA-S-CALIBRACIJO (s44_hisna_cal@5×: z60-'1'-ozka + z61-'5'-kapa-čelada + z62/z63-'8'-dvojna-zanka → z61 = 5! duels: VLM-'3'-×2-FALSIFICIRANA — KURRENT-3/5/8-zmeda-LEKCIJA!) + ★ NOVA-hiša-h5 (korpus-93 brez h5? X-open!) + stan-'¼'-KROP-CAL (duel-VLM-'½'!)"},
    64: {"ime": "Mathias Zager [~Gašek/Jager?]",
         "_opomba": "★ KURRENT-J/G/Z-duel ('Zager'-KROP vs VLM-'Gazek/Gašek' — X-open!) + h27-nit"},
    85: {"hisna": "11", "ime": "Anna Pezdirc [KROP-VIZUAL!]", "smrt": "2.", "pokop": "4.",
         "_opomba": "★★★ KROP-VIZUALNA-ADJUDIKACIA ×3: (1) ime-'Anna-Pezdirc'@4× (duel-VLM-'Petzler'/'Pezdir'!) (2) hisna-'11'-DVE-OZKI-1 ≠ z18-'14'-ZANKA (isti-pisar-istega-dneva!) (3) datumi-Dec-2./4.-ČISTO (s45_datumi_tail@4×!; KROP-VLM-'pokop-11'-FALSIFICIRAN!) + ★★★ ANOMALIJA-NE-KRONOLOŠKI-VNOS-2.-×-leta: z85 (Dec 2./4.) vpisan-PO-z84 (Dec 11.[~]/13.[~]) — cf. P212-z13-pokop-pred-smrtjo! + ★★★ PEZDIRC-h11 (ANNA!) — PEZDIRC-nit-2-hiši-1864 (h14-Michael + h11-Anna!)"},
}

entries = []
for item in PLAN:
    sken, z_list, op = item[0], item[1], item[2]
    min_vrsta = item[3] if len(item) > 3 else 1
    d = json.load(open(f"{TMP}/vlm-page/s{sken}.json"))
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
        # s39: tail-1863 (vrsta 1–10) preskoči!
        if sken == 39 and (x.get("vrsta") or 0) < min_vrsta: continue
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

# --- s46-tail z88–z91 (P212-KROP-dokaz: arb_s46_tail; sveža-križ-3/4-EXAKT!) ---
TAIL_P213 = [
    (88, {"mesec": "December", "smrt": "12.", "pokop": "14.", "vas": "Otok", "hisna": "20",
          "ime": "Maria Križan", "stan": "Ablabamin[?]-isti-stan-kot-z1-1865!", "starost": "48 J.",
          "bolezen": None},
     "★★★ 2×-MARIA-KRIŽAN-v-1-TEDNU-tail-polovica (z88-Otok-h20-48-J-12.Dez + z1-1865-GRIBLJE-h3-81-J-16.Jan — ista-bazna-beseda-stana!)"),
    (89, {"mesec": "December", "smrt": "14.", "pokop": "21.", "vas": "Gradac", "hisna": "26",
          "ime": "Johann Topič [P212-KROP; svež-KROP-2026-duel: 'Johanna-Soprič[~]-Kerssnbraid.-hči' — DUAL-KROP-DUEL-HONEST!]",
          "stan": "Lavtinar[?] kbr.", "starost": "3 tedni[?] (izbrisano, otrok)",
          "bolezen": None},
     "★ z89-starost-KOREKCIJA-V-ZAPISU (prekrižan-zapis + prevlada — potrjeno-v-obe-seji!) + smrt-DUEL (P212-'14.' vs sveža-'19.' — KURRENT-4/9!)"),
    (90, {"mesec": "December", "smrt": "26.", "pokop": "28.", "vas": "Podžemelj", "hisna": "3",
          "ime": "Michael Pezdirc", "stan": "Ablabano[?]", "starost": "63 J.", "bolezen": None},
     "★ PEZDIRC-ime-tail (Podžemelj-h3-63-J — cf. Griblje-PEZDIRC-nit h14/h11!)"),
    (91, {"mesec": "December", "smrt": "30.", "pokop": "1. Jänner 1865", "vas": "Klošter", "hisna": "35",
          "ime": "Josef Grah", "stan": "ganf. Kaplan und Beneficial zu Gradac", "starost": "66 J.", "bolezen": None},
     "★★★ ULEDBA-#11-10.INSTANCE (smrt-30.Dez-1864→pokop-1.Jänner-1865 — čez-mejo!)"),
]
for z, fix, op2 in TAIL_P213:
    entries.append({"z": z, "sken": 46, "pag": 41, "vrsta_sken": z - 87, "vir": "P212-KROP arb_s46_tail (sveža-križ-3/4-EXAKT + z89-duel!)",
                    "ord_opomba": "s46-TAIL-1864-z88–z91 (P212-KROP-dokaz!)", "krop": True,
                    "krop_opomba": op2, **fix})

for e in entries:
    if not e.get("bolezen"): e["bolezen"] = e.get("bolezen") or None

# --- mesec-zapuščanje (z25-'Totgeborenes-Söhnlein' — vrsta-brez-meseca-v-April-kontekstu!) ---
prev_mes = None
for e in entries:
    mm = (e.get("mesec") or "").strip()
    if mm and mm != "—" and mm.split()[0] not in ("—", ""):
        prev_mes = mm.split()[0]
    elif not mm or mm == "—":
        if prev_mes:
            e["mesec"] = f"{prev_mes} [kontekst-zapuščanje!]"
            e["mesec_deduced"] = True

# --- statistika ---
meseci_all = {}
for e in entries:
    m = (e.get("mesec") or "").strip().split()[0] if (e.get("mesec") or "").strip() else "?"
    m = {"Januar": "J", "Jänner": "J", "Februar": "F", "Feber": "F", "März": "M", "Marec": "M",
         "April": "A", "Mai": "M2", "Maj": "M2", "Juni": "J2", "Junij": "J2", "July": "J3", "Juli": "J3",
         "August": "A2", "Avgust": "A2", "September": "S", "October": "O", "Oktober": "O",
         "November": "N", "December": "D", "Dezember": "D"}.get(m, m)
    meseci_all[m] = meseci_all.get(m, 0) + 1

grib = [e for e in entries if "gribl" in str(e.get("vas", "")).lower() and not str(e.get("vas", "")).lower().startswith("grem")]
# izloči Grem (Griblje-glyph false-positive!)
grib = [e for e in grib if "grem" not in str(e.get("vas", "")).lower()]

out = {
    "faza": "P213",
    "leto": 1864,
    "knjiga": "04106",
    "okvir": {"skeni": "s039–s046", "pag": "34–41", "pag_formula": "sken−5",
              "meja_1863_64": "s39 (tail-1863-z55–z64 + vsotna-vrstica-1-8-6-4 + RESTART-z1–z2!; '1864'-VELIKA-LETVICA-na-s40-glavi = 51.-POTRDITEV-invariante!)",
              "meja_1864_65": "s46-tail (z88–z91-P212-KROP + ULEDBA-#11-z91!)",
              "vrstna_aritmetika": "2+14+14+14+15+14+14+4 = 91"},
    "statistika": {"vpisov_1864": len(entries), "griblje": len(grib),
                   "hise": len({e.get("hisna") for e in grib}),
                   "meseci": meseci_all},
    "krop_vizualne": [{"z": z, **{k: v for k, v in k.items() if not k.startswith("_")}} for z, k in sorted(KROP.items())],
    "s41_shift": "VLM-zap-stolpec-+1-pomik-razkrit: margin-N == fresh-row(N-16); KROP-stripi-s41_zap_top/bot (23–30-VLM ✓ + 17–23-VIZUALNO!) + s40_zap (3–9 + 10–16-VLM ✓) + s42_zap_top (31–32 ✓) → s41 = z17–z30-ČISTO!",
    "entries": entries,
    "griblje_entries": grib,
    "leadP214": None,
}
json.dump(out, open(f"{TMP}/entries_1864.json", "w"), ensure_ascii=False, indent=1)
print(f"1864: {len(entries)} vpisov / {len(grib)} Griblje / {len({e.get('hisna') for e in grib})} hiš")
print("meseci:", meseci_all)
print("Griblje z:", [e["z"] for e in grib])
print("Griblje hiše:", [e.get("hisna") for e in grib])
