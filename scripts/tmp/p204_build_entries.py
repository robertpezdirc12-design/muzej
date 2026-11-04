#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P204 — agregacija 212 vpisov leta 1873 (ŠTEVJE-IZ-VRSTIC-6.×!).
Struktura per sken (ordinal-preslikava KROP-potrjena):
  s102: 12 vpisov (VLM vrste 1–12; vrsta0 = glava-leta '1873. Incipit annus Domini'!)
  s103 == s104: DOUBLE-SCAN (pag-×2!) → samo s103: 12 vpisov (z13–z24)
  s105: 14 vpisov (r1-ordinal-24 = DUPKAT-ordinal!)
  s106: 12 vpisov (r1-ordinal-37 = DUPKAT; '1873. Jüni'-glava-v-r1!)
  s107: 13 vpisov (z49–z61)
  s108: 13 vpisov (r1-ordinal-61 = DUPKAT; 'August'-glava-v-r1!)
  s109: 13 (z74–z86) · s110: 13 (z87–z99) · s111: 12 · s112: 12 · s113: 13 (124–136)
  s114: 13 (137–140 + 145–153; luknje-ordinalov-141–144-pisarske!)
  s115: 12 (153–164; r1-153-DUPKAT; '1873. October'-glava-v-r1!)
  s116: 12 · s117: 13 · s118: 14 (190–203)
  s119: tail-9 (P203-tail-vrste 1–9 == z204–z212 1:1; 'December 1873'-glava-v-z204!)
Dupkati-ordinali: 24, 37, 61, 153 (4!) + luknje: 141–144 (4!) → neto-0 → Σ-vrstic 212 == ordinal-end 212!
Izhod: /tmp/p204/entries_1873.json (entries + griblje + tail_1872 + leadP205)."""
import json, os

TMP = "/tmp/p204"
OUT = f"{TMP}/entries_1873.json"

# preslikava: sken → (offset_z, vrste_VLM, opomba-ordinala)
PLAN = [
    (102, 1, 12, "z1–z12; r0=glava-leta"),
    (103, 13, 12, "z13–z24; DOUBLE-SCAN s104!"),
    (105, 25, 14, "z25–z38-stevje; ord-r1=24-DUPKAT"),
    (106, 39, 12, "z39–z50-stevje; ord-r1=37-DUPKAT; '1873. Jüni'-glava"),
    (107, 52, 13, "z52–z64-stevje; ord 49–61"),
    (108, 65, 13, "z65–z77-stevje; ord-r1=61-DUPKAT; 'August'-glava"),
    (109, 78, 13, "z78–z90-stevje; ord 74–86"),
    (110, 91, 13, "z91–z103-stevje; ord 87–99"),
    (111, 104, 12, "z104–z115-stevje; ord 100–111"),
    (112, 116, 12, "z116–z127-stevje; ord 112–123"),
    (113, 128, 13, "z128–z140-stevje; ord 124–136"),
    (114, 141, 13, "z141–z153-stevje; ord 137–140+145–153 (luknje 141–44!)"),
    (115, 154, 12, "z154–z165-stevje; ord 153–164; r1-DUPKAT-153; '1873. October'-glava"),
    (116, 166, 12, "z166–z177-stevje; ord 165–176"),
    (117, 178, 13, "z178–z190-stevje; ord 177–189"),
    (118, 191, 14, "z191–z204-stevje; ord 190–203"),
]

def main():
    entries = []
    for sken, z_start, n_vrst, op in PLAN:
        d = json.load(open(f"{TMP}/vlm-page/s{sken}.json"))
        vrste = d.get("vrstice", [])
        # preskoči glavne-vrste (ime='Anno Domini...' ali vrsta=0 brez vas/datumov)
        realne = []
        for x in vrste:
            ime = (x.get("ime") or "").strip()
            vas = (x.get("vas") or "").strip()
            mes = (x.get("mesec") or "").strip()
            smrt = (x.get("smrt") or "").strip()
            pokop = (x.get("pokop") or "").strip()
            if not ime and not vas:
                continue  # prazna vrsta
            if not mes and not smrt and not pokop:
                continue  # glava-vrsta ('Anno Domini'/'Incipit' — brez datuma!)
            realne.append(x)
        if len(realne) != n_vrst:
            print(f"⚠ s{sken}: pričakovano {n_vrst}, najdeno {len(realne)} realnih vrstic (VLM n={len(vrste)})")
        for i, x in enumerate(realne[:n_vrst]):
            x = dict(x)
            x["z"] = z_start + i
            x["sken"] = sken
            x["pag"] = sken - 5
            x["vrsta_sken"] = i + 1
            x["ord_opomba"] = op
            entries.append(x)
    # s119-tail: P203-tail_1873 vrste 1–9 (KROP-verificirane v P204 krops!)
    p203 = json.load(open("/tmp/p203/entries_1874.json"))
    tail = p203.get("tail_1873", [])
    for i, x in enumerate(tail):
        x = dict(x)
        if x.get("vrsta_sken", i + 1) <= 9:
            x["z"] = 204 + i
            x["pag"] = 114
            entries.append(x)
    # zadnji tail-vpis (vrsta 10 = Jän-1874 Podiner) NE spada v 1873!

    griblje = [e for e in entries if "gribl" in (e.get("vas") or "").lower()
               or "grible" in (e.get("vas") or "").lower()
               or "hrible" in (e.get("vas") or "").lower()]

    out = {
        "leto": 1873,
        "vseskupaj": len(entries),
        "griblje": len(griblje),
        "ord_kaskada": {"dupkati": [24, 37, 61, 153], "luknje": [141, 142, 143, 144],
                        "double_scan": "s103==s104", "ordinal_end": 212, "stevje_iz_vrstic": 212},
        "entries": entries,
        "griblje_entries": griblje,
        "tail_1872_hint": "s101: 9 vrstic Dez-1872 (zap 102–110) + 'finis' — P205-lead!",
        "leadP205": {"sken": 101, "pag": 96, "vrste": 9, "mesec": "December 1872",
                     "opomba": "TAIL-1872-na-s101 (zap 102–110); 'finis'-zaključek-pred-1873-mejo-s102!"},
    }
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f"1873: {len(entries)} vpisov (z1–z{len(entries)}), Griblje: {len(griblje)}")
    for e in griblje:
        print(f"  z{e['z']} s{e['sken']}r{e['vrsta_sken']} h{e.get('hisna')} {str(e.get('ime') or '')[:40]} — {str(e.get('starost') or '')} — {str(e.get('bolezen') or '')[:30]}")

if __name__ == "__main__":
    main()
