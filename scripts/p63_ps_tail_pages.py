#!/usr/bin/env python3
# P63 — zaključne strani registra PS (138–139): deterministična konsolidacija
# transkripcij tail tabel (VLM 2 prehoda + agent-oči 3. prehod na fokusiranih
# izrezih 5×) → dokaz + runtime. Metodika P59 (2-od-3 konsenz, [~] negotovo,
# alternativе dokumentirane).
#
#   str. 139 = Blatt IIb (P63 KOREKCIJA — glava je 'Nro. des Blattes.',
#              prejšnja očesna razlaga 'Nro. des Hauses.' očesna napaka →
#              P58 open #6 zaprt):
#     LEVA knjižna stran  ('Des Eigenthümers'): Parzelle 41–60 + Dominical,
#     Rustical (prazno), Haus Nº (rdeče), Vor und Zuname (številke 62–80!),
#     Stand, Wohnort (rdeče); vsote 82|81, 125|183.
#     DESNA knjižna stran ('Des Grundstückes'): Kulturs Gattung 81–100,
#     Flächen (N.Oe + QK), Classe 101–120, Ertrag (prazna, r1 '101⁴⁄₅'[~]),
#     Capital fl (velike, rdeče) + kr (male, rdeče); Fürtrag 189|1228;
#     vsota 162|1447; robni zapisi.
#   str. 138: leva tabela IZBRISANA (bledi ostanki 'T. 191'[~] @ r14 +
#     parzelle 23/24[~], '89'/'86'[~] @ r27; rdeče prečrtani zapisi 18–40
#     @ srednja kolona [~]); desna = 'Zusammenstellung der Grundstücke'
#     (Wiese 1–20, Classe 21–40, vsota 101|15320 [~], rob 89|78 [~]).
#
# Invariante I1–I10, --check bajtno determinističen.
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "research/issue17/ps-raw")
OUT_EV = os.path.join(ROOT, "research/issue17/ps-tail-pages.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-tail-pages.json")
BH_RT = os.path.join(ROOT, "src/data/atlas/ps-blatt-headers.json")


def fail(msg):
    print(f"FAIL I: {msg}")
    sys.exit(1)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load(name):
    p = os.path.join(RAW, name)
    if not os.path.exists(p):
        fail(f"manjka {name}")
    return json.load(open(p))


# ————— I1 pokritost: 11 tail VLM branj + blatt-138/139 × 2 prehoda —————
TAIL_PARTS = [
    "tail-139-left-a.json", "tail-139-left-b.json",
    "tail-139-right-a.json", "tail-139-right-b.json",
    "tail-139-colsL-a.json", "tail-139-colsL-b.json",
    "tail-139-colsR-a.json", "tail-139-colsR-b.json",
    "tail-139-full-b2.json",
    "tail-138-left-a.json", "tail-138-right-a.json",
]
TAIL_PARTS_SET = set(TAIL_PARTS)
for n in TAIL_PARTS:
    load(n)
for s in ["", "-pass2"]:
    load(f"blatt-138{s}.json")
    load(f"blatt-139{s}.json")

# ————— CONS: agent-oči 3. prehod (fokusirani izrezi 5×) + 2-od-3 konsenz —————
# p139 LEVA: row: [dominical, haus, vorUndZuname, stand, wohnort]
#  vrednost 'X' = soglasje ≥2 prehoda; ('X', [alt...]) = razhodi → [~]
CONS_LEFT = {
    1:  ["1", "1082", "G. l. fin.[~]", None, "63"],
    2:  ["1", "1030", "62", "3", "1135"],
    3:  ["1", ("998", ["398"]), "63", "9", ("289", ["859", "259"])],
    4:  ["3", "266", "64", "2", "410"],
    5:  ["1", "695", "65", "6", "1318"],
    6:  ["5", "88", "66", "6", "1560"],
    7:  ["1", ("1048", ["1045", "1095"]), "67", "9", "384"],
    8:  ["1", ("286", ["386"]), "68", "3", ("1294", ["1394", "1396"])],
    9:  ["1", ("1284", ["1204", "1254"]), "69", "10", "901"],
    10: ["1", ("1317", ["1217", "1244"]), "70", "8", "324"],
    11: [("7", ["1"]), "960", "71", "13", ("4", ["7"])],
    12: [("7", ["1"]), "943", "72", ("4", ["1"]), "1482"],
    13: [("7", ["1"]), ("973", ["993"]), "73", ("4", ["1"]), "824"],
    14: ["1", "1359", "74", "6", ("1082", ["1052"])],
    15: ["1", "946", "75", ("8", ["5"]), ("1246", ["1244"])],
    16: ["1", "306", "76", ("4", ["1"]), ("789", ["489"])],
    17: ["2", "762", "77", "2", "180"],
    18: ["1", "1484", "78", "2", ("864", ["564"])],
    19: ["5", ("145", ["115", "118"]), "79", ("8", ["5"]), ("834", ["534"])],
    20: ["3", ("345", ["844", "944"]), "80", "3", ("1159", ["1154"])],
}

# p139 DESNA: row: [kultur, noe, klafter, classe, capitalFl, capitalKr]
CONS_RIGHT = {
    1:  ["81", "4", ("590", ["490"]), "101", "1860", "4"],
    2:  ["82", "8", "686", "102", ("1146", ["146"]), "7"],
    3:  ["83", ("3", [None]), "296", "103", None, None],
    4:  ["84", "2", ("869", ["864"]), "104", "831", "4"],
    5:  ["85", "6", ("1809", ["1309"]), "105", "909", "8"],
    6:  ["86", "4", ("991", ["921"]), "106", "982", "15"],
    7:  ["87", "3", "64", "107", "1086", "16"],
    8:  ["88", "12", ("1179", ["1177"]), "108", "1234", "6"],
    9:  ["89", "10", "27", "109", "80", "12"],
    10: ["90", "8", ("193", ["198"]), "110", "128", "6"],
    11: ["91", "13", ("1462", ["1162"]), "111", "781", "6"],
    12: ["92", "11", ("1807", ["1507"]), "112", "366", "4"],
    13: ["93", "14", ("1829", ["1329"]), "113", ("1149", ["1169"]), None],
    14: ["94", "12", "904", "114", ("999", ["997"]), "6"],
    15: ["95", "11", "178", "115", "1060", ("8", ["5"])],
    16: ["96", "11", ("805", ["888"]), "116", "1513", "10"],
    17: ["97", "11", "1006", "117", "649", "13"],
    18: ["98", "13", ("693", ["679"]), "118", "1346", "16"],
    19: ["99", "17", ("449", ["479"]), "119", "1046", "12"],
    20: ["100", "13", "701", "120", "584", None],
}

SUMS_LEFT = {"dominical": "82", "haus": "81", "stand": "125", "wohnort": "183"}
SUMS_RIGHT = {"furetragNoe": "189", "furetragKlafter": "1228",
              "totalCapA": "162", "totalCapB": "1447"}

P138_LEFT_REMAINS = [
    {"row": 14, "blatt": "T. 191[~]", "parzelle": "23[~]"},
    {"row": 15, "parzelle": "24[~]"},
    {"row": 27, "blatt": ("89", ["86"]), "parzelle": ("86", ["89"])},
]
P138_LEFT_RED_INK = ("rdeče prečrtani zapisi 18–40 @ srednja kolona leve strani "
                     "(x≈320–420, cona Rustical/Haus) — oči z4/z6, VLM neviden [~]")
P138_RIGHT = {
    "title": "Zusammenstellung der Grundstücke[~]",
    "rows": 20,
    "kulturRange": "1.–20. (Wiese)", "classeRange": "21–40",
    "sums": {"noe": "101", "klafter": "15320"},
    "edge": {"vrednost": ("89", ["78"]), "opomba": "robni zapis spodaj [~]"},
    "vmesVsota": "Suma 120 (rdeče prečrtano) + Suma 403 @ ~r20/~r40 — oči z4/z6 [~]",
}


def norm(v):
    """('998', [alt]) → '998' + flag + alternatives; čisti string → soglasje."""
    if v is None:
        return None, False, []
    if isinstance(v, tuple):
        return v[0], True, v[1]
    return v, False, []


def main():
    # ————— I4: IIb konsenz (blatt-139 2 prehoda '11b' + tail-139-left-a 'IIb'
    #        + oči 'IIb') → pageAttribution P59 == 'IIb' —————
    b139 = [load("blatt-139.json"), load("blatt-139-pass2.json")]
    blatt139_vals = []
    for d in b139:
        v = [x.get("value") for x in (d["parsed"].get("blatt") or [])]
        blatt139_vals.append(v)
    if not any("11b" in (v or []) for v in blatt139_vals):
        fail(f"I4 blatt-139 prehodi ne vsebujejo '11b': {blatt139_vals}")
    ta = load("tail-139-left-a.json")["parsed"]
    if ta["vrstice"][0].get("blatt") != "IIb":
        fail("I4 tail-139-left-a r1 blatt != 'IIb'")
    bh = json.load(open(BH_RT))
    pa139 = bh["pageAttribution"]["139"]
    if pa139.get("blatt") != "IIb":
        fail(f"I4 pageAttribution p139 != 'IIb': {pa139.get('blatt')}")
    if bh["pageAttribution"]["138"].get("blatt") is not None:
        fail("I4 pageAttribution p138 != None")

    # ————— I2: parzelle 41–60 (CONS + tail-139-left-a + blatt-139) —————
    expected = [str(i) for i in range(41, 61)]
    for d in b139:
        pz = [x.get("parzella") for x in d["parsed"]["vrstice"]][:20]
        if pz != expected:
            fail(f"I2 blatt-139 parzelle: {pz[:5]}...")
    pzA = [v.get("parzelle") for v in ta["vrstice"]][:10]
    if pzA != expected[:10]:
        fail(f"I2 tail-139-left-a parzelle: {pzA}")

    # ————— I3: VorUndZuname 62–80 —————
    vz = [norm(CONS_LEFT[i][2])[0] for i in range(1, 21)]
    if vz[1:] != [str(i) for i in range(62, 81)]:
        fail(f"I3 VorUndZuname: {vz}")

    # ————— I5: kultur 81–100, classe 101–120, Fürtrag —————
    kul = [norm(CONS_RIGHT[i][0])[0] for i in range(1, 21)]
    cla = [norm(CONS_RIGHT[i][3])[0] for i in range(1, 21)]
    if kul != [str(i) for i in range(81, 101)]:
        fail(f"I5 kultur: {kul}")
    if cla != [str(i) for i in range(101, 121)]:
        fail(f"I5 classe: {cla}")
    rb = load("tail-139-right-b.json")
    vs = rb["parsed"].get("vsote") or []
    if not any(str(v.get("kol1")) == "189" and str(v.get("kol2")) == "1228" for v in vs):
        fail(f"I5 Fürtrag 189|1228 ni v tail-139-right-b vsote: {vs}")
    clb = load("tail-139-colsL-b.json")["parsed"]
    vsL = clb.get("vsote") or []
    if not any(str(v.get("vrednost")) == "82" for v in vsL) or \
       not any(str(v.get("vrednost")) == "81" for v in vsL):
        fail(f"I7 82|81 ni v colsL-b vsote: {vsL}")
    crb = load("tail-139-colsR-b.json")["parsed"]
    vsR = crb.get("vsote") or []
    if not any("183" in str(v) for v in vsR):
        fail(f"I7 183 ni v colsR-b vsote: {vsR}")

    # ————— I6: Capital kolone pini —————
    if norm(CONS_RIGHT[1][4])[0] != "1860" or norm(CONS_RIGHT[20][4])[0] != "584":
        fail("I6 Capital fl pini (r1=1860, r20=584)")
    kr_vals = [norm(CONS_RIGHT[i][5])[0] for i in range(1, 21)]
    kr_sum = sum(int(v) for v in kr_vals if v)
    if kr_sum != 153:
        fail(f"I6 Capital kr vsota {kr_sum} != 153")

    # ————— I8: p138 —————
    gl = load("tail-138-left-a.json")["parsed"]
    gl_rows = {v.get("row"): v for v in gl["vrstice"] if any(
        k for k in v if k not in ("row",) and v[k])}
    if 14 not in gl_rows or "191" not in str(gl_rows[14].get("blatt", "")):
        fail(f"I8 p138 r14 ostanki: {gl_rows.get(14)}")
    gr = load("tail-138-right-a.json")["parsed"]
    if not gr["vrstice"] or "Wiese" not in str(gr["vrstice"][1]):
        fail("I8 p138 Zusammenstellung '1. Wiese' @ r2")

    # ————— izpisi —————
    def row_out(r, c):
        vals, flags, alts = [], [], {}
        for k, v in zip(["dominical", "haus", "vorUndZuname", "stand", "wohnort"], c):
            nv, fl, a = norm(v)
            vals.append(nv)
            if fl:
                flags.append(k)
            if a:
                alts[k] = a
        return {"row": r, "dominical": vals[0], "haus": vals[1],
                "vorUndZuname": vals[2], "stand": vals[3], "wohnort": vals[4],
                "flags": flags, "alternatives": alts or None}

    def row_out_right(r, c):
        vals, flags, alts = [], [], {}
        for k, v in zip(["kultur", "noe", "klafter", "classe", "capitalFl", "capitalKr"], c):
            nv, fl, a = norm(v)
            vals.append(nv)
            if fl:
                flags.append(k)
            if a:
                alts[k] = a
        return {"row": r, "kultur": vals[0], "noe": vals[1], "klafter": vals[2],
                "classe": vals[3], "capitalFl": vals[4], "capitalKr": vals[5],
                "flags": flags, "alternatives": alts or None}

    n_flags = sum(len(row_out(i, CONS_LEFT[i])["flags"]) +
                  len(row_out_right(i, CONS_RIGHT[i])["flags"]) for i in range(1, 21))

    ev = {
        "task": "P63 — zaključne strani registra PS (138–139): transkripcija tail tabel + korekcija p139 = Blatt IIb (P58 open #6 zaprt)",
        "date": "2026-10-14",
        "method": ("3 neodvisna prehoda: (A) agent-oči na izrezih 3×/4×/5×; (B) VLM glm-5v-turbo na polnih "
                   "izrezih (tail-139-left/right, tail-138-left/right); (C) VLM glm-5v-turbo na fokusiranih "
                   "izrezih kolon 5× (tail-139-colsL/colsR/full-b2) + agent-oči 3. prehod na desnih kolonah 5×; "
                   "2-od-3 konsenz, razhodi → [~] + alternatives; p138 desna in p139 desna tretji prehod očesno"),
        "inputs": {
            "tailReads": "research/issue17/ps-raw/tail-*.json (11 VLM branj, skip-existing)",
            "blattReads": "research/issue17/ps-raw/blatt-138{,-pass2}, blatt-139{,-pass2}.json (P62)",
            "crops": "/tmp/p63/ (p138 6× 4×; p139 head/sum/full/cols/right/desna @ 2–5×, Lanczos q95)",
            "blattHeaders": "src/data/atlas/ps-blatt-headers.json (P59 v2 + P63 korekcija)",
        },
        "p139": {
            "glava": "'Nro. des Blattes.' | 'Benennung des Riedes.' | 'Nro. der Parzelle.' | "
                     "'Gesetzliche Eigenschaft des Grundstückes' (Dominical | Rustical ×3) | 'Haus Nº' | "
                     "'Vor und Zuname' | 'Stand' | 'Wohnort' — DESNA: 'Des Grundstückes': 'Kulturs Gattung' | "
                     "'Flächen Inhalt' (N.Oe Sache | Quadrat Klafter) | 'Classe' | 'Reiner jährlicher Ertrag "
                     "in Metall-Münze' (fl|kr) | 'Capital Werth nach p.Ct.' (fl|kr) | 'Anmerkung.'",
            "blatt": "IIb @ r1 + ditto (P63 KOREKCIJA — glava je 'Nro. des Blattes.', prejšnja očesna "
                     "razlaga 'Nro. des Hauses.' očesna napaka; 'b' [~]; P58 open #6 ZAPRT)",
            "parzelle": "41–60 (20 vrstic, naraščajoče)",
            "vorUndZuname": "rokopisne ŠTEVILKE 62–80 @ r2–20 (ne imena); r1 = 'G. l. fin.'[~] — "
                            "interpretacija (konskripcija/Einlage?) ODPRTA [~]",
            "leva": [row_out(i, CONS_LEFT[i]) for i in range(1, 21)],
            "desna": [row_out_right(i, CONS_RIGHT[i]) for i in range(1, 21)],
            "desnaOpombe": {
                "ertrag": "Ertrag fl|kr PRAZNA @ r2–20; r1 = '101⁴⁄₅'/'101 ja8'[~] (blede zapis z popravek)",
                "capitalKr_r3": "r3 = prazna ('—' prečrtano)",
                "robniZapisi": "'156', '9', '6.49'[~], '116', '146'[~] @ spodnji rob [~]",
            },
            "vsote": {"leva": SUMS_LEFT, "desna": SUMS_RIGHT,
                      "opomba": "82|81 = vsoti pod Dominical/Haus črto (vsota vidnih Dominical = 32 — "
                                "rekapitulacija čez več strani [~]); 125|183 = vsoti pod Stand/Wohnort; "
                                "Fürtrag 189|1228 = preneseno s prejšnje tabele [~] (QK te strani = 16543); "
                                "162|1447 = vsoti pod Capital črto (razlaga enot/fl-kr ODPRTA [~])"},
        },
        "p138": {
            "leva": {"status": "tabela IZBRISANA (bledi ostanki)",
                     "ostanki": P138_LEFT_REMAINS,
                     "rdeciZapisi": P138_LEFT_RED_INK,
                     "podglave": "'Lotus'/'Lotas'[~], 'Lung'/'Lang'[~], 'Al'/'Ae'[~] rokopisne podglave "
                                 "pod 'Vor und Zuname' (p138 z1 oči + VLM) [~]"},
            "desna": P138_RIGHT,
        },
        "structureImpact": {
            "blattNumerele": "I–V + IIb (pod-list) — IIb NOV v strukturi registra PS",
            "pageAttribution": {"138": None, "139": "IIb"},
            "v2Impact": "p138/139 brez vrstic v v2 → perBlattAmbiguity 211/110/17 NESPREMENJENI; "
                        "join v2 NESPREMENJEN (disciplina P56/P58)",
        },
        "invariants": ["I1 pokritost 11/11 tail VLM + 2/2 blatt × 2 prehoda", "I2 parzelle 41–60",
                       "I3 VorUndZuname 62–80", "I4 IIb konsenz == P59 pageAttribution",
                       "I5 kultur 81–100 + classe 101–120 + Fürtrag 189|1228",
                       "I6 Capital pini (r1 1860, r20 584, kr Σ=147)",
                       "I7 vsote 82|81 + 125|183", "I8 p138 ostanki + Zusammenstellung",
                       "I9 dokaz ⊇ runtime bajtno", "I10 determinizem"],
        "statusLine": (f"P63 TAIL STRANI: p139 = Blatt IIb (Parzelle 41–60 + lastninske kolone; P58 open #6 "
                       f"ZAPRT — glava 'Nro. des Blattes.', ne 'Haus'), p138 = izbrisana leva + "
                       f"'Zusammenstellung der Grundstücke' desna; transkripcija 20+20 vrstic, {n_flags} "
                       f"flagov [~]; join v2 nespremenjen"),
        "verdictSi": ("Zaključne strani registra PS paleografsko zaključene: p139 nosi Blatt IIb z "
                      "parcelami 41–60 (duplikat številk Blatt I pod pod-listom IIb) in lastninskimi "
                      "kolonami (Haus Nº rdeče, 'Vor und Zuname' izpolnjen s številkami 62–80 — ne imena); "
                      "desna stran = kultura rekapitulacija 81–100 s Classo 101–120. p138 = izbrisana "
                      "tabela z bledimi ostanki + 'Zusammenstellung der Grundstücke' (Wiese 1–20). "
                      "Prejšnja očesna razlaga 'Nro. des Hauses.' @ p139 = očesna napaka (korigirana); "
                      "enote vsot 82|81, 125|183, 162|1447 ostajajo razlagalno odprte [~]"),
        "verdictEn": ("Tail pages of the PS register completed paleographically: p139 carries Blatt IIb "
                      "with parcels 41-60 (duplicate Blatt I numbers under sub-leaf IIb) and owner columns "
                      "(red Haus Nº, 'Vor und Zuname' filled with numbers 62-80, not names); right page = "
                      "culture recap 81-100 with Classe 101-120. p138 = erased table with faint remains + "
                      "'Zusammenstellung der Grundstuecke' (Wiese 1-20). The earlier 'Nro. des Hauses.' "
                      "reading was an eye error (corrected); unit meaning of sums 82|81, 125|183, 162|1447 "
                      "remains open [~]"),
        "next": [
            "razlaga 'Vor und Zuname' = številke 62–80 (konskripcija/Einlage?) — povezava s PF protokolom",
            "razlaga enot vsot 82|81, 125|183, 162|1447 (dominikalni/rustikalni deleži?) [~]",
            "p138 rdeči zapisi 18–40 @ srednja kolona — paleografska razlaga [~]",
            "'Zusammenstellung der Grundstücke' (p138 desna) ↔ kulture tabele p61–99 — povezava [~]",
        ],
    }

    runtime = {
        "version": 1,
        "task": ev["task"],
        "date": ev["date"],
        "blattIIb": {"page": 139, "parzelle": "41–60", "vorUndZuname": "62–80",
                     "vsote": {"dominical": "82", "haus": "81", "stand": "125", "wohnort": "183"}},
        "leva": [row_out(i, CONS_LEFT[i]) for i in range(1, 21)],
        "desna": [row_out_right(i, CONS_RIGHT[i]) for i in range(1, 21)],
        "p138": {"leva": {"status": "izbrisana", "ostanki": P138_LEFT_REMAINS},
                 "desna": P138_RIGHT},
        "statusLine": ev["statusLine"],
    }

    # ————— I9: dokaz ⊇ runtime bajtno —————
    ev_sub = json.loads(json.dumps(ev))
    ev_sub["runtime"] = runtime
    with open(OUT_EV, "w") as f:
        json.dump(ev_sub, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    with open(OUT_RT, "w") as f:
        json.dump(runtime, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    # ————— I10: determinizem —————
    if "--check" in sys.argv:
        with open(OUT_EV, "rb") as f:
            ev_b = f.read()
        with open(OUT_RT, "rb") as f:
            rt_b = f.read()
        with open(OUT_EV, "w") as f:
            json.dump(ev_sub, f, indent=1, ensure_ascii=False, sort_keys=True)
            f.write("\n")
        with open(OUT_RT, "w") as f:
            json.dump(runtime, f, indent=1, ensure_ascii=False, sort_keys=True)
            f.write("\n")
        with open(OUT_EV, "rb") as f:
            if f.read() != ev_b:
                fail("I10 dokaz ni bajtno determinističen")
        with open(OUT_RT, "rb") as f:
            if f.read() != rt_b:
                fail("I10 runtime ni bajtno determinističen")
        print("I10 --check: PASS")

    print(f"OK: p139 leva 20 vrstic, desna 20 vrstic, flagi [~] {n_flags}")
    print(f"OK: vsote {SUMS_LEFT} | Fürtrag 189|1228 | 162|1447")
    print(f"OK: dokaz {OUT_EV}, runtime {OUT_RT}")


if __name__ == "__main__":
    main()
