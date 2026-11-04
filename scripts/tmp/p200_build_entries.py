#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P200 — agregacija 7 VLM-branj (s142–s147) + P199-reuse s148 → 60 vpisov za
leto 1877 (mrliška 04106, 9/29). Preslikava: pag = sken − 6 (P197→P198→P199→
P200-veriga; md5-križna-validacija-ta-seja: s148/s149-sveže == P199-disk-1:1!).
Ordinali-NEVIDNI-na-vseh-6-straneh (forma-brez-stolpca/scan-edge) → ŠTEVJE-IZ-
VRSTIC (recept-s148-2.×!): s143=z1–z11 · s144=z12–z21 · s145=z22–z33 ·
s146=z34–z43 · s147=z44–z52 · s148(P199-reuse)=z53–z60 = 60 vpisov."""
import json
from pathlib import Path

VLM = Path("/tmp/p200/vlm-page")
P199_RAW = json.load(open("/tmp/p199/entries_1878.json"))
OUT = Path("/tmp/p200/entries_1877.json")

# ——— KROP-izreki (agent-oči; ključi = (sken, VLM-vrsta-1-based)) ———
KROP = {
    # ——— s142 (1876-Dez-TAIL — P201-LEAD-kontekst!) ———
    (142, 1): {"glava": "★ '1876.'-glava-v-z1 (Dezember-blok-tail-1876!)", "krop": "s142-z1"},
    (142, 4): {"vas": "Griblje (★h44 = PEGLIC-hiša-nit → 1878-z77-h44 + 1879-z27/z28-katastrofa!)",
               "starost": "24 uri [~KROP-'24 Stunden'-grafia; VLM-soglasje]",
               "bolezen": "Vesperstbrand?[?KROP-'Vesperstmörfer'-neberljivo — cf. 'Br[a]stfbrand'-klaster-1877!]",
               "krop": "s142-z4-vas + desno"},
    (142, 6): {"vas": "Griblje (★h75-nov-dokaz!)", "starost": "50 2/3 J [~KROP-'50⅔'-frakcija]",
               "bolezen": "Asthma (KROP-jasno!)", "krop": "s142-z6-vas + desno"},
    (142, 7): {"vas": "Griblje (★h16-nit → 1878-z41-JILAK-h16-DVOJNA-identifikacija!)",
               "ime": "Anna Pilah [~Spilak? — VLM-nesoglasje-2-viri]",
               "starost": "3 2/4 J [~KROP-'3½'-frakcija]", "bolezen": "Hirnentzündung (KROP!)",
               "krop": "s142-z7-vas + desno"},
    # ——— s143 (MEJA-1876/77 + z1–z11) ———
    (143, 1): {"zap_krop": "1 (restart-MEJA — ordinalni-stolpec-OFF-SCAN!)",
               "glava": "★★★ MEJA-1876/77 = s143-top: '18 77.'-glava-ODREZANA-off-scan (scan-edge!) — restart-evidenca = Dez-1876-nad (s142) + Jänner-pod + pokop-'1.'; [z1 = delno-odrezana-vrstica: smrt-[?], pokop-1., vas-[?odrezana]-h-'8'-v-2.-vrstici-vase-celice (vzorec-z2-Gradac+h8!), ime-'f f.'-kriptično [?] + nemška-opomba-'...in Podzemelj zu begraben' (KROP!) + nenadna-smrt]",
               "hisna": "8 [~hišna-v-2.-vrstici-vase-celice; ime-vase-ODREZANO!]",
               "krop": "s143-kotek-max + z1-nemška-opomba"},
    (143, 3): {"vas": "'Hrible'[?★★★ NOVA-LOKALNOST-'Hrib'? — 1.-pojav-v-korpusu! G-glyph-duel-3.×-POZITIVEN: ≠Gradac-G + ≠s145-Griblje-G + ≠z4-'Gribl[j]ar'-G (vsi-descender-G; z3-inicial-BREZ-descenderja!) — cf. 'Ukolk'[?]-1878-2.-neznana-vas!]",
               "hisna": "2 [~KROP-'2.'; VLM-'h1'-ZAVRJEN]",
               "ime": "Margaretha Tomc, [Witwe] des [Mathias ¼-]Gütlers, und Barbara[?] [~stan-glif]",
               "starost": "9 mesecev (KROP-'9 Monat' ✓)", "bolezen": "Fraisen (KROP-descender-F + VLM-'Frissen'-soglasje! — ★FRISEN-nit-do-1877!)",
               "duhovnik": "Franz Dovgan (KROP-podpis!)", "krop": "s143-z3-vas-max-8× + z3-desno + z3-bolezen-6×"},
    (143, 4): {"vas": "Primostek (KROP ✓)", "hisna": "10 (KROP ✓)",
               "ime": "Anna Maru, [Witwe] des Georg Grünzüchners, 'Gribl[j]ar[?]' [★GRIBLJE-MENCIJA-v-ime-stolpcu — vdova-po-Gribljarju! ne-Griblje-vpis!]",
               "starost": "57 let (KROP-'57' ✓)", "bolezen": "Magenbünden[? — VLM-'Magenkrebs'-nesoglasje-2-viri]",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s143-z4-ime-3-cropa + z4-desno"},
    (143, 5): {"starost": "47½ let (KROP-'47½' ✓)", "bolezen": "'___frauung'[? — KROP-'kindzfrauung'-neberljivo; VLM-'Vodnafranzing[~Wassersucht?]'-nesoglasje]",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s143-z5-desno"},
    (143, 6): {"vas": "'Hrible'[?NOVA-LOKALNOST-×2!]", "hisna": "2 [~KROP; VLM-'h1'-ZAVRJEN]",
               "ime": "Katharina Tomc (KROP ✓)", "starost": "3 ¼ J [KROP-'3¼'-frakcija-jasno — VLM-'3½'-ZAVRJEN-γ-frakcija!]",
               "bolezen": "MASERN (KROP-'Masern'-jasno! — ★★★ MASERN-nit-do-1877-na-'Hrib'-h2! → 1878-×2-adjacent + 1880-FLOOD!)",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s143-z6-vas + z6-desno"},
    (143, 7): {"vas": "'Hrible'[?NOVA-LOKALNOST-×3!]", "hisna": "1 (KROP-'1.' ✓)",
               "ime": "Maria Tomc, z 'H.' [~KROP-'z H.'-kratica-v-ime! — samo-referenca-na-'Hrib'!]",
               "starost": "19 let (KROP-'19' ✓)", "bolezen": "'im Feb. an Entzündung'[? — KROP-2-vrstici! ANOMALIJA: smrt-Jänner-28-ampak-opomba-im-Feb.!]",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s143-z7-vas + z7-desno"},
    (143, 8): {"starost": "32 dni [~KROP-'32 J.'-grafia]", "krop": "s143-z8-desno"},
    # ——— s145 (glava-'1877.'-v-z22-celici! + z22–z33) ———
    (145, 1): {"zap_krop": "22 (vrstno-štetje!)",
               "glava": "★★★ '1877.'-glava-ZAPISANA-V-Z22-DATUMSKI-CELICI (nad-'März-28.'-KROP-jasno — 'prečrtan'-izgled = prepisano-nad-mesecem!) = 39.-POTRDITEV-invariante 'glava-v-z1-celici-letnega-odseka' (VLM-'tail'-zastavica-NAPAČNI-ALARM!)",
               "krop": "s145-levi-rob-4×"},
    (145, 3): {"vas": "Griblje (KROP-G-descender-jasno!)", "hisna": "42 (KROP ✓)",
               "ime": "Catharina Pestotnik (KROP-'Catharina P...'-jasno!)",
               "stan": "¼ Güblner[?KROP-'¼ Gübln...'-grafia = ¼-Gütler]",
               "starost": "53 2/4 J [KROP-'53 2/4'-frakcija-jasno = 53½; VLM-soglasje]",
               "bolezen": "Asthma (KROP-jasno!)", "duhovnik": "substituendus Hoggai[s] Coop. (KROP-podpis = KOGEJ-subst.-grafia-P199-identična!)",
               "krop": "s145-z24-vas-ime + z24-desno"},
    (145, 5): {"vas": "Griblje (KROP ✓)", "hisna": "18 (KROP ✓ — ★h18-NIT!)",
               "ime": "Barbara Siniec [★ŠIMEC-grafia! — VLM-'Siniec'-soglasje; cf. 1878-z32/z44-Simec + 1881-h18-TIMEC!]",
               "stan": "¼ G. s[p]elinq: daughter [~KROP-'¼ G. tpelinq: daughter' = ¼-Gütler's-daughter!]",
               "starost": "8 ½ J [KROP-'8½'-frakcija ✓]", "bolezen": "Abzehrung (KROP-'Anbzoforning'-grafia-jasno!)",
               "duhovnik": "substituendus Hoggai[s] Coop. (KROP!)", "krop": "s145-z26-full + z26-desno"},
    # ——— s146 (z34–z43; VLM-v5/v6-DRIFT-popravek!) ———
    (146, 5): {"zap_krop": "38 (vrstno!)", "vas": "Krasinec (KROP ✓)", "hisna": "13 (KROP ✓)",
               "ime": "Nicolaus Jaklevič [~Jakofčič-grafia-nit-kontekst!]",
               "stan": "nepol. ½ Gütterspflege[?KROP-'gütterspfeger'-grafia]",
               "krop": "s146-v5-full"},
    (146, 6): {"zap_krop": "39 (vrstno!)", "vas": "Griblje (KROP-G-descender ✓ — VLM-soglasje!)",
               "hisna": "8 (KROP ✓ — ★h8-nov-dokaz-1877!)", "ime": "Catharina Jakofčič (KROP ✓)",
               "stan": "nepol. Tochter des Gübln[er]s: Johann und Anna, ¼ G. (KROP-2-vrstici!)",
               "starost": "9 ½ Mon. [KROP-'9½ Mon.' ✓]", "bolezen": "Hirnfall (KROP-jasno!)",
               "duhovnik": "Franz Dovgan (KROP-podpis-dvojna-črta!)", "krop": "s146-v6-full + v6-desno"},
    # ——— s147 (z44–z52) ———
    (147, 5): {"zap_krop": "48 (vrstno!)", "vas": "Griblje (KROP ✓)", "hisna": "62 (KROP-'62'-jasno!)",
               "ime": "Barbara Hure [~KURE-grafia! VLM-'Hurie'-varianta — cf. 1878-z9-Marcus-Kure[~Hure]!]",
               "stan": "Erbin des Anton, ¼ G. [~KROP-'lrb Anton... ¼ J.'-grafia]",
               "starost": "3 ¼ J [KROP-'3¼'-frakcija — VLM-'3½'-ZAVRJEN-γ-frakcija!]",
               "bolezen": "'Br[a]stfbrand'[?KROP-neberljivo-fraza — VLM-'Brennfieber'-ZAVRJEN; isti-word-×3-klaster-z49/z52!]",
               "duhovnik": "Franz Dovgan (KROP-podpis-velik!)", "krop": "s147-z48-datum-5× + z48-desno"},
    (147, 6): {"zap_krop": "49 (vrstno!)", "vas": "Griblje (KROP ✓)", "hisna": "57 (KROP-'57'-jasno! — ★h57-NIT → 1878-z80-Logar-GEHIRNENTZÜNDUNG!)",
               "ime": "Johann Lozar (KROP-jasno!)", "stan": "des Michael, Gütler [~KROP-'Sed Michael... Gütler' = Sohn/Erbe-des-Michael?]",
               "starost": "2 J. (KROP ✓)", "bolezen": "'Br[a]stfbrand'[?isti-word-kot-z48!]",
               "duhovnik": "Franz Dovgan (KROP-podpisan — podpis-continuira!)", "krop": "s147-z48z49-vas-ime + z48z49-desno"},
    (147, 8): {"zap_krop": "51 (vrstno!)", "vas": "Griblje (KROP ✓)", "hisna": "53 (KROP ✓ — ★h53-NIT → 1878-z83-PEGLAVC-87J!)",
               "ime": "Maria Pezdinc [★★★ PEZDINC-GRAFIA-NIT-#7! (→ 1878-×6-'Vezdirz/Pozdrin/Pecolar' + 1879-katastrofa-h40/h44!) KROP-'Pezdinc'-jasno — VLM-'Perdinc'-t/d-zmeda!]",
               "stan": "nepol. Tochter des Johann und [der] Anna, ½ G. (KROP-2-vrstici!)",
               "starost": "1 Jahr (KROP-'1 Jahr' ✓)", "bolezen": "Wasserfriesl (KROP-jasno! — VLM-soglasje! 'friesl'-grafia = FRISELN-nit!)",
               "duhovnik": "Franz Dovgan (KROP-podpis-dvojna!)", "krop": "s147-v8v9-full + z51z52-desno"},
    (147, 9): {"zap_krop": "52 (vrstno!)", "vas": "Griblje (KROP ✓)", "hisna": "6 [KROP-'6'-jasno-samo — VLM-'h6[~46?]'-REŠENO: ni-46!]",
               "ime": "Anna Jakofčič (KROP — VLM-'Jakopič'-ZAVRJEN! — ★JAKOFČIČ-×2-1877-z39+z52!)",
               "stan": "nepol. Tochter des Mathias und [der] Anna, ¼ G. (KROP!)",
               "starost": "3 ¾ J (KROP-'3¾'-frakcija-jasno!)", "bolezen": "'Br[a]stfbrand'[?isti-word-klaster-3/3!]",
               "duhovnik": "Franz Dovgan (KROP!)", "krop": "s147-v8v9-full + z51z52-desno"},
    # ——— s148 (P199-REUSE: z53–z60 + z56-KROP-ta-seja!) ———
    (148, 4): {"zap_krop": "56 (vrstno!)",
               "vas": "Griblje (KROP-G-10×-jasno! — P199-soglasje!)",
               "hisna": "12 [★★★ KROP-'12'-JASNO — P199-'h18[~]'-POPREVEK! (h18-nit-referenca-v-P199-z1-bloku-oslabljena!)]",
               "ime": "Katharina Dragoš [KROP-'Dragoš'-š-čarec; VLM-'Dragos'-soglasje]",
               "stan": "'lbb.'[?KROP-abb-3-črkovna — neberljivo]",
               "starost": "21 J [KROP-'21'-2/7-KURRENT-zmeda-'71'; VLM-'21'-soglasje → 21!]",
               "bolezen": "'Alt___sfr____'[?KROP-neberljivo — VLM-'Albrandstbrünst[~]'-nesoglasje-2-kandidata]",
               "duhovnik": "Franz Dovgan (KROP-podpis-dvojni-flourish!)", "krop": "s148-v4-full + z56-desno2 + z56-starost-bolezen-5× + v4_ini10-10×"},
}

MONTHS = {"Jänner": 1, "Feber": 2, "Februar": 2, "März": 3, "April": 4, "Aprilis": 4, "Mai": 5,
          "Juni": 6, "Junii": 6, "July": 7, "Juli": 7, "August": 8, "September": 9,
          "October": 10, "November": 11, "Dezember": 12, "Dec": 12, "Nov.": 11, "Nov": 11}


def month_no(mes):
    if not mes:
        return None
    m = str(mes).strip().split()[0]
    for k, v in MONTHS.items():
        if m.lower().startswith(k[:5].lower()):
            return v
    return None


def rows_of(sken):
    d = json.load(open(VLM / f"s{sken}.json"))
    return d.get("vrstice", []), d


def build(sken, zap_start, vr_slice=None, mesec_default=None, leto=1877, prefix=""):
    vr, _ = rows_of(sken)
    off = 0
    if vr_slice:
        vr = vr[vr_slice[0]:vr_slice[1]]
        off = vr_slice[0]
    out = []
    for i, v in enumerate(vr):
        e = {
            "leto": leto, "sken": sken, "pag": sken - 6, "zap": f"{prefix}{zap_start + i}",
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
    # s143: z1–z11 (MEJA-1876/77-top! z1-delno-odrezana!)
    ent += build(143, 1)
    for e in ent[:11]:
        if not e["mesec"]:
            e["mesec"], e["mesec_no"] = "Jänner", 1
    # s144: z12–z21 (März-glava!)
    ent += build(144, 12, mesec_default="März")
    # s145: z22–z33 (glava-'1877.'-v-z22-celici + März28→Juni)
    ent += build(145, 22)
    # s146: z34–z43 (Juni26→Sept11)
    ent += build(146, 34)
    # s147: z44–z52 (Sept28→Okt17)
    ent += build(147, 44)

    # ——— normalizacija: mesec-ditto-naprej ———
    prev = None
    for e in ent:
        if e.get("mesec"):
            e["mesec_no"] = month_no(e["mesec"])
        if not e.get("mesec_no") and prev:
            e["mesec_no"] = prev["mesec_no"]
            if not e.get("mesec"):
                e["mesec"] = prev["mesec"]
        prev = e

    # ——— s148 = z53–z60 (P199-REUSE tail_1877 — KROP-ta-seja: z56-h12!) ———
    tail77 = P199_RAW.get("tail_1877", [])
    assert len(tail77) == 8, f"tail_1877={len(tail77)}"
    for i, t in enumerate(tail77):
        e = dict(t)
        e["zap"] = 53 + i
        e["reuse"] = "P199-seja-tail_1877-VLM + ta-seja-KROP (z56-definitivno!)"
        kp = KROP.get((148, i + 1))
        if kp:
            for k, val in kp.items():
                if k == "zap_krop":
                    e["zap_krop"] = val
                else:
                    e[k] = val
            e["krop"] = (kp.get("krop") or "") + " + P199-reuse"
        ent.append(e)

    grib = [e for e in ent if e["vas"] and "ribl" in str(e["vas"]).lower() and "Gribljar" not in str(e["ime"] or "")]
    # izloči 'Griblje'-mencije (z4-Anna-Maru 'Gribljar' = Primostek!) — vas-filter-zadostuje

    out = {
        "meta": {
            "leto": 1877, "knjiga": "04106",
            "preslikava": "pag = sken − 6 (P197→P198→P199-veriga + md5-križna-ta-seja: s148/s149-sveže == P199-disk-1:1!)",
            "okvir": "s143 (MEJA-1876/77 + z1–z11) → s144 (z12–z21) → s145 (z22–z33) → s146 (z34–z43) → s147 (z44–z52) → s148-P199-reuse (z53–z60)",
            "meja_1876_77": "★★★ s143-top: '18 77.'-glava-ODREZANA-off-scan (scan-edge — nasprotje-s148-'18 77.'-vidna? NE — s148-brez-glave!) — restart-evidenca: s142-Dez-1876-nad + s143-Jänner-pod + z1-pokop-'1.'; ★★★ 39.-POTRDITEV-invariante = s145-'1877.'-glava-ZAPISANA-V-Z22-DATUMSKI-CELICI (mid-year-glava-vrsta — 'prečrtan'-izgled = prepis-nad-mesecem! VLM-'tail'-zastavica-NAPAČNI-ALARM!)",
            "meja_1877_78": "s149 (P199-38.-potrditev-reuse: '18 78.'-SPLIT-v-z1 + restart-1!)",
            "konec_1877": "z60 = s148-v8: Dez 21. (Krasinec-h41-Katharina-Bahovič[?]-68J)",
            "stevec": "60 vpisov (z1–z60) — vrstna-aritmetika 11+10+12+10+9+8 + datum-veriga-continuous (Jän1→Feb28/Mär1→März5→März28→Juni26→Sept28→Okt18→Dez21→1878-restart!); P199-'1877 ≈ 85-?ven'-ocena-FALSIFICIRANA (groba-ocena!)",
            "ordinalna_metodologija": "ordinali-NEVIDNI-na-vseh-6-straneh (forma-BREZ-stolpca/scan-edge-off!) → ŠTEVJE-IZ-VRSTIC (recept-s148-2.×!) — P199-lekcija-#18-double-scan-RE-ALIGNMENT-uporabljena-×15!",
            "duhovniki": "★★★ KOGEJ-OBDOBJE-RAZŠIRJENO-NAZAJ: substituendus-Kogej/Hoggai-Coop-1877-Jänner→Mai (z2/z8/z9/z11 + Griblje-z24/z26!) — P199-'1878-Jänner–April'-RAZŠIRJENA! + Franz-DOVGAN-dominanta-1877 (Griblje-×6: z39/z48/z49/z51/z52/z56 + Tomc-×3!) + NO-Jančar-1877 (★★★ JANČAR-NIT-1878→1883-SPREMENJENA-NE-RAZŠIRJENA!)",
            "griblje": "8 vpisov / 8 hiš (h42, h18, h8, h62, h57, h53, h6, h12) — P199-tail-z4-'h18[?]'→KROP-h12-POPREVEK!",
            "hrib_nova_lokalnost": "★★★ 'Hrible'[?='Hrib'?]-×3-1877 (z3/z6/z7-Tomc-klaster-h2/h2/h1!) — 1.-pojav-v-korpusu; G-glyph-duel-3.×-POZITIVEN (≠G: Gradac-G + s145-Griblje-G + z4-'Gribl[j]ar'-G-vsi-descender; z3-inicial-brez!) — cf. 'Ukolk'[?]-1878 = 2.-neznana-vas-v-2-letih!",
            "pezdinc_nit": "★★★ PEZDINC-GRAFIA-#7 (z51-Maria-Pezdinc-h53!) — veriga: 1877-z51-PEZDINC → 1878-×6 (Vezdirz×2/Pozdrin/Pezdir(e)/Pecolar) → 1879-katastrofa-h40/h44!",
            "h_niti": "h18-ŠIMEC-NIT (z26-Siniec→1878-Innec?-z1 + z32/z44-Simec + 1881-TIMEC!) · h53-NIT (z51-Pezdinc→z83-Peglavc-87J!) · h57-NIT (z49-Lozar→z80-Logar-GEHIRN!) · h44-1876-Dez (tail! Barbara-Kavčič-24-URE-Vesperstbrand[?]→1878-z77 + 1879-katastrofa!) · h16-NIT (tail-1876-Spilak?[?]→1878-z41-DVOJNA!)",
            "brastfbrand_klaster": "★★★ 'Br[a]stfbrand'[?]-×3-OKTOBER-1877 (z48-h62 + z49-h57 + z52-h6 — zaporedoma! VLM-'Brennfieber/Bran[dt]'-nesoglasja; isti-word-3×) — cf. tail-1876-'Vesperstmörfer[?]'-h44!",
            "uledba_10": "z24-Griblje-h42: smrt-29-April → pokop-1-Mai = 8.-instance (KROP-datum! cf. P199-×7!)",
            "krop_izreki": len(KROP),
            "vlm_krop_korekcije": "×7: z48-3½→3¼J + z6-3½→3¼J + z56-h18[?]→h12 + s148-v3-'Kreuzsteing[?]'→'Abzehrung' + z39-VLM-v5/v6-DRIFT (real-v6=Griblje ✓) + z2/z3-'Frissen/Amirsan'→'Fraisen' (z3-VLM-soglasje) + z52-'Jakopič'→'Jakofčič' + z52-h6[~46?]→h6",
        },
        "tail_1876": [
            {"leto": 1876, "sken": 142, "pag": 136, "zap": f"s142-vrsta-{i + 1} (1876-Dez-TAIL — P201-LEAD!)",
             "mesec": v.get("mesec"), "smrt": v.get("smrt"), "pokop": v.get("pokop"),
             "vas": v.get("vas"), "hisna": v.get("hisna"), "ime": v.get("ime"),
             "starost": v.get("starost"), "bolezen": v.get("bolezen"),
             "opomba": "1876-tail (P201-LEAD-SCOPE; Griblje-×3: z4-h44-24-URE + z6-h75 + z7-h16!)"}
            for i, v in enumerate(rows_of(142)[0])
        ],
        "entries": ent,
    }
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)

    print(f"vpisov-1877: {len(ent)}")
    print(f"GRIBLJE: {len(grib)}")
    for e in grib:
        print(f"  z{e['zap']} h{e['hisna']} {str(e['ime'])[:42]} | {e['starost']} | {str(e['bolezen'])[:26]} | {str(e['duhovnik'])[:28]}")
    hrib = [e for e in ent if e["vas"] and "rible" in str(e["vas"]).lower()]
    print(f"'HRIB'[?]: {len(hrib)}")
    for e in hrib:
        print(f"  z{e['zap']} h{e['hisna']} {str(e['ime'])[:36]} | {e['starost']} | {str(e['bolezen'])[:24]}")
    print(f"tail-1876-nota: {len(out['tail_1876'])} vrstic (Griblje-×3!)")


if __name__ == "__main__":
    main()
