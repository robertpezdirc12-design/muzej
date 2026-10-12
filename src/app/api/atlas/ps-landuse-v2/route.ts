import { NextResponse } from "next/server";
import psLanduseV2 from "@/data/atlas/ps-landuse-v2.json";

export const dynamic = "force-static";

/**
 * ISSUE #10 (P42) — PS 1825: pravilnik rab v2 — deterministična razširitev
 * klasifikacije rab nad P39 model (parcela × raba), brez AI ob delovanju.
 * 12 v1 pravil nespremenjenih + 13 priloženih pravil (13–25, prvi zadetek =
 * primarni razred): umlaut Gärten, sredbesedni -wald/-weid, Wein, Öd/Wüst
 * družine, Schupfe, Maid = Mahd, Gemainde (Gmde/Gimand), Rüben/Schlagfeld …
 * Izrecna ločitev termType: KULTURA 2199 parov (83,5 %; v1 72,0 %) ·
 * TOPONIM 122 (ležajna imena, NI raba) · ARTIFAKT 29 (številke/registrične
 * opombe) · NEKLASIFICIRANO 282 (16 družin z so-odvisnostnimi dokazi —
 * Lhut-jedro 36, Lohn/Raut 29, Äfling 13 … — čaka paleografijo).
 * Pojasnjeno 89,3 % parov. V2 ⊇ V1 — noben v1 primarni razred ni spremenjen.
 * Status REVIEW — klasifikacija je za statistiko, surove vrednosti nedotaknjene.
 * Dokaz: research/issue17/ps-landuse-v2.json (identičen izpis skripta).
 */
export async function GET() {
  return NextResponse.json(psLanduseV2, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
