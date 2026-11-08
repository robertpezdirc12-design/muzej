#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P175 — gradnik dokaza research/issue17/parish-death-1909.json (55 entries)."""
import json

def E(row, zap, house, scan, mesec, smrt, pokop, vas, ime, stan, starost, bolezen, pv, duh, op=None):
    return {"row": row, "zap": zap, "houseNo": house, "bookSignature": "04894", "year": 1909,
            "scan": scan, "page": scan - 1, "mesec": mesec, "smrt": smrt, "pokop": pokop,
            "vas": vas, "ime": ime, "stan": stan, "starost": starost, "bolezen": bolezen,
            "previden": pv, "duhovnik": duh, "opomba": op}

ent = []
# ——— s121 (str. 120): 1909-zap1–10 (za velikim separatorjem '1909.' — P174-meja!) ———
ent.append(E(1, 1, "16", 121, "Januar", "8", "10", "Krasinec", "Anton Žužanič [~ P174-lead-'Žugarič']", "¼ zemljakov sin", "4 mesece", "Jelika [~ Jetika]", ".", "Gregor Cerar mgn.", "ne-Griblje; VLM-raw"))
ent.append(E(2, 2, "31", 121, "Januar", "13", "15", "Gradac", "Matija Viličič", "starjena ¼ zemljak", "63 let", "Hujšnica [~ hujšanje]", "1", "Gregor Cerar", None))
ent.append(E(3, 3, "4", 121, "Januar", "13", "14", "Petrovišče", "Peter Stublar", "vdovec in vžigalec [~ 'ožigkar'-P174-lead]", "92 let", "Starost", "1.", "Gregor Cerar", "★★★ 92-let = IZENAČENJE-REKORDA-LINIJE (1889-P155-92!) — 2.×-92-v-liniji!"))
ent.append(E(4, 4, "36", 121, "Januar", "18", "20", "Gorenje", "Neža Bajuk", "¼ zemljakova hči", "3 dni", "Slabost / Vmedje pljuči [~ vmedju-pljuč]", ".", "Gregor Cerar", None))
ent.append(E(5, 5, "31", 121, "Januar", "25", "24 [~]", "Otok", "Neža Novak", "¼ zemljaka hči", "10 dni", "Božjast", ".", "Gregor Cerar", "pokop-VLM-'24'-pred-smrtjo-'25'-[?] — VLM-podatna [~]"))
ent.append(E(6, 6, "59", 121, "Februar", "1", "3", "Gradac", "Ana Novanič", "svojemca bajtariča [~]", "63 let", "Mrtvoud-[?] [★ X-ANOMALIJA — VLM-'Mrkavud']", "1", "Gregor Cerar", "★ z6-'Mrtvoud-[?]' = X-ANOMALIJA (63-let + pokop-3-dni — NI-mrtvorojen! P174-lead-'z6-MRTVOROD'-POL-KOREKCIJA — samo-z7-jest!)"))
ent.append(E(7, 7, "68", 121, "Februar", "1", "2", "Gradac", "J. Mihelič", "¼ zemljakov otrok", ".", "Mlozgajena [~ mrtvorojena]", ".", "——", "★★ MRTVOROJEN-#1 (starost-'.' + podpis-'——' — r53-vzorec-#18!)"))
ent.append(E(8, 8, "18", 121, "Februar", "9", "11", "Primostek", "Helena Županič", "omožena ½ zemljakinja", "24 let", "Jelika [~ Jetika]", "1", "Jos. Pauč [~]", None))
ent.append(E(9, 9, "5", 121, "Februar", "21", "23", "Krasinec", "Barbara Junačevič", "½ zemljakova hči", "2 leti", "Jetka [~ Jetika]", ".", "Gregor Cerar", None))
ent.append(E(10, 10, "22", 121, "Februar", "22 ★★★ pisar-korekcija-nad-prečrtanim-'24'", "24", "Dobravice", "Ana Štefanič", "vdova in bajtariča", "59 let", "Maduha [~ Naduha]", "1", "Jos. Pauč [~]", "★★ z10-PISAR-KOREKCIJA: smrt-'22'-nad-prečrtanim-'24' (1. številčna-korekcija-v-vrstici-linije!)"))
# ——— s122 (str. 121): zap11–22 ———
ent.append(E(11, 11, "2", 122, "Februar", "25", "27", "Griblje", "Barbara TOME", "vdova vrškarica [~ VLM-'vrhbašica']", "86 let", "Naduhova", "1", "Jos. Rauq [★★ VLM-'Jož.-Punc'-ZAVRJENO!]", "★★ diag-'Toma'-KOREKCIJA — max-zoom-'Tome.'-s-piko! + h2 = 8. mrliški vpis (1892 + 1897-×2 + 1902 + 1904 + 1905 + 1908 + 1909!)"))
ent.append(E(12, 12, "13", 122, "Februar", "28", "1. marca", "Žorinja vas [~ Črnomelj?]", "Katarina Nemanič [~ NEMANIŠ-vez-P173!]", "žafranica, omožena [~]", "71 let", "Slabost", "1", "Gregor Cerar", None))
ent.append(E(13, 13, "15", 122, "Februar", "28", "2", "Obrhoviče", "Janez Mavrin", "¼ zemljak", "68 let", "Naduhova", "1", "Gregor Cerar", None))
ent.append(E(14, 14, "29", 122, "Marec", "11", "13", "Hrasinca [~ Hrasinec]", "Jurij Kupančič", "¼ zemljak", "73 let", "Naduhova", "1", "Gregor Cerar", None))
ent.append(E(15, 15, "30", 122, "Marec", "16", "18", "Gradac", "Vincencij Jožečič", "sinjer bogatac [~]", "71 let", "Slabost", "1", "Gregor Cerar", None))
ent.append(E(16, 16, "15", 122, "Marec", "23", "25", "Griblje", "Marija JAKOFČIČ [~ max-zoom-'Jakfjič'-forma-ISTA-kot-z51-Brošt!]", "½ zemljakova kmetica [~ VLM-'1/4 zemljiška kmetica']", "75 let", "Jetika", "1", "Gregor Cerar", "~ VLM-'Jakše'-ZAVRJENA + h15 = 3. mrliški vpis (1886-Muc + 1897-JAKLIČ + 1909! = 3-priimka-hiše!) + P132-leksikon"))
ent.append(E(17, 17, "43", 122, "April", "8", "10", "Griblje", "Marija LAŠIČ [~ max-zoom-'Lasič'-s-karonom — cf.-P153-h43-1887!]", "omožena ½ zemljakinja [★★ VLM-'komuflarij'-ZAVRJENO]", "64 let [★★★ P174-lead-'84'-KOREKCIJA — KURRENT-6 = samo-spodnja-zanka!]", "Narust [★★ crop-korekcija — VLM-'Slabost']", "1", "Gregor Cerar", "★★★ P174-LEAD-KOREKCIJA-'84'→64 + hiša-'43'-jasno-ne-13! + h43 = 3. mrliški vpis (1887 + 1892 + 1909!)"))
ent.append(E(18, 18, "9", 122, "Marec", "13", "15", "Vranoviče", "Marija Hemic [~]", "vdova vrškarica [~]", "76 let", "Slabost", "1", "Gregor Cerar", None))
ent.append(E(19, 19, "30", 122, "Marec", "16", "18", "Hrasinca [~]", "Marija Jakša", "vdova vrškarica [~]", "74 let", "Slabost", "1", "Gregor Cerar", None))
ent.append(E(20, 20, "12", 122, "Marec", "18", "20", "Otok [~ VLM-'Otak']", "Anton Hire [~]", "bajtarjev sin", "11 mesecev", "Pljučnica", ".", "Gregor Cerar", None))
ent.append(E(21, 21, "34", 122, "Marec", "19", "20", "Griblje", "Matija ŠILAK [★★★ max-zoom-'Šilak'-karon-nad-S!]", "½ zemljakov sin", "½ dne [★★★ NAJKRAJŠA-STAROST-GRIBLJE-KADARKOLI!]", "Slabost", ".", "Gregor Cerar", "★★★ ŠILAK-DVOJČKI-#1 (P174-lead-100%-POTRJEN — VLM-'Tlak'-×2-ZAVRJEN!) + h34 = 5. mrliški vpis"))
ent.append(E(22, 22, "34", 122, "Marec", "21", "22", "Griblje", "Nikolaj ŠILAK [★★★ max-zoom-×2!]", "½ zemljakov sin", "2 dni", "Slabost", ".", "Gregor Cerar", "★★★ ŠILAK-DVOJČKI-#2 (2-dni-apart — PADEC-vzorec-6.-leto!) + h34 = 6. mrliški vpis + NIKOLAJ-ime-vez (cf.-×3-1908!)"))
# ——— s123 (str. 122): zap23–34 ———
ent.append(E(23, 23, "15", 123, "Maj", "3", "5", "Gradac", "Marija Marentič", "omožena ž.-romfalšinja [~]", "36 let", "Jetika", "1", "Gegor Čerar [~ VLM-raw]", None))
ent.append(E(24, 24, "16", 123, "Maj", "8", "10", "Dobravica", "Marija Matkovič", "omožena vrškarica [~ VLM-'vdiškarica']", "64 let", "Vodeniča [~ vodeniča]", "1", "Jos. Rumpf [~ VLM-raw — cf.-RAUQ-lekcija]", None))
ent.append(E(25, 25, "29", 123, "Maj", "11", "13", "Griblje", "Marija KRIŽAN [~ max-zoom-isti-glyph-kot-z52! cf.-h36-1882-poročna-Mathias-KRIŽAN + 1888-×5-krstna!]", "kmečka delavka [~ 1.-TA-STAN-linije? cf.-X7-Notarica]", "74 let", "Naduhova [★★ crop-korekcija — VLM-'Nadutba']", "1", "Gregor Cerar [~ VLM-'Gegor-Čerar']", "~ VLM-'Vržan'→KRIŽAN[~] + h29 = 5. mrliški vpis (1886-×3-EPIDEMIJA + 1901 + 1909!)"))
ent.append(E(26, 26, "28", 123, "Maj", "22", "24", "Vranoviče", "Jožef Pečaver", "bajtarjeva hiša [~]", ".", "Hlabost [~ Slabost]", ".", "Gegor Čerar [~]", "z26-starost-'.'-PIKA (vrsta-v-VLM-1.-branjem-brez-starosti — diag-rešena!)"))
ent.append(E(27, 27, "17", 123, "Maj", "25", "27", "Žemelj [~ VLM-'Kamelo']", "Marija Muc", "omožena ž.-gospodinja [~ VLM-'gumflabinja']", "23 let", "Pljučnica", "1", "Jos. Rumpf [~]", "★ z27-'Marija-MUC' — MUC-vez-P173-h91!"))
ent.append(E(28, 28, "2", 123, "Maj", "30", "31", "Gradac", "Terezija Novak", "½ romfalova hiša [~]", "2 leti", "Pljučnica", "1", "Gegor Čerar [~]", None))
ent.append(E(29, 29, "21", 123, "Junij", "3", "5", "Hrašinec", "Peter Jurajevič", "½ romfalov sin [~]", "46 let", "Srčno kap [~]", ".", "Gegor Čerar [~]", None))
ent.append(E(30, 30, "48", 123, "Junij", "13", "14", "Gradac", "Janez Marentič", "bajtarjev sin", "2 dni", "Prirojena slabost", ".", "Gegor Čerar [~]", None))
ent.append(E(31, 31, "19", 123, "Junij", "14", "15", "Hrasinec", "Ana Vržan [~ KRIŽAN-mreža!]", "¼ gospodinja hiša [~ VLM-'gumflava']", "12 let", "Jetika", "1", "Gegor Čerar [~]", None))
ent.append(E(32, 32, "18", 123, "Julij", "1", "3", "Griblje", "Peter ŠIMEC [★★★ max-zoom-'Šimec'-karon-nad-S + ŠIMEC-vez-P173!]", "samoski hlapec [~ 'samostanski hlapec'? — cf.-X-Notarica-leksikon]", "64 let", "Pljučnica", "1", "Gregor Cerar [~ VLM-'Gegor']", "★★★ VLM-'Lincet'-ZAVRJEN! + h18 = 7. mrliški vpis (1890 + 1903-×2 + 1905-×2 + 1906 + 1909!)"))
ent.append(E(33, 33, "24", 123, "Julij", "2", "4", "Vranoviče", "Ana Haraja [~]", "¼ romfaltova hiša [~]", "6 let", "Želodčni tafar [~]", "1", "Gega Čerar [~ VLM-raw]", None))
ent.append(E(34, 34, "34", 123, "Julij", "3", "4", "Hrasinec", "Frančišek Urhovec", "¼ umfakar sin [~ vrškar?]", "¼ ure [~ NAJKRAJŠA-STAROST-LINIJE!]", "Prirojena slabost", ".", "Gegor Čerar [~]", None))
# ——— s124 (str. 123): zap35–46 ———
ent.append(E(35, 35, "53", 124, "Julij", "26", "28", "Gradac", "Marija Marenčič", "½ zemljakova hiša [~]", "3 mesece", "Mladosť [~ Slabost]", ".", "Gregor Cerar", None))
ent.append(E(36, 36, "57", 124, "Julij", "30", "1. avg.", "Gradac", "Marija Marenčič", "¼ vrškar hiša [~ VLM-'umf']", "4 let", "Prehladjenje [~]", ".", "Gregor Cerar. 07. 1909. [~ VLM-dodatek]", None))
ent.append(E(37, 37, "27", 124, "Avgust", "7", "9", "Pilovje", "Janez Černič", "oženjen ¼ zemljak", "63 let", "Želodčni katar [~ katarr]", "1.", "Jos. Vouk [~ VLM-raw — cf.-RAUQ-lekcija-z11-'Punc']", None))
ent.append(E(38, 38, "10", 124, "Avgust", "19", "21", "Gradac", "Francisk Jakša [~ Frančišek]", "bajtarski sin [~ VLM-'hajtajež']", "5 let", "Zastrupljenje [~]", ".", "Lavfin Bitmar [~ →Bitnar]", None))
ent.append(E(39, 39, "21", 124, "Avgust", "20", "21", "Hrašinec", "Josefa Juračevič", "½ zemljakova hiša [~]", "9 mesecev", "Gliste", ".", "Lavfin Bitmar [~ →Bitnar]", None))
ent.append(E(40, 40, "33", 124, "September", "5", "7", "Goriče", "Marija Papič", "samotna ½ gosp. hiša [~ VLM-'gemf']", "36 let", "Vodenica [~]", ".", "Jos. Vouk [~]", None))
ent.append(E(41, 41, "16", 124, "September", "11", "13", "Orehoviše [~ Obrhoviče?]", "Peter Jakobčič", "¼ zemljakov sin", "36 let", "Herić [~ jetika?]", ".", "Lavfin Bitmar [~]", None))
ent.append(E(42, 42, "22", 124, "September", "17", "19", "Boršt", "Marija Hvalj [~ HRALJ-vez-P174-z74!]", "½ zemljakov sin [~ stan-ANOMALIJA?-v-VLM]", "2 meseca", "Jedka [~ Jetika]", ".", "Jos. Vouk [~]", None))
ent.append(E(43, 43, "24", 124, "September", "17", "19", "Otok [~ VLM-'Ofork']", "Neža Dajnar", "mlinarjeva hiša [~]", "6 tednov", "Mladosť [~]", ".", "Jos. Vouk [~]", None))
ent.append(E(44, 44, "85", 124, "September", "26", "28", "Griblje", "Jožef PEZDIREC [★★★ max-zoom-z-DESCENDER-@3.-črka — ISTA-forma-kot-1908-z25-h85!]", "¼ zemljakov sin", "2 dni", "Slabost [★★ crop-korekcija — VLM-'Mladosť']", ".", "Lausin Bitnar [~ — NOVI-DUHOVNIK-#16 (1.-podpis!); VLM-'Lavfin-Bitmar']", "★★★ h85-vez-1908/09 (1908-Jožef-VSLED-TEŽKEGA-PORODA + 1909-Jožef-2-dni = 2-otroka-v-2-letih-ISTA-hiša!) + h85 = 3. mrliški vpis"))
ent.append(E(45, 45, "25", 124, "November", "10", "10", "Gradac", "F. Juračevič", "¼ zemljakov sin [~ VLM-'zemljakovod']", "- [MRTVOROJEN]", "Mrtvorojen [~ VLM-'Mrlovožen']", ".", "—", "★★ MRTVOROJEN-#2 (starost-'-' + BREZ-podpisa — r53-vzorec-#19! + VLM-VRSTA-IZPUŠČENA-diag-REŠENA — vrsta-bila-izpuščena-v-VLM-1.-branjem!)"))
ent.append(E(46, 46, "14", 124, "November", "23", "25", "Boršt", "Matija Hvalj [~ Hralj?]", "vdovec in vrškar [~ VLM-'mrtikar']", "84 let", "Mladosť [~]", "1.", "Jos. Vouk [~]", None))
# ——— s125 (str. 124): zap47–55 ———
ent.append(E(47, 47, "18", 125, "November", "30", "1. dec.", "Žumberk", "Barbara Juvančič", "vdova hiši [~]", "1 leto", "Slabost", ".", "Jos. Umek [~]", None))
ent.append(E(48, 48, "62", 125, "December", "1", "3", "Gradac", "Ana Staričar [~]", "vdova, vdovica [~]", "66 let", "Nadutost [~ Naduha]", ".", "Lavtin Bitenc [~ →Bitnar]", None))
ent.append(E(49, 49, "33", 125, "December", "1", "3", "Griblje", "Marija DEBLIČ [~ max-zoom-'Deblič' — cf.-P166-1899-Matija-DEBLIČ-h33 + P118-1888-'Dehlič?'-vez!]", "vdova vrškarica", "70 let [★★ diag-'76'-ZAVRJENO — max-zoom-'70'-jasno!]", "Narust", "1", "Lausin Bitnar [~]", "★★ diag-'76'→70-KOREKCIJA (cropi-×3.0-zlati-standard!) + P168-lead-'Dehlič?-h33'-NASLOV-KONSISTENTEN + h33 = 6. mrliški vpis + DEBLIČ-vez-×3 (1899 + 1902 + 1909!)"))
ent.append(E(50, 50, "13", 125, "December", "2", "3", "Griblje", "Marija JAKOBIČ [~ max-zoom-'Jakobič/Jakobšič' — h13-CLUSTER (1886-Jakobuč + 1887-Jakofčič + 1888-Jakobčič)!]", "omožena ½ gosp. gospodinja [~ 'gospodinjstva'?]", "59 let", "Naduha", "1", "Lausin Bitnar [~]", "~ h13-CLUSTER-vez + TRI-VIRSKA-h13-nadaljevanje (1885-poročna + 1886/1887/1888 + 1909 = 5. leto!) + h13 = 4. mrliški vpis"))
ent.append(E(51, 51, "47", 125, "December", "5", "7", "Bošt [~ Boršt?]", "Matija Jaklič [~ cf.-z16-'Jakše'-ISTA-Jak-glyph-forma!]", "oženjen sin", "23 let", "Jetika", "1", "Jos. Umek [~]", None))
ent.append(E(52, 52, "86", 125, "December", "7", "8", "Griblje", "Marija KRIŽAN [~ max-zoom-ISTA-forma-kot-z25-h29! cf.-h36-1882-mreža!]", "omožena ¼ gosp. gospodinja", "57 let", "Pljučnica", "1", "Lausin Bitnar [~]", "★★★ h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (korpus-04455-1910 + 04105-1912/1913/1918 — VSE-KASNEJE! = 31.-PT-kandidat; p80-92-NESPREMENJENO — h86-ŽE-v-filtru!) + ★★ VLM-'Mišma'-ZAVRJENO→KRIŽAN + diag-hišna-'26'→86-KOREKCIJA!"))
ent.append(E(53, 53, "25", 125, "December", "7", "8", "Obravice [~ Obrh?]", "Anton Pleč", "½ gosp. očetov sin [~ VLM-'oče sin']", "11 let", "Jetika", "1", "Jos. Umek [~]", None))
ent.append(E(54, 54, "5", 125, "December", "11", "12", "Hrastovice", "Štefan Pavčič", "gospodar ¼ gosp. žen [~]", "74 let [~ VLM-'50'-diag-vez-z55]", "Slabost", ".", "Lavtin Bitenc [~]", "~ starost-[~] — cf.-diag-lekcija-z55 (cropi-×3.0)"))
ent.append(E(55, 55, "2", 125, "December", "27", "29", "Gradac", "Janez Novak", "oženjen ½ gosp. rat. [~ VLM-'fat.']", "50 let [★★ diag-'58'→50-KOREKCIJA!]", "Jetika", "1", "Jos. Umek [~]", "★★ diag-'58'→50-KOREKCIJA (cropi-×3.0-zlati-standard!)"))

assert len(ent) == 55, len(ent)
grib = [e for e in ent if e["vas"].startswith("Griblje")]
assert len(grib) == 11, len(grib)
assert [e["zap"] for e in grib] == [11, 16, 17, 21, 22, 25, 32, 44, 49, 50, 52]
assert sorted(int(e["houseNo"]) for e in grib) == [2, 13, 15, 18, 29, 33, 34, 34, 43, 85, 86]

dokaz = {
    "status": "SAMPLE-TRANSCRIPTION-D1909",
    "generated": "P175",
    "phase": "P175 — mrliška 1909 (23. → 24. polno leto mrliške linije)",
    "source": "matricula-online.eu 04894, skeni 121–125 (1909-zap1–55; s121-dno = P174-meja-reuse!) + meja-1909/10 = s126 (P176-lead)",
    "frame": {
        "leto": 1909,
        "vrstic": 55,
        "zap_oštevilčenih": 55,
        "neštevilčenih": 0,
        "vpisi": 55,
        "dup_zaporedna": None,
        "griblje_vpisi": 11,
        "hise": 10,
        "hise_seznam": "2,13,15,18,29,33,34,34,43,85,86",
        "ponovitve": "34",
        "meja_1908_09": "s121-dno (velika-'1909.'-INSIDE-band2-prazne-vrste + PIKA + restart 76→1 = 16. POTRDITEV — P174-koda!)",
        "meja_1909_10": "s126 (glava-'Leto 18 1910' + restart-55→1-BREZ-velikega-separatorja = NOV-PODVZOREC-7.-STIL-familija-brez-velike-glave-1.×! P174-lead-'[~ s125+?]' POTRJEN-→-s126)",
        "glave_napake": [
            "s121-'Leto 18 1908' (meja-stran — stran-začeta-v-1908, separator-1909-NA-DNU!)",
            "s122–s125-'Leto 18 1909' = '185309'-PREDPONSKA-'18'-navada-×4-UNIVERZALNO — 0-EKZOTIČNIH (kontrast-1907-rekord-5!)",
            "s126-'Leto 18 1910' (1910-prva-stran — P176-scope!)"
        ],
        "stran_invarianta": "stran == sken − 1 (s121–s125 == str. 120–124 — 96.–100. potrditev VIZUALNO-diag)"
    },
    "entries": ent,
    "excluded": [
        {"id": "X1", "opis": "s126–s127 (1910-scope: glava-'Leto 18 1910' + restart-55→1 + zap1–24 — 5-GRIBLJE-ŽE-vidnih: z3-Mihael-PEZDIREC?-h14-72 + z9-Marjeta-h49-66 + z10-h74-'Marija-Hanžič?'[~] + z13-Marija-Vötter?-h4-40 + z23-Alojzij-Kralj-h35-25-dni!) — P176-lead!"}
    ],
    "anomalies": [
        {"id": "A1", "opis": "★★★ z3-Peter-Stublar-92-let = IZENAČENJE-REKORDA-LINIJE (1889-P155-92!) — 2.×-92-v-liniji (s121-zap3 — Petrovišče-h4-vdovec-'ožigkar'[~]!)"},
        {"id": "A2", "opis": "★★★ z21/z22-h34-ŠILAK-DVOJČKI (Matija-½-dne + Nikolaj-2-dni — P174-lead-100%-POTRJEN; VLM-'Tlak'-×2-ZAVRJEN — max-zoom-karon-nad-S!) — h34-×2-v-1909-1.-del + PADEC-vzorec-6.-leto"},
        {"id": "A3", "opis": "★★★ P174-KOREKCIJA-'PERDINEC'→PEZDIREC-×3 (1908-z25-h85 + z70-h20 + z71-h30 — max-zoom-z-DESCENDER-@3.-črka — ista-forma-kot-1909-z44! + h20-1892/1906-PEZDIREC-hiša-ne-menja-priimka-v-2-letih + P163-leksikon-vez-'Perdivec'/'Perdinec'→PEZDIREC-×3 + poročna-1908-v17-'Dorothea-PEZDIREC-h14'!) — parish.ts-3-bloki-korigirani"},
        {"id": "A4", "opis": "★★★ z44-h85-Jožef-PEZDIREC-2-dni = h85-vez-1908/09 (1908-porodna-smrt + 1909-dojenček = 2-otroka-v-2-letih-ISTA-hiša!) — VLM-'Perdinec'/'Mladosť'-ZAVRJENA"},
        {"id": "A5", "opis": "★★ z52-h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (korpus-04455-1910 + 04105-1912/1913/1918 — VSE-KASNEJE!) = 31.-PT-kandidat; p80 92-NESPREMENJENO (h86-ŽE-v-p80-prek-04455-1910-poročna-P139!) — VLM-'Mišma'-ZAVRJENO + diag-hišna-'26'→86!"},
        {"id": "A6", "opis": "★★ MRTVOROJENI-×2-nad-Griblji (z7-s121-'Mrtvorojena'-starost-'.'-podpis-'——' + z45-s124-'Mrtvorojen'-starost-'-'-BREZ-podpisa + VLM-VRSTA-IZPUŠČENA-diag-REŠENA!) — r53-vzorec-#18–#19"},
        {"id": "A7", "opis": "★★ z10-PISAR-KOREKCIJA: smrt-'22'-nad-prečrtanim-'24' (1. številčna-korekcija-v-vrstici-linije — pisar-sam-korigiral!)"},
        {"id": "A8", "opis": "★ z6-bolezen-'Mrtvoud-[?]' = X-ANOMALIJA (63-let + pokop-3-dni — NI-mrtvorojen! P174-lead-'z6/z7-MRTVOROD-×2'-POL-KOREKCIJA — samo-z7-jest!)"},
        {"id": "A9", "opis": "★★ NOVI-DUHOVNIK-#16-'Lausin-Bitnar-[~]' (×5-Griblje-z44/z49/z50/z52 + s124/z38/z39/z41-skeni; VLM-'Lavfin-Bitmar'/'Lavtin-Bitenc'-2-forme — max-zoom-podpis-B-i-t-n-a-r!)"},
        {"id": "A10", "opis": "★★ VLM-korekcije-imen-×8 (z11-'Toma'→TOME + z16-'Jakše'→JAKOFČIČ[~] + z17-'Lovšic'→LAŠIČ[~] + z21/z22-'Tlak'→ŠILAK-×2 + z25-'Vržan'→KRIŽAN[~] + z32-'Lincet'→ŠIMEC + z44-'Perdinec'→PEZDIREC + z52-'Mišma'→KRIŽAN[~]-h86-ne-26!)"},
        {"id": "A11", "opis": "★★ diag-korekcije-×3 (z49-starost-'76'→70 + z55-starost-'58'→50 + z52-hišna-'26'→86 = cropi-×3.0-zlati-standard!)"},
        {"id": "A12", "opis": "★ z17-h43-Marija-LAŠIČ-64-let = P174-LEAD-'84'-KOREKCIJA (KURRENT-6 = samo-spodnja-zanka — 8-bi-imel-DVE!) + hiša-'43'-jasno-ne-13 + z26-starost-'.'-PIKA + z27-'Marija-MUC'-h17 (MUC-vez-P173-h91!)"}
    ],
    "crossChecks": [
        {"id": "C1", "opis": "zap-kontinuiteta: 55-oštevilčenih == 55-VPISOV — ČISTA-SEKVENCA-zap1–55 (5.-čisto-leto! 0-predorov/0-duplikatov/0-neštevilčenih!)"},
        {"id": "C2", "opis": "stran == sken − 1: s121–s125 == str. 120–124 (96.–100. potrditev VIZUALNO-diag!)"},
        {"id": "C3", "opis": "glave-konzistenca: s121-'Leto 18 1908' (meja-stran!) + s122–s125-'Leto 18 1909' + s126-'Leto 18 1910' — '18'-navada-0-EKZOTIČNIH"},
        {"id": "C4", "opis": "hišna-konzistenca: dokaz-11-Griblje-vpisov == parish.ts-11-blokov-1:1 (hiše 2,13,15,18,29,33,34,34,43,85,86 — h34-×2-DVOJČKI!)"},
        {"id": "C5", "opis": "P174-KOREKCIJA-leksikon-vez: 'Perdivec'/'Perdinec'→PEZDIREC (P163-leksikon + h20-1892/1906 + poročna-1908-v17-Dorothea-PEZDIREC-h14 + 1909-z44-max-zoom!)"}
    ],
    "honesty": [
        "rows-v3-FAIL-lekcija-4.-leto (diag-grid-fiksni-recept-ponovno-vzpostavljen — 7/7-skenov-diag-prebranih!)",
        "VLM-mesec/ime-številne-napake (z11-'Jož.-Punc'→RAUQ + z17-'84'→64 + 'komuflarij'→zemljakinja + z44-'Mladosť'→Slabost — vse-korigirano-z-cropi-×2.2/×3.0)",
        "'Lausin-Bitnar-[~]' = konservativna-lekcija (VLM-2-forme-'Lavfin-Bitmar'/'Lavtin-Bitenc' — max-zoom-podpis-preberi-'Bitnar' — status-[~] OHRANJEN!)",
        "JAKOFČIČ/JAKOBIČ-[~]-nejasnost (h15-z16-'Jakfjič' + h13-z50-'Jakobič/Jakobšič' — h13-cluster-leksikon-vez, status-[~] OHRANJEN)",
        "KRIŽAN-[~]-×2 (z25-h29 + z52-h86 — isti-glyph-2-Mariji-v-1-letu! VLM-'Vržan'/'Mišma' — status-[~] OHRANJEN)",
        "s126-meja-BREZ-velikega-separatorja = 7.-STIL-1.× (glava-'Leto 18 1910' edini-marker + restart-55→1-vizualno — VLM-meseci-raw-'Novemba'/'Decembe'-ohranjeni)",
        "P176-lead-KONSERVATIVNO (z3-'Mihael-PEZDIREC?' + z10-'Marija-Hanžič?'[~VLM-'Vambič'] + z13-'Vötter?' — vse-kandidati-[~]-do-P176-forenzične-verifikacije!)"
    ],
    "nextSteps": [
        {"korak": "P176-lead", "opis": "mrliška 1910: s126-zap1–12 ŽE-prebrani (3-GRIBLJE: z3-Mihael-PEZDIREC?-h14-72-'Mrko-najden'[~] + z9-Marjeta-h49-66 + z10-h74-'Marija-Hanžič?'[~-VLM-'Vambič']!) + s127-zap13–24-ŽE-prebrani (2-GRIBLJE: z13-Marija-Vötter?-h4-40-'Altersschwäche'-NEMŠČINA! + z23-Alojzij-Kralj-h35-25-dni!); meja 1910/11 [~ s131+?]"}
    ]
}

out = "research/issue17/parish-death-1909.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(dokaz, f, ensure_ascii=False, indent=1)
print("WROTE", out, "entries:", len(dokaz["entries"]), "griblje:", len(grib))
