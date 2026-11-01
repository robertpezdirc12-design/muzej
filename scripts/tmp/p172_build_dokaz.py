# -*- coding: utf-8 -*-
"""P172 — gradnja dokaza parish-death-1906.json (56 vrstic = 55 vpisov + dup-21)."""
import json

D = "/tmp/p172/vlm-page"
OUT = "/home/z/muzej/research/issue17/parish-death-1906.json"

# ——— diag-korekcije (diag + KOMPOZIT-soglasje; vir: p172_diag-Read-očmi + forensic/) ———
# (zap, sken) → popravki nad VLM-izhodom
KOR = {
    # ——— s104 ———
    ("s104", 1): {"hisna": "49", "vas": "Griblje", "ime": "Ana BRINEC",
                  "stan": "vdova, bajtarica", "starost": "66 let",
                  "bolezen": "Slabost [~ diag-'Slarost' — KURRENT-š/s; VLM-'Šarost'-ZAVRJENA!]",
                  "duhovnik": "H. Lengsfeld", "opomba": "★★★ P171-lead-POTRJEN-×3 (kompozit-'49'-jasno-NI-'19'!); BRINEC-vez: 1907-s109-z1-Anton-vdovec-ISTA-h49!"},
    ("s104", 6): {"hisna": "20", "vas": "Griblje", "ime": "Katarina PEZDIREC",
                  "stan": "možina oziškarica [~ diag-'mžidina-ožiškarica']",
                  "starost": "61 let", "bolezen": "Nadruka [~ VLM-'Nadluhec'-ZAVRJENA — kompozit-r!]",
                  "duhovnik": "H. Lengsfeld", "opomba": "★★★ P171-lead-POTRJEN + PEZDIREC-era-13-nadaljevanje (era-×12-v-5-letih!)"},
    ("s104", 2): {"ime": "Matija HRASTOVIČ? [~ diag-'Hrabaršec/Hrastbahec'; VLM-'Herbower'-zmeda]",
                  "starost": "74 let (diag; VLM-'44'!)", "bolezen": "Nadruka [~ VLM-'Nadluha']",
                  "hisna": "91"},
    ("s104", 3): {"ime": "Marko MUDROVEC [~ diag-'Mudrovec'; VLM-'Hudorovac']", "stan": "cigánov otrok [~ diag]",
                  "bolezen": "Rube [~ diag; VLM-'Ždile'-zmeda]", "starost": "2 leti"},
    ("s104", 4): {"ime": "Marija MEC [~ diag-'Mec'; VLM-'Medved'-zmeda]", "hisna": "70",
                  "bolezen": "črevna griža [~ diag]"},
    ("s104", 5): {"ime": "Marija CIMERIČ [~ diag-'Cimerič'; VLM-'Perovič'-zmeda]",
                  "starost": "78 let (diag; VLM-'73')", "bolezen": "Nadruka [~ VLM-'Nadluha']"},
    ("s104", 7): {"ime": "Marija HUGELJ [~ diag-'Hugely'; VLM-'Zugelj'-zmeda]", "starost": "71 let"},
    ("s104", 8): {"ime": "Milan KOGOVŠEK [~ diag-'Kogovšek'; VLM-'Megušar'-zmeda]",
                  "stan": "navedenjski? sin [~ diag; VLM-'nadučniška-žena'-zmeda]",
                  "starost": "4 leta? [~ diag; VLM-'8/3-[~83?]'-NEUPORABNA]", "bolezen": "zastrupitev krvi [~ diag]"},
    ("s104", 9): {"ime": "Nikolaj KOVAČ [~ diag-'Kovač']", "stan": "oženjen ½ zemljak", "bolezen": "Nadruka [~ VLM-'Nadluha']"},
    # ——— s105 ———
    ("s105", 10): {"ime": "J. KUPANIČ [~ diag-'Kupanič'; VLM-'Lešnik'-zmeda]", "stan": "¼ samostojen? sin [~ diag]",
                   "starost": "PRAZNA", "bolezen": "Marbmrojen [~ diag-'Mtorožen' = mrtvorojen!]"},
    ("s105", 11): {"ime": "J. MIHELIČ [~ diag-'Mihelič']", "stan": "samše? dekle hči [~ diag; VLM-'samka-delilna-hiša'-zmeda]",
                   "starost": "PRAZNA", "bolezen": "Marbmrajena [~ diag]"},
    ("s105", 12): {"vas": "Cerovlj [~ diag-'Certovlj'; VLM-'Hrnelj'-zmeda]", "ime": "J. JURAJEVIČ [~ diag]",
                   "stan": "bajtares sin", "starost": "PRAZNA", "bolezen": "Marbmrojen [~ diag]"},
    ("s105", 13): {"ime": "Katarina JUŽNA [~ diag-'Južna'; VLM-'Jušina'-zmeda]", "stan": "možena bajterica", "starost": "60 let"},
    ("s105", 14): {"vas": "Krupa (župnija Semič!) [~ diag-'Kruša-zmeda']", "ime": "Jurij POTOKAR [~ diag-'Potokar' — NE-Griblje!]",
                   "stan": "oženjen bajtar", "starost": "60 let", "bolezen": "Slabost [~ VLM-'Šarost']"},
    ("s105", 15): {"ime": "J. DOLKŠIŠ [~ diag-'Dolkšiš'; VLM-'Ahlešič'-zmeda]", "stan": "¼ zemljakov dela",
                   "starost": "PRAZNA", "bolezen": "Marbmrajena [~ diag]"},
    ("s105", 16): {"hisna": "44", "vas": "Griblje", "ime": "Matija ŠTRUKELJ [~ diag-'Štruelly' — KURRENT-k/l; kompozit-'Štrukelj'[~]]",
                   "stan": "oženjen oziškar [★★ VLM-'črnjen-vrtnar'-ZAVRJENA!]", "starost": "68 let",
                   "bolezen": "Pljučnica [~ diag-'Rjučnica?' — KURRENT-p/r]", "duhovnik": "H. Lengsfeld",
                   "opomba": "h44 = 2. mrliški vpis (1887 + 1906 — 19-letna-vrzela!)"},
    ("s105", 17): {"ime": "Cecilija LEVSTIK [~ diag-'Levstik']", "stan": "možena štvancarica? [~ diag-'domačica-zmeda']", "starost": "69 let"},
    ("s105", 18): {"ime": "Jurij MAROVT [~ diag-'Marovt'; VLM-'Marencič'-zmeda]", "stan": "vdovec oziškar [~ diag-'vdovec-očitnar']",
                   "starost": "67 let (diag; VLM-'81'!)", "bolezen": "Slabost [~ VLM-'Šarost']"},
    ("s105", 19): {"ime": "Božidar JANAČEK [~ diag-'Janacek'; VLM-'Jamšek'-zmeda]", "starost": "4 leta (diag; VLM-'1-leto')"},
    ("s105", 20): {"ime": "Doroteja STIBLAR [~ diag-'Stiblar'; VLM-'Štulhar'-zmeda]", "starost": "62 let"},
    ("s105", 21): {"hisna": "19", "vas": "Griblje", "ime": "Janez KRIŽE [~ diag-'Krizc/Heiže'; VLM-'Klinc'-ZAVRJENA!]",
                   "stan": "samotnega delavca sin", "starost": "1 mesec", "bolezen": "Slabost",
                   "duhovnik": "J. R. KUHINEK [#13 — NOVI DUHOVNIK — 1. mrliški podpis!]",
                   "opomba": "★★★ NOV-DUHOVNIK-KUHINEK + PISAR-DUPLIKAT-21 (zap-21-tudi-s106-z21!)"},
    # ——— s106 ———
    ("s106", 21): {"vas": "Klošter [~ diag-'Kloster']", "ime": "Neža SRAIJER [~ diag-'Sraijer'; VLM-'Lovšeger'-zmeda]",
                   "stan": "ožidina ¼ zemljakinja [~ diag]", "starost": "81 let", "bolezen": "Slabost",
                   "duhovnik": "J. R. KUHINEK [#13!]", "opomba": "PISAR-DUPLIKAT-21-2.-del (s105-z21-Maj-10!; 1.-v-liniji!)"},
    ("s106", 22): {"ime": "Marjeta JAKŠA [~ diag-'Jakša'; VLM-'Jakšič'-zmeda]", "stan": "ožidina ožiškarica", "starost": "72 let"},
    ("s106", 23): {"hisna": "39", "vas": "Griblje", "ime": "Katarina ŠIMEC [~ diag-'Šimec' + VLM-potrjena!]",
                   "stan": "vdova oziškarica", "starost": "56 let", "mesec": "Juni (diag; VLM-page-None!)",
                   "bolezen": "Vodenica [~ dropsy]", "duhovnik": "J. R. KUHINEK [#13!]",
                   "opomba": "★★★ h39 = 1. MRLIŠKI VPIS KADARKOLI (29.-PT-vez-kandidat!)"},
    ("s106", 24): {"vas": "Cerkviše [~ diag-'Ceroviše']", "ime": "Martin JURAJEVIČ [~ diag-'Jurajevič'; VLM-'Jurkošič'-zmeda]",
                   "stan": "samoski naseljenik? [~ diag-'raselnik']", "starost": "68 let (diag; VLM-'63'!)", "bolezen": "Nadruka [~ VLM-'Nadluha']"},
    ("s106", 25): {"mesec": "Juli (diag; VLM-None!)", "ime": "Marija JAKOFČIČ [~ diag-'Jakofčič']",
                   "stan": "vdova ožiškarica", "starost": "65 let", "bolezen": "Vodenica",
                   "duhovnik": "Leopold PODLOGAR, kapelan izven-župnije? [~ diag-'kap. v Črnomlju' — ★ NOV-PODPIS!]",
                   "opomba": "★ LEOPOLD-PODLOGAR-1.-podpis-v-liniji!"},
    ("s106", 26): {"mesec": "Juli (diag; VLM-None!)", "ime": "Marija JAPEC [~ diag-'Japeč'; VLM-'Tapušič'-zmeda]", "starost": "2 meseca"},
    ("s106", 27): {"ime": "Martin ŠTRAVS [~ diag-'Štravs']", "stan": "bajtares sin [~ diag; VLM-'kmetijca-sin'-zmeda]", "starost": "19 let"},
    ("s106", 28): {"mesec": "Avgust (diag; VLM-None!)", "ime": "Ana VLAŠIČ [~ diag-'Vlašič']", "starost": "71 let"},
    ("s106", 29): {"hisna": "58", "vas": "Griblje", "ime": "Matija TOŽEK [~ diag-'Toizek/Tojzek'; VLM-'Tožek'-potrjen [~]]",
                   "stan": "¼ zemljakov sin [~ diag-'1/1[?]-zmeda']", "starost": "10 mesecev",
                   "mesec": "Avgust (diag; VLM-None!)", "bolezen": "Slabost", "duhovnik": "J. R. KUHINEK [#13!]",
                   "opomba": "★★★ h58 = 8. mrliški vpis = REKORDISTKA-1906 + h58-×2-v-1-letu (z35!)"},
    ("s106", 30): {"mesec": "Avgust (diag; VLM-None!)", "ime": "Ana JAKOBIČ [~ diag-'Jakobič'; VLM-'Jakobčič'-zmeda]", "starost": "2 meseca"},
    ("s106", 31): {"mesec": "Avgust (diag; VLM-None!)", "ime": "Josifa PEZDIREC [~ diag-'Josefa-Pezdirec' — PEZDIREC!]",
                   "stan": "¼ zemljakova hči [~ diag; VLM-'1/2-kumfjakova'-zmeda]", "starost": "1 mesec",
                   "opomba": "PEZDIREC-×2-v-1906-vpisih (z6-Katarina-GRIBLJE + z31-Krasinec-ne-Griblje!)"},
    ("s106", 32): {"mesec": "September (diag)", "ime": "Anton STARŠINIČ [~ diag-'Staršinič'; VLM-'Haravtič'-zmeda]", "starost": "14 dni"},
    # ——— s107 ———
    ("s107", 33): {"vas": "Klošter [~ diag-'Klost(e)r']", "ime": "Marjina POTRNIK [~ diag-'Dotromiš'-NEBERLJIVA; VLM-'Mihajla-Potoknik'-zmeda]",
                   "stan": "vdova oziškarica [~ diag; VLM-'[~]haviča'-zmeda]", "starost": "71 let", "bolezen": "Slabost [~ VLM-'Stawost']"},
    ("s107", 34): {"hisna": "57", "vas": "Griblje", "ime": "Matija URH [~ diag-'Urh' + VLM-potrjen!]",
                   "stan": "vdovec in vrškar [~ diag-'vrškar'; VLM-'vršhar'-zmeda]", "starost": "78 let",
                   "bolezen": "Slabost [~ diag-'Stawost']", "duhovnik": "BREZ-PODPISA (z33–z36-neodpisani!)",
                   "opomba": "h57 = 4. mrliški vpis (1892 + 1894 + 1902 + 1906!) + URH-veriga"},
    ("s107", 35): {"hisna": "58", "vas": "Griblje", "ime": "Janez FOČEK [~ diag-'Foček/Sosek'; kompozit-'Foček'[~]]",
                   "stan": "oženjen ¼ zemljak", "starost": "49 let",
                   "bolezen": "Nadruka [~ VLM-'Nadluka'-ZAVRJENA — r/u-KURRENT!]", "duhovnik": "BREZ-PODPISA (z33–z36!)",
                   "opomba": "★★ h58-×2-v-1-letu-2.-del (z29-8-tednov-apart!)"},
    ("s107", 36): {"ime": "Jožef MALEŠIČ [~ diag-'Malešič'; VLM-'Malovšič'-zmeda]", "starost": "42 leta (diag; VLM-'1½-leta'!)",
                   "bolezen": "Hripa [~ diag; VLM-'Griža'-zmeda]"},
    ("s107", 37): {"vas": "Krivoglavce [~ diag-'Krivoglavce'; VLM-'Vinoglavce'-P171-ZMEDA-RECIDIV!]",
                   "ime": "Jožef KUNRČ [~ diag-'Kunrč'; VLM-'Lumic'-zmeda]", "stan": "nabolavorje? sin [~ diag-NEBERLJIVO]", "starost": "1 mesec"},
    ("s107", 38): {"ime": "Katarina DOLTAR [~ diag-'Doltar'; VLM-'Dolinar'-zmeda]",
                   "stan": "carova?...-žena [~ diag-NEBERLJIVO; VLM-'rojena-Hambič'-zmeda]", "hisna": "29",
                   "starost": "44 let", "bolezen": "Vodenica", "duhovnik": "J. FLORJANČIČ coadj. [~ diag-'Florjanc-coadj.'-zmeda]"},
    ("s107", 39): {"ime": "Katarina TONE [~ diag-'Tone'; VLM-'Tomc'-zmeda]", "starost": "3 leta", "bolezen": "Rube [~ diag; VLM-'Bele'-zmeda]"},
    ("s107", 40): {"ime": "Jožef STARK [~ diag-'Stark'; VLM-'Sterk'-zmeda]", "stan": "hvariatski? sin [~ diag]", "starost": "2 meseca"},
    ("s107", 41): {"ime": "Marija HUGELJ [~ diag-'Hugelj'; VLM-'Kugelj'-zmeda]", "hisna": "13", "starost": "6 let", "bolezen": "Davica"},
    ("s107", 42): {"ime": "Janez ULARČ [~ diag-'Ularč'; VLM-'Vlašič'-zmeda]", "stan": "¼ zemljaškova sina", "starost": "4 mesece (diag; VLM-'11-mesec'!)", "bolezen": "Davica [~ VLM-'Mrzlica']"},
    ("s107", 43): {"vas": "Ceroviše [~ diag-'Crovoviše'; VLM-'Vranoviče'-zmeda!]", "ime": "Katarina ŠTRAVC-žena [~ diag-'žena-Antona-Štravca-roj.-Plovnice'; VLM-'Žena-Črtana'-ZMEDA]",
                   "starost": "71 let", "bolezen": "Nadruka [~ VLM-'Nadluka']"},
    ("s107", 44): {"ime": "Nikolaj JERAJEVIČ [~ diag-'Jerajevič'; VLM-'Jurjevič'-zmeda]", "stan": "vdovec ¼ zemljak [~ diag-'siromak-½-zemljak'-zmeda]",
                   "starost": "63 let", "bolezen": "Marbmca? [~ diag-'Asijemca'-NEBERLJIVO]"},
    # ——— s108 ———
    ("s108", 45): {"ime": "Jožef JURAJEVIČ [~ diag-'Jurajevič'; VLM-'Zuanajevič'-zmeda]",
                   "bolezen": "~~Bazljenica-prečrtano~~ Črevesni katar [~ diag-'Grovers'-čolov'-zmeda]",
                   "opomba": "VLM-'November-1905'-HALUCINACIJA — VIZUALNO-November-1906 (glava-s108-'181906'!)"},
    ("s108", 46): {"ime": "Anton KUPANIČ [~ diag-'Kupanič'; VLM-'Župančič'-zmeda]", "mesec": "November (diag; VLM-None!)"},
    ("s108", 47): {"ime": "Matija KUPANIČ [~ diag-'Kupanič'; VLM-'Župančič'-zmeda]", "mesec": "November (diag; VLM-None!)"},
    ("s108", 48): {"hisna": "77", "vas": "Griblje", "ime": "Jurij JOČEK [★★★ VLM-'Potokar'-ZAVRJENA — diag-'Joček'+kompozit!]",
                   "stan": "oženjen bajtar [~ diag-'ostenjen-bajtar' — 'oženjen'!]", "starost": "55 let",
                   "bolezen": "Pljučnica [~ diag-'Pjučnica']", "duhovnik": "St. Florijana FLORJANČIČ cap. [~ diag-'svp'-zmeda]",
                   "opomba": "★★★ h77 = 1. MRLIŠKI VPIS KADARKOLI (3.-najvišja-mrliška-po-h91/h81!)"},
    ("s108", 49): {"ime": "Jakob POPIČ [~ diag-'Popič'; VLM-'Jofrič'-zmeda]", "starost": "68 let (diag; VLM-'83'!)", "mesec": "December (diag; VLM-None!)"},
    ("s108", 50): {"ime": "Jožef JAKŠA [~ diag-'Jakša']", "stan": "gostilov? sin [~ diag; VLM-'gostilnar'-zmeda]",
                   "bolezen": "Krčev? bronhialni katar [~ diag-'Bronkjalni-katar'-zmeda]", "mesec": "December (diag; VLM-None!)"},
    ("s108", 51): {"ime": "Jakob CAJNAR [~ diag-'Cajnar']", "stan": "oženjen oziškar [~ diag; VLM-'ostenjen-čivtkar'-zmeda]",
                   "starost": "69 let", "bolezen": "Pljučnica [~ diag-'Pjučnica']", "mesec": "December (diag; VLM-None!)"},
    ("s108", 52): {"vas": "Dobravice [~ diag-'Perkoviše'-VLM + 'Dobravice'-diag-ZMEDA — vzemim-Dobravice-[~]]",
                   "ime": "Anton LUKANIČ [~ diag-'Lukanič']", "starost": "2 meseca", "mesec": "December (diag; VLM-None!)"},
    ("s108", 53): {"ime": "J. JAGIRA [~ diag-'J. Jagira'; VLM-'J. Legina'-zmeda]", "starost": "PRAZNA!",
                   "bolezen": "Marbmjena? [~ diag-'Mtorvjena'-zmeda]", "mesec": "December (diag; VLM-None!)",
                   "opomba": "starost-PRAZNA + podpis-'———'-ČRTA (NEBERLJIVO-vzorec!)"},
    ("s108", 54): {"hisna": "18", "vas": "Griblje", "ime": "Alojzij ŠIMEC [★★★ VLM-'Timec'-ZAVRJENA — diag-'Šimec'+kompozit!]",
                   "stan": "¼ zemljakov sin", "starost": "5 mesecev", "mesec": "December (diag; VLM-None!)",
                   "bolezen": "Božjast", "duhovnik": "St. Florijana FLORJANČIČ cap. [#14?]",
                   "opomba": "★★★ h18 = 6. mrliški vpis + ZADNJA-GRIBLJE-1906 (meja-1906/07 = s109!)"},
    ("s108", 55): {"vas": "Dolnja-v-Kandlj? [~ diag; VLM-'Boginja-vas-v-Kandiji'-zmeda]",
                   "ime": "Nikolaj VARRICA [~ diag-'Varrica/Čarica'; VLM-'Uhančič'-zmeda]", "stan": "oženjen tovariš [~ diag; VLM-'družen-posestnik'-zmeda]",
                   "starost": "32 let", "bolezen": "Tuberculosis-pulm. [~ diag]", "mesec": "December (diag; VLM-None!)"},
}

SCAN_RANGE = {"s104": (1, 9), "s105": (10, 21), "s106": (21, 32), "s107": (33, 44), "s108": (45, 55)}
PAGE = {"s104": 103, "s105": 104, "s106": 105, "s107": 106, "s108": 107}
SCAN_NO = {"s104": 104, "s105": 105, "s106": 106, "s107": 107, "s108": 108}

entries = []
row = 0
for scan in ["s104", "s105", "s106", "s107", "s108"]:
    d = json.load(open(f"{D}/{scan}.json"))
    lo, hi = SCAN_RANGE[scan]
    for v in d["vrstice"]:
        try:
            z = int(str(v.get("zaporedna", "")).strip("."))
        except Exception:
            continue
        if not (lo <= z <= hi):
            continue
        if scan == "s104" and z in (61, 62):
            continue  # 1905-vrstici (P171!)
        row += 1
        kor = KOR.get((scan, z), {})
        hisna = kor.get("hisna", str(v.get("hisna", "")).strip("."))
        vas = kor.get("vas", v.get("vas", ""))
        is_grb = "gribl" in vas.lower()
        e = {
            "row": row, "zap": z, "houseNo": hisna if is_grb else hisna + "*",
            "bookSignature": "04894", "year": 1906, "scan": SCAN_NO[scan],
            "page": PAGE[scan], "mesec": kor.get("mesec", v.get("mesec", "")),
            "smrt": str(v.get("smrt", "")), "pokop": str(v.get("pokop", "")),
            "vas": vas, "ime": kor.get("ime", v.get("ime", "")),
            "stan": kor.get("stan", v.get("stan", "")),
            "starost": kor.get("starost", v.get("starost", "")),
            "bolezen": kor.get("bolezen", v.get("bolezen", "")),
            "previden": kor.get("previden", v.get("previden", "")),
            "duhovnik": kor.get("duhovnik", v.get("duhovnik", "")),
            "opomba": kor.get("opomba"),
        }
        entries.append(e)

grb = [e for e in entries if not str(e["houseNo"]).endswith("*")]
dokaz = {
    "status": "SAMPLE-TRANSCRIPTION-D1906",
    "generated": "P172",
    "phase": "death-1906-full-year",
    "source": "matricula-online.eu 04894, skeni 104–108 == str. 103–107",
    "frame": {
        "leto": 1906, "vrstic": len(entries), "zap_oštevilčenih": 56,
        "neštevilčenih": 0, "vpisi": 55, "dup_zaporedna": "21 (s105-z21-Maj-10-Griblje + s106-z21-Maj-22-Klošter = PISAR-DUPLIKAT-1.-v-liniji!)",
        "griblje_vpisi": len(grb), "hise": len(set(e["houseNo"] for e in grb)),
        "hise_seznam": sorted(set(e["houseNo"] for e in grb), key=int),
        "ponovitve": "h58-×2 (z29-Matija-TOŽEK-10-mes + z35-Janez-FOČEK-49-let — 8-tednov-apart!)",
        "meja_1905_06": "s104 ('— 1906 —'-VELIKOPISANO + restart zap 61→1 + Januar-podčrtan — 13. POTRDITEV 5. STIL)",
        "meja_1906_07": "s109 (velika-'1907.' + Januar + restart zap 55→1 + glava-'181907' = 14. POTRDITEV 5. STIL; P171-lead-[~ s107+?]-KOREKCIJA-→-s109!)",
        "glave_napake": ["s104-'Leto 48/1905'-'4'-za-'1'-NOV-vzorec!", "s105-'Leto 18906'", "s106-'Leto 18.1906'", "s107-'Leto 181906'", "s108-'Leto 181906'"] ,
        "stran_invarianta": "stran == sken − 1 (77.–81. potrditev VIZUALNO!)",
    },
    "entries": entries,
    "excluded": [
        {"id": "X1", "opis": "s104-zap61-62 = 1905-vrstici (P171-ŽE-v-korpusu!): zap61-Anton-PEZDIREC-h42-8-mes-Dec + zap62-Gradac-h34-Ana-Hrastovšec?-72"},
        {"id": "X2", "opis": "s109 = MEJA-1906/07 + ZAČETEK-1907 (zap1–11-Januar-1907 = P173-LEAD!): z1-Anton-BRINEC-h49-66-vdovec-SPOL-KOREKCIJA + z2-Ana-VELJKO-h1 + z4-Ana-MEC-h91 + z5-Barbara-KRISTOF?-h87 + z9-Marija-POVH-h52-'+-Janezu-Pezdirec' + z11-Alojzij-DRIŠEK?-h31 = 6-GRIBLJE-v-Januarju-SAMO!"},
        {"id": "X3", "opis": "s110 = 1907-nadaljevanje (zap12–23-Februar–Marec): z13-Anton-Veljko-h60 + z18-Matija-Urh-h32-16-let; meja-1907/08 [~ s113+?]" },
    ],
    "anomalies": [
        {"id": "A1", "opis": "★★★ 5 GLAVE-NAPAKE = REKORD-LINIJE-IZENAČEN (P170-rekord-5!): s104-'Leto 48/1905'-'4'-za-'1'-NOV-vzorec + s105-'Leto 18906' + s106-'Leto 18.1906' + s107-'Leto 181906' + s108-'Leto 181906' — pisar-'18'-navada-×5-v-1-letu!"},
        {"id": "A2", "opis": "★★★ PISAR-DUPLIKAT-zaporedna-21 = 1.-V-LINIJI: s105-z21-Maj-10-Griblje-h19-Janez-KRIŽE + s106-z21-Maj-22-Klošter-h56-Neža-SRAIJER = 56-oštevilčenih-vrstic = 55-vpisov!"},
        {"id": "A3", "opis": "★★★ NOV DUHOVNIK #13: J. R. KUHINEK (×3-GRIBLJE: z21-h19-1.-podpis + z23-h39 + z29-h58 + s106-DOMINANTA-×9-vpisov!; ×13-duhovnik-linije)"},
        {"id": "A4", "opis": "★ LEOPOLD-PODLOGAR-kapelan-×1 (s106-z25-'kap. v Črnomlju'-izven-župnijski-1.-podpis-v-liniji!)"},
        {"id": "A5", "opis": "★ FLORJANČIČ-×2-s108 (z48-z54 — 1.-mrliški-podpisi-Florjančič-vzorec!; diag-'coadj./svp'-zmede; St.-Florijana-forma)"},
        {"id": "A6", "opis": "★ PODPISI-BREZ: z33–z36-s107-neodpisani (vzorec-1904-vpisi-4–19!) + z53-starost-PRAZNA + podpis-'———'-črta"},
        {"id": "A7", "opis": "★ VLM-HALUCINACIJE-×4-imen (z48-'Potokar'→JOČEK! + z54-'Timec'→ŠIMEC! + z21-'Klinc'→KRIŽE + z16-'črnjen-vrtnar'→'oženjen-oziškar'!) — kompozit-B2-×2-potrjene!"},
        {"id": "A8", "opis": "★ VLM-korekcije-boleznih-×3 (z1-'Šarost'→SLABOST-s/z-KURRENT + z6-'Nadluhec'→NADRUKA + z35-'Nadluka'→NADRUKA-r/u!) + z45-'November-1905'-HALUCINACIJA-VIZUALNO-Nov-1906"},
        {"id": "A9", "opis": "★★ h58-×2-v-1-letu (z29-Matija-TOŽEK-10-mes + z35-Janez-FOČEK-49-let — 8-tednov-apart!) + h58 = 8.-vpis-REKORDISTKA-izenačen-h18-1905"},
        {"id": "A10", "opis": "★ IZVEN-ŽUPNIJE: z14-s105-'Krupa-župnija-Semič'-Jurij-POTOKAR-60 + z49-h49-Gradac-Jakob-POPIČ (h49-ISTA-št.-kot-Griblje-Brinec-NE-ISTA-vas!) + h18-PADEC-vzorec-×3-leto-zapored"},
    ],
    "crossChecks": [
        {"id": "C1", "opis": "ZAP-KONTINUITETA: zap1–9 (s104) + zap10–21 (s105) + zap21–32 (s106 — DUP-21!) + zap33–44 (s107) + zap45–55 (s108) = 56-oštevilčenih = 55-vpisov (ČISTO-LETO-z-DUPLIKATOM!)"},
        {"id": "C2", "opis": "10 Griblje-vpisov = parish.ts-bloki-1906 (1:1!) + 9 hiš [18,19,20,39,44,49,57,58,77] (h58-×2!)"},
        {"id": "C3", "opis": "duhovniki-Griblje: Lengsfeld-×3 (z1-z6-z16) + KUHINEK-×3 (z21-z23-z29) + brez-×2 (z34-z35) + Florjančič-×2 (z48-z54) = 10/10-pokriti = 4-duhovniki-v-1-letu"},
        {"id": "C4", "opis": "meseci-Griblje: Jan1·Feb1·Mar1·Maj1·Jun1·Avg1·Okt2·Dec2 = 10 ✓ + starosti-1-mes→78-let + otroška-smrt-4/10"},
        {"id": "C5", "opis": "56-vrstic == s104-9 + s105-12 + s106-12 + s107-12 + s108-11 = 56 ✓ + stran == sken − 1 (77.–81.-potrditev-VIZUALNO!)"},
    ],
    "honesty": [
        "honesty-1: z16-bolezen-'Pljučnica'[~ diag-'Rjučnica?' — KURRENT-p/r]",
        "honesty-2: z21-ime-'KRIŽE'[~ diag-'Krizc/Heiže'-zmeda]",
        "honesty-3: z35-ime-'FOČEK'[~ diag-'Foček/Sosek']",
        "honesty-4: z33-ime-'POTRNIK'[~ diag-'Dotromiš'-NEBERLJIVA]",
        "honesty-5: VLM-page-mesec-None-×8 (s106-×7 + s108-×6 — diag-vizualno-popravljeni)",
        "honesty-6: rows-v3-detekcija-FAIL-s107–s110 (celice-manjka) — diag-grid-recept-P170-metoda-REŠILA!",
        "honesty-7: z8-s104-starost-'4-let?[~]' — VLM-'8/3-[~83?]' + diag-'4?'-NEUSKLJENA",
    ],
    "nextSteps": {"P173-lead": "mrliška-1907 (s109-zap1–11-ŽE-prebrani: z1-Anton-BRINEC-h49-66-Jan-VDovec [P172-lead-'Ana'-SPOL-KOREKCIJA!] + z2-Ana-VELJKO-h1-6-let + z4-Ana-MEC-h91-4?-let [2.-najvišja-hiša!] + z5-Barbara-KRISTOF?-h87-3-tednov + z9-Marija-POVH-h52-44-let-'+-Janezu-Pezdirec'-stan! + z11-Alojzij-DRIŠEK?-h31-6-mes = 6-GRIBLJE-v-Januarju-1907-SAMO!; s110-z13-Anton-Veljko-h60 + z18-Matija-Urh-h32-16-let; meja-1907/08 [~ s113+?])"},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(dokaz, f, ensure_ascii=False, indent=1)
print(f"dokaz: {OUT}")
print(f"entries: {len(entries)} | Griblje: {len(grb)} | hiše: {dokaz['frame']['hise_seznam']}")
grb_z = [e['zap'] for e in grb]
print("Griblje-zap:", grb_z)
