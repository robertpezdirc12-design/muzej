#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P197 — build proof JSON: research/issue17/parish-death-1880-04106.json
(Zrcaljenje P196-strukture: faza/tema/knjiga/okvir/statistika/anomalije/
duhovniki/epidemija/hišne_kontinuitete/forme/crossChecks/honesty/kaskada/
lead/entries/notes — VSA forenzika te seje!)"""
import json, re
from collections import Counter
from pathlib import Path

RAW = json.load(open("/tmp/p197/entries_raw.json"))
ENT = RAW["entries"]
TAIL = RAW["tail_1879"]
OUT = Path("/home/z/muzej/research/issue17/parish-death-1880-04106.json")

# ——— starost-parser (P196-vzorec) ———
def starost_j(mala):
    if not mala:
        return None
    s = str(mala).lower()
    m = re.search(r"(\d+)\s*(?:¾|\.75)?", s)
    if not m:
        return None
    n = float(m.group(1))
    if "¾" in s or ".75" in s:
        n += 0.75 if float(m.group(1)) == n else 0
    if "¾" in s and re.search(r"1\s*¾", s):
        n = 1.75
    if "mesec" in s or "monat" in s:
        return round(n / 12, 3)
    if "teden" in s or "woche" in s:
        return round(n / 52, 3)
    if "tednov" in s:
        return round(n / 52, 3)
    if " dan" in s or "tage" in s:
        return round(n / 365, 3)
    if "ura" in s or "minut" in s:
        return 0.001
    return n

# ——— spol-hevristika (ime-based; honesty-flag!) ———
Z_IME = ["maria", "anna", "ana ", "katharina", "catharina", "margaretha", "theresia",
         "elisabeth", "agnes", "barbara", "ursula", "lucia", "johanna", "magdalena",
         "vdova", "hči", "hcer", "dohtar", "chter", "tochter", "žena", "egovina",
         "služkinja", "magd", "-in ", "jarina", "mati"]
M_IME = ["johannes", "joannes", "johann", "janez", "georg", "joseph", "josef", "jožef",
         "mathias", "matthias", "matevž", "michael", "mich.", "nicolaus", "miklavž",
         "jakob", "peter", "vinzenz", "rudolf", "andreas", "anton", "felix", "julius",
         "ignatius", "simon", "martin", "jernej", "lenart", "urban", "franz", "fran ",
         "sine", "sin ", "moš", "vdovec", "otrok"]


def spol(ime, stan):
    t = f"{ime or ''} {stan or ''}".lower()
    for k in Z_IME:
        if k in t:
            return "Z"
    for k in M_IME:
        if k in t:
            return "M"
    return "?"


grib = [e for e in ENT if e["vas"] and "gribl" in e["vas"].lower()]
hise = sorted({int(re.match(r"\d+", str(e["hisna"])).group()) for e in grib if e["hisna"] and re.match(r"\d+", str(e["hisna"]))})
hx2 = []
hc = Counter(int(re.match(r"\d+", str(e["hisna"])).group()) for e in grib if e["hisna"] and re.match(r"\d+", str(e["hisna"])))
for h, c in sorted(hc.items()):
    if c > 1:
        zx = [f"z{e['zap']}-{e['ime'].split()[0] if e['ime'] else '?'}-{e['mesec']}" for e in grib if str(e["hisna"]).startswith(str(h))]
        hx2.append(f"h{h} (×{c}: {' + '.join(zx)}!)")

starosti = [(starost_j(e["starost"]), e) for e in ENT]
with_s = [x for x in starosti if x[0] is not None]
najst = max(with_s, key=lambda x: x[0])
najml = min(with_s, key=lambda x: x[0])
spol_c = Counter(spol(e["ime"], e["stan"]) for e in ENT)

def zstr(e):
    return f"z{e['zap']}-{e['vas']}-h{e['hisna']}-{e['starost']}"

# ——— bolezni-skupine ———
def b_group(b):
    b = (b or "").lower()
    if any(k in b for k in ["fraisen", "friesen", "frisen", "kravipen", "krup"]):
        return "FRISELN-družina"
    if "masch" in b:
        return "MASERN-glif"
    return (b.split() or ["?"])[0].rstrip('.,')

bg = Counter(b_group(e["bolezen"]) for e in ENT)
fr_total = sum(v for k, v in bg.items() if "FRISELN" in k or "MASERN" in k)

proof = {
    "faza": "P197",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1880 = 6/29 (issue #18)",
    "knjiga": {
        "signature": "04106",
        "obdobje": "1857–1885",
        "zupnija": "Podzemelj (Nadškofijski arhiv Ljubljana)",
        "vrsni": "matricula-online.eu",
        "vir": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
    },
    "okvir": {
        "leto_1880": "71-vsebinskih-vpisov (z1–z72 z z55-IZPUŠČENO!) — P196-lead-napoved-'71'-EXAKT-MATCH!",
        "meja_1879_80": "s164 mid-page velika-'1880'-črta = SPLIT-ČEZ-RAZPON ('1 8'-L | '8 0'-R KROP-POTRJENO!) = 36.-POTRDITEV-invariante (P196-'18/81'-35. + P195-34. + ...) + P194-TEHNIKA-#9-ponovitev! + restart-63→1 (rdeči-margin-KROP: 62,63,1,2,3,4,5,6,7!) — 1879 = 63-vpisov!",
        "meja_1880_81": "s171-tail + '18/81'-SPLIT (= P196-35.-potrditev-reuse!) — 1880-konec = z72",
        "konec_1880": "z72-Dezember-Vranoviče-h14-Jože-Valčič-72J-Wassersucht (P196-KROP-POTRJENO: 72-ne-92-γ-7!)",
        "zaporedna": "z1–z72 z ★ z55-IZPUŠČENO-ŠTEVILKO (s169-rdeči-margin-KROP: 53,54,56,57,58,59,60,61,62 — pisar-preskok! cf. P196-z8-DUPLIKAT-5.×-linije = 2. številčna-anomalija-04106!)",
        "forma": "nemška-tiskana-'Sterb-Buch'-razprt (dvostanski-čez-gutter!) + rdeči-ročni-margini-ordinali (KROP-berljivi!) + mesečne-glave-v-vrstici (August@z53 + September@z56 + November@z63!)",
        "skeni": "s164–s171 (Pag. 158–165 = sken − 6; md5-validirano-s171-inventar-208 + Pag.158/159/163/164-VIZUALNO-KROP!)",
        "preštevanje": "s164 z1–z7 → s165 z8–z18 → s166 z19–z30 → s167 z31–z41 → s168 z42–z52 → s169 z53,z54,z56–z62(z55-preskok!) → s170 z63–z71 → s171-tail z72 = 71-vsebinskih ✓ (VLM-protislovje-'53–61'-vs-'53–62' → KROP-leva-cela-REŠITEV: 55-prazna!)",
    },
    "statistika": {
        "vpisane_vrstice": len(ENT),
        "griblje_vpisov": len(grib),
        "griblje_hise": hise,
        "griblje_hise_x2": hx2,
        "najstarejsa": f"{zstr(najst[1])} — {najst[0]}-let [{najst[1]['starost']}]",
        "najmlajsa": f"{zstr(najml[1])} — {najml[0]}-let [{najml[1]['starost']}]",
        "male": spol_c.get("M", 0),
        "female": spol_c.get("Z", 0),
        "spol_neopredeljen": spol_c.get("?", 0),
        "bolezni_skupine": dict(bg.most_common()),
        "meseci": dict(sorted(Counter(e["mesec_no"] for e in ENT if e["mesec_no"]).items())),
    },
    "anomalije": [
        "★★★ MEJA-1879/80-s164: velika-'1880'-črta-SPLIT-ČEZ-RAZPON ('1 8'-levo | '8 0'-desno — KROP-POTRJENO!) = 36.-POTRDITEV-invariante + P194-TEHNIKA-#9-ponovitev (s171-'18/81'-35. + s180-'18/82'-34.!) + RESTART-63→1 (rdeči-margini-62,63,1–7-KROP!)",
        "★★★ z55-IZPUŠČENA-ŠTEVILKA: s169-rdeči-margini-53,54,56–62 (KROP-leva-cela!) — pisar-preskok = 2. številčna-anomalija-04106 (cf. P196-z8-DUPLIKAT-5.×!) — VLM-sam-protisloven ('53–61'-lista + '53–62'-tail-tekst!)",
        "★★★ VLM-LETO-MISREAD-×2: '1859'(s165) + '1839'(s170) = KURRENT-8-dvojna-zanka-zmeda — KROP-glavi-'1880 Feber' + '1880 Novobr' POTRJENI! (3. KURRENT-cifra-lekcija-seje)",
        f"★★★ FRISELN-EPIDEMIJA-1880: ×{fr_total}-družina (FRAISEN-10 + FRIESEN-6 + FRISEN-2 + KRUP/KRAVIPEN-4 + Kopfraisen/gichtern-...) = {round(100 * fr_total / len(ENT))}%-vpisov! KRIVULJA: 1880-×{fr_total} → 1881-×3-DOLINA → 1882-×16-FLOOD (P195) = W-krivulja-epidemije (otroška — večina-<4J!)",
        "★★★ JANČAR-NASLOVNI-NARAŠČAJ-1880: 'coop.'(Jan) → 'v. kaplan'(März) → 'v.R.D./VRD Priester'(Aug/Okt) — naraščajoči-hierarhija + GRIBLJE-12/13-Jančar-91% (cf. 1881-19/19-100%-DOMINANTA-3.-leto!) — JANČAR-nit-4.-leto!",
        "★★ Dovgan-z10-GRIBLJE-IZJEMA (Katharina-Knuel-pokop-18.2.) — cf. 1881-DOVGAN-izključno-ne-Griblje → 1880-lahko-Dovgan-Griblje = vloga-vmes!",
        "★★ ŠIMEC/TIMEC-DVOJNICA-nit: z19-Anna-Simec-Vdova-h39[~29] + z66-Anna-Simec-Kindsmagd-h18 (KROP-'S'-začetnica!) + 1881-h18-TIMEC-P196 (VLM-zavrnitev-'Timec'-za-z19!) — cf. BRINC/PRINC-dvojnica-P196!",
        "★★ PEZDIREC-nit: z54-Georg-Pozdirec-Krasinec + z58-Ana-Pezdirc-Griblje-h42 (cf. P195-1882-z1-Pozdire + P171-PEZDIREC-era-h20!)",
        "★★ h10-×2-1880 (z2-Anna-Huore-Jan + z57-Nicolaus-Kere-Sept) — cf. P196-h21-×2 + h37-×2-KATASTROFA!",
        "★★ MESEC-SPREMEMBA-V-VRSTICI (ULEDBA-#10-instance): z63-tail1879-Jakofčič-smrt-31.12.1879→pokop-'Jänner-1'-1880! (cf. P196-z80 + z73 + z68 + z18 = 5.-instance!)",
        "★ z1-IME-NEGOTOVOST: 'Peter-Staravinič'[~Karavanič/Maravanič-VLM] — 'St'-ligatura-KROP [~ostaja!]",
        "★ h39[~29]-3/9-KURRENT-zmeda (z19-Anna-Simec — KROP-dvoumna!)",
        "★ Tuberculose-×2-1880 (z6-Jablonovič-20J-Jan + P196-1881-z90-Köhler-1.×-linije-nadaljevanje!)",
        "★ Gehirnentzündung-×2-1880 (z4-42J + z61-5J-rudolf-Toma — cf. 1881-×2-nit!)",
    ],
    "duhovniki": {
        "Jančar-dominanta": "GRIBLJE-12/13 (92%) — z2,z3,z4-coop. + z19,z22-v.kaplan + z52-z58-VRD + z65,z66-WRD — NASLOVNI-NARAŠČAJ-1880 = hierarhija-v-realnem-času! (1881-19/19-100% + 1882-P195-dominanta!) 4.-leto-nit!",
        "Dovgan": "z10-Kuncelj-GRIBLJE-pokop (IZJEMA!) + večina-ne-Griblje-vpisov (z7,z62,z63-tail...) — cf. 1881-izključno-ne-Griblje = 1880-meja-vloge!",
        "Prieſter-ligatura": "'VRD/WRD-Priester' + 'coor./coop.'-forme — KURRENT-ſ-nit (P195-rešitev-reuse!)",
        "opomba": "Jančar-'Janežal'-glifa-×3 (s169 — KURRENT-j/ž!) = isti-duhovnik [~]",
    },
    "epidemija": {
        "Friseln": f"×{fr_total}-skupina (FRAISEN-10 + FRIESEN-6 + FRISEN-2 + KRUP/KRAVIPEN-4 + ...)! W-KRIVULJA: 1880-×{fr_total} → 1881-×3 → 1882-×16! (OTROŠKA-EPIDEMIJA!)",
        "M/W-NIT": "×3 (Mascherfräufel-×2 + z29-Maschukrankt-79J-Gradec [~Mascharenkrankheit=MASERN!] — cf. P196-Maffpüffl/Maspenn-×4-1881-[~Masern-pustl?]!)",
        "Abzehrung": "×6 (cf. 1881-nit!)",
        "Asthma": "×6 (cf. 1882-×3 + 1883-×3!)",
        "Gehirnentzündung": "×2 (z4 + z61!)",
        "Tuberculose": "×2 (z6-Jan-20J — 2. leto-po-P196-1.×!)",
        "Wassersucht": "×1 (z72-KROP-POTRJENO!)",
        "Altersschwäche": "×2 (obe-70J: z10 + z65!)",
    },
    "hišne_kontinuitete": [
        "h2-GRIBLJE: z56-Anna-Klepec-1880 → HLEBEC-1881-P196-z89 → HLEBČAR-h48-DVOJNICA! (h2-nit-3.-vpis!)",
        "h8-GRIBLJE: z3-Mich.-Krian-otrok-1880 → BRINC-1881-P196-z51 (h8-nit!) — cf. KLOBUČAR-h47-z52-1880 → P193-KLOBUČAR-1884-h44-veriga!",
        "h10-×2-1880: z2-Huore-Jan + z57-Kere-Sept (dve-družini-ena-št.? cf. P196-h36-dve-družini-04105!)",
        "h18-GRIBLJE: z66-Anna-Simec-1880 → TIMEC-1881-P196 = ŠIMEC/TIMEC-DVOJNICA-nit!",
        "h21-GRIBLJE: z4-Mathias-Novak-1880 → 1881-×2-P196 (Ožolt + Pögl!) — h21-hot-spot!",
        "h22-GRIBLJE: z53-Georg-Mihelič-17J-1880 (nov-dokaz!)",
        "h27-GRIBLJE: z65-Jakob-Hukar-70J-1880 (cf. h27-1885/84? preveriti-ko-P198-nazaj!)",
        "h42-GRIBLJE: z58-Ana-Pezdirc-otrok-1880 → PEZDIREC-nit (cf. P195-1882-z1 + P171-era!)",
        "h39[~29]-GRIBLJE: z19-Anna-Simec-Vdova-1880 (3/9-zmeda-dokumentirana!)",
        "h47-GRIBLJE: z52-Johann-Klobučar-11M-1880 → KLOBUČAR-priimek-nit (P193-1884!)",
        "h5-GRIBLJE: z10-Katharina-Knuel[~Kuncelj]-70J-1880 (nov-dokaz!)",
        "h20-GRIBLJE: z22-Fabian-Grabrian-3½J-1880 (cf. P171-Katarina-PEZDIREC-h20-1906-04894!)",
    ],
    "forme": [
        "nemška-tiskana-'Sterb-Buch'-skroz (slovenska-šele-1885-s205/s206-P192!)",
        "RADEČI-MARGINI-ORDINALI = NOVA-FORENZIČNA-SLOJ (KROP-berljivi: 62,63,1–7-s164 + 53,54,56–62-s169 + 63–71-s170!) — VLM-jih-ne-vidi → KROP-OBVEZEN!",
        "MEJA-marker-v-PRAZNI-vrsti (s164-'1880'-split + s171-'18/81'-split) = invarianta (36.+35.-potrditev!)",
        "mesečne-glave-z-notranjim-letom ('1880 Feber'@s165-top + '1880 August'@z53 + 'September'@z56 + '1880 Novobr'@z63) — letnica-v-glavi-2.×-potrjena!",
        "pog-pogostitve: '¼/½-Götbl'-stan-glifi = GÜTLER-sloj (mikro-kmetije!) — cf. 1825-PT-atlas!",
    ],
    "crossChecks": [
        "pag=sken−6: Pag.158(s164) + Pag.159(s165) + Pag.163(s169) + Pag.164(s170) VIZUALNO-KROP ✓ (16.–19.-potrditev-preslikave!)",
        "md5-s171.jpg == P196-s171.jpg (inventar-208-slik; idx=sken−1!)",
        "restart-63→1: rdeči-margini-KROP (62,63,1,2,3,4,5,6,7-s164!) ✓",
        "z-continuity-×8-strani: 7→18→30→41→52→62→71→72 ✓ (brez-restarta-z-notranjost!)",
        "z72-s171-tail == P196-tail-anchor ✓ (Valčič-Vranoviče-72J-Wassersucht-KROP!)",
        "1879-konec = z63 (s163-z50–61 + s164-z62–z63-tail!) — P198-LEAD-SIDRO!",
        "meseci-sklenjeni: Januar-7 → Dezember-1 (brez-luknje; Juli-×6-matcher-popravek!) ✓",
        "letnica-×4-viri: 2-leto-glavi-KROP (s165 + s170) + 2-MEJA-split (s164 + s171) ✓",
        "s169-'53–61'-VLM-protislovje-'53–62'-tail → rdeči-margin-KROP-REŠITEV (55-prazna!) ✓",
    ],
    "honesty": {
        "H1": "VLM-branja-×8-fresh (s163–s170) + P196-s171-reuse-za-z72 — isti-scan/inventar (md5!)",
        "H2": "KROP-izreki-×10 (agent-oči-1.7×) — PIŠČANČNI-slepi-točke: z1-ime 'Staravinič'[~Karavanič] OSTAJA-negotov!",
        "H3": "h39[~29] — 3/9-KURRENT-dvoumnost NERAZREŠENA (dokumentirana-oben!)",
        "H4": "spol = IME-HEVRISTIKA (M/Ž/?) — NI-prebrano-iz-kljukic-stolpcev! (P196-M33/Ž60-enako!)",
        "H5": "z55-PRESKOK = rdeči-margin-dokaz — VLOM-Verme-'53–61'-bio off-by-one-od-3.-vrste (dokumentirano!)",
        "H6": "tail=DA-flagi-s167/s169 = FALSE-POSITIVI (VLM-lastni-tekst: 'konec-NI-na-strani!') — dokumentirano-in-zavrnjeno!",
        "H7": "1879-tail (z62-Cvikl + z63-Jakofčič) IZKLJUČEN-iz-1880-nabora (le-dokaz-zh; P198-jih-vzame!)",
        "H8": "Juli-matcher-popravek (6-vpisov) — meseci-zdaj-sklenjeni-1→12 ✓",
        "H9": "VLM-'1859'/'1839'-misread-×2 ZAVRJENA (KROP-glavi!) — pri-prvi-branji-bi-bil-NAPAČEN-leto-okvir!",
        "H10": "ime-'Knuel[~Kuncelj]' + 'Huore[~Huoe/Thure]' + 'Krian[~Kovian]' — priimki-[~]-ostajajo (crop-1.7×-limit!)",
        "H11": "z72 = P196-s171.json-reuse (vrsta-1) — polja-nespremenjena (KROP-že-potrjen-v-P196-seji!)",
        "H12": "VLM-zap-shift-s169 (+1-od-3.-vrste) programsko-popravljen — zap_raw-ohranjen-vsak-vpis!",
        "krop_seja_2025-11-03": "10-cropov (p197_crop.mjs) + 2-polna-leva-stran — VSI-izreki-v-KROP-poljih!",
    },
    "kaskada": {
        "vitals": "1302 → 1355 (+13-blokov-04106-1880!)",
        "04106": "83 → 96 (16×-1885 + 21×-1884 + 11×-1883 + 16×-1882 + 19×-1881 + 13×-1880!)",
        "04894": "520-NESPREMENJENO",
        "p80": "94-NESPREMENJENO",
        "korpus": "93-NESPREMENJEN",
        "pt_luknja": "18-NESPREMENJENA",
        "qa": "qa-p197 = 197.-kontrola (vzorec-qa-p196!)",
    },
    "lead": {
        "P198": "mrliška 04106, leto 1879 (7/29!) — SIDRO-ŽE-KROP-POTRJENO: 1879-konec = z63-s164 (rdeči-margini-62,63!) + s163-ŽE-PREBRAN (z50–z61 = 12-vrstic + Griblje-z58-Križan-h30 + z59-Kraus-h32!) → probe: s157–s164; 1879-začetek = z1-išče-nazaj!",
        "krstna": "04104-1871–1885-×200-skenov-čaka (vzporedno!)",
        "poročna": "04455-začetek-1873–1885-čaka",
    },
    "entries": [],
    "notes": [
        "Nastalo: P197 (2025-11-03) — fetch-s163–s171 (p197_fetch.py: inventar-208 + md5-s171-validacija + preslikava-idx=sken−1!) + VLM-×8-fresh (p197_read_page.mjs) + P196-s171-reuse + KROP-×10-cropov (p197_crop.mjs — agent-oči!) + builder (p197_build_entries.py + p197_build_proof.py)",
        "METODOLOŠKE-LEKCIJE: (1) VLM-leto-misread ('1859'/'1839') — LETO-VEDNO-KROP-POTRDI (glava + MEJA + aritmetika!); (2) rdeči-margini = avtoritativni-ordinals (VLM-off-by-one-nevidno!); (3) VLM-tail-flags = navodila-za-KROP, ne-izreki; (4) ozadjski-nohup-VM-umira-med-klici → foreground-batche!",
        "Entries-71 (z1–z72, z55-prazna) — 1879-tail-z62/z63-ločeno (tail_1879-ključ!)",
        "GRIBLJE-13-vpisov/12-hiš (h10-×2) — parish.ts-bloki-vitajšnji-pd-1880-skeni!",
    ],
}

# ——— entries v P196-formatu ———
for e in ENT:
    proof["entries"].append({
        "skan": f"s{e['sken']}",
        "pag": e["pag"],
        "zaporedna": str(e["zap"]),
        "zap_raw": e.get("zap_raw"),
        "mesec": e["mesec"],
        "mesec_no": e["mesec_no"],
        "smrt": e["smrt"],
        "pokop": e["pokop"],
        "vas": e["vas"],
        "hisna": e["hisna"],
        "ime": e["ime"],
        "stan": e["stan"],
        "starost": e["starost"],
        "bolezen": e["bolezen"],
        "previden": e["previden"],
        "duhovnik": e["duhovnik"],
        "opomba": e["opomba"],
        "krop": e.get("krop"),
        "vlm_zavrnjeno": e.get("vlm_zavrnjeno") or None,
    })

OUT.write_text(json.dumps(proof, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK → {OUT}")
print(f"entries: {len(proof['entries'])} | griblje: {len(grib)} | hiše: {hise}")
print(f"spol: M{spol_c.get('M',0)}/Ž{spol_c.get('Z',0)}/?{spol_c.get('?',0)} | FRISELN-skupina: ×{fr_total}")
print(f"najstarejša: {najst[0]}J — {najst[1]['ime']} (z{najst[1]['zap']}) | najmlajša: {najml[0]}J — {najml[1]['ime']} (z{najml[1]['zap']})")
