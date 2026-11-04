#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P199 — agregacija 10 VLM-branj → 85 vpisov za leto 1878 (mrliška 04106, 8/29).
Preslikava: pag = sken − 6 (P197/P198-veriga; md5-križna-validacija-ta-seja!).
Okvir: s149 (MEJA-1877/78: glava-'1878'-SPLIT-v-z1 + restart-1 + z1–z9)
  → s150 (z10–16) · s151 (17–23) · s152 (24–33) · s153 (34–43) · s154 (44–53)
  · s155 (54–62) · s156 (63–72) · s157 (73–82 — P198-REUSE: KROP-×2-seji!)
  · s158 (tail-z83–z85 — P198-REUSE: KROP + RE-READ-SOGLASJE!)
= 85 vpisov EXAKT (P197-'restart-85→1'-napoved-POTRJENA!)."""
import json
from pathlib import Path

VLM = Path("/tmp/p199/vlm-page")
P198_RAW = json.load(open("/tmp/p199/entries_raw.json"))
OUT = Path("/tmp/p199/entries_1878.json")

# ——— KROP-izreki (agent-oči; ključi = (sken, VLM-vrsta-1-based)) ———
KROP = {
    # ——— s149 (MEJA-1877/78 + z1–z9) ———
    (149, 1): {"zap_krop": "1 (restart-1 — MEJA!)",
               "glava": "★★★ '18 78.'-SPLIT-VARIANTA-v-z1-datuma-celici (KROP-max-zoom: γ-7-s-prečko — VLM-'1848'-4/7-ZAVRJEN!) = 38.-POTRDITEV-invariante!",
               "duhovnik": "substituendus Kogoj/Kogej Corp. (KROP-'Hoggaj'-grafia!)",
               "krop": "s149-meja-glava"},
    (149, 4): {"ime": "Mathias Pezdirc [KROP-jasno!]", "stan": "sohn des Joh. u. Valburdua? Mathias u. Theodita? Güttler [~KROP-partial]",
               "starost": "6 let [~KROP-'6 Jfr.'-grafia]", "bolezen": "Brustsucht? [~KROP-'Brunn?fuffun'-neberljivo; VLM-'Brustst[A?]'-variante]",
               "duhovnik": "substituendus Kogoj/Kogej Corp.", "krop": "s149-full + z4-datum (19/20 ✓)"},
    (149, 9): {"ime": "Marcus Kure [~Hure-KROP-grafia]", "duhovnik": "substituendus Kogoj/Kogej Corp.", "krop": "s149-full ('Marcus Hure 47f Asthma'-jasno!)"},
    # ——— s150 (z10–16) ———
    (150, 1): {"hisna": "1/a [~KROP-'1/a'-frakcija]", "krop": "s150-levi"},
    (150, 4): {"vas": "Geriče (KROP-'Gersič'-grafia)", "krop": "s150-levi"},
    (150, 5): {"ime": "Johann Klobučar, ¼ Gütler (KROP-ime-crop-JASNO!) — ★KLOBUČAR-nit-1878 (cf. P197-h47 + P193-veriga!)",
               "hisna": "48 (KROP ✓)", "starost": "35½ let (KROP-'35½ J.' ✓)", "bolezen": "Abzehrung (KROP ✓)",
               "duhovnik": "substituendus Kogej Corp. (KROP-podpis-'Hogeju'!)", "krop": "s150-z14-ime + desni + podpis"},
    (150, 6): {"hisna": "1/a [~]", "krop": "s150-levi"},
    # ——— s151 (z17–23) ———
    (151, 1): {"hisna": "2 [~KROP-'2'+nadpis]", "krop": "s151-levi"},
    (151, 4): {"hisna": "23 (KROP — VLM-'20'-ZAVRJEN!)", "krop": "s151-levi"},
    (151, 5): {"hisna": "48 [~KROP — VLM-'18'-ZAVRJEN; blind-oseba!]", "krop": "s151-levi"},
    # ——— s152 (z24–33; glava-'1878'!) ———
    (152, 1): {"glava": "★ '1878.'-glava-top (KROP — levi-strip!)", "hisna": "18 (KROP ✓)", "krop": "s152-levi"},
    (152, 5): {"vas": "Begunja vas pri Gribljah [~KROP: 'pri Griblje'-JASNO; 1.-beseda-'Sračuk/Gradec?'-NEBERLJIVA [?] — hamlet-Griblja!]",
               "hisna": "16 (KROP ✓)", "duhovnik": "Fortin? [~VLM-'Fortin aus Kogelnik Corp.' — cf. Kogeju-grafija-KROP-z31/32!]",
               "krop": "s152-levi"},
    (152, 8): {"ime": "Maria Hrizan [~Križan! — VLM-'Horvat'-ZAVRJEN; KROP-ime-crop!] — ★HRIZAN/KRIŽAN-grafija-nit!",
               "stan": "nepol. ½ J. [~'Točken?'-f: Johann u. Cath. — 2.-vrstica-partial]",
               "starost": "8 let (KROP-'8 J.' ✓)", "bolezen": "Frisen (KROP-'Fraisan'-grafia ✓)",
               "duhovnik": "substituendus Kogeju coop (KROP-podpis! — VLM-'Fortin-aus-Kogelnik'-ZAVRJEN!)",
               "krop": "s152-z31z32-ime + desni + podpis"},
    (152, 9): {"ime": "Maria Simec, nepol. [¼/½?] J. — Točkan[?] (KROP; ★ŠIMEC-nit!)",
               "starost": "1½ let (KROP-stolpec-'1½ J.'-AVTORITATIVNO)", "bolezen": "Brustentzündung (KROP ✓)",
               "duhovnik": "substituendus Kogeju coop (KROP!)", "krop": "s152-z31z32-ime + desni + podpis"},
    # ——— s153 (z34–43; glava-'1878'+Aprilis; RE-ALIGNED-6-vrstic!) ———
    (153, 1): {"glava": "★ '1878.'-glava + 'Aprìlis' (KROP-levi-top — VLM-'1875'-5/7-Zmeda-ZAVRJEN!)",
               "ime": "Nicolaus Jakofčič, nepol. ½ J. Sohn f: Johann u. Maria (KROP-ime-crop! — VLM-'Natalia'-ZAVRJEN!) — ★JAKOFČIČ-nit!",
               "starost": "2½ let [~KROP-desni-'2½J.' vs ime-nota-'½J.' — stolpec-avtoritativno]",
               "bolezen": "Friesen (KROP ✓)", "duhovnik": "Franz Dovgan (KROP-podpis!)",
               "krop": "s153-z34-ime + z34-desni + podpis34-36"},
    (153, 5): {"ime": "M[ar]___ Ana P. [?KURRENT-raw-'NrtffyabhanfAna P.'], Wwe./v. Math. Brinec[?]; '¼ J./G.'-nota [?] — ★BRINC/PRINC-nit!",
               "starost": "54 let (KROP-'54 J.' ✓✓ — VLM-soglasje!)", "bolezen": "Asthma (KROP ✓✓)",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s153-levi38-40 + desni38-43-ALL + podpis"},
    (153, 6): {"ime": "Anna P[ar/g]___rb [?KURRENT; VLM-'Maria[?]'] — 2.-beseda-neberljiva",
               "stan": "'¼ G.'-nota[?]", "starost": "★ NI-VPISAN — tilda-'~' (KROP-desni-ALL-crop!) — 2.-prazna-starost-04106 (cf. P198-z47!)",
               "bolezen": "Abzehrung (KROP — VLM-'Tizanica[?]'-ZAVRJEN!)",
               "duhovnik": "substituendus Kogeju coop (KROP!)", "krop": "s153-desni38-43-ALL + z39-ime + podpis"},
    (153, 8): {"ime": "Johann Jilak [~Ilak/Jelak], Sohn f: Jacob u. Mathia (KROP!)",
               "hisna": "16 (KROP ✓)", "starost": "2 leti (KROP-'2 J.' ✓)", "bolezen": "Marbmil (KROP ✓)",
               "duhovnik": "substituendus Kogeju coop (KROP!)", "krop": "s153-z41b-desni + levi38-40 + podpis"},
    (153, 9): {"ime": "Johann Pozdrin [~PEZDIRC-grafija? — cf. h40-nit!]", "hisna": "40 (KROP ✓)",
               "starost": "3 leta (KROP-'3 J.' ✓)", "bolezen": "Brustentzündung (KROP ✓)",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s153-z41z42z43-desni + podpis"},
    (153, 10): {"ime": "Johann Hrovat (KROP ✓)", "hisna": "47 (KROP ✓ — ★KLOBUČAR-h47-nit!)",
                "starost": "56 let (KROP-'56 J.' ✓)", "bolezen": "Lungenentzündung (KROP ✓)",
                "duhovnik": "Franz Dovgan (KROP!)", "krop": "s153-z41z42z43-desni + podpis"},
    # ——— s154 (z44–53; glava-'1878'!) ———
    (154, 1): {"glava": "★ '1878.'-glava-top (KROP!)",
               "ime": "Maria Simec, nepol. Gütlers-tochter f: Georg u. Anna (KROP-ime-crop! — ★ŠIMEC-nit-×2-1878!)",
               "hisna": "38 (KROP ✓)", "starost": "87 let (KROP-'87 J.' ✓ — desni-ALL-crop!)",
               "bolezen": "Lungenentzündung [~ + 2.-vrstica-'-irny?'[?]-nerazrešena; VLM-'Altersmarbmil'-ZAVRJEN!]",
               "duhovnik": "Franz Dovgan (KROP-podpis!)", "krop": "s154-z44-ime + desni44-47 + podpis44-46"},
    (154, 3): {"ime": "Anna Zelko (KROP-ime-crop! — ★ZELKO/ZELIHA-nit-h1!)",
               "stan": "¼ Gütlerswirth [~KROP-'güblnwirtb']", "starost": "34 let (KROP-'34 J.' ✓✓ — desni-ALL!)",
               "bolezen": "In Entbindung (KROP-'In ___ Entbindung'-2-vrstici; VLM-'In kindbett gestor'-SEMANTIČNO-SOGLASJE!)",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s154-z46b-ime + desni44-47 + podpis44-46"},
    (154, 6): {"hisna": "22 [~KROP — VLM-'82'-ZAVRJEN]", "krop": "s154-levi"},
    (154, 8): {"vas": "Gradec [~KROP — VLM-'Dobravice'-ZAVRJEN!]", "krop": "s154-levi"},
    (154, 9): {"hisna": "28 [~KROP — VLM-'18'-ZAVRJEN]", "krop": "s154-levi"},
    # ——— s155 (z54–62; glava-'1878.'+Juni!) ———
    (155, 1): {"glava": "★ '1878.'-glava + 'Juni' v-z1-datuma-celici (KROP-jasno!)", "krop": "s155-levi"},
    (155, 2): {"ime": "Barbara Vezdirz [~PEZDIR-grafija! — VLM-'Pegelj[?]'-ZAVRJEN; cf. ord62-Markus-Pezdir(e)!]",
               "stan": "nepol. Gutfrau[? — KROP-'npfol. ½ J. Gutfrau']", "starost": "10 mesecev (KROP ✓)",
               "bolezen": "Krastelj (KROP-'Chrzfa/Mrzfa'-grafia[~])", "duhovnik": "Franz Jančar coop [~partial-KROP]",
               "krop": "s155-z55z56-ime + z55z56-desni + podpis55-62"},
    (155, 3): {"ime": "Johann Debevc [~Debevec/Debliv — KROP]", "stan": "nepol. Sohn [+½G?-nota]",
               "starost": "37 let [~KROP-'3[7] J.' — 7-v-cut; VLM-'37'-soglasje]", "bolezen": "Abzehrung (KROP ✓)",
               "duhovnik": "Franz Jančar coop (KROP-podpis-JASNO!) — ★★★ JANČAR-na-Griblju-1878-#1!",
               "krop": "s155-z55z56-ime + z55z56-desni + podpis55-62"},
    (155, 7): {"ime": "Katharina Vezdirz [~PEZDIR-grafija! — VLM-'Pegelj[?]'-ZAVRJEN]", "hisna": "20 (KROP ✓ — ★PEZDIRC-era-h20!)",
               "starost": "10 mesecev (KROP-'10 Monate' ✓✓ — re-aligned!)", "bolezen": "Masern (KROP ✓✓ — ★MASERN-nit!)",
               "duhovnik": "Franz Jančar coop (KROP-JASNO!) — ★★★ JANČAR-na-Griblju-1878-#2!",
               "krop": "s155-desni60-62 + podpis55-62"},
    (155, 8): {"hisna": "36 [~KROP — VLM-'56'-ZAVRJEN]", "starost": "1 dan (KROP-'Tag' ✓)",
               "bolezen": "Masern (KROP — identična-grafia-kot-ord60! — VLM-'Fraisen[?]'-ZAVRJEN!) — ★★★ MASERN-×2-ADJACENT (ord60+61)!",
               "krop": "s155-desni60-62"},
    (155, 9): {"ime": "Markus Pezdir(e) [?PEZDIR-grafija! — VLM-'Pegelj[?]'-ZAVRJEN]", "hisna": "30 (KROP ✓)",
               "starost": "35 let [~KROP-3/5-zmeda-'55?'; VLM-'35'-soglasje]", "bolezen": "Cholik (KROP ✓)",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s155-desni60-62 + z60z62-ime + podpis62"},
    # ——— s156 (z63–72) ———
    (156, 2): {"vas": "Krivoglavce (KROP-'Krivoglauve' — VLM-'Primostek'-ZAVRJEN!)", "hisna": "38 [~]", "krop": "s156-levi"},
    (156, 5): {"vas": "Ukolk [?★★★ NEZNANA-VAS-×5-1878 (ord36/67/71/75/78!) — VLM-'Hrast'-ZAVRJEN-×3; cf. P195-'Wolk[~Volk?]'-1882 = verjetno-ista-vas!]",
               "krop": "vas-u-z67d max-zoom"},
    (156, 8): {"ime": "Anna Hrizan [~Križan! — VLM-'Muc'-ZAVRJEN; KROP-ime-crop!]", "stan": "nepol. ¼ J.[?]",
               "hisna": "15 (KROP ✓)", "starost": "5 let (KROP-'5 J.' ✓)", "bolezen": "Fraisen (KROP ✓)",
               "duhovnik": "Franz Jančar coop (KROP-JASNO!) — ★JANČAR-Griblje-#3!",
               "krop": "s156-z70b-desni + z70-ime + podpis70"},
    (156, 9): {"vas": "Ukolk [?NEZNANA-×4!]", "hisna": "34 [~]", "krop": "s156-levi + vas-u-z71b"},
    (156, 10): {"zap_krop": "72 (KROP-γ-7-s-prečko! — VLM-'62[~ker-je-verjetno-72]'-ZAPORedna-misread — 7→6-vzorec-3.×!)",
                "hisna": "24 [~]", "krop": "s156-levi"},
    # ——— s157 (z73–82 — P198-REUSE: ordinali-KROP-×2-seji 73–82!) ———
    (157, 1): {"glava": "★ '1878.'-glava + 'Nov.' (KROP — P198-seja + ta-seja = 2-viri!)",
               "hisna": "37 (KROP ✓)", "starost": "41 let (KROP-'41 J.' ✓)", "bolezen": "Asthma (KROP ✓✓)",
               "duhovnik": "Franz Jančar coop (KROP-podpis! — ★JANČAR-Griblje-#4!)",
               "krop": "s157-levi + desni73-80 + podpis73-82"},
    (157, 3): {"vas": "Ukolk [?NEZNANA-×3!]", "hisna": "34 [~KROP; VLM-'31' — 1/4-zmeda]", "krop": "s157-levi"},
    (157, 5): {"ime": "Mathias Pecolar [~PEZDIR/Peglic-grafija[?] — VLM-'Pecolar[?]']",
               "hisna": "44 (KROP ✓ — ★PEGLIC-h44-nit — 1879-z27/z28-katastrofa!)",
               "starost": "44 let (KROP-'44 Jahre' ✓✓)", "bolezen": "Zagfuß [?KROP-'Zagfus/Zapfus'-neberljivo; VLM-'Hustend[?]'-'ZAVRJEN]",
               "duhovnik": "Franz Jančar coop (KROP! — ★JANČAR-Griblje-#5!)",
               "krop": "s157-levi + desni73-80 + podpis73-82"},
    (157, 6): {"vas": "Ukolk [?NEZNANA-×5!]", "hisna": "25 [~]", "krop": "s157-levi"},
    (157, 8): {"ime": "Maria Logar, nepol. Gütlersfrau (KROP-ime-crop-JASNO!)",
               "hisna": "57 (KROP-γ-7 — VLM-'51[?]'-'ZAVRJEN!)", "starost": "17 let (KROP-'17 J.'-γ-7-jasno! — VLM-'17?/37?'-REŠENO!)",
               "bolezen": "Gehirnentzündung [~KROP-'G___ntzündung'-grafia — ★GEHIRNENTZÜNDUNG-nit-1878/79-×3+2!]",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s157-z80c-ime + z80c-desni + podpis73-82"},
}

MONTHS = {"Jänner": 1, "Feber": 2, "Februar": 2, "März": 3, "April": 4, "Aprilis": 4, "Mai": 5,
          "Juni": 6, "Junii": 6, "July": 7, "Juli": 7, "August": 8, "September": 9,
          "October": 10, "November": 11, "Dezember": 12, "December": 12, "Nov.": 11, "Nov": 11}


def month_no(mes):
    if not mes:
        return None
    m = str(mes).strip()
    for k, v in MONTHS.items():
        if m.lower().startswith(k[:5].lower()):
            return v
    return None


def rows_of(sken):
    d = json.load(open(VLM / f"s{sken}.json"))
    return d.get("vrstice", []), d


def build(sken, zap_start, zap_list=None, mesec_default=None, vr_slice=None, leto=1878):
    vr, _ = rows_of(sken)
    off = 0
    if vr_slice:
        vr = vr[vr_slice[0]:vr_slice[1]]
        off = vr_slice[0]
    out = []
    for i, v in enumerate(vr):
        zap = zap_list[i] if zap_list else zap_start + i
        e = {
            "leto": leto, "sken": sken, "pag": sken - 6, "zap": zap,
            "mesec": v.get("mesec") or mesec_default,
            "mesec_no": month_no(v.get("mesec") or mesec_default),
            "smrt": v.get("smrt"), "pokop": v.get("pokop"),
            "vas": v.get("vas"), "hisna": v.get("hisna"),
            "ime": v.get("ime"), "stan": v.get("stan"),
            "starost": v.get("starost"), "bolezen": v.get("bolezen"),
            "previden": v.get("previden"), "duhovnik": v.get("duhovnik"),
            "opomba": v.get("opomba"), "zap_raw": v.get("zaporedna"), "krop": None,
        }
        kp = KROP.get((sken, i + 1 + off))
        if kp:
            for k, val in kp.items():
                if k == "zap_krop":
                    e["zap_krop"] = val
                else:
                    e[k] = val
            e["krop"] = kp.get("krop") or "KROP"
        out.append(e)
    return out


def main():
    ent = []
    # s149: z1–z9 (MEJA-1877/78: glava-'1878'-SPLIT-v-z1 + restart-1; vrsta-10 = prazna!)
    ent += build(149, 1, vr_slice=(0, 9))
    for e in ent[:9]:
        if not e["mesec"]:
            e["mesec"], e["mesec_no"] = "Jänner", 1
    # s150–s156
    ent += build(150, 10)
    ent += build(151, 17)
    ent += build(152, 24)
    ent += build(153, 34)
    ent += build(154, 44)
    ent += build(155, 54)
    ent += build(156, 63)
    # s157 (P198-REUSE: ordinali-KROP-×2-seji 73–82; VLM-'63–72'-7→6-misread-3.×-potrjen!)
    ent += build(157, 73)
    for e in ent:
        if e["sken"] == 157:
            e["reuse"] = "P198-seja-VLM + KROP-ordinali-×2-seji (73–82!) + ta-seja-KROP-podrobnosti"

    # s158-tail z83–z85 — REUSE-1:1-iz-P198-entries_raw (KROP + RE-READ-SOGLASJE!)
    tail_reuse = P198_RAW.get("tail_1878", [])
    assert len(tail_reuse) == 3, f"tail_1878={len(tail_reuse)}"
    for t in tail_reuse:
        e = dict(t)
        e["reuse"] = "P198-seja-tail_1878-KROP + RE-READ-SOGLASJE-2-viri (sejni-zapis-1:1!) + ta-seja-podpis-KROP"
        ent.append(e)
    # ta-seja-podpis-doplačilo za z83
    for e in ent:
        if e["sken"] == 158 and str(e.get("zap", "")).startswith("83"):
            e["duhovnik"] = "Franz Jančar coop (ta-seja-KROP-podpis-'Franz Jančar coop'-JASNO!)"
            e["krop"] = (e.get("krop") or "") + " + s158-podpis83"

    # ——— normalizacija: mesec-ditto-naprej-polnjenje ———
    prev = None
    for e in ent:
        if e.get("mesec"):
            e["mesec_no"] = month_no(e["mesec"])
        if not e.get("mesec_no") and prev:
            e["mesec_no"] = prev["mesec_no"]
            if not e.get("mesec"):
                e["mesec"] = prev["mesec"]
        prev = e

    # ——— s148 = 1877-tail (P200-lead; ordinali-NEVIDNI!) ———
    vr148, _ = rows_of(148)
    tail77 = []
    for i, v in enumerate(vr148):
        tail77.append({
            "leto": 1877, "sken": 148, "pag": 142,
            "zap": f"s148-vrsta-{i + 1} (ord-neviden — scan-edge!)",
            "mesec": v.get("mesec"), "mesec_no": month_no(v.get("mesec")),
            "smrt": v.get("smrt"), "pokop": v.get("pokop"),
            "vas": v.get("vas"), "hisna": v.get("hisna"),
            "ime": v.get("ime"), "starost": v.get("starost"),
            "bolezen": v.get("bolezen"), "duhovnik": v.get("duhovnik"),
            "opomba": "1877-tail (P200-LEAD-SCOPE!)",
        })

    out = {
        "meta": {
            "leto": 1878, "knjiga": "04106",
            "preslikava": "pag = sken − 6 (P197/P198-veriga + md5-križna-validacija-ta-seja: s157/s158-sveže == P198-seja-1:1!)",
            "okvir": "s149 (MEJA-1877/78 + z1–z9) → s150–s157 → s158-tail (z83–z85)",
            "meja_1877_78": "★★★ s149: '18 78.'-SPLIT-VARIANTA-v-z1-datuma-celici (KROP-max: γ-7-s-prečko — VLM-'1848'-4/7-ZAVRJEN!) = 38.-POTRDITEV-invariante + restart-1 + Jänner-z1–z7 (z8–z9-Februar); s148 = 1877-Oct–Dez-tail (ordinali-NEVIDNI-scan-edge!)",
            "stevec": "85 vpisov (z1–z85) — P197-'restart-85→1'-napoved-EXAKT-POTRJENA + P198-'1878 ≈ 85'-lead-1:1!",
            "ordinalna_čistost": "1878 = ordinalno-ČISTO (85/85, brez-dup/skip — v-nasprotju-z-1881-z8-DUP + 1880-z55-SKIP + 1879-z28-DUP!); s156-z72-KROP-γ-7 (VLM-'62'-7→6-misread-3.×-potrjen!)",
            "kronološki_preskoki": "s149: Jänner 5→9→12→19→19(?)→25→26; s155-ord56: smrt-29-Juni → pokop-1-Juli (★★★ ULEDBA-#10-7.-instance!); s155-ord57: Juli-4/6",
            "uledba_10": "z56-Griblje-h33: smrt-'29'-Juni → pokop-'1.'-'Juli'-header-v-vrstici = 7.-instance (KROP-levi-strip!)",
            "duhovniki": "★★★ TRANZICIJA-1878-V-REALNEM-ČASU: Franz-DOVGAN (dominanta + Griblje-×8!) + substituendus-KOGEJ-coop (Griblje-×8-Jänner–April; VLM-'Fortin-aus-Kogelnik'-ZAVRJEN-KROP!) + Franz-JANČAR-coop (od-junija-raste: Griblje-×6+tail! — ★★★ JANČAR-NIT-1878→1883 = 6-LET, P198-'5-let'-RAZŠIRJENA!)",
            "krop_izreki": len(KROP),
            "neznan_vas": "★★★ 'Ukolk'[?]-×5-1878 (ord36/67/71/75/78) — NEZNANA-VAS (VLM-'Hrast'-ZAVRJEN-×3!) — cf. P195-'Wolk[~Volk?]'-1882 = verjetno-ista-vas; cf. P198-'Oho-b?'-1879",
        },
        "tail_1877": tail77,
        "entries": ent,
    }
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)

    grib = [e for e in ent if e["vas"] and "ribl" in str(e["vas"]).lower()]
    print(f"vpisov-1878: {len(ent)}")
    print(f"GRIBLJE: {len(grib)}")
    for e in grib:
        print(f"  z{e['zap']} h{e['hisna']} {str(e['ime'])[:40]} | {e['starost']} | {str(e['bolezen'])[:24]} | {str(e['duhovnik'])[:26]}")
    print(f"tail-1877-nota: {len(tail77)} vrstic")


if __name__ == "__main__":
    main()
