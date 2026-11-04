#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P203 — build entries 1874 (ŠTEVJE-IZ-VRSTIC, recept-5.×!) iz VLM-branj /tmp/p203/vlm-page.
Okno: s119-glava ('18 74. Jänner'-VELIKA-glava — MEJA-1873/74!) do s127-z10 (Dez-1874).
s123 = DVOKRAT-SKANA-ISTA-STRAN-kot-s124 (pag 118-×2! lekcija-#18-DOUBLE-SCAN-2.×!) → SKIP!
Preslikava-pag: s118–s123 = sken−5, s124+ = sken−6 (natisnjene-št.-strani-×7-preverjene!).
94-vpisov: 3+11+16+15+14+13+12+10 = 94 ✓ (s123-duplikat-izpuščen!).
KROP-korekcije-×8: Lunič-h11-16-dni + Brime-h24/h28-×2 + Tilak-h39 (NE-h34!) + Brune-28/30-69J[?56¾]
+ Križan-h33 (NE-h83!) + Logar-h57 (NE-h8! + modra-'12'-annotacija!) + Krič-h19 + Miler-h29!
Izhod: /tmp/p203/entries_1874.json"""
import json

VP = "/tmp/p203/vlm-page"
KROP = {
    (119, 12): {"hisna": "11", "ime": "Katharina LUNIČ[?] [★★★ KROP-slika-'Katharina Lunic, ledinske-hči[?]'-h11-jasno! h11 = KUNIĆ-hiša (1875-z71!)!]", "starost": "16 dni", "bolezen": "Frisen[?]"},
    (120, 3): {"hisna": "24", "ime": "Maria BRIME [KROP-'Maria Brime, ofd.'-h24-jasno!]", "pokop": "23. [KROP — VLM-'20.'-misread!]"},
    (120, 10): {"hisna": "28", "ime": "Maria BRIME, nšl. [KROP-'Maria Brime, praD. ofd.'-h28-jasno! ★BRIME-×2-v-5-tednih-h24/h28!]"},
    (124, 1): {"hisna": "39", "ime": "Mathias TILAK[?Silak] [★★★ KROP-slika-'Griblje 39. Mathias Tilak, ½-Gabrielsova[?]'-1J-Halborn! s123==s124-DVOSCAN-KROP-×2-soglasje! VLM-'h34/h39'-DUEL-RAZREŠEN-h39!]", "stan": "½ Gabrielsova[?Gabrielsova/kriptično]"},
    (124, 6): {"hisna": "69", "ime": "Joannes BRUNE [★★★ KROP-'Griblje 69. Joannes Brune'-jasno! h69-×2-1874 (→ r1-s121-Brinc!)]", "starost": "69 [★★★ KROP-'6g-jasno-69'-vs-VLM-'56¾ J'-NESOGLASJE-[~]!]", "smrt": "28. [KROP — VLM-'23.'-misread!]", "bolezen": "¾-Ziblav[?kriptično-'bolehal-¾-leta']"},
    (125, 10): {"hisna": "33", "ime": "Katharina KRIŽAN [★★★ KROP-'33.'-glif-za-glifom-'ne-5-ne-8-ne-9' — NE-h83! KRIŽAN-nit-NOVA-hiša! VLM-'Valbarina[?]'-→-KROP-'Katharina'!]", "duhovnik": "provisorium Kogej [★★★ KOGEJ-'provisorium'-podpis-1874! NIT-4.-leto!]"},
    (126, 9): {"hisna": "57", "ime": "Michael LOGAR, kolonist[?] [★★★ KROP-'57.'-glavni-stolpec — NE-h8! + modra-tinta-'12'-annotacija-kasneje (anomalija!) h57 = P200-h57-NIT-1874→1877!]", "bolezen": "Gichtern", "duhovnik": "c. fr. Franc Dougan [DOVGAN-nit!]"},
    (127, 1): {"hisna": "19", "ime": "Catharina KRIČ[?] [★★★ KROP-slika-'Griblje 19.'-h19-jasno! P202-tail-hisna=None→POPRAVEK!]", "stan": "nšl.[?]"},
    (127, 4): {"hisna": "29", "ime": "Mathias MILER[?Milek], 'Abb.'[?opat/vdovec-grafia] [★★★ KROP-slika-'Griblje 29.'-h29-jasno! P202-tail-hisna=None→POPRAVEK!]", "stan": "Abb.[?]"},
}

MES_GLAVE = {(122, 1): "Mai", (125, 1): "September", (126, 1): "September"}  # '1874.'-glave-v-celicah: s122-z1-Mai (45.-POTRDITEV!) + s125-z1 (46.-POTRDITEV!)

# s123 = duplikat s124 — SKIP celoten!
entries, tail_1873 = [], []
zap = 0
for sken in range(119, 128):
    if sken == 123:
        continue  # DVOSCAN == s124!
    d = json.load(open(f"{VP}/s{sken}.json"))
    for r in d.get("vrstice", []):
        v = int(r.get("vrsta") or 0)
        rec = {"sken": sken, "pag": (sken - 5 if sken <= 123 else sken - 6), "vrsta_sken": v,
               "mesec_raw": (r.get("mesec") or "").strip(), "smrt": (r.get("smrt") or "").strip() or None,
               "pokop": (r.get("pokop") or "").strip() or None, "vas": (r.get("vas") or "").strip() or None,
               "hisna": (str(r.get("hisna")) if r.get("hisna") is not None else "").strip() or None,
               "ime": (r.get("ime") or "").strip() or None, "stan": (r.get("stan") or "").strip() or None,
               "starost": (r.get("starost") or "").strip() or None, "bolezen": (r.get("bolezen") or "").strip() or None,
               "previden": r.get("previden"), "duhovnik": (r.get("duhovnik") or "").strip() or None,
               "opomba": (r.get("opomba") or "").strip() or None, "krop": None}
        if sken == 119 and v < 11:
            rec["leto"] = 1873
            tail_1873.append(rec)
            continue  # December-1873-tail (P204-lead!)
        if sken == 127 and v > 10:
            continue  # s127-z11 = 1875-z1 (ŽE-V-P202!)
        rec["leto"] = 1874
        mes = (r.get("mesec") or "").split()[0].strip(".,") or "[?]"
        if mes in ("Janner", "Jänner 1874") or "Jänner" in mes:
            mes = "Jänner"
        # FORCE-mesece (KROP-potrjene strukture!):
        if sken == 125:
            mes = "September"  # VLM-'Jänner'-×13-FALSIFICIRAN → KROP-'9.'-numerično = September!
        elif sken == 120:
            mes = "Jänner" if v == 1 else "Feber" if 2 <= v <= 6 else "März" if 7 <= v <= 10 else "April"  # KROP-s120-levo!
        mg = MES_GLAVE.get((sken, v))
        if mg:
            rec["krop"] = f"s{sken}-z{v}-GLAVA-V-CELICI: '{mg} 1874.' (invariante!)"
            mes = mg
        k = KROP.get((sken, v))
        if k:
            rec.update(k)
            rec["krop"] = (rec["krop"] + " + " if rec["krop"] else "") + f"s{sken}-z{v}-KROP"
        rec["mesec"] = mes
        zap += 1
        rec["zap"] = str(zap)
        entries.append(rec)

for e in entries:
    e["zap_raw"] = "[?]-ordinali-ZMEDANI (s119-'3'-marginal + s127-'14.'/'29.'-VLM-claimi) → ŠTEVJE-IZ-VRSTIC-5.×"

out = {"leto": 1874, "vseskupaj": len(entries),
       "griblje": sum(1 for e in entries if e["vas"] and "gribl" in str(e["vas"]).lower()),
       "tail_1873_n": len(tail_1873), "entries": entries, "tail_1873": tail_1873}
json.dump(out, open("/tmp/p203/entries_1874.json", "w"), ensure_ascii=False, indent=1)
g = [(e["zap"], e["sken"], e["vrsta_sken"], e["hisna"], (e["ime"] or "")[:42], e["starost"]) for e in entries if e["vas"] and "gribl" in str(e["vas"]).lower()]
print(f"vpisov-1874: {len(entries)} | Griblje: {len(g)} | tail-1873: {len(tail_1873)}")
for x in g:
    print("  z%s s%s r%s h%s | %s | %s" % x)
mesi = {}
for e in entries:
    mesi[e["mesec"]] = mesi.get(e["mesec"], 0) + 1
print("meseci:", mesi)
