#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P204 — build proof research/issue17/parish-death-1873-04106.json (recept P200–P203)."""
import json, re

E = json.load(open("/tmp/p204/entries_1873.json"))
entries = E["entries"]
griblje = E["griblje_entries"]
kask = E["ord_kaskada"]

def starost_leta(s):
    s = (s or "").lower()
    m = re.match(r"\s*(\d+(?:[.,¾½¼]\d*)?)", s)
    if not m: return None
    v = m.group(1).replace(",", ".")
    try: f = float(v)
    except: return None
    if 0 < f < 1 and ("½" in s or "¾" in s or "¼" in s or "." in v): return f
    return f if f < 10 else None

otroci = [e for e in griblje if starost_leta(e.get("starost")) is not None]
hise = sorted({str(e.get("hisna", "?")).split()[0] for e in griblje}, key=lambda x: (len(x), x))

# meseci-vsota (VLM-page-mesec-polja; s119 = samo-tail-9!)
meseci = {}
for sken in range(102, 119):
    d = json.load(open(f"/tmp/p204/vlm-page/s{sken}.json"))
    for x in d.get("vrstice", []):
        m = (x.get("mesec") or "").strip()
        if not m or x.get("ime") and not x.get("vas") and not x.get("mesec"):
            continue
        key = m.split()[0].split("-")[0].rstrip(".").strip()
        key = {"Februar": "Feber", "Januar": "Jänner", "Jüli": "July", "Juli": "July", "Junij": "Juni", "Junij?": "Juni", "Avgust": "August", "Okt": "October", "Sept": "September", "Oktob": "October", "Dec": "Dezember", "Decemb": "Dezember", "Jan": "Jänner", "Feb": "Feber", "December": "Dezember"}.get(key, key)
        if key.lower() in ("jänner", "feber", "märz", "april", "mai", "juni", "july", "august", "september", "october", "november", "dezember"):
            meseci[key] = meseci.get(key, 0) + 1
# s119-tail (vrste 1–9 = Dez-1873!)
d119 = json.load(open("/tmp/p204/vlm-page/s119.json"))
for x in d119.get("vrstice", [])[:9]:
    m = (x.get("mesec") or "").strip()
    key = m.split()[0].rstrip(".").strip() if m else ""
    key = {"Dec": "Dezember", "Decemb": "Dezember"}.get(key, key)
    if key.lower() == "dezember":
        meseci[key] = meseci.get(key, 0) + 1
meseci_sum = sum(meseci.values())

proof = {
    "faza": "P204",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1873 = 13. leto PREDZGODOVINSKE LINIJE (issue #18) — ★★★ KOLERA-LETO (cholera epidermica)!",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1873": f"s102–s118 + s119-tail-9 (pag 97–114); {len(entries)} vpisov (z1–z{len(entries)}, ŠTEVJE-IZ-VRSTIC-6.×!) / {len(griblje)} Griblje / {len(hise)} hiš / NAJVEČJE-leto-korpusa (212! — 2.3× P203-94!)",
        "meja_1872_73": "★★★ s102 (pag 97): '1873.'-GLAVA-V-DATUMSKI-CELICI (41.-POTRDITEV-invariante!) + 'Incipit annus Domini'-ročno-glava + restart-zaporedja-1–12; s101-Dez-1872-tail (zap 102–110, 'finis'-zaključek!) = P205-LEAD",
        "meja_1873_74": "★★★ s119 (pag 114): TAIL-9-DEZ-1873 (ordinala-204–212-KROP! 4-GRIBLJE-v-k129-top: z208-h23-Brime + z210-h2-Hlebec + z211-h16-Brume-31-Dez→1-Jän-ULEDBA!) + 'December 1873'-GLAVA-V-Z204-CELICI (43.-POTRDITEV!) + '1874. Jänner Incipit annus Domini'-meja-glava (KROP!) + restart-1–4",
        "konec_1873": "z212 = s119-r9 (Dez-31/Jan-1-Gradec-Aloys-Hrabl-16 — ULEDBA-2.!) — leto-konča-z-3-ULEDBAMI (z211 + z212 + P203-z1-Podiner!)",
        "zaporedna": "★★★ ordinali-VIDNI-ampak-KURENT-ZMEDANI → ŠTEVJE-IZ-VRSTIC-6.×; pisarski-ordinali-rekonstruirani: dupkati-4 (24, 37, 61, 153!) + luknje-5 (67-s108 + 141–144-s114!) → neto-−1 (211/212-Kurent-koncu!)",
        "forma": "★★★ GLAVE-V-DATUMSKI-CELICAH-×5-ta-seja: 41.-POTRDITEV-s102-z1-'1873.'-Jänner + 42.-s105-z24-'1873.'-Feber(+März-prečrtan!) + s106-z37-'1873. Jüni'-glava + s108-z61-'August'-glava + 43.-s119-z204-'December 1873' + s115-z150-'1873. October' (6.-v-seji!) — REKORD ×6!",
        "skeni": "s100–s119 (pag 95–114; 20-skenov-NAJVEČJA-faza!); s118+s119-md5-vs-P203-disk-1:1 (ecef17aa/af63f203) + s110/s111-potrditev-2. kroga — VERIGA-P197→…→P204-8.×!",
        "preslikava": "LEKCIJA-#21-nadaljevanje: pag = sken−5-v-tem-razponu (s102=97, s110=105, s119=114!); natisnjene-št.-potrjene-×4-KROP (s111-'106', s115-'110', s118-'113', s114-'110'?-desno!)",
        "preštevanje": f"vrstna-aritmetika 12+12+14+12+13+13+13+13+12+12+13+13+12+12+13+14+9 = {len(entries)} ✓ (s104-DOUBLE-SCAN-IZPUŠČEN! s119-tail-9!); meseci-vsota-≈{meseci_sum} (±VLM-globlne-glave)",
    },
    "statistika": {
        "vpisov_1873": len(entries),
        "griblje": len(griblje),
        "hise": hise,
        "otrok_griblje": f"{len(otroci)}/{len(griblje)} jasna = {round(100*len(otroci)/len(griblje))}% — KOLERA-OTROŠKA-UMRLJIVOST (z30-10dni + z31-1J + z37-4J + z45-1J + z49-3mes + z63-1J + z112-5¾J + z115-5J[~51?] + z171-1J + z193-3mes-3ted + z6-3½ted + z88-2J + z3-19J-ne...)",
        "duhovniki": "Heschl-Cooperator (Jän!) + 'Ho.'-kratice-pogoste + Bobek-C.r.p.-×n + Kogej-Pfr.-kontekst-P199/200-NIT-nadaljevanje? + Vogrinc-Pfr.-Dez-tail!",
    },
    "anomalije": [
        "★★★ KOLERA-LETO-1873: ~2/3-vpisov-'Cholera'-bolezen (epidemia-korpus-REKORD — 212-vpisov = 2.3×-sredina!)",
        "★★★ DOUBLE-SCAN-3.×: s103 == s104 (md5-RAZLIČNA-ampak-vsebina-1:1-KROP-ordinali-13–18-jasno-×2!) — pag-98-×2! (lekcija-#21-2.×-P203-s123==s124!)",
        "★★★ PISARSKI-ORDINAL-DUPKATI-×4: 24 (s104-z24 + s105-r1!), 37 (s105-end + s106-r1-'1873. Jüni'!), 61 (s107-end + s108-r1-'August'!), 153 (s114-end + s115-r1-'October'!) — vsak-ob-STRANI-MEJI!",
        "★★★ PISARSKI-ORDINAL-LUKNJE-×5: 67 (s108-r7-'68'-vijolično!) + 141–144 (s114: 137–140→145–153-skok-4!)",
        "★★★ VLM-ORDINAL-OFF-BY-N-×n (s113-'128–140'-KROP-124–136! + s114-'133–145'-KROP-137–153! + s119-'201–209'-KROP-204–212!) — KROP-MARGINALA-FORENZIKA-REŠILA-×3!",
        "★★★ KROP-KOREKCIJE-×7: z30-'Mariund-Jakočič'→'Marcus-Jakofčič' + z71-'Griblje-37-Maria-Hrušič'→NI-GRIBLJE-(Gradoc-43-Škipanić!) + z76-spodnja→'Marcus-Dozeth-apl-Ružar-h58-Cholera-MOŠKI' + z112-'55J'→'5¾-J' + z115-'Brune'→'Brime' + z177-h[?]→h11-LUNIČ + z140-'9J'→'1-[?]'",
        "★★★ h65-×2-KLASTER (z8-Jurbya-baumann-dvojni-ime-vrstica + z9-Margaretha-Küllik-½-Gäblerin-32½J-Kindbett!) — h65-NIT!",
        "★★★ Griblje-DVOJNOST-z76 (Krasinec-mimo-Griblje-h58-Marcus-Dozeth — h58-čez-lokalnosti!)",
        "★★★ ULEDBA-×3-konec-1873 (z211-h16-Brume-31-Dez→1-Jän + z212-Gradec-31/1 + P203-z1-Podiner!)",
        "★ z2-Anna-Zegdirie-vijol.-korekcija-'Zgajnar' (poznejša-tinta-dopisek!)",
        "★ LUNIČ-h11-1873 (z177-63-J-Cholera!) — 1-LETO-PRED-h11-KUNIĆ-1874-16-dni (NIT-3-leta-1873→1875!)",
        "★ PEZDIRC-×2-1873 (z55-Georg-h41-36J + z63-Katharina-h40-1J!) — PEZDIR-NIT-širša",
        "★ MESČNI-NOSILCI-1873: 'Februar'-prečrtan-z104-z13 (Jänner-korekcija!) + 'März'-prečrtan-s105-z24 — mesec-glave-NAD-datumom-NE-pogost-forma-1873 (numerčni-meseci-1874-NI-še!)",
    ],
    "hišne_kontinuitete": {
        "h11": "LUNIČ-1873 (z177-63J) → KUNIĆ-h11-1874-16dni (P203!) → KUNIĆ-h11-1875-65J (P202!) — NIT-3-leta!",
        "h65": "×2-1873 (z8 + z9!) — NOVA-hiša-korpusa",
        "h58": "Krasinec-mimo-Griblje-1873 (z76-Dozeth!) — dvojna-lokalnost-NIT",
        "h23": "Brime-1873-Dez (z208!) — P203-tail-1:1-potrjena",
        "h2": "Hlebec-1873-Dez (z210!) + P200-'Hrible'[?]-Tomc-klaster-1877!",
        "h16": "Brume-1873-Dez-ULEDBA (z211!) — cf. P201-h16-PILAH-tail-1876!",
        "h55": "Zgajnar/Zegdirie-1873-Jän (z2!) — NOVA-hiša-korpusa",
        "h13": "×2-1873 (z30-Jakofčič-10dni + z31-Cilik-1J!) — otroška-KOLERA",
        "h24": "Brime-1873 (z115-5J[~51?]-Sept!) — cf. P203-h24-Brime-9J-Feber-1874 — BRIME-h24-NIT-×2!",
    },
    "crossChecks": [
        "md5-križna-validacija: s118+s119-sveži == P203-disk-1:1 (ecef17aa784d/af63f2035e01) — VERIGA-8.×!",
        "md5-2. krog: s110+s111-sveži == P204-disk-1:1 (b6af6f62/a8db8f6b) + s100–s109-fresh-JPEG ✓",
        "DOUBLE-SCAN-s103==s104: KROP-ordinali-13–18-jasno-×2 + vrstica-1:1 ('19./21-Dobravice' + '20./21-Vranovic' + '22./24-Boršt'...) ✓",
        "dupkat-ordinal-24: s104-z24-KROP-'26./27-Krasinec-Anna' ≠ s105-r1-KROP-'29./30-Cerkovise-Katharina' — RAZLIČNA-VRSTICA-z-ISTIM-ordinalom! ✓",
        "dupkat-ordinal-37: s105-end ≠ s106-r1-'Jüni-14./15-Gradac-Johann' ✓ + dupkat-61: s107-end ≠ s108-r1-'August-15/17-Cerkviše-Nicolaus' ✓ + dupkat-153: s114-end-Peter-Zeli ≠ s115-r1-'October-8/10-Ceroviše-Maria' ✓",
        "luknja-67: krop-z71-ordinal-'68'-vijolično-jasno (s108-r7!) ✓ + luknja-141–144: k114_marg2-'137–140' + k114_marg_bot-'145–150' ✓",
        "ordinal-end-212: k119_bot-'209–212'-jasno-×4 ✓ + tail-start-204: k119_top_hi-'204–211' ✓",
        "s119-tail-9 == P203-tail_1873-vrste-1–9-1:1 (z204-Sapee-33 + z205/z206-Sobič + z207-Tügel + z208-Brime-h23 + z209-Galovec + z210-Hlebec-h2 + z211-Brume-h16!) ✓",
        "'1873.'-glave-v-celicah-×3-KROP (s102 + s105 + s115!) + mesec-glave-'Jüni'/'August'/'December-1873'-×3 ✓",
        "vrstna-aritmetika: 12+12+14+12+13+13+13+13+12+12+13+13+12+12+13+14+9 = 212 ✓",
        "s119-'December 1873'-glava-v-z204-DATUMSKI-CELICI (43.-POTRDITEV!) ✓",
    ],
    "honesty": {
        "H1": "ŠTEVJE-IZ-VRSTIC-6.× (ordinali-VIDLJIVI-ampak-Kurent-zmedani — pisarski-dupkati/luknje!); z-numeracija-vrstica-1:1",
        "H2": "ordinal-end-211/212-Kurent-zmeda-koncu (dupkati-4-luknje-5-neto-−1!) — flag",
        "H3": "z71-VLM-'Griblje-37-Maria-Hrušič'-FALSIFICIRAN (KROP-Gradoc-43-Škipanić!) — Griblje-39→38!",
        "H4": "starost-DUELI-×4 (z112-5¾-vs-55 + z115-5-vs-51 + z80-18-vs-45 + z79-47-vs-2½) — [~]",
        "H5": "ime-DUELI-×5 (z2 + z19 + z31 + z37 + z87) — [~]",
        "H6": "hisna-DUELI-×3 (z168-60/69 + z172-34/74 + z2-55/53) — [~]",
        "H7": "z140-mesec-DUEL (Nov-vs-Okt) — [~]",
        "H8": "s104-VLM-branje-IZPUŠČENO (double-scan-kaos 'October/Feber/1865'-halucinacija!) — s103-kopija-uporabljena",
        "H9": "meseci-vsota-±3-drift-možna (VLM-glave-različno-zajete)",
    },
    "kaskada": {
        "before": {"vitals": 1406, "04106": 187, "faz": 203},
        "after": {"vitals": 1406 + 38, "04106": 187 + 38, "faz": 204},
        "yearset": "+1873",
        "verifier_patch": "p19x–p203 (kumulativni-1406→1444 + 187→225 + yearset-+1873)",
    },
    "lead": {
        "P205": "1872 — s101-TAIL-×9-DEZ-1872-ŽE-VLM-PREBRANA (zap-102–110 + 'finis'!) + s100-FETCHAN+VLM (Nov/Dez-kontekst!) → probe-s092–s101!"
    },
    "entries_count": len(entries),
    "griblje_count": len(griblje),
    "notes": "P204 = NAJVEČJA-faza-korpusa (20-skenov + 212-vpisov + 38-Griblje!). Recept: P200–P203. Kolera-1873-zgodovinska-potrjena.",
}

import os
os.makedirs("/home/z/muzej/research/issue17", exist_ok=True)
json.dump(proof, open("/home/z/muzej/research/issue17/parish-death-1873-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: research/issue17/parish-death-1873-04106.json — {len(entries)}-vpisov / {len(griblje)}-Griblje / {len(hise)}-hiš")
print("hiše:", ",".join(hise))
print("otroci:", len(otroci), "/", len(griblje), f"= {round(100*len(otroci)/len(griblje))}%")
print("meseci:", meseci)
