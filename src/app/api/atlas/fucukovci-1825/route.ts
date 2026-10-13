import { NextResponse } from "next/server";
import fucukovci1825 from "@/data/atlas/fucukovci-1825.json";

export const dynamic = "force-static";

/**
 * ISSUE #14 / §3 AUDITA (P49) — FUČKOVCI 1825: MODERN-ANCHORED SYMBOL
 * EVIDENCE + STRIKTNA DETEKCIJA JEDER + OBSEG SKLOPA (delna vektorizacija A05).
 *
 * PRINCIP (determinističen, brez AI ob delovanju) — tri neodvisni dokazni sloji:
 *  1) MODERN-ANCHORED: 95 sodobnih stavb celice ch (GURS eZKN WFS) preslikanih
 *     prek P46 afine nazaj na sken; cov@best ≥ 0.5 na erodirani maski (plus 3×3,
 *     prag 195) = stavbno mesto 1825 z naslednikom (26; 25 v sklopu vasi);
 *  2) STRIKTNA DETEKCIJA JEDER: lokalni kontrast (mean9−mean25 ≤ −13) + delež
 *     zelo temnega (g<145 ≥ 0.55) + izključitev papirja + test obroča + oblika →
 *     53 temnih jeder; 7 koreliranih z on-symbol mesti, 19 neujemanih v sklopu
 *     z vizualno triažo (2 stavbe + 4 nejasni = GONE-kandidati [~], ostalo
 *     text/črta/drevo/številka);
 *  3) OBSEG SKLOPA: konveksna lupina 25 dokazanih mest (36 336 m², WGS84 ring v
 *     izpisu) + masa črnila (257 571 px, največja erodirana komponenta).
 *
 * KLJUČNI REZULTATI:
 * - pariteta s P48 (96 v celici / 95 evalviranih / 26 on-symbol), residual
 *   mediana 9.8 m
 * - P10 sidro iz geografske tarče prek afine: (1945, 637) — odmik 43 px od VLM
 *   branja (1975, 606); najbližje dokazano mesto 48.9 px ≈ 38 m (skladno s
 *   P46 "Fučkovci 33 m")
 * - ocena števila stavb: [27, 44] — P10 ocena ~45 znotraj mej, brez
 *   protislovja; razlika = odzivnost detektorja (hatchirani simboli se
 *   staknejo z gostoto vasi)
 * - DOKAZ O NEIZVEDLJIVOSTI celotne vektorizacije: rožnati parcelni fill
 *   (siva ~168.9) je pod pragom 195, erodirana maska se v vasi zasiči (40.3 %
 *   temnega), številke/črki/drevesa v istem kontrastnem razredu kot simboli —
 *   za razliko od A02 (P9: 156 tlorisov)
 * - kontinuiteta Fučkovci (spodnja meja) ≥ 0.806 [~] — jedro vasi je
 *   ohranjeno (pozitivno glede na P48: A02 razpršena zidanica 136/156 brez
 *   naslednika)
 *
 * Status: ANALYSIS-DETERMINISTIC. SHEET_GEOREFS in obstoječi dokazi P40–P48
 * nespremenjeni (lekcija P9).
 *
 * Dokaz: research/issue17/fucukovci-1825.json (identičen izpis skripta
 * scripts/p49_fucukovci1825.py; invarianti I1–I8) + 9 izrezov
 * research/issue17/fucukovci-crops/.
 */
export async function GET() {
  return NextResponse.json(fucukovci1825, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
