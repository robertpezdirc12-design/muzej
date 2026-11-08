#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P218 — dokaz parish-death-1859-04106.json (103 entries: 23-Griblje + 80-druge!)."""
import json
from collections import defaultdict

TMP = "/tmp/p218"
E = json.load(open(f"{TMP}/entries_1859.json"))
entries = E["entries"]
grib = E["griblje_entries"]

hise = sorted({e.get("hisna") for e in grib}, key=lambda x: int(x))
hise_map = defaultdict(list)
for e in grib:
    hise_map[e.get("hisna")].append(e["z"])

# otroci Griblje 1859 (≤5 let): z6(1J) + z19(10mj) + z24(2tedna) + z31(1mj) + z35(Leg.Kind-—) + z53(3mj) + z65(5J) + z94(14-DNI) = 8
OTROCI_Z = [6, 19, 24, 31, 35, 53, 65, 94]
otrostenje = f"{len(OTROCI_Z)}/{len(grib)} = {round(100*len(OTROCI_Z)/len(grib))}%"

meseci_g = defaultdict(int)
for e in grib:
    m = str(e.get("mesec", "")).split()[0]
    meseci_g[{"Januar": "J", "Februar": "F", "Mai": "M", "Maj": "M", "Oktober": "O", "November": "N", "December": "D"}.get(m, m)] += 1

proof = {
    "faza": "P218",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1859 = 27/29 (issue #18)",
    "knjiga": "04106 (matricula-online.eu — župnija Podzemelj, mrliška 1857–1885)",
    "okvir": {
        "skeni": "s011–s019 (9 svežih 2×-md5-NEODVISNA-PRENOSA — SANDBOX-RESET-REGENERACIJA: veriga-md5-RESTART; vsebinska-križ-tail-s17–s19-vs-P217-dokumentacija!)",
        "pag": "6–13 (pag = sken − 5)",
        "meja_1858_59": "s11 (★★★ NASLOVNI-LIST-'Sterb-Buch.'-DEEL-2-NOVI-TISKANI-STOLPCI (Religion/Ledig/Verheirath/Verwittwet/Geschlecht-ločeno!) + '1858'-tail-glava-KROP-POTRJENA (arb_s11_meja: glyph-analiza-1-8-5-8-BREZ-'9'!) + tail-54–57 (4-vrstice-1858: Zemelj + Krasinec-×2 + Gradac — 0-GRIBLJE!) + DVOJNA-debela-ČRTA + VSOTNA-'1 8 [5 9]'-RAZPETE-CIFRE (P214-TIP-2.-INSTANCE! — '1 8'-KROP-JASNO + '5'-rob-delno + '9'-izven-rezine-[~]!) + restart-z1–z7-BREZ-Ločne-'1859'-glave — MARKER = VSOTNA!) = 56.-POTRDITEV-invariante!",
        "meja_1859_60": "s20 ('1860'-rokopisna-glava-KROP-POTRJENA — VLM-'1800'-misread-KOREKCIJA! + restart-z1–z13 — P217!) = 55.-POTRDITEV!",
        "s19_naslovni_list": "★★★ 'Sterb-Buch.'-PONOVLJEN (s19 = nov-quire-naslovni-list!) + Dec-1859-nadaljevanje-93–103-BREZ-restarta (duhovnik-piše-ČEZ-natisnjeni-naslov!) — LUKNJA-92!",
        "vrstna_aritmetika": "7+12+14+11+12(+1-NEŠTEVILČENA!)+12+12+12+11 = 103 (kronološko!; written-1–91-ČISTO + 93–103 = 102-written + 1-NEŠTEVILČENA-s15-r12-Jalkič — ŠTEVJE-IZ-VRSTIC-20.×!)",
    },
    "statistika": {
        "vpisov_1859": len(entries),
        "griblje_vpisov": len(grib),
        "griblje_hise": len(hise_map),
        "griblje_hise_seznam": hise,
        "griblje_hise_ponovitve": {k: v for k, v in hise_map.items() if len(v) > 1},
        "meseci_griblje": dict(meseci_g),
        "meseci_vsi": E["statistika"]["meseci"],
        "otroška_umrljivost": otrostenje,
        "otroci_z": OTROCI_Z,
        "ekstremi": "99J[~83!]-TRAJNI-DUEL (z81-Posdiac-h52!) ← → 14-DNI (z94-Padierž[?]-h49!) — razpon 14-DNI→99J!",
    },
    "anomalije": [
        {"id": "luknja-92", "opis": "★★★ LUKNJA-92 (NOV-TIP-ANOMALIJE!): s18-konča-written-91 (KROP-2.×!) → s19-začne-written-93 (KROP-'93-pravilna'!) — duhovnik-PRESKOČIL-92-ob-prehodu-na-naslovni-list! (cf. 1860-WRITTEN-DUP-53–59 — RAZLIČNA-anomalija-TIPA!)"},
        {"id": "nestevilcena-jalkic", "opis": "★★★ NEŠTEVILČENA-VRSTICA (NOV-TIP!): s15-r12-'Mafflina(?)-Jalkič-Ceroviše/Vranoviče-h6-6-mj-Wunden-Aug-11/13-Joh.-Knavs' — duhovnik-je-skočil-55→56 (r12-BREZ-ordinala!; page-VLM-'56'-margin = [~]-nezaupanja-vredno) — kronološko-#56!"},
        {"id": "naslovni-list-×2", "opis": "★★★ NASLOVNI-LIST-×2-v-1859: s11 (DEEL-2-začetek — NOVI-TISKANI-STOLPCI: Religion/Ledig/Verheirath/Verwittwet/Geschlecht-ločeno — STAREJŠA-knjiga-format-sprememba!) + s19 (nov-quire!) — duhovnik-piše-VPISE-ČEZ-natisnjene-naslovne-strani! + ordinali-s11-pri-x<0.02 (izven-standardnega-stolpca!)"},
        {"id": "p217-tail-korekcije", "opis": "★★★ P217-TAIL-MISREADI-KOREKCIJE (s19-nikoli-KROP'd-v-P217!): MARGINALI: z95→z94 + z100→z97 (KROP-stolpec-93–103-ČISTO + '93-pravilna'!) + z94: 'Jožef-Petek'→'Josmat[?]-Padierž[?]' (TRI-DUEL-X-open!) + '16-J'→'14-DNI' (PAS+VLM-2:1-vs-13-KROP-row! — ENOTE-DNI!) + 'Hauswinskrabn'→'Naussumsfinkrahn[?]' + z97: 'Valentin-Brino'→'⅄onalfur[?Valentin?]-Brince[~]' (TRI-DUEL-X-open!) + z73-ime-KLARA-potrjena (KROP-row-'Klana'-vs-fresh-'Elena'!) + z76-ime-TRI ('Marlfannina[?]'/'Katharina'/'Paulmann') + z86-ime-DUEL ('Anastasia'[P217+KROP-glyph]-vs-'Katharina'[fresh])!"},
        {"id": "genickstarre-epidemija", "opis": "★★★ GENICKSTARRE-EPIDEMIJA-×4 (NOV-VZROK-v-korpusu!): z24 (Anton-Graes-h65-2-tedna-Apr-16) + z25 (Anna-Keržan-h57-63J-Apr-19) + z31 (Georg-Trnovec-h5-1-mj-Mai-14) + z32 (Ana-Križič-h19-40J-Mai-21) — 4-smrti-v-5-tednih (Apr-16→Mai-21)! — meningitis-klaster (2-otroka + 2-odrasla!)"},
        {"id": "nov-duhovnik-knavs", "opis": "★★★ NOV-DUHOVNIK: 'Joh.-Knavs' (Johannes/Janez-Knavs!) — podpisi-×7-JASNIH (z5/z6/z73/z80/z86/z94/z97) + 1-DUEL (z76-'J.-Halo[?]'!) + Jalkič-vrstica-duhovnik-polje! — cf. Knavs-DRUŽINA-h52 (1880s-'Stillgeborenes-Kind-der-Äublas-Markl.-Knavs'!) — duhovnik-in-družina-ISTA-PRIIMKA-X-open! (prej: Dovgan/Glibe/Romej-1887 + Jančar-1878!)"},
        {"id": "paric-fraisen-klaster", "opis": "★★★ z5+z6-PARIČ-FRAISEN-KLASTER-×2-ISTA-DATA (Jän-27/29!): z5-Marija-Parič-Vranoviče-h15-10-tednov + z6-Marko[?]-Parič-GRIBLJE-h69-1J — 2-otroka-ista-družina-hipoteza-ČEZ-VASI (Fraisin-epidemija-Jänner!) + h69-NIT (P155-1889-h69-Brinec-Janez-16-DNI!)"},
        {"id": "z81-trajni-duel-99-83", "opis": "★★★ z81-STAROST-TRAJNI-DUEL-X-open: 99-J[VLM-fresh+KROP-row-2×!]-vs-83-J[P217-KROP!] — Andrej/Andreas/Johann[?]-Posdiac[~Pestik/Pesdire/Pestiric-TRI!]-h52-Ablaber-Okt-24/26 — NAJSTAREJŠI-1859! (PEZDIRC-MREŽA: 'Posdiac/Pesdire'≈Pezdirc-grafije!)"},
        {"id": "meseci-juni-0-griblje", "opis": "★ MESeci-GRIBLJE-1859: Juni-×0 (EDINA-luknja!) + August-×6-MAX-klaster (z52+z53+z57+z61+z64+z65!) + J-1-F-1-M-2-A-2-M-4-J3-1-A2-6-S-1-O-2-N-1-D-2"},
        {"id": "marktsfreibn-×2", "opis": "★ VZROK-PARALELA-×2: 'Marktsfreibn[~Marbmil?]'-z57 (Hrič-h19-28J-Aug-14) + z65 (Miličk-h29-5J-Aug-28) — 14-dni-apart (garble-×2-ISTA-formulacija! — Marbmil-hipoteza)"},
    ],
    "hišne_kontinuitete": [
        "★★★ h65-×2-1859 (z24-Anton-Graes-von-Griblje-2-tedna-Genickstarre + z97-'⅄onalfur[?Valentin?]'-Brince-58J-Magenkrampf!) — h65 = P155-1889-MILEK-hiša (Barbara-13-DNI!) — 3-obdobja!",
        "★★★ h52-×2-1859 (z46-Anton-Peterle-47J + z81-Posdiac-99J[~83!]!) — h52 = Knavs-DRUŽINA-hiša (1880s!) + P153-1887-h53-Šimec-62 — sosedska-nit!",
        "★★★ h19-×2-1859 (z32-Ana-Križič-40J + z57-Antončina-Hrič-28J!) — KRIŽIČ/HRIČ-2-branji-iste-hiše (X-open!) — h19 = ŽUNIČ-hiša (P211-1866-dvojčki-Žunič!)",
        "★★★ h21-×2-1859 (z9-Korencij-Pirczl-80J + z86-Anastasia[?]-Požekh-69J!) — h21-že-P217-tail ('h21'-z86)!",
        "★★★ h39-×2-1859 (z19-Rudolfina-Stähler-10-mj + z52-Anton-Simic-54J-ŠIMEC-grafia!)",
        "★★★ h5-×2-1859 (z31-Georg-Trnovec-1-mj + z53-Gregor-Strucelj-3-mj!) — h5 = P215-1862-FILAK-hiša (Nicolaus-'Kind-von-ANNA-FILAK'!) — FILAK-nit-globlje!",
        "★★★ h58-NIT-1-LETO-PRED-POŽEKOM (1859-z35-'A.-Stracina'-Leg.Kind-— + 1860-z27-Barbara-Požek-8-mes!) + POŽEK-MREŽA-1859: h21 (z86-Požekh) + h58 (z35) — 2-hiši!",
        "★★★ h57-NIT-2-LETA (1859-z25-Anna-Keržan-63J-Weberstochter → 1860-z69/z70-VALENTIN-×2-h57!)",
        "★★★ h26-NIT (1859-z34-Anna-Kure-80J-Lastnica → 1861-P216-MALEŠIČ-h26-NOVA-z30-Mathias-59J!)",
        "★★★ h69-NIT (1859-z6-Marko[?]-Parič-1J → P155-1889-h69-Janez-Brinec-16-DNI — 30-letna-nit!)",
        "★★★ h33-NIT (1859-z61-Matthias-Ulasič-VOJAK-44J → 1863-P214-FILAK-Grem-h33-×2-v-3-tednih!)",
        "★ h37-DUEL-NIT (1859-z16-'37[~17!]' → 1865-P212-HUSIČ-h37-½-Güblerswirt!)",
        "★ h24-NIT (1859-z76-Milich[?]-24J → 1860-P217-z61-Brenc[~Brinar?]-h24-23J!)",
        "★ h20-NIT (1859-z73-Klara[?]-Podire-23J — P217-tail-'h20[~10!]'-sedaj-1:1-KROP-potrjeno-h20!)",
        "★★★ NOVE-HIŠE-korpusa-1859: h69 + h26 + h29 (Miličk-5J!) + h33 + h49 (Padierž[?]-14-DNI!) + h74 (Barbara-Brenc-76J!) + h20 + h57-že-1860... — korpus-100→107-hiš-X-open!",
    ],
    "crossChecks": [
        "2×-NEODVISNA-PRENOSA-9/9-md5 (s011–s019-fresh — SANDBOX-RESET-REGENERACIJA: veriga-RESTART; vsebinska-križ-tail-vs-P217: z73/z76/z81/z86-1:1-vas/hiša/starost/vzrok!)",
        "zap-chain-1859: s11-restart-1–7 → s12-8–19 (KROP-ČISTO!) → s13-20–33 (KROP!) → s14-34–44 (bracket-KROP!) → s15-45–55 (KROP-'55-pravilna'!) → [NEŠTEVILČENA-r12!] → s16-56–67 (KROP!) → s17-68–79 (KROP!) → s18-80–91 (KROP-2.×-P217!) → s19-93–103 (KROP-'93-pravilna'! LUKNJA-92!) — ŠTEVJE-IZ-VRSTIC-20.×-EXAKT-103!",
        "tail-križ-P217: z73-h20-23J-Sep30/Okt1-Lungenentzündung-1:1 + z76-h24-24J-Okt10/12-Magenkrampf-1:1 + z81-h52-Okt24/26-Altersschwäche-1:1 + z86-h21-69J-Nov13/15-1:1 — 4/6-tail-GRIBLJE-1:1-VSEBINSKO (ime-dueli-dokumentirani!) + 2/6-KOREKCIJE (z94/z97-MARGINALI+IME+STAROST+VZROK!)",
        "arb_s11_meja-KROP: '1858'-tail-glava-POTRJENA (glyph-1-8-5-8-BREZ-'9'!) + VSOTNA-'1 8'-KROP-JASNO + '5'-rob = 56.-POTRDITEV (P214-TIP-2.-INSTANCE!)",
        "arb_s11_vsota_glava-KROP: vsotna-vrsta-'1 8'-JASNO-v-ime-stolpcu + ordinali-s11-pri-x<0.02 (z1–z7-vidni!) + z1-'Jänner-5./7.-Vranoviče-h9-Marianna-Hudak-¼-Güblers[?]'",
        "z6_s11_grib2-KROP: z6-'Griblje-h69-Marko[?]-Parič-1J-Jän-27/29-Fraisin-Joh.-Knavs' + z5-'Maria-Parič-Vranoviče'-PARIČ-KLASTER!",
        "z94/z97_s19_grib-KROP + PAS-×2: h49-'Josmat[?]-Padierž[?]-½-Säugl[?]-14-DNI-Naussumsfinkrahn[?]' + h65-'⅄onalfur[?]-Brince-58J-Magenkrampf' + podpis-'J.-Knavs'-×2-JASNO!",
        "z81/z86_s18_grib-KROP: z80-'October-1859'-glava-JASNO + 'Joh.-Knavs'-podpis + z86-'Griblje-21-JASNO-Snlfannina[?]-Požek-Abloverin-69J-Nov-13/15'!",
        "z73/z76_s17_grib-KROP: z73-'Griblje-20-JASNO-Klana[?]-Resdire-23-Langenfinft' + z76-'Griblje-24-JASNO-Marlfannina[?]-Milich-24-Magenkrampf'!",
        "s19_glava-KROP: 'Sterb-Buch.'-natisnjen-DVOJNI-naslovni-list-POTRJEN (fraktur!) — rokopisna-'1859'-izven-rezine-[~] (page-VLM!)",
        "VIZUALNA-verifikacija-skenov-s011–s019 (direktni-vpogled-×8: arb_s11_meja + arb_s11_vsota + z6_grib2 + z73 + z76 + z81 + z86 + z94 + z97 + PAS-×4!)",
        "vrstna-aritmetika-7+12+14+11+12(+1!)+12+12+12+11 = 103-EXAKT (kronološko!)",
    ],
    "honesty": [
        "z6-ime-DUEL-X-open (Marko[~VLM]/Marlfaud[?KROP]-Parič[~Pašč?]) + stan-GARBLE-X-open + hisna-'69 [~89?]'-X-open",
        "z9-bolezen-GARBLE-X-open ('Gallensteine[~]' — nemško-v-slovenski-knjigi-X-open!) + stan-2-del-garble ('Dragos[?]')",
        "z16-ime-TRI-GARBLE-X-open + hisna-DUEL (37[2×]/17[KROP]!) + starost-[?]",
        "z19-ime-[~] + stan-[?] + starost-[~]",
        "z24-ime-[~] + starost-[~]",
        "z25-ime-DUEL (Keržan/Križan!) + starost-[~]",
        "z31-ime-DUEL (Trnovec/Struchl!)",
        "z32-ime-DUEL (Križič/Kerc!) + 'von-Griblce[?]'-oznaka + stan-[?]",
        "z34-hisna-'26 [~]'-X-open + stan-[~]",
        "z35-ime-X-open ('A.-Stracina-iz-željk[?]-Leg.Kind') + starost-PRAZNA-('—')",
        "z46-stan-GARBLE ('mlad-Koleđal[?]-X-open!)",
        "z52-bolezen-GARBLE ('Gicht...[?]')",
        "z53-ime-[~] + stan-GARBLE ('infulat-Bond[?]-X-open') + bolezen-[~]",
        "z57-ime-[~] + stan-garble + 'Griblč.-Ponik[?]'-X-open",
        "z61-bolezen-2-vrstični-garble ('Harnblutungsfieber[~]-bena[?]')",
        "z64-stan-GARBLE ('dečka-Brenczova-besittng-benin[?]-X-open!)",
        "z65-ime-[~] + stan-garble ('Gößl.-Aschlän[?]')",
        "z73-ime-DUEL-X-open (Klara[KROP-2×]/Elena[VLM!]!) + priimek-TRI (Podire/Pardire/Pezdire!) + stan-[~]",
        "z76-ime-TRI-DUEL-X-open (Marlfannina[?KROP]/Katharina[VLM]/Paulmann[P217]!) + priimek-TRI (Milich/Mihle/Miklik!) + podpis-DUEL ('J.-Halo[?]')",
        "z81-ime-TRI-DUEL-X-open (Andrej/Andreas/Johann!) + priimek-TRI (Posdiac/Pestik/Pesdire!) + starost-TRAJNI-DUEL (99/83!)",
        "z86-ime-DUEL-X-open (Anastasia[P217+KROP-glyph]/Katharina[VLM]!) + priimek-[~Poček]",
        "z94-ime-TRI-DUEL-X-open (Josmat[?]/Josip/Jožef!) + priimek-X-open (Padierž[?]/Podleber/Petek!) + starost-TRI-DUEL (14-DNI-2:1/13/16-J-FALSIFICIRAN!) + bolezen-GARBLE ('Naussumsfinkrahn[?]')",
        "z97-ime-TRI-DUEL-X-open (⅄onalfur[?]/Valentin/Ana!) + priimek-TRI (Brince/Brino/'Kruška-Bina'!) + stan-DUEL-X-open ('Janezfarain[?]'-vs-'Inočfrau-vdova')",
        "s11-ordinali-54–57-tail-[~] (stolpec-izven-standardnega-x!) + VSOTNA-'5-9'-delno-izven-rezine + s19-rokopisna-'1859'-glava-[~] (izven-KROP-rezine!)",
        "VLM-margin-misreadi: page-VLM-'20'/'56'-na-s12-r13/s15-r12 (halucinacija/NEŠTEVILČENA!) + s16-'1857'-glava-'1859'-KOREKCIJA-[~]!",
    ],
    "kaskada": {
        "vitals": "1609 → 1632 (+23 blokov 1859)",
        "04106": "390 → 413",
        "yearset": "+1859 (04106-predzgodovina-27/29!)",
        "meja_1858_59": "s11-naslovni-list-DEEL-2 + '1858'-tail-glava-KROP + VSOTNA-'1 8 [5 9]'-marker (56.-POTRDITEV!) + restart-z1–z7",
    },
    "lead": {"P219": "1858 — s11-tail-ŽE-VLM (54–57: 4-vrstice-1858 + vsotna + '1858'-glava-KROP!) → probe-s004–s011! (1858 = PREDZGODOVINA-28/29; tail-1858: Zemelj-h22[?]-Antonija-Brodarič-10-tednov + Krasinec-h7-Gregor-Brodarič-63J + Krasinec-h16-Jožef-Hoenigman-16 + Gradac-h36-Martin-Plut-29J — 0-GRIBLJE-tail!)"},
    "entries_count": len(entries),
    "griblje_count": len(grib),
    "tail_1858": {
        "vir": "s11-r1–r4 (tail-1858: Okt-30→Dez-31; '1858'-glava-KROP! + vsotna-'1 8 [5 9]'-marker!)",
        "vrstice_1858_tail": "Zemelj-h22[?]-Antonija-Brodarič-10-tednov-Griža-[~]-Okt-30/Nov-1 + Krasinec-h7-Gregor-Brodarič-63J-Nov-20/22 + Krasinec-h16-Jožef-Hoenigman-'¼-Güblersjhn[?]'-16-Dez-11/13 + Gradac-h36-Martin-Plut-'Dzelambra[?]'-29J-Dez-29/31 — 0-GRIBLJE-tail!",
        "stevilo": 4,
    },
    "notes": [
        "★★★ DEEL-2-FORMAT-SPREMEMBA: s11-naslovni-list-nove-knjige (deel-2!) z NOVIMI-TISKANIMI-STOLPCI (Religion-kath/akath + Ledig/Verheirath/Verwittwet + Geschlecht-männl/weibl-ločeno + Alter + Krankheit + Versehen + ärztlich!) — STAR-FORMAT-04106-končan!",
        "★★★ LUKNJA-92 + NEŠTEVILČENA-Jalkič = 2-NOVI-TIPA-ANOMALIJ-ordinalov (za-WRITTEN-DUP-1860!)",
        "★★★ GENICKSTARRE ×4 = 1. EPIDEMIJA-z-ENO-VZROKA-v-predzgodovini (meningitis! Apr-16→Mai-21!)",
        "★★★ Joh.-Knavs = NOV-DUHOVNIK-1859 (podpisi-×7+) — Knavs-družina-h52-X-open-vez!",
        "★★★ P217-tail-NEKDAJ-ne-KROP'd → P218-KROP-korekcije-×5 (z73/z76/z81/z86-ime-dueli + z94/z97-marginali-ime-starost-vzrok!)",
        "SANDBOX-RESET-REGENERACIJA: /tmp-pobrisan → vse-fresh (2×-md5-9/9) + repo-sinhroniziran-iz-GitHub-@-P217!",
    ],
    "entries": entries,
    "griblje_entries": grib,
}
json.dump(proof, open("research/issue17/parish-death-1859-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: research/issue17/parish-death-1859-04106.json ({len(entries)} entries / {len(grib)} Griblje / {len(hise_map)} hiš)")
print("ponovitve:", {k: v for k, v in hise_map.items() if len(v) > 1})
