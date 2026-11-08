#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — zgradi research/issue17/parish-death-1885-04106.json iz VLM-JSON + kuratorskih korekcij."""
import json, glob, re

# 1) preberi VLM-page JSON
vlm = {}
for f in sorted(glob.glob('/tmp/p192/vlm-page/s*.json')):
    d = json.load(open(f))
    vlm[d['skan']] = d

# 2) kuratorske korekcije (T2 forenzika — crops + Read-oči)
KOREKCIJE = {
    ("s199", "4"): {"vas": "Griblje", "hisna": "1", "ime": "Matthias Dragot", "stan": "½ gütl.besitzer",
        "starost": "10 mesecev", "bolezen": "Difteribis [~difteritis = davica!]", "duhovnik": "And. Glibe[l] [~Gleibe] coöp",
        "opomba": "z4-DUPLIKAT-VSTAVEK (pisar izpustil → vstavil s št. 4! duplikat z z4-Krasinec-Husič!) + hišno-ime 'Dragot'[~]-annotacija v vas-celici"},
    ("s199", "12"): {"vas": "Griblje", "hisna": "31", "ime": "Martin Župarič[~Duprič]", "stan": "Wagner- in gütl.besitzer[~]",
        "starost": "3 LETA (VLM '3 dni' ZAVRŽEN — max-zoom '3-Jahren'!)", "bolezen": "[~neberljivo ~Rubeolis/Masernike? = rdečke?]", "duhovnik": "And. Glibe[l] coöp", "opomba": None},
    ("s200", "24"): {"vas": "Griblje", "hisna": "62", "ime": "Maria Hrijan[~Hojan/Prijan/Križan?]", "stan": "[~neberljiv ~gospodinja/svekrova?]",
        "starost": "60", "bolezen": "Asthma", "duhovnik": "And. Glibe[l] coöp",
        "opomba": "h62 = KURE-hiša-1924 (P190-z30) → verjetno Kure-svečerva[~] roj. Hrijan"},
    ("s201", "26"): {"vas": "Griblje", "hisna": "31", "ime": "Maria Papič[~Paprič]", "stan": "gütl.bes.? ... hči[~]",
        "starost": "25", "bolezen": "Masernkrämpfen [~rdečke-zapleti! max-zoom M-a-s-e-r-n jasno]", "duhovnik": "And. Glibe[l] coöp", "opomba": "h31-PAPIČ-KATASTROFA-1/3"},
    ("s201", "29"): {"vas": "Griblje", "hisna": "31", "ime": "Maria Papič[~]", "stan": "... hči[?]",
        "starost": "19", "bolezen": "Frais [~Fraisen = otroški krči]", "duhovnik": "And. Glibe[l] coöp",
        "opomba": "h31-KATASTROFA-2/3 — sestra?[~] 3 dni po z26"},
    ("s202", "39"): {"vas": "Griblje", "hisna": "31 (kurator: NE '4'-VLM! Nr-celica '31' identično glifom z26/z29 @×3.4!)",
        "ime": "Anna Papič (kurator: VLM 'Pajer' ZAVRŽEN)", "stan": "Mw.[vdova] + gütl.besitz.-frau[~]",
        "starost": "'1½ Monate' [STAROST-NESKLADJE — vdova-gospodarica! ~71-J?]", "bolezen": "Frais[en]",
        "duhovnik": "And. Glibe[l] coöp", "opomba": "h31-KATASTROFA-3/3 = mati-vdova — mesec po hčerkah!"},
    ("s202", "43"): {"vas": "Griblje", "hisna": "78", "ime": "Maria Stubler[~]", "stan": "gütl.besitzerin",
        "starost": "87", "bolezen": "Asthma", "duhovnik": "And. Glibe[l] coöp",
        "opomba": "NAJSTAREJŠA-1885 + h78 = LOZAR-hiša (1903/1924) → Lozar-mati[~]?"},
    ("s203", "60"): {"vas": "Griblje", "hisna": "5", "ime": "Peter Brgum[~Dragun?]", "stan": "½ gütl.besitzer",
        "starost": "1 leto", "bolezen": "Abzehrung [= sušica]", "duhovnik": "And. Glibe[l] coöp",
        "opomba": "glava 'Jahr 18' NEPOPOLNA-1.×"},
    ("s203", "61"): {"vas": "Griblje", "hisna": "13", "ime": "Barbara Kusič[~Kusic]", "stan": "Abbenarin-Milchb[~]",
        "starost": "58", "bolezen": "Sušica[~ 'Suširinng']", "duhovnik": "Andreas Glibe[l] coöp (FULL-FORM!)",
        "opomba": "h13 = JAKOFČIČ-hiša → verjetno žena/mati roj. Kusič[~]"},
    ("s204", "64"): {"vas": "Griblje", "hisna": "54", "ime": "Maria Simec (VLM 'Limer' ZAVRŽEN)", "stan": "½ gütl.besit. und Wirths-frau[~]",
        "starost": "24", "bolezen": "Abzehrung[~]", "duhovnik": "And. Glibe[l] coöp",
        "opomba": "DUAL-NUMBERING-START (črnilo 64 + svinčnik 65!) + SIMEC-mreža"},
    ("s204", "66"): {"vas": "Griblje", "hisna": "63", "ime": "Johann Križan (VLM 'Prigožan' ZAVRŽEN — K/P-Kurrent!)",
        "stan": "½ gütl.besitzer", "starost": "4 mesece", "bolezen": "Wümmanen[~ ~Wundrose?]",
        "duhovnik": "Franz Dovgan[~Dorgun — = poročna-1886 ISTI!]", "opomba": "h63 = KRIŽAN-hiša-pred-04894!"},
    ("s204", "68"): {"vas": "Griblje", "hisna": "21", "ime": "Janez Požek (VLM 'Peček' ZAVRŽEN — 'Požeh'-glif!)",
        "stan": "[~neberljiv ~'Wagner-?']", "starost": "64", "bolezen": "Magenkrämpfe[~]", "duhovnik": "Franz Dovgan[~]",
        "opomba": "h21 = POŽEK-hiša-pred-04894 (1887-Matija!)"},
    ("s205", "77"): {"vas": "Griblje", "hisna": "9", "ime": "Maria Jakofčič (VLM 'Valdbeič' ZAVRŽEN)", "stan": "Wirtin[~Wirtshaus-bes.?]",
        "starost": "69", "bolezen": "Abzehrung [= sušica — VLM 'Magenleiden' ZAVRŽEN]", "duhovnik": "And. Glibe[l] coöp",
        "opomba": "h9 = JAKOFČIČ-hiša-pred-04894 + s205 HIBRID-forma + glava 'Jahr 18' 2.×"},
    ("s206", "83"): {"vas": "Griblje", "hisna": "58", "ime": "Janez Požek (VLM 'Pegan' ZAVRŽEN)", "stan": "½ gütl.besitzer",
        "starost": "3 mesece", "bolezen": "Gliste [= gliste — 1. slovenska forma!]", "duhovnik": "And. Glibe[l] coöp",
        "opomba": "h58 = POŽEK-hiša (1887-Anton!) — POŽEK-×2-v-1885 + SPREMEMBA-FORME (slovenska!) + prečrtan-z81-nad"},
    ("s206", "84"): {"vas": "Griblje", "hisna": "68", "ime": "Ana Alth[~Alrh]", "stan": "'Nemeška-hi'[? ~hišno-ime/hči?]",
        "starost": "6 tednov[~]", "bolezen": "Božjast[~božnik]", "duhovnik": "And. Glibe[l] coöp",
        "opomba": "h68 = MLEK-hiša-1924 — kontinuiteta-39-let"},
    ("s206", "89"): {"vas": "Griblje", "hisna": "63", "ime": "Katarina Hrovatič[~]", "stan": "[~najemna?-žena-omožena-?]",
        "starost": "31", "bolezen": "sušica (slovensko!)", "duhovnik": "And. Glibe[l] coöp",
        "opomba": "2. h63-vpis-1885 (po z66-otoku!) → verjetno Križan-žena roj. Hrovatič[~]"},
}

GRIBLJE_KEYS = [("s199","4"),("s199","12"),("s200","24"),("s201","26"),("s201","29"),
                ("s202","39"),("s202","43"),("s203","60"),("s203","61"),("s204","64"),
                ("s204","66"),("s204","68"),("s205","77"),("s206","83"),("s206","84"),("s206","89")]

entries = []
for skan in sorted(vlm, key=lambda s: int(s[1:])):
    d = vlm[skan]
    for r in (d.get('vrstice') or []):
        zap = str(r.get('zaporedna') or '').strip().rstrip('.')
        if not zap:
            continue
        key = (skan, zap)
        griblje = bool(re.search(r'gribl', (r.get('vas') or ''), re.I))
        if key in KOREKCIJE and 'Griblje' in KOREKCIJE[key]['vas']:
            griblje = True  # kuratorska-korekcija-vas (VLM-zmede z4/z77!)
        e = {
            "skan": skan, "pag": int(skan[1:]) - 6, "zaporedna": zap,
            "mesec": r.get('mesec'), "smrt": r.get('smrt'), "pokop": r.get('pokop'),
            "vas": r.get('vas'), "hisna": r.get('hisna'), "ime": r.get('ime'),
            "stan": r.get('stan'), "starost": r.get('starost'), "bolezen": r.get('bolezen'),
            "previden": r.get('previden'), "duhovnik": r.get('duhovnik'),
            "griblje": griblje, "blok_v_parish": False,
        }
        if key in KOREKCIJE:
            k = KOREKCIJE[key]
            for f in ("vas","hisna","ime","stan","starost","bolezen","duhovnik","opomba"):
                if k.get(f): e[f] = k[f]
            e["kurator_korekcija"] = True
            if griblje: e["blok_v_parish"] = True
        entries.append(e)

# kontekst: meja 1884-vrstice na s198 (zap 69–76) so v entries z griblje-flag — z71/z76 griblje ampak 1884!
for e in entries:
    if e["skan"] == "s198" and e["griblje"]:
        e["leto_1884_kontekst"] = True
        e["blok_v_parish"] = False
        e["opomba"] = "MEJA-KONTEKST: dec-1884 (z71-Agnes-Jalenšič-h8 + z76-Nikolaus-Huzič-h10) — NE-blok-1885!"

grib = [e for e in entries if e["blok_v_parish"]]
assert len(grib) == 16, f"Griblje-bloki {len(grib)} ≠ 16!"

dokaz = {
    "faza": "P192",
    "tema": "MRLIŠKA PREDHODNICA 04106, leto 1885 — 1. leto predzgodovinske linije (Griblje-vpisov)",
    "knjiga": {"signature": "04106", "vrsta": "death", "obdobje": "1857–1885", "skeni": 208,
               "url": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"},
    "okvir": {"skani": "s198–s207", "pag": "192–201", "preslikava": "pag == sken − 6",
              "zaporedna": "z1–z93 (črnilo; svinčnik-preštevanje = 93 veljavnih!)",
              "meja_1884_85": "s198-mid ('Jänner anno, 1885.' zapisano čez vas+ime + restart z1!) — 31. potrditev invariante",
              "konec_knjige": "s207-z92/93 († 28./30. december 1885) + s208 platnica 'PODZEMELJ / M / 1857–1885'"},
    "statistika": {"vpisov_1885": 93, "griblje": 16, "ne_griblje": len([e for e in entries if e['griblje'] and not e['blok_v_parish'] and not e.get('leto_1884_kontekst')]),
                   "kontekst_1884": 2, "prebrani_skeni": 11, "blokov_v_parish": 16,
                   "gostota": "16/93 = 17.2% (pod 04894-povprečjem ~19%)"},
    "anomalije": [
        "A1: GLAVE 'Jahr 18' NEPOPOLNE ×2 (s203 + s205 — pisar pustil letnico nedokončano!)",
        "A2: PREČRTAN VNOS s203-z62 (Podzemelj Maria Pogliačnik[~] — X čez desni del + 'Za folgo den Erklärung'[~]!)",
        "A3: PREČRTAN VNOS s206-z81 (Gemišče 46 Mathias Padina[~] — X čez celo vrstico!)",
        "A4: DUAL NUMBERING s204–s207 (črnilo-št. + svinčnik-preštevanje off-by-one — svinčnik = veljavne vrstice, preskoči prečrtane!)",
        "A5: z4-DUPLIKAT-VSTAVEK (Dragot †5./6. jan vstavljen s št. 4 = duplikat z z4-Husič — 3.× linije cf. 1921-s218 + 1904-s253!)",
        "A6: z39 STAROST-NESKLADJE ('1½ Monate' za vdovo-gospodarico! ~71-J Kurrent-zmeda ali pisar-napaka)",
        "A7: SPREMEMBA FORME MID-BOOK (nemška s198–s204 → hibrid s205 → slovenska s206–s207 'Mrtvaška knjiga'!)",
        "A8: s203-z53 PRAZEN starost+vzrok (Mathias Kumpes, Knecht, Krapišče 9 — Mai 5./6.)",
        "A9: COMPOUND-VAS ×2 ('Certoviše od Griblje № 10' z40 + 'Otok od Gemihe № 3' z44)",
        "A10: VLM-zavrnitve ×6 (Pajer→Papič + h4→h31 + Peček→Požek + Pegan→Požek + Valdbeič→Jakofčič + Prigožan→Križan) + '3-dni'→3-LETA (z12)",
        "A11: MASERN/DAVICA-EPIDEMIJA Nov 1884–Mär 1885 (Difteribis[~davica!] + ~Rubeolis? + Masernkrämpfen + ~Masernika? + Fraisen-kopica)",
        "A12: neberljiva priimka ×2 dokumentirana (Hrijan[~Hojan/Prijan/Križan?] + Brgum[~Dragun?])",
    ],
    "duhovniki": {
        "Glibe[l]": {"forma": "And. Glibe[l] [~Gleibe] coöp — DOMINANTA ×13/16 Griblje + Andreas-FULL-FORM (z61!)",
                     "seam": "= P153-1887 'Andrej Glibel' (parish.ts-442!) — ISTI duhovnik čez šiv knjig 04106→04894!"},
        "Dovgan": {"forma": "Franz Dovgan [~Dorgun] ×2 (z66 + z68)",
                   "seam": "= poročna-1886 'franz Dovgan' (parish.ts-6095 vpis-2!) — ISTI!"},
    },
    "hišne_kontinuitete": {
        "h9": "1885-Maria-Jakofčič[~] → 1922-P188-z31-JAKOFČIČ-posestnica-h9 (37 let!)",
        "h13": "1885-Barbara-Kusič[~] → P189-z13-Matija-JAKOFČIČ-h13 (38 let! verjetno žena/mati roj. Kusič)",
        "h21": "1885-Janez-POŽEK-64-l → P153-r55-Matija-POŽEK-h21-1887 (2 leti!)",
        "h31": "1885-PAPIČ-×4 → 1886-poroka-Martin-Papič-h31 + krstna-Joana-PAPIČ-h31 (družina-epidemično-uničena → nasledstvo!)",
        "h58": "1885-Janez-POŽEK-3-mes → P153-r66-Anton-POŽEK-h58-1887 (2 leti!)",
        "h62": "1885-Maria-Hrijan[~] → P190-z30-Jožef-KURE-h62-1924 (39 let! verjetno svečerva)",
        "h63": "1885-KRIŽAN-×2 (otok-4-mes + žena-31!) → krstna-1892-oče-Jurij-h63 + poročna-1911-№1-h63 (družina-preživela-epidemijo!)",
        "h68": "1885-Ana-ALTH[~] → P190-z24-Jožefa-MLEK-h68-1924 (39 let! menjava-družine)",
        "h78": "1885-Maria-STUBLER[~]-87-l → P190-z45-Julij-LOZAR-h78-1924 (39 let! verjetno Lozar-mati)",
    },
    "epidemija": {"obdobje": "Nov 1884 – Mär 1885", "vzroki": ["Difteribis [~difteritis = davica!] (z4dup-10-mes)",
                  "[~Rubeolis/Masernike? = rdečke?] (z12-3-l)", "Masernkrämpfen (z26-25-l)",
                  "Frais[en] (z29-19-l + z39-vdova)", "[~Masernika?] (1885-z1-1-l-Gradec!)", "[~Rubeolis?] (1884-z69-2-l-Certoviše!)"],
                  "h31_katastrofa": "mati-vdova-Anna + hčerki-Maria-25+19 = 3-smrti-v-enem-mesecu!"},
    "forme": {"s198–s204": "nemška tiskana ('Sterb-Register' / 'Krankheit und Todesart' / 'Hat die Sterbsakramente empfangen')",
              "s205": "HIBRID (nemška-levo + slovenska-desno 'knjiga.' / 'Bolezen ali vzrok smrti' / 'Previden (a) ali ne')",
              "s206–s207": "polno slovenska ('Mrtvaška knjiga' / 'Bivališče mrličevo' / 'Podpis duhovna pokopovalca')"},
    "crossChecks": [
        "CC1: meja-1884/85 (s198 'Jänner anno, 1885.' + restart z1) — zapisano čez dva stolpca = nedvoumno",
        "CC2: s199-z4dup '4' vs s198-z4-'Krasinec-Husič' — dve vrstici št. 4 → duplikat-dokumentiran",
        "CC3: dual-numbering svinčnik 62–93 = 93 − (prečrtana-2) ✓ aritmetika",
        "CC4: glava-s199 'Jahr 1885' jasna (@a199-crop) — s200/s201-glave garble-VLM (1883/1855) ZAVRŽENE — kontinuiteta-zaporedna-razrešuje",
        "CC5: zaporedna-kontinuiteta z1–z93 prek 11 skenov (s198-bot–s207) — brez prelomov razen dokumentiranih duplikatov",
        "CC6: P153-podpis 'Andrej Glibel' (parish.ts-442) == 04106-'And. Gleibe coöp' — glif-kontinuiteta duhovnika",
        "CC7: poroka-1886-vpis-2 'franz Dovgan' (parish.ts-6095) == 04106-'Franz Dorgun' — glif-kontinuiteta",
        "CC8: h21/h58-POŽEK-glif-identična-priimka (P153-r55/r66 + z68/z83-@max-zoom)",
    ],
    "honesty": [
        "H1: priimek z24 'Hrijan' — 4 kandidati [~Hojan/Hrijan/Prijan/Križan?] — neodločljivo @×4.2 — dokumentirano-kakršno-je",
        "H2: priimek z60 'Brgum' — [~Dragun?] — Kurrent-B/D-zmeda — neodločljivo",
        "H3: starost z39 '1½ Monate' — fizično nemogoče za vdovo-gospodarico — verjetno '71-J' ali pisar-napaka — ZAPISANO-KAKRŠNO-JE",
        "H4: bolezen z12 — neberljiva — [~Rubeolis/Masernike?] — hipoteza-rdečke iz epidemije-konteksta",
        "H5: bolezen z66 'Wümmanen' — [~Wundrose?] — špekulativno",
        "H6: starost z84 '6 tednov' — enota-neberljiva ('6-J-lott') — tednov[~]",
        "H7: stan-z26/z29/z39 — končnica '-hi/-hü' — hči[?]/hiša[?] — dvoumno",
        "H8: vas-z4dup 'Griblje + (Drago?)' — hišno-ime-annotacija[~] — ne zagotovo-2.-vas",
        "H9: s203-z62-precrtan-razrok — 'Za folgo den Erklärung'[~] — neberljivo",
        "H10: Kusič vs Kužič vs Kusić — 'Kusič[~]'",
        "H11: svinčnik-preštevanje-intepretacija ('veljavne-vrstice') — logična-ne-dokazana-mehanika",
        "H12: 1884-kontekst-vrstici (z71/z76) v evidence z flagom, NE-v-parish.ts",
    ],
    "kaskada": {"vitals": "1219 → 1235 (+16)", "04106": "0 → 16", "04894": "520 nespremenjeno",
                "p80": "94 nespremenjeno", "korpus": "93 nespremenjeno", "PT_luknja": "18 nespremenjena",
                "qa": "qa-p192 = 192. kontrola", "stale": "40 skript (p80 + p153–p191) VITALS_TOTAL 1219→1235"},
    "lead": {"P193": "mrliška-04106-leto-1884 (s195–s198-pred! zap.-1884-z69–z76-že-videni + s193/s194-probe-potrebni — 2. leto predzgodovine: 28/29!) + vzporedno krstna-04104-1871–1885 (200 skenov!) čaka",
             "linija": "predzgodovina-mrliška-1/29-let (1885 → 1857!)"},
    "entries": entries,
    "notes": "VLM-vhod: /tmp/p192/vlm-page/s198–s208.json (11 skenov; s208 = platnica). Kurator-crops: /tmp/p192/crops2–crops6 (33 + celice). Meja: s198-mid. Vsa-neskladja-dokumentirana-v-honesty.",
}

out = "research/issue17/parish-death-1885-04106.json"
json.dump(dokaz, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{out}: entries={len(entries)} griblje={len(grib)} anomalije={len(dokaz['anomalije'])}")
