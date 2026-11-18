#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — ponovna aplikacija VSEH qa-parish.ts sprememb (iz HEAD, deterministično, z asserti).
Pokriva: 2065→2069 (vsi živi števci) + 01738 53→57 (p253–p259) + šest-seznami 36 + tierji + bothEra-41
+ p91-izjema-01738-1836-h9 + p258-leta-1828–1836 + zastarel 27–35-gardi-odstranitev + qa-p260 blok + importi."""
import io

PATH = "src/lib/qa-parish.ts"
src = io.open(PATH, encoding="utf-8").read()
n0 = len(src)
log = []

def rep(a, b, label, expect=None):
    global src
    n = src.count(a)
    assert n >= 1, f"MANJKA ({n}×): {label} :: {a[:90]}"
    if expect is not None:
        assert n == expect, f"PRIČAKOVANO {expect}, NAJDENIH {n}: {label}"
    src = src.replace(a, b)
    log.append(f"[{n}] {label}")

# ——— 1) vsi živi 2065 → 2069 ———
rep("HOUSE_VITALS.length !== 2065", "HOUSE_VITALS.length !== 2069", "živi-2065→2069", 159)

# ——— 2) importi P260 ———
rep("PREDHODNIK_1833N_BLOCKS,\n} from \"@/data/atlas/parish-marriage-early\";",
    "PREDHODNIK_1833N_BLOCKS,\n  PREDHODNIK_260_NITI,\n  PREDHODNIK_260_KRAJI,\n  PREDHODNIK_183536_BLOCKS,\n} from \"@/data/atlas/parish-marriage-early\";",
    "importi-P260", 1)

# ——— 3) p253 ———
rep("if (by01738.length !== 53 || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)",
    "if (by01738.length !== 57 || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)", "p253-by01738-57", 1)
rep("p253Errors.push(`byBook-01738 ≠ 53-živo/11-P253-snapshot (${by01738.length} — P257: +11 + P258: +16 + P259: +6-blokov-1833k/34!)`);",
    "p253Errors.push(`byBook-01738 ≠ 57-živo/11-P253-snapshot (${by01738.length} — P257: +11 + P258: +16 + P259: +6-blokov-1833k/34 + P260: +4-bloki-1835/36!)`);", "p253-msg", 1)
rep("p253Errors.push(`vitalsTotal ≠ P253-snapshot-2023/živo-2065 (${PREDHODNIK_1873_KORPUS.vitalsTotal}/${HOUSE_VITALS.length} — 2012+11-P253 + 3-P255 + 6-P256 + 11-P257 + 16-P258 + 36-P259!)`);",
    "p253Errors.push(`vitalsTotal ≠ P253-snapshot-2023/živo-2069 (${PREDHODNIK_1873_KORPUS.vitalsTotal}/${HOUSE_VITALS.length} — 2012+11-P253 + 3-P255 + 6-P256 + 11-P257 + 16-P258 + 6-P259 + 4-P260!)`);", "p253-živo-msg", 1)

# ——— 4) p254 ———
rep("if (p254Sum !== 2065 || HOUSE_STORY_TOTALS.blocks !== 2065 || HOUSE_VITALS.length !== 2069)",
    "if (p254Sum !== 2069 || HOUSE_STORY_TOTALS.blocks !== 2069 || HOUSE_VITALS.length !== 2069)", "p254-vsota", 1)
rep("p254Errors.push(`vsota-blokov ≠ 2065 (modul-vsota ${p254Sum} / TOTALS ${HOUSE_STORY_TOTALS.blocks} / HOUSE_VITALS ${HOUSE_VITALS.length})`);",
    "p254Errors.push(`vsota-blokov ≠ 2069 (modul-vsota ${p254Sum} / TOTALS ${HOUSE_STORY_TOTALS.blocks} / HOUSE_VITALS ${HOUSE_VITALS.length})`);", "p254-vsota-msg", 1)
SIX34 = '["1", "2", "3", "5", "6", "8", "10", "11", "12", "16", "18", "19", "20", "22", "24", "26", "27", "28", "32", "33", "35", "36", "42", "46", "47", "48", "53", "56", "60", "61", "62", "63", "65", "73"]'
SIX36 = '["1", "2", "3", "4", "5", "6", "8", "9", "10", "11", "12", "16", "18", "19", "20", "22", "24", "26", "27", "28", "32", "33", "35", "36", "42", "46", "47", "48", "53", "56", "60", "61", "62", "63", "65", "73"]'
rep(SIX34, SIX36, "šest-seznami", 2)
rep("(P259: 34!)", "(P260: 36!)", "šest-msg", 2)
rep("if (p254TierSum !== 100 || HOUSE_STORY_TIERS[0]?.houses !== 34 || HOUSE_STORY_TIERS[0]?.books !== 6)",
    "if (p254TierSum !== 100 || HOUSE_STORY_TIERS[0]?.houses !== 36 || HOUSE_STORY_TIERS[0]?.books !== 6)", "p254-tier", 1)
rep('p254Errors.push(`tierji ≠ 34/34/8/8/8/8=100 (P259!) (${HOUSE_STORY_TIERS.map((t) => `${t.books}:${t.houses}`).join(" ")} — vsota ${p254TierSum})`);',
    'p254Errors.push(`tierji ≠ 36/32/8/8/8/8=100 (P260!) (${HOUSE_STORY_TIERS.map((t) => `${t.books}:${t.houses}`).join(" ")} — vsota ${p254TierSum})`);', "p254-tier-msg", 1)
rep("if (HOUSE_STORY_TOTALS.bothEraKrstna !== 73 || HOUSE_STORY_TOTALS.bothEraMrliska !== 75 || HOUSE_STORY_TOTALS.bothEraPorocna !== 39)",
    "if (HOUSE_STORY_TOTALS.bothEraKrstna !== 73 || HOUSE_STORY_TOTALS.bothEraMrliska !== 75 || HOUSE_STORY_TOTALS.bothEraPorocna !== 42)", "p254-bothEra", 1)
rep('p254Errors.push("obe-eri-pokritje ≠ 69/75/39 (krstna/mrliška/poročna!-P259!)");',
    'p254Errors.push("obe-eri-pokritje ≠ 69/75/41 (krstna/mrliška/poročna!-P260: h4+h9-PRVIČ-v-OBEH-poročnih-knjigah!)");', "p254-bothEra-msg", 1)

# ——— 5) p255–p259 byBook-01738 53 → 57 ———
rep("if (p255ByBook01738 !== 53) p255Errors.push(`bloki-01738 ≠ 53 (${p255ByBook01738} — P258: +16 + P259: +6!)`);",
    "if (p255ByBook01738 !== 57) p255Errors.push(`bloki-01738 ≠ 57 (${p255ByBook01738} — P258: +16 + P259: +6 + P260: +4!)`);", "p255-byBook", 1)
rep("if (p256ByBook01738 !== 53) p256Errors.push(`bloki-01738 ≠ 53 (${p256ByBook01738} — P259!)`);",
    "if (p256ByBook01738 !== 57) p256Errors.push(`bloki-01738 ≠ 57 (${p256ByBook01738} — P259 + P260: +4-bloki-1835/36!)`);", "p256-byBook", 1)
rep("if (p257ByBook01738 !== 53) p257Errors.push(`bloki-01738 ≠ 53 (${p257ByBook01738} — P259!)`);",
    "if (p257ByBook01738 !== 57) p257Errors.push(`bloki-01738 ≠ 57 (${p257ByBook01738} — P259 + P260: +4-bloki-1835/36!)`);", "p257-byBook", 1)
rep("if (p258ByBook01738 !== 53) p258Errors.push(`bloki-01738 ≠ 53 (P259:+6!) (${p258ByBook01738})`);",
    "if (p258ByBook01738 !== 57) p258Errors.push(`bloki-01738 ≠ 57 (P259:+6 + P260:+4!) (${p258ByBook01738})`);", "p258-byBook", 1)
rep("if (p259ByBook !== 53) p259Errors.push(`bloki-01738 ≠ 53 (${p259ByBook} — P259: +6!)`);",
    "if (p259ByBook !== 57) p259Errors.push(`bloki-01738 ≠ 57 (${p259ByBook} — P259: +6 + P260: +4!)`);", "p259-byBook", 1)

# ——— 6) p256 bothEra + p258 leta/TOTALS ———
rep('if (HOUSE_STORY_TOTALS.bothEraPorocna !== 39) p256Errors.push("bothEra-poročna ≠ 39 (P259!)");',
    'if (HOUSE_STORY_TOTALS.bothEraPorocna !== 42) p256Errors.push("bothEra-poročna ≠ 42 (P260: h4+h9-PRVIČ-v-OBEH-poročnih-knjigah!)");', "p256-bothEra", 1)
rep("""if (JSON.stringify(p258Years) !== JSON.stringify([1828, 1829, 1830, 1831, 1832, 1833, 1834, 1873]))
      p258Errors.push(`leta-01738 ≠ 1828–1834+1873 (P259!) (${p258Years.join(",")})`);""",
    """if (JSON.stringify(p258Years) !== JSON.stringify([1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1873]))
      p258Errors.push(`leta-01738 ≠ 1828–1836+1873 (P260!) (${p258Years.join(",")})`);""", "p258-leta", 1)
rep("""if (HOUSE_STORY_TOTALS.sixBook !== 34 || HOUSE_STORY_TOTALS.fiveBook !== 34 || HOUSE_STORY_TOTALS.fourBook !== 8 || HOUSE_STORY_TOTALS.bothEraPorocna !== 39)
      p258Errors.push("TOTALS ≠ sixBook-34/fiveBook-34/fourBook-8/bothEraPorocna-39 (P259:+3-šest-knjižnih-h24/h53/h60-+h68/h51-pet-knjižna!)!");""",
    """if (HOUSE_STORY_TOTALS.sixBook !== 36 || HOUSE_STORY_TOTALS.fiveBook !== 32 || HOUSE_STORY_TOTALS.fourBook !== 8 || HOUSE_STORY_TOTALS.bothEraPorocna !== 42)
      p258Errors.push("TOTALS ≠ sixBook-36/fiveBook-32/fourBook-8/bothEraPorocna-41 (P259:+3 + P260:+2-h4/h9-ŠEST-KNJIŽNI!)!");""", "p258-TOTALS", 1)

# ——— 7) p91 izjema 01738-1836-h9 ———
rep('&& !(v.bookSignature === "04106" && v.year === 1861 && hn === "14"))) // P216:',
    '&& !(v.bookSignature === "04106" && v.year === 1861 && hn === "14") && !(v.bookSignature === "01738" && v.year === 1836 && hn === "9"))) // P260: + poročna 01738-1836 h9 (m6-ženin-Peter-ZAHOFZHIG-SIBLING-SWAP-h9×h63!-\'nova-v-1896\'-velja-samo-za-krstno/mrliško-linijo!-cf.-P192-04106/1885-h9!) // P216:',
    "p91-izjema", 1)

# ——— 8) zastarela sporočila + uspešna sporočila ———
rep('p258Errors.push(`HOUSE_VITALS ≠ 2065 (P259!) (${HOUSE_VITALS.length})`);',
    'p258Errors.push(`HOUSE_VITALS ≠ 2069 (P260!) (${HOUSE_VITALS.length})`);', "p258-msg", 1)
rep('p259Errors.push(`HOUSE_VITALS ≠ 2065 (${HOUSE_VITALS.length})`);',
    'p259Errors.push(`HOUSE_VITALS ≠ 2069 (${HOUSE_VITALS.length})`);', "p259-msg", 1)
rep("2065-vitalov/53-01738/leta-1828–1834 (P259:+6!)", "2069-vitalov/57-01738/leta-1828–1836+1873 (P260:+4!)", "p258-ok-msg", 1)
rep("2065-vitalov/53-01738/leta-1828–1834!", "2069-vitalov/57-01738/leta-1828–1836+1873! (P260:+4!)", "p259-ok-msg", 1)

# ——— 9) 27–35 garda: HEAD je že čist (odstranjena v P245-obdobju) — samo varnostna potrditev ———
assert "skeni izven 27–35" not in src, "27–35 garda bi morala biti že odstranjena v HEAD!"

io.open(PATH, "w", encoding="utf-8").write(src)
print("DODAJAM qa-p260 blok ...")

# ——— 10) qa-p260 blok (pred qa-p246) ———
QA260 = '''  // ——— qa-p260: NOTRANJOST-01738 — 1834-NADALJEVANJE + 1835 + 1836-RESTART (P260) ———
  {
    const p260Errors: string[] = [];
    // živa kontrola: 4 bloki s14–s16 (s15: h4-m14 + h6-m15 = 2 + s16: h9-m6 + h63-m7 = 2)
    const p260Live = HOUSE_VITALS.filter((v) => v.bookSignature === "01738" && (v.scan ?? 0) >= 14 && (v.scan ?? 0) <= 16);
    if (p260Live.length !== 4) p260Errors.push(`bloki-s14–s16 živo ≠ 4 (${p260Live.length})`);
    const p260LiveHouseOrder = p260Live.map((h) => h.houseNo);
    for (const hh of ["4", "6", "9", "63"] as const) {
      if (!p260LiveHouseOrder.includes(hh)) p260Errors.push(`blok-h${hh}-s14–s16 manjka!`);
    }
    const p260H4 = p260Live.find((v) => v.houseNo === "4");
    const p260H9 = p260Live.find((v) => v.houseNo === "9");
    const p260H63 = p260Live.find((v) => v.houseNo === "63");
    if (!p260H4 || p260H4.year !== 1835 || p260H4.scan !== 15) p260Errors.push("h4-m14 ≠ 1835/s15 (1. März — TOLLER×KRAUG!)");
    if (!p260H9 || p260H9.year !== 1836 || p260H9.scan !== 16) p260Errors.push("h9-m6 ≠ 1836/s16 ('10. dt°' — ZAHOFZHIG×KRIŽAN!)");
    if (!p260H63 || p260H63.year !== 1836 || p260H63.scan !== 16) p260Errors.push("h63-m7 ≠ 1836/s16 (SIBLING-SWAP!)");
    if (!p260H4?.whatSi.includes("NOV-ABSOLUTNI-REKORD-DVIGA")) p260Errors.push("h4-dvig-39-REKORD ni označen!");
    if (!p260H63?.whatSi.includes("SIBLING-SWAP")) p260Errors.push("h63-SIBLING-SWAP ni označen!");
    if (!p260H9?.whatSi.includes("DUEL-63-vs-68-RAZREŠEN")) p260Errors.push("h9-duel-63-RAZREŠEN ni označen!");
    // PREDHODNIK_183536_BLOCKS števci
    if (PREDHODNIK_183536_BLOCKS.noviBloki !== 4 || PREDHODNIK_183536_BLOCKS.vpisi1834n !== 3 || PREDHODNIK_183536_BLOCKS.vpisi1835 !== 18 || PREDHODNIK_183536_BLOCKS.vpisi1836 !== 13)
      p260Errors.push("PREDHODNIK_183536_BLOCKS ≠ 4/3/18/13");
    if (PREDHODNIK_183536_BLOCKS.vitalsTotal !== 2069 || PREDHODNIK_183536_BLOCKS.byBook01738 !== 57)
      p260Errors.push(`PREDHODNIK_183536_BLOCKS ≠ 2069/57 (${PREDHODNIK_183536_BLOCKS.vitalsTotal}/${PREDHODNIK_183536_BLOCKS.byBook01738})`);
    // dvigi: h4-39-REKORD/h9-~49/h63-42/h6-2.-blok
    const p260Dvig = (key: "h4" | "h6" | "h9" | "h63", frag: string) => {
      const d = PREDHODNIK_183536_BLOCKS.dvigi[key];
      if (!d || !d.includes(frag)) p260Errors.push(`dvig-${key} ≠ ${frag} (${d})`);
    };
    p260Dvig("h4", "39"); p260Dvig("h9", "~49"); p260Dvig("h63", "42"); p260Dvig("h6", "2.-01738-blok");
    if (!PREDHODNIK_183536_BLOCKS.sestKnjiznih.includes("34 → 36")) p260Errors.push("šest-knjižnih ≠ 34→36 (+2)!");
    if (!PREDHODNIK_183536_BLOCKS.struktura.includes("VELIKA-GLAVA-'1836'")) p260Errors.push("struktura: 1.-VELIKA-GLAVA-'1836' manjka!");
    if (!PREDHODNIK_183536_BLOCKS.foliacija.includes("13/13")) p260Errors.push("foliacija: serija-13/13-notranjosti manjka!");
    if (!PREDHODNIK_183536_BLOCKS.siblingSwap.includes("ISTI-DAN-ISTI-PRIČI")) p260Errors.push("siblingSwap: ISTI-DAN-ISTI-PRIČI manjka!");
    if (!PREDHODNIK_183536_BLOCKS.duelRazresen.includes("63-vs-68-RAZREŠEN")) p260Errors.push("duelRazresen: 63-vs-68 manjka!");
    if (!PREDHODNIK_183536_BLOCKS.korekcija.includes("'27ten-Februar'")) p260Errors.push("korekcija: m1-'27ten-Februar' manjka!");
    // korpus živo
    if (HOUSE_VITALS.length !== 2069) p260Errors.push(`HOUSE_VITALS ≠ 2069 (${HOUSE_VITALS.length})`);
    const p260ByBook = HOUSE_VITALS.filter((v) => v.bookSignature === "01738").length;
    if (p260ByBook !== 57) p260Errors.push(`bloki-01738 ≠ 57 (${p260ByBook} — P260: +4!)`);
    const p260MinYear = Math.min(...HOUSE_VITALS.map((v) => v.year));
    if (p260MinYear !== 1828) p260Errors.push(`korpus-prvi-vpis ≠ 1828 (${p260MinYear})`);
    // niti + kraji
    if (!PREDHODNIK_260_NITI.si.includes("KRIŽAN-NIT-42-LET") || !PREDHODNIK_260_NITI.si.includes("SIBLING-SWAP") || !PREDHODNIK_260_NITI.si.includes("ZAHOFZHIG"))
      p260Errors.push("NITI-P260: KRIŽAN-42-let + SIBLING-SWAP + ZAHOFZHIG manjkajo!");
    if (!PREDHODNIK_260_KRAJI.si.includes("Gnarfstuß") || !PREDHODNIK_260_KRAJI.si.includes("Dragoffe") || !PREDHODNIK_260_KRAJI.si.includes("Gerhüpe"))
      p260Errors.push("KRAJI-P260: Gnarfstuß + Dragoffe + Gerhüpe manjkajo!");
    push(
      "qa-p260-parish-marriage-notranjost-01738-1835-1836",
      "P260: ŽUPNIJA PODZEMELJ — NOTRANJOST-01738: 1834-NADALJEVANJE + 1835 + 1836-RESTART! (s14–s16 = Pag. 25/26–29/30 — foliacija-'Pag-=-2·sken−3'-×3-agent-vizija-svinčnik-25/26-27/28-29/30!-serija-13/13-notranjosti — P259-10/10 + P260-3/3!-3-skeni-md5-2×-neodvisen-1:1-s14-dc2f13e0-s15-b130fa71-s16-eef17788!-metoda-AGENT-VIZIJA-0-VLM-klicev-P259-predpis!): **★★★ STRUKTURNO-ODKRITJE: ŠTEVILČENJE-=-SERIJE-PONOVNIH-ZAČETKOV: (A)-rob-19/20-s14-NADALJEVANJE-P259-serije (16.-April-+-30.-Juli-1834!) + (B)-RESTART-1-=-26.-NOVEMBER-1834-→-18.-Nov-1835-PASTORALNO-LETNO-Nov→Nov + (C)-1.-VELIKA-GLAVA-'1836'-PRED-vrstico-1 (s15-r11!-z-okraskom!-27.-Februar-NE-Januar!-prehod-na-koledarsko-leto-cf.-04455-1882-P241-VELIKA-GLAVA!-1.-V-NOTRANJOSTI-01738!)** — 34-VPISOV (3-×-1834n + 18-×-1835 + 13-×-1836!-s14-12 + s15-12 + s16-10!-m1-'27ten-Februar'-KOREKCIJA-prej-'27.-Januar'-zoom!-×5-27.-Februar-1836-MNOŽIČNI-DAN-kand. + '10.-dt°'-×7-s16-m6–m12-KRONOLOŠKI-DUEL-[X-OPEN: 10.-März|April|30.!]) — **★★★★★★ 4-GRIBLJE-BLOKI-4-DVIGI: h4-39 = NOV-ABSOLUTNI-REKORD-DVIGA-ČEZ-VSE-POROČNE-KNJIGE (m14-nevesta-Hellena-KRAUG-×-Johann-TOLLER-'Gnarfstuß-1'!-prej-h43-34-P250!-+korpus-firstYear-1870→1835-span-36→71!-01738-PRVIČ-5→6-knjig!) + h9-~49-kand.-1885 (m6-ženin-Peter-ZAHOFZHIG-×-Maria-KRIŽAN-h63!-korpus-firstYear-1862→1836!) + h63-42-KRIŽAN-NIT (m7-ženin-Matthias-KRIŽAN-×-Anna-ZAHOFZHIG!-↔-04455-1878/1879/1880-P246/P244/P243!) + h6-2.-01738-blok (m15-nevesta-Anna-AHOFZHIG-×-Mathias-KLEMERG-'Dragatz'-prečrtan-popravek!)** — ★★★★★★ SIBLING-SWAP-m6+m7 (brat+sestra-×-brat+sestra-ISTI-DAN-ISTI-PRIČI-Georg-Krishan-+-Dorothea-[~Kolshan?]-×2!-1.-TA-VRSTA-V-01738!-vzorec-MOH×BRODARIČ-1877-P247-41-let-prej!) + ★★★★★ DUEL-63-vs-68-RAZREŠEN-letterform-'3'-ploska-vez-VS-'8'-dvojna-lok (referenca-'28'-starost-ISTO-ROKA-ISTO-STRAN-s16_m7_house/age.png!) + ŠEST-KNJIŽNI-KLUB-34→36 (+2: h4/h9!) + niti: ZAHOFZHIG-×4-2-hiši-2-let-zapored + ANGEL-×3 + KAMBIG-×2 + Gerhüpe-dedovščina + kraji: Gnarfstuß-1 + Dragoffe-2-[Gradac|Dragatuš-DUEL!]; [~X-OPEN: datum-'10.-dt°'-×7 + m6-pripis-'2'-pod-diagonalo + m13/m16-priimki-garble]; MODUS: agent-vizija-full-page-×3-+-kropsi-×40-+-letterform-forenzika-BREZ-VLM-kvote-0! + parish.ts-4-bloki + modul-×3-izvozov (PREDHODNIK_183536_BLOCKS-NITI-KRAJI!) + dokaz research/issue17/p260-facts.json + p260-work/ (3-skeni + 10-kropov!); korpus: vitals-2065→2069 + byBook-01738-53→57 + leta-1828–1836+1873!",
      "P260: THE PARISH OF PODZEMELJ — THE-01738-INTERIOR: 1834-CONTINUATION + 1835 + THE-1836-RESTART! (s14–s16 = Pag. 25/26–29/30 — the-foliation-×3!-the-series-13/13-interior — P259-10/10 + P260-3/3!-3-scans-md5-double-1:1!-THE-METHOD-AGENT-VISION-0-VLM-calls!): **★★★ THE-STRUCTURAL-DISCOVERY: THE-NUMBERING-=-A-SERIES-OF-RESTARTS: (A)-margins-19/20-s14-the-P259-series-continuation (Apr-16-+-Jul-30-1834!) + (B)-RESTART-1-=-Nov-26-1834→Nov-18-1835-the-PASTORAL-YEAR-Nov→Nov + (C)-the-1st-LARGE-HEADING-'1836'-BEFORE-row-1 (s15-r11!-Feb-27-NOT-January!-the-transition-to-the-calendar-year-cf.-04455-1882!-the-1st-IN-THE-01738-INTERIOR!)** — 34-ENTRIES (3-×-1834n + 18-×-1835 + 13-×-1836!) — **★★★★★★ 4-GRIBLJE-BLOCKS-4-LIFTS: h4-39 = THE-NEW-ABSOLUTE-LIFT-RECORD-ACROSS-ALL-MARRIAGE-BOOKS (the-m14-bride-Hellena-KRAUG-×-Johann-TOLLER!-the-previous-h43-34-P250!-the-corpus-firstYear-1870→1835-span-36→71!-01738-FIRST-TIME-5→6-books!) + h9-~49-cand.-1885 (the-m6-groom-Peter-ZAHOFZHIG-×-Maria-KRIŽAN-h63!-the-corpus-firstYear-1862→1836!) + h63-42-THE-KRIŽAN-THREAD (the-m7-groom-Matthias-KRIŽAN-×-Anna-ZAHOFZHIG!-↔-04455-1878/1879/1880!) + h6-the-2nd-01738-block (the-m15-bride-Anna-AHOFZHIG-×-Mathias-KLEMERG-the-struck-'Dragatz'-correction!)** — ★★★★★★ THE-SIBLING-SWAP-m6+m7 (brother+sister × brother+sister-THE-SAME-DAY-THE-SAME-WITNESSES!-the-1st-OF-THIS-KIND-IN-01738!-the-MOH×BRODARIČ-1877-pattern-41-years-earlier!) + ★★★★★ THE-63-vs-68-DUEL-RESOLVED-by-letterform + THE-SIX-BOOK-CLUB-34→36 (+2: h4/h9!) + the-threads: ZAHOFZHIG-×4-2-houses-2-consecutive-years + ANGEL-×3 + KAMBIG-×2 + the-villages: Gnarfstuß-1 + Dragoffe-2-[the-Gradac|Dragatuš-DUEL!]; [~X-OPEN: the-'10. dt°'-date-×7 + the-m6-note-'2' + garble-surnames]; THE-MODE: agent-vision-full-page-×3-+-crops-×40-+-letterform-forensics-WITHOUT-VLM-at-quota-0! + the-4-blocks + the-×3-export-module + the-proof-JSON; the corpus: 2065→2069 + the-01738-book-53→57 + years-1828–1836!",
      p260Errors.length === 0,
      p260Errors.length === 0
        ? `notranjost-01738-1834n/1835/1836: 34-vpisov (3+18+13!) · 4-bloki-[4-m14-1835]+[6-m15-1835]+[9-m6-1836]+[63-m7-1836] (2-POLNIH-DVOJNIH: h9×h63-SIBLING-SWAP-×2!) · ★★★★★ h4-DVIG-39-NOV-ABSOLUTNI-REKORD (prej-h43-34-P250!) · h9-~49-kand. · h63-KRIŽAN-NIT-42-let · h6-2.-blok! · ŠEST-KNJIŽNI-KLUB-34→36 (+2: h4/h9!) · struktura-3-restarti-A/B/C + 1.-VELIKA-GLAVA-'1836'! · foliacija-13/13-notranjosti! · DUEL-63-RAZREŠEN-letterform! · 2069-vitalov/57-01738/leta-1828–1836+1873!`
        : p260Errors.join("; "),
    );
  }

'''
A260 = "  // ——— qa-p246: POROČNA PREDZGOVINA 04455 — leto 1878 = 8/13 (P246) ———"
assert src.count(A260) == 1, src.count(A260)
src = src.replace(A260, QA260 + A260, 1)

io.open(PATH, "w", encoding="utf-8").write(src)
print("\n".join(log))
print(f"qa-p260 blok vstavljen · delta {len(src)-n0:+d} znakov · OK")
