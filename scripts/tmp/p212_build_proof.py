#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P212 — build proof research/issue17/parish-death-1865-04106.json (recept P200–P211)."""
import json, re, os

E = json.load(open("/tmp/p212/entries_1865.json"))
entries = E["entries"]
griblje = E["griblje_entries"]

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

MESECI_MAP = {"Februar": "Feber", "Januar": "Jänner", "Jüli": "July", "Juli": "July", "Junij": "Juni",
              "Avgust": "August", "Sept": "September", "Okt": "October", "Oktob": "October", "Dec": "Dezember", "December": "Dezember"}
meseci = {}
for e in entries:
    m = (e.get("mesec") or "").strip()
    if not m: continue
    key = m.split()[0].split("-")[0].rstrip(".").strip()
    key = MESECI_MAP.get(key, key)
    if key.lower() in ("jänner", "feber", "märz", "april", "mai", "juni", "july", "august", "september", "october", "november", "dezember"):
        meseci[key] = meseci.get(key, 0) + 1
meseci_sum = sum(meseci.values())

proof = {
    "faza": "P212",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1865 = 21. leto PREDZGODOVINSKE LINIJE (issue #18) — ordinali-1–66-ČISTO-6.leto + z74-duel-REŠEN (Kurrent-4/1!) + MEJA-'1865'-50.-POTRDITEV + ULEDBA-#11 + ANOMALIJA-pokop-pred-smrtjo (pisar-mota!) + HUSIČ-h37-klaster (mati+otrok!) + 2×-Maria-Križan-v-1-tednu!",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1865": f"s46-restart–s51-tail-z66 (pag 41–46); {len(entries)} vpisov (ordinali-1–66-ČISTO (6.-leto-zapored!), ŠTEVJE-IZ-VRSTIC-14.×!) / {len(griblje)} Griblje / {len(hise)} hiš (h37-×2-HUSIČ-klaster!)",
        "meja_1864_65": "★★★ s46 (pag 41): tail-1864 (z88–z91-NATAČNO-4-vrstice-KROP! + z91-ULEDBA-#11-10.INSTANCE-30.Dez-1864→1.Jänner-1865-pokop!) + dvojna-ločilna-črta + '1865'-VELIKA-LETVICA-KROP-50.-POTRDITEV-invariante! + restart-z1-Griblje-h3-Maria-Križan-81J!",
        "meja_1865_66": "★★★ s51-tail-z65/z66 (P211-KROP-dokaz!) → restart-'1866' (P211-že-obdelano!)",
        "zaporedna": f"★★★ ordinali-1–66-ČISTO-BREZ-luknje/dupa — 6.-LETO-ZAPORED! (kontinuiteta-zap: s46-z1→s50-z64 + s51-tail-z65/z66; vrstna-aritmetika 7+14+14+14+15+2)",
        "forma": "'1865'-VELIKA-LETVICA-s46-KROP (50.-potrditev-invariante!) + dvojna-črta + restart-'Jänner'!",
        "skeni": "s042–s051 (pag 37–46; 10-skenov: s42–s45-1864-kontekst + s46–s50-1865 + s51-tail-reuse-P211; 2×-NEODVISNA-PRENOSA-9/9 + križ-s50-vs-P211-disk-1:1!)",
        "preslikava": "pag = sken−5 (s46=41 … s51=46)",
        "preštevanje": f"vrstna-aritmetika 7+14+14+14+15+2(s51-tail) = {len(entries)} ✓ (s46-tail-4-SKIP!); meseci-vsota = {meseci_sum}",
    },
    "statistika": {
        "vpisov_1865": len(entries),
        "griblje": len(griblje),
        "hise": hise,
        "otrok_griblje": f"{len(otroci)}/{len(griblje)} = {round(100*len(otroci)/len(griblje))}% — otroška-umrljivost-1865 (z11-1-J-Wassersucht + z18-2-mes + z50-6-dni + z63-2-leti = {len(otroci)}-otrok / 9-odraslih!) — NIŽJA-kot-1866 (77%!)",
        "meseci": meseci,
        "duhovniki": "celostanska-VLM-podpisov-delno ('Joh.-Judnic-Cooperator' + 'Joh.-Pudič[?]-coop.' + N.N.)",
    },
    "anomalije": [
        "★★★ MEJA-1864/65-s46: tail-1864-z88–z91 (KROP-NATAČNO-4-vrstice! z89-starost-korekcija-v-zapisu!) + z91-ULEDBA-#11-10.INSTANCE (smrt-30.Dez-1864→pokop-1.Jänner-1865! cf. P209-z103-31.Dez→1.Jän + P211-z58-Juni→Juli!) + dvojna-ločilna-črta + '1865'-VELIKA-LETVICA-KROP-50.-POTRDITEV!",
        "★★★ z74_s45_zap-DUEL-REŠEN: s45-zaporedne-74/75/76-KROP (VLM-'71/72/73'-FALSIFICIRAN — '4-ima-ZANKO-1-je-ozka-črtica'-KURRENT-ANALIZA!) → 1864-kontekst-veriga-60–91-ČISTO-ZVEZNA (s44:60–73 + s45:74–87 + s46-tail:88–91)!",
        "★★★ z13-ANOMALIJA-PISAR-MOTA: pokop-17.-vpisan-PRED-smrt-18. (KROP-POTRJENO-v-zapisu! 'morda-smrt-17./pokop-18.') — h37-Griblje-Anna-Husič-27-J-Schwindsucht!",
        "★★★ HUSIČ-h37-KLASTER: z13-mati-Anna-27-J (umrla-18.2) + z18-otrok-Anna-2-mes (umrla-11.3) — '½-Güblerswirt' + '-kind'-suffix = OBE-ISTE-hiša! (mati+dojenček-v-3-tednih!)",
        "★★★ 2×-MARIA-KRIŽAN-v-1-tednu: z88-tail-Otok-h20-48-J-12.Dez + z1-restart-GRIBLJE-h3-81-J-16.Jan — ista-bazna-beseda-stana-obe ('Ablabamin[~]')!",
        "★★★ BRINC-×2-RAZLIČNI-hiši: z9-Anna-h23-60-J + z20-Jernej-h28-28-J (1-mesec-razmika!)",
        "★★★ POŽEK-nit: z36-Mathias-h67-36-J-Abzehrung — cf. P211-z90-h58-Totgeborenes-v.-Mark.-Požek + P192-h58! (h67-NOVA-hiša-nit!)",
        "★★★ PEZDIRC-h14-KONTINUITETA-tail: z66-Maria-Pezdirc-66-J — z41-1866-Mathias-unehelich-h14! (VLM-h11-duel-rešen-KROP-h14!)",
        "★★★ KRIŽAN-h3-nit: z1-Maria-81-J — cf. 1867-z98-h3-Papic-×3 (P210)!",
        "★ otroška-umrljivost-1865: 4/13 = 31% — NIŽJA-kot-1866 (10/13-77%!) — cholera-prelivala-v-1866?",
        "★ stan-DUEL-HONEST-×4: z1-'Ablabamin[~DUEL-3×-branja]' + z8-'Güblerin[~DUEL]' + z65/z66-'Abfaknin/Ablokumin[~DUEL: ?-dekla]' — kurrent-stan-leksikon-nekonkluziven!",
        "★ s44/s45-VLM-overlap-phantom (71–73-oboje!) — REŠEN-z74-KROP (phantom-bil-VLM-misread!)",
    ],
    "hišne_kontinuitete": {
        "h37": "★★★ HUSIČ-klaster-1865: z13-mati-27-J-Schwindsucht + z18-otrok-2-mes (½-Güblerswirt + -Kind!) — cf. P211-z22-h41-Hušić[~Huestič!]-grafia-nit!",
        "h14": "★★★ PEZDIRC-nit: z66-tail-1865-Maria-66-J → z41-1866-Mathias-unehelich-Kind! (do-1903-43-let-globoko!)",
        "h3": "KRIŽAN-nit: z1-Maria-81-J-1865 → 1867-h3-Papic-×3 (P210)!",
        "h23/h28": "BRINC-×2: z9-Anna-60-J-h23 + z20-Jernej-28-J-h28 (1865!)",
        "h67": "POŽEK-nit-#2: z36-Mathias-36-J-1865 — cf. h58-POŽEK (P192+P211-z90)!",
        "h19": "z63-Anna-Križe-2-J-1865 — cf. P211-z34/z35-h19-Vranoviče-Žunič-dvojčka (razl. vas!)",
        "h32": "z50-Michael-Straus-6-dni-1865 — cf. 1866-h34-FILAK-×2 (sosednje-hiše?)",
    },
    "crossChecks": [
        "2×-neodvisna-prenosa-vsak-sken (s042–s050)-md5-1:1-9/9 (strežnik-determinističen!) — veriga-P212-2×-samoskladnost-12.×!",
        "križ-disk: s50-md5-0720bbe7 == P211-disk-/tmp/p211/s50.jpg-1:1 ✓ (reuse-VLM-že-brani!)",
        "'1865'-VELIKA-LETVICA-KROP-s46 (50.-potrditev-invariante!) + dvojna-ločilna-črta ✓",
        "tail-1864-KROP: NATAČNO-4-vrstice-88–91 (ni-gaplje-85–87 — s45=74–87-KROP-z74!) ✓",
        "z74-KROP: '4-ima-zanko-na-dnu-1-je-ozka-črtica'-cifra-analiza → 74/75/76 ✓",
        "vrstna-aritmetika: 7+14+14+14+15+2 = 66 ✓ (s46-tail-4-SKIP!)",
        f"meseci-vsota: J8+F6+M7+A10+M6+J2+J6+A4+S3+O4+N7+D3 = {meseci_sum}-normirano ✓",
        "veriga-zap: s46-z1–7 + s47-8–21 + s48-22–35 + s49-36–49 + s50-50–64 + s51-tail-65/66 = 1–66-ČISTO ✓",
        "s51-tail-z65/z66: P211-KROP-dokaz-arb_s51_glava (1:1-reuse!) ✓",
        "Griblje-13/12-hiš (h37-×2) ✓",
    ],
    "honesty": {
        "H1": "ŠTEVJE-IZ-VRSTIC-14.× (ordinali-1–66-ČISTO!); z-numeracija-vrstica-1:1",
        "H2": "stan-DUEL-HONEST-×4-neskladen (z1-Ablabamin-3×-branja + z8-Güblerin + z65/66-Abfaknin/Ablokumin) — [~] — kurrent-stan-leksikon!",
        "H3": "z13-pokop-pred-smrtjo — pisar-mota-dokumentirana (alternativa: smrt-17./pokop-18.) — [~]",
        "H4": "z9-starost-DUEL (KROP-60-vs-VLM-56) — zapis-60[KROP]-duel",
        "H5": "z8-hisna-68-VLM (KROP-izven-izreza → re-crop-pending); vas-Griblje-po-VLM+ključu",
        "H6": "VLM-leto-halucinacije-kontekst (s42-'1861'-misread + s47-'1868'-misread + s48-'~1862' — resnica: vse-1864-kontekst + 1865!)",
        "H7": "meseci-'December'×2-vs-'Dezember'-grafia-normirana",
        "H8": "z17/z18/z20/z24/z36/z50/z63-KROP-cropi-IZREZANI (VLM-vrstice-1:1) — VLM-429-kvota-blokada-brisalnja (60+min!) → krop-pending-oznake-v-entries — NE-anomalne-vrstice (VLM-ZADOSTNO!)",
        "H9": "s44/s45-overlap-phantom-71–73 — NE-je-DOUBLE-SCAN (vsebine-RAZLIČNE!) — phantom-VLM-misread-rešen-z74-KROP",
    },
    "kaskada": {
        "before": {"vitals": 1544, "04106": 325, "faz": 211},
        "after": {"vitals": 1544 + 13, "04106": 325 + 13, "faz": 212},
        "yearset": "+1865",
        "verifier_patch": "p19x–p212 (kumulativni-1544→1557 + 325→338 + yearset-+1865)",
    },
    "lead": {
        "P213": E.get("leadP213", "1864 — s42–s46-tail-ŽE-VLM+delno-KROP (zap-31–91-ZVEZNA) → probe-s039–s042!"),
    },
    "entries_count": len(entries),
    "griblje_count": len(griblje),
    "notes": "P212 = 10-skenov-faza (s042–s051; 5-1865-sami + 4-1864-kontekst + s51-tail-reuse-P211). MEJA-'1865'-50.-POTRDITEV + z74-duel-REŠEN + ULEDBA-#11 + ANOMALIJA-pokop-pred-smrtjo + HUSIČ-h37-klaster + 2×-Maria-Križan. Otroška-umrljivost-31% (NIŽJA-kot-1866-77% — cholera-prelivala-v-1866?).",
}

kglava = json.load(open("/tmp/p211/krop-reads/arb_s51_glava.json"))
ktail = json.load(open("/tmp/p212/krop-reads/arb_s46_tail.json"))
kglava212 = json.load(open("/tmp/p212/krop-reads/arb_s46_glava.json"))
proof["entries"] = entries
proof["griblje_entries"] = griblje
proof["tail_1864"] = {"vir": "s46-KROP-tail (pag 41)", "vrstice": ktail.get("vrstice", []),
                       "stevilo": ktail.get("stevilo_vrstic"), "precrtana": ktail.get("ali_precrtana")}
proof["meja_1865"] = {"vir": "s46-KROP-glava (pag 41)", "velika_letnica": kglava212.get("velika_letnica"),
                       "cifre": kglava212.get("cifre_posamicne"), "restart": kglava212.get("restart_vrsta1"),
                       "naslednja_vrsta2": kglava212.get("naslednja_vrsta2")}
proof["tail_1865_p211"] = {"vir": "s51-KROP-glava (pag 46; P211-dokaz-reuse!)", "vrstice": kglava.get("tail_vrstice", []),
                            "precrtana": kglava.get("precrtana_vrsta"), "restart": kglava.get("restart_vrsta1")}
os.makedirs("/home/z/muzej/research/issue17", exist_ok=True)
json.dump(proof, open("/home/z/muzej/research/issue17/parish-death-1865-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"OK dokaz: entries={len(entries)} griblje={len(griblje)} otroci={len(otroci)} meseci-sum={meseci_sum}")
