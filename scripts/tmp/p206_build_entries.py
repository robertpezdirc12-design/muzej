#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P206 — agregacija 73 vpisov leta 1871 (ŠTEVJE-IZ-VRSTIC-8.×!).
s86 = MEJA-1870/71: 1870-tail (zap-64–70 + vsota-'1|8') + restart-'Jänner'-'1871'-z1–z4!
s88 = ordinala-19,19,20–30 (DUP-19 ×2! + LUK-18-pisarski-preskok-iz-s87-zap-17!)
s92 = 1871-tail-×3 (zap-71–73) + vsota → P205-soglasje-1:1!
Izhod: /tmp/p206/entries_1871.json"""
import json

TMP = "/tmp/p206"
# (sken, z-list-po-vrsticah, opomba) — z-po-REALNIH-ordinalih (KROP-forenzika!)
PLAN = [
    (86, [1, 2, 3, 4], "z1–z4-restart-'Jänner'-1871 (tail-64–70-Dec-1870 + vsota-'1|8'-SKIP!)"),
    (87, list(range(5, 18)), "z5–z17 (13)"),
    (88, [19, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], "13-vrstic: DUP-19-×2 (r1-Drugoše-Kumin + r2-Primostek-Klavec!) + ordinala-20–30 — LUK-18-pisarski-preskok! (ord-stolpec-cele-s88-×3.5: 19,19,20–30!)"),
    (89, list(range(31, 45)), "z31–z44 (14; r1-31-Plut-'1871-Mai-25./27.'-letnica-v-celici!)"),
    (90, list(range(45, 59)), "z45–z58 (14)"),
    (91, list(range(59, 71)), "z59–z70 (12)"),
    (92, [71, 72, 73], "z71–z73-TAIL-1871 ('December-1871'-glava-KROP! + vsota-'1|8') → restart-1872-P205!"),
]

entries = []
for sken, z_list, op in PLAN:
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
        # s86: 1870-tail (zap-64–70 + vsota) preskoči!
        z_raw = (x.get("zaporedna") or "").strip().lower()
        if sken == 86 and (z_raw in ("64", "65", "66", "67", "68", "69", "70") or "vsota" in z_raw or "1870" in (x.get("opomba") or "")):
            continue
        # s92: 1871-tail SAMO (71–73); vsota + 1872-restart (zap-1–9) preskoči!
        if sken == 92 and (z_raw in ("1", "2", "3", "4", "5", "6", "7", "8", "9") or "vsota" in z_raw or "1872" in (x.get("opomba") or "")):
            continue
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
        entries.append(x)

griblje = [e for e in entries if any(w in (e.get("vas") or "").lower() for w in ("gribl", "grible", "hrible"))]
out = {"leto": 1871, "vseskupaj": len(entries), "griblje": len(griblje),
       "ord_kaskada": {"meja_1870_71": "s86 (1870-tail-64–70 + 'vsota'-'1|8' + restart-'Jänner'-1871!)",
                        "luknja_18": "ordinala-18-pisarski-preskok (s87-zap-17 → s88-zap-19!) — vzorec-P204-luknje!",
                        "dup_19": "s88-r1-r2-ordinal-19-×2 (Drugoše-Kumin + Primostek-Klavec!) — vzorec-P204-dupkatov!",
                        "stevje_iz_vrstic": len(entries)},
       "entries": entries, "griblje_entries": griblje,
       "leadP207": "1870 — s86-tail-×7 (zap-64–70-Dec-1870 + vsota-'1|8')-ŽE-VLM-PREBRANA → probe-s078–s086!"}
json.dump(out, open(f"{TMP}/entries_1871.json", "w"), ensure_ascii=False, indent=1)
print(f"1871: {len(entries)} vpisov (ordinali-1–73; LUK-18 + DUP-19!), Griblje: {len(griblje)}")
for e in griblje:
    print(f"  z{e['z']} s{e['sken']}r{e['vrsta_sken']} h{e.get('hisna')} {str(e.get('ime') or '')[:42]} — {str(e.get('starost') or '')} — {str(e.get('bolezen') or '')[:30]}")
