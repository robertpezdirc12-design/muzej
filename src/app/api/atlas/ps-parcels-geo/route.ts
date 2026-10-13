import { NextResponse } from "next/server";
import psParcelsGeo from "@/data/atlas/ps-parcels-geo.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P55) — GEOLOKACIJA GRUNDPARCELLEN: PS PROTOKOL 1825 ↔ SODOBNE PARCELE KO 1544.
 *
 * PS = »Protocol der Grund-Parcellen der Gemeinde GRÜBLE« (N083PS, 143 strani):
 * 2505 Grundparzellen + 102 Bauplätze = 2607 vrstic — lastniki, rabe, površine,
 * a brez geometrije. P55 protokol prvič geolocira:
 *  · povezava po parcelni številki na sodobne parcele k.o. 1544 (P47 prenos);
 *    delitve po 1825 = base + pripona (površine delov seštejte);
 *  · vztrajnost oštevilčenja dokazana z dvema neodvisnima testoma:
 *    (A) površine — median modern/QK 3.6984 ≈ 1 Wiener QK 3.59665 m²
 *        (Δ +2.83 %; premešana kontrola 3.9731, pas ±10 % 16.9 % vs 4.0 %);
 *    (B) prostorska soslednost (odločilni) — zaporedne številke 51.8 m narazen
 *        (kontrola 1436.9 m — 27.8×); 89.3 % parov ≤ 150 m (kontrola 2.5 %);
 *  · zaupanje vrstic: STRONG 171 / MEDIUM 775 / WEAK 164 — per-parcelno [~];
 *  · odkritje: »Furkofze« (Fučkovci) = 2 vrstici, parceli 2159/2160,
 *    lastnik Van Wawech Mihó — prvi imenovani Fučkovci v arhivu.
 *
 * Status: DISCOVERED-DETERMINISTIC. SHEET_GEOREFS in dokazi P40–P54
 * nespremenjeni.
 *
 * Dokaz: research/issue17/ps-parcels-geo.json (celoten izpis skripta
 * scripts/p55_ps_parcels_geo.py; invarianti I1–I8, `--check` = determinizem).
 * Runtime: src/data/atlas/ps-parcels-geo.json (samo povezane vrstice).
 */
export async function GET() {
  return NextResponse.json(psParcelsGeo, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
