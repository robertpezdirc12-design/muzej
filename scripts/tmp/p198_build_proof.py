#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P198 — build proof JSON: research/issue17/parish-death-1879-04106.json
(Zrcaljenje P197-strukture; SANACIJA-RE-RUN-usklajen: re-fetch-1:1 + re-VLM-×7
+ re-arbitraža-×5 + re-read-soglasja-dokumentirana!)"""
import json, re
from collections import Counter
from pathlib import Path

RAW = json.load(open("/tmp/p198/entries_raw.json"))
ENT = RAW["entries"]
TAIL78 = RAW["tail_1878"]
OUT = Path("/home/z/muzej/research/issue17/parish-death-1879-04106.json")


# ——— starost-parser (P196/P197-vzorec; '('-split-proti-note-leak!) ———
def starost_j(mala):
    if not mala:
        return None
    s = str(mala).lower().split("(")[0]
    m = re.search(r"(\d+)", s)
    if not m:
        return None
    n = float(m.group(1))
    if "¾" in s and re.search(r"1\s*¾", s):
        n = 1.75
    if "mesec" in s or "monat" in s:
        return round(n / 12, 3)
    if "teden" in s or "woche" in s:
        return round(n / 52, 3)
    if " dan" in s or "tagn" in s or "tage" in s:
        return round(n / 365, 3)
    if "ura" in s or "minut" in s or "std" in s:
        return 0.001
    return n


Z_IME = ["maria", "anna", "ana ", "katharina", "catharina", "margaretha", "theresia",
         "elisabeth", "agnes", "barbara", "ursula", "lucia", "johanna", "magdalena",
         "vdova", "hči", "hcer", "dohtar", "chter", "tochter", "žena", "egovina",
         "služkinja", "magd", "-in ", "jarina", "mati", "rosalia", "doroth", "martha"]
M_IME = ["johannes", "joannes", "johann", "janez", "georg", "joseph", "josef", "jožef",
         "mathias", "matthias", "matevž", "michael", "mich.", "nicolaus", "miklavž",
         "jakob", "peter", "vinzenz", "rudolf", "andreas", "anton", "felix", "julius",
         "ignatius", "simon", "martin", "jernej", "lenart", "urban", "franz", "fran ",
         "sine", "sin ", "moš", "vdovec", "otrok", "nicol"]


def spol(ime, stan):
    t = f"{ime or ''} {stan or ''}".lower()
    for k in Z_IME:
        if k in t:
            return "Z"
    for k in M_IME:
        if k in t:
            return "M"
    return "?"


grib = [e for e in ENT if e["vas"] and str(e["vas"]).startswith("Griblje")]
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
spol_c = Counter(spol(e["ime"], e["stan"]) for e in ENT)


def zstr(e):
    return f"z{e['zap']}-{e['vas']}-h{e['hisna']}-{e['starost']}"


def b_group(b):
    b = (b or "").lower()
    if any(k in b for k in ["fraisen", "friesen", "frisen", "kravipen", "krup", "krämpf", "krampf", "krivec"]):
        return "FRISELN-družina"
    if "maff" in b or "masern" in b or "masch" in b:
        return "MASERN-glif"
    return (b.split() or ["?"])[0].rstrip('.,')


bg = Counter(b_group(e["bolezen"]) for e in ENT)
fr_total = sum(v for k, v in bg.items() if "FRISELN" in k or "MASERN" in k)

proof = {
    "faza": "P198",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1879 = 7/29 (issue #18; SANACIJA-RE-RUN-seja!)",
    "knjiga": {
        "signature": "04106",
        "obdobje": "1857–1885",
        "zupnija": "Podzemelj (Nadškofijski arhiv Ljubljana)",
        "vrsni": "matricula-online.eu",
        "vir": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
    },
    "sanacija": "/tmp-wipe-med-sejo → muzej-re-clone-iz-GitHub-@195b4e1 (P197-komplet!) + re-fetch-8/8 (velikosti-1:1-P197-seji!) + re-VLM-×7 (s157–s163) + tail-z62/z63-iz-SEJNEGA-ZAPISA (P197-KROP-1:1!) + re-arbitraža-×5-cropov — deterministična-reprodukcija (vzorec-P156-sanacija!)",
    "okvir": {
        "leto_1879": "64-fizičnih-vrstic / 63-ordinalov (z1–z63 + ★z28-DUPLIKAT!) — P197-'63-vpisov'-napoved-EXAKT-MATCH!",
        "meja_1878_79": "s158 'Incipit annus' (KROP-1.-seje; re-read-'Summarischer-Anno'-ZAVRJEN!) + velika-'1879'-črta = SPLIT-VARIANTA ('1 8' + '7 9'-STACKED-na-desni-TP — KROP-POTRJENO!) = 37.-POTRDITEV-invariante (P197-'1 8|8 0'-36. + P196-'18/81'-35. + ...) + restart-85→1!",
        "meja_1879_80": "s164-mid-'1 8|8 0'-SPLIT (= P197-36.-potrditev-reuse!) + tail-z62,z63 (P197-KROP-1:1-reuse!)",
        "konec_1879": "z63-Dezember-smrt-31.12→pokop-1.1.1880-Certoviše-h7-Nicol-Jakofčič-9-mes-Friesen (P197-KROP-1:1! ULEDBA-#10!)",
        "zaporedna": "z1–z63 + ★ z28-DUPLIKAT (s160-konec-'28'-Mathias-Peglic-h40-97J + s161-top-'28'-Martin-Pezdirc-h20-44J — rdeči-margin-KROP + RE-READ-SOGLASJE-28!) = 3.-številčna-anomalija-04106 (cf. P196-z8-DUPLIKAT + P197-z55-IZPUŠČENA!)",
        "forma": "nemška-tiskana-'Sterb-Buch'-razprt (dvostanski-čez-gutter!) + rdeči-ročni-margini-ordinali + 'Incipit-annus'-band (NOVO-forma-element!)",
        "skeni": "s157–s164 (Pag. 151–158 = sken − 6; re-fetch-velikosti-1:1 + PRINTED-'152/153/154/155/156'-×5-VIZUALNO-KROP!)",
        "preštevanje": "s158 z1–z6 → s159 z7–z17 → s160 z18–z28 → s161 z28-DUP,z29–z37 → s162 z38–z49 → s163 z50–z61 → s164-tail z62–z63 = 63-ordinalov ✓ (P197-napoved-'63'-EXAKT!)",
    },
    "statistika": {
        "vpisane_vrstice": len(ENT),
        "ordinali": 63,
        "griblje_vpisov": len(grib),
        "griblje_hise": hise,
        "griblje_hise_x2": hx2,
        "najstarejsa": f"{zstr(najst[1])} — {najst[0]}-let ★KORPUS-REKORD (KROP-max-zoom-'9'+γ-7+'.'-identično-z27-'37.' + RE-READ-SOGLASJE-'97[~9J/97?]'!; cf. 1881-Jure-Movrin-90J-prejšnji-max!)",
        "najmlajsa": f"{zstr(najml[1])} — {najml[0]}-let [{najml[1]['starost']}]",
        "male": spol_c.get("M", 0),
        "female": spol_c.get("Z", 0),
        "spol_neopredeljen": spol_c.get("?", 0),
        "bolezni_skupine": dict(bg.most_common()),
        "meseci": dict(sorted(Counter(e["mesec_no"] for e in ENT if e["mesec_no"]).items())),
    },
    "anomalije": [
        "★★★ MEJA-1878/79-s158: 'Incipit annus' + velika-'1879'-SPLIT-VARIANTA ('1 8'+'7 9'-stacked-desno-TP — KROP!) = 37.-POTRDITEV-invariante + restart-85→1 (tail-ordinali-83–85: KROP-hipoteza-1.-seje + RE-READ-SOGLASJE-2.-seje = RAZREŠENO-v-fakt!)",
        "★★★ z28-DUPLIKAT: obe-vrstici-'28' (Mathias-Peglic-h40-97J + Martin-Pezdirc-h20-44J) — s161-margin-strip-28,29,30–37-KROP-VSI-JASNI + RE-READ-SOGLASJE-28! = 3.-številčna-anomalija-04106 (P196-z8-dup-1. + P197-z55-skip-2.!)",
        "★★★ KRONOLOŠKI-PRESKOKI-×2-LOKACIJE: Jänner z6(26.)→z7(23.)→z8(24.)-KROP-max('23'+'24'-jasna!) + Dezember-1879 3→13→12→7→21 (s163-z57–z61-KROP-datumi + RE-READ-SOGLASJE!) — nazaj-zapolnitve/vpisi-po-pokopu (vzorec-za-P199+!)",
        "★★★ z28-Mathias-Peglic = 97-LET ★KORPUS-REKORD-STAROSTI (KROP-max-zoom-'9'+γ-7+'.'-struktura-identična-z27-'37.' + RE-READ-'97[~9J/97?]'-SOGLASJE!) — cf. 1881-Movrin-90J = prejšnji-max!",
        "★★★ GEHIRNENTZÜNDUNG-KATASTROFA-×2-ISTEGA-DNA: z27-Maria-Peglic-h44-37J + z28-Mathias-Peglic-h40-97J (obe-26./28.-Mai!) — h44+h40-sosednji = žarišče? (ARBITRAŽA: '-entzündung'-konec-umlaut — re-read-'Gichtarmzündung'-ZAVRJEN!)",
        f"★★★ FRISELN-×{fr_total}-1879 — KRIVULJA: 1879-×{fr_total} → 1880-×28-FLOOD-P197 → 1881-×3-DOLINA → 1882-×16 (W-oblika!)",
        "★★ ULEDBA-#10-6.-INSTANCE: z28-DUP-smrt-'Junii-29'→pokop-'1.'+'Juliβ'-header-v-vrstici (ARBITRAŽA-A1-ODLOČILNA: 'Junii'-jasno — re-read-'July-29/Aug-1'-ZAVRJEN!) + z63-tail-31.12→1.1. (P197-1:1!) — cf. P196-z80+z73+z68+z18 = 4-instance!",
        "★★ z47-Griblje-h20-BREZ-starosti/bolezni (RE-READ-SOGLASJE-[?]!) + ime-'Nelly?[~Molly/Marija/Marthy-4-varianti!]-Abramšek?[~]-Pivk?[~Elend-re-read]' — mrtvorojen?/nedokončan-vpis!",
        "★★ z35-totgeboren (tod-'—', starost-'—', bolezen-'—' — Prilozje-h25!) + z30-'unget'[ungetauft!]-Ceroviše-h11-10J",
        "★★ h20-×2-1879: z28-DUP-Pezdirc (Juni) + z47-Abramšek/Pivk (Okt) — cf. PEZDIREC-era-h20-P171-1906!",
        "★ z1-vas-'Oho-b?'[~Otok-re-read — NERAZREŠENO [?]] + z1-ime-'Mathias-Novak'-ARBITRAŽA-JASNO (re-read-'Dovgan'-ZAVRJEN!)",
        "★ z17-eksotična-vrsta: 'Im-Prgadton-Turškem[?]-bei-Leuggers' + 2-imeni — zunaj-parafija? [?]",
        "★ z42-Zemelj-h24-DVOJNICA-z45 (Martin-Kuc-12-tednov?-Sept + Anna-Kuc-42J-Gehirnentzündung-Okt — ista-hiša-v-3-tednih!)",
        "★ VLM-RE-READ-VARIANCA-×5: z5-'88'→82-KROP + z6-'¾-J'→74-KROP + z83-'Marthe-17'→Mathias-87-KROP + z1-'Dovgan'→Novak-ARBITRAŽA + z27-'14'→44-ARBITRAŽA — max-zoom-KROP > VLM (6.-potrditev-vzorca-P156!)",
    ],
    "duhovniki": {
        "Jančar-dominanta": "GRIBLJE-9/9 (100%!) — coop.-forma-skroz (5.-leto-nit: 1879→1880→1881→1882→1883!) — VLM-variant-podpisov-'Janezak/Hancar/Jančar/Lončar/Vančar/Janičar' = ISTA-PODPIS-KURRENT-forenzika (P197-naraščaj-reuse!)",
        "Dovžan/Dovgan": "ne-Griblje-vpisov (z1-'Franc-Dovgan'-re-read-soglasje! + z9,z11,z12,z13,z16 + z29,z31,z32 + z41,z45...) — cf. 1881-izključno-ne-Griblje = vzorec-ostaja!",
        "opomba": "Jančar-coop-×Griblje-9/9 = 100%-dominanta-tudi-v-1879 (5.-časovno-leto-nit-od-1883-nazaj!)",
    },
    "epidemija": {
        "Friseln": f"×{fr_total}-skupina — W-KRIVULJA: 1879-×{fr_total} → 1880-×28 (P197!) → 1881-×3 (P196!) → 1882-×16 (P195!) — otroška-epidemija-cikliranje!",
        "M/W-NIT": "×1 (z2-Anna-'Maffpüffl'?[~Masern-glif-1.-branje; re-read-'Wassersucht'-varianca-[~]!]-60J-Mlake — cf. P196-×4 + P197-×3-nit!)",
        "Gehirnentzündung": "×2-istega-dna (z27-37J + z28-97J — Peglic-katastrofa!) + z45-'In folge der Gehirnentzündung' (Anna-Kuc-42J!) = ×3-skupaj!",
        "Abzehrung": "×6+ (z1,z4,z20?,z28-DUP-[Abmattsschwäche?]...) — cf. 1881-nit!",
        "Asthma": "×3+ (z5-Griblje-h56! + z85-tail-1878 + z49)",
        "Wassersucht": "×1 (z83-tail-1878-Griblje-h53-87J!)",
    },
    "hišne_kontinuitete": [
        "h56-GRIBLJE: z5-Peter-Šimec-82J-1879 → ŠIMEC-nit (cf. 1880-z19-Anna-Simec-h39 + 1881-h18-TIMEC-P196!)",
        "h1-GRIBLJE: z6-Anna-Zeliha-74J-1879 → ZELŠKO-h1-×2-1882-P195 (h1-nit-2.-vpis-nazaj!)",
        "h53-GRIBLJE: tail-1878-z83-Mathias-Peglavc-87J-Wassersucht + z15-Peter-Bežek?-½J-1879 (h53-nit-×2-v-2-letih!)",
        "h44-GRIBLJE: z27-Maria-Peglic-37J-1879 (nov-dokaz! ARBITRAŽA-'44'-jasno!)",
        "h40-GRIBLJE: z28-Mathias-Peglic-97J-★KORPUS-REKORD-1879 (nov-dokaz! RE-READ-SOGLASJE!)",
        "h20-GRIBLJE-×2: z28-DUP-Martin-Pezdirc-44J-Juni + z47-Nelly?-Abramšek/Pivk-Okt (cf. PEZDIREC-era-h20-P171-1906-04894!)",
        "h30-GRIBLJE: z58-Martha-Križan-60J-1879 (nov-dokaz! RE-READ-SOGLASJE-vas/ime/starost!)",
        "h32-GRIBLJE: z59-Maria-Kraus-½J-1879 (nov-dokaz! RE-READ-SOGLASJE!)",
    ],
    "forme": [
        "nemška-tiskana-'Sterb-Buch'-skroz (slovenska-šele-1885-s205/s206-P192!)",
        "'Incipit annus'-band-NOVO-forma-element (KROP-1.-seje! re-read-'Summarischer-Anno'-ZAVRJEN!) = letni-uvodni-zapis",
        "MEJA-'1879'-SPLIT-VARIANTA: '1 8'+'7 9'-STACKED-na-desni-TP (ne-Levo|Desno-kot-1880!) — invarianta-37.-potrditev-v-novi-obliki!",
        "RADEČI-MARGINI-ORDINALI = KROP-berljivi (s161-strip-28–37-VSI + s157-strip-73–82-VSI!) — VLM-misread-7→6-sistemsko-obeh-sej!",
        "PRINTED-page-številke-×5 (152–156) — nova-potrditvena-sloj-preslikave!",
        "mesečne-glave-v-vrstici: '1879-Jänner'@z1+s159-top + 'Feber'@z9 + 'März'@z13 + 'April'@z19 + 'Mai'@z25 + 'Juliβ'@z28-DUP-ULEDBA + 'August'@z32 + 'September'@z38 + 'October'@z44 + 'December'@z57 ✓",
    ],
    "crossChecks": [
        "pag=sken−6: PRINTED-152(s158) + 153(s159) + 154(s160) + 155(s161) + 156(s162) = ×5-VIZUALNO-KROP ✓ (17.–21.-potrditev-preslikave!)",
        "re-fetch-md5-velikosti-1:1-P197-seji (s163=421706-B + s164=384600-B + s158=430346-B!) ✓ — matricula-stabilni-JPEG",
        "restart-85→1: 'Incipit-annus'-band-s158-KROP + rdeči-margini-1.–6. + RE-READ-tail-83/84/85-SOGLASJE ✓",
        "z-continuity-×7-strani: 6→17→28→[28-DUP!]→37→49→61→63 ✓ (dup-dokumentiran! RE-READ-zap-listi-1:1-s-1.-sejo!)",
        "1879-konec = z63-s164-tail (P197-KROP-1:1: rdeči-margini-62,63!) ✓ == P197-napoved-'63-vpisov'-EXAKT!",
        "Griblje-z58/z59-s163: RE-READ-SOGLASJE-×2-branji (Martha-Križan-h30-60J + Maria-Kraus-h32-½J!) + datumi-KROP-crop (Dec-13/15 + Dec-12/13!) ✓",
        "meseci-sklenjeni: Jänner-9 → Dezember-6 (brez-luknje; vsota=64!) ✓",
        "letnica-×2-viri: 'Incipit-annus'+big-'1 8'/'7 9'-KROP (s158) + '1879'-glava-s159-KROP ✓",
        "s157-ordinali-73–82-KROP (VLM-'63–72'-7→6-obeh-sej!) → 1878 ≈ 85-vpisov [P199-potrdi!] ✓",
        "ARBITRAŽE-×5 (re-run): A1-Junii-datum + A2-h44 + A3-Gehirn + A4-Novak + A5-Mlake — max-zoom > VLM ✓",
    ],
    "honesty": {
        "H1": "VLM-branja-×7-fresh-re-run (s157–s163) + tail-z62/z63-iz-SEJNEGA-ZAPISA (P197-KROP-1:1-prebran-na-zacetku-te-seje!) — matricula-1:1 (velikosti-md5!)",
        "H2": "KROP-izreki-×24 (1.-seja-cropi-×20 + RE-RUN-arbitraže-×5-cropov) — VSE-v-KROP-poljih!",
        "H3": "z47-ime-'Nelly?[~Molly/Marija/Marthy]-Abramšek?[~]-Pivk?[~Elend]' — 4-ime-varianti-NERAZREŠENE [~] (vas-Griblje-h20-JASNO-obeh-branj!)",
        "H4": "spol = IME-HEVRISTIKA (M/Ž/?) — NI-prebrano-iz-kljukic-stolpcev!",
        "H5": "tail-1878-ordinali-83–85: KROP-hipoteza-1.-seje + RE-READ-SOGLASJE = 2-viri-fakt (P199-potrdi-s156!)",
        "H6": "s157-VLM-'63–72'-7→6-misread-obeh-sej (KROP-margin-strip-73–82-1.-seje!) — VLM-marginalni-ordinali-NIČE-vredni-brez-KROP (lekcija-#12-potrjena!)",
        "H7": "z1-vas-'Oho-b?'[?] + z17-eksotična-vrsta [?] + z15-priimek-'Bežek?[~Grčevac-re-read]' [?] — ne-Griblje-identitete/priimki NERAZREŠENI (dokumentirani!)",
        "H8": "z15-bolezen-'Krämpfe?[~Farnism]' + z42-starost-'12-tednov?[~]' — kripto-abreviature [~]",
        "H9": "z28-DUP-mesec: 'Junii-29'-smrt (ARBITRAŽA-A1!) — re-read-'July-29'-ZAVRJEN (vzela-'Julβ'-header-kot-mesec-smrti!)",
        "H10": "z6-bolezen-'Fraisen' — SOGLASJE-obeh-branj (1.-seja-KROP-potrjeval-VLM!)",
        "H11": "z58/z59 = RE-READ-SOGLASJE-×2-branji (P197-vlm + fresh) — datumi-KROP-crop-te-seje; stan-varianti-dokumentirane ('½-Grefin-Altna'-P197 vs '½-hči-dekla'-fresh [~]!)",
        "H12": "z62/z63 = P197-KROP-1:1-reuse-iz-sejnega-zapisa (/tmp-wipe; P199-jih-vzame!)",
        "H13": "z3-starost-'10-dni' (VLM-'mesecev/Montag'-ZAVRJEN-obeh-branj-KROP!) + bolezen-'Friesen' (F-ligatura!)",
        "H14": "najstarejša-97J = KROP-max-zoom-dokaz + RE-READ-SOGLASJE ('97[~9J/97?]' — re-read-vprašaj-dokumentiran, KROP-odločil)",
        "H15": "z27-priimek-'Peglic?[~Pegelj/~Pezdirc]' + z28-isto — priimkov-varianta-NERAZREŠENA [~] (hiši-h44/h40-JASNI!)",
    },
    "kaskada": {
        "vitals": "1315 → 1484 (+9-blokov-04106-1879!)",
        "04106": "96 → 105 (16×-1885 + 21×-1884 + 11×-1883 + 16×-1882 + 19×-1881 + 13×-1880 + 9×-1879!)",
        "04894": "520-NESPREMENJENO",
        "p80": "94-NESPREMENJENO",
        "korpus": "93-NESPREMENJEN",
        "pt_luknja": "18-NESPREMENJENA",
        "qa": "qa-p198 = 198.-kontrola (vzorec-qa-p197!)",
    },
    "lead": {
        "P199": "mrliška 04106, leto 1878 (8/29!) — SIDRO-ŽE-POTRJENO-×2-SEJI: s157 = z73–z82 (margin-strip-KROP-1.-seje-73–82-VSI-JASNI; VLM-'63–72'-7→6-obeh-sej!) + s158-tail = z83–z85 (KROP-hipoteza + RE-READ-SOGLASJE-2.-seje = 2-viri! 1878 ≈ 85-vpisov!) → probe: s150–s157; 1878-začetek = z1-išče-nazaj + krstna-04104-čaka!",
        "krstna": "04104-1871–1885-×200-skenov-čaka (vzporedno!)",
        "poročna": "04455-začetek-1873–1885-čaka",
    },
    "entries": ENT,
    "tail_1878": TAIL78,
    "notes": [
        "P198-metodologija: P197-recept-100%-reuse + SANACIJA-RE-RUN (muzej-re-clone-iz-GitHub + re-fetch-1:1 + re-VLM + tail-iz-sejnega-zapisa) — deterministična-reprodukcija (vzorec-P156!)",
        "NOVA-LEKCIJA-#12-potrjena: VLM-marginalni-ordinali-sistemsko-zanesljivi-SAMO-v-3/8-cifrah (s157-7→6-obeh-sej!) — KROP-margin-strip-OBVEZEN!",
        "NOVA-LEKCIJA-#13: PRINTED-page-številke = poceni-×5-preslikava-dokaz (vsak-sken!)",
        "NOVA-LEKCIJA-#14: VLM-bolezen-raw-syllables ('Gulmenzindung'/'Gichtarmzündung') = boljši-forenzik-kot-VLM-interpretacija — KROP-konec-crkva-odloča ('-entzündung'-umlaut!)",
        "NOVA-LEKCIJA-#15: RE-READ = neodvisni-2.-viri — soglasja-povišajo-[?]-v-fakt (tail-83/84/85! 97J! z28-DUP!) — nesoglasja-zahtevajo-arbitražni-crop (×5!)",
        "z28-DUPLIKAT + P196-z8-DUPLIKAT = vzorec-pisarjev-dup (ne-skip!) — 04106-številčenje-forenzika-3-anomalije-v-3-letih!",
        "SANACIJA-POTEK: /tmp-wipe + muzej-pobrisan → re-clone-@195b4e1 → vse-faze-reproducirane (fetch-1:1 + VLM-×7 + KROP-iz-conversation + tail-iz-sejnega-zapisa) — 0-izgubljenih-dokazov!",
    ],
}

OUT.parent.mkdir(parents=True, exist_ok=True)
json.dump(proof, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"PROOF-OK: {OUT}")
print(f"vpisov={len(ENT)} griblje={len(grib)} hise={hise} h×2={hx2}")
print(f"najst={najst[0]}J-z{najst[1]['zap']} najml={najml[0]}J-z{najml[1]['zap']}")
print(f"spol={dict(spol_c)} friseln={fr_total}")
print(f"meseci={dict(sorted(Counter(e['mesec_no'] for e in ENT if e['mesec_no']).items()))}")
