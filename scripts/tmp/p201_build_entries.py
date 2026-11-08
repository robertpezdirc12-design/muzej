#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P201 — build entries 1876 (ŠTEVJE-IZ-VRSTIC) iz VLM-branj /tmp/p201/vlm-page.
s134-z5..z10 (Jänner) + s135–s142 → z1–z89 (89 vpisov; ordinali-NEVIDNI-×9!).
KROP-korekcije: s142-ALL → NOVEMBER (VLM-'Dezember'-FALSIFICIRAN — KROP-'N-o-v-e-m-b-e-r'!);
s136-z4 → März-29/30 (KROP + monotoničnost!); s137-z6 → ¼J + 'sin Joanes-DRAGOŠ';
s141-z9/z10 starosti; s142-z4 → Arnuetz[?]; s139-z9 → Marzin-dojenček.
Izhod: /tmp/p201/entries_1876.json"""
import json

VP = "/tmp/p201/vlm-page"
KROP = {
    # (sken, vrsta-1-based): dict-popravek
    (136, 4): {"mesec": "März", "ime": "Maria Perdire [★★★ KROP: 'P-e-r-d-i-r-e' ≈ PEZDIR! PEZDINC-GRAFIA-#8 — VLM-'Perdiue/Perdiu'-t/d-zmeda! → h53-NIT-1876/77: babica-62J (März-1876) + dojenček-1J (Okt-1877)!]", "smrt": "29.", "pokop": "30.", "stan": "Auszüglerin [KROP-'Einzüglerin'-grafia]"},
    (137, 6): {"ime": "Anton, sin Joanes-DRAGOŠ [★★★ KROP-'So des Joanes Dragoš' — DRAGOŠ-h12-NIT-1876/77 (→ 1877-z56-Katharina-h12!)!]", "starost": "¼ J. [KROP — VLM-'2½ J.'-ZAVRJEN!]", "stan": "ehelicher Sohn des Joannes Dragoš [KROP; VLM-'unehelich?'-zavržen]"},
    (139, 9): {"ime": "[?] dojenček, hči Magd. Agnes Marzin [~Marin] [KROP-s139_spodaj: 'Griblje 55 — (Noth-)gemein(?) hči Magd. Agnes Marzin, dojenček'!]", "starost": "[?] (dojenček)"},
    (141, 9): {"ime": "Maria ŠIMEC [★★★ h18-ŠIMEC-NIT-1876! KROP-'Maria Simec, Mädchen' — VLM-'Zupančič?/Zimec?'-nesoglasje → ŠIMEC-nit-3.-leto (1876-Šimec + 1877-Siniec + 1878-Innec? + 1881-TIMEC)!]", "starost": "72 3/4 J. [KROP-'72 3/4'; KROP-2.-branje-'74'-NEUSKLAJENO — [~]; VLM-'72 2/5'-zavrženo]", "stan": "Mädchen [KROP]"},
    (141, 10): {"ime": "Anna Jakofčič [KROP — 'Jakopič'-VLM-varianta]", "starost": "27 1/2 J. [KROP-2.-branje-'½ leta'-NEUSKLAJENO — [~]; 3.-branje-soglasje-27½]", "bolezen": "Hirnhautentzündung [KROP — VLM-'Brustbekfinbar?'-ZAVRJEN]"},
    (142, 4): {"ime": "Barbara Arnuetz[?] [KROP-'Arnuetz, legitimirana hči Antona' — VLM-nesoglasje-×3: 'Kavčič[?]/Kauer/Arnuetz/Struselj' — [?]!]", "mesec": "November", "smrt": "24.", "pokop": "25."},
    (135, 3): {"opomba": "[~datum-zmeda: z3-Feb-16 vs z4-Feb-15 — VLM-nestabilnost-datumov]"},
    (135, 4): {"opomba": "[~datum-zmeda: z3-Feb-16 vs z4-Feb-15 — VLM-nestabilnost-datumov]"},
}

MES_POPRAVEK = {"s142": "November"}  # KROP-'N-o-v-e-m-b-e-r'-pod-'1876.'-glavo!

entries = []
zap = 0
tail_1875 = []
for sken in range(134, 143):
    d = json.load(open(f"{VP}/s{sken}.json"))
    for r in d.get("vrstice", []):
        v = int(r.get("vrsta") or 0)
        rec = {
            "sken": sken,
            "pag": sken - 6,
            "vrsta_sken": v,
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
        # s134-z1..z4 = TAIL-1875 (Dezember)!
        if sken == 134 and v <= 4:
            rec["leto"] = 1875
            rec["mesec"] = "December"
            tail_1875.append(rec)
            continue
        rec["leto"] = 1876
        mes = (r.get("mesec") or "").split()[0].strip(".,")
        if str(sken) in MES_POPRAVEK:
            mes = MES_POPRAVEK[f"s{sken}"]
            rec["krop"] = "s142-glava-KROP: 'N-o-v-e-m-b-e-r.'-pod-'1876.'-glavo (VLM-'Dezember'-FALSIFICIRAN!)"
        k = KROP.get((sken, v))
        if k:
            rec.update(k)
            rec["krop"] = (rec["krop"] + " + " if rec["krop"] else "") + f"s{sken}-z{v}-KROP"
        rec["mesec"] = mes
        zap += 1
        rec["zap"] = zap
        entries.append(rec)

# ordinali-NEVIDNI: zap = rekonstruiran-iz-vrstic
for e in entries:
    e["zap_raw"] = "[?]-ordinali-NEVIDNI"
    e["zap"] = str(e["zap"])

out = {"leto": 1876, "vseskupaj": len(entries), "griblje": sum(1 for e in entries if e["vas"] and "gribl" in e["vas"].lower()), "tail_1875_n": len(tail_1875), "entries": entries, "tail_1875": tail_1875}
json.dump(out, open("/tmp/p201/entries_1876.json", "w"), ensure_ascii=False, indent=1)
g = [(e["zap"], e["sken"], e["hisna"], e["ime"], e["starost"]) for e in entries if e["vas"] and "gribl" in e["vas"].lower()]
print(f"vpisov-1876: {len(entries)} | Griblje: {len(g)} | tail-1875: {len(tail_1875)}")
for g_ in g:
    print("  z%s s%s h%s | %s | %s" % g_)
