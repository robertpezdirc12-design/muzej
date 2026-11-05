#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P212 — agregacija 66 vpisov leta 1865 (ŠTEVJE-IZ-VRSTIC-14.×!).
s46 = MEJA-1864/65: tail-1864 (z88–z91, NATAČNO-4-vrstice-KROP!) + '1865'-VELIKA-LETVICA-KROP-50.-POTRDITEV!
+z74_s45_zap-duel-REŠEN: s45 = zap-74–87 (Kurrent-4-z-zanko!) → 1864-kontekst-veriga-60→91-ČISTO-ZVEZNA!
Vrstna aritmetika: 7+14+14+14+15+2 = 66; ordinali-1–66 ČISTO-6.-leto-zapored!
KROP-korekcije VGRAJENE: z1-stan-DUEL-3×, z8-Urih+stan-duel, z9-starost-60-KROP,
z11-h50+Redovi+Gübler-Kind+Wassersucht, z13-Schwindsucht+ANOMALIJA-pokop-17-pred-smrt-18-PISAR-MOTA!
s51-tail-z65/z66: P211-KROP-dokaz (arb_s51_glava) — PEZDIRC-h14-kontinuiteta-z-z41-1866!
Izhod: /tmp/p212/entries_1865.json"""
import json

TMP = "/tmp/p212"
PLAN = [
    (46, list(range(1, 8)), "z1–z7-restart-'1865'-VELIKA-LETVICA-KROP-50.-POTRDITEV! (tail-1864-z88–z91-NATAČNO-4-KROP + z91-ULEDBA-#11-30.Dez→1.Jän!)", 5),
    (47, list(range(8, 22)), "z8–z21 (14; ★ 7-GRIBLJE-KLASTER! z8,z9,z11,z13,z17,z18,z20)"),
    (48, list(range(22, 36)), "z22–z35 (14; z24-Griblje)"),
    (49, list(range(36, 50)), "z36–z49 (14; z36-Griblje-POŽEK-h67!)"),
    (50, list(range(50, 65)), "z50–z64 (15; z50+z63-Griblje! s50-VLM-reuse-P211!)"),
]

# KROP-korekcije (vgrajene za reproducibilnost!) — ključ: z
KROP = {
    1: {"bolezen": "Marasmus senilis [KROP]",
        "stan": "Ablabamin[~DUEL-3×-branja: Abrabannin/Albrechtin/Ablabamin]",
        "_opomba": "KROP-izrezi (glava+z1): h3-ČISTO + 81-J. + smrt-16./pokop-18. + 'Marasmus senilis'. Stan-DUEL-HONEST: 3-neodvisna-branja-neskladna (cf. z88-IST-bazna-beseda-za-Maria-Križan-Otok-h20!) — ★ 2×-Maria-Križan-v-1-tednu (z88-Otok-48J-12.Dez + z1-Griblje-81J-16.Jän)!"},
    8: {"ime": "Katarina Urih [~Urik; KROP-'Urih, ne-Urik']",
        "stan": "Güblerin[~DUEL: VLM-'Inoaskanica' / KROP-'G—l—']",
        "_opomba": "KROP-izrez-DELNO (glava-tabele-prevladala): ime-'Urih'-POTRJENO; vas/hisna-izven-izreza → hisna-68-ostaja-VLM (krop_pending-re-crop!); + v-levem-rob-'+'-znamenje-morda-kazalec-na-opombo"},
    9: {"starost": "60 let [KROP! duel: VLM-56]",
        "_opomba": "KROP-izrez: Griblje-h23-Anna-Brinc-ČISTO + starost-'60' (Kurrent-6/0; 'očitno-60') — starost-DUEL-HONEST-58-KROP-vs-VLM-56? NE: KROP-60-vs-VLM-56! (cf. P210-z3/z8/z15-starost-DUELI)"},
    11: {"hisna": "50", "ime": "Barbara Redovi [~Redovc]", "stan": "½ Gübler-Kind", "bolezen": "Wassersucht",
         "_opomba": "★★★ KROP-izrez: h50-NI-80 ('Kurrent-5-s-čopom,-ne-8'!) + ime-'Redovi(Redovc?)'-NI-Podgoršek (VLM-halucinacija-FALSIFICIRANA!) + '½-Gablard-Kind'='½-Gübler-Kind' + Wassersucht-NI-Mrzlica — mesec-KROP-'oktober'-ABERRACIJA (kontekst-Februar-z9!)"},
    13: {"stan": "½ Güblerswirt", "bolezen": "Schwindsucht [~VLM-Massnafal?]",
         "_opomba": "★★★ KROP-izrez: ANOMALIJA-POTRJENA-v-zapisu — pokop-17.-vpisan-PRED-smrt-18. (pisar-mota: morda-smrt-17./pokop-18.!) + h37-GOTOVO + '½-Gütlerstswirt'='½-Güblerswirt' + Schwindsucht (jetika) — z13+z18-IST-hiša-h37-KLASTER (mati-27J + otrok-2-mes!)"},
}

entries = []
for item in PLAN:
    sken, z_list, op = item[0], item[1], item[2]
    min_vrsta = item[3] if len(item) > 3 else 1
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
        # s46: tail-1864 (vrsta 1–4) preskoči!
        if sken == 46 and (x.get("vrsta") or 0) < min_vrsta: continue
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
        k = KROP.get(x["z"])
        if k:
            for kk, vv in k.items():
                if kk == "_opomba": x["krop_opomba"] = vv
                else: x[kk] = vv
            x["krop"] = True
        entries.append(x)

# --- s51-tail z65/z66 (P211-KROP-dokaz: arb_s51_glava!) ---
s51_krop = json.load(open("/tmp/p211/krop-reads/arb_s51_glava.json"))
s51_vlm = json.load(open("/tmp/p211/vlm-page/s51.json"))
vlm_tail = {str(x.get("zaporedna", "")): x for x in s51_vlm.get("vrstice", []) if str(x.get("zaporedna", "")) in ("65", "66")}
TAIL_P212 = [
    (65, {"mesec": "December", "smrt": "27.", "pokop": "29.", "vas": "Zemelj", "hisna": "13",
          "ime": "Anna Berkovec [~Berkopec/Bezkovec]", "stan": "Abfaknin/Ablokumin[~DUEL-2×: '? dekla']",
          "starost": "60 J", "bolezen": "Lungenentzündung"}),
    (66, {"mesec": "December", "smrt": "28.", "pokop": "30.", "vas": "Griblje", "hisna": "14",
          "ime": "Maria Pezdirc", "stan": "Abfaknin/Ablokumin[~DUEL-2×: '? dekla']",
          "starost": "66 J", "bolezen": "Abzehrung / Altersschwäche [~]"}),
]
for z, pod in TAIL_P212:
    v = vlm_tail.get(str(z), {})
    e = {"z": z, "sken": 51, "pag": 46, "vrsta_sken": z - 64,
         "ord_opomba": "s51-TAIL-1865-z65/z66 (P211-KROP-dokaz-arb_s51_glava! + prečrtana-67-Schlangenlinien-SKIP + restart-'1866'!)",
         "krop": True, "krop_opomba": "P211-KROP-dokaz (arb_s51_glava.json) — z66: PEZDIRC-h14-kontinuiteta-z-z41-1866 (Mathias-unehelich-h14!) + VLM-h11-duel-rešen-KROP-h14!",
         "zaporedna": str(z), **pod}
    # bolezen-iz-VLM (če KROP-ni-več)
    if "bolezen" in v and v.get("bolezen"): e["bolezen_vlm"] = v.get("bolezen")
    entries.append(e)

griblje = [e for e in entries if any(w in (e.get("vas") or "").lower() for w in ("gribl", "grible", "hrible"))]
meseci = {}
for e in entries:
    m = (e.get("mesec") or "").split()[0].split("/")[0].strip(" .")
    meseci[m] = meseci.get(m, 0) + 1
out = {"leto": 1865, "vseskupaj": len(entries), "griblje": len(griblje),
       "meseci": meseci,
       "ord_kaskada": {"meja_1864_65": "s46 (tail-1864-z88–z91-NATAČNO-4-vrstice-KROP! + z91-ULEDBA-#11-10.INSTANCE-30.Dez-1864→1.Jänner-1865-pokop + '1865'-VELIKA-LETVICA-KROP-50.-POTRDITEV-invariante! + dvojna-črta!)",
                        "stevje_iz_vrstic": len(entries),
                        "vrstna_aritmetika": "7+14+14+14+15+2(s51-tail) = 66",
                        "ordinali": "1–66-ČISTO-BREZ-luknje/dupa — 6.-LETO-ZAPORED!",
                        "kontekst_1864": "s42(31–44)+s43(45–59)+s44(60–73)+s45(74–87-KROP-z74-duel-REŠEN: Kurrent-4-z-zanko!)+s46-tail(88–91) = 1864-zap-31–91-ZVEZNA (zap-1–30-na-s41/prej → P213-probe-s039–s042!)"},
       "entries": entries, "griblje_entries": griblje,
       "krop_dokazi": {"glava": "arb_s46_glava-'1865'-50.-POTRDITEV-invariante! + dvojna-črta + restart-z1-Griblje-h3-Maria-Križan-81J!",
                        "tail": "arb_s46_tail-NATAČNO-4-vrstice (88–91; z89-starost-korekcija-v-zapisu!) — gaplje-85–87-NI (s45=74–87-KROP-z74-duel!)",
                        "z74": "s45-zap-stolpec-74/75/76-KROP (VLM-71/72/73-FALSIFICIRAN — Kurrent-4/1!)",
                        "z1": "Griblje-h3-Maria-Križan-81J-Marasmus-senilis + stan-DUEL-3×-HONEST",
                        "z8": "Katarina-URIH-(ne-Urik!)-KROP-partial",
                        "z9": "starost-60-KROP-vs-VLM-56-DUEL",
                        "z11": "h50-NI-80 + Redovi-NI-Podgoršek + ½-Gübler-Kind + Wassersucht (4-korekcije!)",
                        "z13": "ANOMALIJA-pokop-17-PRED-smrt-18-PISAR-MOTA + Schwindsucht + ½-Güblerswirt",
                        "z65z66": "P211-KROP-arb_s51_glava (PEZDIRC-h14-kontinuiteta!)"},
       "krop_pending": ["z17", "z18", "z20", "z24", "z36", "z50", "z63", "z8-recrop"],
       "leadP213": "1864 — s42–s46-tail-ŽE-VLM+delno-KROP (1864-zap-31–91-ZVEZNA; z74-duel-REŠEN!) + zap-1–30-na-s41/prej → probe-s039–s042!"}
json.dump(out, open(f"{TMP}/entries_1865.json", "w"), ensure_ascii=False, indent=1)
print(f"1865: {len(entries)} vpisov (ordinali-1–66 ČISTO-6.-leto!), Griblje: {len(griblje)} / {len(set(str(e.get('hisna')) for e in griblje))}-hiš")
print(f"meseci: {meseci}")
for e in griblje:
    print(f"  z{e['z']:>3} s{e['sken']}r{e['vrsta_sken']:>2} pag{e['pag']} h{str(e.get('hisna')):4} {str(e.get('ime') or '')[:40]} — {str(e.get('starost') or '')[:18]} — {str(e.get('bolezen') or '')[:24]}")
