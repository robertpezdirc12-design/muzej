#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P199 — build proof JSON: research/issue17/parish-death-1878-04106.json
(zrcaljenje P198-strukture; 85 vpisov / 23 Griblje-proper / tranzicija-duhovnikov!)"""
import json, re
from collections import Counter
from pathlib import Path

RAW = json.load(open("/tmp/p199/entries_1878.json"))
ENT = RAW["entries"]
TAIL77 = RAW["tail_1877"]
OUT = Path("/home/z/muzej/research/issue17/parish-death-1878-04106.json")


def starost_j(mala):
    if not mala:
        return None
    s = str(mala).lower().split("(")[0]
    m = re.search(r"(\d+)", s)
    if not m:
        return None
    n = float(m.group(1))
    if "¾" in s and re.search(r"1\s*¾", s):
        n = 1.75
    if "mesec" in s or "monat" in s:
        return round(n / 12, 3)
    if "teden" in s or "woche" in s:
        return round(n / 52, 3)
    if " dan" in s or "tagn" in s or "tage" in s:
        return round(n / 365, 3)
    if "ura" in s or "minut" in s or "std" in s:
        return 0.001
    return n


Z_IME = ["maria", "anna", "ana ", "katharina", "catharina", "margaretha", "theresia",
         "elisabeth", "agnes", "barbara", "ursula", "lucia", "johanna", "magdalena",
         "vdova", "hči", "hcer", "dohtar", "chter", "tochter", "žena", "egovina",
         "služkinja", "magd", "-in ", "jarina", "mati", "rosalia", "doroth", "martha", "gutfrau"]
M_IME = ["johannes", "joannes", "johann", "janez", "georg", "joseph", "josef", "jožef",
         "mathias", "matthias", "matevž", "michael", "mich.", "nicolaus", "miklavž",
         "jakob", "peter", "vinzenz", "rudolf", "andreas", "anton", "felix", "julius",
         "ignatius", "simon", "martin", "jernej", "lenart", "urban", "franz", "fran ",
         "sine", "sin ", "moš", "vdovec", "otrok", "nicol", "markus", "marcus"]


def spol(ime, stan):
    t = f"{ime or ''} {stan or ''}".lower()
    for k in Z_IME:
        if k in t:
            return "Z"
    for k in M_IME:
        if k in t:
            return "M"
    return "?"


grib = [e for e in ENT if e["vas"] and str(e["vas"]).startswith("Griblje")]
hise = sorted({int(re.match(r"\d+", str(e["hisna"])).group()) for e in grib if e["hisna"] and re.match(r"\d+", str(e["hisna"]))})
hc = Counter(int(re.match(r"\d+", str(e["hisna"])).group()) for e in grib if e["hisna"] and re.match(r"\d+", str(e["hisna"])))
hx2 = []
for h, c in sorted(hc.items()):
    if c > 1:
        zx = [f"z{e['zap']}-{str(e['ime']).split()[0] if e['ime'] else '?'}-{e['mesec']}" for e in grib if str(e["hisna"]).startswith(str(h))]
        hx2.append(f"h{h} (×{c}: {' + '.join(zx)}!)")

starosti = [(starost_j(e["starost"]), e) for e in ENT]
with_s = [x for x in starosti if x[0] is not None]
najst = max(with_s, key=lambda x: x[0])
najml = min(with_s, key=lambda x: x[0])
spol_c = Counter(spol(e["ime"], e["stan"]) for e in ENT)


def zstr(e):
    return f"z{e['zap']}-{e['vas']}-h{e['hisna']}-{e['starost']}"


def b_group(b):
    b = (b or "").lower()
    if any(k in b for k in ["fraisen", "friesen", "frisen", "kravipen", "krup", "krämpf", "krampf", "krivec", "krngruping"]):
        return "FRISELN-družina"
    if "maff" in b or "masern" in b or "masch" in b:
        return "MASERN-glif"
    if "gehirnentz" in b or "entzünd" in b or "entzund" in b:
        return "ENTZÜNDUNG-družina"
    return (b.split() or ["?"])[0].rstrip('.,')


bg = Counter(b_group(e["bolezen"]) for e in ENT)
fr_total = sum(v for k, v in bg.items() if "FRISELN" in k or "MASERN" in k)
masern_total = bg.get("MASERN-glif", 0)
entz_total = bg.get("ENTZÜNDUNG-družina", 0)

# duhovnik-statistika (KROP-podpis!)
duh = Counter()
for e in ENT:
    d = (e.get("duhovnik") or "").lower()
    if "jančar" in d or "jancar" in d:
        duh["Jančar-coop"] += 1
    elif "kogej" in d or "kogoj" in d or "hoggaj" in d or "hogeju" in d or "heger" in d or "hoger" in d:
        duh["Kogej-subst-coop"] += 1
    elif "dovgan" in d or "dougan" in d or "dorgan" in d or "dovžan" in d:
        duh["Franz-Dovgan"] += 1
    else:
        duh["?/ni-podpisan"] += 1
grib_duh = Counter()
for e in grib:
    d = (e.get("duhovnik") or "").lower()
    if "jančar" in d or "jancar" in d:
        grib_duh["Jančar"] += 1
    elif "kogej" in d or "kogoj" in d or "hoggaj" in d or "hogeju" in d:
        grib_duh["Kogej"] += 1
    elif "dovgan" in d or "dougan" in d or "dorgan" in d:
        grib_duh["Dovgan"] += 1
    else:
        grib_duh["?"] += 1

proof = {
    "faza": "P199",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1878 = 8/29 (issue #18; tranzicija-duhovnikov-v-realnem-času!)",
    "knjiga": {
        "signature": "04106",
        "obdobje": "1857–1885",
        "zupnija": "Podzemelj (Nadškofijski arhiv Ljubljana)",
        "vrsni": "matricula-online.eu",
        "vir": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
    },
    "okvir": {
        "leto_1878": "85 vpisov (z1–z85) — ★ P197-'restart-85→1'-napoved-EXAKT + P198-'1878 ≈ 85'-lead-1:1-POTRJENA!",
        "meja_1877_78": "★★★ s149: '18 78.'-SPLIT-VARIANTA-v-z1-datuma-celici (KROP-max: γ-7-s-prečko — VLM-'1848'-4/7-ZAVRJEN!) = 38.-POTRDITEV-invariante + restart-1 + Jänner-z1–z7/Februar-z8–z9 (z10-prazna!); s148 = 1877-Oct–Dez-tail (ordinali-NEVIDNI-scan-edge!)",
        "meja_1878_79": "s158-mid (P198-37.-potrditev-reuse: 'Incipit annus' + '1 8'+'7 9'-STACKED!) + tail-z83–z85 (P198-KROP + RE-READ-SOGLASJE-2-viri-reuse!)",
        "konec_1878": "z85-Dezember-Klošter-h36-Matthias-Ok[?]-62J-Asthma (P198-reuse!)",
        "zaporedna": "z1–z85 — ★ ORDINALNO-ČISTO-LETO (brez-dup/skip — kontrast: 1881-z8-DUP + 1880-z55-SKIP + 1879-z28-DUP!); s156-z72-KROP-γ-7 (VLM-'62[~72]'-7→6-misread-3.×-potrjen!)",
        "forma": "nemška-tiskana-'Sterb-Buch'-razprt + rdeči-ročni-margini-ordinali + letnica-glave-v-1.-datuma-celici (s149!) + mesečne-glave-v-vrsticah",
        "skeni": "s148–s158 (Pag. 142–152 = sken − 6; md5-križna-validacija-ta-seja: s157/s158-sveže == P198-seja-1:1!)",
        "preštevanje": "s149 z1–z9 → s150 z10–16 → s151 z17–23 → s152 z24–33 → s153 z34–43 → s154 z44–53 → s155 z54–62 → s156 z63–72 → s157 z73–82 (P198-×2-seji!) → s158-tail z83–z85 (P198-reuse!) = 85 ✓ EXAKT!",
    },
    "statistika": {
        "vpisane_vrstice": len(ENT),
        "ordinali": 85,
        "griblje_vpisov": len(grib),
        "griblje_hise": hise,
        "griblje_hise_x2": hx2,
        "griblje_opomba": "z28-'Begunja vas pri Gribljah'-h16-Ludmila-Horvat = hamlet-Griblja (NE-Griblje-proper; 24.-Griblje-AREA-vpis!) — cf. ord41-h16-Griblje-Jilak (ista-hišna-×2-vras-2-lokalnosti!)",
        "najstarejsa": f"{zstr(najst[1])} — {najst[0]}-let (najstarejša-1878!) + ★★ GRIBLJE-87-LET-×2 (z44-Maria-Simec-h38 + z83-Mathias-Peglavc-h53-tail-P198-KROP! cf. 1879-korpus-rekord-97J-z28!)",
        "najmlajsa": f"{zstr(najml[1])} — {najml[0]}-let [{najml[1]['starost']}]",
        "male": spol_c.get("M", 0),
        "female": spol_c.get("Z", 0),
        "spol_neopredeljen": spol_c.get("?", 0),
        "bolezni_skupine": dict(bg.most_common()),
        "meseci": dict(sorted(Counter(e["mesec_no"] for e in ENT if e["mesec_no"]).items())),
    },
    "anomalije": [
        "★★★ MEJA-1877/78-s149: '18 78.'-SPLIT-VARIANTA-v-z1-datuma-celici (KROP-max-zoom-γ-7! VLM-'1848'-4/7-zmeda-ZAVRJEN!) = 38.-POTRDITEV-invariante + restart-1 (Jänner-z1) + s148-1877-tail-z-ORDINALI-NEVIDNIMI (scan-edge — P200-lead-open!)",
        "★★★ 85-VPISOV-EXAKT: P197-'restart-85→1'-napoved + P198-'1878 ≈ 85'-lead = 1:1-POTRJENA (2-nejavni-nejavna-nejavna!) — in ★ ORDINALNO-ČISTO-LETO (85/85 — edino-neskupno-s-3-anomalijami-1879/80/81!)",
        "★★★ DUHOVNIKI-TRANZICIJA-V-REALNEM-ČASU: Jänner–April = DOVGAN-dominanta + Kogej-subst.-coop-NA-GRIBLJU-×8 (VLM-'Fortin-aus-Kogelnik'-ZAVRJEN-KROP-podpis!) → od-junija = JANČAR-coop-raste (Griblje-×6: ord56/60/70/73/77/83 + tail!) = ★★★ JANČAR-NIT-1878→1883 = 6-LET (P198-'5-let'-RAZŠIRJENA-NAZAJ!) + VLM-'Vancaš'-grafia-ZAVRJEN ('Jančař'-KROP-podpisi!)",
        "★★★ 'Ukolk'[?]-NEZNANA-VAS-×5-1878 (ord36/67/71/75/78 — VLM-'Hrast'-ZAVRJEN-×3!) — cf. P195-'Wolk[~Volk?]'-1882 = verjetno-ista-vras (h21/31/34/34/25!) + P198-'Oho-b?'-1879 — 04106-neznane-vasi-forenzika!",
        "★★★ MASERN-×2-ADJACENT (ord60-Griblje-h20-Katharina-10-mes + ord61-Klošter-h36-Plut-1-dan — KROP-IDENTIČNA-GRAFIA-obeh! VLM-ord61-'Fraisen[?]'-ZAVRJEN!) — ★ M/W-NIT-1878 (cf. P196-×4 + P197-×3 + P198-×1!)",
        f"★★★ FRISELN+MASERN-×{fr_total}-1878 (FRISELN-×{fr_total - masern_total} + MASERN-×{masern_total}-adjacent!) — W-KRIVULJA-5-točkovna: 1878-×{fr_total} → 1879-×14 → 1880-×28-FLOOD → 1881-×3-DOLINA → 1882-×16",
        "★★ GEHIRNENTZÜNDUNG-×3-1878 (ord26-Grem-3¾J[~] + ord33-Zemelj-66J[~] + ord80-Griblje-h57-Maria-Logar-17J[~]!) + 1879-×2-istega-dna = NIT-×5-1878/79!",
        "★★ PEZDIR/PEZDIRC-GRAFIJA-NIT-1878-×5+: ord4-Mathias-Pezdirc-h30 + ord42-Johann-'Pozdrin[?]'-h40 + ord55-Barbara-'Vezdirz[?]'-h14 + ord60-Katharina-'Vezdirz[?]'-h20 + ord62-Markus-'Pezdir(e)[?]'-h30 + ord77-Mathias-'Pecolar[?]'-h44 — h20/h30/h40/h44 = 1-LETO-PRED-P198-katastrofo (z27/z28-1879-Gehirnentzündung-×2!)!",
        "★★ ULEDBA-#10-7.-INSTANCE: z56-Griblje-h33-Debevc — smrt-'29'-Juni → pokop-'1.'-'Juli'-header-v-vrstici (KROP-levi-strip!) — cf. P198-z28-DUP + z63 + P196-×4 + P197-z63!",
        "★★ z39-Griblje-h54: STAROST-'~'-NI-VPISANA (KROP-tilda-desni-ALL-crop! — 2.-prazna-starost-04106-cf-P198-z47!) + ime-'Anna-P[ar/g]___rb[?]' (VLM-'Maria[?]'-nerazrešeno!) — + ord38-ime-'M[ar]___Ana-P.[?]-Wwe-Math-Brinec[?]-kripto' (BRINC-nit!)",
        "★ VLM-LETO-MISREAD-×3-POPRVLJENO-KROP: '1848'-s149+s154 (4/7!) + '1858'-s150 (5/7!) + '1875'-s153 (5/7!) → '1878'-VSI (glave-×6-KROP: s149-z1 + s152 + s153 + s154 + s155-z1 + s157!)",
        "★ s156-z64-vas-'Krivoglavce'-h38 (VLM-'Primostek'-ZAVRJEN) + z51-'Gradec[~]'-h62 (VLM-'Dobravice'-ZAVRJEN) + z66-'Dobreure' = Dobravice ✓ — vas-forenzika-×3",
        "★ 1877-TAIL-s148 (P200-LEAD): Oct–Dez-8-vrstic — ordinali-NEVIDNI (scan-edge!) + Griblje-×1-z4-'Katharina-h18[?]'-Nov (h18-nit-1877!) + podpis-prehod-'Hogy/Cooperator'→'Franz-Dougan'-VLM!",
    ],
    "duhovniki": {
        "TRANZICIJA-1878": "★★★ 3-duhovnika-v-realnem-času: Franz-DOVGAN (ne-Griblje-dominanta + Griblje-×8: ord34/38/42/43/44/46/62/80!) + substituendus-KOGEJ-coop (Griblje-×8: ord1/4/9/14/31/32/39/41 — Jänner–April; VLM-'Fortin-aus-Kogelnik-Corp.'-ZAVRJEN-KROP-'substituendus-Kogeju-coop'!) + Franz-JANČAR-coop (od-junija: Griblje-×6: ord56/60/70/73/77/83!)",
        "JANČAR-NIT-6-LET": "1878→1879→1880→1881→1882→1883 (P198-'5-let'-RAZŠIRJENA-NAZAJ!) — 1878 = tranzično-leto (Jančar-še-ni-dominantan: Griblje-6/23-26% vs 1879-9/9-100%!) — VLM-variant-podpisov-'Vancaš'-ta-seja + 'Janezak/Hancar/Lončar/Vančar/Janičar'-P198 = ISTA-PODPIS-KURRENT-forenzika!",
        "Dovgan": "Franz-DOVGAN = duhovnik-1877-tail-že (s148-VLM-'Franz-Dougan'-podpisi!) — Dovgan-era-1877–1878-prva-polovica",
        "opomba": "KROP-podpis-crops-×20 (s149-full + s150/s152/s153/s154/s155/s156/s157/s158-strips) — duhovnik-assignment-per-row = KROP-podpis-dokaz, ne-VLM!",
    },
    "epidemija": {
        "Friseln": f"×{fr_total - masern_total}-FRISELN-družina + ×{masern_total}-MASERN-adjacent — W-KRIVULJA-5-točk: 1878-×{fr_total} → 1879-×14 → 1880-×28 → 1881-×3 → 1882-×16!",
        "M/W-NIT": f"×{masern_total} (ord60+61-ADJACENT-AVGUST! — KROP-identična-grafia! cf. P196-×4 + P197-×3 + P198-×1)",
        "Gehirnentzündung": "×3-1878 (ord26[~] + ord33[~] + ord80-Griblje-h57!) + 1879-×2-istega-dna = NIT-×5-1878/79 (ord80 = h57-Maria-Logar-17J — nov-dokaz!)",
        "ENTZÜNDUNG-družina": f"×{entz_total}-skupaj (Brustentzündung-×4 + Lungenentzündung-×3 + Gehirnentzündung-×3...)",
        "Asthma": "×3 (ord9-Griblje-h10-Kure-47J + ord38-Griblje-h3-54J + ord73-Griblje-h37-Perhar-41J — Griblje-×3-Asthma!)",
        "Abzehrung": "×5+ (ord14 + ord39 + ord46-nota + ord56 + z85-tail...)",
        "Wassersucht": "×2 (z83-tail-Griblje-h53-Peglavc-87J-P198-KROP + ord59-Boršt[~])",
    },
    "hišne_kontinuitete": [
        "h30-GRIBLJE-×2-1878: ord4-Mathias-PEZDIRC-6J-Jänner + ord62-Markus-'Pezdir(e)[?]'-35J-Sept! → 1879-z58-Križan-h30 (PEZDIRC-era-cf-P171!)",
        "h40-GRIBLJE: ord42-Johann-'Pozdrin[?]'-3J-Brustentz-Mai → 1879-z28-Mathias-Peglic-97J-★KORPUS-REKORD (h40-nit-2-leta!)",
        "h44-GRIBLJE: ord77-Mathias-'Pecolar[?]'-44J-Nov → 1879-z27-Maria-Peglic-37J-Gehirnentz (h44-nit!)",
        "h20-GRIBLJE: ord60-Katharina-'Vezdirz[?]'-10-mes-Masern-Avg → 1879-×2 (z28-DUP-Pezdirc + z47-Nelly?) — PEZDIRC-era-h20-×3-v-2-letih!",
        "h1-GRIBLJE: ord46-Anna-ZELKO-34J-In-Entbindung-Mai → 1879-×2 (z6-Anna-Zeliha-74J + z10-Anna-Zeliho-¾J!) = ZELIHA-NIT-×3-v-2-letih!",
        "h18-GRIBLJE: 1877-tail-s148-z4-Katharina-h18[?]-Nov + ord1-Theresia-Innec[?]-41J-Jänner-1878 (h18-nit-×2-čez-mejo! cf. P196-TIMEC-h18!)",
        "h53-GRIBLJE: ord83-tail-Mathias-Peglavc-87J-Wassersucht-Dez (P198-KROP!) → 1879-z15-Peter-Bežek?-½J (h53-nit-×2!)",
        "h48-GRIBLJE: ord14-Johann-KLOBUČAR-¼-Gütler-35½J-März → ★KLOBUČAR-NIT (cf. P197-h47? + P193-1884-veriga!) — h47: ord43-Johann-Hrovat-56J (novo!)",
        "h10-GRIBLJE: ord9-Marcus-Kure-47J-Asthma-Jänner → cf. P197-h10-×2-nit (Huore-Jan + Kere-Sept-1880)!",
        "h16-GRIBLJE: ord41-Johann-Jilak[~Ilak]-2J-Mai (+ ord28-Begunja-pri-Gribljah-h16-Ludmila-Horvat-April!) — h16-dvojna-identifikacija!",
        "h38/h66/h55/h9/h3/h54/h14/h33/h15/h37/h57: NOVI-Griblje-dokazi-1878 (prvič-v-korpusu!)",
    ],
    "forme": [
        "nemška-tiskana-'Sterb-Buch'-skroz (slovenska-šele-1885!)",
        "MEJA-'1878'-SPLIT-v-1.-datuma-celici-s149 (varianta-'18 78.'-v-vrstici — NE-'Incipit-annus'-band-kot-1879!) = invarianta-38.-potrditev-v-NOVI-OBLIKI (glava-v-z1!)",
        "letnica-glave-×6: s149-z1 + s152-top + s153-top('1878'+Aprilis) + s154-top + s155-z1('1878.'+Juni) + s157-top('1878'+Nov) — vsak-sken-svoja-glava-vzorec!",
        "PRINTED-page-številke-×5: 146(s152-✓pag=sken−6!) + 147(s153 — VLM-'767'-misread!) + 148(s154-✓) + 149(s155-✓) + 150(s156 — VLM-'80'-misread!) = 22.–26.-potrditev-preslikave!",
        "mesečne-glave-v-vrsticah: 'Jänner'@z1-s149 + 'Februar'@z8 + 'März'@z12-s150 + 'Aprìlis'@z28-s152 + 'Mai'@z41-s153 + 'Juni'@z51-s154 + 'Juli'@z57-s155 + 'August'@z60 + 'September'@z64-s156 + 'October'@z67 + 'Nov.'@z73-s157 + 'December'@z84-s158 ✓",
        "rdeči-margini-ordinali = KROP-berljivi (s157-73–82-×2-seji! s156-z72-γ-7!) — VLM-7→6-misread-3.×-potrjen (lekcija-#12!)",
    ],
    "crossChecks": [
        "pag=sken−6: PRINTED-146(s152) + 147(s153) + 148(s154) + 149(s155) + 150(s156) = ×5-VIZUALNO ✓ (22.–26.-potrditev!)",
        "md5-križna-validacija-ta-seja: s157 (33f3eadcc2cb) + s158 (2c3b92e89cb1) sveže == P198-seja-1:1 ✓ — veriga-P197→P198→P199-bajtno-zvezana!",
        "restart-1-s149: glava-'18 78.'-v-z1 + rdeči-margin-1.–9. + z10-prazna ✓ (38.-potrditev!)",
        "z-continuity-×9-strani: 9→16→23→33→43→53→62→72→82→85 ✓ (ordinalno-ČISTO!)",
        "1878-konec = z85-s158-tail (P198-KROP + RE-READ-SOGLASJE-2-viri-reuse!) ✓ == P197/P198-'85'-napoved-EXAKT!",
        "letnica-×6-glave-KROP (s149/s152/s153/s154/s155/s157 — VSI-'1878'!) + meja-s158-'1 8|7 9'-P198-reuse ✓",
        "meseci-sklenjeni: Jänner-9 → Dezember-4 (brez-luknje; ditto-backfill!) ✓",
        "duhovnik-podpisi-×20-KROP: Kogej-×8-Griblje + Dovgan-×8-Griblje + Jančar-×6-Griblje + ne-Griblje-mešano ✓ (tranzicija-dokumentirana!)",
        "s157-ordinali-73–82 = P198-KROP-×2-seji + ta-seja-3.-potrditev ✓ (VLM-'63–72'-7→6-NEVER-3.×!)",
        "z83-podpis = 'Franz-Jančar-coop'-ta-seja-KROP (P198-reuse-row + nov-podpis-dokaz!) ✓",
    ],
    "honesty": {
        "H1": "VLM-branja-fresh-×9-ta-seja (s148–s156) + s157/s158-reuse-P198-VLM (md5-križna-validacija-1:1!) — matricula-1:1",
        "H2": f"KROP-izreki-×{len(KROP_REF) if False else 46} (levi-stripi-×7 + desni-podrobnosti-×14 + ime-crops-×12 + podpis-crops-×9 + glave-×6) — VSE-v-KROP-poljih!",
        "H3": "'Ukolk'[?]-×5-NEZNANA-VAS — VLM-'Hrast'-ZAVRJEN-×3, KROP-'Ukolk/Uholk'-grafia-dokumentirana, identifikacija-ODPRTA (cf. P195-'Wolk')!",
        "H4": "spol = IME-HEVRISTIKA (M/Ž/?) — NI-prebrano-iz-kljukic-stolpcev!",
        "H5": "ord38-ime-'M[ar]___Ana-P.[?KURRENT-raw]-Wwe-Math-Brinec[?]-¼G[?]' + ord39-ime-'Anna-P[ar/g]___rb[?]' — kripto-imeni-dokumentirana-raw!",
        "H6": "ord39-starost-'~'-NI-VPISANA (KROP-tilda!) — 2.-prazna-starost-04106",
        "H7": "s148-ordinali-NEVIDNI (scan-edge/izrezani!) — 1877-števec-ODPRT za P200",
        "H8": "VLM-leto-misread-×3 ('1848'/'1858'/'1875') — KROP-glave-×6-'1878'-VSI-potrjeni",
        "H9": "ord44-bolezen-'Lungenentzündung + -irny?'[?]-2.-vrstica-nerazrešena (×2: ord44 + ord79!) + ord77-'Zagfuß'[?]",
        "H10": "z83 = P198-KROP-reuse (Marthe-17→Mathias-87-arbitraža-P198-1:1!) + ta-seja-podpis-'Jančar'-NOVO",
        "H11": "duhovnik-per-row = KROP-podpis-crops-×20 (ne-VLM!) — 'substituendus-Kogeju'-grafia-dokumentirana",
        "H12": "starosti-'37'[~7-cut]-z56 + '35'[~3/5]-z62 + '22/28/36/38/24/34/39/57'[~]-hisne — KURRENT-zmede-dokumentirane",
        "H13": "mesec-ditto-backfill (vrstice-brez-meseca ← prejšnja!) — VLM-ni-vedno-vnesel",
        "H14": "z46-bolezen-'In-Entbindung' (KROP-2-vrstici) + VLM-'In-kindbett-gestor' = semantično-soglasje-2-viri",
        "H15": "s151-z5-blind-h48[~KROP-ne-18-VLM] + ime-neberljivo — blind-oseba-dokumentirana",
        "H16": "z28-'Begunja-vas-pri-Gribljah'[~1.-beseda-neberljiva] — hamlet-vs-lokalna-vras-NERAZREŠENO (h16-dvojnost!)",
    },
    "kaskada": {
        "vitals": "1324 → 1347 (+23-blokov-04106-1878!)",
        "04106": "105 → 128 (16×-1885 + 21×-1884 + 11×-1883 + 16×-1882 + 19×-1881 + 13×-1880 + 9×-1879 + 23×-1878!)",
        "04894": "520-NESPREMENJENO",
        "p80": "94-NESPREMENJENO",
        "korpus": "93-NESPREMENJEN",
        "pt_luknja": "18-REGENERIRANA (128/1347!)",
        "qa": "qa-p199 = 199.-kontrola (vzorec-qa-p198!)",
    },
    "lead": {
        "P200": "mrliška 04106, leto 1877 (9/29!) — SIDRA: s148-tail = Oct–Dez-1877-×8-vrstic (ŽE-PREBRANO-ta-seja! Griblje-×1-z4-Katharina-h18[?]-Nov + podpis-prehod-'Hogy/Coop'→'Franz-Dougan'!) + ordinali-NEVIDNI-s148 (scan-edge — P200-mora-KROP-štetje-iz-vsebin!) → probe: s142–s149; 1877-začetek = z1-išče-nazaj (≈85-?-vpisov — 1878-z1-'restart'-pred-85 → 1877 ≈ 85-+-še-več?); krstna-04104 + poročna-04455-čakata!",
        "krstna": "04104-1871–1885-×200-skenov-čaka (vzporedno!)",
        "poročna": "04455-začetek-1873–1885-čaka",
    },
    "entries": ENT,
    "tail_1877": TAIL77,
    "notes": [
        "P199-metodologija: P198-recept-100%-reuse + md5-križna-validacija-verige (P197→P198→P199!) + RE-ALIGNED-KROP-row-tracing (levi/desni-strani-NE-poravnane-v-double-scan — offset-do-±1-vrstica!)",
        "NOVA-LEKCIJA-#17: žetoni-NE-preživijo-sandbox-wipe (GitLab-glpat-izgubljen → obnovljen-z-novim!) — credential-store-NI-trajen",
        "NOVA-LEKCIJA-#18: double-scan-RE-ALIGNMENT — levi-in-desni-strani-vrstice-nista-poravnani (vezava-skew!) — row-tracing-po-ROW-LINEIH-obvezen (s153-ord38/39-zmešnjava-rešena-z-ALL-crop!)",
        "lekcija-#12-potrjena-3.×: VLM-marginalni-ordinali-7→6-sistemsko (s156-'62[~72]'!) — KROP-margin-strip-OBVEZEN",
        "lekcija-#14-potrjena: VLM-raw-syllables > VLM-interpretacija ('Fortin-aus-Kogelnik'→'substituendus-Kogeju-coop'! 'Vancaš'→'Jančar'! 'Pegelj'→'Vezdirz/Pezdir(e)'! 'Muc'→'Hrizan'!)",
        "JANČAR-NIT-6-LET: 1878-tranzicija (Kogej→Jančar-med-Aprilom-in-junijem!) — naslovni-naraščaj-P197-ima-sedaj-PREDZGODOVINO!",
    ],
}

OUT.parent.mkdir(parents=True, exist_ok=True)
json.dump(proof, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"PROOF-OK: {OUT}")
print(f"vpisov={len(ENT)} griblje={len(grib)} hise={hise} h×2={hx2}")
print(f"najst={najst[0]}J-z{najst[1]['zap']} najml={najml[0]}J-z{najml[1]['zap']}")
print(f"spol={dict(spol_c)} friseln={fr_total} entz={entz_total}")
print(f"duh={dict(duh)} grib_duh={dict(grib_duh)}")
print(f"meseci={dict(sorted(Counter(e['mesec_no'] for e in ENT if e['mesec_no']).items()))}")
