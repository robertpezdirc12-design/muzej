#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P202 — build entries 1875 (ŠTEVJE-IZ-VRSTIC, recept-4.×!) iz VLM-branj /tmp/p202/vlm-page.
Okno: s127-z11 ('Jänner 1875'-glava-V-CELICI — MEJA-1874/75!) + s128–s133 + s134-z1..z4
(Dez-TAIL) → z1–z71 (71 vpisov; ordinali-NEVIDNI!). Vrstna-aritmetika:
1+11+10+13+12+10+10+4 = 71 ✓; meseci Jan3+Feb3+Mär15+Apr7+Mai6+Jun6+Jul1+Aug6+Sep6+Okt5+Nov8+Dez5 = 71 ✓.
KROP-korekcije: 12-GRIBLJE (s128-×3 + s129-×2 + s130-×2 + s131-×1 + s132-×1 + s133-×2 + s134-×1!)
— VLM-FALSIFIKACIJE-×4: s128-z8-'Georg-h59'-POTRJEN-KROP ('Bezdira[?Peglinc?]'-PEZDIR-DUEL!),
s128-z10-h45-Mathias, s128-z11-h29-Catharina-Kambič ('29'-ne-'59'!), s130-z5-'Matthea-Klemencic'-
FALSIFICIRAN→'Miha-Nemanič-h35!', s131-z5-'h73'→h72 (KURRENT-2/3!), s133-z1-'1875'-glava-v-z1-
celici (44.-POTRDITEV-INVARIANTE!), s133-z4-h26-Georg-Sodja-'¼-Griblanskind'-NEVIDEN-VLM-vas!
DUHOVNIKI-1875: 'provinciat Hogeyu Coop.' (z17!) + 'provinciat Kooci Coop.' (z18!) — KOGEJ-
SUBSTITUENDUS-ŽE-1875 ('provinciat'-rank!) + s127-dno-'Rogejus Coop.'-'121'-pag-št.-V-GLEDU!
Izhod: /tmp/p202/entries_1875.json"""
import json

VP = "/tmp/p202/vlm-page"
KROP = {
    # (sken, vrsta-1-based): dict-popravek — 12-GRIBLJE
    (128, 8): {"hisna": "59", "ime": "Georg Peglinc[?Bezdira?] [★★★ KROP-'Griblje 59. Georg P-e-g/d-linc' — PEZDIR-GRAFIA-DUEL-#1-1875 — cf. PEZDINC-nit-h53-1876/77! VLM-vas-'Griblje'-soglasje; ime-glif-'gmüth[?]'-nejasen!]", "stan": "gmüth[?] [kriptični-stan-glif]"},
    (128, 10): {"hisna": "45", "ime": "Mathias Riünzflißler[?Rinzbissler?] [KROP-'Griblje 45. Mathias' — VLM-z10-soglasje-h45!]", "stan": "Sohn der Anna Braußsche[?], ½ J. vne. Auszüglerin[?]"},
    (128, 11): {"hisna": "29", "ime": "Catharina Kambič[?Kambrič?] [★★★ KROP-'Griblje 29.' — KURRENT-2/5-DUEL-RAZREŠEN: '29'-NE-'59'! (h59-je-samo-z8-Georg!)]", "stan": "Griszäny kindemachine[?kriptični-stan-glif]"},
    (129, 5): {"hisna": "31", "ime": "Maria Kambič, Kurpašnič[?] [KROP-'Griblje 31.'-jasno!]", "starost": "24 7/8 [★ KROP-'24 7/8' — VLM-'24 tj.'-FALSIFICIRAN! enota-[?]-leta/tednov-NEJASNA]", "stan": "¼ Gribl. Taglöhnerin [KROP-'¼ Gribl.'-stan-glif!]", "duhovnik": "provinciat Hogeyu Coop. [★★★ KOGEJ-SUBSTITUENDUS-1875-'provinciat'-rank!]", "bolezen": "Brüzframeng[?mhfak][?kriptično]"},
    (129, 6): {"hisna": "17", "ime": "Anna Kraus, ansl. Tochter des Josus Kraus [KROP-'Griblje 17.'-jasno!]", "starost": "24 [?] (+'¾ J.'-glif-v-imeni-stolpcu — ure/leta-[?]!)", "duhovnik": "provinciat Kooci Coop. [★★★ EKSPLICITNO-'Kooci'-COOP. = KOGOJ/KOGEJ-GRAFIA!]", "bolezen": "Blattronn[?Blatkronn-kriptično]"},
    (130, 5): {"hisna": "35", "ime": "Miha Nemanič [★★★ KROP-FALSIFIKACIJA-VLM-'Matthea-Klemencic-43J'-'14./16. Griblje 35. Miha Nemanič, gründbm'-moško-ime!]", "stan": "gründbm[?Güntblom-kriptično]"},
    (130, 8): {"hisna": "22", "ime": "Maria Mihel[?Milek] [KROP-'Griblje 22. Maria Mihel/Milek, nfml. Tauf.'-m/n-DUEL]", "stan": "nfml. Tauf."},
    (131, 5): {"hisna": "72", "ime": "Joannes, ansl. Sohn des Marcus Brauše [★★★ KROP-'Griblje 72.' — KURRENT-2/3-DUEL-RAZREŠEN: h72-NE-h73! BRAUŠ-nit (→ z9-h59-'Braußsche'-mama? + cf. 1876-Brodarič?)!]", "starost": "5 tednov [VLM-soglasje]"},
    (132, 7): {"hisna": "5", "ime": "Joanes Štuzel[?Sturzel] [KROP-'Griblje 5.'-jasno! STURZEL-grafia-dvom]", "stan": "¼ Gübler [KROP-'¼ Gübler'-stan-glif!]"},
    (133, 1): {"mesec": "Oktober", "smrt": "26.", "pokop": "28.", "hisna": "69", "ime": "Georg Husič [KROP-'Griblje 69. Georg Husič, nfml. Sohn'-jasno! '1875'-GLAVA-V-Z1-DATUMSKI-CELICI = 44.-POTRDITEV-INVARIANTE!]", "stan": "nfml. Sohn."},
    (133, 4): {"mesec": "November", "smrt": "6.", "pokop": "7.", "hisna": "26", "ime": "Georg Sodja[?Sodjak?] [★★★ KROP-'Griblje 26.' — NEVIDEN-V-VLM-'vas'-stolpcu-ZMEDE — KROP-ODKRIL! SODJA-nit-nova!]", "stan": "nfml. ¼ Griblanskind [KROP-'¼ Griblans-kind'-stan-glif!]"},
}

MES_GLAVE = {
    # (sken, vrsta): mesec-glave-v-datumska-celica (invariante!)
    (127, 11): "Jänner",   # 'Jänner 1875' — MEJA-1874/75! 45.-POTRDITEV
    (128, 6): "März",      # März-glava-v-celici (k128_levoA)
    (131, 6): "Juli",      # Juli-glava (k131_z40b)
    (133, 2): "November",  # November-glava (k133_levoA)
    (133, 10): "Dezember", # Dezember-glava (k133_levoB)
}

entries = []
zap = 0
tail_1874 = []   # s127-z1..z10 = Nov/Dez-1874 (pripada prejšnjemu P-izdanju — ZA-LEAD!)
for sken in range(127, 135):
    d = json.load(open(f"{VP}/s{sken}.json"))
    for r in d.get("vrstice", []):
        v = int(r.get("vrsta") or 0)
        rec = {
            "sken": sken, "pag": sken - 6, "vrsta_sken": v,
            "mesec_raw": (r.get("mesec") or "").strip(),
            "smrt": (r.get("smrt") or "").strip() or None,
            "pokop": (r.get("pokop") or "").strip() or None,
            "vas": (r.get("vas") or "").strip() or None,
            "hisna": (str(r.get("hisna")) if r.get("hisna") is not None else "").strip() or None,
            "ime": (r.get("ime") or "").strip() or None,
            "stan": (r.get("stan") or "").strip() or None,
            "starost": (r.get("starost") or "").strip() or None,
            "bolezen": (r.get("bolezen") or "").strip() or None,
            "previden": r.get("previden"),
            "duhovnik": (r.get("duhovnik") or "").strip() or None,
            "opomba": (r.get("opomba") or "").strip() or None,
            "krop": None,
        }
        # s133-z11 = PRAZNA-vrstica-tabele (k133_levoB: Dez-z10-zadnji-VPIS!)
        if sken == 133 and v > 10:
            continue
        # s134-z5..z10 = 1876-Jänner (ŽE-V-P201-produkciji!)
        if sken == 134 and v > 4:
            continue
        # s127-z1..z10 = Nov/Dez-1874 (pred-mejo!)
        if sken == 127 and v < 11:
            rec["leto"] = 1874
            tail_1874.append(rec)
            continue
        rec["leto"] = 1875
        mes = (r.get("mesec") or "").split()[0].strip(".,") or "[?]"
        mg = MES_GLAVE.get((sken, v))
        if mg:
            rec["krop"] = f"s{sken}-z{v}-GLAVA-V-CELICI: '{mg}' (invariante!)"
            mes = mg
        k = KROP.get((sken, v))
        if k:
            rec.update(k)
            rec["krop"] = (rec["krop"] + " + " if rec["krop"] else "") + f"s{sken}-z{v}-KROP"
        rec["mesec"] = mes
        zap += 1
        rec["zap"] = str(zap)
        entries.append(rec)

# ordinali-NEVIDNI: zap = rekonstruiran-iz-vrstic (recept-4.×)
for e in entries:
    e["zap_raw"] = "[?]-ordinali-NEVIDNI"

out = {"leto": 1875, "vseskupaj": len(entries),
       "griblje": sum(1 for e in entries if e["vas"] and "gribl" in str(e["vas"]).lower()),
       "tail_1874_n": len(tail_1874), "entries": entries, "tail_1874": tail_1874}
json.dump(out, open("/tmp/p202/entries_1875.json", "w"), ensure_ascii=False, indent=1)
g = [(e["zap"], e["sken"], e["hisna"], e["ime"], e["starost"]) for e in entries if e["vas"] and "gribl" in str(e["vas"]).lower()]
print(f"vpisov-1875: {len(entries)} | Griblje(VLM-vas): {len(g)} | tail-1874: {len(tail_1874)}")
for g_ in g:
    print("  z%s s%s h%s | %s | %s" % g_)
# KROP-Griblje (tiste-katere-KROP-potrdil-tudi-če-VLM-vas-zmedena):
krop_griblje = [(e["zap"], e["sken"], e["hisna"], e["ime"][:40]) for e in entries if e.get("krop") and "KROP" in str(e.get("krop")) and (e["vas"] and "gribl" in str(e["vas"]).lower() or e["sken"] in (128, 129, 130, 131, 132, 133) and e["hisna"] in ("59", "45", "29", "31", "17", "35", "22", "72", "5", "69", "26", "11"))]
print(f"--- KROP-Griblje-kandidati: {len(krop_griblje)}")
for k_ in krop_griblje:
    print("  z%s s%s h%s | %s" % k_)
