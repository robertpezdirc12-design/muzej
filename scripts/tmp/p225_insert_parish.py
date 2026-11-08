#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P225 — vstavi 17-GRIBLJE-blokov (krstna 04104, leto 1881 = 5/15!) v parish.ts PRED P224-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P224: krstna PREDZGODOVINA 04104, leto 1882"

E = json.load(open("/tmp/p224/entries_1881.json"))
grib = E["griblje_entries"]
assert len(grib) == 17, f"grib={len(grib)}"

P225_HDR = "  // ——— P225: krstna PREDZGODOVINA 04104, leto 1881"
if P225_HDR in src:
    i = src.index(P225_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P225-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}

KOM = {
 "z1": "★★★ RESTART-z1-NA-DAN-1.-1.-JÄNNER-GRIBLJE-h55 (4.-GRIBLJE-restart-z1!-P221-h21!-P222-h34!) + PEZDIRC-matec-nit-X-open (Podžirec~Pezdirec!-1/9!) + hiša-'55'-VIZUALNO!",
 "z15": "★★★ hiša-'37'-DUEL-1:1 (page-vs-row-krop-'34'!-KURRENT-3/4!) + NEZAKONSKI-vzorec (ime-v-očetovem-stolpcu!) + DEBLIČ-boter-nit (1/2!)",
 "z28": "★★★ KRIŽAN-mreža-×3-v-vrstici (oče+matec+botra-Hrižan!) + SIMEC-boter-nit (1/2!) + '+'-mark (PARALELA-z42!)",
 "z30": "★★★ DRAGOŠ-botra-nit (2×!-P193/P220-nit!) + oče-TRI-garble (Pircer/Pinter/Pimer!) + pripis-MMK-'†-16.12.1931-[~1937-DUEL!]'",
 "z40": "★★★ PEZDIRC-matec-nit (2/9!) + BRODARIČ-oče-nit (1/6!) + DEBLIČ-boter (2/2!) + SIMEC-botra (2/2!) + hiša-'49'-DUEL-1:1 (page-vs-krop-'19'!)",
 "z42": "★★★ PEZDIRC-oče-nit (3/9!-2×!) + August-labela-z42-VIZUALNO (blok-start!) + DEBLIČ-matec-nit (2/2!) + BRODARIČ-boter!",
 "z43": "★★★ pripis-MMK-'Umrła-11.11.1960-v-Črnomelju' + 'Črnušnjak-24.1.[?]' + Jabl[ov]šič-oče/botra-DUPLIKAT-priimek (PARALELA-z45!)",
 "z45": "★★★ KLOBUČAR-botra-nit (2×!-z10/z34/z97-1882-nit-nadaljevanje!) + Jabl[ov]šič-×2-vrstici + ime-'Anna [~Amma]'-honesty",
 "z48": "★★★ BOTRA-PRAZNA-ANOMALIJA (natisnjena-prazna-vrsta!-1.-v-krstni-liniji!) + oče-TRI-garble (Hure/Hmelj/Hrnč!) + ime-garble-MAX (Justina/JustynAnna!) + hiša-'62'-VIZUALNO (P224-z74-h62-PARALELA!)",
 "z52": "★★★ PEZDIRC-botra-nit (4/9!) + KRIŽAN-boter-nit + pripis-POROKA-'Vnalila-2.9.1959-→-Ožbolt-št.6-MŽ-Griblje-1959-št.53' + ime-'Maria'-2:1 (page-'Marta'-ZAVRNJENA!) + oče-DUEL (Brodnik/BRINAR!)",
 "z55": "★★★ PEZDIRC-matec+boter-DVOJNI-nit (×2-v-vrstici!-P224-z90-PARALELA!) + KRIŽAN-oče-nit + BRODARIČ-botra-nit (3/6!) + hiša-'63'",
 "z57": "★★★ PEZDIRC-oče-nit (6/9!-2×!) + October-labela-z57-VIZUALNO (blok-start!) + pripis-POROKA-'Vnalila-30.3.1958-→-Griblje' + BRINC-matec-nit (P224-z71-PARALELA!) + hiša-'14' (P224-z22-PARALELA!)",
 "z66": "★★★ NEZAKONSKI-vpis (edini-eksplicitni-1881!-matec-'ynb.') + PEZDIRC-oče-nit-X-open (7/9!-Pegdire/Bedire-DUEL!) + hiša-'57'-DUEL-1:1 (page-vs-krop-'37'!) + BRODARIČ-boter (4/6!)",
 "z71": "★★★ starši+botra-garble-QUAD-honesty-MAX (Kürne/Kime/Kirn!-Jakschevič!-Brož!-Milhels!) + hiša-'24 [~]' + Okt-30 (November-prelom-PO-z71!)",
 "z75": "★★★ ŽELJKO-matec+boter-nit (×2-v-vrstici!-P139-nit + P224-z29-nit!) + KRIŽAN-botra-nit (5-nit!) + 'in-Griblje'-stan-očeta + Nov-6/7",
 "z78": "★★★ PEZDIRC-matec-nit (8/9!-Perdijc-grafija!) + MILEK-oče-nit (P224-z55-h65-PARALELA!) + BRODARIČ-botra-nit (5/6!) + hiša-'22 [~]'",
 "z81": "★★★ PEZDIRC-oče-nit (9/9-REKORD!) + KRIŽAN-matec+botra-DVOJNI-nit (×2!-6/5-nit!) + hiša-'42 [~]' (P224-z81-DUEL-PARALELA!) + wide-krop-VIZUALNO (z82-shift-ZAVRNJEN!)",
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
    import re as _re
    pag_raw = str(e.get("pag") or "")
    _pm = _re.match(r"(\d+)", pag_raw)
    pag_int = int(_pm.group(1)) if _pm else 0
    if "[" in pag_raw and kom:
        kom += " + pag-konvencija-sken−6"
    hisna_raw = str(e.get("hisna") or "[?]")
    hisna = hisna_raw.split(" ")[0].strip("[],")
    if hisna.startswith("[") or hisna == "":
        hisna = "[?]"  # DUEL-1:1-ohrani-prvo-številko (page-glas!) — DUEL-ostane-v-whatSi-opombi!
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
        "    year: 1881,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {pag_int},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P225: krstna PREDZGODOVINA 04104, leto 1881 = 5/15 — (s135–s147 == gola-svinčna-pag-'sken−6' "
    "(13/13-SEKVENČNO: s135='129'/s136='130'/s137='131'/s138='132'/s139='133'/s140='134'/s141='135'/s142='136'/"
    "s143='137'-sandwich!/s144='138'/s145='139'-sandwich!/s146='140'/s147='141'! — 129–141-brez-luknje-v-1881-oknu!; "
    "2×-neodvisna-prenosa-md5-14/14!); ★★★ MEJA-1880/81-s135/s136 (TAIL-1880-z116–z122-Dez-5–30 + 'Finis' + "
    "'Jahr 18 80.'-BREZ-VSOTNE! + 'Jahr 1881.'-glava + RESTART-z1-NA-DAN-1.-1.-JÄNNER-GRIBLJE-h55-Agnes!-"
    "4.-GRIBLJE-restart-z1!) = 64.-POTRDITEV-invariante! (63.-P224!); 89-vpisov-DISTINCT — vrstna-aritmetika "
    "7+7+7+7+7+7+8+8+8+8+8+7 = 89 = P224-LEAD-'z83–z89-tail'-1:1-INVARIANTA! (zap-stolpci-12/12-ČISTO!); "
    "★★★ 17-GRIBLJE / 17-hiš-VSE-DISTINCT (brez-duplikatov!-vs-25-TIE-P221/P224!) + ★★★ PEZDIRC-×9-NOV-REKORD-"
    "LETA (z1-matec-Podžirec[~]! + z40-matec! + z42-oče-2×! + z52-botra! + z55-matec+boter-DVOJNI! + z57-oče-2×! + "
    "z66-oče-Pegdire-X-open! + z78-matec-Perdijc! + z81-oče-Perdijc! + ×3-ne-Griblje = ×12!) — grafija-continuum-5-let! + KRIŽAN-×6 + "
    "BRODARIČ-×6 + SIMEC-×2 + DEBLIČ-×3 + ŽELJKO-×2 + DRAGOŠ + KLOBUČAR + MILEK + BRINC + JAKOFČIČ-×2 + "
    "★★★ 2-POROKE-PRIPISA-'VNALILA' (z52-2.9.1959-→-Ožbolt! + z57-30.3.1958-→-Griblje!) + ★★★ Z48-BOTRA-PRAZNA-"
    "ANOMALIJA (1.-v-krstni-liniji!) + ★★★ Z66-NEZAKONSKI-VPIS (matec-'ynb.'!) + Z14-MESEC-DUEL-REŠEN (APRIL-1!-April-labela-"
    "VIZUALNO!-page-'31-März'-ZAVRNJENO!) + pripisi-MMK-†-×2 (z30-†1931! + z43-†1960-Črnomelj!) + meseci-Griblje: "
    "J1+A1+Juni2+Juli1+Aug4+Sep2+Okt3+Nov3 (Feber/März/Dez-×0!) + 1880 = 122-vpisov-BONUS → P226-LEAD! ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count('year: 1881,\n    scan:')
print(f"vstavljenih blokov 1881-04104: {n} (pričakovano 17)")
