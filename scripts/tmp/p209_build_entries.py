#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P209 — agregacija 80 vpisov leta 1868 (ŠTEVJE-IZ-VRSTIC-11.×!).
s69 = MEJA-1867/68: tail-×1 (zap-103-Primostek-ULEDBA-31.Dez→1.Jän!) + 'vsota'-4-delna-'1|8|6|8' + restart-'1.-Jänner-1868'-1–10!
Ordinali-1–80 ČISTO (3.-leto-zapored!): ord-stolpec-s69-'1–10' + s75-'77–80' (P208!).
Izhod: /tmp/p209/entries_1868.json"""
import json

TMP = "/tmp/p209"
PLAN = [
    (69, list(range(1, 11)), "z1–z10-restart-'1.-Jänner-1868' (tail-103 + vsota-'1|8|6|8'-SKIP!)"),
    (70, list(range(11, 24)), "z11–z23 (13)"),
    (71, list(range(24, 37)), "z24–z36 (13)"),
    (72, list(range(37, 50)), "z37–z49 (13; VLM-'1871'-letnica-MISREAD!)"),
    (73, list(range(50, 64)), "z50–z63 (14)"),
    (74, list(range(64, 77)), "z64–z76 (13)"),
    (75, list(range(77, 81)), "z77–z80-TAIL (4: Hrovat-41 + Hrovćan-35 + Tome-15 + Jakofčič-13 — P208-soglasje-1:1!)"),
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
        z_raw = (x.get("zaporedna") or "").strip().lower()
        # s69: 1868-restart SAMO (1–10); tail-103 + vsota preskoči!
        if sken == 69 and (z_raw in ("103",) or "vsota" in z_raw or "1867" in (x.get("opomba") or "") or "103" in z_raw):
            continue
        # s75: 1868-tail SAMO (77–80); vsota + 1869-restart (1–9) preskoči!
        if sken == 75 and (z_raw in ("1", "2", "3", "4", "5", "6", "7", "8", "9") or "vsota" in z_raw or "1869" in (x.get("opomba") or "")):
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
out = {"leto": 1868, "vseskupaj": len(entries), "griblje": len(griblje),
       "ord_kaskada": {"meja_1867_68": "s69 (1867-tail-×1-zap-103-Primostek-ULEDBA! + 'vsota'-4-delna-'1|8|6|8' + restart-'1.-Jänner-1868'!)",
                        "stevje_iz_vrstic": len(entries),
                        "ord_stolpci": "s69-'1–10' (×3.5!) + s75-'77–80' (P208!)"},
       "entries": entries, "griblje_entries": griblje,
       "leadP210": "1867 — s69-tail-×1-ŽE-VLM-PREBRANA (zap-103-Primostek-15-Lutblan-80J-ULEDBA-31.Dez→1.Jän!) + s64–s68-ŽE-FETCHAN+VLM (zap-36–102!) → probe-s057–s069!"}
json.dump(out, open(f"{TMP}/entries_1868.json", "w"), ensure_ascii=False, indent=1)
print(f"1868: {len(entries)} vpisov (ordinali-1–80 ČISTO!), Griblje: {len(griblje)}")
for e in griblje:
    print(f"  z{e['z']} s{e['sken']}r{e['vrsta_sken']} h{e.get('hisna')} {str(e.get('ime') or '')[:40]} — {str(e.get('starost') or '')} — {str(e.get('bolezen') or '')[:26]}")
