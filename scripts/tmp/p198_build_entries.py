#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P198 — agregacija 8 VLM-branj → 64 fizičnih vrstic za leto 1879
(mrliška 04106, pag = sken − 6; SANACIJA-RE-RUN: /tmp-wipe → re-fetch (velikosti
1:1-P197-seji!) + re-VLM-×6 + re-arbitraža-×5-cropov!).

Struktura dokazane preslikave (RE-READ-usklajena!):
  s158: tail-1878 z83–z85 (vrste 1–3 — RE-READ-SOGLASJE-s-KROP-hipotezo-1.-seje!)
        + 'Incipit annus'-band (vrsta 4, zap=None — re-read-'Summarischer'-zavrnjen!)
        + z1–z6 (vrste 5–10)
  s159: z7–z17 · s160: z18–z28 · s161: z28-DUPLIKAT + z29–z37 · s162: z38–z49
  s163 (P197-reuse): z50–z61 · s164 (P197-KROP-reuse): z62–z63-tail

★★★ ARBITRAŽE-RE-RUN-SEJE (max-zoom, obe-branji-dokumentirani!):
  A1 z28-DUP-datum: '1879-Julβ'-header + 'Junii-29.' + pokop-'1.' — RE-READ-'July-29/
     Aug-1'-ZAVRJEN (vzela-header-kot-mesec-smrti!) — ULEDBA-#10-STOJI!
  A2 z27-hiša: '44.' (dva-4-glifa-s-križcem!) — RE-READ-'14'-ZAVRJEN!
  A3 z27/z28-bolezen: 'Gehirnentzündung' (konec-'-entzündung'-z-umlautom!) —
     RE-READ-'Gichtarmzündung'-ZAVRJEN!
  A4 z1-ime: 'Mathias Novak' JASNO — RE-READ-'Dovgan'-ZAVRJEN! + vas-'Oho-b?'[?]
  A5 z2-vas: 'Mlake' — RE-READ-'Malše'-ZAVRJEN!
★★★ RE-READ-SOGLASJA: tail-83/84/85 ✓✓ (hipoteza-1.-seje-RAZREŠENA-v-fakt!),
  z28-'97-let'[~9J/97-re-read-vprašaj-ampak-97!] ✓✓, z28-DUP-Griblje-h20-44J ✓✓,
  z47-Griblje-h20-brez-starosti ✓✓ — 4-NEODVISNI-POTRJEVALCI!"""
import json
from pathlib import Path

VLM = Path("/tmp/p198/vlm-page")
P197 = Path("/tmp/p197")
OUT = Path("/tmp/p198/entries_raw.json")

# ——— KROP-izreki (agent-oči; ključi = VLM-vrsta-1-based; 1.-seja-cropi + RE-RUN-arbitraže!) ———
KROP = {
    # (sken, vlm_vrsta): {polja}
    (158, 1): {"zap_krop": "83 (KROP-hipoteza-1.-seje + RE-READ-SOGLASJE-2.-seje = RAZREŠENO-v-fakt!)",
               "ime": "Mathias Peglavc [~Marthe-re-read; KROP-crop-'Mathias'-jasno!]",
               "starost": "87 let [~17-re-read; KROP-crop-'87 J.'-jasno!]", "krop": "s158-meja-tail-incipit"},
    (158, 2): {"zap_krop": "84 (KROP + RE-READ-SOGLASJE!)"},
    (158, 3): {"zap_krop": "85 (KROP + RE-READ-SOGLASJE!) → 1878 = 85-vpisov!"},
    (158, 5): {"vas": "Oho-b? [~Otok-re-read; KROP-arbitraža-'Oho-b.1'; ne-Griblje!]",
               "ime": "Mathias Novak [KROP-arbitraža-JASNO — re-read-'Dovgan'-ZAVRJEN!]",
               "stan": "Unterzünglersohn? [~Vr/D-rünzgünglon; ~Wirtsgütlerson?]",
               "krop": "s158-z1-arbitraza"},
    (158, 6): {"vas": "Mlake (KROP-arbitraža — re-read-'Malše'-ZAVRJEN!)",
               "krop": "s158-z1-arbitraza"},
    (158, 7): {"starost": "10 dni (KROP-max: '10 Tagn.' jasno — VLM-'10-mesecev/Montag'-ZAVRJEN!)",
               "bolezen": "Friesen (KROP: 'Pf≈F-ligatura+'-isen'!) — FRISELN-družina!",
               "krop": "s158-z3-alfa-max"},
    (158, 9): {"ime": "Peter Šimec [~Simec-obeh-VLM! kanon-ŠIMEC-nit!]", "starost": "82 let [~88-re-read; KROP-crop-'82'-jasno!]",
               "krop": "s158-griblje-z5-z6"},
    (158, 10): {"ime": "Anna Zeliha [~Zeliho-obeh!]", "stan": "apf. ¼ Göttlanerstochter [KROP-crop-'apli ifra ¼ Göttlanstochton'; re-read-'½'-varianca!]",
                "starost": "74 let [~¾-J-re-read; KROP-crop-'74 J.'-jasno!]",
                "krop": "s158-griblje-z5-z6 + z6-bolezen-max ('Fraisen' POTRJEN-obeh-branj!)"},
    (159, 1): {"smrt": "23. (KROP-max: '23' jasno — ne-28!)", "krop": "s159-z7-z8-datumi"},
    (159, 9): {"starost": "½ leta (KROP: '½ J.' — VLM-'2-mes/7-dni?'+re-read-'1/2'-SOGLASJE!)",
               "ime": "Peter Bežek? [~Grčevac/Razlava-re-read — priimek-NERAZREŠEN [?]!",
               "bolezen": "Krämpfe? [~Farnism-KROP-neberljivo]", "krop": "s159-griblje-z15"},
    (160, 10): {"hisna": "44 (KROP-arbitraža-'44.'-dva-4-glifa — re-read-'14'-ZAVRJEN!)",
                "bolezen": "Gehirnentzündung (KROP-arbitraža: konec-'-entzündung'-umlaut — re-read-'Gichtarmzündung'-ZAVRJEN!)",
                "ime": "Maria Peglic? [~Pegelj-1.VLM/~Pezdirc-re-read — priimek-[~]!]",
                "stan": "apf. ½ Göttlaner-Kostgängerin? [~Kostbn/Kostbon-obeh!]",
                "duhovnik": "Franz Jančar coop (VLM-varianta-'Lončar' — ista-podpis-forenzika-P197!)",
                "krop": "s160-griblje-z27-z28 + z27-leva-arb + z27-bolezen-arb"},
    (160, 11): {"starost": "97 let ★KORPUS-REKORD (KROP-max-zoom-'9'+γ-7+'.'-identično-z27-'37.' + RE-READ-SOGLASJE-'97[~9J/97?]'!)",
                "bolezen": "Gehirnentzündung (KROP-fragment-'-ntzü-'+umlaut + arbitraža; re-read-'Gichtarmzündung'-ZAVRJEN!)",
                "ime": "Mathias Peglic? [~Pezdirc-re-read — priimek-[~]!]",
                "duhovnik": "Franz Jančar coop (VLM-varianta-'Vančar/Lončar')",
                "krop": "s160-z28-alter-max + z28-bolezen-max"},
    (161, 1): {"zap_krop": "28-DUPLIKAT (rdeči-margin: s160-konec-'28' + s161-top-'28' — pisar-dup! RE-READ-SOGLASJE-28!)",
               "mesec": "Juni (smrt 'Junii 29' — KROP-ARBITRAŽA: '1879-Julβ'-header + 'Junii-29.'-JASNO!)",
               "smrt": "29.", "pokop": "1. (Juli — ULEDBA-#10: mesec-v-vrstici! re-read-'Aug-1'-ZAVRJEN!)",
               "ime": "Martin Pezdirc [~Martinus-Pegdirič-obeh!]",
               "stan": "½ Götlaner-Unterzüngler? [~Unterzinglon-1./~Gutsingler-re-read!]",
               "starost": "44 let (SOGLASJE-obeh-branj!)",
               "bolezen": "Abmattsschwäche? [~Abzehrungsschwäche-1./~Abzehrungsfriesen-re-read!]",
               "duhovnik": "Franz Jančar coop (VLM-varianta-'Janičar')",
               "krop": "s161-top-z28-z29-dup + margin-strip + z28dup-tod-arb"},
    (162, 5): {"ime": "Martin Kuc (VLM-'Margarita-Musc'-ZAVRJEN — stan-'sohn'+tick-M!)",
               "stan": "apf. ex ½ Göttlanerssohn", "starost": "12 tednov? [~'12-W?d.'-KRIPTO; re-read-nejasno]",
               "krop": "s162-z42-gornelc + z42-alfa-max"},
    (162, 6): {"vas": "Otok (VLM-'Mali'-ZAVRJEN)", "starost": "3 leta (VLM-'37-let'-ZAVRJEN)",
               "bolezen": "Fraisen (VLM-'Griža'-ZAVRJEN)", "krop": "s162-z42-alfa-max"},
    (162, 8): {"starost": "42 let [~43-VLM]", "bolezen": "In folge der Gehirnentzündung (VLM-'Vodenica'-ZAVRJEN)"},
    (162, 9): {"starost": "2 meseca (VLM-'82-let-5-mes'-ZAVRJEN — KROP: '2 Mo. mon.'!)",
               "bolezen": "Fraisniša (VLM-'Vodenica'-ZAVRJEN)", "krop": "s162-z45-alfa-max"},
    (162, 10): {"ime": "Nelly? [~Molly-1./~Marija-1.VLM/~Marthy-re-read — 4-ime-varianti-NERAZREŠENE!] Abramšek? [~abramſkon-1./~Abram-re-read] — Pivk? [2.-vrstica-1.; ~Elend-re-read!]",
                "krop": "s162-z47-ime-max"},
    (162, 11): {"ime": "Nicolaus Jarovajšič [~Jerejšič-VLM]", "bolezen": "Chronischer Darmkatarrh (VLM-'Brummschnitt'-ZAVRJEN)"},
    (162, 12): {"starost": "69 let [~68-VLM]"},
}

MONTHS = {"Jänner": 1, "Feber": 2, "Februar": 2, "März": 3, "April": 4, "Mai": 5,
          "Juni": 6, "Junii": 6, "July": 7, "Juli": 7, "August": 8, "September": 9,
          "October": 10, "November": 11, "Dezember": 12, "December": 12}


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


def build(sken, zap_start, zap_list=None, mesec_default=None, vr_slice=None):
    """Preslikaj VLM-vrste skena → vpisi z ordinali (KROP-ključi = VLM-vrsta-1-based!)."""
    vr, _ = rows_of(sken)
    off = 0
    if vr_slice:
        vr = vr[vr_slice[0]:vr_slice[1]]
        off = vr_slice[0]
    out = []
    for i, v in enumerate(vr):
        zap = zap_list[i] if zap_list else zap_start + i
        e = {
            "leto": 1879, "sken": sken, "pag": sken - 6,
            "zap": zap,
            "mesec": v.get("mesec") or mesec_default,
            "mesec_no": month_no(v.get("mesec") or mesec_default),
            "smrt": v.get("smrt"), "pokop": v.get("pokop"),
            "vas": v.get("vas"), "hisna": v.get("hisna"),
            "ime": v.get("ime"), "stan": v.get("stan"),
            "starost": v.get("starost"), "bolezen": v.get("bolezen"),
            "previden": v.get("previden"), "duhovnik": v.get("duhovnik"),
            "opomba": v.get("opomba"),
            "zap_raw": v.get("zaporedna"), "krop": None,
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
    # s158: vrste 5–10 → z1–z6 (vrsta 4 = 'Incipit-annus'-band; 1–3 = tail-1878)
    ent += build(158, 1, zap_list=[1, 2, 3, 4, 5, 6], vr_slice=(4, 10))
    for e in ent[:6]:
        if not e["mesec"]:
            e["mesec"], e["mesec_no"] = "Jänner", 1
    # s159: z7–z17 · s160: z18–z28 · s161: z28-DUP + z29–z37 · s162: z38–z49
    ent += build(159, 7)
    ent += build(160, 18)
    ent += build(161, 28, zap_list=["28-DUP", 29, 30, 31, 32, 33, 34, 35, 36, 37])
    ent += build(162, 38)
    # s163 (P197-reuse): z50–z61
    ent += build(163, 50)
    # s164-tail (P197-KROP-reuse): z62–z63 — /tmp wiped → podatki-iz-SEJNEGA-ZAPISA
    # (P197-entries_raw-tail_1879, prebran-na-zacetku-te-seje — 1:1-vrednosti!)
    TAIL_REUSE = [
        {"leto": 1879, "sken": 164, "pag": 158, "zap": "z62-tail1879",
         "mesec": "December", "mesec_no": 12, "smrt": "22.", "pokop": "23.",
         "vas": "Krasinec", "hisna": "4", "ime": "Anna Cvikl [~ Ornic?]",
         "stan": "Pebli Anrin? [?], obležnica?", "starost": "74 let",
         "bolezen": "Altersschwäche [~]", "previden": "1",
         "duhovnik": "Franz Dorepan? [?]", "opomba": None, "zap_raw": "1", "krop": None},
        {"leto": 1879, "sken": 164, "pag": 158, "zap": "z63-tail1879",
         "mesec": "Jänner", "mesec_no": 1, "smrt": "31.", "pokop": "1.",
         "vas": "Certoviše", "hisna": "7", "ime": "Nicol Jakofčič [~]",
         "stan": "Gostilna? polhtar? Kinder [~]", "starost": "9 mesecev [~]",
         "bolezen": "Friesen", "previden": "1", "duhovnik": "Franz Vančar coop.",
         "opomba": "smrt 31.12.1879 → pokop 1.1.1880 (Jänner-vrstica!) — '1879-ima-63-vpisov' — ULEDBA-#10!",
         "zap_raw": "2", "krop": None},
    ]
    for t in TAIL_REUSE:
        e = dict(t)
        e["reuse"] = "P197-tail_1879-KROP (s164-rdeči-margini-62,63! — sejni-zapis-1:1!) — P199-jih-vzame!"
        ent.append(e)

    # ——— normalizacija: mesec_no-po-KROP + ditto-naprej-polnjenje (s163-vzorec!) ———
    prev = None
    for e in ent:
        if e.get("mesec"):
            e["mesec_no"] = month_no(e["mesec"])
        if not e.get("mesec_no") and prev:
            e["mesec_no"] = prev["mesec_no"]
            if not e.get("mesec"):
                e["mesec"] = prev["mesec"]
        prev = e

    # tail_1878 (s158 vrste 1–3) — ordinali 83–85 (KROP-hipoteza + RE-READ-SOGLASJE!)
    vr158, _ = rows_of(158)
    tail78 = []
    for i, v in enumerate(vr158[:3]):
        e = {
            "leto": 1878, "sken": 158, "pag": 152,
            "zap": f"{83 + i} (KROP-hip + RE-READ-SOGLASJE! [~zap_raw-{v.get('zaporedna')}-re-read-že-83/84/85!])",
            "mesec": v.get("mesec"), "mesec_no": month_no(v.get("mesec")),
            "smrt": v.get("smrt"), "pokop": v.get("pokop"),
            "vas": v.get("vas"), "hisna": v.get("hisna"),
            "ime": v.get("ime"), "stan": v.get("stan"),
            "starost": v.get("starost"), "bolezen": v.get("bolezen"),
            "previden": v.get("previden"), "duhovnik": v.get("duhovnik"),
            "zap_raw": v.get("zaporedna"), "krop": "s158-meja-tail-incipit",
        }
        kp = KROP.get((158, i + 1))
        if kp:
            for k, val in kp.items():
                if k != "zap_krop":
                    e[k] = val
        tail78.append(e)

    out = {
        "meta": {
            "leto": 1879, "knjiga": "04106",
            "preslikava": "pag = sken − 6 (P197-md5-×2 + TA-seja-re-fetch-velikosti-1:1 + printed-152–156-×5-vizualno!)",
            "sanacija": "/tmp-wipe → re-fetch (8/8-JPEG, velikosti-1:1-P197-seji: s163=421706 + s164=384600!) + re-VLM-×6 + re-arbitraža-×5 — deterministična-reprodukcija (vzorec-P156-sanacija!)",
            "okvir": "s158(tail-1878 z83–z85 + 'Incipit annus'-band + z1–z6) → s164-tail(z62,z63) + MEJA-1880/80",
            "meja_1878_79": "s158 'Incipit annus' (KROP-1.-seja! re-read-'Summarischer Anno'-ZAVRJEN) + big-'1879'-SPLIT-VARIANTA ('1 8'+'7 9'-STACKED-desno-TP!) = 37.-POTRDITEV-invariante + restart-85→1 (tail-KROP + RE-READ-SOGLASJE-83/84/85!)",
            "s157_ordinali": "KROP-margin-strip-1.-seje: 73–82 (VLM-'63–72'-7→6-sistemski-misread-obeh-sej!) → 1878 = 85-vpisov [P199-potrdi]",
            "anomalija_številčenja": "★★★ z28-DUPLIKAT (s160-konec-'28'-Peglic-h40 + s161-top-'28'-Pezdirc-h20 — pisar-dup; 63-ordinalov/64-fizičnih-vrstic; RE-READ-SOGLASJE-28! cf. P196-z8-DUPLIKAT!) = 3.-številčna-anomalija-04106",
            "kronološki_preskoki": "z6-Jan26 → z7-Jan23 → z8-Jan24 (KROP!) + Dezember-1879: 3→13→12→7→21 (s163-z57–z61-KROP!) — nazaj-zapolnitve/vpisi-po-pokopu",
            "uledba_10": "z28-DUP: smrt-'Junii 29' → pokop-'1.'-'Juli'-header-v-vrstici = 6.-instance (ARBITRAŽA-A1-ODLOČILNA!)",
            "krop_izreki": 24,
            "duhovniki": "Franz-JANČAR-coop (GRIBLJE-9/9-100%!) + Franz-DOVŽAN/DOVGAN (ne-Griblje) + Jančar-full-para",
        },
        "tail_1878": tail78,
        "entries": ent,
    }
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)

    grib = [e for e in ent if e["vas"] and str(e["vas"]).startswith("Griblje")]
    print(f"vpisov-1879: {len(ent)} (ordinalov-63 + 1-DUP)")
    print(f"GRIBLJE: {len(grib)} → {[(e['zap'], e['hisna']) for e in grib]}")
    print(f"tail-1878: {len(tail78)}")


if __name__ == "__main__":
    main()
