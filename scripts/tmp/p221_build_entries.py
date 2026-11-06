#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P221 — agregacija 104-vpisov leta 1885 (ŠTEVJE-IZ-VRSTIC-1.×-za-krstno-linijo-04104!).
NOVA-LINIJA: krstna-predzgodovina-04104 (mrliška-04106-KONČANA-29/29-P220!).
MEJA-1884/85 = s186 (tail-1884-z111[prečr]+z112[prečr] + VSOTNA + restart-z1!).
Ordinalna linija: z1–z104 (104-KRONOLOŠKIH; vrstna-aritmetika 4+8+8+8+9+9+8+8+8+7+8+8+9+2 = 104!).
★★★ DVOJČKI-GRADAC-×2-2-VRSTICI (z92-Anton-umrl + z93-Jožef-živ — Dez 14/14! — page-VLM-spojil!)
★★★ z100 = Anton-GRIBLJE-h1 (page-VLM-'Škrilje'-MISREAD-KOREKCIJA — r7-krop-1:1!)
★★★ z101 = NEIDENTIFICIRANA-VRSTICA (page-VLM-zamujena! t4-fragment-'Janez-Tomaž-½-gem.'!
     — DOKAZ: popravek-pisarja-s199-102/103→103/104 = pisar-sprva-pozabil-štet-z101!)
★★★ POPRAVEK-PISARJA-s199 (102[prečr]→103 + 103[prečr]→104!)
★★★ 25-GRIBLJE = NOV-REKORD (prej-23-P218-1859-mrliška!) / ~22-hiš (h1-×2 + h55-×2!)
pag = sken+13 = FOLIO-SVINČNIK (razprti-list = 1-folio! potrjeno-5×: s185=198/s190=203/s193=206/s196=209/s199=212!)
Izhod: /tmp/p221/entries_1885.json"""
import json, re as _re, re

TMP = "/tmp/p221"

# (sken, z-list, opomba, mode) — page-VLM-vrstice → korektni-ordinali
PLAN = [
    (186, [f"z{i}" for i in range(1, 5)],
     "s186-z1–z4 (4; ★★★ MEJA-1884/85: TAIL-1884-z111[prečr!]-Gradac-68-Maria-†25.9.1885-pripis! + z112[prečr!]-GRIBLJE-h43-Mathias-†28.12.1887-pripis! + VSOTNA-razpete-'1/8/8/5'-P214-TIP + rokopisna-'Jänner'-glava + RESTART-z1 (Jan-1-GRIBLJE-h21!) = 60.-POTRDITEV-invariante!; ★ z1-pripis-†7.9.1887 = KRIŽ-z-mrliško-04106!)", "meja"),
    (187, [f"z{i}" for i in range(5, 13)],
     "s187-z5–z12 (8; Pag.200-folio!; ★ z5-GRIBLJE-Martin-oče-Popić-pripis-'gest.-12.[?]1888'-KRIŽ-04106! + z6-GRIBLJE-Anna-h31!; ★ MESEČNI-DUEL: z9-Feber-5-nato-z10–z12-Januar-12/14/15 (pisarjeva-rahljanje-ali-VLM-misread — X-open!))", "pool"),
    (188, [f"z{i}" for i in range(13, 21)],
     "s188-z13–z20 (8; ★ 3-GRIBLJE: z14-h61[page-'6'-MISREAD-korekcija-trak+krop!]-Marija-oče-POŽEK-½-Gütl! + z15-h11[trak-'41'-MISREAD!]-Mathias-oče-Plavc + z20-h63-Johan-oče-Petrič!; rdeče-kljukice-ob-stolpcu-očeta-kontrolni-znaki!)", "pool"),
    (189, [f"z{i}" for i in range(21, 29)],
     "s189-z21–z28 (8; ★★★ page-VLM-ordinali-SHIFT−1-KOREKCIJA (VLM-'22'→z21! — zap-stolpec-21–28-ČISTO!); ★ 2-GRIBLJE: z26-h49[TRI-DUEL-X-open: 49[page]/17[trak]/'1[8?]'[krop-tail!]!]-Maria-oče-Hlobucar + z28-h28-Margaretha (page-VLM-'28-dup'='28/29'-MISREAD-korekcija!))", "pool"),
    (190, [f"z{i}" for i in range(29, 38)],
     "s190-z29–z37 (9; ★★★ NASLOVNA-GLAVA-SREDI-LETNIKA ('Geburts-und-Tauf-Buch.'-natisnjena-PONOVLJENA! — paralela-mrliška-04106-s9+s10-SREDI-1858!) + ★★★ glava-'18 85'-page-VLM-'1886'-MISREAD-KOREKCIJA (krop-1:1-'85'!); ★ 3-GRIBLJE: z30-h42[page-'45'-MISREAD-korekcija-trak+krop!]-Georg-oče-Pegivec + z33-h1-Mathias-oče-ŽELKO-¼! + z37-h55[~53-duel!]-Johann-oče-Simec-¼!)", "pool"),
    (191, [f"z{i}" for i in range(38, 47)],
     "s191-z38–z46 (9; Pag.204-folio!; 0-GRIBLJE (edina-stran-brez-Griblje-v-oknu-poleg-s195/s197/s198-z-dela!))", "pool"),
    (192, [f"z{i}" for i in range(47, 55)],
     "s192-z47–z54 (8; ★ 2-GRIBLJE: z47-h53[page-'33'-MISREAD-korekcija-trak+krop-2:1!]-Katharina-oče-Pegdic-½-Gärtl-PEZDIRC-grafija! + z48-h35[page-'33'-MISREAD-korekcija!]-Mathias-botra-Uhr! — ★★★ h33-×2-HIPOTEZA-MRTVA (h53+h35!)!)", "pool"),
    (193, [f"z{i}" for i in range(55, 63)],
     "s193-z55–z62 (8; ★ 4-GRIBLJE: z56-h16-Mathias + z57-h24-Michael-oče-Princz (datum-duel-z57-Aug-2-vs-z58-Jul-31/3-kronološki-preskok-X-open!) + z59-h[?]-QUAD-DUEL-hiša-(27/47/37/21!)+otrok-TRI-DUEL-(Marko/Maria/Martin/Martha!)-honesty-MAX + z62-h17[page-'19'-MISREAD-korekcija-trak+krop!]-Georg-oče-Hval-¼-Gärtler!)", "pool"),
    (194, [f"z{i}" for i in range(63, 71)],
     "s194-z63–z70 (8; ★ 3-GRIBLJE: z63-h58-Janez-oče-Piček-mati-DRAGOŠ-nit! + z64-h9-Janez + z68-h55-Mathias-oče-Simic-SIMIC-nit! — ★ h55-×2 (z37+z68)!)", "pool"),
    (195, [f"z{i}" for i in range(71, 78)],
     "s195-z71–z77 (7; Pag.208-folio (page-VLM-'268'-MISREAD-tens!); 0-GRIBLJE)", "pool"),
    (196, [f"z{i}" for i in range(78, 86)],
     "s196-z78–z85 (8; ★ 3-GRIBLJE: z78-h[?]-TRI-DUEL-hiša-(17/29/9/99!)-Katharina-oče-Pogelb + z82-h2-Katharina-oče-Hlebec-¼! + z85-h23[page-'39-ep-91'-MISREAD-korekcija-trak+krop!]-Mathias-mati-PEZDIRC-nit-(Katharina-roj.-Pegdirec!))", "pool"),
    (197, [f"z{i}" for i in range(86, 94)],
     "s197-z86–z93 (8; ★★★ DVOJČKI-GRADAC-×2-2-VRSTICI (z92-Anton-umrl-'Na-umrla' + z93-Jožef-živ — OBA-Dez-14/14-Gradac-5[~]! — page-VLM-SPOJIL-v-1-vrstico-'92'-KOREKCIJA! — PARALELA-P219-DVOJČKI-SIMIC-h19-1858-2-VRSTICI!) + robni-svinčnik-92[prečr]/93/94-na-dnu (revizija!) + 0-GRIBLJE)", "dvojcki"),
    (198, [f"z{i}" for i in range(94, 103)],
     "s198-z94–z102 (9; ★★★ z100 = GRIBLJE-h1-Anton (page-VLM-'Škrilje'-MISREAD-KOREKCIJA-r7-krop-1:1-'Gribile-h1'!) — h1-×2 (z33+z100)! + ★★★ z101 = NEIDENTIFICIRANA-VRSTICA (page-VLM-ZAMUJENA! t4-fragment-'Janez-Tomaž-½-gem.'-X-open!) — DOKAZ: POPRAVEK-PISARJA-s199! + z102-Katharina→Marija-POPRAVEK-IME-otroka (prečrtano!) + robni-svinčnik-100/101/102-na-dnu!; 0-GRIBLJE-poleg-z100!)", "s198"),
    (199, [f"z{i}" for i in range(103, 105)],
     "s199-z103–z104 (2; Pag.212-folio!; ★★★ TAIL-1885 = ZADNJA-2-vrstici-knjige-04104! + ★★★ POPRAVEK-PISARJA-×2 (z103-'102'-prečr→103 + z104-'103'-prečr→104! — DOKAZ-za-z101!) + ★★★ 1-GRIBLJE-TAIL: z104-h8-Anton-oče-Brumec-botra-KRIŽAN-(Peter-Krijan!)! + BREZ-VSOTNE-vrste (1886-gre-v-NOVO-knjigo-04105!) + s200-VEZ-platnica!)", "pool"),
]

# KROP/trak-overrides za 25-GRIBLJE-vrstic (triangulacija: page-VLM + traki + krop!)
KROP = {
    1: {"ime": "Mathias", "hisna": "21",
        "ocec": "Jožef Šujc [~Šimic?-garble!]", "matec": "Brne [~]",
        "botra": "Brodarčič [~] + Katarina Hukar [~]",
        "_opomba": "★★★ RESTART-z1 = 1.-vpis-1885-NA-DAN-1.-1.! + pripis-'†-7.9.1887'-KRSTNI-VPIS→KRIŽ-z-mrliško-04106-1887-X-open!"},
    5: {"ime": "Martin", "hisna": "[?] (~10-krop)",
        "ocec": "Martin Popić [~Popit!]-kmet", "matec": "Maria roj. Kotar [~]",
        "botra": "Jakob Kotar [~] + Katharina Pozek [POŽEK!]",
        "_opomba": "★ pripis-'gest.-12.[?]1888'-KRSTNI-VPIS→KRIŽ-z-mrliško-04106-1888-X-open! + POŽEK-botra-nit!"},
    6: {"ime": "Anna", "hisna": "31",
        "_opomba": "★ h31-nit (P220-z56-Ana-Urih-h31-1857-PRVI-vpis!) — mesec-duel (Jan[~30?]-vs-Febr!)"},
    14: {"ime": "Marija", "hisna": "61",
         "ocec": "Požek, ½ Gubb [~Gütl-garble!]", "matec": "Fila[k] [~FILAK!]",
         "botra": "Pezdirec [~!] + Ana Pezdirec [~!]",
         "_opomba": "★★★ page-'h6'-MISREAD-KOREKCIJA (trak+krop-'61'-2:1!) — h61-URIH-hiša (P216-z11!) + oče-POŽEK + mati-FILAK + botri-PEZDIRC-×2 = 3-MREŽE-V-1-VRSTICI!"},
    15: {"ime": "Mathias", "hisna": "11",
         "ocec": "Mathias Plavc [~]-¼-Gribl.", "matec": "Agnes roj. Jakobič [~]",
         "_opomba": "★ page-'h11'-POTRJENO (trak-'41'-MISREAD!) — h11-nit"},
    20: {"ime": "Johan [~Johann]", "hisna": "63",
         "ocec": "Nikolaus Petrič-kmet", "matec": "Marija roj. Petžolec [~]",
         "_opomba": "★ h63-nit (P220-z74-Marijan-KRIŽAN-h63-1857-TAIL! — h63-2-obdobji!)"},
    26: {"ime": "Maria", "hisna": "49 [TRI-DUEL-X-open: 49[page]/17[trak]/1[8?][krop-tail!]!]",
         "ocec": "Peter Hlobucar [~Globučar-garble!]", "matec": "Maria roj. Grabl [~Gribl-dekliški?!]",
         "_opomba": "★ ordinal-DUEL-KOREKCIJA (page-'27'→z26-zap-stolpec-2:1!) + matec-'roj.-Grabl'≈Griblje-dekliški-priimek-X-open!"},
    28: {"ime": "Margaretha", "hisna": "28",
         "_opomba": "★ page-VLM-'28-dup'-MISREAD-KOREKCIJA (z28-EN-VPIS! ordinal-28-zap+trak+krop!) — h28-nit"},
    30: {"ime": "Georg", "hisna": "42",
         "ocec": "Georg Pegivec [~]-Intabvre [~intabuliran?!]", "matec": "Dorothea roj. Krigar [~Križar?]",
         "_opomba": "★ page-'h45'-MISREAD-KOREKCIJA (trak+krop-'42'-2:1!) + 'Intabvre' = intabuliran-zemljiški-status-X-open!"},
    33: {"ime": "Mathias", "hisna": "1",
         "ocec": "Miklo [~Miko!] Želko-¼-Griblj.", "matec": "Katharina [~Kure/Kurc?]",
         "botra": "Georg Želko + Katharina Želko",
         "_opomba": "★★★ h1-nit (1/2!) + ŽELKO-mreža (h1-nit-P215/P216-1862/64!) + oče-'Miklo'≈Miko/z68-'Miko-Simic'-X-open!"},
    37: {"ime": "Johann", "hisna": "55 [duel-53!]",
         "ocec": "Simec [~Simon-Simec?]-¼-Gribler", "matec": "Anna [~]",
         "_opomba": "★ h55-nit (1/2! z68-sledi!) + SIMIC-oče-nit + ordinal-'97'-krop-MISREAD (page+trak-'37'-2:1!)"},
    47: {"ime": "Katharina", "hisna": "53",
         "ocec": "Johan Pegdic [~Pezdic!]-½-Gärtl.", "matec": "Anna roj. Tedić [~]",
         "_opomba": "★★★ page-'h33'-MISREAD-KOREKCIJA (trak+krop-'53'-2:1!) — PEZDIRC-grafija-oče! (h33-×2-HIPOTEZA-MRTVA!)"},
    48: {"ime": "Mathias", "hisna": "35",
         "ocec": "Mathias [priimek-X-open!]", "matec": "Anna [~]",
         "botra": "Mathias Uhr [~URH!]-½-Gärtl.",
         "_opomba": "★★★ page-'h33'-MISREAD-KOREKCIJA (trak+krop-'35'-2:1!) — h33-×2-HIPOTEZA-MRTVA (h53+h35!) + botra-URH-nit!"},
    56: {"ime": "Mathias", "hisna": "16",
         "_opomba": "★ h16-nit — ordinal-'36'-krop-MISREAD (page+trak-'56'!)"},
    57: {"ime": "Michael", "hisna": "24",
         "ocec": "Matthias Princz [~Princ/?!]", "matec": "Barbara roj. Gaborič [~]",
         "_opomba": "★ ordinal-DUEL (page-'57'/trak-'58'/krop-'59'-KURRENT-ZMEDA! — zap-stolpec-pozicija-3.-od-8 = z57!) + ★ datum-kronološki-preskok (z57-Aug-2-vs-z58-Jul-31/3! — pisarjev-zaporedni-vpis-nazaj-X-open!)"},
    59: {"ime": "Martha [TRI-DUEL-X-open: Martha[2×-krop!]/Marko[page]/Maria[trak]/Martin[krop!]!]",
         "hisna": "[?] (QUAD-DUEL-X-open: 27[page]/47[trak]/37[krop]/21[hi-krop!]!)",
         "ocec": "Martin Hrizon [~Hrižnik?-garble!]-kmetar", "matec": "Marija Stravs [~]",
         "_opomba": "★★★ honesty-MAX-1885 (ordinal-59-ČISTO + hiša-QUAD-DUEL + ime-TRI-DUEL!)"},
    62: {"ime": "Georg", "hisna": "17",
         "ocec": "Janez Hval [~]-¼-Gärtler", "matec": "Anna roj. Jakljevič [~]",
         "_opomba": "★ page-'h19'-MISREAD-KOREKCIJA (trak+krop-'17'-2:1!)"},
    63: {"ime": "Janez", "hisna": "58",
         "ocec": "Janez Piček [~Böič?-garble!]", "matec": "Ana roj. DRAGOŠ [~!]",
         "botra": "Marko Straus [~] / Ana Pezdirc [~!]",
         "_opomba": "★★★ mati-DRAGOŠ-nit (P193-h3-DRAGOŠ-1864 + P220-z45-Dragos-h13!) + botra-PEZDIRC-nit!"},
    64: {"ime": "Janez", "hisna": "9",
         "_opomba": "★ h9-nit (page+trak+krop-3×!)"},
    68: {"ime": "Mathias", "hisna": "55",
         "ocec": "Miko Simic [~SIMIC!]", "matec": "Maria Podlivc [~]",
         "_opomba": "★ h55-nit (2/2 — h55-×2-v-1885!) + SIMIC-oče (z37-'Simec'-X-open-ista-družina!)"},
    78: {"ime": "Katharina", "hisna": "[?] (TRI-DUEL-X-open: 17[page]/29[trak]/9-99[2×-krop!]!)",
         "ocec": "Georg Pogelb [~garble!]", "matec": "Katharina Zag. [~]",
         "_opomba": "★ hiša-TRI-DUEL (17-vs-29-vs-9/99!) — ordinal-'98'-krop-MISREAD (page+zap-'78'!)"},
    82: {"ime": "Katharina", "hisna": "2",
         "ocec": "Peter Hlebec [~HLEBEC/KLEPEC-nit!]-¼-Gäbl", "matec": "Anna roj. Jakofčič [~]",
         "_opomba": "★ h2-nit (P219-h2-KLEPEC/HLEBEC-1858-z47! — HLEBEC-nit-2-obdobji!) + datum-duel (Okt-20[~26?]/26!)"},
    85: {"ime": "Mathias", "hisna": "23 [~]",
         "ocec": "Nikolaus Kupanič [~Skupanič?]", "matec": "Katharina roj. Pegdirec [~PEZDIRC!]",
         "botra": "Anton Cajnar [~] + Maria Skaradinič [~]",
         "_opomba": "★★★ mati-PEZDIRC-nit (Katharina-roj.-Pegdirec!) + page-'39-ep-91'-MISREAD-KOREKCIJA (trak+krop-'23'-2:1!) + ordinal-'88'-trak-MISREAD ('85'-page+zap+krop!)"},
    92: {"ime": "Anton (dvojček-1/2!)", "vas": "Gradac", "hisna": "5 [~]",
         "_opomba": "★★★ DVOJČKI-GRADAC-×2-2-VRSTICI (1/2 — umrl-'Na-umrla'-pripis!) — page-VLM-SPOJIL-z92+z93-KOREKCIJA! — PARALELA-P219-DVOJČKI-SIMIC-h19! + pripis-'Umrła-dne-28.4.1965-v-Zagrebu'-MMK!"},
    93: {"ime": "Jožef (dvojček-2/2!)", "vas": "Gradac", "hisna": "5 [~]",
         "_opomba": "★★★ DVOJČKI-GRADAC-×2 (2/2 — živ!) — 2-VRSTICI-1.-DOKUMENTIRANA-DVOJČKA-KRSTA-V-PREDZGODOVINI!"},
    100: {"ime": "Anton", "vas": "Griblje", "hisna": "1",
          "ocec": "[~] (r7-krop!)", "matec": "[~]",
          "_opomba": "★★★ page-'Škrilje'-MISREAD-KOREKCIJA (r7-krop-'Gribile-h1'-1:1!) — h1-×2 (z33!) = 25.-GRIBLJE-VPIS-1885!"},
    104: {"ime": "Anton", "hisna": "8",
          "ocec": "Peter Brumn [~Brumec!]-kmet", "matec": "Marija roj. Harasimovič [~]",
          "botra": "Peter Krijan [KRIŽAN!] + Marjeta [~]",
          "_opomba": "★★★ TAIL-1885 = ZADNJI-VPIS-KNJIGE-04104 + ordinal-POPRAVEK-PISARJA ('103'-prečr→104!) + botra-KRIŽAN-nit (h36/h63-niti!)"},
}

entries = []
for sken, zlist, op, mode in PLAN:
    d = json.load(open(f"{TMP}/vlm-page/s{sken}.json"))
    vrste = d.get("vrstice", [])
    realne = []
    for x in vrste:
        ime = (x.get("ime") or x.get("otrok") or x.get("ime_otroka") or "").strip()
        vas = (x.get("vas") or x.get("kraj") or "").strip()
        mes = (x.get("mesec") or "").strip()
        roj = (x.get("rojen") or x.get("smrt") or "").strip()
        krst = (x.get("krsten") or x.get("pokop") or "").strip()
        x["_ime_norm"] = ime
        if not ime and not vas:
            continue
        if not mes and not roj and not krst:
            continue
        realne.append(x)
    want = len(zlist)
    if mode == "meja":
        # s186: preskoči 1884-tail-vrstice (ime+vas z mesecem December!) — vzemi zadnjih want vrstic (restart-z1+)
        pool = realne[-want:] if len(realne) >= want else realne
    elif mode == "dvojcki":
        # s197: 6 prvih → z86–z91, zadnja (dvojčki-spojena) → SPLIT z92+z93
        pool = realne[:6]
    elif mode == "s198":
        # s198: 7 prvih → z94–z100, zadnja (K→M) → z102; z101 = NEIDENTIFICIRANA!
        pool = realne[:7]
    else:
        pool = realne
    if len(pool) != want and mode == "pool":
        print(f"⚠ s{sken}: pričakovano {want}, najdeno {len(pool)} (VLM-n={len(vrste)}, realne={len(realne)})")
    for i, x in enumerate(pool[:want]):
        x = dict(x)
        x["z"] = zlist[i]
        x["sken"] = sken
        x["pag"] = sken + 13  # folio-svinčnik (razprti-list = 1-folio!)
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

# --- s197: SPLIT dvojčkov (z92 Anton + z93 Jožef iz spojene vrstice) ---
s197 = json.load(open(f"{TMP}/vlm-page/s197.json"))
twin = None
for x in s197.get("vrstice", []):
    if "Anton" in str(x.get("ime") or "") and "Jožef" in str(x.get("ime") or ""):
        twin = x; break
for znum, ime_d in [(92, "Anton"), (93, "Jožef")]:
    x = dict(twin or {})
    x["z"] = f"z{znum}"; x["sken"] = 197; x["pag"] = 210
    x["ime"] = ime_d
    x["vrsta_sken"] = twin.get("vrsta") if twin else None
    x["ord_opomba"] = dict(PLAN[-4])[ "op" ] if False else "s197-z86–z93 (8; ★★★ DVOJČKI-SPLIT!)"
    x["dvojcki_split"] = True
    k = KROP.get(znum)
    if k:
        for kk, vv in k.items():
            if kk == "_opomba": x["krop_opomba"] = vv
            else: x[kk] = vv
        x["krop"] = True
    entries.append(x)

# --- s198: vstavi z101-NEIDENTIFICIRANA (med z100 in z102) + preskoči VLM-zadnjo (K→M→z102 posebej) ---
s198 = json.load(open(f"{TMP}/vlm-page/s198.json"))
km = None
for x in s198.get("vrstice", []):
    nm = str(x.get("ime") or x.get("otrok") or "")
    vs = str(x.get("vas") or "")
    if "Marija" in nm and ("Primostek" in vs or "Primo" in vs):
        km = x; break
if km is None:
    # zadnja vrstica s198 = K→M (vas-Primostek!)
    cand = [x for x in s198.get("vrstice", []) if "Primostek" in str(x.get("vas") or "")]
    if cand: km = cand[-1]
z101 = {
    "z": "z101", "sken": 198, "pag": 211, "zaporedna": "[?]",
    "mesec": "December [~]", "rojen": "[?]", "krsten": "[?]",
    "vas": "[?]", "hisna": "[?]", "ime": "[NEIDENTIFICIRANA-VRSTICA!]",
    "ocec": "Janez Tomaž [~ — t4-trak-fragment-parents-glimpse!]", "matec": "[?]",
    "botra": "[?]", "duhovnik": "[?]", "opomba": None,
    "ord_opomba": "s198-z94–z102 (9; ★★★ z101 = NEIDENTIFICIRANA!)",
    "krop_opomba": "★★★ page-VLM-ZAMUJENA-VRSTICA (t4-trak-fragment-'oče-Janez-Tomaž-½-gem.'!) — DOKAZ-za-obstoj: POPRAVEK-PISARJA-s199 ('102'→103 + '103'→104 = pisar-sprva-pozabil-z101!) + robni-svinčnik-100/101/102-na-dnu-s198 (revizija!) — X-open: morda-probita/squeezed-vrstica!",
    "neidentificirana": True,
}
entries.append(z101)
if km:
    km = dict(km)
    km["z"] = "z102"; km["sken"] = 198; km["pag"] = 211
    km["ord_opomba"] = "s198-z94–z102 (9; ★ z102-Katharina→Marija-POPRAVEK-IME!)"
    km["krop_opomba"] = "★ ordinal-DUEL (r9-'101'-vs-r8-'102'-vs-t4-'101/102-prečr'!) + IME-POPRAVEK-otroka (Katharina-prečrtano→Marija!) + robni-svinčnik-101-prečr/102!"
    entries.append(km)

# --- razvrsti po ordinalu ---
def znum(e): return int(str(e["z"]).replace("z", ""))
entries.sort(key=znum)

# --- mesec-normalizacija + statistika ---
meseci_all = {}
for e in entries:
    m = (e.get("mesec") or "").strip()
    m = _re.sub(r"[\[\]\(\)]", "", m).strip()
    m = m.split()[0] if m else "?"
    m2 = {"Januar": "J", "Jänner": "J", "Jannuar": "J", "Februar": "F", "Feber": "F", "März": "M", "April": "A",
          "Mai": "M2", "Maijo": "M2", "Juni": "J2", "July": "J3", "August": "A2", "September": "S",
          "October": "O", "Oktober": "O", "November": "N", "December": "D", "Dezember": "D",
          "Januar/Februar": "J", "Mai/Juni": "M2"}.get(m, m)
    if m2.startswith("3.") or m2 in ("?",): m2 = "?"
    meseci_all[m2] = meseci_all.get(m2, 0) + 1

grib = [e for e in entries if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]

# hišne-korekcije za Griblje (hisna-DUEL-normalizacija: prva-cifra)
import re as _re
for e in grib:
    h = str(e.get("hisna") or "").strip()
    mfirst = _re.match(r"^(\d+)", h)
    if h and mfirst and not h.startswith("[?]"):
        clean = mfirst.group(1)
        if clean != h:
            e["hisna_duel"] = h
            e["hisna"] = clean

out = {
    "faza": "P221",
    "leto": 1885,
    "knjiga": "04104",
    "okvir": {"skeni": "s185–s199 (15 svežih 2×-md5-NEODVISNA-PRENOSA-15/15 + s200-vez-proba!; s185 = 1884-tail-kontekst; s200 = VEZ-platnica-0-vrstic!)",
              "okno_1885": "s186–s199 (14 skenov: MEJA + celo leto 1885 + TAIL!)",
              "pag": "sken + 13 = FOLIO-SVINČNIK-ARHIVARJA (razprti-dvostranski-list = 1-FOLIO! potrjeno-5×-natančno: s185='198'/s190='203'/s193='206'/s196='209'/s199='212'! + page-VLM-tens-MISREADI-dokumentirani: s188-'241'→201 + s195-'268'→208!) — NOVA-KONVENCIJA-za-04104 (04105-korpus: sken−1; 04106-predzgodovina: sken−5/sken−1!)",
              "meja_1884_85": "s186 (TAIL-1884-z111[prečrtano!]-Gradac-68-Maria-†25.9.1885-pripis + z112[prečrtano!]-GRIBLJE-h43-Mathias-†28.12.1887-pripis + VSOTNA-razpete-'1/8/8/5'-P214-TIP-sorodna + rokopisna-'Jänner'-glava + RESTART-z1-na-DAN-1.-1.-GRIBLJE-h21!) = 60.-POTRDITEV-invariante! + 1884 = 112-vpisov (s185-ordinali-103–110!)",
              "meja_1885_86": "NE-OBSTAJA-v-04104 (TAIL-z103–z104-Dez-29/30 + BREZ-VSOTNE + s200 = VEZ-platnica! — 1886-gre-v-NOVO-knjigo-04105 = KORPUS-ŽE-POKRIT-P79!) — KNJIGA-04104-KONČANA!",
              "vrstna_aritmetika": "4+8+8+8+9+9+8+8+8+7+8+8+9+2 = 104 (kronološko z1–z104 — ŠTEVJE-IZ-VRSTIC-1.×-za-krstno-linijo-04104!; zap-stolpci-15/15-ČISTO!)",
              "dvojcki_gradac": "★★★ DVOJČKI-GRADAC-×2-2-VRSTICI (z92-Anton-'Na-umrla'-umrl + z93-Jožef-živ — OBA-Dez-14/14-Gradac-5[~]! — page-VLM-SPOJIL-v-1-vrstico-'92'-KOREKCIJA-2-vrstici!) — PARALELA-P219-DVOJČKI-SIMIC-h19-1858!",
              "z101_neidentificirana": "★★★ z101 = NEIDENTIFICIRANA-VRSTICA (page-VLM-ZAMUJENA!) — DOKAZ-za-obstoj: POPRAVEK-PISARJA-s199 (z103-'102'-prečr→103 + z104-'103'-prečr→104 = pisar-sprva-pozabil-štet-z101!) + t4-trak-fragment-'oče-Janez-Tomaž-½-gem.' + robni-svinčnik-100/101/102-na-dnu-s198 (revizija!) — X-open!",
              "popravek_pisarja": "s199-×2 (z103-'102'-prečrtano→103 + z104-'103'-prečrtano→104!) + z102-IME-POPRAVEK (Katharina-prečrtano→Marija!)",
              "naslovna_sredi_letnika": "★★★ s190 = NASLOVNA-GLAVA-SREDI-LETNIKA ('Geburts-und-Tauf-Buch.'-natisnjena-PONOVLJENA! — paralela-mrliška-04106-s9+s10-SREDI-1858-quiri!) + glava-'18 85'-page-VLM-'1886'-MISREAD-KOREKCIJA (krop-'85'-1:1!)",
              "foliacija_misreads": "page-VLM-tens-MISREADI (0↔4/6/8-zmeda!): s185-'148'→198 + s188-'241'→201 + s193-'266'→206 + s195-'268'→208 — pag=sken+13-NEOMAJNO (5×-natančno!)",
    },
    "statistika": {"vpisov_1885_kronolosko": len(entries),
                   "vpisov_written": 104,
                   "griblje": len(grib),
                   "hise": len({e.get("hisna") for e in grib}),
                   "meseci": meseci_all},
    "krop_vizualne": [{"z": z, **{k: v for k, v in k.items() if not k.startswith("_")}} for z, k in sorted(KROP.items())],
    "anomalije_ordinali": "★★★ 1885: DVOJČKI-SPLIT (z92+z93!) + z101-NEIDENTIFICIRANA (DOKAZ-popravek-pisarja!) + POPRAVEK-PISARJA-s199-×2 + robni-svinčnik-revizija (s197-dno + s198-vrh-'71'-prečr + s198-dno-100/101/102!) + ordinal-DUELI-rešeni-zap-stolpcem (s189-shift−1 + s190-'31'-vs-'30' + s193-z57-'59'-krop-MISREAD + s196-'98'-krop-MISREAD!)",
    "entries": entries,
    "griblje_entries": grib,
    "leadP222": "krstna-04104-PREDZGODOVINA-2/15: leto-1884 (descending! — 1884 = 112-vpisov; s185-tail-ŽE-VLM (z105-GRIBLJE-h62-Johann-oče-Kure-½! + z106–z110) → MEJA-1883/84-pred-s185 → probe-s178–s185!)",
}
json.dump(out, open(f"{TMP}/entries_1885.json", "w"), ensure_ascii=False, indent=1)
print(f"1885: {len(entries)} kronoloških (104-written!) / {len(grib)} Griblje / {len({e.get('hisna') for e in grib})} hiš")
print("meseci:", meseci_all)
print("Griblje z:", [e["z"] for e in grib])
print("Griblje hiše:", [e.get("hisna") for e in grib])
