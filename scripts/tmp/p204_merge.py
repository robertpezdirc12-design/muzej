#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P204 — MERGE KROP-forenzike v entries_1873.json (ročna-tabela-korekcij iz vizualnih-Readov!).
Recept: VLM-page-entries = baza; KROP-JSON = korekcije (SAMO-sklenne!); ročni-Read = arbiter-duelov."""
import json

TMP = "/tmp/p204"
ent = json.load(open(f"{TMP}/entries_1873.json"))

# ——— ROČNA-TABELA (iz-osebnih-Readov-kropov: z2, z8, z9, z71, z72/z76, z112, z115, z208!) ———
MANUAL = {
    2:  {"ime": "Anna Zegdirie [~ Zogdirie], vijol. dopisek 'Zgajnar' [?]", "opomba": "vijolična-poznejša-korekcija-ime! (VLM-Zgajnar/Zogbyer ~ KROP-Zegdirie-DUEL)"},
    8:  {"hisna": "65", "ime": "Jurbya baumann [~ Turbya?], ehm. + Mathias Milthin [~ Milthan?], Mary.", "opomba": "DVOJNI-ime-v-vrstici; h65-jasna (ne-66!)"},
    9:  {"hisna": "65", "ime": "Margaretha Küllik [~ Kullik], ½ Gäblerin", "starost": "32½ let", "opomba": "h65-×2-KLASTER (z8+z9!); pokop 1. Feber"},
    19: {"ime": "Maria Frupar [~ Krekar KROP-DUEL]", "opomba": "ime-DUEL: VLM-Frupar vs KROP-Krekar"},
    30: {"ime": "Marcus Jakofčič", "starost": "10 dni", "opomba": "KROP-KOREKCIJA-ime (VLM-'Mariund Jakočič'-halucinacija!)"},
    31: {"ime": "Maria Cilik [~ Salak?]", "starost": "1 leto", "opomba": "DUEL: VLM-'Halak-28J' vs KROP-'Cilik-1J'"},
    37: {"ime": "Georg Krik [~ Jakl/Jakoš?]", "starost": "4 leta", "opomba": "DUEL: KROP-Krik vs VLM-Jakl; starost 4 (ne-40!)"},
    45: {"ime": "Georg Mihik [~ Mikik?]", "starost": "1 leto [~ 4?]", "opomba": "starost-DUEL 1-vs-4 (Kurent!)"},
    55: {"opomba": "KROP-neučinkovit (zamenjana-vrstica) — VLM-ostaje: Georg Pezdirc h41 36J Magenkrampf"},
    71: {"vas": "Gradoc", "hisna": "43", "ime": "Johan Škipanić, nymf. R.", "starost": "1¾ let", "bolezen": "Ruhr", "opomba": "★ NI-GRIBLJE (VLM-halucinacija!) — Gradoc-43; pisarski-ordinal-68 = LUKNJA-67-s108!"},
    76: {"vas": "Krasinec mimo Griblje", "hisna": "58", "ime": "Marcus Dozeth [~ Dorgai?], apl. Ružar Pemgler [?]", "starost": "30 let", "bolezen": "Cholera", "opomba": "Griblje-DVOJNOST (h58!); VLM-'Mariana Pojkl'-NAPAKA; spol-MOŠKI-KROP!"},
    79: {"ime": "Josef Jakopič [~ Math. Golobič VLM-DUEL]", "starost": "47 let", "bolezen": "Nervöser Typhus [~ Entzündung]", "opomba": "ime/starost-DUEL VLM-vs-KROP"},
    80: {"starost": "18 let [~ 45?]", "opomba": "starost-DUEL KROP-18 vs VLM-45"},
    87: {"ime": "Anna Zajec [~ Ložež VLM-DUEL]", "opomba": "ime-DUEL (Ložež-×2-klaster z88!)"},
    112: {"starost": "5¾ let", "opomba": "KROP-KOREKCIJA-starost (VLM-'55J'-NAPAKA — 5¾-jasna!)"},
    115: {"ime": "Anna Brime", "starost": "5 let [~ 51?]", "opomba": "ime-KOREKCIJA (Brime!); starost-DUEL 5-vs-51"},
    140: {"ime": "Marcus Hure [~ Kure?]", "opomba": "mesec-DUEL: KROP-Nov-30./Dez-2. vs k113_marg-30./Okt-1. — VLM-ostaje"},
    168: {"hisna": "60 [~ 69?]", "opomba": "hisna-DUEL Kurent-9-0"},
    172: {"hisna": "34 [~ 74?]", "opomba": "hisna-DUEL KROP-74 vs VLM-34"},
    177: {"hisna": "11 [~ II.?]", "ime": "Mathias Lunič [~ Hunič/Tunič]", "opomba": "hisna-KOREKCIJA-h11 (VLM-'[?]'); LUNIČ-h11-NIT (P203-h11-KUNIĆ-1874!)"},
    208: {"ime": "Mathias Brime [~ Brinec]", "starost": "74 let", "bolezen": "Altersschwäche", "opomba": "P203-tail-1:1; KROP-vizualno-'Brime'-jasno"},
}

# ——— krop-JSON: dodaj-duhovnik-če-manjka + bolezen-nemška-če-različna (samo-sklenne!) ———
import glob, os
krops = {}
for f in glob.glob(f"{TMP}/krop-grib/z*.json"):
    d = json.load(open(f))
    try:
        z = int(os.path.basename(f).split("_")[0][1:])
        krops[z] = d
    except Exception:
        pass

fixed = 0
for e in ent["entries"]:
    z = e.get("z")
    if z in MANUAL:
        e.update(MANUAL[z])
        fixed += 1
    k = krops.get(z)
    if k and e["z"] not in (71, 55):  # z71/z55 = zamenjana-vrstica (ignore!)
        if k.get("duhovnik") and not e.get("duhovnik"):
            e["duhovnik"] = k["duhovnik"]
        if k.get("bolezen") and e.get("bolezen") and k["bolezen"][:12].lower() not in (e["bolezen"] or "").lower():
            e["bolezen_krop"] = k["bolezen"]

# Griblje-rebuild po-korekcijah (z71-IZPIST!)
griblje = [e for e in ent["entries"]
           if ("gribl" in (e.get("vas") or "").lower() or "grible" in (e.get("vas") or "").lower()
               or "hrible" in (e.get("vas") or "").lower())
           and e["z"] != 71]

ent["griblje"] = len(griblje)
ent["griblje_entries"] = griblje
ent["korekcije"] = {"manual": sorted(MANUAL.keys()), "n_fixed": fixed}
ent["ord_kaskada"]["luknje"] = [67, 141, 142, 143, 144]
ent["ord_kaskada"]["dupkati"] = [24, 37, 61, 153]
ent["ord_kaskada"]["honesty"] = "ordinal-end-211/212-Kurent-zmeda-koncu (dupkati-4-luknje-5-neto-−1)"

json.dump(ent, open(f"{TMP}/entries_1873.json", "w"), ensure_ascii=False, indent=1)
print(f"MERGE: {fixed} ročnih-korekcij; Griblje-FINAL: {len(griblje)} (z71-izpust!)")
print("Griblje-z:", [e["z"] for e in griblje])
