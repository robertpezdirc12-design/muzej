#!/usr/bin/env python3
# P254 generator: aggregates HOUSE_VITALS (2023) by house across 6 books
# and emits src/data/atlas/parish-house-stories.ts
import re
from collections import defaultdict

SRC = "src/data/atlas/parish.ts"
OUT = "src/data/atlas/parish-house-stories.ts"

src = open(SRC, encoding="utf-8").read()
m = re.search(r"export const HOUSE_VITALS: HouseVital\[\] = \[(.*?)\n\];', src", src, re.S) or \
    re.search(r'export const HOUSE_VITALS: HouseVital\[\] = \[(.*?)\n\];', src, re.S)
body = m.group(1)
pat = re.compile(r'houseNo:\s*"([^"]+)",\s*bookSignature:\s*"([^"]+)",\s*year:\s*(\d+)')
entries = pat.findall(body)
assert len(entries) == 2023, f"expected 2023, got {len(entries)}"

houses = defaultdict(lambda: defaultdict(list))
for h, b, y in entries:
    houses[h][b].append(int(y))

BOOKS = ["01738", "04104", "04105", "04455", "04106", "04894"]
book_meta = {
    "01738": ("poročna-predhodnik", "marriage predecessor", "1873", "h28 ×2 — dve družini (m2 Mavrin + m4 Tomc)"),
    "04104": ("krstna-predzgodovina", "baptism prehistory", "1871–1885", "h6 · h40 · h[?] (8 blokov vsak)"),
    "04105": ("krstna-linija", "baptism line", "1887–1919", "h24 (18 blokov!)"),
    "04455": ("poročna-linija + predzgodovina", "marriage line + prehistory", "1873–1922", "h27 SEGINA (8 blokov)"),
    "04106": ("mrliška-predzgodovina", "death prehistory", "1857–1885", "h13 · h65 (14 blokov vsak)"),
    "04894": ("mrliška-linija", "death line", "1886–1924", "h35 HRIŽAN (15 blokov!)"),
}

def kind_of(h):
    if h.isdigit():
        return "griblje" if 1 <= int(h) <= 78 else "druga-vas"
    return "neznano"

griblje = sorted([h for h in houses if kind_of(h) == "griblje"], key=int)
drugavas = sorted([h for h in houses if kind_of(h) == "druga-vas"], key=int)
neznano = ["13 [~]", "17 [~]", "32 [~]", "29 [~X-OPEN]", "[?]", "sub dioe."]
order = griblje + drugavas + neznano
assert set(order) == set(houses.keys()), sorted(set(order) ^ set(houses.keys()))

def entry(h):
    d = houses[h]
    tot = sum(len(v) for v in d.values())
    yrs = sorted(y for v in d.values() for y in v)
    per = ", ".join(f'{{ sig: "{b}", n: {len(d[b])} }}' for b in BOOKS if b in d)
    return (f'  {{ houseNo: "{h}", kind: "{kind_of(h)}", blocks: {tot}, books: {len(d)}, '
            f'perBook: [{per}], firstYear: {yrs[0]}, lastYear: {yrs[-1]}, span: {yrs[-1]-yrs[0]} }},')

lines = []
A = lines.append
A("// P254: HIŠNE ZGODBE GLOBJE — mreže hiš čez 6 knjig (P252-lead-② + P253-lead nadaljevanje; 2026-11-11)")
A("// SINTEZNA FAZA: NI NOVIH BRANJ, NI NOVIH SKENOV — agregacija celotnega korpusa HOUSE_VITALS (2023")
A("// vitalov) po hišah čez VSEH 6 knjig: 01738 (poročna-predhodnik 1873) + 04104 (krstna-predzgodovina")
A("// 1871–1885) + 04105 (krstna-linija 1887–1919) + 04455 (poročna 1873–1922) + 04106 (mrliška-")
A("// predzgodovina 1857–1885) + 04894 (mrliška-linija 1886–1924). 100 hišnih oznak = 78 Griblje (1–78)")
A("// + 16 druga-vas (79–98) + 6 neznanek ([?], sub dioe., 13/17/32 [~], 29 [~X-OPEN]).")
A("// ★★★ 9 ŠEST-KNJIŽ-HIŠ (blok v VSEH 6 knjigah!): 3, 10, 12, 16, 18, 20, 28, 63, 73 — isto 9 kot")
A("// 'polni življenjski cikel' (obe eri × vse 3 vrste). Dokaz: research/issue17/parish-house-stories.json;")
A("// verifikator: scripts/p254_house_stories.py --check (I1–I10).")
A("")
A("export interface HouseStory {")
A("  houseNo: string;")
A('  kind: "griblje" | "druga-vas" | "neznano";')
A("  /** skupno število vitalnih blokov hiše v korpusu */")
A("  blocks: number;")
A("  /** število različnih knjig s hišnim blokom (1–6) */")
A("  books: number;")
A("  perBook: { sig: string; n: number }[];")
A("  firstYear: number;")
A("  lastYear: number;")
A("  span: number;")
A("}")
A("")
A("export interface HouseStoryBookMeta {")
A("  sig: string;")
A("  roleSi: string;")
A("  roleEn: string;")
A("  years: string;")
A("  blocks: number;")
A("  houses: number;")
A("  recordSi: string;")
A("}")
A("")
A("export const HOUSE_STORY_BOOKS: HouseStoryBookMeta[] = [")
for b in BOOKS:
    roleSi, roleEn, years, rec = book_meta[b]
    n_blocks = sum(len(v) for d in houses.values() for bb, v in d.items() if bb == b)
    n_houses = sum(1 for d in houses.values() if b in d)
    A(f'  {{ sig: "{b}", roleSi: "{roleSi}", roleEn: "{roleEn}", years: "{years}", blocks: {n_blocks}, houses: {n_houses}, recordSi: "{rec}" }},')
A("];")
A("")
A("/** Vseh 100 hišnih oznak korpusa — Griblje (1–78) številsko, druga-vas (79–98), nato neznanke. */")
A("export const HOUSE_STORIES: HouseStory[] = [")
for h in order:
    A(entry(h))
A("];")
A("")
A("export function houseStoryByNo(no: string): HouseStory | undefined {")
A("  return HOUSE_STORIES.find((h) => h.houseNo === no);")
A("}")
A("")
A("export interface HouseStorySix {")
A("  houseNo: string;")
A("  blocks: number;")
A("  years: string;")
A("  storySi: string;")
A("  storyEn: string;")
A("}")
A("")
A("/** ★★★ 9 ŠEST-KNJIŽ-HIŠ — blok v VSEH 6 knjigah = polni življenjski cikel (krst+poroka+smrt × obe eri). */")
A("export const HOUSE_STORY_SIX: HouseStorySix[] = [")

six = {
 "3":  ("HRIŽAN/KRIŽAN-hiša: Peter Hrižan krstni oče 1872–1881 (4 krsti) + †1888 Peter Križar/Križan 80 let; 1864 Georg DRAGOŠ †70 (najstarejša omemba); m11-HLEBEC-1873 v predhodniku (P253!); 1907 PEZDIREC-poroka (h3 = 2. poročni dokaz).",
        "The HRIŽAN/KRIŽAN house: Peter Hrižan the baptismal father 1872–1881 (4 baptisms) + Peter Križan †1888 aged 80; Georg DRAGOŠ †70 in 1864 (the oldest mention); the m11-HLEBEC-1873 in the predecessor (P253!); a PEZDIREC marriage 1907."),
 "10": ("MUC-hiša: m6-1873 poroka neveste Muc — KOLBEZEN h16 × MUC h10 polni dvojni (P253!); KRAUE-h10 52-letna nevesta 1874 = NAJSTAREJŠA PREDZGODOVINE (P250!); 11 mrliških blokov 04106 (1857–1885) — med najglobljimi smrtnimi zgodovinami.",
        "The MUC house: the m6-1873 marriage of a Muc bride — KOLBEZEN h16 × MUC h10 the full double (P253!); the 52-year-old bride of 1874 = THE OLDEST OF THE PREHISTORY (P250!); 11 death blocks 04106 (1857–1885) — among the deepest death histories."),
 "12": ("DRAGOŠ-50-LET: 1869 Michael Dragos †27 → 1871 Joannes Dragoš krstni oče (z46!) → 1919 Franc DRAGOS poroka + Vincencij DRAGOS † — ISTA DRUŽINA 1869–1919! + PEZDIRC-continuum (z59-1872, P235!); 14 blokov v 04105 = 2.-največ v knjigi.",
        "The DRAGOŠ 50 YEARS: 1869 Michael Dragos †27 → 1871 Joannes Dragoš the baptismal father (z46!) → 1919 Franc DRAGOS marries + Vincencij DRAGOS † — THE SAME FAMILY 1869–1919! + the PEZDIRC continuum (z59-1872, P235!); 14 blocks in 04105 = the 2nd most of the book."),
 "16": ("KOLBEZEN-hiša: m6-1873 ženin Georg KOLBEZEN (h16 × h10 polni dvojni, P253!); 1918 Ana FILAK roj. NEMANIČ †75 (poročena 1879!); 1924 Alojzy NOVAK †27. 9. — zadnja leta mrliške linije (04894 se konča 31. 12. 1924, P190!).",
        "The KOLBEZEN house: the m6-1873 groom Georg KOLBEZEN (h16 × h10 the full double, P253!); Ana FILAK née NEMANIČ †75 in 1918 (married 1879!); Alojzy NOVAK †Sep 27 1924 — the final years of the death line (04894 ends Dec 31 1924, P190!)."),
 "18": ("ŠIMEC-hiša (P246-h18-ŠIMEC-1:1!): 1863 Georg Simic †53; 1878 dve INTRA-poroki v 1 letu (h18 × h65, P246!); 1921 Karolina PEZDIRC †1,3 (zadnji PEZDIRC-blok hiše); 36 blokov = najglasnejša šest-knjižna hiša.",
        "The ŠIMEC house (P246-h18-ŠIMEC-1:1!): Georg Simic †53 in 1863; two INTRA-marriages in one year 1878 (h18 × h65, P246!); Karolina PEZDIRC †1.3 in 1921 (the house's last PEZDIRC block); 36 blocks = the loudest six-book house."),
 "20": ("BORŠT-h20: z72/z73 DVOJČKI 1871 Georg + Catharina = 1. DVOJČKI KRSTNE LINIJE (P235!); 1869 Marko PEZDIRE †24 + 1859 [~Klara/Elena-Podire-garble]; 1919 Peter PEZDIRC poroka — PEZDIRC-nit čez 3 generacije (1859→1919 = 60 let!).",
        "The BORŠT h20: the z72/z73 TWINS 1871 Georg + Catharina = THE FIRST TWINS OF THE BAPTISM LINE (P235!); Marko PEZDIRE †24 in 1869 + the 1859 [~Klara/Elena-Podire garble]; Peter PEZDIRC marries 1919 — the PEZDIRC thread across 3 generations (1859→1919 = 60 years!)."),
 "28": ("DVE-DRUŽINI-HIŠA — edina z ×2 blokoma v 01738 (P253: m2-MAVRIN + m4-TOMC!): 1871 Pezdirc (z81) + Požek (z83) krstni (P235-h28-dve-družini!); 1916/1917 Ana + Anton PEZDIREC — poročena 30. 1. 1861, Anton †78 let = 56-LETNA ZAKONSKA ZVEZA!",
        "THE TWO-FAMILY HOUSE — the only one with ×2 blocks in 01738 (P253: m2-MAVRIN + m4-TOMC!): 1871 Pezdirc (z81) + Požek (z83) baptisms (P235-h28-two-families!); 1916/1917 Ana + Anton PEZDIREC — married Jan 30 1861, Anton †78 = A 56-YEAR MARRIAGE!"),
 "63": ("KRIŽAN-HIŠA (korpus-uradno: 'h63 = KRIŽAN-hiša'!): Križan/Hrižan-continuum 1862–1921 (9+ blokov); m1-KURE-29. 1. 1873 = PRVI VPIS PREDHODNIKA (P253-RESTART-1!); tri poroke Križan 1911/1912/1921; PEZDIRC-mati ×4 (1881–1896).",
        "THE KRIŽAN HOUSE (officially in the corpus: 'h63 = KRIŽAN-hiša'!): the Križan/Hrižan continuum 1862–1921 (9+ blocks); the m1-KURE-Jan 29 1873 = THE FIRST ENTRY OF THE PREDECESSOR (the P253 RESTART-1!); three Križan marriages 1911/1912/1921; the PEZDIRC mother ×4 (1881–1896)."),
 "73": ("★ TIHA-HIŠA — samo 9 blokov v 6 knjigah (1–2 na knjigo, najtišja šest-knjižna — naslednja h3 ima 23!): m12-KUPAMIČ-1873 s pisarjevim popravkom '13'→'73' (P253!); Županič/Lupanič/Lepančič-garble-continuum 1869–1921; PEZDIRC-mati ×4 (Pezdire/Pegdire/Pozdirec/Pegdirec — 4 grafije!).",
        "★ THE QUIET HOUSE — only 9 blocks in 6 books (1–2 per book, the quietest six-book house — the next, h3, has 23!): the m12-KUPAMIČ-1873 with the scribe's correction '13'→'73' (P253!); the Županič/Lupanič/Lepančič garble continuum 1869–1921; the PEZDIRC mother ×4 (four spellings!)."),
}
for h in ["3", "10", "12", "16", "18", "20", "28", "63", "73"]:
    d = houses[h]
    yrs = sorted(y for v in d.values() for y in v)
    tot = sum(len(v) for v in d.values())
    si, en = six[h]
    A(f'  {{ houseNo: "{h}", blocks: {tot}, years: "{yrs[0]}–{yrs[-1]}", storySi: "{si}", storyEn: "{en}" }},')
A("];")
A("")
A("export interface HouseStoryTier {")
A("  books: number;")
A("  houses: number;")
A("  labelSi: string;")
A("}")
A("")
A("/** Pokritje po številu knjig: 9/53/14/8/8/8 = 100. */")
A("export const HOUSE_STORY_TIERS: HouseStoryTier[] = [")
tiers = {6: 9, 5: 53, 4: 14, 3: 8, 2: 8, 1: 8}
labels = {6: "šešt-knjižne (polni cikel!)", 5: "pet-knjižne", 4: "štiri-knjižne", 3: "tri-knjižne", 2: "dvo-knjižne", 1: "eno-knjižne"}
for k in [6, 5, 4, 3, 2, 1]:
    A(f'  {{ books: {k}, houses: {tiers[k]}, labelSi: "{labels[k]}" }},')
A("];")
A("")
A("export const HOUSE_STORY_TOTALS = {")
A("  houses: 100,")
A("  griblje: 78,")
A("  drugaVas: 16,")
A("  neznano: 6,")
A("  blocks: 2023,")
A("  sixBook: 9,")
A("  fiveBook: 53,")
A("  fourBook: 14,")
A("  bothEraKrstna: 69,")
A("  bothEraPorocna: 10,")
A("  bothEraMrliska: 75,")
A('  loudest: "24",')
A("  loudestBlocks: 45,")
A('  quietest6: "73",')
A("  quietest6Blocks: 9,")
A("  longestSpan: 66,")
A('  longestSpanHouses: ["2", "13", "50", "60", "64"],')
A('  deathsGap: "25",')
A("} as const;")
A("")
A("export interface HouseStoryNotable {")
A("  id: string;")
A("  titleSi: string;")
A("  titleEn: string;")
A("  bodySi: string;")
A("  bodyEn: string;")
A("}")
A("")
A("/** Osamelci, rekordi in vrzeli mreže — 7 zgodb. */")
A("export const HOUSE_STORY_NOTABLES: HouseStoryNotable[] = [")
notables = [
 ("najglasnejsa", "h24 = najglasnejša hiša korpusa",
  "The h24 = the loudest house of the corpus",
  "45 blokov (1859–1920) — 18 v 04105 = REKORD KRSTNE LINIJE; a samo 5 knjig: 01738 (leto 1873) je nima — h24 v predhodniku ne poroči nihče. 8 blokov tudi v 04104.",
  "45 blocks (1859–1920) — 18 in 04105 = THE BAPTISM LINE RECORD; but only 5 books: nobody of h24 marries in the 01738 predecessor. Also 8 blocks in 04104."),
 ("h65", "h65 = 43 blokov, rekord mrliške predzgodovine",
  "The h65 = 43 blocks, the death-prehistory record",
  "43 blokov (1857–1914); 14 v 04106 = REKORD skupaj s h13; MILEK-družina (P218/P220/P224/P246 — 4 viri!); 11 blokov v 04105. Najgloblja smrtna zgodovina med pet-knjižnimi.",
  "43 blocks (1857–1914); 14 in 04106 = THE RECORD together with h13; the MILEK family (4 sources!); 11 blocks in 04105. The deepest death history among the five-book houses."),
 ("h35", "h35 = rekord mrliške linije 04894",
  "The h35 = the death-line 04894 record",
  "15 blokov v 04894 (1886–1924) = NAJVEČ V ENI KNJIGI med vsemi hišami; HRIŽAN-družina (P229!). Skupaj 24 blokov 1857–1922.",
  "15 blocks in 04894 (1886–1924) = THE MOST IN ONE BOOK of all houses; the HRIŽAN family (P229!). Altogether 24 blocks 1857–1922."),
 ("h27", "h27 = rekord poročne knjige 04455",
  "The h27 = the marriage-book 04455 record",
  "8 blokov v 04455 = REKORD POROČNE (SEGINA-hiša: 1875 + 1881 + 1882 + 1884 + …); Jacob-63-l-×-Anna-HRIŽAN-1875 (P250). Skupaj 30 blokov 1857–1922.",
  "8 blocks in 04455 = THE MARRIAGE RECORD (the SEGINA house: 1875 + 1881 + 1882 + 1884 + …); Jacob-63-y-o × Anna HRIŽAN 1875 (P250). Altogether 30 blocks 1857–1922."),
 ("smrtna-vrzeli", "h25 = SMRTNA VRZEL 29 let",
  "The h25 = A 29-YEAR DEATH GAP",
  "5 knjig a BREZ 04106: noben mrliški zapis 1857–1885 (29 let!) kljub krstnim blokom 1876 + 1883 ×2 in poroki v 01738 (m3-kandidat, P253!). Šele 04894 prinese 7 blokov (1888–1923) — mrežna luknja, ne stvarna.",
  "5 books but WITHOUT 04106: no death record 1857–1885 (29 years!) despite the baptism blocks 1876 + 1883 ×2 and a marriage in 01738 (the m3 candidate, P253!). Only 04894 brings 7 blocks (1888–1923) — a network hole, not a real one."),
 ("razponi-66", "5 hiš z 66-letnim razponom",
  "5 houses with a 66-year span",
  "h2, h13, h50, h60, h64 — vsaka dokumentirana 1857/58 → 1923/24 (66 let!): od prve strani mrliške predzgodovine do zadnjega leta mrliške linije. Najdaljše kontinuitete korpusa.",
  "h2, h13, h50, h60, h64 — each documented 1857/58 → 1923/24 (66 years!): from the first page of the death prehistory to the last year of the death line. The longest continuities of the corpus."),
 ("skrita-hisa", "h[?] = skrita hiša brez številke",
  "The h[?] = the hidden house without a number",
  "10 blokov 1857–1885 (8 v 04104 + 2 v 04106) z izpraznjeno hišno celico — edina hiša korpusa brez številke; P235/P220 X-OPEN. V kasnejših knjigah izgine (razrešena številka?).",
  "10 blocks 1857–1885 (8 in 04104 + 2 in 04106) with an emptied house cell — the only corpus house without a number; P235/P220 X-OPEN. It vanishes in the later books (a resolved number?)."),
]
for nid, tsi, ten, bsi, ben in notables:
    A(f'  {{ id: "{nid}", titleSi: "{tsi}", titleEn: "{ten}", bodySi: "{bsi}", bodyEn: "{ben}" }},')
A("];")

open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"OK: wrote {OUT}: {len(lines)} lines, {len(order)} houses")
print("tiers:", tiers, "sum:", sum(tiers.values()))
