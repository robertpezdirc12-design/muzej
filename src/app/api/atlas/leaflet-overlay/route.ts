import { NextResponse } from "next/server";
import leafletOverlay from "@/data/atlas/leaflet-overlay.json";

export const dynamic = "force-static";

/**
 * ISSUE #14 / §3 AUDITA (P51) — LEAFLET OVERLAY A03–A05: AKTIVACIJA SLIKOVNIH PREKRIVK.
 *
 * P50 je izpisal boundsImageNWSE (oglišča skena prek P46 afine) »za prihodnji
 * Leaflet overlay« — P51 ga aktivira v atlasnem UI:
 *  · ovoj skena NEODVISNO preračunan iz P46 afine (NW = affine(0,0),
 *    SE = affine(W,H); pixels iz model.ts prek regexa) == P50 boundsImageNWSE
 *    ≤ 5e-6° — ni ročno prepisanih koordinat;
 *  · MERJENA SUBTELNOST pošteno dokumentirana: Leaflet ne podpira rotiranih
 *    prekrivk — slika je razpete v osno poravnan okvir; odmik vogalov izmerjen
 *    iz členov afine (lng |b|·H, lat |d|·W): A03 19.3 m, A04 20.0 m, A05 20.0 m
 *    (dva vogala točna) — del ±40/50 m negotovosti lista, zapisan per sheet
 *    (overlayDeviationM); skew 0.5475/0.568/0.5708° ≤ 1.0°;
 *  · slike preverjene: PIL dims == model.ts + sha256;
 *  · UI: stikala privzeto IZKLOPLJENA — začetni pogled nespremenjen;
 *    črtkani neatline okvirji s statusom; skupna prosojnost.
 *
 * Status: UI-ACTIVATED-DETERMINISTIC. SHEET_GEOREFS in dokazi P40–P50
 * nespremenjeni.
 *
 * Dokaz: research/issue17/leaflet-overlay.json (identičen izpis skripta
 * scripts/p51_leaflet_overlay.py; invarianti I1–I8, `--check` = determinizem).
 */
export async function GET() {
  return NextResponse.json(leafletOverlay, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
