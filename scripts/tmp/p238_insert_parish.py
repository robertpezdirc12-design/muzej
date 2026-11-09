#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P238 — vstavi 7-GRIBLJE-blokov (poročna 04455, leto 1885 = 1/13 NOVA LINIJA!) v parish.ts PRED P79-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P79 vzorec: polno leto 1886 (vsi Griblje vpisi, strani 1–14) ———"

E = json.load(open("/home/z/my-project/research/issue17/parish-marriage-1885-04455.json"))
grib = [e for e in E["entries"] if e.get("griblje") is True]
assert len(grib) == 7, f"grib={len(grib)}"

P238_HDR = "  // ——— P238: poročna PREDZGOVINA 04455, leto 1885"
if P238_HDR in src:
    i = src.index(P238_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P238-bloke (idempotenca)")

KOM = {
    1: "★★★ RESTART-z1 = 1.-VPIS-1885 (25.-Jän!) + ★★★ hišni-DUEL-58-vs-38-RAZREŠEN-2:1 (krop: pet-zanka + marginalna-isto!) + OBE-vasi-GRIBLJE (h58 × h34) + mati-roj.-BRUNC [~BRINC!] = P237-BRINC-MREŽA-nit! + oče-DUEL-Matko/Marko + margin-»Griblje-dd.-25-Jänner-1885«",
    2: "★★★ štajerska-oblika-RAZREŠENA (blok-bere-se-desno→levo — 4-pasovi-krop!) + ženin-Griblje-60-1:1 (Pas-A-Wohnort-dve-števki!) + OBA-starševska-bloka-»½ Gribl./½ Gütbl.« = POL-KMETIJE-h60! + nevesta-Felško-GARBLE-MAX + nevesta-hiša-X-OPEN + datum-duel-2/3-Febr + zap-vpis-2 (3-PRESKOČEN!)",
    5: "★ nevesta-GRIBLJE-32 (×2-1:1!) + mati-roj.-DRAGOŠ = DRAGOŠ-nit! + ženin-Krasinec-h6/8-duel + h32-nit (04104-1885-sosedstvo-h35-×2!)",
    8: "★★★ h71 = STRAUS-hiša-1885-PRED-P80-sidrom-1887 (1:1-isto-hišo!) + mati-roj.-ŠUBLER + ★★ priče-MILEK? [~] + PEZDIREC [~] = 2-MREŽE-V-PRIČAH! + margin-Gemeindevorst.-Griblje",
    11: "★★★ ŽENIN = Georg-PEZDIRC (krop-1:1!-IME-+oče-Andreas!) = PEZDIRC-CONTINUUM-v-poročni (04104-×131-nit!) + nevesta-vas-DUEL-»Gern/Gornje-29«-vs-GRIBLJE-29-X-OPEN (h29-MILEH-epidemija-1886-PRED-1-leto!) + ½-Gütl-stand-≠-hiša!",
    16: "★★★ h26-GRIBLJE-BRINEC-hiša (usnjar!) = P237-BRINC/BRINEC-MREŽA-nit-ŠIRŠA (h65-pred-doba + h69-doba!) + Georg-22-leta + priča-Peter-BRINEC (brat?) + LEDERER-×4 + datum-duel-16/10-Maj + VPIS-16 (po-preskočeni-3!)",
    22: "★★★ TAIL-1885 = ZADNJI-VPIS-LETA-22 (22.-Nov!) + OBE-vasi-GRIBLJE (h13 × h23/28-DUEL!) + mati-roj.-PEZDIREC [~!] = PEZDIREC-×3-v-letu! + h13-nit (P80-krstni-Matija-JAKOPIČ-1886-isti-priimek!) + veliko-1886-restart-na-isti-strani (MISREAD-»1883«-duel!)",
}

def blk(e):
    row = e["row"]
    scan = e["scan"]
    page = e["page"]
    h = e["pin"]["house"]
    g = e["groom"]; b = e["bride"]
    s = e["date"]
    d = s.split(".")
    dan = d[0]
    mesec = {"1": "Januar", "2": "Februar", "3": "Marec", "4": "April", "5": "Maj", "7": "Julij", "8": "Avgust", "11": "November", "?": "[?]"}.get(d[1], "[?]")
    dan_en = dan
    mesec_en = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "7": "Jul", "8": "Aug", "11": "Nov", "?": "[?]"}.get(d[1], "[?]")
    kom = KOM.get(row, "")
    what_si = (f"poroka {dan}. {mesec} 1885 (vpis {row}) — ženin {g['name']}, {g['age']} let, {g['status']}"
               f"{', ' + g['stand'] if g.get('stand') else ''}, {g['village']} {h} × nevesta {b['name']}, {b['age']} let, {b['village']}"
               f"{(' ' + str(b['houseNo'])) if b.get('houseNo') else ''}; starši ženina: {e['parentsGroom']}; starši neveste: {e['parentsBride']}; priče: {e['witnesses']}; duhovnik {e['priest']}; + {kom}")
    what_en = (f"marriage {dan_en}. {mesec_en} 1885 (entry {row}) — groom {g['name']}, {g['age']} y., {g['status']}"
               f"{', ' + g['stand'] if g.get('stand') else ''}, {g['village']} {h} × bride {b['name']}, {b['age']} y., {b['village']}"
               f"{(' ' + str(b['houseNo'])) if b.get('houseNo') else ''}; groom's parents: {e['parentsGroom']}; bride's parents: {e['parentsBride']}; witnesses: {e['witnesses']}; priest {e['priest']}; + [see-SI]")
    return (
        "  {\n"
        f"    houseNo: \"{h}\",\n"
        "    bookSignature: \"04455\",\n"
        "    year: 1885,\n"
        f"    scan: {scan},\n"
        f"    page: {page},\n"
        f"    whatSi: {json.dumps(what_si, ensure_ascii=False)},\n"
        f"    whatEn: {json.dumps(what_en, ensure_ascii=False)},\n"
        "    status: \"DOCUMENTED\" as const,\n"
        "  },\n"
    )

header = (
    "  // ——— P238: poročna PREDZGOVINA 04455, leto 1885 = 1/13 NOVA LINIJA — (s56–s61 == Pag. 55–60, "
    "22-vpisov-leta-1885-ŠTEVJE-IZ-ZAP-STOLPCA-1.× (zap-2,4,5,6-ULTRA-ZOOM-1:1 — ★★★ VPIS-3-PRESKOČEN-pisarja-ENKRATNO!); "
    "★★★ RESTART-1885 = s56 (tail-1884-vpisi-15–18 + veliko-»1885« + vpis-1-25.-Jän-NA-ISTI-STRANI!) + "
    "★★★ MEJA-1885/86 = s61 (vpis-22-TAIL-22.-Nov + velike-»1 8 8 6« + restart-vpisi-1–3/1886-1:1-z-P84-korpusom!-MISREAD-»1883«-duel!); "
    "★★★ Pag = sken−1-RAZŠIRJENO-na-55–66 (prej-P84-samo-61–66!-s57→56-1:1 + s59→58-1:1 + s61→60-1:1-P80-sidro!); "
    "★★★ ŠTAJERSKA-OBLIKA-RAZREŠENA (blok-bere-se-desno→levo-4-pasovi-krop!-nevesta-≠-ženin-stolpca!) — "
    "7-GRIBLJE-blokov / 7-hiš (h58-×-h34-DVOJNI + h60 + h32 + h71 + h29[~X] + h26 + h13-×-h23[28-DUEL!]-DVOJNI!) + "
    "3-X-OPEN-vas-dueli (h29/h15/h9 — »½-Gütl-Gern/Glob«-vs-GRIBLJE!) + ★★★ PEZDIRC-×3-v-letu (vpis-11-ŽENIN-1:1-krop!-vpis-22-mati!-vpis-7-starši-×2[~]!-+TAIL-15-Mattias-PEZDIREC-Otok-1884!) = PEZDIRC-CONTINUUM-04104-×131→04455! + "
    "★★★ BRINC/BRINEC-MREŽA-ŠIRŠA (vpis-1-mati-roj.-BRUNC[~Brinc!]-h58 + vpis-16-Georg-BRINEC-h26-usnjar + priča-Peter-BRINEC + vpis-17-Marko-BRINEC-50-let!) + "
    "★★★ h71-STRAUS-1885 (P80-sidro-1887-precejeno-1:1!) + DATUM-IZVEN-VRSTI-vpis-7 (7.-Feb-po-8.-Feb!) + LEDERER-usnjarska-veja-×14-vpisov-16–22 + MUC-×3-nit + NAJSTAREJŠI-PAR-97-let (48+49-vpis-21!) + duhovnik-Franz-Dovgan-EDINI-vseh-22! ———\n"
)

i = src.index(ANCHOR)
src = src[:i] + header + "".join(blk(e) for e in grib) + src[i:]
TS.write_text(src, encoding="utf-8")
n = src.count('bookSignature: "04455"')
print(f"vstavljenih 7 blokov P238; 04455-skupaj={n}")
