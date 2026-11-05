#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P211 — agregacija 104 vpisov leta 1866 (ŠTEVJE-IZ-VRSTIC-13.×!).
s51 = MEJA-1865/66: tail-1865 (z65/z66) + PREČRTANA-PRAZNA-VRSTA (Schlangenlinien) + restart-'1866'-VELIKA-LETVICA-KROP-49.-POTRDITEV!
DOUBLE-SCAN-4.×: s53==s54 (md5-različna 450719B/470425B, vsebina-1:1 po-imenih+datumih!) → s54-SKIP.
Vrstna aritmetika: 8+12+13+12+13+13+11+12+10 = 104; ordinali-1–104 ČISTO-5.-leto-zapored!
KROP-korekcije VGRAJENE: z22-h41+Hušić (HUESTIČ-1903-h41-kontinuiteta!), z34/z35-DVOJČKA,
z41-h14+starost-duel, z58-ULEDBA-Juli-1, z90-Totgeborenes-Kind-Požek (2-OSEBI-FALSIFICIRAN!),
z98-Missgeborenes-Kind-d.-Janez-Pezdirc ('Anton'-FALSIFICIRAN!).
Izhod: /tmp/p211/entries_1866.json"""
import json

TMP = "/tmp/p211"
PLAN = [
    (51, list(range(1, 9)), "z1–z8-restart-'1866'-VELIKA-LETVICA-KROP-49.-POTRDITEV! (tail-1865-z65/z66 + prečrtana-67-SKIP!)", 4),
    (52, list(range(9, 21)), "z9–z20 (12)"),
    (53, list(range(21, 34)), "z21–z33 (13; Double-Scan-4.×: s54==s53-SKIP!)"),
    (55, list(range(34, 46)), "z34–z45 (12; z34/z35-DVOJČKA-Totgeborenes-Žunič!)"),
    (56, list(range(46, 59)), "z46–z58 (13; z58-ULEDBA-Juni-29→Juli-1!)"),
    (57, list(range(59, 72)), "z59–z71 (13)"),
    (58, list(range(72, 83)), "z72–z82 (11)"),
    (59, list(range(83, 95)), "z83–z94 (12; z90-Totgeborenes-Požek-2-OSEBI-FALSIF!)"),
    (60, list(range(95, 105)), "z95–z104 (10; z98-Missgeborenes-Kind-Janez-Pezdirc!)"),
]

# KROP-korekcije (vgrajene za reproducibilnost!) — ključ: z
KROP = {
    22: {"hisna": "41", "ime": "Maria Hušić [~Huestič/Kusić?]",
         "starost": "22 let (22 Jahre)", "bolezen": "Abzehrung",
         "stan": "¼ güblerštofa [~griblarštofa]",
         "_opomba": "KROP-izrez: h41-ČISTO (4-z-zanko+1!) + VLM-B + ★ HUESTIČ-1903-poroka: Maria-HUESTIČ-GRIBLJE-41-½-griblarštofa + oče-Matthias-¼-griblar = h41+¼-gübler-KONTINUITETA! (VLM-A-h11 + prejšnja-seja-'Kusić'-FALSIFICIRANA!)"},
    34: {"ime": "Totgeborenes Kind v. Josef Žunič", "starost": "2 dni [~D.]",
         "_opomba": "KROP-izrez: 'Totgeborenes Kind v. Josef Zunic(i)' — VLM-'Posmrhlanski'-halucinacija-FALSIFICIRANA! Vranoviče h19, April 22./23."},
    35: {"ime": "Totgeborenes Kind v. (Josef) Žunič [ditto]",
         "_opomba": "KROP-izrez: ditto-Vranoviče-h19, pokop-23. — DVOJČKA-MRTVOROJENA!"},
    41: {"hisna": "14", "starost": "19 [enota-nečitljiva! duel: VLM-'19-dni[?]' / KROP-'1½-let[?]' / stara-seja-'1-leto']",
         "stan": "unehelich Kind ¼ gübler[?]",
         "_opomba": "KROP-izrezi: h14-ČISTO (tight-4×!) + ★ Pezdirc-h14-kontinuiteta (z66-tail-1865-Maria-Pezdirc-h14!) — starost-duel-HONEST"},
    58: {"pokop": "1.", "mesec_pokop": "Juli", "stan": "½ [~¼] güblerštocha",
         "_opomba": "★★★ ULEDBA-#10-9.INSTANCE: smrt-29-Juni → pokop-1-Juli (KROP-'Juli 1'-ČISTO!) — cf. P209-z103-31.Dez→1.Jän + P203/P202-ULEDBA"},
    90: {"ime": "Totgeborenes [~Taubgebarend?] Kind v. Mark. Požek", "hisna": "58",
         "_opomba": "★★★ KROP-4.2×-izrez: 'Taųbgebarend(?) Kind / v. Mark. Požek' — 2-OSEBI-HIPOTEZA-FALSIFICIRANA (mrtvorojen-otrok-od-Marka-POŽKA!) + POŽEK-h58-kontinuiteta (P192-h58-POŽEK!) — VLM-'Laufgrabend-žival' + KROP-'Laurentius-Ažić+še-Marjeta'-obe-FALSIFICIRANI!"},
    98: {"ime": "Missgeborenes Kind d. Janez Pezdirc", "starost": "[~¼ J.?]",
         "_opomba": "★★★ KROP-4.2×-izrez: 'Missgeborenes Kind d. / ¼ J.(?) Janez Pezdarc' — P210-tail-'Anton-dešk'-halucinacija-FALSIFICIRANA! (oče-Janez-PEZDIRC-h53!)"},
}

entries = []
for item in PLAN:
    sken, z_list, op = item[0], item[1], item[2]
    min_vrsta = item[3] if len(item) > 3 else 1
    d = json.load(open(f"{TMP}/vlm-page/s{sken}.json"))
    vrste = d.get("vrstice", [])
    realne = []
    for x in vrste:
        ime = (x.get("ime") or "").strip()
        vas = (x.get("vas") or "").strip()
        mes = (x.get("mesec") or "").strip()
        smrt = (x.get("smrt") or "").strip()
        pokop = (x.get("pokop") or "").strip()
        if not ime and not vas: continue
        if not mes and not smrt and not pokop: continue
        # s51: tail-1865 (vrsta 1–2) + prečrtana-67 (vrsta 3) preskoči!
        if sken == 51 and (x.get("vrsta") or 0) < min_vrsta: continue
        realne.append(x)
    if len(realne) != len(z_list):
        print(f"⚠ s{sken}: pričakovano {len(z_list)}, najdeno {len(realne)} (VLM n={len(vrste)})")
    for i, x in enumerate(realne[:len(z_list)]):
        x = dict(x)
        x["z"] = z_list[i]
        x["sken"] = sken
        x["pag"] = sken - 5
        x["vrsta_sken"] = i + 1
        x["ord_opomba"] = op
        k = KROP.get(x["z"])
        if k:
            for kk, vv in k.items():
                if kk == "_opomba": x["krop_opomba"] = vv
                else: x[kk] = vv
            x["krop"] = True
        entries.append(x)

griblje = [e for e in entries if any(w in (e.get("vas") or "").lower() for w in ("gribl", "grible", "hrible"))]
out = {"leto": 1866, "vseskupaj": len(entries), "griblje": len(griblje),
       "ord_kaskada": {"meja_1865_66": "s51 (tail-1865-z65/z66-KROP + prečrtana-67-Schlangenlinien-SKIP + restart-'1866'-VELIKA-LETVICA-KROP-49.-POTRDITEV!)",
                        "double_scan": "s53==s54-4.× (md5-različna-450719B/470425B — vsebina-1:1: zap-21–33-enako, vas-13/13, imena-13/13, smrti-13/13!) → s54-SKIP (cf. P204-s103==s104!)",
                        "stevje_iz_vrstic": len(entries),
                        "vrstna_aritmetika": "8+12+13+12+13+13+11+12+10 = 104",
                        "ordinali": "1–104-ČISTO-BREZ-luknje/dupa — 5.-LETO-ZAPORED!"},
       "entries": entries, "griblje_entries": griblje,
       "krop_dokazi": {"glava": "arb_s51_glava-'1866 Jänner'-49.-POTRDITEV-invariante!",
                        "z22": "h41+Hušić (HUESTIČ-1903-h41-¼-griblar-KONTINUITETA!)",
                        "z34z35": "DVOJČKA-Totgeborenes-Kind-v.-Josef-Žunič-Vranoviče-h19",
                        "z41": "h14-Pezdirc-kontinuiteta-z-z66-tail!",
                        "z58": "ULEDBA-#10-9.INSTANCE-Juli-1",
                        "z90": "Totgeborenes-Kind-v.-Mark.-Požek-h58 (2-OSEBI-FALSIFICIRAN!)",
                        "z98": "Missgeborenes-Kind-d.-Janez-Pezdirc-h53 ('Anton'-FALSIFICIRAN!)"},
       "leadP212": "1865 — s50-ŽE-FETCHAN+VLM (zap-50–64: 15-vrstic-1865-kontekst!) + s51-TAIL-z65/z66-ŽE-KROP (z66-Griblje-h14-Maria-Pezdirc-66J!) → probe-s042–s050!"}
json.dump(out, open(f"{TMP}/entries_1866.json", "w"), ensure_ascii=False, indent=1)
print(f"1866: {len(entries)} vpisov (ordinali-1–104 ČISTO-5.-leto!), Griblje: {len(griblje)} / {len(set(str(e.get('hisna')) for e in griblje))}-hiš")
for e in griblje:
    print(f"  z{e['z']:>3} s{e['sken']}r{e['vrsta_sken']:>2} pag{e['pag']} h{str(e.get('hisna')):4} {str(e.get('ime') or '')[:44]} — {str(e.get('starost') or '')[:22]} — {str(e.get('bolezen') or '')[:22]}")
