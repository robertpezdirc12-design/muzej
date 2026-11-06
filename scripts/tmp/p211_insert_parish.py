#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P211 — vstavi 13-GRIBLJE-blokov (04106, leto 1866) v parish.ts PRED P210-sekcijo."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/muzej-backup/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P210: mrliška PREDZGODOVINA 04106, leto 1867"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert src.count('year: 1866,') == 0, "1866-bloki-že-obstajajo?!"

E = json.load(open("/tmp/p211/entries_1866.json"))
grib = E["griblje_entries"]
assert len(grib) == 13, f"grib={len(grib)}"

KOM = {
    19: "★ h19-1.-GRIBLJE-dokaz (Anna-Ginić[~Vinic?]-61-J — hišna-DUEL-[?]-mlajša-potrditev-čaka!)",
    22: "★★★ HUESTIČ-h41-KONTINUITETA (Maria-Hušić[~Huestič/Kusić?]-22-J-¼-güblerštofa — 1903-poroka-Maria-HUESTIČ-GRIBLJE-41-½-griblarštofa + oče-Matthias-¼-griblar = 37-let-globoko!) + hiša-DUEL-rešen-KROP (VLM-A-'11'-FALSIFICIRAN — izrez-'4-z-zanko+1'-ČISTO!)",
    41: "★★★ PEZDIRC-h14-KONTINUITETA (Mathias-unehelich-Kind-¼-gübler[?] — z66-tail-1865-Maria-Pezdirc-h14!) + starost-DUEL-HONEST ('19'-ČISTO-ampak-enota-nečitljiva: VLM-'19-dni' / KROP-'1½-let'!)",
    48: "★★★ h34-FILAK-×2-#1 (Katarina-6½-J-Marbmil[~])",
    50: "★ h3-nit (Štefan-Štrucelj[~]-5-mes — cf. 1867-z98-h3-Papic!)",
    58: "★★★ ULEDBA-#10-9.INSTANCE (Maria-Želko-4-mes — smrt-29-JUNI→pokop-1-JULI — KROP-'Juli-1'-ČISTO! — cf. P209-z103-31.Dez→1.Jän!) + h1-nit + ½-güblerštocha",
    63: "★ h37-nit (Mathias-Hrovatič[~Hrušič?]-44-J — HROVAT/HRUŠ-grafia!)",
    64: "★ h13-nit (Jura-Zakotnik[~Jure-Zakotnič?]-2-J-Griža — cf. h13-JAKOFČIČ-nit-1867!)",
    78: "★★★ KLOBUČAR-×2-v-4-dneh-#1 (Maria-h47-3½-tedna — Erschfallene[?]!)",
    79: "★★★ KLOBUČAR-×2-v-4-dneh-#2 (Maria-h48-9-dni[~4½-t?] — 2-RAZLIČNI-hiši!)",
    80: "★★★ h34-FILAK-×2-#2 (Josip[~Filip]-1-teden-Frisen — 2-otroka-isti-hiši-v-3-mesecih!)",
    90: "★★★ TOTGEBORENES-v.-Mark.-POŽEK-h58 (KROP-4.2×-'Taųbgebarend(?) Kind / v. Mark. Požek' — 2-OSEBI-HIPOTEZA-FALSIFICIRANA! — POŽEK-h58-kontinuiteta-P192!) — smrt-'—'-pokop-2.-Nov-črtice-vsi-stolpci!",
    98: "★★★ MISSGEBORENES-Kind-d.-Janez-PEZDIRC-h53 (KROP-4.2× — P210-tail-'Anton'-halucinacija-FALSIFICIRANA!) — '¼-J.[?]'-starost",
}

def gen_block(e):
    z = e["z"]
    ime = (e.get("ime") or "?").strip()
    stan = (e.get("stan") or "").strip()
    starost = (e.get("starost") or "?").strip()
    mesec = (e.get("mesec") or "").strip()
    smrt = (e.get("smrt") or "").strip()
    pokop = (e.get("pokop") or "").strip()
    bolezen = (e.get("bolezen") or "?").strip()
    kom = KOM.get(z, "")
    mes_dejansko = {"Februar": "Feber", "Januar": "Jänner", "December": "Dezember", "Junij": "Juni",
                    "Martii": "März", "Maii": "Mai", "Julii": "July"}.get(mesec.split()[0] if mesec else "", mesec.split()[0] if mesec else "")
    what_si = f"umrl(a) {ime}"
    if stan: what_si += f", '{stan}'"
    what_si += f", {starost} ({mes_dejansko} {smrt}, pokop {pokop}) — {bolezen}"
    if kom: what_si += f"; + {kom}"
    if e.get("krop_opomba"): what_si += f"; [KROP: {e['krop_opomba']}]"
    what_si += f" + [z{z}]"
    hn = str(e.get('hisna', '?')).split()[0]
    return f"""  {{
    houseNo: "{hn}",
    bookSignature: "04106",
    year: 1866,
    scan: {e['sken']},
    page: {e['pag']},
    whatSi: "{what_si.replace('"', "'")}",
    whatEn: "died {ime}, {starost} ({mes_dejansko} {smrt}, buried {pokop}) — {bolezen}; + [see-SI] + [z{z}]",
    status: "DOCUMENTED",
  }},
"""

header = """  // ——— P211: mrliška PREDZGODOVINA 04106, leto 1866 = 20. leto PREDZGODOVINSKE LINIJE (s051–s060 == Pag. 46–55, z1–z104 = 104 vpisov — ŠTEVJE-IZ-VRSTIC-13.× (ordinali-1–104-ČISTO — 5.-LETO-ZAPORED-BREZ-luknje/dupa!; vrstna-aritmetika 8+12+13+12+13+13+11+12+10; meseci J8+F5+M10+A12+M10+J13-MAX+J9+A7+S7+O7+N11+D4; pag = sken−5; SANDBOX-RESET-REGENERACIJA: 2×-neodvisna-prenosa-md5-11/11 + vsebinska-križ-s60↔P210-tail-zap-95–104-10/10!) — 13-GRIBLJE-blokov / 12 hiš (h34-×2-FILAK!) + ★★★ DOUBLE-SCAN-4.×: s53==s54 (md5-različna-450719B/470425B — vsebina-1:1-po-imenih-13/13!) → s54-SKIP (cf. P204-s103==s104!) + ★★★ MEJA-1865/66-s51 (tail-1865-z65/z66-KROP: z66-Griblje-h14-Maria-Pezdirc-66J! + PREČRTANA-PRAZNA-VRSTA-67-Schlangenlinien-SKIP + restart-'Jänner'-'1866'-VELIKA-LETVICA-KROP-49.-POTRDITEV-invariante!) + ★★★ DVOJČKA-MRTVOROJENA-z34/z35-'Totgeborenes-Kind-v.-Josef-Žunič'-Vranoviče-h19 (VLM-halucinaciji-FALSIFICIRANI!) + ★★★ ULEDBA-#10-9.INSTANCE-z58 (29-JUNI→1-JULI-KROP-'Juli-1'-ČISTO!) + ★★★ HUESTIČ-h41-KONTINUITETA-z22 (Maria-Hušić[~Huestič]-¼-güblerštofa → 1903-Maria-HUESTIČ-h41-37-let!) + ★★★ PEZDIRC-h14-KONTINUITETA-z41 (+z98-h53-Missgeborenes-d.-Janez-Pezdirc — 'Anton'-FALSIFICIRAN!) + ★★★ POŽEK-h58-z90-Totgeborenes (2-OSEBI-FALSIFICIRAN-KROP-4.2×!) + ★★★ otroška-umrljivost-77%-10/13-GRIBLJE + KLOBUČAR-×2-v-4-dneh + FILAK-h34-×2 + ½/¼-GÜBLER-leksikon ———
"""

blocks = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, header + blocks + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
print(f"OK — 1866-bloki: {len(grib)}")
