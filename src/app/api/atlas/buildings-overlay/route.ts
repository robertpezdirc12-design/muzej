import { NextResponse } from "next/server";
import buildingsOverlay from "@/data/atlas/buildings-overlay.json";

export const dynamic = "force-static";

/**
 * ISSUE #14 / §3 AUDITA (P48) — STAVBNI OVERLAY: GURS stavbe ↔ stavbna mesta
 * 1825 — most PUA↔PT↔PS↔GURS.
 *
 * PRINCIP (determinističen, brez AI ob delovanju): sodobni stavbni tlorisi
 * (GURS eZKN WFS SI.GURS.KN:STAVBE, OBRIS_GEOM, EPSG:3794 → WGS84) preslikani
 * prek GEOTRUTH meja A02 / P46 afin A03–A05 morajo pasti na narisane stavbne
 * simbole 1825. Merimo pokritost črnila notranjosti+oboda na ERODIRANI maski
 * (plus-oblika 3×3, prag 195 — tanke parcelne črte izginejo, polni simboli
 * ostanejo) pri brez zamika in pri najboljšem zamiku ±12 px; kontrole-zamiki
 * 100/200/400 px × 8 smeri; strata po pravilu P47.
 *
 * REZULTATI:
 * - A02 (cf): 154 evalviranih stavb, on-symbol 149/154 (cov@best mediana 1.0,
 *   DRAWN cov@0 0.85), residual mediana 9.8 m (p90 13.7 m; DRAWN stratum 9.9 m) — stavbna raven
 *   potrjuje parcelno raven P47 (9.8 m)
 * - A05 (ch, Fučkovci): on-symbol 26/95, residual 10.1 m — neodvisna potrditev
 *   P46 afine na stavbni ravni
 * - A04 (cg): on-symbol 0 — vse sodobne stavbe v celici so novejše od risbe
 *   (paša WEIDENDORF, skladno s P47 EMPTY stratum)
 * - Kontinuiteta A02: 37 parov tloris↔stavba (≤ 25 px, 36 strong), 113
 *   on-symbol brez vektorizacije, 136/156 tlorisov 1825 brez naslednika
 *   (razpršena zidanica — vinice/hambi na zahodnih pobočjih) — nadgradja
 *   P16 present.json (OSM 15/26/115) z uradnimi GURS obrisi
 * - Blatt X (str. 138–139): direktna referenca na register 1825 REFRIRANA
 *   (0/37 identičnih površin), površine vrstic (mediana 6.3 Joch) so red
 *   velikosti nad GRUND dvorišči (0.28 Joch) — kvantitativna opomba k
 *   interpretaciji P40/P42 "register stavbnih mest" (ostaja [~] do človeške
 *   paleografije)
 *
 * Status: ANALYSIS-DETERMINISTIC. SHEET_GEOREFS in obstoječi dokazi P40–P47
 * nespremenjeni (lekcija P9).
 *
 * Dokaz: research/issue17/buildings-overlay.json (identičen izpis skripta
 * scripts/p48_buildings_overlay.py; invarianti I1–I8) + 12 izrezov
 * research/issue17/buildings-crops/.
 */
export async function GET() {
  return NextResponse.json(buildingsOverlay, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
