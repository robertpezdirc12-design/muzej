#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P205 — agregacija 110 vpisov leta 1872 (ŠTEVJE-IZ-VRSTIC-7.×!).
s92 = MEJA-1871/72: 1871-tail (vrste 71–73-VLM-[?] + 'vsota') + restart-1–9-'Jänner' 1872!
Izhod: /tmp/p205/entries_1872.json"""
import json, re

TMP = "/tmp/p205"
# (sken, z_start, n_vrst, opomba) — s92: samo-restart-del (z1–z9); 1871-tail-NE-1872!
PLAN = [
    (92, 1, 9, "z1–z9-restart-'Jänner'-1872 (VLM-13-vrstic-vklj.-1871-tail-71–73 + vsota!)"),
    (93, 10, 11, "z10–z20"),
    (94, 21, 12, "z21–z32 (VLM-13-vklj.-'31[~]/32[~]'-duplji!)"),
    (95, 33, 12, "z33–z44"),
    (96, 45, 11, "z45–z55"),
    (97, 56, 11, "z56–z66"),
    (98, 67, 14, "z67–z80"),
    (99, 81, 13, "z81–z93"),
    (100, 94, 12, "z94–z105"),
    (101, 106, 9, "z106–z114-tail-Dez!"),
]

entries = []
for sken, z_start, n_vrst, op in PLAN:
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
        # s92: 1871-tail vrste (zap-'71'/'72'/'73'/'vsota') preskoči!
        z_raw = (x.get("zaporedna") or "").strip()
        if sken == 92 and (z_raw in ("71", "72", "73") or "vsota" in z_raw.lower() or "1871" in (x.get("opomba") or "")):
            continue
        realne.append(x)
    if len(realne) != n_vrst:
        print(f"⚠ s{sken}: pričakovano {n_vrst}, najdeno {len(realne)} (VLM n={len(vrste)})")
    for i, x in enumerate(realne[:n_vrst]):
        x = dict(x)
        x["z"] = z_start + i
        x["sken"] = sken
        x["pag"] = sken - 5
        x["vrsta_sken"] = i + 1
        x["ord_opomba"] = op
        entries.append(x)

griblje = [e for e in entries if any(w in (e.get("vas") or "").lower() for w in ("gribl", "grible", "hrible"))]
out = {"leto": 1872, "vseskupaj": len(entries), "griblje": len(griblje),
       "ord_kaskada": {"meja_1871_72": "s92 (1871-tail-71–73 + 'vsota' + restart-'Jänner'-1872!)",
                        "double_scan": None, "stevje_iz_vrstic": len(entries)},
       "entries": entries, "griblje_entries": griblje,
       "leadP206": "1871 — s92-1871-tail-×3-ŽE-VLM-PREBRANA (vrste-71–73!) → probe-s084–s092!"}
json.dump(out, open(f"{TMP}/entries_1872.json", "w"), ensure_ascii=False, indent=1)
print(f"1872: {len(entries)} vpisov (z1–z{len(entries)}), Griblje: {len(griblje)}")
for e in griblje:
    print(f"  z{e['z']} s{e['sken']}r{e['vrsta_sken']} h{e.get('hisna')} {str(e.get('ime') or '')[:40]} — {str(e.get('starost') or '')} — {str(e.get('bolezen') or '')[:28]}")
