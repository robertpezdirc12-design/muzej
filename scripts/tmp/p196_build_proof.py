#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P196 — dokaz-gradilnik: parish-death-1881-04106.json (93 vpisov = z1–z92 + z8-DUPLIKAT)."""
import json, re, os

VLM = "/tmp/p196/vlm-page"
OUT = "/home/z/muzej/research/issue17/parish-death-1881-04106.json"
STRANI = [("s171",165),("s172",166),("s173",167),("s174",168),("s175",169),
          ("s176",170),("s177",171),("s178",172),("s179",173)]

Z = re.compile(r"^(Maria|Anna|Margaretha|Barbara|Katharina|Theresia|Elisabeth|Agnes|Ursula|Jožefa|Josefa|Juliana|Magdalena)", re.I)
M = re.compile(r"^(Johann|Johannes|Michael|Matthias|Mathias|Josef|Joseph|Georg|Franz|Martin|Nikolaus|Nikolaj|Anton|Andreas|Jakob|Peter|Paul|Simon|Thomas|Valentin|Wolfgang|Adam|Karl|Leopold|Julius|Aloys)", re.I)

def spol(ime):
    if not ime: return None
    if Z.match(ime): return "Ž"
    if M.match(ime): return "M"
    return None

# ——— KURATOR-FORENZIČNE KOREKCIJE (avtoriteta: parish.ts P196-bloki + header-komentar) ———
KOR = {
    ("s171","1"): dict(ime="Ursula Movrin [~ne-Jure! repo-forenzika]", hisna="15", starost="90 [~ne-70! Kurrent-9/7-zmeda]", bolezen="Abzehrung [~ne-Asthma! — restart-z1-1881!]"),
    ("s171","2"): dict(ime="Margaretha REAF [~Reaß?]", stan="'Brig-zy-honn' [~stan-glif]", starost="59 [~ne-56! VLM-zavrnitev]", bolezen="Lungen-mantz-bündung-glifa [~Lungenentzündung?]", duhovnik="Franz Jančar 'v.R.C.-Pfarrer'"),
    ("s171","8"): dict(vas="Geršiče [~]", ime="Janez Toprič [~]", stan="½ gütl.bes-Ehe? [~]", starost="½ Jahr [~ne-2-leti! VLM-zavrnitev]", duhovnik="Franz Dovgan"),
    ("s172","8"): dict(vas="Griblje", hisna="4", ime="Anna BRINE [~Brinc? — VLM-'Božinec'-ZAVRŽEN!]", stan="'Alt-bannsin' [~stan-glif]", starost="63", bolezen="Maffpüffl-glifa [★★★ M/W-NIT-1/4! ~Masern-pustl?]", duhovnik="Franz Jančar"),
    ("s172","9"): dict(vas="Prilozje [VLM-'Griblje-h30'-ZAVRŽEN!]", ime="Martha [~] (priimek-neprebran [~])"),
    ("s172","15"): dict(hisna="56", ime="Maria ŠIMEC", stan="'Aul-wirtin' [~stan-glif]", starost="56", bolezen="Asthma", duhovnik="Franz Jančar"),
    ("s173","29"): dict(hisna="37", ime="Matthias HLINAR jun. [~Hliunar-glif]", stan="'nachl.-Defron'-glif [~]", starost="1", bolezen="Frisern [★★★ FRISELN-1/3-1881!]", duhovnik="Franz Jančar 'v.H.O.-Priester'"),
    ("s174","30"): dict(hisna="37", ime="Anna HUDIČ", stan="'Interša' [~stan-glif]", starost="31", bolezen="an der Lähmung [~paraliza!]", duhovnik="Franz Jančar 'v.R.C.-Pfarrer'"),
    ("s174","33"): dict(ime="Anna TIMEC", stan="⅔ Güblann's-wittbe [~migrant-glif!]", starost="33", bolezen="[Schlafsucht? ~Sl-ff-glif]", duhovnik="Franz Jančar 'v.R.C.-Pfarrer'"),
    ("s174","35"): dict(hisna="44", ime="Katharina HAMBIČ [~Hamzić?]", stan="'Lind-wirtin' [~stan-glif]", starost="35", bolezen="[Schlachon? ~glif]", duhovnik="Franz Jančar 'v.R.C.-Pfarrer'"),
    ("s175","47"): dict(ime="Barbara OŽOLT [~Ožbolt?]", stan="⅔ Güblann's-wittbe [~migrant-glif!]", starost="50", bolezen="Asthma", duhovnik="Franz Jančar (podpis)"),
    ("s176","51"): dict(hisna="8", ime="Barbara BRINC [~Princ?]", stan="⅔ Güblann's-wirthin [~migrant-glif!]", starost="8 mesecev", bolezen="[Krämpfe? ~Brüpe-glif — FRISELN-sorodna!]", duhovnik="Franz Jančar"),
    ("s176","54"): dict(hisna="66", ime="Matthias KRIŽAN [~Hrižan? — V/K-glif]", stan="'Magzinjter' [~stan-glif — ista-kot-z1-Movrin!]", starost="¾ let [~]", bolezen="Blasensucht [~Blasp-fucht-glif]", duhovnik="Franz Jančar"),
    ("s177","60"): dict(hisna="78", ime="Anna LOŽAR", stan="Gärtners-tochter [~vrtičkarjeva-hči!]", starost="1", bolezen="Maspenn-glifa [★★★ M/W-NIT-2/4! ~Masern?]", duhovnik="Franz Jančar 'v.R.C.-Priester'"),
    ("s178","77"): dict(ime="Josef KMECL", stan="⅔ Gült. [~gütl.bes-glif]", starost="6¼ let [~ne-6½!]", bolezen="[Schlarme? ~glif]", duhovnik="Franz Jančar 'v.R.C.-Priester'"),
    ("s178","78"): dict(ime="Johann PÖGL [~Pögek?]", stan="Lanns-Kind [~glif]", starost="[blede — odsek]", bolezen="Entzündung-glifa [~Binözfpfiung]", duhovnik="Franz Jančar 'v.H.C.-Priester'"),
    ("s178","79"): dict(ime="Katharina TOMINC", stan="Müllers-wittwe [~mlinarjeva-vdova — MÜHLZÜGLER-ženska-nit!]", starost="71", bolezen="[Abzehrung? ~Abz-glif]", duhovnik="Franz Jančar 'v.H.C.-Priester'"),
    ("s178","80"): dict(ime="Michael JANOPIRČ [~Janopitsch?]", stan="⅔ Gültler-sohn [~glif]", starost="19", bolezen="Entzündung-glifa", duhovnik="Franz Jančar 'v.H.C.-Priester'"),
    ("s179","82"): dict(ime="Maria HLEBČAR [~Hlebec?]", stan="⅔ Güblanns-wirthin? [~migrant-glif]", starost="31", bolezen="Brünnow-glifa [~Bräune? — DAVICA-sorodna!]", duhovnik="Franz Jančar 'v.R.C.-Priester'"),
    ("s179","85"): dict(ime="Margaretha MILEK", stan="'Anzüglannsin' [~stan-glif]", starost="71 [~ne-91! VLM-zavrnitev]", bolezen="Altersschwäche [dolgi-ſ-ligatura!]", duhovnik="Franz Jančar 'v.H.C.-Priester'"),
    ("s179","86"): dict(ime="Barbara PRINC", stan="Lanns-wirtin [~glif] + (Lanič?-nadpis [~])", starost="61", bolezen="Asthma", duhovnik="Franz Jančar (podpis)"),
    ("s179","89"): dict(ime="Maria HLEBEC", stan="⅔ Gribljann's-tochter [~migrant-glif!]", starost="27", bolezen="Lungenentzündung", duhovnik="Franz Jančar 'v.H.C.-Priester'"),
}
# GRIBLJE-bloki: (skan, z) → houseNo v parish.ts
BLOKI = {("s171","2"):"17", ("s172","8"):"4", ("s172","15"):"56", ("s173","29"):"37",
         ("s174","30"):"37", ("s174","33"):"18", ("s174","35"):"44", ("s175","47"):"21",
         ("s176","51"):"8", ("s176","54"):"66", ("s177","60"):"78", ("s178","77"):"31",
         ("s178","78"):"21", ("s178","79"):"60", ("s178","80"):"13", ("s179","82"):"48",
         ("s179","85"):"65", ("s179","86"):"26", ("s179","89"):"2"}

entries = []
for skan, pag in STRANI:
    d = json.load(open(f"{VLM}/{skan}.json", encoding="utf-8"))
    for r in d.get("vrstice", []):
        zp = r.get("zaporedna")
        if zp is None or zp == "[?]":  # MEJA-marker-vrstica (s171) + fantomski-[?]-vrstica (s172)
            continue
        if zp == "72" and skan == "s171":  # tail-1880 — NI-vpis-1881 (→ P197-lead!)
            continue
        ime0 = r.get("ime") or ""
        vas0 = r.get("vas") or ""
        e = {
            "skan": skan, "pag": pag,
            "zaporedna": zp if (skan, zp) != ("s172", "8") else "8-dup",
            "mesec": r.get("mesec"), "smrt": r.get("smrt"), "pokop": r.get("pokop"),
            "vas": vas0, "hisna": r.get("hisna"), "ime": ime0,
            "stan": r.get("stan"), "starost": r.get("starost"), "bolezen": r.get("bolezen"),
            "previden": "/", "duhovnik": r.get("duhovnik"),
            "spol": spol(ime0), "griblje": False, "blok_v_parish": False,
            "leto": 1881, "opomba": None,
        }
        k = (skan, zp)
        if k in KOR:
            e.update(KOR[k])
            e["spol"] = spol(e["ime"]) or e["spol"]
        if k in BLOKI:
            e["griblje"] = True
            e["blok_v_parish"] = True
            e["hisna"] = BLOKI[k]
        e["griblje"] = "Griblje" in (e["vas"] or "") and "ZAVRŽEN" not in (e["vas"] or "")
        entries.append(e)

assert len(entries) == 93, f"vpisov={len(entries)} (pričakovano 93)"
grib = [e for e in entries if e["blok_v_parish"]]
assert len(grib) == 19 and len({e["hisna"] for e in grib}) == 17

d = json.load(open("/home/z/muzej/research/issue17/parish-death-1882-04106.json", encoding="utf-8"))

def starost_leta(s):
    """Pretvori starost-v-leta (float) — podpira: '76', '10 tednov', '5 mesecev', '¾ let', '½ Jahr', '8 mesecev'."""
    if not s: return None
    t = str(s)
    m = re.match(r"^\s*(\d+)\s*¼", t)  # 6¼ → 6.25
    if m: return float(m.group(1)) + 0.25
    m = re.match(r"^\s*(\d+)\s*½", t)  # 6½ → 6.5
    if m: return float(m.group(1)) + 0.5
    m = re.match(r"^\s*(\d+)\s*¾", t)  # ¾ → 0.75
    if m: return float(m.group(1)) + 0.75
    if re.match(r"^\s*¾", t): return 0.75
    if re.match(r"^\s*3\s*/\s*4\b", t): return 0.75
    if re.match(r"^\s*½\b", t): return 0.5
    m = re.match(r"^\s*(\d+)\s*tedn", t)  # tednov/tedne → tedni/52
    if m: return int(m.group(1)) / 52.0
    m = re.match(r"^\s*(\d+)\s*mese[cč]", t)  # mesecev/mesecov → meseci/12
    if m: return int(m.group(1)) / 12.0
    m = re.match(r"^\s*(\d+)", t)
    return float(m.group(1)) if m else None

odrasli = [(starost_leta(e["starost"]), e) for e in entries if starost_leta(e["starost"] or "") and starost_leta(e["starost"]) >= 20]
najst = max(odrasli, key=lambda x: x[0]) if odrasli else (None, None)
otroci = [(starost_leta(e["starost"]), e) for e in entries if starost_leta(e["starost"] or "") is not None]
najml = min([x for x in otroci if x[0] is not None], key=lambda x: x[0]) if otroci else (None, None)
moski = sum(1 for e in entries if e["spol"] == "M")
zenske = sum(1 for e in entries if e["spol"] == "Ž")

# nove-hiše: Griblje-hiše-1881, ki-NE-obstajajo-v-04106-blokih-1882–1885
src = open("/home/z/muzej/src/data/atlas/parish.ts", encoding="utf-8").read()
novejse_hise = set(re.findall(r'houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*(?:188[2-5])', src))
nove_1881 = sorted({e["hisna"] for e in grib} - novejse_hise, key=int)

proof = {
  "faza": "P196",
  "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1881 = 5/29 (issue #18)",
  "knjiga": d["knjiga"],
  "entries": entries,
  "okvir": {
    "leto_1881": "z1 = Jänner 3./5. (s171-po-MEJI; Certoviše-Ursula-Movrin-h15-90J-Abzehrung [repo-forenzika — VLM-'Jure-70J-Asthma'-zavrnjeno!]); velika-rokopisna-oznaka-'18/81'-čez-prazno-vrstico",
    "meja_1880_81": "s171 (tail-1880-z72-Jože-Valčič-Vranoviče + '/81'-velika-črta + restart-z1 = 35.-POTRDITEV-invariante + P194-tehnika-#9-ponovitev!)",
    "meja_1881_82": "s180-top (ŽE-P195: '1882.'-glava-desno + 'Jänner' + 'Anno-Domini' + restart-z1 = 34.-POTRDITEV!)",
    "konec_1881": "s179-z92-December-29/31 (Krasinec-h24-Marija-Starovinič-27J)",
    "zaporedna": "z1–z92 (92 vpisanih vrstic) + z8-DUPLIKAT (s171-z8-Geršiče-Toprič ≠ s172-z8-Griblje-BRINE = 2-različna-vpisa-ISTA-številka = 5.×-linija!) = 93 vpisov",
    "forma": "nemška-tiskana-'Sterb-Buch'-skroz (slovenska-šele-1885-s205/s206-P192!)",
    "skeni": "s171–s179 (9 skenov; Pag. 165–173 = sken − 6!) + s180-top-probe (meja-1881/82)",
    "preštevanje": "pag == sken − 6: s171-165 + s172-166 + s173-167-IZPISANO + s174-168 + s175-169 + s176-170 + s177-171 + s178-172 + s179-173 (17.–21.-potrditev-preslikave; margini-165/166/167/172/173-vizualno!)"
  },
  "statistika": {
    "vpisane_vrstice": 92,
    "vpisov_skupaj": 93,
    "griblje_vpisov": 19,
    "griblje_hise": 17,
    "griblje_hise_x2": 2,
    "male": moski, "female": zenske,
    "najstarejsa": f"{najst[0]} J — {najst[1]['ime']} ({najst[1]['vas']} h{najst[1]['hisna']}, {najst[1]['mesec']})" if najst[1] else None,
    "najmlajsa": f"{najml[0]} — {najml[1]['ime']} ({najml[1]['vas']} h{najml[1]['hisna']})" if najml[1] else None,
    "nove_hise_04106": nove_1881
  },
  "anomalije": [
    "★★★ MEJA-1880/81-s171: tail-z72-Jože-Valčič?-Vranoviče-h14-Wassersucht?-F.Jančar + velika-rokopisna-'18/81'-čez-prazno-vrstico + restart-z1 = 35.-POTRDITEV-invariante (pag==sken−6 dopolnjena-do-21.-potrditev)!",
    "★★★ z8-DUPLIKAT-ŠTEVILČENJA-5.×-linija: s171-z8-Geršiče-Janez-Toprič-½J-F.Dovgan ≠ s172-z8-Griblje-h4-Anna-BRINE-63J-F.Jančar (cf. 1921-s218 + 1904-s253 + 1885-z4 + 1882-z33!)",
    "★★★ MEJA-1881/82-s180-top ŽE-P195-potrjena ('1882.'-glava + 'Jänner' + Anno-Domini + restart-z1) — 1881-konec = s179-z92-31.12.-Krasinec!",
    "★★★ s177-'1881'-letnica-glava-SEPTEMBER-brez-restarta (številčenje-nadaljuje-z60!) — srednjeletna-glava-REDKOST (cf. restart-obvezno-ob-MEJI!)",
    "★★★ NOVA-ULEDBA-#10: MESEC-SPREMEMBA-V-VRSTICI (z80: smrt-29-November → pokop-'Dezember-1'-izpisan-z-mesecom — meja-pada-ZNOTRAJ-vrstice! cf. s172-z18-Feb/März-24/25!)",
    "★★★ h37-KATASTROFA-×2-V-2-DNEH: z29-Matthias-HLINAR-jun.-1J (18./19.-4.) + z30-Anna-HUDIČ-31J (19./21.-4.) — NASLEDNJI-DAN! (cf. h1-ZELŠKO-×2-1882-P195 + h1-DAVICA-1885-P192!)",
    "★★★ HLEBEC-DVOJNICA-×2-v-2-tednih: z82-h48-Maria-HLEBČAR-31J (7./9.-12.) + z89-h2-Maria-HLEBEC-27J (22./24.-12.) (cf. h44-HLEBUČAR-veriga-1883-P194→BRINEC-1901!)",
    "★★★ BRINC/PRINC-DVOJNICA-×2: z51-h8-dojenček-8-MESECEV-avgust + z86-h26-61-J-december (babica-vnuček?-hipoteza [~]!)",
    "★★★ h21-×2-1881: z47-Barbara-OŽOLT-50J-julij + z78-Johann-PÖGL-november!",
    "★★★ M/W-NIT-×4-1881: z8-Maffpüffl-h4-63J + z60-Maspenn-h78-1J + z69/z70-Prilozje-63J-×2 [~Masern-pustl?-hipoteza — cf. P195-Waſſerſucht-dolgi-ſ-rešitev!]",
    "★★★ FRISELN-×3-1881: z29-Griblje-h37-1J + z34-Prilozje-17J + z84-Dobravce-1J — cf. FRISELN-FLOOD-×16-1882-P195 = EPIDEMIJA-RAST-NAZAJ!",
    "★★★ ANGINA-1.×-PREDZGODOVINE: z81-Gradac-h32-Katharina-Svec?-2J (latinsko-modro-črnilo! cf. DAVICA-'Angina'-×2-1882-P195-nit!)",
    "★★★ TUBERCULOSE-1.×-PREDZGODOVINE: z90-Gradac-h1-Julius-Köhler-35J-Gasthaus-wirth (latinsko!)",
    "★★★ ŠIMEC-MREŽA-h56-1881: Maria-56J-Asthma (VLM-'h36'-ZAVRŽEN! → h54-×2 + h55-1882-P195!)",
    "★★★ LOZAR-NIT-h78: Anna-Ložar-Gärtners-tochter-1J (P195-nit: Legan→Funkl→Lozar→LOZAR-1883!)",
    "★★★ TOMINC-h60: Katharina-Müllers-wittwe-71J (MÜHLZÜGLER-ženska-forma-nit! cf. P195-z58-Peclir!)",
    "★★★ MILEK-NIT-h65: Margaretha-71J-Altersschwäche (cf. h65-1882-P195 + z46-Zemelj-Maria-Milek-1881!)",
    "★★★ MIGRANTI-Gribljančani-'⅔-Güblann'-glif-×7 (z33-wittbe + z47-wittbe + z51-wirthin + z82-wirthin? + z89-tochter + z78-Kind + cf.) — diaspora-dokumentirana!",
    "s172-fantomski-[?]-vrstica-#13 (vse-polja-[?]) — IZKLJUČENA-iz-93-vpisov-dokumentirana!",
    "VLM-leto-zavrnitve: s175-'1887' + s176-'1887' + s178-'[~1870-1871]' — KURRENT-8/7+8/0-ZMEDA — korigirano-na-1881-prek-zaporedne-kontinuitete-z40–z80 (ne-vizualno!)",
    "s172-TAIL-polje-VLM-zmeda ('tail-prejšnjega-leta' — dejansko-Jänner-1881-nadaljevanje!) — korigirano",
    "h66 = NOVA-GRIBLJE-hiša-1881 (VLM-'h6e'-ZAVRŽEN!) + KRIŽAN-nit (cf. 1920-KRIŽAN-P186!)",
    "h13-JANOPIRČ-19J (→ JAKOFČIČ-1882-P195-nit!) + h44-HAMBIČ [~Hamzić?] (→ HLEBUČAR-1883-P194-z73-veriga!)"
  ],
  "duhovniki": {
    "Jančar-dominanta": "Franz-JANČAR-19/19-GRIBLJE = 100%-DOMINANTA (3.-leto-zapored: 1881-×19/19 → 1882-~25+/59-P195 → 1883-dominanta-P194!); title-varijante: 'v.R.C.-Pfarrer' + 'v.H.O.-Priester' + 'v.H.C.-Priester' + podpis",
    "Dovgan": "Franz-DOVGAN-×~10-IZKLJUČNO-ne-Griblje (Prilozje/Krasinec/Zemelj/Dobravce!)",
    "opomba": "'Prieſter'-Kurrent-ligatura-ULEDBA (VLM-'Pircber'-napačna-branja-RAZREŠENA — dolgi-ſ+in-2.-lekcija! cf. P195-Waſſerſucht!)"
  },
  "epidemija": {
    "Friseln": "×3-1881 (z29-h37-1J + z34-Prilozje-17J + z84-Dobravce-1J) → FRISELN-FLOOD-×16-1882-P195 = EPIDEMIJA-RAST! + z51-'Brüpe'-glif-[Krämpfe?-sorodno!]",
    "M/W-nit": "×4-1881 (z8-Maffpüffl + z60-Maspenn + z69 + z70) [~Masern-pustl? — cf. P195-dolgi-ſ-forenzika!]",
    "Angina": "1.×-PREDZGODOVINE (z81-Gradac-2J-latinsko-modro-črnilo!) → DAVICA-'Angina'-×2-1882-P195-nit!",
    "Tuberculose": "1.×-PREDZGODOVINE (z90-Gradac-35J-Gasthaus-wirth-latinsko!) → ×9-1882-P195!",
    "Asthma-nit": "×3-1881 (z15-h56-56J + z47-h21-50J + z86-h26-61J!) → ×3-1882-P195 → ×3-1883-P194 = ASTHMA-3-LETNICA!",
    "Wassersucht": "tail-1880-z72-Valčič (s171-top — leto-1880 → P197!)"
  },
  "hišne_kontinuitete": [
    "h17-GRIBLJE: REAF-59J-z2 (1.-vpis-1881-po-MEJI! cf. 1882-z1-Pozdire-P195!)",
    "h4-GRIBLJE: BRINE-63J-z8-dup (BRINC/PRINC-dvojnica!) → JAKOFČIČ-1882-P195-h8-nit-sorodstvo [~]",
    "h56-GRIBLJE: ŠIMEC-56J-z15 (VLM-'h36'-ZAVRŽEN!) → ŠIMEC-MREŽA-h54/h55-1882-P195!",
    "h37-GRIBLJE: HLINAR-jun.-1J-z29 + HUDIČ-31J-z30 = KATASTROFA-×2-V-2-DNEH → DAVICA-1883-P194-z70-nit!",
    "h18-GRIBLJE: TIMEC-33J-z33 (datum-razkol-9-vs-4 [~]!)",
    "h44-GRIBLJE: HAMBIČ-35J-z35 → HLEBUČAR-1883-P194-z73 → Klobučar-1884 → BRINEC-1901-veriga!",
    "h21-GRIBLJE: OŽOLT-50J-z47 + PÖGL-z78 = ×2-1881!",
    "h8-GRIBLJE: BRINC-dojenček-8M-z51 → JAKOFČIČ-1882-P195-nit!",
    "h66-GRIBLJE: KRIŽAN-¾J-z54 = NOVA-HIŠA-1881 (VLM-'h6e'-ZAVRŽEN! cf. 1920-KRIŽAN-P186!)",
    "h78-GRIBLJE: LOŽAR-1J-z60 → LOZAR-1883-nit (P195: Legan→Funkl→Lozar→LOZAR!)",
    "h31-GRIBLJE: KMECL-6¼J-z77 (cf. KMECL-nit?)",
    "h60-GRIBLJE: TOMINC-71J-z79 (MÜHLZÜGLER-ženska-forma! cf. P195-h60-nit!)",
    "h13-GRIBLJE: JANOPIRČ-19J-z80 (→ JAKOFČIČ-1882-P195! cf. h13-Kusič-1885-P192!)",
    "h48-GRIBLJE: HLEBČAR-31J-z82 (HLEBEC-DVOJNICA-1/2!)",
    "h65-GRIBLJE: MILEK-71J-z85 (→ h65-1882-P195! cf. 1922-MILEK-h68!)",
    "h26-GRIBLJE: PRINC-61J-z86 (BRINC/PRINC-DVOJNICA-2/2!)",
    "h2-GRIBLJE: HLEBEC-27J-z89 (HLEBEC-DVOJNICA-2/2 — zadnji-Griblje-vpis-1881!)"
  ],
  "forme": [
    "nemška-tiskana-'Sterb-Buch'-skroz (slovenska-šele-1885-s205/s206-P192!)",
    "'Germ.'-ZEMELJ-vas-forma (P194-'Germ'-×3 + P195-×2-potrditev!)",
    "M/W-stan-glifi-družina (Maffpüffl/Maspenn/Mumpfpüffl — GLIFA-forenzika-×4!)",
    "'⅔-Güblann'-migrant-glif-×7 — Griblje-diaspora-v-sosednjih-vasih!",
    "mesec-izpisan-v-pokopnem-stolpcu-ob-meji-znotraj-vrstice (z80-'Dezember-1' — NOVA-ULEDBA-#10!)"
  ],
  "crossChecks": [
    "pag == sken − 6: s171-165 + s172-166 + s173-167 (IZPISANO-v-markerji!) + s174-168 + s175-169 + s176-170 + s177-171 + s178-172 + s179-173 = 17.–21.-potrditev-preslikave!",
    "MEJA-1880/81-s171 = 35.-POTRDITEV-invariante (restart-z1!)",
    "MEJA-1881/82-s180-top = 34.-POTRDITEV (ŽE-P195!) — ista-vrstica-deluje-kot-konec-1881!",
    "z-numeracija-kontinuiteta: z1–z92-brez-presetk (z8-dup = edini-izjemni!)",
    "s174-glava-'1881'+'April'-VIZUALNO-potrjena (h37-z30-blok!)",
    "s177-glava-'1881'-VIZUALNO-potrjena (h78-z60-blok!) — september-brez-restarta",
    "z8-DUPLIKAT-cf.: 1921-s218 + 1904-s253 + 1885-z4 + 1882-z33 = 5.×-linija!",
    "19-blokov-parish.ts == 19-Griblje-vpisov == 17-hiš (h37-×2 + h21-×2) — statistika-konsistentna!"
  ],
  "honesty": {
    "H1": "74-ne-Griblje-vpisov = RAW-VLM-branje-brez-kurator-crops (19-Griblje = forenzično-korigirani!) — kakovostna-asimetrija-dokumentirana!",
    "H2": "VLM-zavrnitve-×9-dokumentirane (z8-'Božinec'→BRINE! + z9-'Griblje-h30'→PRILOZJE! + z70-'Griblje-h26'→PRILOZJE! + z74-'Griblje-h21'→PRILOZJE! + z54-'h6e'→h66! + z15-'h36'→h56! + z85-'91-let'→71! + s171-z8-'2-leti'→½-Jahr! + z2-'56'→59-J!) + DODATNA-restart-z1-korekcija (VLM-'Jure-Movrin-70J-Asthma' → repo-forenzika-'Ursula-Movrin-h15-90J-Abzehrung' — Kurrent-J/U + 9/7 + bolezen-glif!)",
    "H3": "z33-datum-VLM/crop-razkol (9-vs-4-Maj [~]) — OBE-branja-dokumentirani!",
    "H4": "VLM-leto-branja-zavrnjene-×3 (s175/s176-'1887' + s178-'[~1870-1871]') — korekcija-prek-številčne-kontinuitete-NE-vizualno!",
    "H5": "tail-1880-z72-branje-negotovo ('Jože-Valiča(?)' + 'Bažigar(?)/Obžigobar(?)' + 'Wasser(?)-glif') — pripada-P197-1880!",
    "H6": "s172-fantomski-[?]-vrstica-#13-izključena (vse-polja-[?] — ne-je-vrstica!)",
    "H7": "stan-glifi-neberljivi-z[~]: 'Brig-zy-honn' (z2) + 'Alt-bannsin' (z8) + 'Aul-wirtin' (z15) + 'nachl.-Defron' (z29) + 'Interša' (z30) + 'Lind-wirtin' (z35) + 'Magzinjter' (z54) + 'Anzüglannsin' (z85) + 'Lanns-wirtin/Kind' (z78/z86)",
    "H8": "starosti-specijalni-glifi: '¾-let' (z54) + '6¼-let' (z77) + '½-Jahr' (s171-z8) + '[blede-odsek]' (z78) — dokumentirani!",
    "H9": "z29-starost-'1'[~7?]-Kurrent-zmeda (HLINAR-jun.-1J — h37-KATASTROFA-odvisna!) — [~]-dokumentirano!",
    "H10": "s177-'1881'-glava-SEPTEMBER-brez-restarta = REDKOST — vseeno-ni-meja (le-srednjeletna-glava)!",
    "H11": "duhovnik-title-varijante (v.R.C.-Pfarrer / v.H.O.-Priester / v.H.C.-Priester) — Kurrent-H/O/R-zmeda-[~]-dokumentirana!",
    "H12": "M/W-nit-hipoteza-[~Masern-pustl?]-NE-potrjena — samo-glif-družina-dokumentirana (cf. P195-Waſſerſucht-forenzika-rešitev)!"
  },
  "kaskada": {
    "vitals": "1283 → 1472 (+19 blokov 04106-1881!)",
    "04106": "64 → 83 (16×-1885 + 21×-1884 + 11×-1883 + 16×-1882 + 19×-1881!)",
    "04894": "520-NESPREMENJENO",
    "p80": "94-NESPREMENJENO",
    "korpus": "93-NESPREMENJEN",
    "pt_luknja": "18-NESPREMENJENA (h50-izven-vzorca-42–60-brez-h50-1881!)",
    "qa": "qa-p196 = 196.-kontrola + qa-p195-števec-1283→1472-sanacija (counting-upgrade!)"
  },
  "lead": {
    "P197": "mrliška 04106, leto 1880 (s171-top-tail-z72-ŽE-viden: Jože-Valčič?-Vranoviče-h14-72J?-Wassersucht?-F.Jančar → 1880-konec = z72 → 1880 = s164?–s171 + probe-s164/165 [hipoteza-z-nazaj-štetjem ~72-vrstic!])",
    "krstna": "04104-1871–1885-×200-skenov-čaka (vzporedno!)",
    "poročna": "04455-zacetek-1873–1885-čaka"
  },
  "notes": [
    "Nastalo: P196 (2026-11-03) — VLM-branje ×9 (p196_read_page.mjs; s175-gateway-EOF-prekinitev-OBNOVLJENA — vse-9-JSON-na-disku!) + kurator-vizualna-forenzika ×19-Griblje-blokov (parish.ts) + MEJA/TAIL-markerji (s171 + s179!)",
    "VLM-uspešnost: 9/9-strani-JSON-ok; ampak-3-leto-zavrnitve (1887/1887/1870-71) + ×9-vpis-zavrnitev — korekcije-v-KOR-mapi-dokumentirane!",
    "pag == sken − 6 potrdjen-vseh-9-straneh (s173-IZPISANO-'167'!)",
    "z8-DUPLIKAT = 5.×-linija (cf. 1921 + 1904 + 1885 + 1882) — ISTA-številka-2-različna-vpisa!",
    "ANGINA + TUBERCULOSE = 1.×-PREDZGODOVINE (oba-latinsko-črnilo!)",
    "ASTHMA-nit-sedaj-3-letnica: ×3-1881 → ×3-1882 → ×3-1883!",
    "viri: Matricula-04106-s171–s179"
  ]
}

json.dump(proof, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK zapisano {OUT}")
print(f"vpisov={len(entries)} griblje={len(grib)} hiš={len({e['hisna'] for e in grib})} M={moski} Ž={zenske}")
print(f"najstarejša: {proof['statistika']['najstarejsa']}")
print(f"najmlajša: {proof['statistika']['najmlajsa']}")
print(f"nove hiše 1881: {nove_1881}")
