#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P207 — agregacija 70 vpisov leta 1870 (ŠTEVJE-IZ-VRSTIC-9.×!).
s80 = KONEC-LETOVNIKA-1869 ('valovita-črta'!); s81 = velika-letnica-'1870'-+restart-1 (KROP-×2!).
Ordinali-1–70 ČISTO (BREZ-luknje/dupa!): ord-stolpci-×3.5 (recept-P206): s83-'25–37' (celostanska-zamik-−2!), s84-'38–50'.
Izhod: /tmp/p207/entries_1870.json"""
import json

TMP = "/tmp/p207"
# (sken, z-list-po-vrsticah, opomba)
PLAN = [
    (81, list(range(1, 12)), "z1–z11-restart (velika-letnica-'1870'-KROP-×2! tail-1869-SKIP!)"),
    (82, list(range(12, 25)), "z12–z24 (13)"),
    (83, list(range(25, 38)), "z25–z37 (13) — ord-stolpec-'25,26,...,37'! (celostanska-zap-'23–35'-zamik-−2! 36/37-TUKAJ — NI-luknje!)"),
    (84, list(range(38, 51)), "z38–z50 (13) — ord-stolpec-'38–50'"),
    (85, list(range(51, 64)), "z51–z63 (13)"),
    (86, list(range(64, 71)), "z64–z70-TAIL (7) — 'vsota'-'1|8' + restart-1871-SKIP! (P206-soglasje!)"),
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
        # s86: 1870-tail SAMO (64–70); vsota + 1871-restart (1–4) preskoči!
        if sken == 86 and (z_raw in ("1", "2", "3", "4") or "vsota" in z_raw or "1871" in (x.get("opomba") or "")):
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
out = {"leto": 1870, "vseskupaj": len(entries), "griblje": len(griblje),
       "ord_kaskada": {"meja_1869_70": "s80-KONEC-LETOVNIKA-1869 ('valovita-črta'-KROP! + '1869'-VLM-misread-'1849'!) → s81-velika-letnica-'1870'-×2-KROP + restart-1!",
                        "stevje_iz_vrstic": len(entries),
                        "ord_stolpci": "s83-'25–37' + s84-'38–50' (×3.5, recept-P206! celostanska-s83-zamik-−2!)"},
       "entries": entries, "griblje_entries": griblje,
       "leadP208": "1869 — s80-TAIL-konec-LETOVNIKA ('valovita-črta'!) ŽE-VLM-PREBRANA (zap-65–76!) + s78/s79-ŽE-FETCHAN+VLM (zap-38–64!) → probe-s071–s080!"}
json.dump(out, open(f"{TMP}/entries_1870.json", "w"), ensure_ascii=False, indent=1)
print(f"1870: {len(entries)} vpisov (ordinali-1–70 ČISTO!), Griblje: {len(griblje)}")
for e in griblje:
    print(f"  z{e['z']} s{e['sken']}r{e['vrsta_sken']} h{e.get('hisna')} {str(e.get('ime') or '')[:42]} — {str(e.get('starost') or '')} — {str(e.get('bolezen') or '')[:28]}")
