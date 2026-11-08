#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P208 — agregacija 76 vpisov leta 1869 (ŠTEVJE-IZ-VRSTIC-10.×!).
s75 = MEJA-1868/69: tail-×4 (zap-77–80) + 'vsota'-'1|8'-3.× + '1869-Jänner'-glava (KROP-47.!) + restart-1–9!
Ordinali-1–76 ČISTO (2.-leto-zapored!): ord-stolpci-×3.5 s75-'77–80→1–9' + s80-'65–76'.
Izhod: /tmp/p208/entries_1869.json"""
import json

TMP = "/tmp/p208"
PLAN = [
    (75, list(range(1, 10)), "z1–z9-restart-'1869-Jänner' (KROP-47.-potrditev! tail-77–80 + vsota-'1|8'-3.×-SKIP!)"),
    (76, list(range(10, 24)), "z10–z23 (14)"),
    (77, list(range(24, 38)), "z24–z37 (14)"),
    (78, list(range(38, 51)), "z38–z50 (13)"),
    (79, list(range(51, 65)), "z51–z64 (14)"),
    (80, list(range(65, 77)), "z65–z76-KONEC-LETOVNIKA (12; 'valovita-črta'-KROP-P207!)"),
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
        # s75: 1869-restart SAMO (1–9); tail-77–80 + vsota preskoči!
        if sken == 75 and (z_raw in ("77", "78", "79", "80") or "vsota" in z_raw or "1868" in (x.get("opomba") or "")):
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
out = {"leto": 1869, "vseskupaj": len(entries), "griblje": len(griblje),
       "ord_kaskada": {"meja_1868_69": "s75 (1868-tail-×4-zap-77–80 + 'vsota'-'1|8'-3.× + '1869-Jänner'-glava-KROP-47.-potrditev + restart-1–9!)",
                        "konec_1869": "s80-'valovita-črta'-KROP (P207-potrjeno!)",
                        "stevje_iz_vrstic": len(entries),
                        "ord_stolpci": "s75-'77,78,79,80→1–9' + s80-'65–76' (×3.5!)"},
       "entries": entries, "griblje_entries": griblje,
       "leadP209": "1868 — s75-tail-×4-ŽE-VLM-PREBRANA (zap-77–80: Hrovat-41 + Hrovćan-35 + Tome-15 + Jakofčič-13!) + s71–s74-ŽE-FETCHAN+VLM (zap-24–76-kontekst!) → probe-s064–s075!"}
json.dump(out, open(f"{TMP}/entries_1869.json", "w"), ensure_ascii=False, indent=1)
print(f"1869: {len(entries)} vpisov (ordinali-1–76 ČISTO!), Griblje: {len(griblje)}")
for e in griblje:
    print(f"  z{e['z']} s{e['sken']}r{e['vrsta_sken']} h{e.get('hisna')} {str(e.get('ime') or '')[:40]} — {str(e.get('starost') or '')} — {str(e.get('bolezen') or '')[:26]}")
