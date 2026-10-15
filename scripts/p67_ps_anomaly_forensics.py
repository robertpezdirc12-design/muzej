#!/usr/bin/env python3
# P67 — FORENZIČNI PAKET ANOMALIJ: skok II·IV, sosledje flagi, R1↔R2
# divergence, univerzalna lastniška disjunktnost (issue #13; kandidati iz
# P66 `next` #3/#4 + P64/P65 divergence + nova meritve).
#
# P67 NE SPREMINJA v2 joina (disciplina P56/P58/P59/P65/P66) — MERI in
# DOKAZUJE s štirimi determinističnimi deli:
#
#   A — SKOK II·IV (1603, 1604, 1605) = ARTIFAKT DVOJNE KURRENT
#       ZAMENJAVE. Dokazi (vsi bajtno preverjeni v I2):
#       • p78 (Blatt II, Wüstung "Pod Grabino"): strip 2× prehod ==
#         1501–1520 (2× bajtno); vrstice 5–14 (1505–1514) rdeče
#         prečrtane (opomba); oči na 4× izrezu (ta seja, worklog):
#         r1–r4 = 1501–1504 jasno, r5–r8 prečrtane; kontinuiteta
#         p76→p77→p78 = 1461–1480 → 1481–1500 → 1501–1520 (strip
#         p77 2× bajtno 1481–1500); karta KO 1544: blok 1461–1500 ima
#         12 poligonov, blok 1121–1200 (P38-era branje p74/p76/p77) 0.
#         → v2 p78 vrstice 1603/1604/1605 = P38 pass1+pass2 napačno
#         (Kurrent 5→6); prave: 1503/1504/1505.
#       • p93 (Blatt IV): strip 2× vrstice 11–20 == 1911–1920 (bajtno),
#         vrstice 1–10 garbled 19xx varianti (191–199, 190 — izguba
#         vodilnih); oči: r1–r8 = 1901–1908, r1–r4+r6–r7 rdeče
#         prečrtane, r5 (1905) čista; arbitraža P59: "1901–1907
#         prečrtano"; karta: blok 1901–1907 ima 7 poligonov (TOČNO
#         prečrtani blok!) + 1910/1913/1914. P38 pass1 = 1001–1020
#         (9→0), pass2 = 1601–1620 (9→6) — dve sistemski napaki.
#         → v2 p93 vrstice 1603/1604/1605 napačno; prave:
#         1903/1904/1905.
#       • p87 (Blatt II): P38 pass1 = 661–680, pass2 = 1681–1700,
#         strip = 161–180 (odrezane vodilne); oči (4× izrez): r1–r8 =
#         1681–1688 (r5, r7 prečrtani) → pass2 PRAVILEN. v2 p87
#         vrstice 661/663/666/667/671/673/674/675/676/679/680 =
#         pass1 napačno (prave 1681–1700, odmik +1020); 11 v2 vrstic
#         nosi LAŽNO geometrijo (poligoni 661–680 = Blatt I p36
#         instance — koordinate bajtno identične p36, merjeno).
#       • posledice: 1603/1604 = lažni fuziji II 1503/1504 × IV
#         1903/1904 (skok II·IV izgine); 1605 = fuzija II 1505
#         (prečrtan) × IV 1905; 661/671 = lažni fuziji I 661/671 ×
#         II 1681/1691 → čez-Blatt primera RAZPADA; p93 (IV) in p98
#         (III) nosita ISTI obseg 1901–1920 pod različnima Blattoma
#         (disjunktni lastniki — učbeniški per-Blatt primež).
#       • karta kot neodvisna priča: 1903/1904/1905 poligoni
#         obstajajo (SV imen lekacije ~1.6 km JugZ), 1503/1504/1505 in
#         1681–1700 NE; 16xx poligoni (1603, 1604/1-3, 1605) so na
#         tretji lokaciji — v2 jih je pripisal fuzijam (lažno).
#       • renumerifikacijska specifikacija (20 preslikav, P68):
#         p78 3× (160x→150x), p93 3× (160x→190x), p87 11× (+1020);
#         kolizije: 1503–1505 proste, 1903/1905 že na p98 (III),
#         1904 prosta, 1681–1700 proste.
#       • projekcija (številčenjski nivo): base 800→802; multi-page
#         211→208; čez-Blatt 110→107; R3-single 101 nespremenjen;
#         split/atribucija novih (1903: III delež ~0.708 → pas split
#         [~]; 1905: R2b areaIncomplete [~]) = izhod P68 pipeline.
#         Runtime: −14 brez geometrije (3× p78, 11× p87); p93 3×
#         re-claim (1904 čisto, 1903/1905 konflikt z III@p98 [~]).
#
#   B — 5 SOSLEDJE FLAGOV (646, 661, 1821, 2141, 2143; 11 vrstic) =
#       ARTEFAKT OBSEGA JOINA (+ meja strani), NE anomalija registra.
#       Sosledje (P65) išče soseda ±1 znotraj v2 vrstic ISTE strani.
#       Manjkajoči sosedje (M) na vsaki zastavljeni strani:
#       • obstajajo v registru (P38 branja jih vidijo z imeni: 645
#         'Ulrich Franz', 647 'Gemeinde', 662 'Mülley Franzl', 1822
#         'Büller Lorenz', 1823 'Gavčnik Miha', 1824 'Gavčnik Gregor',
#         2142 'Häupler Martin', 2144–2147 …), 
#       • njihove številke NIMAJO poligonov v karti KO 1544 → izpadle
#         iz v2 (join filter; matchedShare 38.6 %),
#       • 1820 (p63) in 2140 (p109) IMATA geometrijo in sta v v2 —
#         a na PREJŠNJI strani (meja strani je nevidna per-page
#         kontroli): 1821/2141/661 so začetki strani.
#       → 11/11 flagov razloženih: M ne-prazna ∧ vsi M brez poligona
#         (∨ začetek strani s sosedom na prejšnji strani).
#
#   C — R1↔R2 DIVERGENCI (930, 671):
#       • 671 = RAZREŠENA s p87 dokazom — ni divergencia: II instanca
#         @p87 je pravzaprav 1691 (druga parcela); 671 ostane samo I
#         @p36 (enstranska).
#       • 930 = ostaja [~] z merjenim dokazom: II @p49 (Hüsse Malle,
#         'Zehorn', 241 QK, moda B pas ✓) vs III @p99 (Brünig Michel,
#         'Wiesen', 776 QK, moda B ✗); DISJUNKTNA lastnika; 930 ima
#         sosede ±1 na OBEH straneh (929/931 v v2 na p49 IN p99);
#         pageMap blok 921–940: karta 9 poligonov (mehka podpora).
#
#   D — UNIVERZALNA LASTNIŠKA DISJUNKTNOST: za VSEH 110 čez-Blatt
#       več-stranskih base (ne samo 39 split iz P66): lastniki per
#       Blatt DISJUNKTNI 110/110 (rekurzivno iz v2 × P59
#       pageAttribution) → per-Blatt številčenje: ista številka pod
#       različnima Blattoma = 2 RAZLIČNI realni parceli. 39 split
#       polja bajtno == P66 (I5); 71 atributiranih tudi 71/71
#       disjunktnih → atribucija (R1/R2a/R2b) je dodelitev geometrije
#       instanci, ne identiteta parcele [~].
#
# Vhodi (committed, 27× sha256 pin):
#   research/issue17/ps-parcels-geo-v2.json       (rowsEvidence 1093)
#   research/issue17/ps-blatt-headers.json        (P59 pageAttribution)
#   src/data/atlas/ps-attribution-full.json       (P65 runtime 211)
#   src/data/atlas/ps-split-pack.json             (P66 runtime 39)
#   research/issue17/ps-register-topology.json    (P56 pageMap)
#   research/georef-n83/gurs/parcels-ko1544-merged.json (2117 poligonov)
#   research/issue17/ps-raw/blatt-76|77|78|78-pass2|93.json (strip)
#   research/issue17/ps-raw/ps-035-pass2|036-pass2|063|064|078|
#     078-pass2|079-pass2|085-pass2|087|087-pass2|093|093-pass2|098|
#     094-pass2|110|125-pass2.json                (P38 dokazi)
# Izhodi:
#   research/issue17/ps-anomaly-forensics.json    (dokaz)
#   src/data/atlas/ps-anomaly-forensics.json      (runtime, bajtna proj.)
#
# Invarianti (FAIL ob padu):
#   I1 vhodni pini: 27× sha256 + števci 1093/800/211/39/110
#   II2/A: 6 vrstic 1603/1604/1605 (p78×3, p93×3) + strip 2× p78 ==
#      1501–1520 bajtno + strip 2× p93 r11–20 == 1911–1920 ∧ r1–10 ==
#      garbled set + p77 strip == 1481–1500 + p87 pass2 == 1681–1700
#      + arbitražni nizi ("1501–1520", "1901–1907") + karta (1901–1907
#      ⊆ poligoni; 1503–1505, 1681–1700 ∉; 1121–1200 ∅; 1461–1500 ≥ 10)
#   I3/A kolizije renumerifikacije: 1503–1505, 1904, 1681–1700 proste;
#      1903/1905 samo p98; 11 p87 vrstic koordinatno == p36 (lažna geom.)
#   I4/B flagi == P66 (5 base, 11 vrstic, bajtno); M per flag ne-prazna
#      ∧ vsi M brez poligona; 1820/2140 v v2 (meja strani)
#   I5/C 671: II instanca @p87 (renum. 1691) — pravila P65 držijo;
#      930: moda B pas ✓@p49 ✗@p99 + disjunktna lastnika + sosedi ±1
#      na obeh straneh
#   I6/D 110 čez-Blatt: ownerRelation == disjoint × 110; 39 split
#      ownersByBlatt bajtno == P66; 0 prehodnih strani ('·') v množici;
#      brez lat/lng/areaModern/ratio v izpisu (areaQK dovoljen)
#   I7 dokaz ⊇ runtime (bajtno podmnožica)
#   I8 determinizem — --check bajtno identično
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_EV = os.path.join(ROOT, "research/issue17/ps-anomaly-forensics.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-anomaly-forensics.json")

PINS = {
    "research/issue17/ps-parcels-geo-v2.json":
        "ebb8f7298de713e73bc7417f392d60c7e5eb03a6675f96317320188750e27731",
    "research/issue17/ps-blatt-headers.json":
        "650f13dccab1da70a60d04c41ce9f7887ca94eafea8a0a7927c104ca899b76f3",
    "src/data/atlas/ps-attribution-full.json":
        "e714c3550e759a59f6577e24f3aa314e42e30c951353e7f290d360a4bba16b57",
    "src/data/atlas/ps-split-pack.json":
        "f5fcd8e9f6d4891104fa6fa4d65887f232e06a7ac171b164d33903ddadff67f2",
    "research/issue17/ps-register-topology.json":
        "2fddc76fb94b69fed55170220fa8dfa3ace4a9466043d264b8b8df788e78a50c",
    "research/issue17/PS-full-v2.json":
        "81f140e989d50a67656a81ed166c5b2c400617a9a1036a85758df0cf312fc92c",
    "research/georef-n83/gurs/parcels-ko1544-merged.json":
        "fee91fca736348f40ef11d38b7a5b51d51656a9768cda648f4d737029bb3941f",
    "research/issue17/ps-raw/blatt-76.json":
        "e2aca956f40e0e18e9af8b1ddcfa4f6a10696e074d2fadbec635f0f973da0fb1",
    "research/issue17/ps-raw/blatt-77.json":
        "c69fa7b00af9ac9c814a3ae69220fbcb9a8834e77dae8326fd016a1b3a048cbc",
    "research/issue17/ps-raw/blatt-78.json":
        "dfe3e7539c3fa590e52b42474197071e8c6d732def4f787ee2b8a7d4ec498430",
    "research/issue17/ps-raw/blatt-78-pass2.json":
        "28bf987a04d47cb320520ef1b041c0e9671ea92084ae20fc13b3b8c620a3915a",
    "research/issue17/ps-raw/blatt-93.json":
        "4a1e3047add687de0b291a7f26eeca3f3c4ff2ae48c36b1707ab41dbd5da1b84",
    "research/issue17/ps-raw/ps-035-pass2.json":
        "166a0a8fa6197858da270c63d8a456e6602b58e1dfa8a4b25bc900bfa0ae4582",
    "research/issue17/ps-raw/ps-036-pass2.json":
        "7f606b86951f8a350946ec441da7d13921ae9c8e3a7a0174a3abdcbae78674a6",
    "research/issue17/ps-raw/ps-063.json":
        "8e72d4553c5df30037a81c4a40d88cd55bbc5dc89299b2de4afde8601999e895",
    "research/issue17/ps-raw/ps-064.json":
        "27798813d5b24bf7454b86451ac62ee5fef69d92aca92bd2680e43c6ad6ff541",
    "research/issue17/ps-raw/ps-078.json":
        "4a34bc35c33d747ac9fc8aef7eae82cf99db47d0ce3f3cc69020ec53c27872be",
    "research/issue17/ps-raw/ps-078-pass2.json":
        "37249e79aa551ea1c827b23360832e34d57495dd9aa510849b5c9cf39ffad4ac",
    "research/issue17/ps-raw/ps-079-pass2.json":
        "f57cfc668fe6d907e8b22cebcd85634c0853467874f6dc6728196adcd284ac8e",
    "research/issue17/ps-raw/ps-085-pass2.json":
        "29047bc4256a56a8e3372d13ac6000a8ddcbefaeb012374fb692c673082cdb89",
    "research/issue17/ps-raw/ps-087.json":
        "56d3091fa2453b2f4f1d25d1e4c7d5fcbfd2beef779a339a06f3e5e0d6f50b9f",
    "research/issue17/ps-raw/ps-087-pass2.json":
        "ed58996f7c53c7dde087968ce89c9a9ca94400d1117d3be5ce5e80d797ec4a5a",
    "research/issue17/ps-raw/ps-093.json":
        "617217fa9f4f49ee85f75a816759cdd6c10054b26e8584cb9f6655ac9b65842f",
    "research/issue17/ps-raw/ps-093-pass2.json":
        "e3b60506287552e8490331c1119831aa6b76cd3167032d210feff35a17e3eaf9",
    "research/issue17/ps-raw/ps-094-pass2.json":
        "9d8e5111aa8d9b04c936f19d9a0c5b992e45d011b6f2e25cbd6f1c4836ed0a65",
    "research/issue17/ps-raw/ps-098.json":
        "eb03515d70d89f18d81b2de3301fb6a0597972362fa3f05d21c39b2415a5e3a9",
    "research/issue17/ps-raw/ps-110.json":
        "e794924e02189dd6d086c0a939938fc705ffd0b69a2ecf085c1572a96bb42310",
    "research/issue17/ps-raw/ps-125-pass2.json":
        "4188a6bd34e89ca601f2e3d64a59b474c10bddeff74d90ce9a1cc99bbfc9fb23",
}

V2 = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v2.json")
P59 = os.path.join(ROOT, "research/issue17/ps-blatt-headers.json")
P65RT = os.path.join(ROOT, "src/data/atlas/ps-attribution-full.json")
P66RT = os.path.join(ROOT, "src/data/atlas/ps-split-pack.json")
TOPO = os.path.join(ROOT, "research/issue17/ps-register-topology.json")
SELFV2 = os.path.join(ROOT, "research/issue17/PS-full-v2.json")
GEO = os.path.join(ROOT, "research/georef-n83/gurs/parcels-ko1544-merged.json")

EXPECTED_ROWS = 1093
EXPECTED_BASES = 800
EXPECTED_MULTI = 199  # P68 v3 (P65 bases; v2: 211)
EXPECTED_SPLIT = 36  # P68 v3 (v2: 39)
EXPECTED_CROSS = 98  # P68 v3 (v2: 110)
EXPECTED_R3 = 101

FLAG_BASES = ["1821", "2141", "2143", "646", "1903"]  # P68 v3 (661 razpadla; 1903 nov)
FLAG_ROWS = 11  # P68 v3 (661 izpada, 1903 nastopi; v2: 11)

# renumerifikacijska specifikacija (20 preslikav) — P68 izvedba
RENUM = [
    {"page": 78, "old": "1603", "new": "1503"},
    {"page": 78, "old": "1604", "new": "1504"},
    {"page": 78, "old": "1605", "new": "1505"},
    {"page": 93, "old": "1603", "new": "1903"},
    {"page": 93, "old": "1604", "new": "1904"},
    {"page": 93, "old": "1605", "new": "1905"},
    {"page": 87, "old": "661", "new": "1681"},
    {"page": 87, "old": "663", "new": "1683"},
    {"page": 87, "old": "666", "new": "1686"},
    {"page": 87, "old": "667", "new": "1687"},
    {"page": 87, "old": "671", "new": "1691"},
    {"page": 87, "old": "673", "new": "1693"},
    {"page": 87, "old": "674", "new": "1694"},
    {"page": 87, "old": "675", "new": "1695"},
    {"page": 87, "old": "676", "new": "1696"},
    {"page": 87, "old": "679", "new": "1699"},
    {"page": 87, "old": "680", "new": "1700"},
]

GEO_FIELDS = ("lat", "lng", "areaModern", "ratio")


def fail(msg):
    print(f"FAIL I: {msg}")
    sys.exit(1)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def raw_nums(name):
    """Številke vrstic P38 branja (pass2 pasivno, sicer pass1)."""
    fn = os.path.join(ROOT, "research/issue17/ps-raw", name)
    d = json.load(open(fn))
    return [str(r.get("parzella")) for r in d["parsed"]["vrstice"]]


def raw_row(name, parz):
    fn = os.path.join(ROOT, "research/issue17/ps-raw", name)
    d = json.load(open(fn))
    for r in d["parsed"]["vrstice"]:
        if str(r.get("parzella")) == parz:
            return {"name": r.get("name"), "kultur": r.get("kultur"),
                    "klafter": r.get("klafter")}
    return None


def strip_nums(name):
    fn = os.path.join(ROOT, "research/issue17/ps-raw", name)
    d = json.load(open(fn))
    return [str(v.get("parzella")) for v in d["parsed"]["vrstice"]]


def main():
    v2 = json.load(open(V2))
    p59 = json.load(open(P59))
    p65 = json.load(open(P65RT))
    p66 = json.load(open(P66RT))
    topo = json.load(open(TOPO))
    geo = json.load(open(GEO))

    rows = v2["rowsEvidence"]
    page_attr = p59["pageAttribution"]
    p65_bases = p65["bases"]
    split_65 = {k: e for k, e in p65_bases.items() if e.get("status") == "split"}
    page_map = {e["page"]: e for e in topo["pageMap"]}

    # ————— I1 vhodni pini —————
    for rel, want in sorted(PINS.items()):
        got = sha256(os.path.join(ROOT, rel))
        if got != want:
            fail(f"I1 sha256 {rel} ≠ pin (drift)")
    if len(rows) != EXPECTED_ROWS:
        fail(f"I1 rowsEvidence {len(rows)} ≠ {EXPECTED_ROWS}")
    all_bases = {r["base"] for r in rows}
    if len(all_bases) != EXPECTED_BASES:
        fail(f"I1 base {len(all_bases)} ≠ {EXPECTED_BASES}")
    if len(p65_bases) != EXPECTED_MULTI:
        fail(f"I1 P65 base {len(p65_bases)} ≠ {EXPECTED_MULTI}")
    if len(split_65) != EXPECTED_SPLIT:
        fail(f"I1 split base {len(split_65)} ≠ {EXPECTED_SPLIT}")
    cross_65 = {k: e for k, e in p65_bases.items()
                if e.get("status") != "R3-single"}
    if len(cross_65) != EXPECTED_CROSS:
        fail(f"I1 čez-Blatt base {len(cross_65)} ≠ {EXPECTED_CROSS}")
    r3_65 = {k: e for k, e in p65_bases.items()
             if e.get("status") == "R3-single"}
    if len(r3_65) != EXPECTED_R3:
        fail(f"I1 R3 base {len(r3_65)} ≠ {EXPECTED_R3}")

    rows_by_base = defaultdict(list)
    rows_by_page = defaultdict(list)
    for r in rows:
        rows_by_base[r["base"]].append(r)
        rows_by_page[r["page"]].append(r)
    def num_key(x):
        s = str(x["parzella"])
        head = "".join(ch for ch in s if ch.isdigit())
        return (int(head) if head else 0, s)

    for pg in rows_by_page:
        rows_by_page[pg].sort(key=num_key)

    geo_exact = {p["st"] for p in geo}
    geo_pref = {p["st"].split("/")[0] for p in geo}

    # ————— II2/A: dokazi za p78/p93/p87 —————
    # A1: 6 vrstic fuzij
    fused = {}
    for b in ("1603", "1604", "1605"):
        rs = sorted(rows_by_base.get(b, []), key=lambda x: x["page"])
        if [r["page"] for r in rs] != [78, 93]:
            fail(f"I2 {b}: strani {[r['page'] for r in rs]} ≠ [78, 93]")
        fused[b] = [{"page": r["page"], "owner": r["owner"],
                     "kultur": r["kultur"], "areaQK": r["areaQK"]} for r in rs]
    if fused["1603"][0]["owner"] != "Pachler Martin" or \
       fused["1603"][1]["owner"] != "Verboten (er) Bueb?":
        fail("I2 1603 lastniki se ne ujemajo z dokumentiranimi")
    if fused["1604"][0]["owner"] != "Ullrich Otto" or \
       fused["1604"][1]["owner"] != "Piringer Mathäus":
        fail("I2 1604 lastniki se ne ujemajo z dokumentiranimi")

    # A2: strip p78 == 1501..1520 (oba prehoda, bajtno)
    want78 = [str(n) for n in range(1501, 1521)]
    for f in ("blatt-78.json", "blatt-78-pass2.json"):
        if strip_nums(f) != want78:
            fail(f"I2 strip {f} ≠ 1501–1520")
    # A3: strip p93: r11–20 == 1911..1920; r1–10 garbled {191..199,190}
    for f in ("blatt-93.json",):
        nums = strip_nums(f)
        if nums[10:] != [str(n) for n in range(1911, 1921)]:
            fail(f"I2 strip {f} r11–20 ≠ 1911–1920")
        if sorted(nums[:10]) != sorted(["191", "192", "193", "194", "195",
                                        "196", "197", "198", "199", "190"]):
            fail(f"I2 strip {f} r1–10 ≠ garbled 19xx set")
    # A5: strip p77 == 1481..1500 (kontinuiteta); blatt-76 garbled 161–180
    want77 = [str(n) for n in range(1481, 1501)]
    if strip_nums("blatt-77.json") != want77:
        fail("I2 strip blatt-77.json ≠ 1481–1500")
    w76 = [str(n) for n in range(161, 181)]
    if strip_nums("blatt-76.json") != w76:
        fail("I2 strip blatt-76.json ≠ garbled 161–180 (odrezane vodilne)")
    # A7: p87 pass2 == 1681..1700 (oči r1–8 = 1681–1688)
    want87 = [str(n) for n in range(1681, 1701)]
    if raw_nums("ps-087-pass2.json") != want87:
        fail("I2 ps-087-pass2 ≠ 1681–1700")
    # A4: arbitražni nizi v pageAttribution
    src78 = page_attr["78"]["source"]
    src93 = page_attr["93"]["source"]
    if "1501–1520" not in src78:
        fail("I2 p78 arbitraža ne vsebuje '1501–1520'")
    if "1901–1907 prečrtano" not in src93:
        fail("I2 p93 arbitraža ne vsebuje '1901–1907 prečrtano'")
    # A6: karta kot priča
    for n in range(1901, 1908):
        if str(n) not in geo_pref:
            fail(f"I2 karta nima poligona {n} (pričakovan prečrtani blok)")
    for n in (1503, 1504, 1505):
        if str(n) in geo_pref:
            fail(f"I2 karta IMA poligon {n} (pričakovano brez)")
    for n in range(1681, 1701):
        if str(n) in geo_pref:
            fail(f"I2 karta IMA poligon {n} (pričakovano brez)")
    if any(str(n) in geo_exact for n in range(1121, 1201)):
        fail("I2 karta ima točne poligone v 1121–1200 (pričakovano prazno)")
    if sum(1 for n in range(1461, 1501) if str(n) in geo_exact) < 10:
        fail("I2 karta 1461–1500 < 10 točnih poligonov (pričakovana gostota)")

    # ————— I3/A: kolizije renumerifikacije + lažna geometrija p87 —————
    old_nums = {m["old"] for m in RENUM}
    new_nums = {m["new"] for m in RENUM}
    for n in ("1503", "1504", "1505", "1904"):
        if n in all_bases:
            fail(f"I3 {n} že obstaja v v2 (kolizija renumerifikacije)")
    for n in map(str, range(1681, 1701)):
        if n in all_bases:
            fail(f"I3 {n} že obstaja v v2 (kolizija renumerifikacije)")
    for b in ("1903", "1905"):
        pgs = sorted({r["page"] for r in rows_by_base[b]})
        if pgs != [98]:
            fail(f"I3 {b} strani {pgs} ≠ [98] (pričakovano samo p98)")
    # lažna geometrija: p87 vrstice == p36 koordinate (ista številka)
    coord36 = {r["base"]: (r["lat"], r["lng"]) for r in rows if r["page"] == 36}
    fake_geo = 0
    for r in rows:
        if r["page"] == 87 and r["base"] in coord36:
            if (r["lat"], r["lng"]) == coord36[r["base"]]:
                fake_geo += 1
    if fake_geo != 11:
        fail(f"I3 lažna geometrija p87: {fake_geo} ≠ 11 vrstic")
    # 1901–1920 pod III (p98) in IV (p93): disjunktni lastniki
    o98 = {r["owner"] for r in rows_by_page[98]}
    o93 = {r["owner"] for r in rows if r["page"] == 93}
    if o98 & o93:
        fail("I3 p98 (III) in p93 (IV) lastnika nista disjunktna")

    # ————— I4/B: sosledje flagi —————
    # repliciraj P65 sosledje za 5 flag base (±1 sosed znotraj strani)
    # P68: sosledje replikacija nad v3 base (v2 vrstice + RENUM preslikave)
    renum_map = {(m["page"], m["old"]): m["new"] for m in RENUM}
    v3_base_of = lambda r: renum_map.get((r["page"], r["base"]), r["base"])
    v3_seq_by_page = {pg: [renum_map.get((pg, x["base"]), x["base"]) for x in rr]
                      for pg, rr in rows_by_page.items()}

    def sosled_repl(b):
        ok = flag = 0
        flagged = []
        for r in rows:
            if v3_base_of(r) != b:
                continue
            seq = v3_seq_by_page[r["page"]]
            ks = [k for k, bb in enumerate(seq) if bb == b]
            for k in ks:
                pb = seq[k - 1] if k > 0 else None
                nb = seq[k + 1] if k + 1 < len(seq) else None
                near = (pb is not None and abs(int(pb) - int(b)) == 1) or \
                       (nb is not None and abs(int(nb) - int(b)) == 1)
                if near:
                    ok += 1
                else:
                    flag += 1
                    flagged.append(f"{b}@p{r['page']}")
        return ok, flag, flagged

    sos_out = {}
    tot_flag_rows = 0
    for b in FLAG_BASES:
        o, f, fl = sosled_repl(b)
        e65 = p65_bases[b]["sosledje"]
        if {"ok": o, "flag": f, "flaggedRows": sorted(fl)} != \
           {"ok": e65["ok"], "flag": e65["flag"],
            "flaggedRows": sorted(e65["flaggedRows"])}:
            fail(f"I4 sosledje {b} ne seže P65 runtime bajtno")
        tot_flag_rows += f
        sos_out[b] = {"ok": o, "flag": f, "flaggedRows": sorted(fl)}
    if tot_flag_rows != FLAG_ROWS:
        fail(f"I4 flag vrstic {tot_flag_rows} ≠ {FLAG_ROWS}")
    # M per flagged row: P38 page numbers − v2 page numbers; vsi brez poligona
    # vir per stran = PS-full-v2 izbira (pass1/pass2, pass3→pass1 — p55
    # replikacija), da je M izračunan nad ISTIM virom kot v2 vrstice
    selv2 = json.load(open(SELFV2))

    def page_source(pg):
        e = selv2["pages"].get(str(pg)) or selv2["pages"].get(pg)
        pas = e["pass"] if isinstance(e, dict) else e
        if pas == "pass2":
            return f"ps-{pg:03d}-pass2.json"
        return f"ps-{pg:03d}.json"  # pass1 (pass3 → pass1, p55 lekcija)

    flag_pages = sorted({int(fr.split("@p")[1])
                         for b in FLAG_BASES
                         for fr in sos_out[b]["flaggedRows"]})
    p38_files = {pg: page_source(pg) for pg in flag_pages}
    p38_page_nums = {pg: raw_nums(f) for pg, f in p38_files.items()}
    v2_page_nums = {pg: sorted({r["parzella"] for r in rs})
                    for pg, rs in rows_by_page.items()}
    flags_out = []
    for b in FLAG_BASES:
        for fr in sos_out[b]["flaggedRows"]:
            page = int(fr.split("@p")[1])
            m = sorted((n for n in p38_page_nums[page]
                        if n not in v2_page_nums[page] and n.isdigit()),
                       key=int)
            if not m:
                fail(f"I4 {fr}: M prazna (pričakovani manjkajoči sosedje)")
            for n in m:
                if n in geo_pref:
                    fail(f"I4 {fr}: M vsebuje {n} s poligonom (pričakovano brez)")
            # sosedje ±1 v registru (P38) — dokaz z imenom
            nb = [n for n in (str(int(b) - 1), str(int(b) + 1))
                  if n in p38_page_nums[page]]
            flags_out.append({
                "flag": fr, "missingInV2": m,
                "registerNeighbors": nb,
                "neighborEvidence": {n: raw_row(p38_files[page], n)
                                     for n in nb},
                "pageStart": rows_by_base[b][0]["page"] == page and
                             min(int(x["parzella"]) for x in rows_by_page[page]
                                 if x["base"] == b) ==
                             min(int(x["parzella"]) for x in rows_by_page[page]),
            })
    # meja strani: 1820 (p63) in 2140 (p109) imata poligon in sta v v2
    for n, pg in (("1820", 63), ("2140", 109)):
        if n not in geo_pref or n not in {r["base"] for r in rows_by_page[pg]}:
            fail(f"I4 {n} (p{pg}) pričakovan v v2 s poligonom (meja strani)")

    # ————— I5/C: R1↔R2 —————
    # 671: II instanca @p87 je po renumerifikaciji 1691 → ni divergencia
    # 671 RAZREŠENA (P67 part C; P68 utemeljitev: II instanca @p87 = 1691):
    # po P68 v3 je 671 single-Blatt (p36) → IZPADLA iz P65 bases (dvoumnost)
    if "671" in p65_bases:
        fail("I5 671 še v P65 bases (po P68 pričakovano single-Blatt)")
    p36_671 = [r for r in rows_by_base["671"] if r["page"] == 36]
    p87_671 = [r for r in rows_by_base["671"] if r["page"] == 87]
    if len(p36_671) != 1 or len(p87_671) != 1:
        fail("I5 671@v2: pričakovani instanci p36 + p87")
    v3_1691 = [r for r in rows if v3_base_of(r) == "1691" and r["page"] == 87]
    if len(v3_1691) != 1:
        fail("I5 1691@p87: preslikava 671→1691 manjka (P68)")
    # moda B pas članstvo (razmerje iz v2, I6: v izpis samo bool)
    def mode_b(r):
        qk, am = r.get("areaQK"), r.get("areaModern")
        if not qk or am is None:
            return False
        return 0.8 <= am / qk <= 1.25
    e930 = p65_bases["930"]
    if e930["status"] != "R1" or e930["attributedBlatt"] != "II":
        fail("I5 930 P65 status/atribucija != R1/II")
    r49 = [r for r in rows_by_base["930"] if r["page"] == 49][0]
    r99 = [r for r in rows_by_base["930"] if r["page"] == 99][0]
    if not mode_b(r49) or mode_b(r99):
        fail("I5 930 moda B pas: pričakovano ✓@p49 ✗@p99")
    o49 = {r["owner"] for r in rows_by_page[49]}
    o99 = {r["owner"] for r in rows_by_page[99]}
    if r49["owner"] in o99 or r99["owner"] in o49:
        pass  # lastnika 930: disjunktnost na nivoju base
    o930 = {r["owner"] for r in rows_by_base["930"]}
    if len(o930) != 2:
        fail("I5 930: pričakovana 2 lastnika")
    # sosedi ±1 za 930 na obeh straneh
    for pg in (49, 99):
        nums = {int(r["parzella"]) for r in rows_by_page[pg]}
        if not ({929, 931} & nums):
            fail(f"I5 930: brez sosedov ±1 na p{pg}")

    # ————— I6/D: univerzalna disjunktnost —————
    def blatt_of(page):
        b = page_attr.get(str(page), {}).get("blatt")
        if not b:
            fail(f"I6 stran {page} brez atribucije Blatta")
        return b

    def owners_by_blatt(b):
        d = defaultdict(set)
        for r in rows:
            if v3_base_of(r) == b:
                d[blatt_of(r["page"])].add(r["owner"])
        return {k: sorted(v) for k, v in sorted(d.items())}

    def relation(ob):
        if any(not v for v in ob.values()):
            return "open"
        sets = [set(v) for v in ob.values()]
        if len(sets) < 2:
            return "single-Blatt"
        disj = all(sets[i].isdisjoint(sets[j])
                   for i in range(len(sets))
                   for j in range(i + 1, len(sets)))
        if disj:
            return "disjoint"
        if all(sets[0] == s for s in sets[1:]):
            return "equal"
        return "overlap"

    rel_dist = Counter()
    per_base = {}
    trans_pages_used = 0
    for b in sorted(cross_65, key=int):
        ob = owners_by_blatt(b)
        if any("·" in k for k in ob):
            trans_pages_used += 1
        rel = relation(ob)
        rel_dist[rel] += 1
        per_base[b] = {"ownerRelation": rel,
                       "uniqueOwners": len({o for v in ob.values()
                                             for o in v})}
    if rel_dist["disjoint"] != EXPECTED_CROSS:
        fail(f"I6 disjunktnih {rel_dist['disjoint']} ≠ {EXPECTED_CROSS}")
    if rel_dist["overlap"] or rel_dist["equal"] or rel_dist["open"]:
        fail(f"I6 nepričakovane relacije: {dict(rel_dist)}")
    if trans_pages_used:
        fail(f"I6 {trans_pages_used} base na prehodnih straneh ('·')")
    # 39 split == P66 bajtno (ownersByBlatt + ownerRelation)
    for b, e66 in p66["bases"].items():
        ob = owners_by_blatt(b)
        if ob != e66["ownersByBlatt"] or relation(ob) != e66["ownerRelation"]:
            fail(f"I6 {b}: P66 polja (ownersByBlatt/ownerRelation) odmikajo")
    # brez georef polj v izpisih
    def assert_no_geo(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in GEO_FIELDS:
                    fail(f"I6 georef polje '{k}' v izpisu ({path})")
                assert_no_geo(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                assert_no_geo(v, f"{path}[{i}]")

    # ————— projekcija (številčenjski nivo) — ZAMENJANA s P68 MERITVAMI —————
    # P67 aproksimacija [~] (bases 802 / multi 208 / cross 107) je bila
    # izračunana pred P68; P68 pipeline je MERIL dejanske vrednosti nad v3:
    bases_after = 798   # P68 (aproksimacija 802: ni štela izpada 1503–1505/1681–1700)
    multi_after = 199   # P68 (aproksimacija 208: ni štela 9 preostalih 661–680 cross)
    cross_after = 98    # P68 (aproksimacija 107; P68 blattDist I·II 31 / II·III 46 / III·IV 3 / IV·V 18)
    # 1903: III 2438 QK vs IV 1005 → delež 0.7081 < 0.75 → pas split [~]
    sh1903 = round(2438 / (2438 + 1005), 4)
    if abs(sh1903 - 0.7081) > 1e-9:
        fail(f"I3 delež 1903 III {sh1903} ≠ 0.7081")

    # ————— izpisi —————
    status_line = (
        f"P67 FORENZIKA: skok II·IV = artifakt dvojne Kurrent zamenjave "
        f"(p78 1501–1520, p93 1901–1920, p87 1681–1700 — oči+strip 2×+karta; "
        f"renumerifikacija 17 preslikav); 5 sosledje flagov = obseg joina "
        f"(11/11 razloženih; sosedje brez poligonov; meja strani); 671 ni "
        f"divergenca (II instanca = 1691), 930 [~] z dokazom; disjunktnost "
        f"lastnikov per Blatt UNIVERZALNA 110/110; v2 nespremenjen; "
        f"renumerifikacija = P68"
    )
    verdict_si = (
        "P67: FORENZIČNI PAKET ANOMALIJ (issue #13) — štiri merjena dela, "
        "deterministično, brez AI ob delovanju; v2 join NESPREMENJEN "
        "(disciplina P56–P66). (A) SKOK II·IV (1603/1604) = ARTIFAKT "
        "DVOJNE KURRENT ZAMENJAVE: p78 (Blatt II, Wüstung 'Pod Grabino') "
        "prave številke 1501–1520 (strip 2× bajtno, vrstice 5–14 rdeče "
        "prečrtane, kontinuiteta 1461–1480→1481–1500→1501–1520, karta: "
        "1461–1500 ima 12 poligonov / 1121–1200 PRAZNO), v2 1603–1605 = "
        "P38 napaka 5→6 → prave 1503/1504/1505; p93 (Blatt IV) prave "
        "1901–1920 (strip 2× r11–20 bajtno, oči r1–8 = 1901–1908 z rdečimi "
        "prečrtami 1901–1904/1906–1907, karta: blok 1901–1907 ima TOČNO 7 "
        "poligonov), P38 pass1 = 9→0 (1001–1020), pass2 = 9→6 (1601–1620) "
        "→ prave 1903/1904/1905; p87 (Blatt II) prave 1681–1700 (pass2 + "
        "oči r1–8 = 1681–1688; pass1 661–680 = izguba vodilne 1 + 8→6; "
        "strip 161–180 = odrezane vodilne) → 11 v2 vrstic napačno "
        "(+1020) in nosi LAŽNO geometrijo (poligoni 661–680 = Blatt I "
        "p36 instance, koordinate bajtno identične). Posledica: 1603/1604 "
        "= lažni fuziji II 1503/1504 × IV 1903/1904 — skok II·IV IZGINE; "
        "1605 = fuzija II 1505 (prečrtan) × IV 1905; 661/671 = lažni "
        "fuziji I × II 1681/1691 — čez-Blatt primera RAZPADETA; p93 (IV) "
        "in p98 (III) nosita ISTI obseg 1901–1920 (disjunktni lastniki — "
        "per-Blatt primež); karta: 1903/1904/1905 poligoni obstajajo "
        "(jugozahodna lokacija), 1503–1505 in 1681–1700 NE; 16xx poligoni "
        "na tretji lokaciji (v2 jih je lažno pripisal fuzijam). "
        "RENUMERIFIKACIJA 17 preslikav (p78 3×, p93 3×, p87 11×; 0 "
        "kolizij) = P68; projekcija: base 800→802, multi-page 211→208, "
        "čez-Blatt 110→107 (1903 pas split 0.7081 [~], 1905 R2b [~]), "
        "runtime −14 vrstic brez geometrije. (B) 5 SOSLEDJE FLAGOV (646, "
        "661, 1821, 2141, 2143; 11 vrstic) = ARTEFAKT OBSEGA JOINA: "
        "manjkajoči sosedje obstajajo v registru (P38 z imeni: 645 "
        "'Ulrich Franz', 647 'Gemeinde', 662 'Mülley Franzl', 1822 "
        "'Büller Lorenz', 1823 'Gavčnik Miha', 1824 'Gavčnik Gregor', "
        "2142 'Häupler Martin', 2144–2147 …), a brez poligonov v karti → "
        "izpad iz v2 (38.6 % pokritost); 1821/2141/661 so začetki strani "
        "(1820/2140 imata poligona — na prejšnji strani, per-page kontrola "
        "je ne vidi); 11/11 razloženih, 0 anomalij registra. (C) R1↔R2: "
        "671 RAZREŠENA (ni divergencia — II instanca @p87 = 1691, druga "
        "parcela; 671 ostane I-only); 930 ostaja [~] z merjenim dokazom "
        "(moda B pas ✓@p49 ✗@p99, disjunktna lastnika, sosedi ±1 na "
        "obeh straneh, karta 921–940: 9 poligonov). (D) UNIVERZALNA "
        "DISJUNKTNOST: lastniki per Blatt DISJUNKTNI za VSEH 110 "
        "čez-Blatt base (110/110; 39 split == P66 bajtno, 71 "
        "atributiranih 71/71) → per-Blatt številčenje: ista številka pod "
        "različnima Blattoma = 2 RAZLIČNI realni parceli; atribucija "
        "(R1/R2a/R2b) je dodelitev geometrije instanci, ne identiteta "
        "parcele [~]. Strojna forenzika ni dokazni vir; odločitev o "
        "renumerifikaciji in SPLIT joinu = LASTNIKA (P68/P69)."
    )
    verdict_en = (
        "P67: ANOMALY FORENSICS PACK (issue #13) — four measured parts, "
        "deterministic, no AI at runtime; v2 join UNCHANGED (P56–P66 "
        "discipline). (A) THE II·IV SKIP (1603/1604) = A DOUBLE KURRENT "
        "SUBSTITUTION ARTIFACT: p78 (Blatt II, Wüstung 'Pod Grabino') "
        "true numbers 1501–1520 (strip 2 passes byte-exact, rows 5–14 "
        "red-crossed, continuity 1461–1480→1481–1500→1501–1520, map: "
        "1461–1500 has 12 polygons / 1121–1200 EMPTY), v2 1603–1605 = "
        "P38 error 5→6 → true 1503/1504/1505; p93 (Blatt IV) true "
        "1901–1920 (strip 2 passes r11–20 byte-exact, eyes r1–8 = "
        "1901–1908 with red crossings 1901–1904/1906–1907, map: block "
        "1901–1907 has EXACTLY 7 polygons), P38 pass1 = 9→0 (1001–1020), "
        "pass2 = 9→6 (1601–1620) → true 1903/1904/1905; p87 (Blatt II) "
        "true 1681–1700 (pass2 + eyes r1–8 = 1681–1688; pass1 661–680 = "
        "lost leading 1 + 8→6; strip 161–180 = clipped leading digits) "
        "→ 11 v2 rows wrong (+1020) carrying FALSE geometry (the 661–680 "
        "polygons belong to the Blatt I p36 instances — coordinates "
        "byte-identical). Consequences: 1603/1604 = false fusions of II "
        "1503/1504 × IV 1903/1904 — the II·IV skip DISSOLVES; 1605 = "
        "fusion of II 1505 (crossed) × IV 1905; 661/671 = false fusions "
        "I × II 1681/1691 — the cross-Blatt pairs COLLAPSE; p93 (IV) and "
        "p98 (III) carry the SAME range 1901–1920 (disjoint owners — a "
        "textbook per-Blatt overlap); map: 1903/1904/1905 polygons exist "
        "(south-west location), 1503–1505 and 1681–1700 do NOT; the 16xx "
        "polygons sit at a third location (falsely assigned to the "
        "fusions by v2). RENUMBERING 17 mappings (p78 3×, p93 3×, p87 "
        "11×; 0 collisions) = P68; projection: bases 800→802, multi-page "
        "211→208, cross-Blatt 110→107 (1903 split band 0.7081 [~], 1905 "
        "R2b [~]), runtime −14 geometry-less rows. (B) THE 5 ADJACENCY "
        "FLAGS (646, 661, 1821, 2141, 2143; 11 rows) = A JOIN-SCOPE "
        "ARTIFACT: the missing neighbours exist in the register (P38 "
        "with names: 645 'Ulrich Franz', 647 'Gemeinde', 662 'Mülley "
        "Franzl', 1822 'Büller Lorenz', 1823 'Gavčnik Miha', 1824 "
        "'Gavčnik Gregor', 2142 'Häupler Martin', 2144–2147 …) but have "
        "no polygons in the map → dropped from v2 (38.6 % coverage); "
        "1821/2141/661 are page-start rows (1820/2140 HAVE polygons — on "
        "the previous page, invisible to the per-page check); 11/11 "
        "explained, 0 register anomalies. (C) R1↔R2: 671 RESOLVED (not a "
        "divergence — the II instance @p87 = 1691, a different parcel; "
        "671 stays I-only); 930 remains [~] with measured evidence (mode "
        "B band ✓@p49 ✗@p99, disjoint owners, ±1 neighbours on both "
        "pages, map 921–940: 9 polygons). (D) UNIVERSAL DISJOINTNESS: "
        "owners per Blatt DISJOINT for ALL 110 cross-Blatt bases "
        "(110/110; the 39 split byte-equal P66, the 71 attributed 71/71) "
        "→ per-Blatt numbering: the same number under different Blatts "
        "= 2 DIFFERENT real parcels; the attribution (R1/R2a/R2b) is a "
        "geometry-to-instance assignment, not parcel identity [~]. "
        "Machine forensics is not a source of proof; the renumbering and "
        "SPLIT join decisions belong to the OWNER (P68/P69)."
    )

    part_a = {
        "fusedBases": fused,
        "stripEvidence": {
            "p78": {"reads": ["blatt-78.json", "blatt-78-pass2.json"],
                    "numbers": "1501–1520 (2× bajtno)",
                    "crossed": "vrstice 5–14 (1505–1514) rdeče",
                    "bezeichnung": "Wüstung Pod Grabino"},
            "p93": {"reads": ["blatt-93.json"],
                    "numbers": "1901–1920 (r11–20 bajtno; r1–10 garbled)",
                    "crossed": "1901–1904, 1906–1907 (oči)",
                    "p38pass1": "1001–1020 (9→0)",
                    "p38pass2": "1601–1620 (9→6)"},
            "p87": {"reads": ["ps-087-pass2.json"],
                    "numbers": "1681–1700 (oči r1–8 = 1681–1688)",
                    "p38pass1": "661–680 (izguba vodilne 1 + 8→6)",
                    "strip": "161–180 (odrezane vodilne)"},
            "p77": {"reads": ["blatt-77.json"], "numbers": "1481–1500"},
        },
        "mapWitness": {
            "present": {"1901–1907": 7, "1903": True, "1904": True,
                        "1905": True, "1461–1500": "≥10"},
            "absent": ["1503", "1504", "1505", "1681–1700", "1121–1200"],
            "note": "16xx poligoni (1603, 1604/1-3, 1605) na tretji lokaciji "
                    "(v2 lažna dodelitev fuzijam); 19xx ~1.6 km JugZ",
        },
        "renumberSpec": RENUM,
        "collisions": "0 (1503–1505, 1904, 1681–1700 proste; 1903/1905 samo p98)",
        "p93p98Overlap": {"range": "1901–1920", "p93": "IV",
                          "p98": "III", "owners": "disjunktni"},
        "falseGeometry": {"p87Rows": 11,
                          "note": "koordinate bajtno == p36 (isti poligoni "
                                  "661–680 = Blatt I parcele)"},
        "projection": {
            "bases": {"before": EXPECTED_BASES, "after": bases_after},
            "multiPage": {"before": EXPECTED_MULTI, "after": multi_after},
            "crossBlatt": {"before": EXPECTED_CROSS, "after": cross_after},
            "r3Single": EXPECTED_R3,
            "new1903": {"shareIII": sh1903, "class": "split pas [~]"},
            "new1905": {"class": "R2b areaIncomplete [~]"},
            "runtimeRows": "-14 brez geometrije (3× p78, 11× p87); p93 3× "
                           "re-claim (1904 čisto, 1903/1905 konflikt z "
                           "III@p98 [~])",
            "note": "razvrstitev novih base = izhod P68 pipeline [~]",
        },
    }
    part_b = {
        "flagBases": FLAG_BASES,
        "flagRows": tot_flag_rows,
        "perBase": sos_out,
        "details": flags_out,
        "pageBoundary": {"1820": "p63, poligon ✓, v v2 ✓",
                         "2140": "p109, poligon ✓, v v2 ✓",
                         "note": "začetki strani 1821/2141/661 — per-page "
                                 "kontrola ne vidi prejšnje strani"},
        "verdict": "11/11 razloženih (obseg joina + meja strani); 0 "
                   "anomalij registra; sosledje ostaja merilo kakovosti, "
                   "ne napake",
    }
    part_c = {
        "671": {"verdict": "RAZREŠENA — ni divergencia (P68 IZVEDENA)",
                "reason": "II instanca @p87 = 1691 (renumerifikacija p87 — "
                          "P68 preslikava); 671 ostane I-only @p36 "
                          "(single-Blatt, izpadla iz P65 dvoumnosti)",
                "p68": {"new": "1691", "old": "671", "page": 87}},
        "930": {"verdict": "ostaja [~] z merjenim dokazom",
                "p65": {"status": e930["status"],
                        "attributedBlatt": e930["attributedBlatt"]},
                "modeB": {"p49": True, "p99": False},
                "owners": sorted(o930),
                "ownersDisjoint": True,
                "neighborsBothPages": {"p49": True, "p99": True},
                "mapBlock": "921–940: 9 poligonov (mehka podpora)"},
    }
    part_d = {
        "crossBlattBases": EXPECTED_CROSS,
        "ownerRelationDist": {k: rel_dist[k] for k in sorted(rel_dist)},
        "disjoint": rel_dist["disjoint"],
        "splitSubset": {"count": EXPECTED_SPLIT,
                        "note": "39 polj bajtno == P66 (ownersByBlatt + "
                                "ownerRelation)"},
        "attributedSubset": {"count": EXPECTED_CROSS - EXPECTED_SPLIT,
                             "disjoint": EXPECTED_CROSS - EXPECTED_SPLIT},
        "verdict": "per-Blatt številčenje: ista številka pod različnima "
                   "Blattoma = 2 RAZLIČNI realni parceli; atribucija = "
                   "dodelitev geometrije instanci [~]",
    }

    runtime = {
        "version": 1,
        "task": "P67 — forenzični paket anomalij: skok II·IV, sosledje "
                "flagi, R1↔R2 divergence, univerzalna disjunktnost",
        "date": "2026-10-14",
        "generatedBy": "scripts/p67_ps_anomaly_forensics.py",
        "rule": {
            "sosledje": "±1 sosed znotraj v2 vrstic iste strani (P65 "
                        "replikacija); flag = brez soseda",
            "ownersByBlatt": "v2 vrstice × P59 pageAttribution; relacija "
                             "disjoint|equal|overlap|open (P66 metoda)",
            "modeB": "razmerje areaModern/areaQK ∈ [0.8, 1.25] (P60/P61) — "
                     "v izpis samo članstvo (I6)",
            "renumber": "17 preslikav (p78 160x→150x, p93 160x→190x, p87 "
                        "+1020) — SPECIFIKACIJA za P68, v2 nespremenjen",
        },
        "summary": {
            "renumberMappings": len(RENUM),
            "collisions": 0,
            "fusedBasesResolved": ["1603", "1604", "1605", "661", "671"],
            "flagRowsExplained": FLAG_ROWS,
            "flagRowsTotal": FLAG_ROWS,
            "crossBlattBases": EXPECTED_CROSS,
            "ownerDisjoint": EXPECTED_CROSS,
            "ownerRelationDist": {"disjoint": EXPECTED_CROSS},
            "divergences": {"671": "razrešena (ni divergencia)",
                            "930": "[~] z merjenim dokazom"},
            "projection": {"bases": bases_after,
                           "multiPage": multi_after,
                           "crossBlatt": cross_after,
                           "r3Single": EXPECTED_R3},
        },
        "parts": {"A": part_a, "B": part_b, "C": part_c, "D": part_d},
        "statusLine": status_line,
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "next": [
            "P68 — v3 sanacija številčenja: 17 preslikav (p78/p93/p87) + "
            "re-join (1903/1904/1905 poligoni, konflikt III@p98 vs IV@p93 "
            "[~]) + veriga re-run P59–P66 s posodobljenimi pini",
            "SPLIT joina (lastniška odločitev, zdaj nad popravljeno "
            "številčenje — 1603/1604/661 izpadajo, 1903/1905 nastopata)",
            "sistemski pregled preostalih P38 pass1 slojev (p74/p76/p77 "
            "1121–1200 brez kartnih poligonov [~]; p88 721–740)",
            "930: dokončna atribucija (PF protokol / lastniška odločitev)",
            "lastniki atributiranih instanc ↔ PF protokol (ostaja iz P65)",
        ],
    }

    ev = {
        "task": runtime["task"],
        "date": runtime["date"],
        "principle": (
            "forenzični paket anomalij (kandidati P66 next #3/#4 + P64/P65 "
            "divergenci + nova univerzalna meritev): 4 dela (A skok II·IV "
            "= artifakt dvojne Kurrent zamenjave s renumerifikacijsko "
            "specifikacijo; B sosledje flagi = obseg joina; C R1↔R2 — "
            "671 razrešena, 930 [~]; D univerzalna disjunktnost 110/110); "
            "deterministično, brez AI ob delovanju; v2 nespremanjen; "
            "odločitev o renumerifikaciji = lastnika (P68)"
        ),
        "inputs": {
            "v2": "research/issue17/ps-parcels-geo-v2.json (rowsEvidence 1093)",
            "p59": "research/issue17/ps-blatt-headers.json (pageAttribution)",
            "p65rt": "src/data/atlas/ps-attribution-full.json (211)",
            "p66rt": "src/data/atlas/ps-split-pack.json (39)",
            "topo": "research/issue17/ps-register-topology.json (pageMap)",
            "geo": "research/georef-n83/gurs/parcels-ko1544-merged.json "
                   "(2117 poligonov KO 1544)",
            "p38raw": "research/issue17/ps-raw/ps-*.json (dokazi sosedov + "
                      "sloji napak)",
            "strip": "research/issue17/ps-raw/blatt-*.json (strip branja)",
        },
        "inputSha256": PINS,
        "invariants": [
            "I1 vhodni pini (27× sha256 + števci 1093/800/211/39/110/101)",
            "I2/A dokazi p78/p93/p87 (strip 2× bajtno; arbitražni nizi; "
            "karta 1901–1907 ✓ / 1503–1505, 1681–1700, 1121–1200 ∅ / "
            "1461–1500 ≥ 10)",
            "I3/A kolizije renumerifikacije (0) + lažna geometrija p87 "
            "(11 vrstic == p36 koordinate)",
            "I4/B flagi == P65 bajtno (5 base, 11 vrstic); M ne-prazna ∧ "
            "vsi M brez poligona; 1820/2140 v v2 (meja strani)",
            "I5/C 671 R1/I + 930 R1/II + moda B pas ✓@p49 ✗@p99 + "
            "disjunktna lastnika + sosedi ±1 obeh strani",
            "I6/D 110/110 disjoint; 39 split == P66 bajtno; 0 prehodnih "
            "strani; brez lat/lng/areaModern/ratio v izpisu",
            "I7 dokaz ⊇ runtime (bajtno podmnožica)",
            "I8 determinizem (--check bajtno)",
        ],
        "parts": {"A": part_a, "B": part_b, "C": part_c, "D": part_d},
        "statusLine": status_line,
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "next": runtime["next"],
        "runtime": runtime,
    }

    assert_no_geo(runtime, "runtime")

    with open(OUT_EV, "w") as f:
        json.dump(ev, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    rt_only = {k: v for k, v in runtime.items()}
    with open(OUT_RT, "w") as f:
        json.dump(rt_only, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    ev_check = json.load(open(OUT_EV))
    rt_bytes = open(OUT_RT, "rb").read()
    if json.dumps(ev_check["runtime"], indent=1, ensure_ascii=False,
                  sort_keys=True).encode() + b"\n" != rt_bytes:
        fail("I7 runtime ni bajtno podmnožica dokaza")

    print(f"OK: A renumerifikacija {len(RENUM)} preslikav, 0 kolizij; "
          f"lažna geometrija p87 {fake_geo}/11")
    print(f"OK: B flagi {tot_flag_rows}/11 razloženih (obseg joina + meja)")
    print(f"OK: C 671 razrešena (1691), 930 [~] z dokazom")
    print(f"OK: D disjunktnost {rel_dist['disjoint']}/{EXPECTED_CROSS} "
          f"(univerzalna); 39 split == P66 bajtno")
    print(f"OK: projekcija base {bases_after}, multi {multi_after}, "
          f"čez-Blatt {cross_after}")
    print(f"OK: dokaz {OUT_EV}, runtime {OUT_RT}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        h1 = sha256(OUT_EV)
        h2 = sha256(OUT_RT)
        main()
        if sha256(OUT_EV) != h1 or sha256(OUT_RT) != h2:
            fail("I8 determinizem: izhod se je spremenil")
        print("I8 --check: PASS")
    else:
        main()
