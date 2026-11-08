#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P220 — agregacija 73-vpisov leta 1857 (ŠTEVJE-IZ-VRSTIC-22.×!).
KNJIGA-START: s1 = NASLOVNI-LIST ('Tom. III' + 'Sterb-Buch' + 'Podzemelj' — 0-vrstic!)
+ s2 = '18 57'-RAZPETA-letnica-glava (rokopisna, nadčrtana!) + RESTART-z1 — KNJIGA-SE-ZAČNE-1857!
★★★ LUKNJA-32 (NOV-TIP-v-knjigi — pisarski-preskok!): s3-ordinalni-stolpec-konča-31 (15-ordinalov!)
+ s3-dno-RAZPRAZNO (y0.925–1.0-brez-vsebine — 3-kropi!) + s4-začne-z-33 (Juni-21./23.!) +
kronološki-seam-z31-Juni-21/22 → z33-Juni-21/23-GLADAK! → 73-kronoloških (z1–z31 + z33–z74;
WRITTEN-1–31 + 33–74 = 73-ČISTO — 1-LUKNJA! — 3.-instance-pisarskega-preskoka-v-knjigi-po-LUKNJA-92-1859!)
— X-open: morda-32-obrezan-na-dnu-s3 (tabela-do-roba!)!
vrstna-aritmetika 16+15+13+13+14+2 = 73; meseci J4+F8+M5+A5+M2-7+J2-3+J3-6+A2-18+S8+O-0!!+N5+D4;
★★★ OKTOBER-×0 (z65-Sep-24/26 → z66-Nov-9/11 — 15-dnevna-luknja!);
★★★ SCARLATINA?-klaster: 'Rušfieber/Rušenfleck'-×6–7 (z36–z46, July-24→Aug-12) + 'Amigdilitis[?]-garble'-×7
(s5: z48–z57) — isti-garble-družina?-X-open (2.-val?) — 1-GRIBLJE-v-klasterju (z45!);
★★★ 10-GRIBLJE / 9-hiš (h36-×2-KRIŽAN: z50-Georg/Jurij-4J + z74-Marijan-73J-TAIL!)
+ z71-hiša-NEBERLJIVA-3× ([?]!); tail-z74-duhovnik-'J.-Knauš/Kranz[?]' — MOŽEN-ZGODNJI-Knavs-podpis
(KOREKCIJA-P219-lead: Knavs-morda-ŽE-DEC-1857! X-open!);
Izhod: /tmp/p220/entries_1857.json"""
import json

TMP = "/tmp/p220"
# (sken, z-list, opomba, mode) — mode: 'pool' (vse page-vrste z vsebino) | 'tail2' (vrste 1–2)
PLAN = [
    (2, [f"z{i}" for i in range(1, 17)],
     "s2-z1–z16 (16; KNJIGA-START: NASLOVNA-LISTA-'Sterb-Buch.'-RAZPRTA + ★★★ '18 57'-RAZPETA-letnica-glava (rokopisna-nadčrtana!) + restart-z1!; ★ 3-GRIBLJE: z4-h60[?]/66-Lazar/Luka-TRI-DUEL + z5-h64-Matija-Verbičar-4×-križ + z10-h52-Jožef-Peskar-TRI-DUEL!)", "pool"),
    (3, [f"z{i}" for i in range(17, 32)],
     "s3-z17–z31 (15; NASLOVNA-LISTA-razprta + '1867'-prečrtano→1857-popravek-pisarja (vrsti-30/31-ob-robu!); ★ z29-'p.-Gübl[?]'-stan-vez (Sonel/Grem!) + z30-'p.-Gübl[?]'-stan-vez (Ceroviče!) — 2-Griblje-STAN-vezi-NI-vpisa!; ★★★ ZADNJA-VRSTICA = z31 — LUKNJA-32-SLEDI!)", "pool"),
    (4, [f"z{i}" for i in range(33, 46)],
     "s4-z33–z45 (13; ★★★ z33-ZAČNE-Z-33 (LUKNJA-32-PRED-tem!!) Juni-21./23.-seam-gladak-po-z31-Juni-21/22!; ★ z33-'1858'-prečrtano→1857-popravek-pisarja!; ★★★ SCARLATINA?-klaster-start: z36-Rušfieber + z40–z45-×5 (Aug-1→11!); ★ 1-GRIBLJE: z45-h13[?]/12-Marija/Martin-DUEL-Dragos-Rušfieber!; s4-desna-stran-December-vrstice-X-open (morda-drugi-del-knjige-quiri!))", "pool"),
    (5, [f"z{i}" for i in range(46, 59)],
     "s5-z46–z58 (13; ★★★ 'Amigdilitis[?]'-garble-klaster-×7 (z48–z57 — Rušfieber-družina?-2.-val-X-open!) + '1857'-glava-nadaljevanje (NObrestart!) + September-glava-z58; ★ 3-GRIBLJE: z50-h36-Georg/Jurij-KRIŽAN[2×-križ-vs-Krajncan-page!] + z56-h31[?]/51/57-TRI-Ana-Urih-3×-križ + z58-h48[?]/43/145-TRI-Anna-Stamcar/Straus-DUEL!)", "pool"),
    (6, [f"z{i}" for i in range(59, 73)],
     "s6-z59–z72 (14; NASLOVNA-LISTA-razprta + '1857'-glava (September); ★★★ OKTOBER-×0 (z65-Sep-24/26 → z66-Nov-9/11!); ★ z60-'gospod-Griblem[≈iz-Griblje?]'-stan-vez (Dobravce!); ★ 2-GRIBLJE: z61-h65-Georg-Mulik-TRI-garble + z71-h[?]-NEBERLJIVA-3×-Martin/Max-Zager-STAROST-DUEL (14-let-vs-1-mj-1-dan!)!)", "pool"),
    (7, [f"z{i}" for i in range(73, 75)],
     "s7-TAIL-1857-z73–z74 (2; P219-meja-dokumentirana + re-križ-P220-arb_s7_meja-1:1: VSOTNA-'1 8 5 [8]'-RAZPETE-P214-TIP-3.-INSTANCE ('1-8'+5-vidno!) + DVOJNA-ČRTA + rokopisna-'Jänner-1858'-glava + restart-z1–z11 + NEŠTEVILČENA-zadnja!; ★ z73-Gradac-h1-Martin-Kuncel/Kunstel/Kunovlt-TRI-DUEL-26J[2×-fresh!]-vs-86J[P219]-vs-1J-1M[P219-krop]-KOREKCIJA-P219-'Amalia-Rundel'!; ★★★ 1-GRIBLJE-TAIL: z74-h36-KRIŽAN-Marijan[4×-garble!]-73J-Lungenentzündung + duhovnik-'J.-Knauš/Kranz[?]'!)", "tail2"),
]

# KROP/trak-overrides + dueli za 10-GRIBLJE-vrstic (triangulacija: page-VLM + traki + krop-VLM + hi-zoom!)
KROP = {
    4: {"hisna": "60 [duel-66-page!]",
        "ime": "Lazar [TRI-DUEL-X-open: Lazar[hi-krop]/Luka-Rebernik[page]/Peter-Pečenko[trak]!]",
        "starost": "66 let [~]",
        "bolezen": "Koli[?] [?garble]",
        "_opomba": "★ 1.-GRIBLJE-v-KNJIGI-04106-kadarkoli (z4 = 4.-vpis-knjige!) + h60/66-DUEL (TOMINC-h60-nit-X-open!) + ime-TRI-DUEL + 'Fr.-Xaveryal[?]'-duhovnik-garble"},
    5: {"hisna": "64",
        "ime": "Matija Verbičar [4×-križ: Verbičar[page]/Verbiezer[hi]/Veberkar[trak]/Veibeshar[krop]! — 'in Griable' = iz-Griblje!]",
        "stan": "iz Griblje [~]",
        "starost": "68 let [duel-65!]",
        "bolezen": "Altersschwäche [~]",
        "_opomba": "★ h64-nit + najstarejši-Griblje-1857-kandidat (68J[?] — vs-z74-73J!) + 2.-GRIBLJE-knjige"},
    10: {"hisna": "52",
         "ime": "Jožef Peskar [TRI-DUEL-X-open: Peskar[page]/Bedric[trak]/Petrič[?]-krop!]",
         "starost": "46 let [duel-40!]",
         "bolezen": "Alfersvess [?≈Abzehrung-garble]",
         "_opomba": "★ h52-nit (P218-z81-'Posdiac[?]'-h52-99J-TRAJNI-DUEL + Knavs-družina-h52-1880s!) + zavihek-lista-krije-del-vrstice (dokumentirano!)"},
    45: {"hisna": "13 [duel-12-krop!]",
         "ime": "Marija [spol-DUEL: Marija[page+trak-2×!]-vs-Martin[krop]!] Dragos [~Dragas-2×!]",
         "stan": "½ Zibl, Šajna (Šajara) [~garble]",
         "starost": "1 leto",
         "bolezen": "Rušfieber [★★★ SCARLATINA?-klaster-6/7 (z36–z46)!]",
         "_opomba": "★ h13-DRAGOŠ-nit (ime-Dragos/Dragas = DRAGOŠ-družina! cf. P193-h3-DRAGOŠ-1864!) + edini-GRIBLJE-v-SCARLATINA?-klasterju + s4-desna-stran-December-X-open-quiri-opomba"},
    50: {"ime": "Jurij [≈Georg-trak!] Križan [★★★ DUEL: Križan[2×-križ: krop+trak!]-vs-Krajncan[page]-X-open!]",
         "stan": "¼ Gütl-garble [?]",
         "starost": "4 leta [?]",
         "bolezen": "[?-garble ('Hirzentzündung[?]' — morda-Gehirnentzündung!)]",
         "_opomba": "★★★ h36-KRIŽAN-×2-v-1857 (z50-otrok-4J + z74-Marijan-73J-TAIL!) — KRIŽAN-hiša-2-GENERACIJI! + 'Joan.-Šhubič[?]-P.'-duhovnik ≈ Skubic!"},
    56: {"hisna": "31 [TRI-DUEL: 31[page]/51[hi-krop]/57[trak]! — KURRENT-3/5/7-ZMEDA!]",
         "ime": "Ana Urih [3×-križ: UIRIH[page]/Ulrich[hi]/Urih[trak]! — ≈Uršula?-X-open]",
         "stan": "¼ Gütl-garble ('z Grabl Dorfman[?]' — ¼-Griblje-Gütler?-X-open!)",
         "starost": "3 tedne [?]",
         "bolezen": "Amigdilitis [?garble — SCARLATINA?-družina-X-open!]",
         "_opomba": "★ h31/51/57-TRI-DUEL + ime-3×-križ-STABILNO + pokop-Sep-2 (Aug-31-smrt!) — 1.-September-pokop-1857"},
    58: {"hisna": "48 [TRI-DUEL-X-open: 48[page]/43[?]/145[2×-križ: krop+trak!]!]",
         "ime": "Anna [TRI-DUEL-X-open: Stamcar[page]/Straus[2×-križ: trak+pas-krop!]!/Maria[hi]!]",
         "stan": "¼ Gütl-garble ('ih./in-Gubtl[?]' — ¼-Griblje-Gütler?-X-open!)",
         "starost": "66 let [duel-Kind[?]-pas-krop!]",
         "bolezen": "Magenkrampfung [?garble]",
         "_opomba": "★ honesty-max-vrstica-1857 (vse-celote-TRI-DUEL!) + 'Thom.-Ladargal[~]-Cop.'-duhovnik + h48/43/145-X-open"},
    61: {"ime": "Georg Mulik [TRI-garble-X-open: Mulik[page]/Mililkh[krop]/Gobik/Mulek[?]!]",
         "stan": "Janezov in Alžbete syn [~]",
         "starost": "1 leto [~]",
         "bolezen": "Abzehrung [~]",
         "_opomba": "★★★ h65-MILEK-hiša-nit (1858-z39-'Keržan[?]'-h65 → 1859-×2 → MILEK-mreža-04894-×9!) + 'P.-Kadungal[?]'-Ladergal-klaster-garble"},
    71: {"hisna": "[?]",
         "ime": "Martin Zager [~Zagar-2×! duel-Max[hi-krop]!]",
         "stan": "TRI-garble-X-open: 'najst.-Adejščafa[?]-hčer'[page] / 'gen.-Rimsafraund[?]'[pas] / 'ganz-außerehelich'[hi] (NEZAKONSKI!)",
         "starost": "14 let [★★★ DUEL: 1-mesec-1-dan[hi-krop]! — dojenček-hipoteza (Wasserkopf+außerehelich) — X-open!]",
         "bolezen": "Wasserkopf [~]",
         "_opomba": "★ hiša-NEBERLJIVA-3× (page+pas-krop+hi-krop — edini-primer-v-1857!) + STAROST-DUEL (dojenček-vs-najstnik!) + duhovnik-Johann-Verbič-cooperator + NEZAKONSKI-vpis-kandidat"},
    74: {"hisna": "36",
         "ime": "Marijan [4×-garble-X-open: Križan[arb-krop+P219!]/Kunezl[page]/Krisan/Kristjan[P219]/Danelfa-Vrizan[krop]!] Križan[?]",
         "stan": "vdovec[?]-vs-Ehelmann[?]-vs-Eheleut[?]-TRI-duel",
         "starost": "73 let",
         "bolezen": "Lungenentzündung",
         "_opomba": "★★★ TAIL-1857 = ZADNJI-vpis-leta + h36-KRIŽAN-×2 (z50-otrok!) — 1857-zadnji-Griblje (P219-dokumentirano + 3-fresh-križi!) + ★★★ duhovnik-'J.-Knauš/Kranz[?]' — MOŽEN-ZGODNJI-Knavs-podpis (KOREKCIJA-P219-lead: Knavs-morda-ŽE-DEC-1857 — X-open!) + starost-73J = NAJSTAREJŠI-Griblje-1857!"},
}

entries = []
for sken, zlist, op, mode in PLAN:
    d = json.load(open(f"{TMP}/vlm-page/s{sken}.json"))
    vrste = d.get("vrstice", [])
    realne = []
    for x in vrste:
        ime = (x.get("ime") or "").strip()
        vas = (x.get("vas") or "").strip()
        mes = (x.get("mesec") or "").strip()
        smrt = (x.get("smrt") or "").strip()
        pokop = (x.get("pokop") or "").strip()
        if not ime and not vas:
            continue
        if not mes and not smrt and not pokop:
            continue
        realne.append(x)
    if mode == "tail2":
        pool = [x for x in realne if 1 <= (x.get("vrsta") or 0) <= 2]
    else:
        pool = realne
    want = len(zlist)
    if len(pool) != want:
        print(f"⚠ s{sken}: pričakovano {want}, najdeno {len(pool)} (VLM-n={len(vrste)})")
    for i, x in enumerate(pool[:want]):
        x = dict(x)
        x["z"] = zlist[i]
        x["sken"] = sken
        # pag = sken−1 = svinčnik-foliacija-arhivarja (dokumentirano: s4='3', s5='4', s7='6'!)
        x["pag"] = sken - 1
        x["vrsta_sken"] = x.get("vrsta")
        x["ord_opomba"] = op
        znum = int(str(zlist[i]).replace("z", ""))
        k = KROP.get(znum)
        if k:
            for kk, vv in k.items():
                if kk == "_opomba":
                    x["krop_opomba"] = vv
                else:
                    x[kk] = vv
            x["krop"] = True
        entries.append(x)

# --- mesec-zapuščanje (kontekst) ---
prev_mes = None
for e in entries:
    mm = (e.get("mesec") or "").strip()
    if mm and mm != "—" and not mm.startswith("("):
        prev_mes = mm.split()[0]
    elif not mm or mm == "—":
        if prev_mes:
            e["mesec"] = f"{prev_mes} [kontekst-zapuščanje!]"
            e["mesec_deduced"] = True

# --- normalizacija hišnih ---
import re as _re
for e in entries:
    h = str(e.get("hisna") or "").strip()
    mfirst = _re.match(r"^(\d+)", h)
    if h and mfirst and not h.startswith("[?]"):
        clean = mfirst.group(1)
        if clean != h:
            e["hisna_duel"] = h
            e["hisna"] = clean

# --- statistika ---
meseci_all = {}
for e in entries:
    m = (e.get("mesec") or "").strip().split()[0] if (e.get("mesec") or "").strip() else "?"
    m = m.replace("[kontekst-zapuščanje!]", "").strip() or "?"
    m = {"Januar": "J", "Jänner": "J", "Februar": "F", "Feber": "F", "März": "M", "April": "A",
         "Mai": "M2", "Mai/Juni": "M2", "Juni": "J2", "July": "J3", "August": "A2", "September": "S",
         "October": "O", "November": "N", "December": "D"}.get(m, m)
    meseci_all[m] = meseci_all.get(m, 0) + 1

grib = [e for e in entries if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]

out = {
    "faza": "P220",
    "leto": 1857,
    "knjiga": "04106",
    "okvir": {"skeni": "s001–s007 (7 svežih 2×-md5-NEODVISNA-PRENOSA-7/7 — SANDI-REZET-RESTART; s001 = NASLOVNI-LIST-'Tom. III'-'Sterb-Buch'-'Podzemelj' — 0-vrstic!)",
              "okno_1857": "s002–s007 (6 skenov: KNJIGA-START + celo leto + TAIL-1857!)",
              "pag": "sken − 1 = SVINČNIK-FOLIACIJA-ARHIVARJA (dokumentirano-3×: s4='3', s5='4', s7='6'-P219!) — ★ KONVENCIJSKI-PREHOD: KORPUS-sken−5-NEMOŽEN-za-s1–s5 (negativne-strani!) — prehod-dokumentiran-v-glavi-blokov!",
              "knjiga_start": "★★★ KNJIGA-04106-SE-ZAČNE-1857: s1-NASLOVNI-LIST ('Tom. III'-rokopisno + 'Sterb-Buch' + 'Podzemelj'!) + s2-RAZPRTA-NASLOVNA + '18 57'-RAZPETA-letnica-glava (rokopisna-nadčrtana! — P214-TIP-sorodna-razpeta-cifra!) + restart-z1 — BREZ-taila-1856 (knjiga-se-nadaljuje-v-novo-knigo-1856/57? X-open!)",
              "meja_1856_57": "NE-OBSTAJA-v-04106 (knjiga-se-začne-1857!) — '18 57'-glava = KNJIGA-START-marker!",
              "meja_1857_58": "s7 (P219-potrjeno + re-križ-P220-arb_s7_meja-1:1: TAIL-z73–z74 + DVOJNA-ČRTA + VSOTNA-'1 8 5 [8]'-RAZPETE-P214-TIP-3.-INSTANCE ('1-8'-jasno + '5'-v-starostnem-stolpcu-vidno-tudi-v-P220-kropu!) + rokopisna-'Jänner-1858'-glava + restart-z1–z11 + NEŠTEVILČENA-zadnja!) = 59.-POTRDITEV-invariante!",
              "luknja_32": "★★★ LUKNJA-32 (pisarski-preskok — 3.-instance-v-knjigi-po-LUKNJA-92-1859!): s3-ordinalni-stolpec-KONČA-z-31 (15-ordinalov-17–31!) + s3-dno-RAZPRAZNO (y0.925–1.0 — 3-kropi-brez-vsebine!) + s4-ZAČNE-z-33 (Juni-21./23.!); kronološki-seam-z31-Juni-21/22 → z33-Juni-21/23-GLADAK! — X-open: morda-32-obrezan-na-dnu-s3 (tabela-se-konča-na-scan-rob!)",
              "vrstna_aritmetika": "16+15+13+13+14+2 = 73 (kronološko; WRITTEN-1–31 + 33–74 = 73-ČISTO-brez-dvojnih-luknij — 1-LUKNJA-32!); meseci J4+F8+M5+A5+M7+J3+J6+A18+S8+O0!!+N5+D4",
              "oktober_luknja": "★★★ OKTOBER-1857-×0 (celotna-župnija!): z65-Sep-24/26 → z66-Nov-9/11 — 15-dnevna-luknja-brez-vpisa — edini-mesec-×0-v-1857 (X-open: z66-'November'-glava-2×-križ!)",
              "scarlatina_klaster": "★★★ SCARLATINA?-EPIDEMIJA-klaster: 'Rušfieber/Rušenfleck'-×6–7 (z36-July-24 → z46-Aug-12!) + 'Amigdilitis[?]'-garble-×7 (s5: z48–z57!) — isti-garble-družina?-2.-val?-X-open — 13–14-vpisov-v-6-tednih — 1-GRIBLJE-v-klasterju (z45-Rušfieber!)",
    },
    "statistika": {"vpisov_1857_kronolosko": len(entries),
                   "vpisov_written": 73,
                   "luknij": 1,
                   "griblje": len(grib),
                   "hise": len({e.get("hisna") for e in grib}),
                   "meseci": meseci_all},
    "krop_vizualne": [{"z": z, **{k: v for k, v in k.items() if not k.startswith("_")}} for z, k in sorted(KROP.items())],
    "anomalije_ordinali": "★★★ 1-ANOMALIJA-1857: LUKNJA-32 (pisarski-preskok! — ordinali-1–31 + 33–74 ČISTO, 32-NI-vpisana!) — cf.-LUKNJA-92-1859! + NEŠTEVILČENA-1858-restart-s7 (P219!)",
    "entries": entries,
    "griblje_entries": grib,
    "leadP221": "PREDZGODOVINA-LINIJA-04106-KONČANA (29/29!) → NASLEDNJA-FAZA: krstna-04104-PREDZGODOVINA (1871–1885, 15-let — ×200-skenov-čaka! P196-worklog-lead!) — pričakovani-start: 1885 (1/15) po-descending-vzorca-mrliške-predzgodovine; s-proba-potreben (krstna-04104-obdobje-na-Matriculi!)",
}
json.dump(out, open(f"{TMP}/entries_1857.json", "w"), ensure_ascii=False, indent=1)
print(f"1857: {len(entries)} kronoloških (73-written + LUKNJA-32!) / {len(grib)} Griblje / {len({e.get('hisna') for e in grib})} hiš")
print("meseci:", meseci_all)
print("Griblje z:", [e["z"] for e in grib])
print("Griblje hiše:", [e.get("hisna") for e in grib])
