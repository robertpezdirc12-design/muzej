#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P219 — agregacija 58-vpisov leta 1858 (ŠTEVJE-IZ-VRSTIC-21.×!).
MEJA-1857/58 = s7: TAIL-1857 (z73–z74: 2-vrstici — Gradac + ★ GRIBLJE-h36!) + DVOJNA-ČRTA +
VSOTNA-'1 8 [5 8]'-RAZPETE-MARKER (P214-TIP-3.-INSTANCE!) + RESTART-z1–z11 (11!) +
★★★ NEŠTEVILČENA-ZADNJA-VRSTICA-s7 (Jan-29/31-Gradac-12-Ivan[?]-Mali — levi-stolpec-PRAZEN!
KROP-potrjeno-2.×!) — duhovnik-skoči-nepreštevano! → s8-z12 = '1.-Feb'!
ČISTA-ORDINALNA-LINIJA-1–57 (BREZ-luknij!): s8-z12–z25 (14) + s9-z26–z39 (14) + s10-z40–z53 (14)
+ s11-tail-z54–z57 (4; P218-KROP-potrjeno!) = 57-written + 1-NEŠTEVILČENA = 58-kronološko!
★★★ s9 + s10 = NASLOVNA-LISTA-'Sterb-Buch.'-RAZPRTE (quiri-prelom-sredi-1858!) — page-VLM-na-s10
ujel-LE-4/14-vrstic ('30–33'-MISREAD!) — KROP-zap-stolpci-POTRDILI-40–53-ČISTO (moji-oči-1:1!)!
★★★ 10-GRIBLJE / 8-hiš (h19-×3: DVOJČKI-Simic-z16+z17 + Kurič-z27!) + h50-PEZDIRC-MREŽA-'Padire'!
+ FRAISEN/GAUFIGALBRANN-nit-×4 (z15/z16/z17/z27 — Feb-Apr!) + otroška-umrljivost-50%-5/10!
Izhod: /tmp/p219/entries_1858.json"""
import json

TMP = "/tmp/p219"
# (sken, z-list, opomba, vrsta_start-za-pool-filter)
PLAN = [
    (7, [f"z{i}" for i in range(1, 12)] + ["z12a-NEŠTEVILČENA"],
     "s7-RESTART-1858-z1–z11 (11) + ★★★ NEŠTEVILČENA-ZADNJA (Jan-29/31 — kronološko-#12! KROP-2.×-PRAZNO!)",
     4, None),   # page-vrstice 4–15 = restart
    (8, [f"z{i}" for i in range(12, 26)],
     "s8-z12–z25 (14; NASLOVNI-LIST-'Sterb-Buch.' + diagonalna-'1858'-glava-KROP!; ★ 3-GRIBLJE: z15-h49-Anna-Radine-19J + z16/z17-DVOJČKI-Simic-h19-Genickfand!)",
     1, None),
    (9, [f"z{i}" for i in range(26, 40)],
     "s9-z26–z39 (14; NASLOVNI-LIST + diagonalna-'1858'-glava-KROP-glyph-8-BREZ-repa!; ★ 3-GRIBLJE: z27-h19-Kurič-7-mj-FRAISEN + z37-h60-Tomcsinič-60J + z39-h65-Keržan[?]-NOV-DUHOVNIK-Auber[?]-DUEL!)",
     1, None),
    (10, [f"z{i}" for i in range(40, 54)],
     "s10-z40–z53 (14; NASLOVNI-LIST! page-VLM-ujel-LE-4/14-'30–33'-MISREAD → KROP-zap-POTRJENO-40–53-ČISTO-1:1!; ★ 4-GRIBLJE: z42-h3-Križan[?]-Kind + z47-h2-Fenz + z51-h44-Strucel[?] + z52-h50-Padire-PEZDIRC-MREŽA!)",
     1, "MANUAL"),
    (11, [f"z{i}" for i in range(54, 58)],
     "s11-z54–z57-TAIL-1858 (4; KROP-P218-potrjeno! re-križ-P219-arb_s11_meja-1:1-struktura: Zemelj + Krasinec-×2 + Gradac — 0-GRIBLJE!; nato-VSOTNA-'1 8 [5 9]'-marker + restart-1859 = P218!)",
     1, "TAIL4"),
]

# KROP-overrides + duels za 10-GRIBLJE-vrstic (triangulacija: page-VLM + traki + krop-VLM + glyph-viz!)
KROP = {
    15: {"hisna": "49 [duel-19-page-VLM/44-krop-VLM — KURRENT-1/4/9-ZMEDA!]",
         "ime": "Anna Radine [~Radin]",
         "stan": "½ Gütl-Mächen [~Gütlers-Mädchen]",
         "starost": "19 let",
         "bolezen": "Gaufigalbrann [?X-open-garble — Gichterbrand?-hipoteza!]",
         "_opomba": "★ h49-NIT-1858-1/2 (z15-Anna-'Radine'[?]-19J + z94-1859-Padierž-14-DNI — BRODARIČ-hiša!) + GAUFIGALBRANN-nit-1/4 (z15/z16/z17-ist-garble! Feb-20–26-klasterr!) + Joh.-Knavs-podpis-1:1!"},
    16: {"ime": "Ana Simic [~Somic]",
         "stan": "[?]",
         "starost": "2 dni",
         "bolezen": "Gaufigabrannt [?X-open — isti-garble-kot-z15! Genickfand[?]-družina!]",
         "_opomba": "★★★ DVOJČEK-1/2 (z16+z17-ZWILLINGE-h19!) + GAUFIGALBRANN-nit-2/4 + h19-DRAMA-nit (1858-×3 → 1859-×2-Križič/Hrič!) + Joh.-Knavs-1:1!"},
    17: {"ime": "Mannier [?X-open-DUEL-Marja[?]] Simic",
         "stan": "zwilling-Genickfand[?]-kinden [2-vrstica — ZWILLING-oznaka!]",
         "hisna": "19 [dto-z16!]",
         "vas": "Griblje [dto-z16!]",
         "starost": "½-dni [?dto-glyph-duel-X-open!]",
         "bolezen": "dto. (= Gaufigabrannt[?])",
         "_opomba": "★★★ DVOJČEK-2/2 (ZWILLINGE! — 'zwilling-Genickfand-kind'-2-vrstica!) + GAUFIGALBRANN-nit-3/4 + pokop-duel (26[?]-vs-23/30) + Joh.-Knavs-1:1!"},
    27: {"ime": "Jožef Kurič [TRI-DUEL-X-open: Kurič[page]/Kreite[t1-trak]/Krix[arb-glava]/Petrič[krop-VLM]!]",
         "stan": "½ Güblers-sohn [~duel-Bolnar-krop-garble!]",
         "starost": "7 mesecev",
         "bolezen": "Fraisin [~ — FRAISEN!]",
         "_opomba": "★ h19-DRAMA-3/3 (dvojčka + Kurič — 3-otroška-smrti-h19-v-1858!) + ★ FRAISEN-nit (→ 1859-Jän-PARIČ-klaster-×2-P218! čez-mejo-nadaljevanje!) + ime-TRI-DUEL + Joh.-Knavs!"},
    37: {"ime": "Jakob Tomcsinič [~Tomecšinc-page-duel!]",
         "stan": "gorn. [?]-Gäbjsfawn [garble-X-open]",
         "starost": "60 let",
         "bolezen": "Abzehrung",
         "_opomba": "★ h60-TOMINC-nit (1858-z37-Jakob-60J → 1881-z?-Katharina-TOMINC-Müllerjeva-vdova!) + Joh.-Knavs-podpis-1:1!"},
    39: {"ime": "N. Keržan [TRI-DUEL-X-open: Keržan[glif-viz]/Kerzmann[krop-VLM]/Deželak[?page-VLM]!]",
         "stan": "invalid [?] ½-göblin [garble-X-open]",
         "starost": "0 [?starost-nezapisana/duel!]",
         "bolezen": "Gaufgeburt [?X-open-garble]",
         "_opomba": "★★★ NOV-DUHOVNIK-DUEL: 'J.-Auber[?]/Huber[?]-P.'-podpis-4×-zoom (vs-Joh.-Knavs-dominanta + Šinkovec[?page-garble]!) + h65-MILEK-hiša (P155-1889!) + ime-TRI-DUEL"},
    42: {"ime": "N. Križan [TRI-DUEL-X-open: Križan[krop+glif]/Horvat-Vozan[page]!]",
         "stan": "ein Kind von Gribl [~]",
         "starost": "0 [?duel-1-J-6-M-krop!]",
         "bolezen": "Gefrorn-fallbrenning [?X-open-garble]",
         "_opomba": "★ h3-KRIŽAN-nit-1/3 (1858-z42-Kind → 1865-Maria-Križan → 1882-Dorothea-VRIŽAN + 04894-KRIŽAN-×4-1887–1917!) + starost-'0'-duel + Joh.-Knavs-1:1!"},
    47: {"ime": "Margaretha Fenz [~Fanz]",
         "stan": "½ Güblers-tojdan [?Tochter-garble-X-open!]",
         "starost": "8 tednov [?duel-8-Mg!]",
         "bolezen": "Swajzne [?≈Schwäche-garble]",
         "_opomba": "★ h2-KLEPEC/HLEBEC-nit (1858-z47-otrok → 1864/67/71-Klepec-×3 → 1880/81!) + otroška-umrljivost + Knavs-grafija-'Khubiz'-varianta!"},
    51: {"ime": "Anna [2×-krop+glif!]-vs-Anton[page]-DUEL Strucel [~Strocel/Strovs-page-duel!]",
         "stan": "½ Gribl-sonnb [?Gäblers-sohn-garble-X-open!]",
         "starost": "18 let",
         "bolezen": "Brustbrafbrand [?≈Brustbrand/Brustkrankheit-garble-X-open!]",
         "_opomba": "★ h44-ŠTRUCELJ-nit-1/3 (1858-z51-18J → 1867-Matija-Strucež-1½J → 1873-Barbara-Struzelj + 04894/04455/04105-Štrucelj-mreža!) + ime-spol-DUEL (Anna-vs-Anton!)"},
    52: {"ime": "Maria [glif+page!]-vs-Martin[krop-VLM]-DUEL Padire [PEZDIRC-MREŽA-grafija! — Radire[?]-duel!]",
         "stan": "½ Gübl-poffn/tohta [garble-X-open!]",
         "starost": "68 let [duel-8[?]/43[?]/87[?]]",
         "bolezen": "?-fall [garble-X-open: Wassfall[?≈Wassersucht]/Lungafall[?]]",
         "_opomba": "★★★ PEZDIRC-MREŽA-NAJGLABLJE: 'Padire'-h50 (1858) → 1868-Perdirc → 1872-Kerdise-PEZDIR → 1924-PERDIRC-POSESTNIK — 4-generacijska-grafija-linija-×4! + h50-nit + podpis-duel (Knavs-vs-Vinaus[?])"},
}

entries = []
for item in PLAN:
    sken, zlist, op, vrsta_start, mode = item
    if mode == "MANUAL":
        vrste = json.load(open(f"{TMP}/s10_manual.json"))
    else:
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
        zap = str(x.get("zaporedna", "")).lower()
        if "vsota" in zap or zap.strip() in ("—", ""): 
            # s7-zadnja NEŠTEVILČENA: vrstica brez številke a z vsebino — pusti če je s7-zadnja
            if not (sken == 7 and (x.get("vrsta") or 0) == 15): continue
        realne.append(x)
    want = len(zlist)
    pool = [x for x in realne if (x.get("vrsta") or 0) >= vrsta_start]
    if mode == "TAIL4":
        pool = [x for x in realne if 1 <= (x.get("vrsta") or 0) <= 4]
    if len(pool) != want:
        print(f"⚠ s{sken}: pričakovano {want}, najdeno {len(pool)} (VLM-n={len(vrste)})")
    for i, x in enumerate(pool[:want]):
        x = dict(x)
        x["z"] = zlist[i]
        x["sken"] = sken
        x["pag"] = {4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None, 11: 6}.get(sken)
        x["vrsta_sken"] = x.get("vrsta")
        x["ord_opomba"] = op
        k = KROP.get(i + {"7": 1, "8": 12, "9": 26, "10": 40, "11": 54}[str(sken)])
        # KROP-ključi so absolutne z-številke: poskobi direktno
        znum = int(str(zlist[i]).replace("z", "").replace("a-NEŠTEVILČENA", "").split("-")[0]) if not str(zlist[i]).startswith("z12a") else None
        k = KROP.get(znum)
        if k:
            for kk, vv in k.items():
                if kk == "_opomba": x["krop_opomba"] = vv
                else: x[kk] = vv
            x["krop"] = True
        if str(zlist[i]).startswith("z12a"):
            x["z"] = "12a-NEŠTEVILČENA"
            x["nesteviceena"] = True
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
    if h and mfirst:
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
         "Mai": "M2", "Juni": "J2", "July": "J3", "August": "A2", "September": "S",
         "October": "O", "November": "N", "December": "D"}.get(m, m)
    meseci_all[m] = meseci_all.get(m, 0) + 1

grib = [e for e in entries if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]

out = {
    "faza": "P219",
    "leto": 1858,
    "knjiga": "04106",
    "okvir": {"skeni": "s004–s011 (8 svežih 2×-md5-NEODVISNA-PRENOSA-8/8 — SANDI-REZET-RESTART; s004–s006 = 1857-tail-proba za-P220-lead!)",
              "okno_1858": "s007–s011 (5 skenov: MEJA-tail + restart + celo leto + tail-1858!)",
              "meja_1857_58": "s7 (NASLOVNI-LIST-'Sterb-Buch.'-RAZPRTA + TAIL-1857-z73–z74 (2-vrstici: Gradac + ★ GRIBLJE-h36-Krisan[?]-73J — 1857-zadnji-Griblje!) + DVOJNA-ČRTA + VSOTNA-'1 8 [5 8]'-RAZPETE-MARKER (P214-TIP-3.-INSTANCE: '1-8'-jasno + '5'-v-Alter-stolpcu-KROP!) + rokopisna-'Jänner-1858'-glava-KROP + restart-z1–z11 (11!) + ★★★ NEŠTEVILČENA-ZADNJA-VRSTICA (Jan-29/31 — levi-stolpec-PRAZEN-KROP-2.× — 2.-instance-v-korpusu-po-P218-s15-Jalkič!) = 57.-POTRDITEV-invariante!)",
              "meja_1858_59": "s11 (P218-potrjeno: tail-54–57 + VSOTNA-'1 8 [5 9]'-marker + restart-1859 — re-križ-P219-arb_s11_meja-1:1!) = 58.-POTRDITEV!",
              "naslovna_lista_×3": "★★★ s9 + s10 = NASLOVNA-LISTA-'Sterb-Buch.'-RAZPRTE-SREDI-1858 (quiri-prelom!) + s7 — page-VLM-na-s10-ujel-LE-4/14-vrstic ('30–33'-MISREAD → KROP-zap-ČISTO-40–53!) — 1859-s19-paralela!",
              "vrstna_aritmetika": "11+1(NEŠTEVILČENA!)+14+14+14+4 = 58 (kronološko!; written-1–57-ČISTO-BREZ-luknij — ČISTA-ORDINALNA-LINIJA! — nasprotje-1859: 103-vpisov-z-LUKNJO-92!)"},
    "statistika": {"vpisov_1858_kronolosko": len(entries),
                   "vpisov_written": 57,
                   "nesteviceenih": 1,
                   "griblje": len(grib),
                   "hise": len({e.get("hisna") for e in grib}),
                   "meseci": meseci_all},
    "krop_vizualne": [{"z": z, **{k: v for k, v in k.items() if not k.startswith("_")}} for z, k in sorted(KROP.items())],
    "anomalije_ordinali": "★★★ 1-ANOMALIJA-1858: NEŠTEVILČENA-ZADNJA-VRSTICA-s7 (Jan-29/31 — duhovnik-prišel-do-roba-strani-in-NE-ŠTEVILČEVAL — s8-z12-nadaljeval!; 2.-instance-po-P218-s15-Jalkič!) — ordinali-1858-drugače-ČISTO-1–57 (BREZ-luknij — nasprotje-1859-LUKNJA-92!)",
    "entries": entries,
    "griblje_entries": grib,
    "leadP220": "1857 — s004–s006-ŽE-PRENESNI (2×-md5!) + s004-VLM-ŽE (z33–z45: 13-vrstic — Juni–August-1857!) + s005-ŽE (z46–z58: 13!) + s006-ŽE (z59–z72: 14!) → s003-nazaj-proba (1857-začetek — restart-po-1856-tailu? knjiga-04106-SE-ZAČNE-1857 — morda-naslovni-list-s001–s003!) + tail-1857-ŽE-KROP'd (s7-z73–z74: Gradac + GRIBLJE-h36!)",
}
json.dump(out, open(f"{TMP}/entries_1858.json", "w"), ensure_ascii=False, indent=1)
print(f"1858: {len(entries)} kronoloških (57-written + 1-NEŠTEVILČENA) / {len(grib)} Griblje / {len({e.get('hisna') for e in grib})} hiš")
print("meseci:", meseci_all)
print("Griblje z:", [e["z"] for e in grib])
print("Griblje hiše:", [e.get("hisna") for e in grib])
