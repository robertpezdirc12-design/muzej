#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P221 — dokaz parish-baptism-1885-04104.json (krstna PREDZGODOVINA 1/15!)."""
import json

TMP = "/tmp/p221"
E = json.load(open(f"{TMP}/entries_1885.json"))

grib = E["griblje_entries"]
anomalije = [
    {"id": "meja-1884-85-s186",
     "opis": "★★★ MEJA-1884/85 = s186 (60.-POTRDITEV-invariante!): TAIL-1884-z111[prečrtano!]-Gradac-68-Maria (†25.9.1885-pripis!) + z112[prečrtano!]-GRIBLJE-h43-Mathias (†28.12.1887-pripis!) + VSOTNA-razpete-'1/8/8/5'-P214-TIP-sorodna + rokopisna-'Jänner'-glava + RESTART-z1-na-DAN-1.-1.-GRIBLJE-h21! + 1884 = 112-vpisov (s185-ordinali-103–110!)",
     "dokazi": ["s186-page-VLM", "s186-zap-stolpec (11[?]-11[?]-prazno-1-2-3-4!)", "arb_s186_meja-krop", "s186_meja_hi-krop"]},
    {"id": "knjiga-konec-04104",
     "opis": "★★★ TAIL-1885 = z103–z104 (Dez-26/30) + BREZ-VSOTNE-vrste + s200 = VEZ-platnica (temno-rjava-usnja!) — 1886-gre-v-NOVO-knjigo-04105 (korpus-ŽE-pokrit-P79!) — KNJIGA-04104-KONČANA-do-konca!",
     "dokazi": ["s199-page-VLM", "arb_s199_tail-krop", "s200-page-VLM (vez!)"]},
    {"id": "dvojcki-gradac-2-vrstici",
     "opis": "★★★ DVOJČKI-GRADAC-×2-2-VRSTICI: z92-Anton-'Na-umrla'-(umrl!) + z93-Jožef-(živ!) — OBA-Dez-14/14-Gradac-5[~]! — page-VLM-SPOJIL-v-1-vrstico ('92') → KOREKCIJA-2-vrstici (zap-stolpec-86–93 + seam-krop-'93' + t4-'94'-marginali!) — PARALELA-P219-DVOJČKI-SIMIC-h19-1858-2-VRSTICI! + pripis-'Umrła-dne-28.4.1965-v-Zagrebu'-MMK-1958/66!",
     "dokazi": ["s197-page-VLM (spoje!)", "s197-zap-stolpec", "seam_s197_bot-krop", "r4_s197_zap_bot_hi", "t4_s197-trak"]},
    {"id": "z101-neidentificirana-vrstica",
     "opis": "★★★ z101 = NEIDENTIFICIRANA-VRSTICA (page-VLM-ZAMUJENA!) — DOKAZ-za-obstoj: POPRAVEK-PISARJA-s199 (z103-'102'-prečr→103 + z104-'103'-prečr→104 = pisar-sprva-pozabil-štet-z101!) + t4-trak-fragment-'oče-Janez-Tomaž-½-gem.' + robni-svinčnik-100/101/102-na-dnu-s198 (revizija!) + r11-mikro-'pravih_vrstic-3'-na-dnu! — X-open: morda-probita/squeezed-vrstica!",
     "dokazi": ["s198-zap-stolpec (94–102 = 9!)", "r11_s198_zap_dno-mikro-8×", "t4_s198-trak-fragment", "s199-popravek-pisarja-krop"]},
    {"id": "popravek-pisarja-s199-×2",
     "opis": "★★★ POPRAVEK-PISARJA-×2: z103-'102'-prečrtano→103 + z104-'103'-prečrtano→104 (THE-SMOKING-GUN-za-z101!) + z102-IME-POPRAVEK (Katharina-prečrtano→Marija!)",
     "dokazi": ["s199-page-VLM", "s199_zap_hi-krop", "r3_z104_s199-krop", "arb_s199_tail-krop"]},
    {"id": "z100-griblje-h1-misread-korekcija",
     "opis": "★★★ page-VLM-'Škrilje-(Strile)'-MISREAD-KOREKCIJA → z100 = Anton-GRIBLJE-h1 (r7-krop-'Gribile-h1'-1:1!) — h1-×2-v-1885 (z33-Mathias-ŽELKO!) — BREZ-te-korekcije-bi-korpus-izgubil-1-GRIBLJE-vpis!",
     "dokazi": ["r7_s198_row7-krop ('108/151-Gribile-1-Anton'!)", "t3_s198-trak ('Hrile-1'-garble!)", "s198-page-VLM ('Škrilje'-napaka!)"]},
    {"id": "naslovna-sredi-letnika-s190",
     "opis": "★★★ s190 = NASLOVNA-GLAVA-SREDI-LETNIKA ('Geburts-und-Tauf-Buch.'-natisnjena-PONOVLJENA! — paralela-mrliška-04106-s9+s10-SREDI-1858-quiri-prelom!) + glava-'18 85'-page-VLM-'1886'-MISREAD-KOREKCIJA (arb_s190_pag-krop-'85'-1:1!)",
     "dokazi": ["s190-page-VLM", "arb_s190_pag-krop"]},
    {"id": "foliacija-pag-sken-plus-13",
     "opis": "pag = sken+13 = FOLIO-SVINČNIK-ARHIVARJA (razprti-dvostranski-list = 1-FOLIO!) — potrjeno-5×-natančno (s185='198'/s190='203'/s193='206'/s196='209'/s199='212'!) + page-VLM-tens-MISREADI-dokumentirani (s185-'148'/s188-'241'/s193-'266'/s195-'268' — 0↔4/6/8-KURRENT-ZMEDA!) — NOVA-KONVENCIJA-za-04104!",
     "dokazi": ["arb_s185_pag", "arb_s188_pag", "arb_s190_pag", "arb_s193_pag", "arb_s195_pag", "arb_s196_pag"]},
    {"id": "ordinalni-dueli-reseni",
     "opis": "Ordinalni-DUELI-rešeni-zap-stolpcem-2:1: s189-page-SHIFT−1 (VLM-'22'→z21! zap-21–28-ČISTO!) + s190-'31'-vs-'30' + s193-z57-'59'-krop-MISREAD (zap-pozicija!) + s196-z78-'98'-krop-MISREAD + z26-'26/27'-trak-vs-page + z28-'28-dup'-page-MISREAD (EN-vpis!) + z102-'101/102'-duel!",
     "dokazi": ["s189-zap-stolpec", "s190-zap-stolpec", "s193-zap-stolpec", "s196-zap-stolpec", "r6/r7/r9-krops"]},
    {"id": "hisa-dueli-tri-quad",
     "opis": "Hišni-DUELI: z59-QUAD-(27/47/37/21!)+ime-TRI-(Marko/Maria/Martin/Martha!)-honesty-MAX-1885! + z78-TRI-(17/29/9/99!) + z26-TRI-(49/17/1[8?]!) + page-VLM-hišne-MISREAD-KOREKCIJE: h6→61 (z14!) + h11-trak-'41' + h45→42 (z30!) + h33→53 (z47!) + h33→35 (z48! — h33-×2-HIPOTEZA-MRTVA!) + h19→17 (z62!) + h39-ep91→23 (z85!) + h37-('z37'-'55/53'-duel!)",
     "dokazi": ["r3_hisna-krops", "z14/z15/z30/z47/z48/z62/z85-krops", "traki-60"]},
    {"id": "krstni-pripisi-kriz-mrlisko",
     "opis": "★★★ POZNEJŠI-PRIPISI-na-krstnih-vpisih = KRIŽ-z-mrliško-04106 (NOVA-VERIFIKACIJSKA-DIMENZIJA!): z1-Mathias-h21-'†7.9.1887' + z5-Martin-h[?]-'gest.-12.[?]1888' + 1884-tail-z111-'†25.9.1885' + z112-'†28.12.1887' + z80-Johann-Grem-'†30.9.99' + z86-'Umrła-28.4.1965-Zagreb'-MMK + s197-modri-pripisi-×5!",
     "dokazi": ["traki + kropi (pripisi!)", "X-open-križ-z-04106-korpusom (P153-1887/P193-1888!)"]},
    {"id": "mezecni-quirk-s187",
     "opis": "MESEČNI-QUIRK-s187: z9-Feber-5-nato-z10–z12-Januar-12/14/15 (pisarjeva-rahljanje-ali-VLM-misread — X-open!) + s193-kronološki-preskok (z57-Aug-2-vs-z58-Jul-31/3!)",
     "dokazi": ["s187-page-VLM", "s193-page-VLM"]},
]

cross_checks = [
    {"tip": "meja-1884/85-re-križ", "opis": "s186-VSOTNA + restart-z1 (arb_s186_meja + s186_meja_hi) — 60.-POTRDITEV-invariante (59.-P220!)", "status": "POTRJENO"},
    {"tip": "1884-tail-griblje", "opis": "z112-h43-Mathias-†28.12.1887-pripis → 04106-1887-korpus-X-open + z105-h62-Johann-oče-Kure-½ (s185-tail!)", "status": "KONTEKST (1884-P222!)"},
    {"tip": "krstni-pripisi-†", "opis": "z1-†7.9.1887 + z5-†12.[?]1888 → 04106-P153/P193-leta-X-open", "status": "X-open-KRIŽ"},
    {"tip": "h1-×2 + h55-×2", "opis": "z33-ŽELKO-h1 + z100-Anton-h1; z37-Simec-h55 + z68-Simic-h55 — 2-hiši-×2-v-1885 (SIMIC/ŽELKO-mreži!)", "status": "DOKUMENTIRANO"},
    {"tip": "PEZDIRC-mreža-krstna", "opis": "z47-oče-'Johan-Pegdic' + z85-mati-'Katharina-roj.-Pegdirec' + z63-botra-'Ana-Pezdirc' + z14-botri-'Pezdirec+Ana-Pezdirec' = ×4-v-1885!", "status": "DOKUMENTIRANO"},
    {"tip": "KRIŽAN-botra-tail", "opis": "z104-botra-'Peter-Krijan[Križan!]'-TAIL-1885 → h36/h63-KRIŽAN-niti (P220!)", "status": "DOKUMENTIRANO"},
    {"tip": "POŽEK-nit", "opis": "z14-oče-'Požek-½-Gütl' + z5-botra-'Katharina-Pozek'", "status": "DOKUMENTIRANO"},
    {"tip": "HLEBEC-nit", "opis": "z82-oče-'Peter-Hlebec-¼' → h2-KLEPEC/HLEBEC-nit (P219-1858!)", "status": "DOKUMENTIRANO"},
    {"tip": "URIH-nit", "opis": "z14-h61 → URIH-hiša (P216-z11-Urih-46J + P220-'Ana-Urih'-h31-X-open!)", "status": "DOKUMENTIRANO"},
    {"tip": "FILAK-nit", "opis": "z14-mati-'Fila[k]'-½-Gütl → FILAK-mreža (P215-h61/h5!)", "status": "DOKUMENTIRANO"},
    {"tip": "DRAGOŠ-nit", "opis": "z63-mati-'Ana-roj.-DRAGOŠ' → DRAGOŠ-družina (P193-h3 + P220-z45-h13!)", "status": "DOKUMENTIRANO"},
    {"tip": "ŽELKO-nit", "opis": "z33-oče-'Miklo-Želko-¼'-botri-Želko-×2 → h1-ŽELKO-nit (P215/P216-1862/64!)", "status": "DOKUMENTIRANO"},
]

honesty = [
    "z101 = NEIDENTIFICIRANA-VRSTICA (vas/hisna/otrok/datum-VSI-[?]! — samo-t4-fragment-oče!) — page-VLM-zamujena — obstoj-dokazan-samo-indirektno (popravek-pisarja + robni-svinčnik + r11-mikro)",
    "z59 = honesty-MAX (hiša-QUAD-DUEL-27/47/37/21 + ime-TRI-DUEL-Marko/Maria/Martin/Martha!)",
    "z78 = hiša-TRI-DUEL (17/29/9/99!) — brez-resolucije",
    "z26 = hiša-TRI-DUEL (49/17/1[8?]!)",
    "z37 = hiša-DUEL (55/53!)",
    "z5 = hiša-[?] (~10-krop-X-open!)",
    "ordinal-s197/s198-seam = X-open-DOKUMENTIRAN (dvojčki-SPLIT-model + zap-stolpci + robni-marginali)",
    "mezecni-quirk-s187 (z9-Feber→z10–z12-Januar!) = X-open (pisar-vs-VLM!)",
    "s193-kronološki-preskok (z57-Aug-2-vs-z58-Jul-31!) = X-open",
    "krop-geometrijske-zamike-dokumentirane (pass-1-zgrešeni-→-pass-3-kalibracija!)",
    "page-VLM-tens-MISREADI-foliacije (4-primera!) — korekcija-prek-5×-natančnih-branj",
    "z100-vas-'Škrilje'→'Griblje'-KOREKCIJA = krop-1:1 (page-VLM-napaka-dokumentirana!)",
    "h33-×2-hipoteza-MRTVA (h53+h35! — korekcija-v-sled!)",
    "meseci-?-×3 (z101 + 2-dueli) — honesty-dokumentirano",
    "1884-tail-ordinali-'111/112'-prečrtana-X-open ('31'-krop-misread!)",
    "botra/starši-večkrat-[~] (Kurrent-garble!) — brez-fabriciranja",
]

out = {
    "phase": "P221",
    "title": "Župnija Podzemelj — krstna knjiga 04104 (predzgodovina), polno leto 1885 = 1/15 NOVE LINIJE (issue #18)",
    "type": "parish-baptism-prehistory",
    "status": "DOCUMENTED",
    "issuedAt": "2026-11-06",
    "source": {"book": "04104", "url": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
               "inventar": 200, "okvir": "s185–s199 (15 skenov) + s200-vez", "prenos": "2×-neodvisna-md5-15/15"},
    "method": "2×-neodvisna-prenosa-md5 + page-VLM-×15 + traki-60 + krop-~75 (zap-stolpci-15 + foliacija-6 + meja/tail-4 + Griblje-25 + seam/mikro-×12!) — triangulacija-page+trak+krop",
    "frame": {"scanFrom": 185, "scanTo": 199, "pagKonvencija": "sken+13 = folio-svinčnik (razprti-list = 1-folio!)", "year": 1885,
              "rowsTotal": 104, "break1884/85": "s186 (VSOTNA + restart-z1!)", "bookEnd": "s199-tail + s200-vez!"},
    "okvir": E["okvir"],
    "entries": E["entries"],
    "stats": {**E["statistika"], "griblje_rekord": "★★★ 25-GRIBLJE = NOV-REKORD-PREDZGODOVINE/KORPUSA (prej-23-P218-1859-mrliška!)"},
    "anomalije": anomalije,
    "crossLinks": cross_checks,
    "honesty": honesty,
    "nextSteps": [
        "P222 = krstna-04104-leto-1884 (2/15 descending!) — s185-tail-ŽE-VLM (z105-GRIBLJE-h62-Johann-oče-Kure-½-Gribl! + z106–z110) → MEJA-1883/84-pred-s185 → probe-s178–s185",
        "krstni-pripisi-†-križ-z-04106 (X-open-verifikacija proti P153-1887/P193-1888-korpusu!)",
        "pogojno: h53/h35-page-'h33'-korekcija-vpliva-na-starejše-04105-niti (X-open)",
    ],
}
json.dump(out, open("/home/z/muzej-repo/research/issue17/parish-baptism-1885-04104.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: entries={len(out['entries'])} griblje={len(grib)} anomalije={len(anomalije)} honesty={len(honesty)}")
