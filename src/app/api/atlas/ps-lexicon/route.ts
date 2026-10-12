import { NextResponse } from "next/server";
import psLexicon from "@/data/atlas/ps-lexicon.json";

export const dynamic = "force-static";

/**
 * ISSUE #10 (P43) — PS 1825: neznane družine — prečni prehodi, PV območna
 * sprava in ledinsko-imenska struktura.
 *
 * 1) PREČNI PREHODI (samo znotraj iste fotografije — sken vsebuje ponovne
 *    posnetke, zato med-fotografske primerjave niso zanesljive): DINGF je
 *    edina 100 % stabilna neznana beseda (10/10 enakih branj do ločila);
 *    GENERIČNI PADCEK — pass1 prebere Wiese/Acker, kjer pass2 prebere
 *    specifično besedo: LHIZ 9/9 (Wiese→Lhize), ERDAR 5/5 (Acker→Achm),
 *    SCHINDEL 1/1 (Acker→Schindel) — specifične besede so V VIRU.
 * 2) BLOKOVSKA KONCENTRACIJA: 13/16 družin na ENI fotografiji s teki
 *    sosednjih parcel (AHN 906–920, AEFLING 1821–1840, EINHART 1644–1658 …)
 *    → hipoteza LEDINSKO IME (ime poljskega bloka), ne splošni termin.
 * 3) PV SPRAVA (uradni Nutzungs-Ausweis 10. 1. 1825, iz committed
 *    transkripcije PV.json): PV Area 1221|1513 ≈ P41 Area 1220|1493
 *    (Δ 0,05 %) ✓; VINOGRAD usklajen (Δ −0,46 J) ✓; WEIDEN-GAP 576,24 J
 *    (uradno 636,16 J pašnikov vs 59,92 J izrecnih Weide/Alm vrstic) —
 *    neznane družine pokrijejo le 96,68 J (17 %) vrzeli; NJIVA +202,29 J in
 *    TRAVNIK +182,12 J nad uradnima kategorijama; vrstični model 1564,78 J −
 *    Area 1221,95 J = 342,84 J ≈ Blatt X + NADALJEVANJE + WALDUNG (zunaj
 *    rekapitulacije) [~].
 * 4) LEKSIKOGRAFSKE HIPOTEZE (2 neodvisna LLM prehoda, committed raw
 *    ps-lexicon-raw/): izrecno HIPOTEZE z viri — viri navaja stroj in so
 *    NEPREVERJENI; rabe se NE prireja (vse ostaja NEKLASIFICIRANO).
 *
 * Status REVIEW — nič ne nadomešča človeške paleografske potrditve.
 * Dokaz: research/issue17/ps-lexicon.json (identičen izpis skripta).
 */
export async function GET() {
  return NextResponse.json(psLexicon, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
