#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P218 — agregacija 103 vpisov leta 1859 (ŠTEVJE-IZ-VRSTIC-20.×!).
s11 = MEJA-1858/59: NASLOVNI-LIST-'Sterb-Buch.'-deel-2 (NOVI-TISKANI-STOLPCI!) + '1858'-tail-glava
(KROP!) + tail-54–57 (4; 1858!) + DVOJNA-ČRTA + VSOTNA-'1 8 [5 9]'-RAZPETE-MARKER (P214-TIP! 1-8-KROP +
5-rob!) + restart-z1–z7 (7; z7 = Februar!). BREZ-Ločne-'1859'-glave — marker = vsotna!
s19 = NASLOVNI-LIST-'Sterb-Buch.'-PONOVLJEN (nov-zvezek-quire!) + Dec-1859-nadaljevanje 93–103
(brez-restarta!) — ★★★ LUKNJA-92 (s18-konča-91 → s19-začne-93!)!
★★★ s15-r12-Jalkič = NEŠTEVILČENA (duhovnik-je-skočil: 55 → [r12-brez-št.] → 56-na-s16!)!
 ordinali-1859-NI-ČISTO (2-anomaliji: NEŠTEVILČENA + LUKNJA-92! — ŠTEVJE-IZ-VRSTIC-še-vedno-EXAKT-103!)
★★★ P217-TAIL-MISREADI-KOREKCIJE (s19-nikoli-KROP'd!): z95→z94 + z100→z97 (marginal!) + 'Petek'→
 'Padierž[?]' + '16J'→'14-DNI' + 'Valentin-Brino'→'⅄onalfur[?Valentin?]-Brince[~]'
★★★ 23-GRIBLJE = NOV-REKORD-PREDZGODOVINE (prej-20-1867!) / 16 hiš (6-×2!) + GENICKSTARRE-EPIDEMIJA ×4
 + NOV-DUHOVNIK-'Joh.-Knavs' (podpisi-×7+) + z5+z6-PARIČ-FRAISEN-klaster-×2!
Izhod: /tmp/p218/entries_1859.json"""
import json

TMP = "/tmp/p218"
# (sken, vrsta_range_zaporedje, opomba)
PLAN = [
    (11, list(range(1, 8)), "z1–z7-RESTART-1859 (MEJA-1858/59-s11 = NASLOVNI-LIST-'Sterb-Buch.'-deel-2! + '1858'-tail-glava-KROP + tail-54–57-1858 + VSOTNA-'1 8 [5 9]'-RAZPETE-MARKER-P214-TIP + restart-BREZ-Ločne-glave!; z7 = Februar!; ★ 1-GRIBLJE: z6-h69-Parič-1J-Fraisin + ★★ z5+z6-PARIČ-FRAISEN-klaster-×2-Jän-27/29!)", 6),
    (12, list(range(8, 20)), "z8–z19 (12; KROP-stolpec-8–19-ČISTO!; r13 = VLM-duplikat-halucinacija-SKIP!; z17/z18-Lemež-Smajo-46/33-DUEL-X-open; ★ 3-GRIBLJE: z9-h21-Pirczl-80J + z16-h37[~17!]-TRI-GARBLE + z19-h39-Stähler-10-mj)", 1),
    (13, list(range(20, 34)), "z20–z33 (14; KROP-stolpec-20–33-ČISTO!; ★★★ GENICKSTARRE-EPIDEMIJA ×4: z24+z25+z31+z32 (Apr-16→Mai-21)! + ★ 4-GRIBLJE: z24-h65-Graes-2-tedna + z25-h57-Keržan-63J + z31-h5-Trnovec-1-mj + z32-h19-Križič-40J!)", 1),
    (14, list(range(34, 45)), "z34–z44 (11; margins-bracket-KROP: s13-konča-33 + s15-začne-45!; ★★ 2-GRIBLJE-ISTA-DATA-Mai-28/30: z34-h26-Kure-80J + z35-h58-Stracina-Leg.Kind-—! + h58-POŽEK-nit!)", 1),
    (15, list(range(45, 56)), "z45–z55 (11; KROP-stolpec-45–55-ČISTO!; ★ 3-GRIBLJE: z46-h52-Peterle-47J + z52-h39-Simic-ŠIMEC-grafia! + z53-h5-Strucelj-3-mj!)", 1),
    (16, list(range(56, 68)), "z56–z67 (12; KROP-stolpec-56–67-ČISTO!; ★ 4-GRIBLJE: z57-h19-Hrič-28J + z61-h33-Ulasič-VOJAK! + z64-h74-Brenc-76J + z65-h29-Miličk-5J!)", 1),
    (17, list(range(68, 80)), "z68–z79 (12; KROP-stolpec-68–79-ČISTO!; ★ 2-GRIBLJE: z73-h20-Klara[?]-Podire-23J + z76-h24-Milich-TRI-ime-DUEL!)", 1),
    (18, list(range(80, 92)), "z80–z91 (12; KROP-stolpec-80–91-2.×-POTRDITEV-P217!; ★ 2-GRIBLJE: z81-h52-Posdiac-99J[~83!]-TRAJNI-DUEL + z86-h21-Požekh[~Poček]-69J-Anastasia[?]-DUEL!)", 1),
    (19, list(range(93, 104)), "z93–z103-TAIL-NA-NASLOVNEM-LISTU (11; KROP-stolpec-93–103-ČISTO! LUKNJA-92!; 'Sterb-Buch.'-PONOVLJEN + Dec-1859-nadaljevanje-BREZ-restarta!; ★ 2-GRIBLJE: z94-h49-Padierž[?]-14-DNI-P217-FALSIFIKACIJA! + z97-h65-Brince-58J!)", 1),
]

KROP = {
    6: {"ime": "Marko [~VLM]-vs-'Marlfaud'[?KROP-row]-DUEL-X-open Parič [~Pašč?]",
        "stan": "[garble-X-open: 'iz-Griblja-Anton?-Jože?'[VLM]-vs-'½-Güblerskopfa-Wifn'[?KROP-row]!]",
        "starost": "1 leto [~]",
        "bolezen": "Fraisin [~]",
        "_opomba": "★★ z5+z6-PARIČ-FRAISEN-klaster-×2-ISTA-DATA-Jän-27/29 (Marija-Vranoviče-h15-10-tednov + Marko-Griblje-h69-1J!) + h69-NIT (P155-1889-h69-Brinec-Janez-16-DNI!) + NOV-DUHOVNIK-'Joh.-Knavs'-podpis!"},
    9: {"ime": "Korencij Pirczl [~Korenclj?]",
        "stan": "vdovec (ovd. kmet) + 'Dragos [?]' — stan-2-del-garble",
        "starost": "80 let [~]",
        "bolezen": "Gallensteine [~ — garble-X-open (Gallsteine/Gallnfieber? — nemško-v-slovenski-knjigi!)]",
        "_opomba": "★★ h21-NIT-1859 (z9-Pirczl-80J + z86-Požekh-69J!) + 80-J-DUEL-z34 (Anna-Kure-h26-tudi-80J!)"},
    16: {"ime": "[TRI-GARBLE-X-open: 'N.-Hosez/Anzujkar-Diwit'[VLM]-vs-'N.-Haus'[KROP-row]!]",
         "hisna": "37 [duel-'17'-KROP-row — 3/7-KURRENT-ZMEDA!]",
         "starost": "10 let [?]",
         "bolezen": "Ausgabust [~ — 'Sušica?'-hipoteza-VLM; garble]",
         "_opomba": "★ h37-DUEL (37[2×-VLM]-vs-17[KROP-row] — 3/7-KURRENT!) + TRI-GARBLE-ime-X-open + h37-NIT (P212-1865-HUSIČ-h37!)"},
    19: {"ime": "Rudolfina Stähler [~Stelzer?]",
         "stan": "hči hlapca Jožefa [?]",
         "starost": "10 mesecev [~]",
         "bolezen": "Gichtern [~ — 'griža?'-hipoteza-VLM]",
         "_opomba": "★ h39-NIT-1859 (z19-Stähler-10-mj + z52-Simic-54J!) + RUDOLFINA-×3-v-1-mesecu (z3?/z10-Krasinec-37J + z19! — P216-h42-družina-hipoteza-vzorec!)"},
    24: {"ime": "Anton Graes [~Gras?] von Griblje",
         "stan": "Witwer [~]",
         "starost": "2 tedna [~]",
         "bolezen": "Genickstarre [~]",
         "_opomba": "★★★ GENICKSTARRE-EPIDEMIJA-1/4 (Apr-16→Mai-21-×4!) + ★ h65-NIT-1859-1/2 (z24-Graes-2-tedna + z97-Brince-58J!) + 'von-Griblje'-dvojna-lokalna-oznaka!"},
    25: {"ime": "Anna Keržan [~Križan-KROP-row-duel!]",
         "stan": "Weberstochter",
         "starost": "63 let [~]",
         "bolezen": "Genickstarre [~]",
         "_opomba": "★★★ GENICKSTARRE-EPIDEMIJA-2/4 + ★ h57-NIT (1859-z25-Keržan-63J → 1860-z69/z70-VALENTIN-×2-h57!) + ime-DUEL (Keržan/Križan!)"},
    31: {"ime": "Georg Trnovec [~Struchl-KROP-row-duel!]",
         "stan": "unverehelicher Knabe",
         "starost": "1 mesec",
         "bolezen": "Genickstarre [~]",
         "_opomba": "★★★ GENICKSTARRE-EPIDEMIJA-3/4 + ★ h5-NIT (1859-×2: z31-Trnovec-1-mj + z53-Strucelj-3-mj!; P215-1862-FILAK-h5!) + nezakonski-otrok (unverehelich!)"},
    32: {"ime": "Ana Križič [~Kerc-KROP-row-duel!] von Griblce [~Griblje?]",
         "stan": "[?]",
         "starost": "40 let [~]",
         "bolezen": "Genickstarre [~]",
         "_opomba": "★★★ GENICKSTARRE-EPIDEMIJA-4/4 (ODRASLA-40J!) + ★ h19-NIT-1859 (z32-Križič-40J + z57-Hrič-28J — KRIŽIČ/HRIČ-2-branji-ista-hiša!) + 'von-Griblce'-dvojna-oznaka"},
    34: {"ime": "Anna Kure [~Kur?]",
         "stan": "Lastnica [~]",
         "starost": "80 let",
         "bolezen": "Altersschwäche [~]",
         "_opomba": "★ h26-NIT (1859-z34-Kure-80J-Lastnica → 1861-P216-MALEŠIČ-h26-NOVA-z30!) + ISTA-DATA-kot-z35 (Mai-28/30-×2!) + 80-J-DUEL-z9 (Pirczl!)"},
    35: {"ime": "A. Stracina [~Stracina?] iz željk [?Otok?]",
         "stan": "Leg. Kind [~ — legitimes Kind!]",
         "starost": "—",
         "bolezen": "Friesen [~]",
         "_opomba": "★★ h58-NIT-1-LETO-PRED-POŽEKOM (1859-z35-Leg.Kind-— → 1860-z27-Barbara-Požek-8-mes — ISTA-HIŠA!) + ISTA-DATA-kot-z34 (Mai-28/30!) + starost-PRAZNA"},
    46: {"ime": "Anton Peterle",
         "stan": "[garble — 'mlad Koleđal(?)'[VLM]-X-open]",
         "starost": "47 let",
         "bolezen": "Lungenentzündung [~]",
         "_opomba": "★ h52-NIT-1859-1/2 (z46-Peterle-47J + z81-Posdiac-99J!) + JULI-luknja (Juni-0-GRIBLJE!)"},
    52: {"ime": "Anton Simic [~Šimec-grafia-INNEC! — cf.-P200-h18-INNEC-lekcija!]",
         "stan": "v Gribljem",
         "starost": "54 let",
         "bolezen": "Gicht...[? — garble]",
         "_opomba": "★ h39-NIT-1859-2/2 + ★ ŠIMEC-grafia (Simic→Šimec!) + AUGUST-klaster-1859 (×6-GRIBLJE!)"},
    53: {"ime": "Gregor Strucelj [~Struclj?]",
         "stan": "[garble — 'infulat(?) Bond(?)'[VLM]-X-open]",
         "starost": "3 mesece",
         "bolezen": "Blenmorrea [~ — Blennorrhoe?-hipoteza]",
         "_opomba": "★ h5-NIT-1859-2/2 (z31 + z53!) + NOV-VZROK-v-korpusu (Blenmorrea[~]!)"},
    57: {"ime": "Antončina Hriče [~Hrič]",
         "stan": "hči Jožefa Hriča, kmeta [~ + 'Griblč. Ponik[?]'-garble]",
         "starost": "28 let",
         "bolezen": "Marktsfreibn [~ — Marbmil?-hipoteza]",
         "_opomba": "★ h19-NIT-1859-2/2 (z32-Križič + z57-Hrič!) + ★★ MARKTSFREIBN-×2-z-2-DNI (z57-Aug-14 + z65-Aug-28 — NISMO-×2-v-2-dneh: 14-dni-apart! — PARALELA-VZROK-×2!) + ime-Antončina (ženska!)"},
    61: {"ime": "Matthias Ulasič [~Ulašič?]",
         "stan": "Lediknant (vojak) [~ — 1. VOJAK-stan-v-predzgodovini!]",
         "starost": "44 let 10 mj.",
         "bolezen": "Harnblutungsfieber [~], bena[? — 2-vrstični-garble]",
         "_opomba": "★ h33-NIT (1859-z61-Ulasič-VOJAK → 1863-P214-FILAK-Grem-h33-×2!) + ★ 1. VOJAK (Lediknant!)-stan-mrliške-predzgodovine + NAJBOGŠEJŠI-starost-format ('44 let 10 mj.'!)"},
    64: {"ime": "Barbara Brenc [~Brenc?]",
         "stan": "[garble — 'dečka Brenczova, besittng: benin[?]' — X-open]",
         "starost": "76 let",
         "bolezen": "Altersschwäche",
         "_opomba": "★ h74-NOVA-HIŠA-korpusa (1859-z64-76J!) + BRENC-nit (1860-z61-h24-Brenc[~Brinar?]-23J!)" },
    65: {"ime": "Maria Miličk [~Miličk/Milikič?]",
         "stan": "žena [~ + 'Gößl. Aschlän[?]'-garble]",
         "starost": "5 let",
         "bolezen": "Marktsfreibn [~ — Marbmil?-hipoteza]",
         "_opomba": "★ h29-NOVA-HIŠA-korpusa (1859-z65-5J!) + ★★ MARKTSFREIBN-×2 (z57 + z65 — paralela-vzrok-×2-v-14-dneh!) + otroška-5J"},
    73: {"ime": "[DUEL-X-open: 'Klara'[KROP-P217+KROP-row-'Klana'-2×!]-vs-'Elena-(Klena?)'[VLM-fresh!]!]-Podire [~Resdire[KROP-row]/Pardire[P217]/Pezdire[?]-TRI!]",
         "stan": "iz Griblje, Hufstau [~]",
         "starost": "23 let [TRI-1:1: VLM+KROP+P217!]",
         "bolezen": "Lungenentzündung [KROP-row-'Langenfinft'-1:1!]",
         "_opomba": "★★ TAIL-P217-KOREKCIJA-1 (z73-1:1-vas/hiša/starost/vzrok! + ime-DUEL-Klara-vs-Elena!) + ★ h20-NIT (P217-'h20[~10!]'-sedaj-potrjeno-h20-1:1-KROP-row!) + Sep-30→Okt-1-mesec-prelom"},
    76: {"ime": "[TRI-DUEL-X-open: 'Marlfannina/Marijannina'[KROP-row!]-vs-'Katharina'[VLM-fresh]-vs-'Paulmann'[P217]!]-Milich [~Mihle[VLM]/Miklik[P217]-TRI!]",
         "stan": "iz Griblje Hufstau [~ + '¼ Griblštofan[?]'-2-vrstica!]",
         "starost": "24 let [~]",
         "bolezen": "Magenkrampf [TRI-1:1!]",
         "_opomba": "★★ TAIL-P217-KOREKCIJA-2 (z76-vas/hiša/starost/vzrok-1:1! + ime-TRI-DUEL!) + ★ h24-NIT (P217-1860-z61-Brenc-h24!) + podpis-DUEL ('J.-Halo[?]-vs-Joh.-Knavs'!)"},
    81: {"ime": "[TRI-DUEL: 'Andrej'[VLM-fresh]-vs-'Andreas'[P217]-vs-'Johann'[P217-duel!]!]-Posdiac [~Pestik[VLM]/Pesdire[P217]/Pestiric[P217]-TRI!]",
         "stan": "kmet (Ablaber)",
         "starost": "99 let [TRAJNI-DUEL: 99[VLM+KROP-row-2×!]-vs-83[P217-KROP!] — X-open!]",
         "bolezen": "Altersschwäche (Alters-verschleiß [~])",
         "_opomba": "★★★ TAIL-P217-TRAJNI-DUEL-3 (z81-99-vs-83-OSTAJA-X-open! + 'PEZDIRC-MREŽA': 'Posdiac/Pesdire'≈Pezdirc-grafije!) + ★ h52-NIT-1859-2/2 (z46 + z81!) + NAJSTAREJŠI-1859 (99J!)"},
    86: {"ime": "[DUEL-X-open: 'Anastasia'[P217+KROP-row-'Snlfannina≈'-glyph!]-vs-'Katharina'[VLM-fresh!]!]-Požekh [~Poček-KROP-row-1:1!]",
         "stan": "Ablaberin (kmetica)",
         "starost": "69 let",
         "bolezen": "Altersschwäche (Alters-schwähe [~])",
         "_opomba": "★★ TAIL-P217-KOREKCIJA-4 (z86-vas/hiša/starost/vzrok-1:1! + ime-DUEL-Anastasia-vs-Katharina!) + ★ h21-NIT-2/2 (z9-Pirczl + z86-Požekh!) + ★ POŽEK-MREŽA (h21 + h58-z35-Leg.Kind — 2-hiši!) + Joh.-Knavs-podpis"},
    94: {"ime": "[TRI-DUEL-X-open: 'Josmat'[KROP-row!]-vs-'Josip'[VLM-fresh]-vs-'Jožef'[P217]!]-Padierž [~Pederž[KROP-row]/Podleber[VLM]/Petek[P217]-X-open!]",
         "stan": "½ Säugl. [?KROP-row-'½-Jaigl' — polletni-dojenček!]",
         "starost": "[TRI-DUEL: 14-DNI[PAS+VLM-2:1!]-vs-13[KROP-row]-vs-'16-J'[P217-FALSIFICIRAN!]! — ENOTE-DNI-NE-LET!]",
         "bolezen": "Naussumsfinkrahn [?KROP-row — 'Nesselsucht?'-hipoteza-VLM; garble]",
         "_opomba": "★★★ TAIL-P217-KOREKCIJA-MAKS (z94: P217-'z95-Jožef-Petek-16J'-FALSIFICIRAN — margin-95→94-KROP + ime-Petek→Padierž[?]-TRI + starost-16J→14-DNI-2:1 + vzrok-'Hauswinskrabn'→'Naussumsfinkrahn[?]'!) + ★ h49-NIT + NAJMLAJŠI-1859 (14-DNI!) + Joh.-Knavs-podpis"},
    97: {"ime": "[TRI-DUEL-X-open: '⅄onalfur'[KROP-row!]-vs-'Valentin'[P217]-vs-'Ana'[VLM-fresh]!]-Brince [~Brinec[P217-Brino]/'Kruška-Bina'[VLM]-TRI!]",
         "stan": "[DUEL-X-open: 'Janezfarain[?]'[KROP-row]-vs-'Inočfrau-(vdova)'[VLM]!]",
         "starost": "58 let [TRI-1:1!]",
         "bolezen": "Magenkrampf [TRI-1:1!]",
         "_opomba": "★★★ TAIL-P217-KOREKCIJA-5 (z97: P217-'z100-Valentin-Brino'-margin-100→97-KROP! + ime-⅄onalfur[?]-vs-Valentin-DUEL-OSTAJA-X-open!) + ★ h65-NIT-2/2 (z24-Graes-2-tedna + z97-58J! — h65 = P155-1889-MILEK-hiša!) + Joh.-Knavs-podpis"},
}

entries = []
for item in PLAN:
    sken, vrste_map, op, vrsta_start = item[0], item[1], item[2], item[3]
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
        if "vsota" in zap or zap.strip() == "—": continue
        realne.append(x)
    # s12: r13 = VLM-duplikat-halucinacija (Lemež-Smajo-3.× — SKIP prek vrsta_start+len)
    want = len(vrste_map)
    pool = [x for x in realne if (x.get("vrsta") or 0) >= vrsta_start]
    # odstrani r13-s12 (vrsta > 12 na s12)
    if sken == 12:
        pool = [x for x in pool if (x.get("vrsta") or 0) <= 12]
    if len(pool) != want:
        print(f"⚠ s{sken}: pričakovano {want}, najdeno {len(pool)} (VLM-n={len(vrste)})")
    for i, x in enumerate(pool[:want]):
        x = dict(x)
        x["z"] = vrste_map[i]
        x["sken"] = sken
        x["pag"] = sken - 5
        x["vrsta_sken"] = x.get("vrsta")
        x["ord_opomba"] = op
        k = KROP.get(x["z"])
        if k:
            for kk, vv in k.items():
                if kk == "_opomba": x["krop_opomba"] = vv
                else: x[kk] = vv
            x["krop"] = True
        entries.append(x)

# --- mesec-'/'-normalizacija + hisna-normalizacija ---
for e in entries:
    m = str(e.get("mesec") or "").strip()
    if "/" in m.split()[0] if m else False:
        e["mesec"] = m.split("/")[0].strip() + " [deljeni-mesec-glava!]"

# --- s15-r12-Jalkič = NEŠTEVILČENA (priest-skipped!) — poseben-vpis ---
d15 = json.load(open(f"{TMP}/vlm-page/s15.json"))
jalk = next((x for x in d15.get("vrstice", []) if (x.get("vrsta") or 0) == 12), None)
if jalk:
    jalk = dict(jalk)
    jalk["z"] = "56a-NEŠTEVILČENA"
    jalk["sken"] = 15
    jalk["pag"] = 10
    jalk["ord_opomba"] = "s15-r12-NEŠTEVILČENA (duhovnik-skoči: 55→[r12-brez-št.!]→56-na-s16! — NOV-TIP-ANOMALIJE!; ne-Griblje: Ceroviše/Vranoviče-h6-Jalkič-6-mj-Wunden!)"
    jalk["nesteviceena"] = True
    entries.append(jalk)
    entries.sort(key=lambda e: (e["sken"], e.get("vrsta_sken") or 0))

# --- normalizacija ---
import re as _re
for e in entries:
    h = str(e.get("hisna") or "").strip()
    mfirst = _re.search(r"\d+", h)
    if h and mfirst:
        clean = mfirst.group(0)
        if clean != h:
            e["hisna_duel"] = h
            e["hisna"] = clean
    m = str(e.get("mesec") or "").strip()
    if m.startswith("[") and "]" in m:
        e["mesec"] = m.replace("[", "").replace("]", "").strip()

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
    "faza": "P218",
    "leto": 1859,
    "knjiga": "04106",
    "okvir": {"skeni": "s011–s019", "pag": "6–13", "pag_formula": "sken−5",
              "meja_1858_59": "s11 (NASLOVNI-LIST-'Sterb-Buch.'-DEEL-2! + '1858'-tail-glava-KROP + tail-54–57 + DVOJNA-ČRTA + VSOTNA-'1 8 [5 9]'-RAZPETE-MARKER (P214-TIP! 2.-instance!) + restart-z1–z7-BREZ-Ločne-glave!) = 56.-POTRDITEV-invariante!",
              "meja_1859_60": "s20 ('1860'-rokopisna-glava-KROP-POTRJENA — P217!)",
              "s19_naslovni_list": "★★★ 'Sterb-Buch.'-PONOVLJEN (nov-quire!) + Dec-1859-nadaljevanje-93–103-BREZ-restarta + LUKNJA-92!",
              "vrstna_aritmetika": "7+12+14+11+12(+1-NEŠTEVILČENA!)+12+12+12+11 = 103 (kronološko!; written-1–91-ČISTO + 93–103 = 102 + 1-NEŠTEVILČENA-Jalkič!)"},
    "statistika": {"vpisov_1859": len(entries), "griblje": len(grib),
                   "hise": len({e.get("hisna") for e in grib}),
                   "meseci": meseci_all},
    "krop_vizualne": [{"z": z, **{k: v for k, v in k.items() if not k.startswith("_")}} for z, k in sorted(KROP.items())],
    "anomalije_ordinali": "★★★ 2-ANOMALIJI-1859: (1) s15-r12-Jalkič-NEŠTEVILČENA (duhovnik-skoči-55→56!) + (2) LUKNJA-92 (s18-91→s19-93!) — ordinali-NI-ČISTO (2.-leto-z-anomalijo-po-1860-WRITTEN-DUP!) — ŠTEVJE-IZ-VRSTIC-še-vedno-EXAKT-103!",
    "entries": entries,
    "griblje_entries": grib,
    "leadP219": None,
}
json.dump(out, open(f"{TMP}/entries_1859.json", "w"), ensure_ascii=False, indent=1)
print(f"1859: {len(entries)} vpisov / {len(grib)} Griblje / {len({e.get('hisna') for e in grib})} hiš")
print("meseci:", meseci_all)
print("Griblje z:", [e["z"] for e in grib])
print("Griblje hiše:", [e.get("hisna") for e in grib])
