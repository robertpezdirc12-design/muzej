#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P210 — agregacija 103 vpisov leta 1867 (ŠTEVJE-IZ-VRSTIC-12.×!).
s61 = MEJA-1866/67: restart-'Jänner'-'1867'-VELIKA-LETVICA-KROP-48.-POTRDITEV! + 1–10!
Ordinali-1–103 ČISTO (kontinuiteta-zap-35→36-s63→s64!).
Izhod: /tmp/p210/entries_1867.json"""
import json

TMP = "/tmp/p210"
PLAN = [
    (61, list(range(1, 11)), "z1–z10-restart-'1867'-VELIKA-LETVICA-KROP-48.-POTRDITEV!"),
    (62, list(range(11, 23)), "z11–z22 (12)"),
    (63, list(range(23, 36)), "z23–z35 (13)"),
    (64, list(range(36, 49)), "z36–z48 (13; '2.36'-pripisa-Kurent-marginal!)"),
    (65, list(range(49, 62)), "z49–z61 (13)"),
    (66, list(range(62, 75)), "z62–z74 (13)"),
    (67, list(range(75, 88)), "z75–z87 (13)"),
    (68, list(range(88, 103)), "z88–z102 (15!)"),
    (69, [103], "z103-TAIL-×1 (Primostek-15-Lutblan-80J-ULEDBA-31.Dez→1.Jän — P209-soglasje!)"),
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
        # s69: 1867-tail SAMO (103); vsota + 1868-restart preskoči!
        if sken == 69 and not ("103" in z_raw):
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
out = {"leto": 1867, "vseskupaj": len(entries), "griblje": len(griblje),
       "ord_kaskada": {"meja_1866_67": "s61 (restart-'1867'-VELIKA-LETVICA-KROP-48.-POTRDITEV! — VLM-'1864'-halucinacija-FALSIFICIRANA!)",
                        "stevje_iz_vrstic": len(entries),
                        "ord_stolpci": "s61-'1–10' (×3.5!) + kontinuiteta-zap-35→36 (s63→s64!)"},
       "entries": entries, "griblje_entries": griblje,
       "leadP211": "1866 — s61-GLAVA-tail-NI (1866-konec-je-s60-konec-zap-104!) + s57–s60-ŽE-FETCHAN+VLM (zap-59–104!) → probe-s050–s060!"}
json.dump(out, open(f"{TMP}/entries_1867.json", "w"), ensure_ascii=False, indent=1)
print(f"1867: {len(entries)} vpisov (ordinali-1–103 ČISTO!), Griblje: {len(griblje)}")
for e in griblje:
    print(f"  z{e['z']} s{e['sken']}r{e['vrsta_sken']} h{e.get('hisna')} {str(e.get('ime') or '')[:40]} — {str(e.get('starost') or '')} — {str(e.get('bolezen') or '')[:26]}")
