#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P176 — zgradi dokaz research/issue17/parish-death-1910.json
54 entries (12 Griblje + 42 s-*) iz VLM-raw + forenzika-korekcije (crops ×3.0/×8.0)
+ meseci-rekonstrukcija (bande z14/z15/z21/z24/z29/z33/z39/z44/z51) + anomalije +
crossChecks + honesty + P177-lead."""
import json, re, datetime

OUT = "research/issue17/parish-death-1910.json"

# ——— meseci-rekonstrukcija (banda-začetki + sekvencna forenzika) ———
MESEC = {}
for z in range(1, 55):
    if z <= 3: MESEC[z] = "Januar"
    elif z <= 8: MESEC[z] = "Februar"
    elif z <= 13: MESEC[z] = "Marec"
    elif z == 14: MESEC[z] = "April"
    elif z <= 20: MESEC[z] = "Maj"
    elif z <= 23: MESEC[z] = "Junij"
    elif z <= 28: MESEC[z] = "Julij"
    elif z <= 32: MESEC[z] = "Avgust"
    elif z <= 38: MESEC[z] = "September"
    elif z <= 43: MESEC[z] = "Oktober"
    elif z <= 50: MESEC[z] = "November"
    else: MESEC[z] = "December"

SMRT = {1:"10",2:"12",3:"14",4:"2",5:"3",6:"19",7:"21",8:"21",9:"1",10:"17",11:"20",12:"20",
        13:"25",14:"24",15:"7",16:"7",17:"11",18:"14",19:"14",20:"23",21:"5",22:"19",23:"26",
        24:"13",25:"15",26:"25",27:"27",28:"28",29:"15",30:"18",31:"21",32:"26",33:"4",34:"7",
        35:"8",36:"8",37:"15",38:"24",39:"6",40:"12",41:"14",42:"27",43:"31",44:"15",45:"15",
        46:"19",47:"20",48:"20",49:"21",50:"25",51:"11",52:"14",53:"16",54:"25"}
POKOP = {1:"11",2:"13",3:"18",4:"4",5:"5",6:"21",7:"23",8:"23",9:"3",10:"19",11:"22",12:"22",
         13:"26",14:"24",15:"8",16:"9",17:"13",18:"14",19:"16",20:"25",21:"6",22:"21",23:"27",
         24:"15",25:"17",26:"24",27:"28",28:"30",29:"18",30:"19",31:"22",32:"28",33:"6",34:"9",
         35:"9",36:"9",37:"17",38:"29",39:"8",40:"13",41:"19",42:"29",43:"2. nov.",44:"17",
         45:"17",46:"21",47:"21",48:"22",49:"23",50:"26",51:"13",52:"15",53:"17",54:"26"}

def scan_of(z):
    if z <= 12: return 126
    if z <= 24: return 127
    if z <= 36: return 128
    if z <= 48: return 129
    return 130

# ——— forenzika-KOREKCIJE (crops) na Griblje ———
FIX = {
    3:  {"ime": "Mihael Pezdirec", "stan": "vdovec in vrtnar [~ 'vrt(h)ar']", "bolezen": "Mrtvo najden", "starost": "72 let", "previden": "."},
    9:  {"ime": "Marjeta Pezdirec", "stan": "samostka delavka [~ samska]", "starost": "66 let [VLM-'86'-ZAVRJEN]", "bolezen": "Utomila [~ izčrpanost]", "previden": "."},
    10: {"ime": "Matija Kambič [VLM-'Vambič'-ZAVRJEN — K-@8×]", "stan": "ženjen vrtnar [VLM-'možen'-ZAVRJEN]", "bolezen": "Vodernica [~ dropsy]", "starost": "69 let", "previden": "1."},
    13: {"ime": "Marjeta Vötter [~ Vöttler — lexikon ×23]", "stan": "vdova vrtnarica", "hisa": "7", "starost": "70 let [lead-'40'-KOREKCIJA]", "bolezen": "Altersschwäche [NEMŠČINA]", "previden": "1", "opomba": "GRIBLJE — forenzika (crops ×2.2/×3.0/×8.0); h7 = P175-lead-'h4'-KOREKCIJA"},
    23: {"ime": "Alojzij Kralj", "starost": "25 dni", "bolezen": "Altersschwäche [NEMŠČINA]", "previden": "."},
    38: {"ime": "Martin Papič [VLM-'Japič'-ZAVRJEN — P-@8×]", "stan": "oženjen ⅛ zemljak [1.-⅛-LINIJE; VLM-'18 umrlat'-ZAVRJEN]", "starost": "53 let", "previden": "1"},
    40: {"ime": "Vincencij Kalan [VLM-'Halam'-ZAVRJEN — lexikon ×34]", "stan": "učiteljev sin [VLM-'nežnjen'-ZAVRJEN]", "starost": "6 mesecev", "previden": "."},
    41: {"ime": "Alojz Muc [VLM-'Huc'-ZAVRJEN — M-@3×]", "stan": "¼ zemljakov sin", "starost": "3 mesece", "previden": "."},
    45: {"ime": "Ana Jakofčič [VLM-'Jakopič'-ZAVRJEN — f-forma]", "stan": "vdova vrtnarica [VLM-'oživljenica'-ZAVRJEN]", "starost": "42 let", "bolezen": "Šanost [~ X-ANOMALIJA]", "duhovnik": "Jos. Punc [~ crop-'Punc'-jasno — VLM-'Pavić'-ZAVRJEN]", "previden": "1"},
    46: {"ime": "Juri Jakofčič [VLM-'Jaklič'-ZAVRJEN — ista-pisava-kot-mati]", "starost": "1 dan", "bolezen": "Slabohotnost [~ 'Slabotnost'?]", "previden": "."},
    51: {"ime": "Ana Novak", "stan": "bajtarjeva hči", "starost": "¼ ure [★★★ EKSTREM]", "previden": "."},
    53: {"ime": "Marko Štravs [~ Štraus — VLM-'Štrancar'-ZAVRJEN]", "stan": "oženjen vrtnar [VLM-'srejenin otrok'-ZAVRJEN]", "starost": "75 let", "bolezen": "Starost", "previden": "1"},
}
GRIBLJE_ZAPS = [3, 9, 10, 13, 23, 38, 40, 41, 45, 46, 51, 53]
GRIBLJE_HISKE = {3:"14", 9:"49", 10:"74", 13:"7", 23:"35", 38:"31", 40:"90", 41:"91", 45:"6", 46:"6", 51:"16", 53:"72"}

VAS_FIX = {"Oerkovšče": "Orehovišče", "Oerhovšče": "Orehovišče", "Orehoviše": "Orehovišče",
           "Gradca": "Gradce", "Gradcae": "Gradce", "Harjugne": "Krivoglave [~]",
           "Hriovoglance": "Krivoglave", "Gipšiče": "Krpšiče [~]", "Iborst": "Boršt [~]",
           "Guadac": "Gradac [~]", "Klošter": "Klošter [~]", "Hastava": "Hrastava [~]",
           "Hruvinica": "Hrušica [~]", "Hrušiče": "Hrušica [~]", "Hrušoglave": "Hrušoglave [~]",
           "Otok": "Otok", "Dragoše": "Dragoše", "Goriče": "Goriče", "Krasinec": "Krasinec",
           "Dobravice": "Dobravice", "Podmelnica": "Podmelnica", "Vranoviče": "Vranoviče",
           "Vranovje": "Vranovje", "Kaštava": "Hrastava [~]", "Mlače": "Mlače [~]", "Kornelj": "Kornelj [~]"}

def duh_norm(d):
    if not d: return "—"
    if "Bit" in d or "Bih" in d or "Bitn" in d: return "Lausin Bitnar [~ #16]"
    if "Punc" in d or "Pomp" in d or "Pavić" in d or "Pauč" in d: return "Jos. Punc [~]"
    if "Pintar" in d: return "Jos. Punc [~ 'ž'-pripis — VLM-'Pintar']"
    return d + " [~]"

rows = []
for scan in (126, 127, 128, 129, 130):
    d = json.load(open(f"/tmp/p176/raw/s{scan}.json"))
    raw = d["raw"]; i = raw.find("{"); j = raw.rfind("}")
    obj = json.loads(raw[i:j+1])
    for r in obj["rows"]:
        zap = int(re.sub(r"[^\d]", "", str(r.get("zap", "0"))) or 0)
        if scan == 130 and zap < 49:
            continue  # 1911-restart-vrstice (P177-lead!) — IZVEN 1910-dokaza
        if not (1 <= zap <= 54):
            continue
        if zap in GRIBLJE_ZAPS:
            f = FIX.get(zap, {})
            ime = f.get("ime", r.get("ime", ""))
            stan = f.get("stan", r.get("stan", ""))
            hisa = f.get("hisa", GRIBLJE_HISKE[zap])
            star = f.get("starost", r.get("starost", ""))
            bol = f.get("bolezen", r.get("bolezen", ""))
            prev = f.get("previden", r.get("previden") or "—")
            duh = f.get("duhovnik", duh_norm(r.get("duhovnik")))
            vas = "Griblje"
            opomba = "GRIBLJE — forenzika (crops ×2.2/×3.0/×8.0)"
        else:
            ime = r.get("ime", "")
            stan = r.get("stan", "")
            hisa = str(r.get("hisa", "")).strip(".")
            star = r.get("starost", "")
            bol = r.get("bolezen", "")
            prev = r.get("previden") or "—"
            duh = duh_norm(r.get("duhovnik"))
            v = r.get("vas", "")
            vas = VAS_FIX.get(v, v)
            opomba = "ne-Griblje; VLM-raw"
        rows.append({
            "row": len(rows) + 1, "zap": zap, "houseNo": hisa, "bookSignature": "04894",
            "year": 1910, "scan": scan_of(zap), "page": scan_of(zap) - 1,
            "mesec": MESEC[zap], "smrt": SMRT[zap], "pokop": str(POKOP[zap]),
            "vas": vas, "ime": ime, "stan": stan, "starost": star, "bolezen": bol,
            "previden": prev, "duhovnik": duh, "opomba": opomba,
        })

rows.sort(key=lambda e: e["zap"])
assert len(rows) == 54, f"rows={len(rows)}"
assert sum(1 for e in rows if e["vas"] == "Griblje") == 12

dokaz = {
    "status": "SAMPLE-TRANSCRIPTION-D1910",
    "generated": datetime.datetime.now().isoformat(timespec="seconds"),
    "phase": "P176 — mrliška 04894, leto 1910 (25. polno leto mrliške linije; issue #18)",
    "source": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/ (skeni 126–130 == str. 125–129; stran == sken − 1 — 101.–105. potrditev VIZUALNO; s126-'Stran 125'!)",
    "frame": {
        "vpisi": 54, "zap_oštevilčenih": 54, "neštevilčenih": 0,
        "griblje_vpisi": 12, "hise": 11, "ponovitve": "6",
        "skeni": "s126 (zap1–12; glava-'Leto 18 1910'; 7. STIL-2. leto) + s127 (zap13–24) + s128 (zap25–36) + s129 (zap37–48) + s130 (zap49–54)",
        "meja_1909_10": "s126 (glava-'Leto 18 1910' + restart-54→1-BREZ-velikega-separatorja = 7. STIL-2. leto — P175-lead-POTRJEN!)",
        "meja_1910_11": "s130-INSIDE (z1-restart-Januar-1911 = 8. STIL-mid-scan-restart-1.×! P175-lead-'[~ s131+?]' KOREKCIJA-→-s130!)",
    },
    "entries": rows,
    "excluded": [
        {"id": "X1", "opis": "s130-z1–5 (1911-Januar — mid-scan-restart! z1-Stampahar-Gradac-h62 + z2-Bohte + z3-Juvančič-¼-ure-×2-EKSTREM-leti! + z4-MRTVOROJENEC-'J.-Škaf'-BREZ-PODPISA + z5-Mura) — P177-lead!"},
        {"id": "X2", "opis": "s131-z6–17 (1911-Continuatio — 2 GRIBLJE-ŽE-vidnih: z13-Ana-BRINEC-h14-8-let + z14-Katarina-HRUŠIČ-h34-88-let-ŠILAK-vrnitev!) — P177-lead!"},
        {"id": "X3", "opis": "s132-z18–29 (1911 — 3-'Pexdipec'=PEZDIREC-×3: z24-Ana-h10-81 + z26-Janez-h42-53 + z27-Vido-h48-3-mes!) — P177-lead!"},
    ],
    "anomalies": [
        {"id": "A1", "opis": "★★★ z51-Ana-Novak-h16-STAROST-'¼ URE' = EKSTREMNA-STAROST-LINIJE (15 minut! 1.-'ure'-enota-v-liniji — prej-minimum-½-dne! max-zoom-'1/4-ure' @3×)"},
        {"id": "A2", "opis": "★★★ z38-Martin-PAPIČ-h31 = IŠTO-IMEŠKI-PAR-24-LETNI-LOK (Martin-Papič-28-poročna-04455-1886-№2-×-Margareth-STRAUS → 1910-†-53-ISTA-HIŠA! VLM-'Japič'-ZAVRJEN @8× — P-zanček)"},
        {"id": "A3", "opis": "★★★ z40-Vincencij-KALAN-učiteljev-sin-h90 = ŠOLSKA-HIŠA-vez (učiteljska-veriga: Klambič-†-1890-20½ → Kopitar → Vetrovnik-1898 → Kalan-1908 → Šušteršič-1914! VLM-'Halam'-'nežnjen-sin'-ZAVRJENA-×2)"},
        {"id": "A4", "opis": "★★★ z23-h35 = 10. MRLIŠKI VPIS HIŠE = NOV REKORD LINIJE (h58-9-prekašan!) + KRIŽAN-hiša→KRALJ-menga"},
        {"id": "A5", "opis": "★★★ z10-Matija-KAMBIČ-h74 = VLM-'Vambič'-ZAVRJEN (K-inicial-@8× — dvojna-zanka!) + 1886-'Hambeč'-koren = H/K/V-zmeda-RAZREŠENA + P175-lead-'Hanžič?'-ZAVRJEN"},
        {"id": "A6", "opis": "★★★ z41-Alojz-MUC-h91 = VLM-'Huc'-ZAVRJEN (M-dvojni-jez @3×!) — h91-MUC-vez (1890 + 1899 + 1910)"},
        {"id": "A7", "opis": "★★★ z53-Marko-ŠTRAVS-h72 = VLM-'Štrancar'-'srejenin otrok'-ZAVRJEN-×2 (h72-poročna-1921-№22-vez! 'Starost'-kot-vzrok = 1.-TA-BOLEZEN-linije)"},
        {"id": "A8", "opis": "★★ z3-'Mrtvo najden' = 1.-TA-BOLEZEN-v-SLOVENŠČINI + 2.-TRAUMA-SMRT-linije (cf.-1908-'Z-VRCA-PADEL-JE-SE-UBIL'!) + ★★ z29-'Je utonil'-Podmelnica-78 = 1.-UTONITEV-LINIJE"},
        {"id": "A9", "opis": "★★ z45/z46-h6-×2 = MATI+SIN-v-4-DNEH (Ana-JAKOFČIČ-42 + Juri-1-dan! VLM-'Jakopič'-'Jaklič'-ZAVRJENA — f-ascender+descender @3×!) = PADEC-vzorec-7.-leto + 4.-družinski-dvojni-smrti-par"},
        {"id": "A10", "opis": "★★ z13-VÖTTER-h7 = P175-lead-'h4-40'-KOREKCIJA-×2 (h7-70-let! TOTTER/FOTTER→VÖTTER-33-let-vez) + ★★ z9-'66'-P175-lead-POTRJEN (VLM-'86'-ZAVRJEN — KURRENT-6-lekcija-×2)"},
        {"id": "A11", "opis": "★★ z38-'⅛ zemljak' = 1.-⅛-ULOMEK-LINIJE (½/¼/⅛-nov-nivo!) + ★★ Altersschwäche-×2-NEMŠČINA-v-3-mesecih (z13 + z23) = 1902-vzorec"},
        {"id": "A12", "opis": "★ meseci-bande-forenzika: 'None'-VLM-artefakt = nadaljevanje-mesecu — bande-rekonstruirane-zaporedno (April-z14 + Maj-z15 + Junij-z21 + Julij-z24 + Avgust-z29 + September-z33 + Oktober-z39 + November-z44 + DECEMBER-z51-VLM-izpuščil!) + s130-glava-'Leto 1910 / ~1911~'"},
    ],
    "crossChecks": [
        {"id": "C1", "opis": "zap-kontinuiteta: 54-oštevilčenih == 54-VPISOV — ČISTA-SEKVENCA-zap1–54 (6.-čisto-leto! 0-predorov/0-duplikatov/0-neštevilčenih!)"},
        {"id": "C2", "opis": "stran == sken − 1 VIZUALNO (s126-'Stran 125' + s127–s130 == str. 126–129 — 101.–105. potrditev!)"},
        {"id": "C3", "opis": "meja 1910/11 = s130 INSIDE (z54-December-25 → z1-Januar-1911-BREZ-velikega-separatorja = 8. STIL-mid-scan-restart-1.× — P175-lead-'[~ s131+?]' KOREKCIJA-→-s130!)"},
        {"id": "C4", "opis": "hišna-številke-križno: h35-'35' = 10.-vpis-rekord + h90-'90' = učiteljska + h91-'91' = MUC + h31-'31' = PAPIČ-poročna-1886-№2 + h72-'72' = ŠTRAVS-1921-№22 — VSE-LEKSIKON-POTRJENE!"},
        {"id": "C5", "opis": "duhovnik-kontinuiteta: 'Lausin-Bitnar-[~]'-#16-DOMINANTA-×~26 (2.-leto!) + Jos.-Punc-×~12 (Punc/Rauq-zmeda-5.-leto!) — 0-NOVIH-duhovnikov (kontrast-1908/09!)"},
    ],
    "honesty": [
        "rows-v3-FAIL-lekcija-5.-leto (diag-grid-fiksni-recept — band-k = 330+135×k-P172-recept-100%-VELJAVEN-za-1910!)",
        "VLM-'None'-mesec-artefakt-NE-zapisan-kot-podatak — bande-rekonstruirane-sekvencno + 2-cropi-potrdila (z21-Junij + z24-Julij + z14-April + z15-Maj)",
        "z51-DECEMBER-band-VLM-izpuščil — rekonstruirano-sekvencno (pokop-13. 12.-skladen); [~] ne-kazuje-napake-v-dokazu",
        "z45-previden-'1'-crop-×4.0 (slash-stroke) — VLM-None; z38/z53-'1' + z40/z41/z46/z51-'.'-crop-×4.0-VSI-potrjeni",
        "z53-priimek-'Štravs'-[~] OHRANJEN (crop-kaže-'Štravs/Štraus'-dvom — lexikon-dvo-pisavi ×70/×35 — NE-odloča)",
        "z46-bolezen-'Slabohotnost'-[~] (VLM-'Slabohot' — končnica-neberljiva)",
        "z12-s126-podpis-'Jos.-Punc-ž.'-'ž'-pripis-ne razrešen (župnik? [?]) — VLM-'Pintar' ZAVRJEN-cropom",
    ],
    "nextSteps": [
        "P177-lead: mrliška 1911 (s130-z1–5 + s131-z6–17 + s132-z18–29 ŽE-prebrani: 5-GRIBLJE-ŽE-vidnih — z13-BRINEC-h14 + z14-HRUŠIČ-h34-88 + s132-PEZDIREC-×3-h10/h42/h48! z4-MRTVOROJENEC-BREZ-PODPISA!; meja 1911/12 [?])",
        "fetch s133–s136 + VLM-branje (≤2-skena/serijo-foreground)",
        "crops-×2.2/×3.0 + forezika (h14-BRINEC-vez + h34-ŠILAK-vrnitev + PEZDIREC-×3)",
        "kaskada: vitals 1032 → +n · bloki 333 → +n · guardi-1911",
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(dokaz, f, ensure_ascii=False, indent=1)
g = sum(1 for e in rows if e["vas"] == "Griblje")
print(f"dokaz: {OUT} — {len(rows)} entries ({g} Griblje + {len(rows)-g} s-*) · {len(dokaz['anomalies'])} anomalij · {len(dokaz['crossChecks'])} crossChecks · {len(dokaz['honesty'])} honesty")
