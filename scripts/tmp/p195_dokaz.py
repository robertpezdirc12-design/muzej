#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P195 — dokaz MRLIŠKE PREDZGODOVINE 04106, leto 1882 (predzgodovina-4/29).
Izhod: research/issue17/parish-death-1882-04106.json
Struktura po vzoru P192–P194 (entries + anomalije + duhovniki + epidemija +
hišne_kontinuitete + forme + crossChecks + honesty + kaskada + lead + notes)."""
import json, os

ROOT = "/home/z/muzej"

def E(skan, pag, z, mesec, smrt, pokop, vas, hisna, ime, stan, starost, bolezen,
      previden, duhovnik, griblje, blok, spol, leto=1882, opomba=None):
    return {"skan": skan, "pag": pag, "zaporedna": z, "mesec": mesec, "smrt": smrt,
            "pokop": pokop, "vas": vas, "hisna": hisna, "ime": ime, "stan": stan,
            "starost": starost, "bolezen": bolezen, "previden": previden,
            "duhovnik": duhovnik, "spol": spol, "griblje": griblje,
            "blok_v_parish": blok, "leto": leto, "opomba": opomba}

JC = "Franz Jančar 'v.R.C.-Pfarrer/Priester' [~Janežič?]"
DVG = "Franz Dovgan [~Dorgun-forma?]"

entries = [
    # --- s180 (Pag. 174) = z1–z10 ---
    E("s180", 174, "1", "Jänner", "7.", "9.", "Wolk [~Volk?]", "1", "Andreas Paliüič [~Palič]", "Mühlzügler [~mlinar! — MÜHLZÜGLER-×6-1/6!]", "86", "Altersschwäche", "/", DVG, False, False, "M"),
    E("s180", 174, "2", "Jänner", "10.", "12.", "Griblje", "20", "Anna Pozdire [~Pezdirc]", "'+Güblanc[?~Gütl.bes.-glif]' + Wirthsthum [~]", "5 [~8?] Monaten", "Friseln [FRISELN-FLOOD-1/16!]", "/", JC, True, True, "F"),
    E("s180", 174, "3", "Jänner", "22.", "23.", "Krasinec", "3", "Barbara Pozdire [~Pezdirc]", "½ gütl.bes.-tochter", "2 Tagen", "Friseln [FRISELN-FLOOD-2/16!]", "/", JC, False, False, "F"),
    E("s180", 174, "4", "februar", "23.", "25.", "Krivoglavce", "29", "Mathias Veure [~Hure/Kure-forma?]", "½ gütl.bes.? [~]", "32", "Lungenentzündung", "/", DVG, False, False, "M"),
    E("s180", 174, "5", "februar", "9.", "11.", "Krasinec", "3", "Maria Pozdire [~Pezdirc]", "Wirtstochter", "36 Jahren", "Lungentuberculose", "/", JC, False, False, "F"),
    E("s180", 174, "6", "februar", "18.", "19.", "Boršt", "16", "Mathias Klepec [~Khepec-VLM!]", "spl. ½ gütl.bes.-sohn [~]", "2 Tagen", "Friseln [FRISELN-FLOOD-3/16!]", "/", DVG, False, False, "M"),
    E("s180", 174, "7", "februar", "21.", "22.", "Prilozje", "32", "Maria Šušarič [~Sulbarič?]", "½ gütl.bes.-tochter", "1½ Jahr", "Friseln [FRISELN-FLOOD-4/16!]", "/", DVG, False, False, "F"),
    E("s180", 174, "8", "februar", "25.", "26.", "Certoviše", "9", "Anton Hudorovac", "Zigernmodlina? [~neberljivo!]", "1 Monat", "Krämpfe? [~Cywäisn-glyph]", "/", JC, False, False, "M"),
    E("s180", 174, "9", "März", "28.", "1.", "Krasinec", "15", "Johann Brodarič", "½ gütl.bes.-sohn", "3 Jahren", "Abzehrung", "/", "Franz Jančar coop. [~]", False, False, "M"),
    E("s180", 174, "10", "März", "28.", "1.", "Boršt", "30", "Mathias Tabor", "gütl.bes.-sohn", "2 Monaten", "Friseln [FRISELN-FLOOD-5/16!]", "/", "Jakob Dovgan [~Jukob? — ★ NOVI-DUHOVNIK-#31!]", False, False, "M"),
    # --- s181 (Pag. 175) = z11–z20 ---
    E("s181", 175, "11", "März", "14.", "16.", "Vranoviče", "2", "Stefan Jaklša [~]", "Mühlzügler [MÜHLZÜGLER-×6-2/6!]", "74", "Lungenentzündung", "/", "Franz Jančar coop.", False, False, "M"),
    E("s181", 175, "12", "März", "15.", "16.", "Gradac", "51", "Maria Jaklša [~]", "gütl.bes.-tochter", "17", "Lungentuberculose", "/", "Franz Jančar coop.", False, False, "F"),
    E("s181", 175, "13", "März", "15.", "17.", "Kloster", "35", "Ana Jaklša [~]", "Gawerßmörin? [~Gastwirtin-glyph!]", "62", "Tuberculose", "/", JC, False, False, "F"),
    E("s181", 175, "14", "März", "22.", "24.", "Griblje", "1", "Maria Zefslo [~Zelško/Zeliško — 3-branja!]", "Wirtstochter [~hünnotönrib-glyph]", "32", "Lungenentzündung", "/", JC, True, True, "F"),
    E("s181", 175, "15", "März", "23.", "25.", "Griblje", "3", "Dorothea Vrižan [~Križan? — V/K-glyph]", "'kinnes-Kind' [~unehel.?-glyph]", "9 Monate", "Friseln [FRISELN-FLOOD-6/16! — VLM-'9-let-Grippe'-ZAVRŽEN!]", "/", JC, True, True, "F"),
    E("s181", 175, "16", "März", "27.", "29.", "Krasinec", "13", "Nikolaus Jučlevič? [~Jaklevič-glyph]", "¾ gütl.bes. [~]", "68", "Abzehrung", "/", DVG, False, False, "M"),
    E("s181", 175, "17", "März", "27.", "29.", "Griblje", "54", "Anna Šimec", "¼ gütl.bes., WITTWE [~vdova!]", "46", "Abzehrung", "/", JC, True, True, "F"),
    E("s181", 175, "18", "April", "6.", "8.", "Griblje", "69", "Milo Terdič [~Miha/Miko-glyph?]", "WIRTH [~gospodar!]", "44", "Gehirnentzündung", "/", DVG, True, True, "M"),
    E("s181", 175, "19", "April", "8? [~6?].", "9? [~7?].", "Primostek", "22", "Rudolf Jurevar? [~Jušuar-glyph]", "Gwerger?-sohn [~neberljivo]", "4 Jahren", "Abzehrung", "/", DVG, False, False, "M"),
    E("s181", 175, "20", "April", "9.", "11.", "Boršt", "21", "Barbara Klepec? [~Vlepec-glyph]", "Krizüngs?-gütlng [~neberljivo]", "66", "Lungenentzündung", "/", DVG, False, False, "F"),
    # --- s182 (Pag. 176) = z21–z29 ---
    E("s182", 176, "21", "April", "8.", "10.", "Gradac", "64", "Georg Kovačič [~Hovače-glyph]", "hibign-dirbnde? [~neberljivo]", "72", "Altersschwäche", "/", JC, False, False, "M"),
    E("s182", 176, "22", "April", "9.", "11.", "Gradac", "80", "Margaretha Šopriič? [~Dopriič-glyph]", "spät. gütl.bes.-tochter [~]", "4 Jahren", "Wassersucht? [~Wüarnmonn-glyph]", "/", DVG, False, False, "F"),
    E("s182", 176, "23", "April", "10.", "12.", "Krivoglavce", "11", "Margaretha Tome", "spät. gütl.bes.-sohn? [~žensko-ime+sohn!]", "2 Monaten", "Friseln [FRISELN-FLOOD-7/16!]", "/", JC, False, False, "F"),
    E("s182", 176, "24", "April", "13.", "15.", "Griblje", "73", "Mathias Lupanič [~Lupančič/Lapanja-VLM!]", "'wirtso-Kind'-glyph [~unehel./Wirths-?]", "2 Monat", "Friseln [FRISELN-FLOOD-8/16!]", "/", JC, True, True, "M"),
    E("s182", 176, "25", "April", "17.", "19.", "Gradac", "64", "Fran Ulčer [~Ucer/Vlčer-glyph]", "Zmqshipes? [~neberljivo] + ★★★ OPOMBA: 'Kind der hiesigen Dienstmagd Maria Ulčer in Meriška vas H 21, Pfarre Toplice' = MIGRANT-tuja-parošija-1.×!", "14 Monate", "Fraisenfall? [~Wrußfall-glyph]", "/", JC, False, False, "M"),
    E("s182", 176, "26", "April", "19.", "21.", "Gradac", "16", "Jožef PLUT [rdeča-kljukica!]", "gütl.bes. [~Gütlbers-glyph]", "37", "Tuberculose", "/", JC, False, False, "M"),
    E("s182", 176, "27", "April", "26.", "28.", "Krasinec", "33", "Maria Žugelj? [~Zugel-glyph]", "Stubmörin? [~neberljivo]", "72", "Altersschwäche", "/", JC, False, False, "F"),
    E("s182", 176, "28", "April", "27.", "28.", "Krasinec", "13", "Ana Jaklevič [~]", "Gawerßmörin? [~Gastwirtin-glyph — 2.×!]", "23", "Tuberculose", "/", JC, False, False, "F"),
    E("s182", 176, "29", "Mai", "30.", "2.", "Certoviše", "16", "Johann Jalkovič? [~Jarlovič-glyph]", "Mühlzügler [MÜHLZÜGLER-×6-3/6!]", "48", "Wassersucht [Waſſerſucht-glyph — 1/4!]", "/", JC, False, False, "M"),
    # --- s183 (Pag. 177) = z30–z37 ---
    E("s183", 177, "30", "Mai", "5.", "7.", "Gradec", "33", "Johann Butala", "gütl.bes.-sohn", "21", "Lungenentzündung", "/", JC, False, False, "M"),
    E("s183", 177, "31", "Mai/Juni", "31.", "2.", "Gradec", "64", "Martin Kovačič", "gütl.bes.-Kind? [~Gärtners-glyph]", "5 Monat", "Fraisenfall? [~Wrußfall-glyph]", "/", JC, False, False, "M"),
    E("s183", 177, "32", "Juni", "1.", "3.", "Griblje", "1", "Katharina Zefslo [~Zelško — ISTI-glyph-kot-z14!]", "'hünno-Kind'-glyph [~unehel.?]", "9 Monate", "Friseln [FRISELN-FLOOD-9/16!]", "/", JC, True, True, "F"),
    E("s183", 177, "33", "Juni", "3.", "4.", "Griblje", "8", "Anne Jakofčič", "Wirtstochter [~hirtstochter-glyph]", "10 Monate [VLM-'10-dni'-ZAVRŽEN!]", "Friseln [FRISELN-FLOOD-10/16!]", "/", JC, True, True, "F"),
    E("s183", 177, "34", "Juni", "26.", "28.", "Gradec", "49", "Ursula Malerič? [~Malenč-glyph]", "Gawerßmörin? [~Gastwirtin-glyph — 3.×!]", "38", "Wassersucht [Waſſerſucht-glyph — 2/4!]", "/", JC, False, False, "F"),
    E("s183", 177, "35", "Juli", "3.", "5.", "Griblje", "29", "Michael Husič", "Mühlzügler [MÜHLZÜGLER-×6-4/6!]", "44", "Wassersucht [Waſſerſucht-glyph — 3/4! VLM-'Nervenfieber'-ZAVRŽEN!]", "/", JC, True, True, "M"),
    E("s183", 177, "36", "Juli", "18.", "20.", "Kloster", "39", "Maria Klemenčič", "unehel. Tohtr. + opomba [~'der-?-Dienstmagd'-neberljivo]", "4 Tagen", "Friseln [FRISELN-FLOOD-11/16!]", "/", JC, False, False, "F"),
    E("s183", 177, "37", "Juli", "15.", "17.", "Griblje", "10", "Peter Mravinec? [~Mravinic-glyph]", "'Dienst' [~Dirnst-glyph?]", "45 [VLM-'48'-ZAVRŽEN!]", "Tuberculose", "/", JC, True, True, "M"),
    # --- s184 (Pag. 178) = z38–z46 ---
    E("s184", 178, "38", "August", "1.", "3.", "Griblje", "54", "Matthias Šimec", "'hünno-sohn'-glyph + 'innestlınwistöchton' [~2-vrstični-stan!]", "20", "Tuberculose", "/", JC, True, True, "M"),
    E("s184", 178, "39", "August", "6.", "7.", "Krasinec", "13", "Johann Jaklevič [~]", "'hünno-Kind'-glyph [~]", "10 Monate", "Friseln [FRISELN-FLOOD-12/16!]", "/", JC, False, False, "M"),
    E("s184", 178, "40", "August", "7.", "9.", "Gradec", "29", "Maria Husič? [~Musič-glyph]", "Fabrikarbeiters-tochter [★★★ FABRIKA-1.×-PREDZGODOVINE!]", "5 Monat", "Fraisenfall? [~Wrußfall-glyph]", "/", JC, False, False, "F"),
    E("s184", 178, "41", "August", "10.", "11.", "Gradec", "29", "Johann Bartl", "'Wfo.bes-Kind'-glyph [~neberljivo]", "3 Monate", "Tuberculose", "/", JC, False, False, "M"),
    E("s184", 178, "42", "August", "18.", "19.", "Prilozje", "29", "Jakob Hrambič? [~Krambič-glyph]", "½ Z. [~½-gütl.bes]", "45 [VLM-'4½-leta/45-mesecev'-ZAVRŽEN!]", "Lungenentzündung", "/", DVG, False, False, "M"),
    E("s184", 178, "43", "August", "20.", "22.", "Griblje", "65", "Maria Milek", "½ Z. [~½-gütl.bes] + Wirthsthum? [~]", "47", "Abzehrung", "/", JC, True, True, "F"),
    E("s184", 178, "44", "August", "25.", "27.", "Griblje", "55", "Agnes Šimec", "'hünno-Kind'-glyph [~unehel.?]", "1½ Jahr [VLM-'11/12-let'-ZAVRŽEN!]", "Wassersucht [Waſſerſucht-glyph — 4/4!]", "/", JC, True, True, "F"),
    E("s184", 178, "45", "September", "9.", "10.", "Primostek", "3", "Maria Tome", "½ Zii.? [~] gütlstochter? [~]", "4 J.", "Angina", "/", DVG, False, False, "F"),
    E("s184", 178, "46", "September", "17.", "19.", "Griblje", "68", "Nikolaus Mrh.? [~URH?! — M/U-glyph-zmeda!]", "½ gütl.bes.-sohn", "7 J. [VLM-'4-leta'-ZAVRŽEN!]", "Krämpfe [~Primpfe-glyph]", "/", JC, True, True, "M"),
    # --- s185 (Pag. 179) = z47–z58 ---
    E("s185", 179, "47", "Oktober [1882-svinčnik-margin!]", "18.", "19.", "Primostek", "17", "Barbara Tome", "½ gütl.bes.-tochter", "3 Wochen [~]", "Friseln [FRISELN-FLOOD-13/16!]", "/", "PRAZNO? [~neviden]", False, False, "F"),
    E("s185", 179, "48", "Oktober", "18.", "20.", "Dobravce", "39 ex 13 [~COMPOUND!]", "Katharina Pust", "Ablalannin? [~neberljivo]", "73", "Asthma [ASTHMA-×3-1882-1/3!]", "/", DVG, False, False, "F"),
    E("s185", 179, "49", "November", "5.", "7.", "Zemelj", "21", "Katharina MUC", "Ablalannin? [~ISTI-glyph-kot-z48!]", "68", "Asthma [ASTHMA-×3-1882-2/3!]", "/", DVG, False, False, "F"),
    E("s185", 179, "50", "November", "9.", "9.", "Dragoše", "4", "TODTGEBOREN [brez-imena!]", "—", "PRAZNO", "gift-blähung? [~blede-neberljivo]", "/", "PRAZNO [~blede]", False, False, "M"),
    E("s185", 179, "51", "November", "18.", "20.", "Germ. [= ZEMELJ-forma!]", "33", "Maria Zilah? [~Gilak/Filak-forma-glyph]", "spät. gütl.bes.-tochter [~]", "4 Jahren", "Diphtheritis ; Angina [★★★ DAVICA-NIT-nazaj-na-NOV-1882-1/2!]", "/", DVG, False, False, "F"),
    E("s185", 179, "52", "November", "20.", "20.", "Hrast", "1.", "Pust-[Lawrenz?/Ambros?-glyph]-Pust? [~DVOJNO-PUST!]", "des Johann Tome [~sin-Johann-Tomega?]", "PRAZNO", "PRAZNO", "/", "PRAZNO? [~blede-squiggle]", False, False, "M"),
    E("s185", 179, "53", "November", "29.", "31.", "Wha-Re.? [~NEZNANA-VAS! — Vrhreke?-glyph]", "5.", "Martin Vrižan [~Križan-glyph]", "½ gütl.bes.-sohn", "1 Jahr", "Diphtheritis ; Angina [★★★ DAVICA-NIT-2/2!]", "/", DVG, False, False, "M"),
    E("s185", 179, "54", "December", "10.", "12.", "Prilozje", "31", "Ana Jaklevič [~]", "gütl.bes.-tochter? [~Gütlbstöchtn-glyph]", "1 Jahr", "Friseln [FRISELN-FLOOD-14/16!]", "/", DVG, False, False, "F"),
    E("s185", 179, "55", "December", "13.", "15.", "Boršt", "21.", "Mathias Klepec [ISTI-IME-kot-z6!]", "Mühlzügler [MÜHLZÜGLER-×6-5/6!]", "63", "Asthma [ASTHMA-×3-1882-3/3!]", "/", DVG, False, False, "M"),
    E("s185", 179, "56", "December", "11.", "13.", "Griblje", "13", "Micolav [~Nikolav!] Jakofčič", "'hirtsto-Kind'-glyph [~unehel./Wirths-?]", "21 Tagen", "Friseln [FRISELN-FLOOD-15/16!]", "/", JC, True, True, "M"),
    E("s185", 179, "57", "December", "23.", "24.", "Certoviše", "14", "Ana Stanadinič? [~Haradinič-glyph]", "unehel. Tohtr. der ledigen Dienstmagd Barb. Stanadinič [IZPISANO!]", "5 Monat", "Abzehrung", "/", JC, False, False, "F"),
    E("s185", 179, "58", "December", "24.", "26.", "Griblje", "50", "Cath. Peclir? [~Beclir/Reclic-glyph — VLM-'h31-Rutar'-ZAVRŽEN!]", "MÜHLZÜGLERIN [ženska-forma! MÜHLZÜGLER-×6-6/6!]", "83 = NAJSTAREJŠI-1882", "Marasmus", "/", "Franz Jančar 'R.C.-Pfarr.'", True, True, "F"),
    # --- s186 (Pag. 180) = z59 (1882-TAIL) + MEJA-1882/83 + [1883-z1–z2-P194] ---
    E("s186", 180, "59", "December", "26.", "28.", "Dragoše", "4", "Mikolaus Dragos [~Dragoš-glyph]", "innwor-blinf-glyph [~unehel.-Kind-glyph-družina? cf.-P194-'Inwohner?']", "2 Monate [P194-dokaz-'9-mesecev' → P195-max-zoom-'2-mesecev' — glifna-dokumentirana!]", "Frais(en) [P194-'Frauenkrankheit?' → P195-max-zoom-'Fraisen' — glifna-dokumentirana!]", "/", JC, False, False, "M",
      "1882-TAIL (ŽE-viden-P194-dokaz! Znova-preverjen-max-zoom!) + nato MEJA-1882/83 (veliki-cifri-'1'-'8'-L + '8'-'3'-R = SPLIT-ČEZ-RAZPON = 33.-POTRDITEV-P194 + 'Jänner' + restart-z1!)"),
]

grib = [e for e in entries if e["griblje"]]

dokaz = {
    "faza": "P195",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1882 = 4/29 (issue #18)",
    "knjiga": {
        "signature": "04106",
        "obdobje": "1857–1885 (208 skenov; platnica s208 'PODZEMELJ / M / 1857–1885')",
        "zupnija": "Podzemelj (Belokrajina)",
        "vrsni": "mrliški vpisi (Sterb-Buch — nemška forma)",
        "vir": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
    },
    "okvir": {
        "leto_1882": "z1 = Jänner 7./9. (s180-top); '1882.'-glava-desno + 'Jänner' + 'Anno-Domini'-zapis-v-imenskem-stolpcu",
        "meja_1881_82": "s180-top ('1882.'-glava + 'Jänner' + 'Anno-Domini' + restart-z1 = 34.-POTRDITEV-invariante!)",
        "meja_1882_83": "s186 (ŽE-P194: veliki-cifri-'1'-'8'-L + '8'-'3'-R = SPLIT-ČEZ-RAZPON = 33.-POTRDITEV + NOVA-TEHNIKA-#9!)",
        "konec_1882": "s186-z59-December-26/28 (Drugoše-4-Mikolaus-Dragoš-2-Monate-Frais(en)en)",
        "zaporedna": "z1–z59 (59 vpisanih vrstic — brez-duplikatov-leta!)",
        "forma": "nemška-tiskana-'Sterb-Buch'-skroz (slovenska-šele-1885-s205/s206-P192!)",
        "skeni": "s180–s186 (7 skenov; Pag. 174–180 = sken − 6!)",
        "preštevanje": "pag == sken − 6: s180-174 ✓ + s181-175 ✓ + s182-176 ✓ + s183-177 ✓ + s184-178 ✓ + s185-179 ✓ + '.59'-margin-s186 ✓ (10.–16.-potrditev-preslikave!)",
    },
    "statistika": {
        "vpisane_vrstice": 59,
        "griblje_vpisov": len(grib),
        "griblje_hise": sorted({int(e["hisna"]) for e in grib}),
        "griblje_hise_x2": ["h1 (ZELŠKO-×2: z14 + z32)", "h54 (ŠIMEC-×2: z17 + z38)"],
        "nove_hise_04106": ["h73 (Lupanič — prvi-dokaz? [~])"],
        "najstarejsa": "z58-h50-Cath.-Peclir?-83-let (Marasmus)",
        "najmlajsa": "z3/z6-2-Tagen + z36-4-Tagen + z50-Todtgeboren",
        "male": sum(1 for e in entries if e["spol"] == "M"),
        "female": sum(1 for e in entries if e["spol"] == "F"),
    },
    "anomalije": [
        "★★★ MEJA-1881/82-s180-top: '1882.'-glava-desno + 'Jänner' + 'Anno-Domini'-zapis-v-imenskem-stolpcu + restart-z1 = 34.-POTRDITEV-invariante!",
        "★★★ FRISELN-FLOOD-×16-1882: z2 + z3 + z6 + z7 + z10 + z15 + z23 + z24 + z32 + z33 + z36 + z39 + z47 + z54 + z56 + z59 — večinoma OTROCI (febrilni-krampi-epidemija — največja-posamezna-bolezen-valova-v-predzgodovini!)",
        "★★★ WASSERSUCHT-×4: z29 + z34 + z35 + z44 — Waſſerſucht-glyph-forenzika (dolgi-ſ-ligatura-RAZREŠILA-'Maffen-'-zmedo — NOVA-forenzična-uledba!)",
        "★★★ DAVICA-NIT-RAZŠIRJENA-NAZAJ-NA-NOVEMBER-1882: Diphtheritis-;Angina-×2 (z51-Zemelj-'Germ.'-4J + z53-'Wha-Re.'?-1J) — nit: NOV-1882 → okt-dec-1883-P194-×4 → mär-1885-P192 = 3-leta-niti!",
        "★★★ ASTHMA-×3-1882: z48-Dobravce-73J + z49-Zemelj-68J + z55-Boršt-63J (cf. ×3-1883-P194 — nit-2-leta!)",
        "★★★ MÜHLZÜGLER-×6-1882 = MLINARSKA-VALOVA: z1-Wolk-Palič + z11-Vranoviče-Jaklša + z29-Certoviše-Jalkovič + z35-GRIBLJE-h29-Husič + z55-Boršt-Klepec + z58-GRIBLJE-h50-Peclir-ženska-forma (MÜHLZÜGLERIN-1.×!)",
        "★★★ TODTGEBOREN-z50-Dragoše-4: brez-imena + starost-PRAZNO + bolezen-blede [~gift-blähung?] + duhovnik-PRAZNO (cf. P194-z7-Hrast + z27-Otok!)",
        "★★★ z52-Hrast-1-DVOJNO-PUST: 'Pust-[Lawrenz?/Ambros?-glyph]-Pust?, des Johann Tome' + starost-PRAZNO + bolezen-PRAZNO + duhovnik-blede (cf. P194-z69-h78!)",
        "★★★ FABRIKARBEITERS-tochter-z40-Gradac-29: Maria-Husič — FABRIKA-1.×-PREDZGODOVINE (industrija-v-globoki-preteklosti!)",
        "★★★ MIGRANT-z25-Gradac-64: Fran-Ulčer 'Kind der hiesigen Dienstmagd Maria Ulčer in Meriška vas H 21, Pfarre Toplice' = TUJA-PAROŠIJA-1.×-PREDZGODOVINE!",
        "Dobravce-'39-ex-13'-COMPOUND-hišna-številka (z48-Katharina-Pust!)",
        "'Germ.'-vas-forma-×2 (= ZEMELJ — 2.-potrditev-forme-P194-'Germ'-×3!): z51 + cf.-z49-Zemelj!",
        "'Wha-Re.'?-NEZNANA-VAS [?] (z53-Martin-Vrižan-[~Križan?] — Vrhreke?-glyph-neberljiva!)",
        "'unehel./hiesig.-Kind'-GLIF-DRUŽINA-×4: z32 + z38 + z56 + z59 [~ne-ločljivo] + izpisano-z57-'unehel. Tohtr. der ledigen Dienstmagd'!",
        "'spät.'-gütl.bes.-tochter-×2 (z22-Gradac-80 + z51-Zemelj-33!)",
        "JAKLŠA-×3-v-2-DNEH (z11-Vranoviče + z12-Gradac + z13-Kloster — 3-vasi-3-hiše!)",
        "h64-Gradac-×3-v-54-dneh (z21-Georg-Kovačič-72 + z25-Fran-Ulčer-migrant-14M + z31-Martin-Kovačič-5M!)",
        "Boršt-KLEPEC-×2-ISTI-IME-Mathias (z6-h16-2-Tagen-februar + z55-h21-63-let-december!)",
        "Krasinec-13-×3 (z16-Nikolaus-68 + z28-Ana-23 + z39-Johann-10M!)",
        "PEZDIRC-'Pozdire'-×3 (z2-GRIBLJE-h20-5M + z3-Barbara-2T + z5-Maria-36J — 1-Griblje + 2-Krasinec-3!)",
        "h1-ZELŠKO-KATASTROFA-×2-v-71-dneh (z14-Maria-32-März + z32-Katharina-9M-Juni — mati+hči?-hipoteza [~]!)",
        "h54-ŠIMEC-KATASTROFA-×2-v-5-mesecih (z17-Anna-wittwe-46-März + z38-Matthias-20-August! + h55-Agnes-1½J = ŠIMEC-mreža-×3-1882!)",
        "h68-'Mrh.'?[~URH!]-M/U-GLIF-ZMEDA (z46 — 4-mesece-pred-URH-×2-1883-P194-JANUARSKA-KATASTROFA!)",
        "VLM-stran-zavrnitve-×8: s184-'leto-1884'→1882! + s186-missed-z59 (1883-rows-prebrani!) + z58-'h31-Rutar'→GRIBLJE-h50-Peclir! + z15-'9-let-Grippe'→9-MESECEV-Friseln! + z33-'10-dni'→10-MESECEV! + z42-'4½-leta/45-mesecev'→45-JAHR! + z37-'48'→45! + z2-s180-'Anna-Peglič'→Pozdire!",
        "z59-GLIFNA-REREAD: P194-dokaz-'9-mesecev-Frauenkrankheit?' → P195-max-zoom-'2-mesecev-Frais(en)' (starost-digitalni-glif == datum-'2'-glif! [~dokumentirana-dokumentirana])",
        "'Wrußfall'-glyph-×3-infanti (z25 + z31 + z40 [~Fraisenfall?])",
    ],
    "duhovniki": {
        "Jančar-dominanta": "Franz-JANČAR-'v.R.C.-Pfarrer/Priester'-DOMINANTA-~25+ (2-vrstični-podpis: ime + title-vrstica! cf. 1883-P194-#30-dominanta — 2.-LETO-ZAPORED!)",
        "Dovgan": f"Franz-DOVGAN-×~12 ('Dorgun'-forma-cf.-P194!)",
        "Jakob-Dovgan-NOVI": "Jakob-DOVGAN-z10-s180 = NOVI-DUHOVNIK-KANDIDAT-#31 (1.×-predzgodovine! Dovgan-družina-2-duhovnika-1882!)",
        "Jančar-coop": "Franz-JANČAR-coop.-×4 (z9-s180 + z11 + z12-s181 + cf.)",
        "opomba": "z47-duhovnik-PRAZNO? [~neviden] + z50/z52-duhovnik-PRAZNO/blede!",
    },
    "epidemija": {
        "Friseln-Flood": "×16-1882 (febrilni-krampi — večinoma-otroci-1½J↓ — 27% vseh-vrstic!)",
        "Wassersucht": "×4-1882 (z29 + z34 + z35 + z44 — odrasli-38–48J + 1-otrok!)",
        "Davica-nit": "NOV-1882-×2 (z51 + z53) → okt-dec-1883-×4-P194 → mär-1885-P192 = DIPHTHERIA-3-LETNICA!",
        "Asthma-nit": "×3-1882 (z48 + z49 + z55) → ×3-1883-P194 = ASTHMA-2-LETNICA!",
        "Tuberculose": "×9-1882 (z5-Lungentuberculose + z13 + z16-Abzehr + z26 + z28 + z30 + z37 + z38 + z41)",
        "Abzehrung": "×7-1882 (z9 + z16 + z17 + z19 + z43 + z57 + cf.)",
    },
    "hišne_kontinuitete": [
        "h1-GRIBLJE: ZELŠKO-×2-1882 (z14 + z32) → Dragot-DAVICA-1885-P192!",
        "h8-GRIBLJE: JAKOFČIČ-1882 (z33) → JABLKONIČ/JALENČIČ-×3-1884-P193 (priimek-zmeda-2-leta!)",
        "h10-GRIBLJE: MRAVINEC-1882 (z37) → ALUŠIČ-1884-'NOVA-mrliška-hiša'-P193-z76!",
        "h13-GRIBLJE: JAKOFČIČ-1882 (z56) → poročna-1885-'Janez-Jakobič-h13'-Leinweber! + Kusič-1885-P192-z61! + P154-1888!",
        "h20-GRIBLJE: PEZDIRC-1882 (z2) → PERDIH-90-let-1883-P194-z6! + krstna-1895-P91!",
        "h29-GRIBLJE: HUSIČ-MÜHLZÜGLER-1882 (z35) → cf. h37-Husić-DAVICA-1883-P194-z70 (HUSIČ-mreža!)",
        "h50-GRIBLJE: PECLIR?-MÜHLZÜGLERIN-83-let-1882 (z58 — izven-PT-vzorca-42–60-brez-h50-P191!)",
        "h54-GRIBLJE: ŠIMEC-×2-1882 (z17-wittwe + z38) → SIMEC-1885-P192-z64!",
        "h55-GRIBLJE: ŠIMEC-Agnes-1882 (z44) → cf. Gradac-55-1884-P193 [~različna-vas]!",
        "h65-GRIBLJE: MILEK-1882 (z43) → 1922-№2-MILEK-h68 + 1914-h68-MLAKOVA (MILEK/MLAK-mreža!)",
        "h68-GRIBLJE: 'Mrh.'?[~URH!]-1882 (z46) → URH-×2-1883-P194 (v-4-mesecih!) + ALTH-1885-P192 + MILEK-1922!",
        "h69-GRIBLJE: TERDIČ-Wirth-1882 (z18) → BRINE-1884-P193-z52-REWRITE (BRINEC-mreža-1901!)",
        "h73-GRIBLJE: LUPANIČ-1882 (z24) = NOVA-mrliška-hiša? [~prvi-dokaz!]",
        "PLUT-NIT: Jožef-PLUT-Gradac-16-1882 (z26) → Klošter-36-×3-1883-P194 (z10 + z14 + z21)!",
        "TOME-nit: z23-Krivoglavce + z45 + z47-Primostek + z52-Hrast-'des-Johann-Tome' (×4-1882!)",
        "JAKLEV/ČIČ-nit: z16 + z28-Krasinec-13-×2 + z39 + z54-Prilozje (×4!)",
    ],
    "forme": [
        "nemška-tiskana-'Sterb-Buch'-skroz (slovenska-šele-1885-s205/s206-P192!)",
        "'Germ.'-ZEMELJ-vas-forma-×2 (P194-'Germ'-×3-potrditev!)",
        "MÜHLZÜGLER-ženska-forma-'MÜHLZÜGLERIN'-1.×-predzgodovine (z58!)",
        "spät.-pred-stanom-×2 (z22 + z51 — 'spät.' = pokojni-starš? [~])",
    ],
    "crossChecks": [
        "s180-pag-174 ✓ + s181-pag-175 ✓ + s182-pag-176 ✓ + s183-pag-177 ✓ + s184-pag-178 ✓ + s185-pag-179 ✓ + s186-'59'-margin ✓ (pag == sken − 6 — 10.–16.-potrditev-preslikave!)",
        "meja-1881/82-s180-top (34.-potrditev!) + meja-1882/83-s186-P194 (33.-potrditev!) — 2-MEJI-v-1-letu-kontekstu!",
        "z1–z59-številčenje-neprekinjeno (brez-duplikatov-leta — cf. z33-DUPLIKAT-1883-P194!)",
        "59-vrstic-vizualno == 59-pričakovano (P194-LEAD!) == 59-VLM-vrstic-po-korekciji (VLM-68 → kurator-59!)",
        "16-Griblje-vizualno (s180-1 + s181-4 + s182-1 + s183-4 + s184-4 + s185-2) — vsi-preverjeni-max-zoom!",
        "h1-×2 + h54-×2-vizualno ✓ (ZELŠKO-mati+hči? + ŠIMEC-wittwe+sin?)",
        "1883-z1/z2-na-s186-pod-mejo (P194-konzistentno!)",
        "Jančar-2-vrstični-podpis-1882 == 1883-'v.R.C.-Pfarrer'-P194-potrditev (isti-podpis-2-knjigah!)",
    ],
    "honesty": {
        "H1": "8-glyph-celic-neberljivo-dokumentirane z [~]: '+Güblanc' (z2) + 'Zigernmodlina' (z8) + 'Gwerger?-sohn' (z19) + 'Krizüngs?-gütlng' (z20) + 'hibign-dirbnde' (z21) + 'Zmqshipes' (z25) + 'Ablalannin'-×2 (z48 + z49) + 'hünno/kinnes/hirtsto-Kind'-glifi-×4",
        "H2": "z50-Todtgeboren: starost-PRAZNO + bolezen-blede [~gift-blähung?] + duhovnik-PRAZNO — PRAZNI-polji-dokumentirani!",
        "H3": "z52-dvojno-PUST: ime-nejasno [Lawrenz?/Ambros?-glyph] + starost-PRAZNO + bolezen-PRAZNO + duhovnik-blede — 4-nejasnosti-dokumentirane!",
        "H4": "z53-'Wha-Re.'?-vas-NEBERLJIVA [?] — NEZNANA-VAS-dokumentirana (ne-pripisana-nobeni-znani-vasi!)",
        "H5": "z59-razlika-P194-'9-mesecov/Frauenkrankheit?' vs P195-max-zoom-'2-mesecev/Frais(en)' — OBE-branja-dokumentirani [~]",
        "H6": "z48-'Ablalannin'-stan-glyph == z49-ISTI-glyph (2-različni-vasi-ISTI-stan-glyph [~neberljivo])",
        "H7": "z14/z32-'Zefslo'-3-branja (Zefslo/Zelško/Zeliško) — ime-dokumentirano-3-branja!",
        "H8": "z46-'Mrh.'?-M/U-glyph-zmeda [~URH!] — OBE-branja-dokumentirani (h68-continuiteta-hipoteza!)",
        "H9": "VLM-68-vrstic → kurator-59 (VLM-duplirate-meja-vrstice + 1883-rows-s186) — številčenje-kuratorja-vizualno-100%!",
        "H10": "z47-duhovnik-PRAZNO? [~neviden] — možno-oblede/izpuščeno-dokumentirano!",
        "H11": "'Güblanc'-glif-z2-nejasno [~Gütl.bes.-glif-družina?] — 2-branja-dokumentirana!",
        "H12": "z2-starost-'5 [~8?]'-meseci — Kurrent-5/8-glyph-zmeda-dokumentirana!",
    },
    "kaskada": {
        "vitals": "1267 → 1324 (+16 blokov 04106-1882!)",
        "04106": "48 → 64 (16×-1885 + 21×-1884 + 11×-1883 + 16×-1882!)",
        "04894": "520-NESPREMENJENO",
        "p80": "94-NESPREMENJENO",
        "korpus": "93-NESPREMENJEN",
        "pt_luknja": "18-NESPREMENJENA (h50-izven-vzorca-42–60-brez-h50!)",
        "qa": "qa-p195 = 195.-kontrola + 106×-1267→1324 + p192-QA (bloki-48→64 + leta-{1882,1883,1884,1885}!) + stale-sanacija",
    },
    "lead": {
        "P196": "mrliška 04106, leto 1881 (s174–s180-probe!) — 1881-tail-s180-top-ŽE-viden ('1882.'-glava + restart-z1 = meja-1881/82-na-s180-TOP → 1881 = s174–s179 + probe!)",
        "krstna": "04104-1871–1885-×200-skenov-čaka (vzporedno!)",
        "poročna": "04455-zacetek-1873–1885-čaka",
    },
    "entries": entries,
    "notes": [
        "Nastalo: P195 (2026-11-03) — VLM-branje ×7 (p195_read_page.mjs) + kurator-vizualna-forenzika ×38-crops (p195_crops.py) + max-zoom-comparisons (kind-stan ×4 + urh-mrh + massen ×5)",
        "VLM-uspešnost: 7/7-strani-JSON-ok; ampak-68-vrstic-raw → 59-po-korekciji (8-stran-zavrnitev!)",
        "pag == sken − 6 potrdjen-vseh-7-straneh (marginal-čevlji!)",
        "FRISELN-FLOOD = največja-posamezna-bolezen-valova-v-predzgodovini-do-sedaj (16/59 = 27%)!",
        "MÜHLZÜGLER-×6 = mlinska-valova (6/59 = 10%!) — inkluzivno-ženska-forma-MÜHLZÜGLERIN-z58!",
        "DAVICA-nit-sedem-3-leta: NOV-1882 → 1883 → 1885!",
        "ASTHMA-nit-2-leta: ×3-1882 → ×3-1883!",
        "viri: Matricula-04106-s180–s186",
    ],
}

out = f"{ROOT}/research/issue17/parish-death-1882-04106.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(dokaz, f, ensure_ascii=False, indent=2)
print(f"dokaz: {out}")
print(f"entries: {len(entries)} ({len(grib)} Griblje, {len(entries)-len(grib)} ne-Griblje)")
print(f"anomalije: {len(dokaz['anomalije'])}")
print(f"honesty: {len(dokaz['honesty'])}")
print(f"hiše: {sorted({int(e['hisna'].split()[0]) for e in grib})}")
