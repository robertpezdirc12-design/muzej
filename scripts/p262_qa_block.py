#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — qa-p262 blok vstavljen za qa-p261 (po checkout-ab944b5)."""
ROOT = "/home/z/my-project"
P = f"{ROOT}/src/lib/qa-parish.ts"
src = open(P, encoding="utf-8").read()
if "qa-p262-parish-marriage-notranjost-01738-1837-1838" in src:
    print("[SKIP] qa-p262 že obstaja")
else:
    BLOCK = '''
  // ——— qa-p262: NOTRANJOST-01738 — 1837-NADALJEVANJE (m6–m12) → POROKE-1.-FEBRUAR-1838 + PROKLAMACIJE (P262) ———
  {
    const p262Errors: string[] = [];
    // živa kontrola: 4 bloki s18 (m6-h36 + m8-h63 + m8-h31 + m10-h17)
    const p262Live = HOUSE_VITALS.filter((v) => v.bookSignature === "01738" && v.scan === 18);
    if (p262Live.length !== 4) p262Errors.push(`bloki-s18 živo ≠ 4 (${p262Live.length})`);
    const p262Keys = p262Live.map((v) => `${v.houseNo}-${v.year}`).sort().join(",");
    if (p262Keys !== "17-1838,31-1838,36-1838,63-1838")
      p262Errors.push(`bloki-s18-ključi ≠ pričakovani (${p262Keys})`);
    const p262H17 = p262Live.find((v) => v.houseNo === "17");
    const p262H31 = p262Live.find((v) => v.houseNo === "31");
    const p262H36 = p262Live.find((v) => v.houseNo === "36");
    const p262H63 = p262Live.find((v) => v.houseNo === "63");
    if (!p262H17 || p262H17.year !== 1838 || p262H17.scan !== 18) p262Errors.push("h17-m10 ≠ 1838/s18 (DVIG-37-2.-NAJVEČJI-NOTRANJOSTI!)");
    if (!p262H31 || p262H31.year !== 1838 || p262H31.scan !== 18) p262Errors.push("h31-m8 ≠ 1838/s18 (DVIG-19!)");
    if (!p262H36 || p262H36.year !== 1838 || p262H36.scan !== 18) p262Errors.push("h36-m6 ≠ 1838/s18 (KRIŠAN-endogamija!)");
    if (!p262H63 || p262H63.year !== 1838 || p262H63.scan !== 18) p262Errors.push("h63-m8 ≠ 1838/s18 (4.-01738-blok!)");
    if (!p262H17?.whatSi.includes("KRAL")) p262Errors.push("h17-KRAL-nit ni označena!");
    if (!p262H63?.whatSi.includes("KRISCHAN")) p262Errors.push("h63-KRISCHAN-nit ni označena!");
    if (!p262H36?.whatSi.includes("endogamija")) p262Errors.push("h36-endogamija ni označena!");
    // živi dvigi 1:1 — firstYear iz korpusa (h17-1875→1838, h31-1857→1838)
    const firstYear262 = (house: string) => Math.min(...HOUSE_VITALS.filter((v) => v.houseNo === house).map((v) => v.year));
    for (const [hh, pri] of [["17", 1838], ["31", 1838]] as const) {
      if (firstYear262(hh) !== pri) p262Errors.push(`h${hh}-firstYear ≠ ${pri} (živo ${firstYear262(hh)})`);
    }
    // PREDHODNIK_1838_BLOCKS števci
    const B2 = PREDHODNIK_1838_BLOCKS;
    if (B2.noviBloki !== 4 || B2.vpisi !== 7) p262Errors.push("PREDHODNIK_1838_BLOCKS ≠ 4/7");
    if (B2.vitalsTotal !== 2081 || B2.byBook01738 !== 69) p262Errors.push(`PREDHODNIK_1838_BLOCKS ≠ 2081/69 (${B2.vitalsTotal}/${B2.byBook01738})`);
    for (const [key, frag] of [["h17", "37"], ["h31", "19"]] as const) {
      const d = B2.dvigi[key as "h17" | "h31"];
      if (!d || !d.includes(frag)) p262Errors.push(`dvig-${key} ≠ ${frag} (${d})`);
    }
    if (!B2.restartStruktura.includes("1.-FEBRUAR-1838")) p262Errors.push("restartStruktura: (D)-1.-FEBRUAR-1838 manjka!");
    if (!B2.restartStruktura.includes("MNOŽIČNI-DAN-×7")) p262Errors.push("restartStruktura: MNOŽIČNI-DAN-×7 manjka!");
    if (!B2.foliacija.includes("15/15")) p262Errors.push("foliacija: serija-15/15-notranjosti manjka!");
    if (!B2.krishanNit.includes("×4")) p262Errors.push("krishanNit: ×4 manjka!");
    if (!B2.noviPrimeki.includes("×9")) p262Errors.push("noviPrimeki: ×9 manjka!");
    if (!B2.urkunden1837.includes("3.-Februar-1837")) p262Errors.push("urkunden1837: m12-3.-Februar-1837 manjka!");
    // korpus živo
    if (HOUSE_VITALS.length !== 2081) p262Errors.push(`HOUSE_VITALS ≠ 2081 (${HOUSE_VITALS.length} — P262: +4!)`);
    const p262ByBook = HOUSE_VITALS.filter((v) => v.bookSignature === "01738").length;
    if (p262ByBook !== 69) p262Errors.push(`bloki-01738 ≠ 69 (${p262ByBook} — P262: +4!)`);
    if (Math.min(...HOUSE_VITALS.map((v) => v.year)) !== 1828) p262Errors.push("korpus-prvi-vpis ≠ 1828");
    // polni-dvojni živo (h63×h31 po (house, year) 1838)
    const p262Have = new Set(p262Live.map((v) => `${v.houseNo}-${v.year}`));
    for (const hh of ["63-1838", "31-1838"]) {
      if (!p262Have.has(hh)) p262Errors.push(`polni-dvojni-m8-${hh} manjka!`);
    }
    // ŠEST-knjižni klub živo: h17/h31 morata imeti 6 knjig v HOUSE_STORIES
    const h17Story = HOUSE_STORIES.find((s) => s.houseNo === "17");
    const h31Story = HOUSE_STORIES.find((s) => s.houseNo === "31");
    if (!h17Story || h17Story.books !== 6) p262Errors.push("h17-ŠEST-knjižna ≠ 6 (P262: 5→6!)");
    if (!h31Story || h31Story.books !== 6) p262Errors.push("h31-ŠEST-knjižna ≠ 6 (P262: 5→6!)");
    // niti + kraji
    if (!PREDHODNIK_262_NITI.si.includes("KRIŠAN-NIT-×4") || !PREDHODNIK_262_NITI.si.includes("NOVI-PRIMEKI-×9"))
      p262Errors.push("NITI-P262: KRIŠAN-×4 + NOVI-PRIMEKI-×9 manjkajo!");
    if (!PREDHODNIK_262_KRAJI.si.includes("VRANOVICH") || !PREDHODNIK_262_KRAJI.si.includes("OLOK") || !PREDHODNIK_262_KRAJI.si.includes("GRADAG"))
      p262Errors.push("KRAJI-P262: VRANOVICH + OLOK + GRADAG manjkajo!");
    push(
      "qa-p262-parish-marriage-notranjost-01738-1837-1838",
      "P262: ŽUPNIJA PODZEMELJ — NOTRANJOST-01738: 1837-NADALJEVANJE (m6–m12) → POROKE-1.-FEBRUAR-1838 + PROKLAMACIJE! (s18 = Pag. 33/34 — foliacija-serija-15/15-notranjosti-P259-10/10-+-P260-3/3-+-P261-1/1-+-P262-1/1!-s18-REZERVA-md5-1bb45fb3-2×-neodvisen-prenos-1:1-inventar-147-URL-1:1!-metoda-AGENT-VIZIJA-0-VLM-klicev-P259-predpis!-full-page-×1-+-margin-×1-+-slices-×6-+-row-kropsi-×14-+-cell-zoomi-×42-+-date-mega-×7-+-odločilni-mega-×14-≈83-izrezkov!): **★★★ STRUKTURNO-ODKRITJE-P262: GLAVNI-DATUM-×7-ALL-'1.-Februar'-d° = POROKE-1.-FEBRUAR-1838 (m6-pisni-'1. Februar'-m7–m12-'d°/tt°'-BREZ-leta-v-celici!-header-'1837'-pastoralno-leto-1837/38-Nov→Nov!) — zgornje-MALI-annotacije = PROKLAMACIJE: m6–m9-'1-Nov'-1837-×4 + m10–m12-'6-Nov'-1837-×3 (RESTART-(D)-1.-FEBRUAR-1838-4.-zaporedna-restart-struktura-A/B/C/D!-MNOŽIČNI-DAN-×7-VSI-VPISI-1-sam-dan!)** — 7-VPISOV (m6–m12-BREZ-preskokov!-margin-6–12-teče-1:1-iz-s17-m5!) — **★★★★★★ 4-GRIBLJE-BLOKOV-2-DVIGI-1-POLNI-DVOJNI: h17-1875→1838-ZA-37 (m10-nevesta-Maria-KRAL!-2.-NAJVEČJI-DVIG-NOTRANJOSTI-PO-h22-41-P255!-NOVA-01738-hiša!-ŠEST-KNJIŽNA-5→6!) + h31-1857→1838-ZA-19 (m8-nevesta-Anna-TILAH!-NOVA-01738-hiša!-ŠEST-KNJIŽNA-5→6!) + brez-dviga: h36-m6-nevesta-Anna-KRISCHAN (firstYear-1832-P258!) + h63-m8-ženin-Johann-KRISCHAN (4.-01738-blok!-firstYear-1836!) — POLNI-DVOJNI-m8-h63×h31-ALL-GRABLJE!** — **★★★★★★ KRIŠAN-NIT-×4 (m6-ženin-Georg-KRISCHAN-×-nevesta-Anna-KRISCHAN-h36-ist-priimek-ENDOGAMIJA!-+ m8-ženin-Johann-KRISCHAN-20-l-NAJMLAJŠI-01738-ženin-+ m8-oče-Georg-+ m12-mat-Maria!-↔-KRIŽAN-konglomerat-6-hiš!) + NOVI-PRIMEKI-×9 (TILAH + BILIZHIGH + KAJSHA-×2 + NAGEL + VIPSAUZ + PAPIGH + KRAL + SIMONIGH + HALZIGH!-+ BULVEG/ŠTAMPAHAR/HLEBEG/NOVAK/HORVATH!) + NOVE-VASI-×7-X-OPEN ('(Kris)ching-35' + 'HARVINJHA-11+5' + '(PREČRTAN)-31' + 'GERZHICH-33' + 'VRANOVICH-14+6'-1:1! + 'KREASING-22' + 'RUMPHANZ') + OLOK-2-3.-hiša + GRADAG-20-2.-vpis + URKUNDEN-1837-×7 (m12-'3.-Feb-1837'-dispens-prej!) + DUHOVNIKI-3-podpisnikov (Dolinšek-Coop.-IDEM!); korpus: vitals-2077→2081 + byBook-01738-65→69 + leta-1828–1838+1873 (11-let-notranjosti!) + ŠEST-knjižni-klub-39→41! [~X-OPEN: m6-dvovrstični-datum + annot-'Raja/Zunglau' + m8-priči-garbles]",
      "P262: THE PARISH OF PODZEMELJ — THE-01738-INTERIOR: THE-1837-CONTINUATION (m6–m12) → THE-MARRIAGES-FEB-1-1838 + THE-PROCLAMATIONS! (s18 = Pag. 33/34 — the-foliation-series-15/15-interior!-s18-RESERVE-md5-1:1!-THE-METHOD-AGENT-VISION-0-VLM-calls!-≈83-crops!): **★★★ THE-STRUCTURAL-DISCOVERY-P262: THE-MAIN-DATE-×7-ALL-'Feb 1'-d° = THE-MARRIAGES-FEB-1-1838 (the-annotations-above = the-PROCLAMATIONS: m6–m9-'Nov 1'-1837-×4 + m10–m12-'Nov 6'-1837-×3!-the-RESTART-(D)-FEB-1-1838-the-4th-consecutive-restart-structure!-the-MASS-DAY-×7-ALL-7-entries-1-single-day!)** — 7-ENTRIES (m6–m12-NO-SKIPS!) — **★★★★★★ 4-GRIBLJE-BLOCKS-2-LIFTS-1-FULL-DOUBLE: h17-1875→1838-BY-37 (the-2ND-LARGEST-INTERIOR-LIFT!-SIX-BOOK-5→6!) + h31-1857→1838-BY-19 (SIX-BOOK-5→6!) + h36-+ h63-no-lift — THE-FULL-DOUBLE-m8-h63×h31-ALL-GRABLJE!** — **★★★★★★ THE-KRIŠAN-THREAD-×4 (the-m6-endogamy-Georg-×-Anna!-+ the-m8-groom-Johann-20-THE-YOUNGEST!) + THE-NEW-SURNAMES-×9 + THE-NEW-VILLAGES-×7-X-OPEN + OLOK-2 + GRADAG-20 + the-URKUNDEN-1837-×7 + THE-PRIESTS-3-signers!; the corpus: 2077→2081 + the-01738-book-65→69 + the-years-1828–1838+1873 (11-years-interior!) + the-six-book-club-39→41!",
      p262Errors.length === 0,
      p262Errors.length === 0
        ? `notranjost-01738-1837/1838: 7-vpisov (m6–m12-ALL-1.-Februar-1838-d°!-PROKLAMACIJE-1-Nov-×4-+-6-Nov-×3!) · 4-bloki-[17-1838,31-1838,36-1838,63-1838] (1-POLNI-DVOJNI-h63×h31-ALL-GRABLJE!) · ★★★★★ h17-DVIG-37-KRAL!-h31-DVIG-19-TILAH!-ŠEST-KNJIŽNI-5→6-×2! · KRIŠAN-×4-endogamija-m6! · NOVI-PRIMEKI-×9! · NOVE-VASI-×7-VRANOVICH-1:1! · foliacija-15/15! · 2081-vitalov/69-01738/leta-1828–1838+1873/klub-41!`
        : p262Errors.join("; "),
    );
  }
'''
    # vstavi za qa-p261 blokom (najdi konec qa-p261 push = ';\\n  }\\n' pred 'qa-p246')
    anchor = src.find("  // ——— qa-p246: POROČNA PREDZGOVINA 04455 — leto 1878 = 8/13 (P246) ———")
    if anchor == -1:
        raise SystemExit("[FAIL] anchor qa-p246 ni najden!")
    src = src[:anchor] + BLOCK + "\n" + src[anchor:]
    open(P, "w", encoding="utf-8").write(src)
    print("[OK] qa-p262 blok vstavljen")
