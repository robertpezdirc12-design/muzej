#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P200 — build proof JSON: research/issue17/parish-death-1877-04106.json
(zrcaljenje P199-strukture; 60 vpisov / 8 Griblje-proper / 3-'Hrib'[?]-Tomc /
Kogej-obdobje-razširjeno-nazaj / P201-lead!)"""
import json, re
from collections import Counter
from pathlib import Path

RAW = json.load(open("/tmp/p200/entries_1877.json"))
ENT = RAW["entries"]
TAIL76 = RAW["tail_1876"]
OUT = Path("/home/z/my-project/research/issue17/parish-death-1877-04106.json")


def starost_j(mala):
    if not mala:
        return None
    s = str(mala).lower().split("(")[0]
    m = re.search(r"(\d+)", s)
    if not m:
        return None
    n = float(m.group(1))
    if "mesec" in s or "monat" in s:
        return round(n / 12, 3)
    if "teden" in s or "woche" in s:
        return round(n / 52, 3)
    if " dan" in s or "tagn" in s or "tage" in s:
        return round(n / 365, 3)
    if "ura" in s or "minut" in s or "std" in s or "stund" in s:
        return 0.001
    return n


Z_IME = ["maria", "anna", "ana ", "katharina", "catharina", "margaretha", "theresia",
         "elisabeth", "agnes", "barbara", "ursula", "lucia", "johanna", "magdalena",
         "vdova", "hči", "hcer", "dohtar", "chter", "tochter", "žena", "egovina",
         "služkinja", "magd", "-in ", "jarina", "mati", "rosalia", "doroth", "martha", "gutfrau"]
M_IME = ["johannes", "joannes", "johann", "janez", "georg", "joseph", "josef", "jožef",
         "mathias", "matthias", "matevž", "michael", "mich.", "nicolaus", "miklavž",
         "jakob", "peter", "vinzenz", "rudolf", "andreas", "anton", "felix", "julius",
         "ignatius", "simon", "martin", "jernej", "lenart", "urban", "franz", "fran ",
         "sine", "sin ", "moš", "vdovec", "otrok", "nicol", "markus", "marcus"]


def spol(ime, stan):
    t = f"{ime or ''} {stan or ''}".lower()
    for k in Z_IME:
        if k in t:
            return "Z"
    for k in M_IME:
        if k in t:
            return "M"
    return "?"


grib = [e for e in ENT if str(e["vas"] or "").startswith("Griblje")]
hrib = [e for e in ENT if "rible" in str(e.get("vas") or "").lower()]
hise = sorted({int(re.match(r"\d+", str(e["hisna"])).group()) for e in grib if e["hisna"] and re.match(r"\d+", str(e["hisna"]))})
hc = Counter(int(re.match(r"\d+", str(e["hisna"])).group()) for e in grib if e["hisna"] and re.match(r"\d+", str(e["hisna"])))
hx2 = []
for h, c in sorted(hc.items()):
    if c > 1:
        zx = [f"z{e['zap']}-{str(e['ime']).split()[0] if e['ime'] else '?'}-{e['mesec']}" for e in grib if str(e["hisna"]).startswith(str(h))]
        hx2.append(f"h{h} (×{c}: {' + '.join(zx)}!)")

starosti = [(starost_j(e["starost"]), e) for e in ENT]
with_s = [x for x in starosti if x[0] is not None]
najst = max(with_s, key=lambda x: x[0])
najml = min(with_s, key=lambda x: x[0])
spol_c = Counter(spol(e.get("ime"), e.get("stan")) for e in ENT)

# Griblje-otroci (starost < 10 let)
grib_otroci = [e for e in grib if (starost_j(e["starost"]) or 99) < 10]


def zstr(e):
    return f"z{e['zap']}-{e['vas']}-h{e['hisna']}-{e['starost']}"


def b_group(b):
    b = (b or "").lower()
    if any(k in b for k in ["fraisen", "friesen", "frisen", "kravipen", "krup", "krämpf", "krampf", "krivec", "krngruping", "friesl"]):
        return "FRISELN-družina"
    if "maff" in b or "masern" in b or "masch" in b:
        return "MASERN-glif"
    if "gehirnentz" in b or "entzünd" in b or "entzund" in b:
        return "ENTZÜNDUNG-družina"
    return (b.split() or ["?"])[0].rstrip('.,')


bg = Counter(b_group(e["bolezen"]) for e in ENT)
fr_total = sum(v for k, v in bg.items() if "FRISELN" in k or "MASERN" in k)
masern_total = bg.get("MASERN-glif", 0)
entz_total = bg.get("ENTZÜNDUNG-družina", 0)

duh = Counter()
for e in ENT:
    d = (e.get("duhovnik") or "").lower()
    if "jančar" in d or "jancar" in d:
        duh["Jančar-coop"] += 1
    elif "kogej" in d or "kogoj" in d or "hoggaj" in d or "hoggai" in d or "hogeju" in d or "heger" in d or "hoger" in d:
        duh["Kogej-subst-coop"] += 1
    elif "dovgan" in d or "dougan" in d or "dorgan" in d or "dovžan" in d:
        duh["Franz-Dovgan"] += 1
    else:
        duh["?/ni-podpisan"] += 1
grib_duh = Counter()
for e in grib:
    d = (e.get("duhovnik") or "").lower()
    if "jančar" in d or "jancar" in d:
        grib_duh["Jančar"] += 1
    elif "kogej" in d or "kogoj" in d or "hoggaj" in d or "hoggai" in d or "hogeju" in d:
        grib_duh["Kogej"] += 1
    elif "dovgan" in d or "dougan" in d or "dorgan" in d:
        grib_duh["Dovgan"] += 1
    else:
        grib_duh["?"] += 1

proof = {
    "faza": "P200",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1877 = 9/29 (issue #18; Kogej-obdobje-razširjeno-nazaj + 'Hrib'[?]-nova-lokalnost + P199-h12-popravek!)",
    "knjiga": {
        "signature": "04106",
        "obdobje": "1857–1885",
        "zupnija": "Podzemelj (Nadškofijski arhiv Ljubljana)",
        "vrsni": "matricula-online.eu",
        "vir": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
    },
    "okvir": {
        "leto_1877": "60 vpisov (z1–z60) — vrstna-aritmetika 11+10+12+10+9+8 + datum-veriga-continuous; P199-'1877 ≈ 85-?'-ocena-FALSIFICIRANA (groba-ocena-brez-podlage!)",
        "meja_1876_77": "★★★ s143-top: '18 77.'-glava-ODREZANA-off-scan (scan-edge!) — restart-evidenca: s142-Dez-1876-nad (10-vrstic + '1876.'-glava-v-z1!) + s143-Jänner-pod + z1-pokop-'1.' + nemška-opomba-'...in Podzemelj zu begraben' (KROP!) — z1 = delno-odrezana-vrstica (vas-'8'-v-2.-vrstici-vzorec + ime-'f f.'-kriptično [?])",
        "meja_1877_78": "s149 (P199-38.-potrditev-reuse: '18 78.'-SPLIT-v-z1-datuma-celici + restart-1!)",
        "konec_1877": "z60 = s148-v8: Dezember 21. (Krasinec-h41-Katharina-Bahovič[?]-68J)",
        "zaporedna": "z1–z60 — ŠTEVJE-IZ-VRSTIC (ordinali-NEVIDNI-na-vseh-6-straneh — forma-BREZ-ordinalnega-stolpca/scan-edge-off! recept-s148-2.×!); brez-znanih-praznih-vrstic (vse-60-vrstic-vsebujejo-vpise!)",
        "forma": "nemška-tiskana-'Sterb-Buch'-razprt + ordinalni-stolpec-OFF-SCAN (s143–s148!) + letnica-glave-v-datuma-celici (s145-z22-'1877.'! + s142-z1-'1876.'!) + mesečne-glave-v-vrsticah",
        "skeni": "s142–s148 (Pag. 136–142 = sken − 6; md5-križna-validacija-ta-seja: s148/s149-sveže == P199-disk-1:1!)",
        "preštevanje": "s143 z1–z11 → s144 z12–z21 → s145 z22–z33 → s146 z34–z43 → s147 z44–z52 → s148 (P199-reuse) z53–z60 = 60 ✓",
    },
    "statistika": {
        "vpisane_vrstice": len(ENT),
        "ordinali": 60,
        "griblje_vpisov": len(grib),
        "griblje_hise": hise,
        "griblje_hise_x2": hx2,
        "griblje_otroci": f"{len(grib_otroci)}/8 = {round(100 * len(grib_otroci) / max(len(grib), 1))}%-otroška-umrljivost-1877 (" + " + ".join(f"z{e['zap']}-{str(e['ime']).split()[0] if e['ime'] else '?'}-{e['starost']}" for e in grib_otroci) + ")!",
        "hrible_neznana": f"{len(hrib)}-vpisov-'Hrible'[?='Hrib'?] (z3/z6/z7-Tomc-klaster-h2/h2/h1! — G-glyph-duel-3.×-POZITIVEN: ≠Gradac-G + ≠s145-Griblje-G + ≠z4-'Gribl[j]ar'-G-vsi-descender-G — z3-inicial-BREZ-descenderja! 1.-pojav-v-korpusu! cf. 'Ukolk'[?]-1878!)",
        "najstarejsa": f"{zstr(najst[1])} — {najst[0]}-let (najstarejši-1877!)",
        "najmlajsa": f"{zstr(najml[1])} — {najml[0]}-let [{najml[1]['starost']}]",
        "male": spol_c.get("M", 0),
        "female": spol_c.get("Z", 0),
        "spol_neopredeljen": spol_c.get("?", 0),
        "bolezni_skupine": dict(bg.most_common()),
        "meseci": dict(sorted(Counter(e["mesec_no"] for e in ENT if e["mesec_no"]).items())),
    },
    "anomalije": [
        "★★★ MEJA-1876/77-s143-top: '18 77.'-glava-ODREZANA-off-scan (scan-edge!) — restart-evidenca-kompozitna (Dez-1876-nad + Jänner-pod + z1-pokop-'1.' + '...in Podzemelj zu begraben'-opomba!); z1 = delno-odrezana (vas-'8'-v-2.-vrstici-vase-celice + ime-'f f.'-kriptično [?] — KROP-kotek-max!)",
        "★★★ 39.-POTRDITEV-invariante: s145-'1877.'-glava-ZAPISANA-V-Z22-DATUMSKI-CELICI (nad-'März-28.' — 'prečrtan'-izgled = prepis-nad-mesecem! VLM-'tail'-zastavica-NAPAČNI-ALARM!) — invarianta-'glava-v-z1-celici-letnega-odseka'-v-NOVI-RAZLIČICI (mid-year!)",
        "★★★ 60-VPIISOV-ŠTEVJE-IZ-VRSTIC: ordinali-NEVIDNI-na-vseh-6-straneh (forma-brez-stolpca — P199-'1877 ≈ 85-?'-ocena-FALSIFICIRANA!) — vrstna-aritmetika + datum-veriga-continuous-×8-mesečnih-prelomov!",
        "★★★ 'HRIBLE'[?='Hrib'?]-NOVA-LOKALNOST-×3 (z3/z6/z7-Tomc-klaster: Margaretha-9mes-Fraisen + Katharina-3¼J-MASERN + Maria-19J-'im Feb. an Entzündung'[?]! h2/h2/h1) — G-glyph-duel-3.×-POZITIVEN (vsi-G-v-roki-descender; z3-inicial-ne!) — 1.-pojav-v-korpusu + 'z H.'-kratica-v-ime-z7!",
        "★★★ KOGEJ-OBDOBJE-RAZŠIRJENO-NAZAJ: substituendus-Hoggai[s]-Coop-1877-Jänner→Mai (s143-z2/z8/z9/z11 + GRIBLJE-z24-Pestotnik-Astma + z26-Šimec-Abzehrung!) — P199-'1878-Jänner–April'-obdobje-RAZŠIRJENA-NAZAJ-za-4-mesece!",
        "★★★ JANČAR-NIT-SPREMENJENA: NO-Jančar-podpis-v-1877 (Dovgan + Kogej-subst-izmenično!) — JANČAR-NIT-1878→1883 = 6-LET-STABILNA (ne-razširjena!) — tranzična-meja-April/Mai-1878-potrjena!",
        "★★★ PEZDINC-GRAFIA-NIT-#7: z51-Maria-PEZDINC-h53-1J-Wasserfriesl-Okt (KROP-'Pezdinc'-jasno — VLM-'Perdinc'-t/d-ZAVRJEN!) — veriga: 1877-z51 → 1878-×6 ('Vezdirz/Pozdrin/Pezdir(e)/Pecolar') → 1879-katastrofa-h40/h44!",
        "★★★ 'Br[a]stfbrand'[?]-KLASTER-×3-OKTOBER-1877 (z48-h62-Barbara-Hure-3¼J + z49-h57-Johann-Lozar-2J + z52-h6-Anna-Jakofčič-3¾J — ZAPOREDOMA! isti-word-3×; VLM-'Brennfieber/Bran[dt]'-nesoglasja!) — cf. tail-1876-s142-z4-'Vesperstmörfer[?]'-h44!",
        "★★★ GRIBLJE-OTROŠKA-UMRLJIVOST-75%-1877 (6/8: z26-8½J-Abzehrung + z39-9½mes-Hirnfall + z48-3¼J + z49-2J + z51-1J-Wasserfriesl + z52-3¾J!) — najvišja-do-sedaj-v-predzgodovini!",
        "★★★ ULEDBA-#10-8.-INSTANCE: z24-Griblje-h42-Pestotnik — smrt-29-April → pokop-1-Mai (KROP-datum!) — cf. P199-×7!",
        "★★★ h12-DEFINITIVNO-POPREVEK: z56-Katharina-DRAGOŠ-h12 (KROP-'12'-10×-jasno!) — P199-tail-'h18[?]'-ZAVRJEN! → h18-nit-referenca-oslabljena + NOVA-★★★ DRAGOŠ-NA-h12-NIT (krstni-1892-'Dragoš POVRAT' + 1907 + 1909 + 1912 + 1916-Dragoši + mrliški-1895/1899/1913/1918/1919-DRAGOŠI!) = 15-LET-PRED-KRSTNIM-PRVENCEM!",
        "★★ h18-ŠIMEC-NIT-1877: z26-Barbara-SINIEC-h18-8½J-Abzehrung-Mai ('Siniec' = ŠIMEC-grafia! VLM-soglasje!) — INNEC(1878)/SIMEC(1878-×2)/TIMEC(1881)-GRAFIA-DVOJNIČKA-4-IMENA-3-LETI-NA-h18!",
        "★★ z7-'im Feb. an Entzündung'[?]-bolezen-opomba-ampak-smrt-Jänner-28 (ANOMALIJA-mesec! KROP-2-vrstici!) + z2/z3-'Fraisen'[?]-'Amirsan'-VLM/KROP-nesoglasje (z3-VLM-'Frissen'-SOLGLASJE → FRISEN-nit-do-1877!)",
        "★ VLM-KROP-KOREKCIJE-×7: z48-3½→3¼J + z6-3½→3¼J (γ-frakcija-2.×!) + z56-h18[?]→h12 + s148-v3-'Kreuzsteing[?]'→'Abzehrung'-KROP + s146-VLM-v5/v6-DRIFT (real-v6 = Griblje-Catharina ✓) + z52-'Jakopič'→'Jakofčič'-KROP + z52-h6[~46?]→h6-samo!",
    ],
    "duhovniki": {
        "KOGEJ-RAZŠIRJENO-NAZAJ": "★★★ substituendus-Kogej/Hoggai[s]-'Coop.'-1877-Jänner→Mai (s143-×4 + Griblje-×2: z24-Astma + z26-Abzehrung!) — KROP-'Hoggai'-grafia-P199-identična!",
        "Dovgan-dominanta": "Franz-DOVGAN-1877-Griblje-×6 (z39/z48/z49/z51/z52/z56!) + Tomc-×3 + ne-Griblje-množica — Dovgan-era-1877–1878-1H",
        "JANČAR-NIT-STABILNA": "NO-Jančar-1877 — JANČAR-NIT-1878→1883 = 6-LET (tranzicija-April/Mai-1878-potrjena!)",
        "opomba": "KROP-podpis-crops-×15 (s143-strips + s145/s146/s147-desne + s148-z56!) — duhovnik-assignment-per-row = KROP-podpis-dokaz!",
    },
    "epidemija": {
        "Friseln": f"×{fr_total}-FRISELN-družina-1877 (vključno-z3-'Hrib'-Fraisen + z51-Wasserfriesl-'friesl'-grafia!) — NIT-kontekst: 1877-×{fr_total} → 1878-×12 → 1879-×14 → 1880-×28-FLOOD → 1881-×3 → 1882-×16!",
        "MASERN": f"×{masern_total}-1877 (z6-'Hrib'-h2-Katharina-Tomc-3¼J — KROP-'Masern'-jasno!) — M-NIT-kontekst: 1878-×2-adjacent + 1880-FLOOD!",
        "Br[a]stfbrand[?]": "×3-OKTOBER-KLASTER (z48/z49/z52-zaporedoma! — neberljivo-word; VLM-nesoglasja; 1.-pojav-v-korpusu!)",
        "Hirnfall": "×1-Griblje (z39-h8-Catharina-Jakofčič-9½mes!) + ×1-'Hrib'[?]... ",
        "ENTZÜNDUNG-družina": f"×{entz_total}-skupaj (Hirnentzündung-tail-1876-×2 + 'im Feb. an Entzündung'-z7!)",
        "Asthma": "×2-Griblje-kandidata (z24-Pestotnik-53½J + tail-1876-z6-Stubler-50⅔J!) + s142... ",
        "Abzehrung": "×3+ (z26-Griblje-h18-Šimec-8½J + s148-v3-KROP-popravek + ...)",
    },
    "hišne_kontinuitete": [
        "h53-GRIBLJE: z51-Maria-PEZDINC-1J-Wasserfriesl-Okt-1877 → 1878-z83-Mathias-PEGLAVC-87J-Wassersucht (h53-nit-×2-v-2-letih! + PEZDINC-#7!)",
        "h57-GRIBLJE: z49-Johann-LOZAR-2J-Okt-1877 → 1878-z80-Maria-LOGAR-17J-GEHIRNENTZÜNDUNG-Nov (h57-nit-×2-v-2-letih!)",
        "h18-GRIBLJE: z26-Barbara-SINIEC[ŠIMEC]-8½J-Mai-1877 → 1878-z1-Theresia-INNEC?-41J-Jänner (h18-nit-×2 + INNEC/SIMEC/TIMEC-4-IMENA!)",
        "h12-GRIBLJE: z56-Katharina-DRAGOŠ-21J-Nov-1877 (P199-'h18[?]'→h12-POPREVEK!) → ★★★ DRAGOŠ-h12-NIT: krstni-1892-DRAGOŠ-prvenec + 1907/1909/1912/1916-Dragoši + mrliški-1895-Janez-DRAGOŠ-69J + 1899-Matija-DRAGOŠ + 1913-Ana-DRAGOŠ-81J + 1918/1919! = 15-LET-PRED-PRVENCEM!",
        "h44-TAIL-1876 (s142-z4): Barbara-KAVČIČ[?]-24-URE!-Dez-Vesperstbrand[?] → 1878-z77-Mathias-'Pecolar[?]'-44J + 1879-z27/z28-GEHIRN-KATASTROFA (h44-nit-×3-čez-3-leta!)",
        "h16-TAIL-1876 (s142-z7): Anna-PILAH[~Spilak?]-3½J-Dez-Hirnentzündung → 1878-z41-Johann-JILAK-h16 (h16-dvojna-identifikacija-1878!)",
        "h75-TAIL-1876 (s142-z6): Joannes-STUBLER-50⅔J-Dez-Asthma → P171?-h75-nit (1.-dokaz-1876!)",
        "h8-GRIBLJE-1877: z39-Catharina-JAKOFČIČ-9½mes-Aug (nov-dokaz! — 1878-BREZ-h8!) — JAKOFČIČ-×2-1877 (z39 + z52!)",
        "h62/h6/h42-GRIBLJE-1877: NOVI-dokazi (1878-BREZ-teh-hiš!)",
    ],
    "forme": [
        "nemška-tiskana-'Sterb-Buch'-skroz (slovenska-šele-1885!)",
        "ORDINALNI-STOLPEC-OFF-SCAN-na-vseh-6-straneh (s143–s148!) — forma-razlika-vs-P199-strani (s150+-ordinali-vidni!) — scan-centering-varia!",
        "MEJA-'1877.'-glava-V-Z22-DATUMSKI-CELICI-s145 (mid-year-različica-'glava-v-z1-celici'! 'prečrtan'-izgled = prepis-nad-mesecem!) = 39.-potrditev-v-NOVI-OBLIKI",
        "'1876.'-glava-v-z1-s142 (tail-1876-kontekst!)",
        "mesečne-glave-v-vrsticah: 'Jänner'@z1-s143-[odrezan?] + 'Februar'@z8/9-s143 + 'März'@s144-top + 'April'@z23-s145 + 'Mai'@z24/25-s145 + 'Juni'@z32/33-s145 + 'Juli'@s146 + 'August'@z38/39-s146 + 'September'@s146-v10/s147 + 'October'@z48-s147 + 'November'@z54-s148 + 'Dezember'@z60-s148 ✓",
        "hišne-v-2.-vrstici-vase-celice-vzorec (z1-'8' + z2-Gradac-'8'!)",
    ],
    "crossChecks": [
        "md5-križna-validacija-ta-seja: s148 (cfb227bde948) + s149 (ae3e71e1853d) sveže == P199-disk-1:1 ✓ — veriga-P197→P198→P199→P200-bajtno-zvezana-4.×!",
        "z-continuity-×6-strani: 11→21→33→43→52→60 ✓ (datum-veriga-continuous: Jän1→Feb28/Mär1→März5→März28→Juni26→Sept28→Okt18→Dez21→1878-restart!)",
        "1877-konec = z60-s148-v8-Dez-21 ✓ + 1878-start = s149-restart-1 (P199-reuse!) ✓",
        "s148-tail-8-vrstic-1:1 == P199-tail_1877-reuse (md5-validirano!) ✓",
        "G-glyph-duel-3.×: Gradac-G + s145-'Griblje'-G + z4-'Gribl[j]ar'-G (vsi-descender!) vs z3/z6/z7-inicial (brez-descenderja!) = 'Hrib'-lokalnost ✓",
        "s145-'1877.'-glava-v-z22-celici (KROP-4×) + s142-'1876.'-glava-v-z1 ✓ (39.-potrditev!)",
        "meseci-sklenjeni: Jänner-11 → Dezember-1 (ditto-backfill!) ✓",
        "duhovnik-podpisi-×15-KROP: Kogej-subst-×6 (vključno-Griblje-×2-Mai!) + Dovgan-×9 (Griblje-×6!) ✓",
        "z48-datum-'October-1|3'-KROP-5× + h62 + 'Erbin-des-Anton-¼G.' ✓ (kompletna-vrstica!)",
        "s147-ordinal-'5'-v-datumskem-stolpcu-pod-z48 = z49-burial-'5' (NE-ordinal! forma-brez-stolpca!) ✓",
    ],
    "honesty": {
        "H1": "VLM-branja-fresh-×6-ta-seja (s142–s147) + s148-reuse-P199-VLM (md5-križna-validacija-1:1!) — matricula-1:1",
        "H2": f"KROP-izreki-×{RAW["meta"]["krop_izreki"]} (vas-max-zoom-8×-×4 + ime-crops + desne-podrobnosti + podpis-crops + datum-crops-5×!) — VSE-v-KROP-poljih!",
        "H3": "'Hrible'[?]-×3-NEZNANA-LOKALNOST — G-glyph-duel-dokumentiran-3.×, identifikacija-ODPRTA ('Hrib'-kandidat; cf. 'Ukolk'-1878)!",
        "H4": "spol = IME-HEVRISTIKA (M/Ž/?) — NI-prebrano-iz-kljukic-stolpcev!",
        "H5": "z1-s143 = delno-ODREZANA-vrstica (smrt-[?] + vas-'8'-h? + ime-'f f.'-kriptično [?] + '...in Podzemelj zu begraben'-opomba) — 1877-z1-dokumentirana-kot-[?]!",
        "H6": "'18 77.'-glava-s143 = ODREZANA-off-scan — MEJA-1876/77-VPREDPOLOŽENA-iz-kompozitne-evidence (restart + Jänner + Dez-1876-nad)!",
        "H7": "ordinali-NEVIDNI-×6 — z-števec = VRSTNO-ŠTETJE (brez-praznih-vrstic-zaznanih; možna-±0-do-±2-nenajdena-prazna-celica!)",
        "H8": "'Br[a]stfbrand'[?]-×3-neberljivo-word (z48/z49/z52) + 'Alt___sfr____'[?]-z56 + 'Vesperstmörfer'[?]-tail-1876 — bolezni-dokumentirane-kot-[?]",
        "H9": "VLM-KROP-korekcije-×7-dokumentirane (frakcije + h12 + 'Abzehrung' + DRIFT + 'Jakofčič' + h6)",
        "H10": "z56 = P199-REUSE-tail_1877 (md5-1:1!) + ta-seja-KROP-h12-DEFINITIVNO — P199-'h18[?]'-IZRAZITO-POPRavljen",
        "H11": "duhovnik-per-row = KROP-podpis-crops-×15 (ne-VLM!) — 'substituendus-Hoggai'-grafia-dokumentirana",
        "H12": "starosti-'3¼'-×2-frakcija-popravki + '21'[2/7-zmeda-'71'] + '24-URE'-tail-1876 — KURRENT-zmede-dokumentirane",
        "H13": "mesec-ditto-backfill (vrstice-brez-meseca ← prejšnja!) — VLM-ni-vedno-vnesel",
        "H14": "z4-'Gribl[j]ar[?]'-mencija-v-ime-stolpcu (Anna-Maru-Primostek-h10-vdova) = GRIBLJE-MENCIJA-ne-vpis!",
        "H15": "s146-VLM-v5/v6-DRIFT: VLM-je-vrste-navedel-v-premaknjenem-vrstnem-redu — real-v6 = Griblje-Catharina (KROP-potrjeno!)",
        "H16": "z2/z3-bolezen-'Fraisen'[?]-'Amirsan'-nesoglasje (z3-VLM-'Frissen'-soglasje → KROP-'Fraisen')!",
    },
    "kaskada": {
        "vitals": "1347 → 1355 (+8-blokov-04106-1877!)",
        "04106": "128 → 136 (16×-1885 + 21×-1884 + 11×-1883 + 16×-1882 + 19×-1881 + 13×-1880 + 9×-1879 + 23×-1878 + 8×-1877!)",
        "04894": "520-NESPREMENJENO",
        "p80": "94-NESPREMENJENO",
        "korpus": "93-NESPREMENJEN",
        "pt_luknja": "18-REGENERIRANA (136/1355!)",
        "qa": "qa-p200 = 200.-kontrola (vzorec-qa-p199!)",
    },
    "lead": {
        "P201": "mrliška 04106, leto 1876 (10/29!) — SIDRA: s142-tail = Dez-1876-×10-vrstic (ŽE-PREBRANO-ta-seja! Griblje-×3: z4-h44-Barbara-KAVČIČ[?]-24-URE-Vesperstbrand[?]-Dez-24/25 + z6-h75-Joannes-STUBLER-50⅔J-Asthma + z7-h16-Anna-PILAH[~Spilak?]-3½J-Hirnentzündung!) + '1876.'-glava-v-z1-s142! + ordinali-[?] (s142-strip-NE-preverjen-ta-seja!) → probe: s134–s142; 1876-začetek = išče-nazaj (≈60-85-?-vpisov); krstna-04104 + poročna-04455-čakata!",
        "krstna": "04104-1871–1885-×200-skenov-čaka (vzporedno!)",
        "poročna": "04455-začetek-1873–1885-čaka",
    },
    "entries": ENT,
    "tail_1876": TAIL76,
    "notes": [
        "P200-metodologija: P199-recept-100%-reuse + md5-križna-validacija-verige (P197→P198→P199→P200-4.×!) + ŠTEVJE-IZ-VRSTIC (recept-s148-2.×-uporaba — ordinali-off-scan-×6!) + G-glyph-duel-nova-metodologija (lokalnost-vs-lokalnost-glyph-primerjava-v-isti-roki!)",
        "lekcija-#18-potrjena-×15: double-scan-RE-ALIGNMENT (levi/desni-strani-skew-do-±2-vrstice-na-s145/s148!) — row-tracing-obvezen",
        "NOVA-metodologija-#19?: VLM-'tail'-zastavica-NAPAČNI-ALARM-na-mid-year-glavo (s145-'1877.'-v-celici!) — meje-samo-prek-restart+datum-verige!",
        "lekcija-#14-potrjena: VLM-raw > VLM-interpretacija ('Perdinc'→'Pezdinc'! 'Jakopič'→'Jakofčič'! 'Kreuzsteing'→'Abzehrung'! 'Siniec'→ŠIMEC-grafia!)",
        "P199-KOREKCIJA: tail-z4-'h18[?]' → KROP-h12 (10×-jasno!) — P199-parish.ts-z1-blok-h18-nit-referenca-OSLABLJENA (blok-vsebuje-'[?]'-oznako — P200-dokumentira-resitev!)",
        "P199-OCENA-KOREKCIJA: '1877 ≈ 85-?' → 60 (vrstna-aritmetika!) — ocena-bila-groba (brez-scan-podlage)",
    ],
}

OUT.parent.mkdir(parents=True, exist_ok=True)
json.dump(proof, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"PROOF-OK: {OUT}")
print(f"vpisov={len(ENT)} griblje={len(grib)} hise={hise} hrible={len(hrib)}")
print(f"najst={najst[0]}J-z{najst[1]['zap']} najml={najml[0]}J-z{najml[1]['zap']}")
print(f"spol={dict(spol_c)} friseln={fr_total} entz={entz_total}")
print(f"duh={dict(duh)} grib_duh={dict(grib_duh)}")
print(f"otroci-griblje={len(grib_otroci)}/8")
print(f"meseci={dict(sorted(Counter(e['mesec_no'] for e in ENT if e['mesec_no']).items()))}")
