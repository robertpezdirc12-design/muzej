#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P19 — FAZA 1: PODATKOVNA PRAVILNOST (revizija uporabnika, 2026-10-10)

Pet ugotovitev, popravljeno na podlagi virov:
  1. DOGODKA 500-letnic: jubilej je CERKVENI — 1526 = prva pisna omemba CERKVE
     sv. Vida (viri MVG-003: Radio Odeon, Moja Dolenjska, Občina Črnomelj,
     Slovenske novice, Wikipedija cerkev; ešd 2122), VAS pa je prvič izpričana
     leta 1468 kot Griblach (MVG-001: EN Wikipedija + Snojev etimološki slovar).
     Slovenska Wikipedija v infopolju napačno navaja "omemba: 1526" za naselje.
  2. MVG-049 (zaselki): yearFrom 1526 → 1468 — zaselki so deli vasi, ki je
     izpričana 1468; ločenih omemb zaselkov viri (še) ne podajajo.
  3. extra.json: 3 postaje z napačnim letom 1526 → 1468; 23 postajam dodani
     KONKRETNI viri (izključno iz virov matičnih zapisov — nič novega);
     vsem preostalim postajam brez lastnega vira evidence "v raziskovanju".
  4. Odstranjeni 2 zastareli related povezavi na neobstoječi MVG-114
     (kresna-pesem-1888 — rezervirana, a dokazi še niso zbrani).

IDs se ne generirajo na novo — obstoječi ostanejo.
"""
import json
import sys

BASE = "/home/z/my-project/muzej-analysis"
sys.path.insert(0, BASE)

def load(p):
    with open(f"{BASE}/{p}", encoding="utf-8") as f:
        return json.load(f)

def save(p, data):
    with open(f"{BASE}/{p}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"  ✓ zapisano {p}")

# ────────────────────────────────────────────────────────────────────
# 1) EVENTS.JSON — dva dogodka 500-letnic (cerkev, ne vas)
# ────────────────────────────────────────────────────────────────────
print("1) events.json — jubilej je cerkveni (1526 = cerkev; vas = 1468)")
events = load("src/data/museum/events.json")

E1 = "0b32dc9c-8640-4bdd-b84e-8ba449def9f4"  # Radio Odeon, 23. 6. 2026
E2 = "5f6599aa-5ef1-4abe-84be-e2081d62d486"  # Slovenske novice, 13. 8. 2026

for e in events["events"]:
    if e["id"] == E1:
        e["titleSi"] = "500-letnica prve omembe cerkve sv. Vida — slovesna maša"
        e["titleEn"] = "500th anniversary of the first written mention of St. Vitus' church — solemn mass"
        e["descriptionSi"] = (
            "Griblje so 23. junija 2026, ob Vidovskem žegnjanju, obeležile 500 let prve pisne "
            "omembe cerkve sv. Vida (1526): svečana maša v Gribljah, ki jo je pozdravil tudi "
            "župnik z ozaveščanjem jubileja krajev ob Kolpi. Vas sama je v listinah starejša — "
            "prvič je izpričana leta 1468 (MVG-001) — zato je jubilej cerkveni, ne vaški. "
            "Podrobnosti slovesnosti v zapisu MVG-003. Vir: Radio Odeon (23. 6. 2026)."
        )
        e["descriptionEn"] = (
            "On 23 June 2026, at the feast of St. Vitus, Griblje marked 500 years since the "
            "first written mention of the church of St. Vitus (1526): a solemn mass in Griblje, "
            "also greeted by the parish priest with a call to honour the jubilee of the places "
            "along the Kolpa. The village itself is older in the records — first attested in "
            "1468 (MVG-001) — so the jubilee belongs to the church, not the village. Details of "
            "the ceremony in record MVG-003. Source: Radio Odeon (23 June 2026)."
        )
        print("  ✓ dogodek 1 (Radio Odeon) popravljen")
    if e["id"] == E2:
        e["titleSi"] = "Butoraj in Griblje — skupna proslava cerkvenih 500-letnic"
        e["titleEn"] = "Butoraj and Griblje — joint celebration of the two churches' 500th anniversaries"
        e["descriptionSi"] = (
            "V Beli krajini so leta 2026 obeležili pomemben cerkveni jubilej, ki povezuje "
            "preteklost, vero in kulturno dediščino krajev ob Kolpi: v Butoraju in Gribljah so "
            "slovesno mašo skupaj proslavili 500-letnici prve pisne omembe obeh cerkva — "
            "sv. Marka v Butoraju in sv. Vida v Gribljah (prvič zapisani leta 1526). "
            "Vir: Slovenske novice/Delo (13. 8. 2026)."
        )
        e["descriptionEn"] = (
            "In 2026 Bela krajina marked an important church jubilee linking the past, faith "
            "and the cultural heritage of the places along the Kolpa: Butoraj and Griblje "
            "celebrated with a joint solemn mass the 500th anniversaries of the first written "
            "mentions of their two churches — St. Mark's in Butoraj and St. Vitus' in Griblje "
            "(both first recorded in 1526). Source: Slovenske novice/Delo (13 Aug 2026)."
        )
        print("  ✓ dogodek 2 (Slovenske novice) popravljen")

assert len(events["events"]) == events["count"] == 11, "število dogodkov se je spremenilo?"
save("src/data/museum/events.json", events)

# ────────────────────────────────────────────────────────────────────
# 2) EXHIBITS.JSON — MVG-049 yearFrom 1526 → 1468
# ────────────────────────────────────────────────────────────────────
print("2) exhibits.json — MVG-049 (zaselki) yearFrom 1526 → 1468")
exhibits = load("src/data/museum/exhibits.json")
m49 = [e for e in exhibits["exhibits"] if e["museumNo"] == "MVG-049"]
assert len(m49) == 1 and m49[0]["yearFrom"] in (1526, 1468), "MVG-049: nepričakovana letnica"
m49[0]["yearFrom"] = 1468
# preveri: noben zapis več nima mejnega leta 1526
still_1526 = [e["museumNo"] for e in exhibits["exhibits"]
              if e.get("yearFrom") == 1526 or e.get("yearTo") == 1526]
assert not still_1526, f"1526 še ostaja pri: {still_1526}"
assert len(exhibits["exhibits"]) == exhibits["count"] == 113
save("src/data/museum/exhibits.json", exhibits)

# ────────────────────────────────────────────────────────────────────
# 3) EXTRA.JSON — letnice 1468, izpolnjeni viri, oznake, MVG-114
# ────────────────────────────────────────────────────────────────────
print("3) extra.json — letnice, viri postaj, oznake 'v raziskovanju', MVG-114")
extra = load("src/data/museum/extra.json")
src_of = {e["slug"]: e.get("sources") or [] for e in exhibits["exhibits"]}

def find_source(slug, prefix):
    """Poišči vir matičnega zapisa po predponi imena (nič izmišljanja)."""
    for s in src_of.get(slug, []):
        if (s.get("nameSi") or "").startswith(prefix):
            return {"sourceName": s["nameSi"], "sourceUrl": s.get("url")}
    raise SystemExit(f"MANJKA VIR: {slug} → {prefix!r}")

def station(slug, year):
    hits = [st for st in extra[slug]["lifeStations"] if st.get("year") == year]
    assert len(hits) == 1, f"postaja {slug}/{year}: {len(hits)} zadetkov"
    return hits[0]

# 3a. griblje-vas: prva omemba 1468 (Griblach) — vir EN Wikipedija (MVG-001)
st = station("griblje-vas", "1526")
st["year"] = "1468"
st["description"] = (
    "V pisnih virih se vas prvič izpriča leta 1468 kot Griblach; sledita obliki "
    "Briglach (1490) in Griblah (1593), v urbarjih in na najstarejšem zemljevidu "
    "pa Grüble. (Slovenska Wikipedija v infopolju navaja omembo 1526 — to je "
    "leto prve omembe cerkve sv. Vida.)"
)
st["evidence"] = "dokumentirano"
st["sourceName"] = "Wikipedia (EN): Griblje — zgodovinska imena 1468–1593 (Griblach), etimologija po Snojevem slovarju"
st["sourceUrl"] = "https://en.wikipedia.org/wiki/Griblje"
st2 = station("griblje-vas", "1526 → 1991")
st2["year"] = "1468 → 1991"
print("  ✓ griblje-vas: nastanek 1468 (Griblach), obdobje 1468 → 1991")

# 3b. zaselki-griblje: 1526 → 1468, iskanje ločenih omemb izrecno
st = station("zaselki-griblje", "1526")
st["year"] = "1468"
st["description"] = (
    "Vas se v listinah prvič zapiše kot Griblach (1468); podoba večdelne vasi — "
    "Dolnje, Srednje in Gornje Griblje ter Brinsko selo — je izpričana v "
    "novoveških virih, ločene omembe posameznih zaselkov pa muzej še išče v arhivih."
)
st["evidence"] = "dokumentirano"
print("  ✓ zaselki-griblje: nastanek 1468")

# 3c. izpolnjeni viri — SAMO iz virov matičnih zapisov
FILLS = [
    # (slug, year, predpona vira matičnega zapisa, evidence ali None = pusti)
    ("sveti-vid", "danes", "Wikipedia (EN): Griblje (cerkev", "dokumentirano"),
    ("niko-zupanic", "danes", "Slovenski etnografski muzej: Niko Županič", "dokumentirano"),
    ("evakuacija-1945", "danes", "RTV Slovenija (2025)", "dokumentirano"),
    ("meja-1991", "1991 → danes", "Vaš kanal: Žičnata ograja", "dokumentirano"),
    ("belokranjska-hisa", "danes", "Slovenska etnografska literatura", "dokumentirano"),
    ("crni-moceril", "do 1986", "Wikipedija: črni močeril", "dokumentirano"),
    ("storklje", "vsako pomlad", "Wikipedija: bela štorklja", "dokumentirano"),
    ("storklje", "danes", "DOPPS — Ptice Slovenije", "dokumentirano"),
    ("jurjevanje", "spomladanski kult", "Wikipedija: Zeleni Jurij", "dokumentirano"),
    ("kresovanje", "do 19. stoletja", "Radio Odeon — Ljudje ob Kolpi: Matija Totter", "dokumentirano"),
    ("zvon-2008", "1526 → 2008", "Radio Odeon — V Gribljah slovesno obeležili 500-letnico", None),
    ("pisanice", "1893", "Bibliografija: Janko Barle", "dokumentirano"),
    ("srednje-njive", "2001", "Mason, P. (2001)", "dokumentirano"),
    ("etimologija-gribljati", "2001", "Bibliografija: Jože Šimec", "dokumentirano"),
    ("griblje-v-stevilkah", "2009", "Marko Snoj: Etimološki slovar", "dokumentirano"),
    ("krizevo-pastirski-dan", "1890-ta", "Dular, A. (1986)", "dokumentirano"),
    ("joze-dular", "1973", "Bibliografija: Jože Dular", "dokumentirano"),
    ("konrad-barle", "1933 → 2012", "Slovenska biografija — Barle, Konrad", "dokumentirano"),
    ("kucar-podzemelj", "pred 1914 → 1995", "Bibliografija: Janez Dular, »Podzemelj«", "dokumentirano"),
    ("kucar-podzemelj", "danes", "Wikipedija: Podzemelj", "dokumentirano"),
    ("ilirska-carina-1809", "1812", "Gašperič, P.", "dokumentirano"),
    ("dkz-griblje", "2012", "WorldCat: Gribeljski žbul", "dokumentirano"),
    ("peter-kambic", "danes", "Svet24: Podružnična šola Griblje", "dokumentirano"),
]
for slug, year, prefix, ev in FILLS:
    st = station(slug, year)
    src = find_source(slug, prefix)
    st["sourceName"] = src["sourceName"]
    st["sourceUrl"] = src["sourceUrl"]
    if ev:
        st["evidence"] = ev
    print(f"  ✓ vir dolozcen: {slug}/{year}")

# 3d. vse preostale postaje brez vira → jasna oznaka (uporabnikova zahteva)
marked = 0
for slug, story in extra.items():
    for st in story.get("lifeStations") or []:
        if not (st.get("sourceUrl") or st.get("sourceName")):
            if st.get("evidence") != "v raziskovanju":
                st["evidence"] = "v raziskovanju"
                marked += 1
print(f"  ✓ {marked} postaj označenih 'v raziskovanju'")

# 3e. odstrani zastareli related povezavi na MVG-114 (neobstoječi zapis)
removed = 0
for slug, story in extra.items():
    rel = story.get("related") or []
    keep = [r for r in rel if r.get("museumNo") != "MVG-114"]
    if len(keep) != len(rel):
        story["related"] = keep
        removed += len(rel) - len(keep)
assert removed == 2, f"pričakovani 2 odstranitvi MVG-114, bilo {removed}"
print("  ✓ 2 zastareli povezavi na MVG-114 odstranjeni")

save("src/data/museum/extra.json", extra)

# ────────────────────────────────────────────────────────────────────
# DOKUMENTACIJA STANJA
# ────────────────────────────────────────────────────────────────────
n_src = sum(1 for s in extra.values() for st in s.get("lifeStations") or []
            if st.get("sourceUrl") or st.get("sourceName"))
n_mark = sum(1 for s in extra.values() for st in s.get("lifeStations") or []
             if st.get("evidence") == "v raziskovanju")
n_mvg = sum(1 for s in extra.values() for r in s.get("related") or []
            if "MVG-" in (r.get("museumNo") or ""))
print(f"\nPOVZETEK: postaje z virom {n_src}, 'v raziskovanju' {n_mark}, "
      f"related brez MVG-114, dogodki 11, MVG-049 letnica 1468")
