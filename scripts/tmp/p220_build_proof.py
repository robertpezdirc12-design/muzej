#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P220 — dokaz parish-death-1857-04106.json (73 kronoloških: 10-Griblje + 63-druge!)."""
import json
from collections import defaultdict

TMP = "/tmp/p220"
E = json.load(open(f"{TMP}/entries_1857.json"))
entries = E["entries"]
grib = E["griblje_entries"]

hise = sorted({e.get("hisna") for e in grib if str(e.get("hisna", "")).startswith(tuple("0123456789"))}, key=lambda x: int(x))
hise_map = defaultdict(list)
for e in grib:
    hise_map[e.get("hisna")].append(e["z"])

# otroci Griblje 1857 (≤ ~2 let): z45 (1J) + z56 (3-tedne) + z61 (1J) + z71 (14-let-vs-1-mj-1-dan-DUEL!)
OTROCI_Z = [45, 56, 61]
otrostenje = f"{len(OTROCI_Z)}/{len(grib)} = {round(100*len(OTROCI_Z)/len(grib))}% (+z71-age-DUEL-X-open: 1-mj-1-dan[hi-krop!] → do-40%!)"

meseci_g = defaultdict(int)
for e in grib:
    m = str(e.get("mesec", "")).split()[0]
    meseci_g[{"Februar": "F", "April": "A", "Juni": "J2", "July": "J3", "August": "A2",
              "September": "S", "October": "O", "Jänner": "J", "December": "D", "Mai": "M2"}.get(m, m)] += 1

proof = {
    "faza": "P220",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1857 = 29/29 (issue #18) — ZADNJE leto knjige — PREDZGODOVINSKA LINIJA KONČANA!",
    "knjiga": "04106 (matricula-online.eu — župnija Podzemelj, mrliška 1857–1885 — knjiga-SE-ZAČNE-1857!)",
    "okvir": {
        "skeni": "s001–s007 (7 svežih 2×-md5-NEODVISNA-PRENOSA-7/7 — SANDI-REZET-RESTART-protokol!; s001 = NASLOVNI-LIST-'Tom. III'-'Sterb-Buch'-'Podzemelj' — 0-vrstic!)",
        "okno_1857": "s002–s007 (6 skenov: KNJIGA-START + celo leto + TAIL-1857!)",
        "pag": "sken − 1 = SVINČNIK-FOLIACIJA-ARHIVARJA (dokumentirano-3×: s4='3'-page-VLM + s5='4'-page-VLM + s7='6'-P219-KROP!) — ★ KONVENCIJSKI-PREHOD: KORPUS-sken−5-NEMOŽEN-za-s1–s5 (negativne-strani!) — prehod-dokumentiran!",
        "knjiga_start": "★★★ KNJIGA-04106-SE-ZAČNE-1857: s1-NASLOVNI-LIST ('Tom. III'-rokopisno + 'Sterb-Buch'-velika-Kurrent + 'Podzemelj'!) + s2-RAZPRTA-NASLOVNA-LISTA ('Sterb-'/'Buch.'-fraktura!) + '18 57'-RAZPETA-letnica-glava (rokopisna-nadčrtana — P214-TIP-sorodna-razpeta-cifra!) + restart-z1 — BREZ-taila-1856 (kje-se-konča-1856? X-open — prejšnja-knjiga-signatura-neznana!)",
        "meja_1856_57": "NE-OBSTAJA-v-04106 (knjiga-se-začne-1857!) — '18 57'-glava = KNJIGA-START-marker (ne-MEJA!)",
        "meja_1857_58": "s7 (P219-potrjeno + re-križ-P220-arb_s7_meja-1:1: TAIL-z73–z74 + DVOJNA-ČRTA + VSOTNA-'1 8 5 [8]'-RAZPETE-P214-TIP-3.-INSTANCE ('1-8'-jasno + '5'-v-starostnem-stolpcu-vidno-tudi-v-P220-kropu!) + rokopisna-'Jänner-1858'-glava + restart-z1–z11 + NEŠTEVILČENA-zadnja!) = 59.-POTRDITEV-invariante!",
        "luknja_32": "★★★ LUKNJA-32 (pisarski-preskok — 3.-instance-v-knjigi-po-LUKNJA-92-1859!): s3-ordinalni-stolpec-KONČA-z-31 (15-ordinalov-17–31!) + s3-dno-RAZPRAZNO (y0.925–1.0-brez-vsebine — 3-kropi: s3_dno_z32-prazno + s3_pas_dno + s3_zadnji_dve!) + s4-ZAČNE-z-33 (Juni-21./23.!); kronološki-seam-z31-Juni-21/22 → z33-Juni-21/23-GLADAK! — X-open: morda-32-obrezan-na-dnu-s3 (tabela-se-konča-na-scan-rob — navpične-linije-do-roba!)",
        "vrstna_aritmetika": "16+15+13+13+14+2 = 73 (kronološko; WRITTEN-1–31 + 33–74 = 73-ČISTO — 1-LUKNJA-32!); meseci J4+F8+M5+A5+M7+J3+J6+A18+S8+O0!!+N5[?4]+D4[?5] (z70-'30.-December'-vs-'November-30./December-1.'-duel!)",
        "oktober_luknja": "★★★ OKTOBER-1857-×0 (celotna-župnija!): z65-Sep-24/26 → z66-Nov-9/11 — 15-dnevna-luknja-brez-vpisa — edini-mesec-×0-v-1857 (November-glava-2×-križ: page + t3_s6-trak!)",
        "scarlatina_klaster": "★★★ SCARLATINA?-EPIDEMIJA-klaster: 'Rušfieber/Rušenfleck'-×6–7 (z36-July-24 → z46-Aug-12!) + 'Amigdilitis[?]'-garble-×7 (s5: z48–z57!) — isti-garble-družina?-2.-val?-X-open (šrlaha/rdečinka-hipoteza!) — 13–14-vpisov-v-6-tednih — 1-GRIBLJE-v-klasterju (z45-Rušfieber-Aug-11!)",
    },
    "statistika": {
        "vpisov_1857_kronolosko": len(entries),
        "vpisov_written": 73,
        "luknij": 1,
        "griblje_vpisov": len(grib),
        "griblje_hise": len(hise_map),
        "griblje_hise_seznam": hise,
        "griblje_hise_ponovitve": {k: v for k, v in hise_map.items() if len(v) > 1},
        "griblje_hise_neberljive": ["[?] (z71 — NEBERLJIVA-3×: page+pas-krop+hi-krop!)"],
        "prvi_vpisi_his_v_korpusu": "★★★ 8-od-10-hiš-dobi-s-1857-PRVI-vpis-v-celotnem-korpusu (h13! h31! h36! h48! h52! h60?/66-DUEL! h64! h65!) — ker-je-1857-1.-leto-knjige-04106!",
        "meseci_griblje": dict(meseci_g),
        "meseci_vsi": E["statistika"]["meseci"],
        "otroška_umrljivost": otrostenje,
        "otroci_z": OTROCI_Z,
        "ekstremi": "3-tedne (z56-Urih[?]-h31!) ← → 73-J (z74-Križan[?]-h36-TAIL!) — razpon-3-tedne-→-73-J!",
        "duhovniki": "Ladergal-garble-klaster-DOMINANTA ('Ladinegal/Ladregal/Ladugal/Kadnegal/Kadungal/Ludegal[?]' — 1-pisar-8-variant!) + 'Joann-Skubic-Pav.' (s6 + z50-'Šhubič[?]'!) + 'Johann-Verbič-cooperator' (z71!) + 'Fr.-Xaveryal[?]' (z4-garble) + 'Thom.-Ladargal-Cop.[?]' (z58) + ★★★ 'J.-Knauš/Kranz[?]' (z74-TAIL — MOŽEN-ZGODNJI-Knavs-podpis — KOREKCIJA-P219-lead: Knavs-morda-ŽE-DEC-1857 — X-open!)",
    },
    "anomalije": [
        {"id": "luknja-32", "opis": "★★★ LUKNJA-32 (pisarski-preskok — 3.-instance-v-knjigi-po-LUKNJA-92-1859!): s3-ordinalni-stolpec-konča-z-31 (15-ordinalov!) + s3-dno-RAZPRAZNO (3-kropi!) + s4-začne-z-33; seam-z31-Juni-21/22 → z33-Juni-21/23-GLADAK — X-open: morda-32-obrezan (scan-rob)!"},
        {"id": "knjiga-start-1857", "opis": "★★★ KNJIGA-START: s1-NASLOVNI-LIST ('Tom. III' + 'Sterb-Buch' + 'Podzemelj') + s2-'18 57'-RAZPETA-letnica-glava (rokopisna-nadčrtana!) + restart-z1 — 1857 = 1.-leto-knjige-04106 — MEJA-1856/57-NE-OBSTAJA!"},
        {"id": "oktober-luknja", "opis": "★★★ OKTOBER-1857-×0-v-celotni-župniji (z65-Sep-24/26 → z66-Nov-9/11 — 15-dni!) — edini-mesec-×0-v-1857."},
        {"id": "scarlatina-klaster", "opis": "★★★ SCARLATINA?-klaster: 'Rušfieber/Rušenfleck'-×6–7 (July-24→Aug-12) + 'Amigdilitis[?]'-garble-×7 (s5) — 13–14-vpisov-v-6-tednih — 2.-val?-X-open — 1-GRIBLJE (z45!)."},
        {"id": "h36-krizan-×2", "opis": "★★★ h36-KRIŽAN-×2-v-1857: z50-Georg/Jurij-Križan[?]-4J (Križan-2×-križ-vs-Krajncan-page-DUEL!) + z74-Marijan-Križan[?]-73J-TAIL (4×-garble!) — KRIŽAN-hiša-2-GENERACIJI-v-1-letu! (cf.-P219-tail-dokumentacija!)"},
        {"id": "z71-hisa-neberljiva-starost-duel", "opis": "★★★ z71: hiša-NEBERLJIVA-3× (page+pas-krop+hi-krop — edini-primer-1857!) + STAROST-DUEL (14-let[page]-vs-1-mesec-1-dan[hi-krop]! — dojenček-hipoteza: Wasserkopf + 'ganz-außerehelich' (NEZAKONSKI!) — X-open!) + ime-duel (Martin-vs-Max!) + TRI-stan-garble."},
        {"id": "z58-honesty-max", "opis": "★ z58-honesty-max-vrstica-1857: hiša-TRI-DUEL (48[page]/43[?]/145[2×-križ!]!) + ime-TRI-DUEL (Stamcar[page]/Straus[2×!]!/Maria[hi]!) + starost-DUEL (66-let-vs-Kind[?]!) + bolezen-garble."},
        {"id": "popravki-pisarja-×2", "opis": "★ 2-POPRAVKI-PISARJA-v-1857: s3-'1867'-prečrtano→1857 (ob-vrsti-30/31!) + s4-z33-'1858'-prečrtano→1857 (začetek-vpisa!) — pisar-začenjal-z-napačno-letnico-2×!"},
        {"id": "s4-desna-stran-quiri", "opis": "★ s4-DESNA-stran-prikazuje-'December'-vrstice-X-open (t4_s4-trak!) — morda-drugi-del-knjige/quiri-ali-druga-sekcija — NE-vpliva-na-1857-linijo (z45-križ-3×-kljub-temu!)."},
    ],
    "hišne_kontinuitete": [
        {"h": "13", "nit": "★★★ 1857-z45-Marija-Dragos-1J-Rušfieber = PRVI-vpis-h13-v-korpusu! (ime-DRAGOŠ-družina! cf. P193-h3-DRAGOŠ-1864!) → 04106-1860/66/67/68/69/71/73/81/82/84/85 + 04894/04105/04455-mreža-×25!"},
        {"h": "31", "nit": "1857-z56-Ana-Urih-3-tedne = PRVI-vpis-h31! → 04106-1875/81/85 + 04894/04455/04105-mreža-×28!"},
        {"h": "36", "nit": "★★★ 1857-×2 (z50-Georg/Jurij-Križan-4J + z74-Marijan-Križan-73J!) = PRVI-vpisi-h36! KRIŽAN-hiša! → 04106-1868/74/83 + 04455-1882 + 04894/04105-mreža-×24!"},
        {"h": "48", "nit": "1857-z58-Anna-Stamcar/Straus[?]-66J = PRVI-vpis-h48! → 04106-1861/66/67/70/74/78/81 + 04894/04105/04455-mreža-×26!"},
        {"h": "52", "nit": "1857-z10-Jožef-Peskar[?]-46J = PRVI-vpis-h52! (P218-z81-'Posdiac[?]'-h52-99J-TRAJNI-DUEL + Knavs-družina-h52-1880s!) → 04106-1859/70/76 + mreža!"},
        {"h": "60", "nit": "1857-z4-Lazar[?]-66J (h60-or-66-DUEL!) = potencialni-PRVI-vpis-h60 (TOMINC-nit: P219-z37-Jakob-Tomcsinič-h60-1858 → 1881-Katharina-TOMINC!) — X-open-hiša-duel!"},
        {"h": "64", "nit": "1857-z5-Matija-Verbičar-68J = PRVI-vpis-h64! → 04106-1874/76/84 + 04894/04455/04105-mreža-×11!"},
        {"h": "65", "nit": "1857-z61-Georg-Mulik[?]-1J = PRVI-vpis-h65-MILEK-hiša! (1858-z39-'Keržan[?]' → 1859-×2 → MILEK-mreža-04894-×9 + 04105-×13 — MILEK-3-obdobja!)"},
    ],
    "crossChecks": [
        "2×-NEODVISNA-PRENOSA-7/7-md5 (s001–s007-fresh — SANDI-REZET-RESTART-protokol-P219!)",
        "zap-chain-1857: s2-z1–z16 (page + 4-traki-križ: t1-1–3/t2-4–8/t3-9–12/t4-13–16!) → s3-z17–z31 (page + traki + zap-stolpec-15-ordinalov!) → [LUKNJA-32!] → s4-z33–z45 (page + P219-lead-križ-1:1!) → s5-z46–z58 (page + P219-lead-križ-1:1!) → s6-z59–z72 (page + P219-lead-križ-1:1!) → s7-tail-z73–z74 (page + arb_s7_meja + krop + P219-dokumentacija!) = 73-ČISTO!",
        "LUKNJA-32-KRIŽ-×4: s3-zap-stolpec (15-ordinalov!) + s3_dno_z32-krop (PRAZNO!) + s3_pas_dno/s3_zadnji_dve (zadnja-vrstica-z31!) + s4-z33-start + kronološki-seam (Juni-21/22 → Juni-21/23-GLADAK!) = 5-križev!",
        "KNJIGA-START-KRIŽ: s1-'Tom. III'-'Sterb-Buch'-'Podzemelj' (page) + s2-'18 57'-razpeta-glava (arb_s2_start-KROP + page-MEJA!) + restart-z1 (arb_s2_start: z1-Jänner-1./3.-h30 + z2!) = 3-križi!",
        "MEJA-1857/58-RE-KRIŽ-P219: arb_s7_meja-P220-KROP-1:1-struktura (tail-2-vrstice + VSOTNA-'1 8'+5 + 'Jänner-1858'-glava + restart!) = P219-dokumentacija-POTRJENA = 59.-POTRDITEV!",
        "GRIBLJE-TRIANGULACIJA-×10: vsaka-vrstica-2–4-vira (page-VLM + traki + krop-VLM + hi-zoom) — z4 (3!) + z5 (4!) + z10 (3!) + z45 (3!) + z50 (3!) + z56 (3!) + z58 (3!) + z61 (2!) + z71 (3!) + z74 (4!)",
        "z50-KRIŽAN-KOREKCIJA: page-'Krajncan'-vs-KRIŽAN-2× (krop + trak 'Georg-Križan'!) — Križan-preferenca + h36-križ-z74-Križan = KRIŽAN-hiša-potrjena!",
        "kronološki-seam-s3→s4: z31-Juni-21/22 → [LUKNJA-32] → z33-Juni-21/23 — GLADAK (brez-razpoka!) = LUKNJA-32-dokaz!",
    ],
    "honesty": [
        "z4-ime-TRI-DUEL-X-open (Lazar/Luka-Rebernik/Peter-Pečenko!) + hiša-DUEL (60-vs-66!) + bolezen-garble ('Koli[?]'!)",
        "z5-starost-DUEL (68-vs-65!) + priimek-4-varianti (Verbičar/Verbiezer/Veberkar/Veibeshar!)",
        "z10-ime-TRI-DUEL-X-open (Peskar/Bedric/Petrič!) + starost-DUEL (46-vs-40!) + bolezen-garble ('Alfersvess[?]'!) + zavihek-lista-krije-del-vrstice!",
        "z45-spol-DUEL (Marija-2×-vs-Martin-1×!) + hiša-DUEL (13-vs-12!) + stan-garble ('½-Zibl-Šajna-Šajara[?]')",
        "z50-ime-DUEL (Križan-2×-vs-Krajncan-1×!) + bolezen-garble ('Hirzentzündung[?]'!)",
        "z56-hiša-TRI-DUEL (31/51/57!) + stan-garble + bolezen-'Amigdilitis[?]'-garble",
        "z58-honesty-MAX: hiša-TRI-DUEL (48/43/145!) + ime-TRI-DUEL (Stamcar/Straus/Maria!) + starost-DUEL (66-vs-Kind!)",
        "z61-priimek-TRI-garble (Mulik/Mililkh/Gobik-Mulek!) + starost-[~]",
        "z71-hiša-NEBERLJIVA-3× + starost-DUEL (14-let-vs-1-mj-1-dan!) + ime-duel (Martin-vs-Max!) + TRI-stan-garble + NEZAKONSKI-kandidat!",
        "z74-priimek-4×-garble (Križan/Kunezl/Krisan-Kristjan/Danelfa-Vrizan!) + stan-TRI-duel (vdovec/Ehelmann/Eheleut!) + duhovnik-garble ('Knauš/Kranz[?]'!)",
        "z70-datum-DUEL ('30.-December'[page]-vs-'November-30./December-1.'[kronologija]!) — meseci-N/D-±1",
        "z31-datum-DUEL ('2./4.'[page]-vs-'21./22.'[2×-krop!]!) — kronološko-21/22-preferenca",
        "s4-desna-stran-'December'-vrstice-X-open (quiri/del-knjige?) — dokumentirano, NE-vpliva-na-linijo!",
        "'Amigdilitis'-garble-×7-X-open (sodobna-diagnoza?-VLM-interpretacija — morda-Rušfieber-družina!)",
        "duhovniki-1857: 'Ladergal'-garble-klaster (8-variant!) + Skubic + Verbič + Xaveryal[?] + Knavs/Kranz[?]-z74 — vsi-[?]/[~]-označeni!",
        "pag-KONVENCIJSKI-PREHOD: sken−1 (svinčnik-foliacija!) za-P220 — sken−5-NEMOŽEN-za-s1–s5 — dokumentirano!",
    ],
    "kaskada": {
        "insert": "10-GRIBLJE-blokov-parish.ts (pred-P219-sekcijo; scan: s2–s7; pag = sken−1-svinčnik-foliacija-dokumentirana!)",
        "sanitizacija": "qa-p220 + števci 1642→1870 + 04106 423→433 + yearset-+1857 + guard-1857 (04106-SET-KOMPLETEN-1857–1885!) + verifierji-patched + pt-luknja-433/1870 + krstne-izjeme-(po-runQA!)",
        "verifikacija": "verifier-p220-I1–I10 + runQA-220/220 + tsc-0 + lint-0 + REGRESIJA-p190–p219 + p80",
    },
    "lead": "PREDZGODOVINA-LINIJA-04106-KONČANA (29/29-let!) — knjiga-04106-POPOLNOTA-prepisana (1857–1885 = 29-let, 433-Griblje-vpisov!) → P221-LEAD: krstna-04104-PREDZGODOVINA (1871–1885, 15-let — ×200-skenov-čaka! P196-worklog-lead!) — pričakovani-start: 1885 (1/15) po-descending-vzorca-mrliške-predzgodovine; s-proba-potreben!",
    "entries_count": len(entries),
    "griblje_count": len(grib),
    "tail_1857": "s7-z73–z74 (2-vrstici — P219-dokumentirano + 3-fresh-križi!)",
    "notes": "P220 = 29/29-let-predzgodovine — ZADNJE-leto-knjige-04106 → PREDZGODOVINSKA-LINIJA-KONČANA! Naslednja-faza: krstna-04104 (1871–1885).",
    "entries": entries,
    "griblje_entries": grib,
}
json.dump(proof, open("/home/z/my-project/research/issue17/parish-death-1857-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: {len(entries)} entries / {len(grib)} griblje / {len(hise_map)} hiš")
print("otroška umrljivost:", otrostenje)
