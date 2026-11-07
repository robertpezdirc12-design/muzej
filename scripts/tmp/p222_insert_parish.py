#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P222 — vstavi 21-GRIBLJE-blokov (krstna 04104, leto 1884 = 2/15!) v parish.ts PRED P221-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P221: krstna PREDZGODOVINA 04104, leto 1885 = 1/15"

E = json.load(open("/tmp/p222/entries_1884.json"))
grib = E["griblje_entries"]
assert len(grib) == 21, f"grib={len(grib)}"

P222_HDR = "  // ——— P222: krstna PREDZGODOVINA 04104, leto 1884"
if P222_HDR in src:
    i = src.index(P222_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P222-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}

KOM = {
 "z1": "★★★ RESTART-z1 = 1.-vpis-1884-NA-DAN-1.-1.! (PARALELA-P221-z1!) + hiša-DUEL (34-vs-84! — '37'-ZAVRNJENA-hi2!)",
 "z19": "★ pripis-garble-'gem/gest-3/5-884'[?]-X-open-KRIŽ! + h13-nit (1/2!)",
 "z21": "★ honesty-TRI-DUEL-mati (Horvatinič/Krizan/Scarasin!) + ordinal-'11'-krop-MISREAD-KOREKCIJA (21!)",
 "z26": "★★★ DRAGOŠ-mati-nit (P193/P220!) + ordinal-page/trak-'10'-MISREAD-KOREKCIJA (26!) + hiša-TRI-DUEL (33/58/38!)",
 "z45": "★ h2-KLEPEC/HLEBEC-hiša-nit (P219-1858!) + ordinal-page-'44'-MISREAD-KOREKCIJA (45-3:1!)",
 "z51": "★★★ URH-oče + SIMEC-mati-niti! + mesec-DUEL (Juni-rekonstrukcija!)",
 "z59": "★★★ KRIŽAN-oče + botri-KRIŽAN-×2! + hiša-page-'96'-MISREAD-KOREKCIJA (36-2:1!) + mesec-page-'Juni'-KOREKCIJA (Juli!)",
 "z61": "★★★ POŽEK-mati-nit! + URIH?-oče-garble-X-open + h68",
 "z65": "★★★ NEZAKONIT (oče-PRAZNO!) + mati-DUEL (Brunec-vs-Dragos!) + botra-POŽEK?-X-open",
 "z69": "★★★ PEZDIRC-mati-nit! + mesec-page-'November'-MISREAD-KOREKCIJA (august-krop!) + h13-×2 (2/2!)",
 "z70": "★★★ pripis-'†29/10-1887' = KRIŽ-04106-X-open! (krop-'1883'-chrono-KOREKCIJA!)",
 "z75": "★ hiša-DUEL (43-vs-13!) + DVOJNI-mesec-MISREAD-KOREKCIJA (chrono-august!) + MMK-'1974'-pripis!",
 "z78": "★★★ PEZDIRC-grafija-oče + DEBLIČ-mati + BRODARIČ-botra-niti!",
 "z84": "★★★ ordinal-KOREKCIJE-s182 (81-DUP→82→83→84!) + botra-KRIŽAN + krop-'Ursch'-MISREAD-DUEL (MRAK!)",
 "z84dup": "★★★ z84-DUPLIKAT-ANOMALIJA (s183-vrsta1-2×-84!) + honesty-MAX-1884 + PEZDIRC-oče-nit!",
 "z93": "★★★ LAZAR-oče-nit (P220-1857!) + hiša-page-'48'-MISREAD-KOREKCIJA (18-2:1!)",
 "z95": "★★★ PEZDIRC-mati-nit (2/2!) + BRODARIČ-oče-nit!",
 "z99": "★★★ vas-DUEL-REŠEN (GRIBLJE-2:1 — 'Podplanina'-ZAVRNJENA!) + JAKLIČ-oče + MMK-'1911'-pripis!",
 "z105": "★★★ oče-DUEL-REŠEN (KURE-vs-'Glazar'!) + botra-MILEK-nit (P218/P220-h65!) + pripis-'1953'-X-open!",
 "z110": "★ honesty-oče-TRI-QUAD-garble (Martincič/Gratzy/Gostofar!) + h8-nit",
 "z112": "★★★ PREČRTANA-TAIL + pripis-'†28/12-1887' = KRIŽ-04106! + TAIL-1884-zadnja-vrstica-leta! (61.-POTRDITEV!)",
}

def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')

def clean_day(d):
    d = str(d or "").strip().rstrip(".")
    d = d.split()[0] if d else "?"
    return d if d else "?"

def gen_block(e):
    z = e["z"]
    ime = (e.get("otrok") or "?").strip()
    ocec = (e.get("ocec") or "").strip()
    matec = (e.get("matec") or "").strip()
    botra = (e.get("botra") or "").strip()
    mesec = (e.get("mesec") or "").strip()
    rojen = clean_day(e.get("rojen"))
    krsten = clean_day(e.get("krsten"))
    kom = KOM.get(z, "")
    hisna_raw = str(e.get("hisna") or "[?]")
    hisna = hisna_raw.split(" ")[0].strip("[],")
    if hisna.startswith("[") or hisna == "" or "DUEL" in hisna_raw:
        hisna = "[?]"
    mm = mesec.split("/")[0].split()[0] if mesec else ""
    mm = mm.strip("[]()~? ").split("-")[0]
    mnum = MESEC_SI.get(mm, "")
    men = MESEC_EN.get(mm, mm or "?")
    mpart = f"{mnum}." if mnum else "[?]"
    what = f"krščena {ime} ({rojen}./{krsten}. {mpart})"
    if ocec: what += f" — oče {ocec}"
    if matec: what += f", mati {matec}"
    if botra: what += f"; botra {botra}"
    if kom: what += f"; + {kom}"
    what += f" + [{z}]"
    what_en = f"baptized {ime} ({men} {rojen}/{krsten})"
    if ocec: what_en += f" — father {ocec}"
    if matec: what_en += f", mother {matec}"
    if botra: what_en += f"; godparents {botra}"
    what_en += "; + [see-SI]" + f" + [{z}]"
    return (
        "  {\n"
        f'    houseNo: "{esc(hisna)}",\n'
        '    bookSignature: "04104",\n'
        "    year: 1884,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['pag']},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P222: krstna PREDZGODOVINA 04104, leto 1884 = 2/15 — (s173–s186 == pag sken+13-FOLIO-SVINČNIK-ARHIVARJA "
    "(razprti-dvostranski-list = 1-folio! — re-potrjeno-×3-sveže: s177='190'/s181='194'/s185='198'! — skupaj-8×!; "
    "2×-neodvisna-prenosa-md5-17/17!); ★★★ MEJA-1883/84-s173 (z99-TAIL-1883 + VSOTNA-razpete-'1/8/8/4'-P214-TIP + "
    "restart-z1-NA-DAN-1.-1.-GRIBLJE!) = 61.-POTRDITEV-invariante! (60.-P221!); 112-vpisov-DISTINCT — ŠTEVJE-IZ-VRSTIC-2.×-za-krstno-linijo "
    "(z1–z112; vrstna-aritmetika 7+7+9+8+8+10+10+10+8+8+9+10+8+2 = 114-vrstic − z84-DUP-korekcija = 112-DISTINCT = P221-'1884-=-112'-1:1!; "
    "★★★ PISARJEVE-ANOMALIJE: s175-prepiše-8–14-za-9-vrstic (2-manjka! '8'-RAZPETA!) — vrstna-aritmetika-REŠI-15–23! + "
    "s177-REORIZENTACIJA (61–68-prečrtano-×8→31–38!) + s178-40/41-wobble + s176-'81'→29-korekcija + s179-top-48/49-korekciji + "
    "s182-81-DUP-korekcije-×3 (→82/83/84!) + ★★★ z84-DUPLIKAT (s182-vrsta8=84 + s183-vrsta1=84! — pisar-2×-84! — NOVA-TIP!) + "
    "s184-93–102 + 1-PRAZNA-NEŠTEVILČENA-VRSTICA (med-99-in-100!) + revizijske-poševnice-×10!) — "
    "★★★ 21-GRIBLJE / 20-hiš (h13-×2!) + vas-DUELI-REŠENI-krop-hi (z99-GRIBLJE-JASNO-vs-'Podplanina'-ZAVRNJENA! + z52-PRILOZJE-IZLOČEN "
    "(page-'Griblje'-MISREAD!) + z60-BORŠT-IZLOČEN!) + ★★★ POZNEJŠI-PRIPISI-KRIŽ-z-mrliško-04106 (z70-†29/10-1887 + z112-†28/12-1887 + "
    "z19-gest-3/5-884[?] + z75-MMK-1974 + z99-1911 + z105-Mrt/Poroč-1.10.1953-X-open!) + mreže: PEZDIRC-×4 (z69-mati + z95-mati+botra + "
    "z78-oče-grafija + z84dup-oče!) + KRIŽAN-×3 (z59-oče+botri-×2 + z84-botra + z105-mati!) + BRODARIČ-×5 + POŽEK-×2 + URIH + SIMEC + URH + "
    "MILEK + LAZAR + DRAGOŠ + DEBLIČ-×2 + JAKLIČ ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count('year: 1884,\n    scan:')
print(f"vstavljenih blokov 1884-04104: {n} (pričakovano 21)")
