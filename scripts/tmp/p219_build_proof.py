#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P219 — dokaz parish-death-1858-04106.json (58 kronoloških: 10-Griblje + 48-druge!)."""
import json
from collections import defaultdict

TMP = "/tmp/p219"
E = json.load(open(f"{TMP}/entries_1858.json"))
entries = E["entries"]
grib = E["griblje_entries"]

hise = sorted({e.get("hisna") for e in grib}, key=lambda x: int(x))
hise_map = defaultdict(list)
for e in grib:
    hise_map[e.get("hisna")].append(e["z"])

# otroci Griblje 1858 (≤ ~2 let): z16 (2-dni) + z17 (½-dni[?]) + z27 (7-mj) + z42 (0[?]/1J-6M) + z47 (8-tednov) = 5
OTROCI_Z = [16, 17, 27, 42, 47]
otrostenje = f"{len(OTROCI_Z)}/{len(grib)} = {round(100*len(OTROCI_Z)/len(grib))}%"

meseci_g = defaultdict(int)
for e in grib:
    m = str(e.get("mesec", "")).split()[0]
    meseci_g[{"Februar": "F", "April": "A", "Juni": "J2", "July": "J3", "August": "A2",
              "September": "S", "October": "O", "Jänner": "J"}.get(m, m)] += 1

proof = {
    "faza": "P219",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1858 = 28/29 (issue #18)",
    "knjiga": "04106 (matricula-online.eu — župnija Podzemelj, mrliška 1857–1885)",
    "okvir": {
        "skeni": "s004–s011 (8 svežih 2×-md5-NEODVISNA-PRENOSA-8/8 — SANDI-REZET-RESTART; s004–s006 = 1857-proba-ŽE-VLM za-P220-lead!)",
        "okno_1858": "s007–s011 (5 skenov: MEJA-1857/58 + restart + celo leto + tail-1858!)",
        "pag": "sken − 5 (KORPUS-KONVENCIJA-P200+!; ★ svinčnikova-foliacija-arhivarja-na-skenih = sken−1: s7='6' s8='7' s9='8' s10='9' s11='10' — DOKUMENTIRANO, konvencija-ostaja-za-skladnost-z-P218-s11=6!)",
        "meja_1857_58": "s7 (★★★ NASLOVNI-LIST-'Sterb-Buch.'-RAZPRTA + TAIL-1857-z73–z74 (2-vrstici: Gradac-'Amalia-Rundel[?]-'86J'[duel-Kunstel-1J-1M-krop!]' + ★ GRIBLJE-h36-'Križan/Krisan/Kristjan[?]-TRI'-73J — 1857-zadnji-Griblje!) + DVOJNA-ČRTA + VSOTNA-'1 8 [5 8]'-RAZPETE-MARKER (P214-TIP-3.-INSTANCE! — '1-8'-KROP-JASNO + '5'-v-Alter-stolpcu!) + rokopisna-'Jänner-1858'-glava-KROP + RESTART-z1–z11 (11!) + ★★★ NEŠTEVILČENA-ZADNJA-VRSTICA (Jan-29/31-Gradac-12-Ivan[?]-Mali-44J — levi-stolpec-PRAZEN-KROP-2.×-POTRJENO! — 2.-instance-v-korpusu-po-P218-s15-Jalkič!) = 57.-POTRDITEV-invariante!)",
        "meja_1858_59": "s11 (P218-potrjeno: tail-54–57 + VSOTNA-'1 8 [5 9]'-marker + restart-1859-z1–z7 — re-križ-P219-arb_s11_meja-1:1-struktura (Zemelj + Krasinec-×2 + Gradac; 0-GRIBLJE!) = 58.-POTRDITEV!)",
        "naslovna_lista_×3": "★★★ s9 + s10 = NASLOVNA-LISTA-'Sterb-Buch.'-RAZPRTE-SREDI-1858 (quiri-prelom-mid-year — paralela-1859-s19!) + s7 — duhovnik-piše-ČEZ-natisnjene-naslove! page-VLM-na-s10-ujel-LE-4/14-vrstic ('30–33'-MISREAD!) → KROP-zap-stolpec-POTRDIL-40–53-ČISTO (glif-viz-1:1!)!",
        "vrstna_aritmetika": "11+1(NEŠTEVILČENA!)+14+14+14+4 = 58 (kronološko!; WRITTEN-1–57-ČISTO-BREZ-luknij — ČISTA-ORDINALNA-LINIJA-2.-leto-zapored! — nasprotje-1859: 103-vpisov-z-LUKNJO-92!)",
    },
    "statistika": {
        "vpisov_1858_kronolosko": len(entries),
        "vpisov_written": 57,
        "nesteviceenih": 1,
        "griblje_vpisov": len(grib),
        "griblje_hise": len(hise_map),
        "griblje_hise_seznam": hise,
        "griblje_hise_ponovitve": {k: v for k, v in hise_map.items() if len(v) > 1},
        "meseci_griblje": dict(meseci_g),
        "meseci_vsi": E["statistika"]["meseci"],
        "otroška_umrljivost": otrostenje,
        "otroci_z": OTROCI_Z,
        "ekstremi": "0[?]-starost-duel (z39-Keržan[?]-h65 + z42-Križan[?]-h3!) ← → 68-J[?]-duel (z52-Padire-h50!) — razpon-0[?]-→-68-J[?]!",
    },
    "anomalije": [
        {"id": "nesteviceena-s7-zadnja", "opis": "★★★ NEŠTEVILČENA-ZADNJA-VRSTICA-s7 (2.-instance-v-korpusu-po-P218-s15-r12-Jalkič!): zadnja-restart-vrstica (Jan-29/31-Gradac-12-Ivan[?]-Mali-44J-Pljučno-vnetje) ima LEVI-STOLPEC-PRAZEN (KROP-s7_zap_tail_kot-2.×-POTRJENO + VLM-krop-soglasje-'PRAZNO (NEŠTEVILČENA)'!) — duhovnik-prišel-do-roba-strani-in-ni-številčil; s8-z12-nadaljeval-z-'12'! → 58-kronoloških-vpisov-oz.-57-written!"},
        {"id": "naslovna-lista-×3-sredi-leta", "opis": "★★★ NASLOVNI-LISTI-'Sterb-Buch.'-×3-v-oknu-s7–s11: s7 (MEJA-1857/58) + s9 (diagonalna-'1858'-glava-KROP-glyph-8-BREZ-repa!) + s10 (quiri-prelom-sredi-1858!) — duhovnik-piše-vpise-ČEZ-natisnjene-naslovne-strani! (paralela-1859: s11-DEEL-2 + s19!) — page-VLM-na-s10-ujel-LE-4/14-vrstic ('30–33'-MISREAD-3/4-ZMEDA!) → KROP-zap-stolpec-glif-viz-1:1-POTRDIL-40–53!"},
        {"id": "dvojcki-simic-h19", "opis": "★★★ DVOJČKI-SIMIC-h19 (z16+z17-ZWILLINGE!): Ana-Simic-2-dni (Feb-21/23) + Mannier[?]-Simic-'zwilling-Genickfand-kind'-½-dni[?] (Feb-21/26[?]) — oba-'Gaufigabrannt[?]'-garble + 'dto.'! — Genickfand[?≈Genickfäule/Genickbrand]-družina = PRE-EHO-1859-GENICKSTARRE-EPIDEMIJE-×4 (P218)! + h19-DRAMA: 3-otroške-smrti-h19-v-1858 (dvojčka + z27-Kurič-7-mj!) → 1859-×2 (Križič-40J + Hrič-28J)!"},
        {"id": "gaufigalbrann-klaster-×4", "opis": "★★★ GAUFIGALBRANN[?]-KLASTER-×4 (Feb-20–26 + Apr-9): z15-Anna-Radine-h49-19J + z16 + z17-dvojčki + z27-Kurič-7-mj-'Fraisin' — isti-garble-vzrok-X-open (Gichterbrand?-hipoteza!) — otroški-klaster-ČEZ-mejo-v-'FRAISEN'-nit (→ 1859-Jän-PARIČ-klaster-×2-P218!)"},
        {"id": "pezdirc-mreza-padire", "opis": "★★★ PEZDIRC-MREŽA-NAJGLABLJE-×4-GENERACIJE: 'Padire'-h50-1858-z52 (Maria[?]/Martin[?]-68-J[?]) → 1868-Johann-Perdirc-h50-5½-J-FRAISEN (P-pred!) → 1872-Barbara-Kerdise-h50-3-ure (PEZDIR-grafia!) → 1924-Matija-PERDIRC-POSESTNIK (04894!) — 4-generacijska-grafija-linija-×4-v-ISTI-HIŠI-h50! (cf. P218-'Posdiac/Pesdire/Pardire/Podire'-z73/z81/z94!)"},
        {"id": "nov-duhovnik-auber-duel", "opis": "★★★ NOV-DUHOVNIK-DUEL: 'J.-Auber[?]/Huber[?]-P.'-podpis (z39-h65-Jun-21 — 4×-zoom-glyph!) — NISMO-Knavs! (vs-Joh.-Knavs-dominanta-×7+ + page-VLM-'Šinkovec[?]'-garble-z26/z28/z30/z31/z39!) — Knavs-je-podpisoval-že-od-Feb-1858 (z15–z17-z27-z37-z42-jasni-1:1!) — P218-'NOV-DUHOVNIK-1859'-KOREKCIJA: Knavs-AKTIVEN-ŽE-1858! + Knavs-grafija-variacije: 'Khubiz/Knavo/Knaff/Kribiz[?]'"},
        {"id": "starost-0-dueli", "opis": "★ STAROST-'0'-×2 (z39-Keržan[?]-h65 + z42-Križan[?]-h3!) — ali-0-dni/stillbirth-oznaka-ali-nezapisano-glyph-X-open! (z42-krop-alt-'1-J-6-M'!)"},
        {"id": "meseci-griblje-1858", "opis": "★ MESeci-GRIBLJE-1858: F3 + A1 + J2(2) + J3-1 + A2-2 + S/O-1 = 10 — LUKNIJE: Januar ×0 + März ×0 + Mai ×0 + November ×0 + Dezember ×0 (5-luknij! vs-1859-samo-Juni-luknja!) + h19-×3-TRIPLE (edina-×3-v-predzgodovini-že!?)"},
    ],
    "hišne_kontinuitete": [
        {"h": "2", "nit": "1858-z47-Margaretha-Fenz-8-tednov → 1864/67-Klepec-×2 → 1871-Klepec → 1873-Hlebec → 1880/81-Klepec/HLEBEC + 04894-HLEBEC-mreža + 04105-Hlebec-krsti"},
        {"h": "3", "nit": "1858-z42-'Križan[?]-Kind' → 1864-DRAGOŠ-Georg → 1865-Maria-Križan → 1866-Štrucelj → 1867-Papic → 1878-kripto-Ana-P → 1882-Dorothea-VRIŽAN + 04894-KRIŽAN-×4-1887–1917 + 04455-PEZDIREC-1907-ženin!"},
        {"h": "19", "nit": "★★★ 1858-×3-TRIPLE (z16/z17-dvojčka-Simic + z27-Kurič-7-mj!) → 1859-×2 (Križič-40J + Hrič-28J) → 1864-Mathias-Simic-65J → 1865-Križe-Anna → 1866-Ginic → 1874-Krič-Catharina + 04894-KRIŽE-×3!"},
        {"h": "44", "nit": "1858-z51-'Strucel[?]-18J' → 1867-Matija-Strucež-1½J → 1872-Bakorić/PRIMEJ → 1873-Barbara-Struzelj → 1876-ARNUETZ → 1878-PECOLAR → 1879-PEGLIC → 1881-HAMBIČ → 1883-HLEBUČAR → 1884-KLOBUČAR + 04894-ŠTRUKELJ/ŠTRUCELJ + 04455-ŠTRUCELJ-×2 + 04105-Štrucelj-krsti-×5!"},
        {"h": "49", "nit": "1858-z15-Anna-'Radine[?]-19J' → 1859-z94-Padierž-14-DNI (P218!) → 1869-Brodarič-3J → 1873-Brodarić-74-dni → 1876-Brodarič-Peter-½J → 1883-Jurij-BRODARIČ → 1884-Matias-BRODARIČ + 04894-BRODARIČ-×5 + 04105-krsti"},
        {"h": "50", "nit": "★★★ 1858-z52-'Padire[?]-68J' → 1860-Petine/Peter[TRI-GARBLE] → 1865-Redovi-Barbara → 1868-Johann-Perdirc-5½-J-FRAISEN → 1872-Kerdise-PEZDIR-3-ure → 1882-PECLIR → 1924-PERDIRC-POSESTNIK — 4-GENERACIJE!"},
        {"h": "60", "nit": "1858-z37-Jakob-Tomcsinič-60J → 1867-Selho-Georg → 1873-Hušič → 1881-Katharina-TOMINC-Müllerjeva-vdova + 04894-ŽELJKO-×7 + 04455 + 04105-krsti-×9"},
        {"h": "65", "nit": "1858-z39-'Keržan[?]' → 1859-×2 (Graes + Brince-58J!) → 1863-Brinc → 1868-Mililc → 1869-×2 → 1871-Mihelič → 1873-×2 → 1881/82/84-MILEK-×3 + 04894-MILEK-×9 + 04455-×4 + 04105-×13 — MILEK-hiša-3-obdobja!"},
    ],
    "crossChecks": [
        "2×-NEODVISNA-PRENOSA-8/8-md5 (s004–s011-fresh — SANDI-REZET-RESTART-protokol-P218!)",
        "zap-chain-1858: s7-restart-1–11 (KROP!) + ★ NEŠTEVILČENA (KROP-2.×-PRAZNO!) → s8-12–25 (KROP-glif-viz!) → s9-26–39 (KROP-glif-viz-1:1!) → s10-40–53 (KROP-glif-viz-1:1 — page-VLM-'30–33'-MISREAD-KOREKCIJA!) → s11-54–57 (P218-KROP + P219-re-križ!) — ČISTA-LINIJA-1–57-BREZ-luknij!",
        "tail-križ-P218-s11: z54–z57-struktura (Zemelj + Krasinec-×2 + Gradac — 0-GRIBLJE!) = P218-okvir-dokumentacija-1:1 + arb_s11_meja-P219-re-križ-soglasje!",
        "arb_s7_meja-KROP: VSOTNA-'1 8 [5 8]'-P214-TIP-3.-INSTANCE ('1-8'-jasno + '5'-Alter-stolpec!) + rokopisna-'Jänner-1858'-glava + tail-1857-2-vrstici (Gradac + GRIBLJE-h36!) = 57.-POTRDITEV!",
        "arb_s9_glava-KROP: diagonalna-'1858'-glava-POTRJENA (glyph-8-dvojni-simetrični-lok-BREZ-repa — NE-9!) = 58.-križ!",
        "s10-page-VLM-MISREAD-KOREKCIJA: page-VLM-ujel-LE-4/14-vrstic ('30–33') → KROP-zap-stolpec-glif-viz-1:1-40–53-ČISTO (t1–t4-traki-križ-delno!) — 3.×-v-knjigi-page-VLM-fail (po-P217-s22 + P216-s23!)",
        "NEŠTEVILČENA-KRIŽ: KROP-s7_zap_tail_kot ('PRAZNO-NEŠTEVILČENA') + VLM-krop-soglasje + s8-zap-stolpec-začne-z-'12' (brez-dupl!) = 3-križi-1:1!",
        "GRIBLJE-TRIANGULACIJA-×10: vsaka-vrstica-3–4-vira (page-VLM + traki + krop-VLM + glif-viz-1:1) — z15/z16/z17/z27/z37/z42-z42/z47/z51/z52!",
    ],
    "honesty": [
        "z15-hisna-DUEL-3× (49[glif-viz]/19[page-VLM]/44[krop-VLM] — KURRENT-1/4/9-ZMEDA!)",
        "z15-bolezen-GAUFIGALBRANN[?]-GARBLE-X-open (Gichterbrand?-hipoteza) + ime-'Radine[?]'",
        "z16-ime-'Somic[?]' + bolezen-garble-X-open",
        "z17-ime-'Mannier[?]'-X-open + starost-'½-dni-vs-dto'-glyph-duel + pokop-duel (26/23/30) + vas/hisna-'dto'-glyph",
        "z27-ime-TRI-DUEL-X-open (Kurič/Kreite/Krix/Petrič!) + stan-garble ('½-Güblers-sohn-vs-Bolnar')",
        "z37-ime-garble ('Tomcsinič[?]/Tomecšinc[?]' + 2-vrstica-'gorn.-Gäbjsfawn[?]')",
        "z39-ime-TRI-DUEL-X-open (Keržan/Kerzmann/Deželak!) + stan-garble ('invalid-½-göblin') + starost-'0[?]-duel' + duhovnik-DUEL (Auber/Šinkovec-garble!)",
        "z42-ime-TRI-DUEL-X-open (Križan/Horvat/Vozan!) + starost-'0[?]-vs-1J-6M'-duel + bolezen-garble",
        "z47-stan-garble ('½-Güblers-tojdan[?]-Tochter!') + starost-duel (8-tednov-vs-8-Mg) + bolezen-'Swajzne[?≈Schwäche]'",
        "z51-ime-spol-DUEL (Anna[2×-viz]-vs-Anton[page-VLM]!) + priimek-duel (Strucel/Strovs) + bolezen-garble",
        "z52-ime-DUEL (Maria[glif+page]-vs-Martin[krop-VLM]!) + priimek-PEZDIRC-grafija-'Padire/Radire'-X-open + starost-duel (68/8/43/87!) + bolezen-'?-fall'-garble + duhovnik-duel (Knavs-vs-Vinaus[?])",
        "s10-vrstice-48-druge: page-VLM-LE-4/14 + ročna-glif-viz-transkripcija + traki-delno — [~]-heavy (honesty-max!)",
        "s9-z26/z28-z36-45: page-VLM-1× + glif-viz-delno — podpisi-garble ('Šinkovec[?]-vs-Knavs-varianti!')",
        "duhovniki-1858: Joh.-Knavs-DOMINANTA (podpisi-jasni-z15/z16/z17/z27/z37/z42-1:1!) + grafija-variacije ('Khubiz/Knavo/Knaff/Kribiz[?]') + 'J.-Auber[?]/Huber[?]-P.'-duel (z39) + 'Šinkovec[?]'-page-garble — KORREKCIJA-P218: Knavs-aktiven-ŽE-Feb-1858!",
        "pag-KONVENCIJA-VS-FOLIACIJA: sken−5-korpus (P200+) vs svinčnik-foliacija-sken−1 (s7='6'...s11='10') — dokumentirano, konvencija-ostaja!",
    ],
    "kaskada": {
        "insert": "10-GRIBLJE-blokov-parish.ts (pred-P218-sekcijo; scan-page: s8→3 s9→4 s10→5 s11→6 = sken−5-konvencija!)",
        "sanitizacija": "qa-p219 + števci 1632→1642 + 04106 413→423 + yearset-+1858 + guard-1858 + verifierji-patched + pt-luknja-423/1642 + krstne-izjeme-(po-runQA!) ",
        "verifikacija": "verifier-p219-I1–I10 + runQA-219/219 + tsc-0 + lint-0 + REGRESIJA-p191–p218",
    },
    "lead": "P220-LEAD: 1857 — s004–s006-ŽE-PRENESNI (2×-md5!) + VLM-ŽE (s004: z33–z45-13-vrstic-Juni–August + s005: z46–z58-13 + s006: z59–z72-14!) → s003-nazaj-proba (1857-začetek — knjiga-04106-SE-ZAČNE-1857: morda-naslovni-listi-s001–s003!) + tail-1857-ŽE-KROP'd (s7-z73–z74: Gradac + ★ GRIBLJE-h36-'Križan/Krisan[?]'-73J — P219-dokumentirano!) + 1857 ≈ 74-vpisov (z1–z74!)",
    "entries_count": len(entries),
    "griblje_count": len(grib),
    "tail_1857": "s7-z73–z74 (2-vrstici — dokumentirano-v-okviru-meja_1857_58!)",
    "notes": "P219 = 28/29-let-predzgodovine; P220 (1857) = ZADNJE-leto-knjige-04106 → KONČAJ-predzgodovinske-linije-29/29!",
    "entries": entries,
    "griblje_entries": grib,
}
json.dump(proof, open("/home/z/my-project/research/issue17/parish-death-1858-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: {len(entries)} entries / {len(grib)} griblje / {len(hise_map)} hiš")
print("otroška umrljivost:", otrostenje)
