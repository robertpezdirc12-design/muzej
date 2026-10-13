import { NextResponse } from "next/server";
import neatlineGeoref from "@/data/atlas/neatline-georef.json";

export const dynamic = "force-static";

/**
 * ISSUE #14 / §3 AUDITA (P46) — NEATLINE GEOREFERENCIRANJE SEKCIJ dg/cg/ch
 * (listi A03–A05) — nadgradnja GRID_APPROX (±200–400 m) na neatline sidro.
 *
 * PRINCIP (determinističen, brez AI ob delovanju): franciscejski sekciji list
 * je narisany z NEATLINE natanko na meji sekcije katastrske mreže eZKN
 * 1:2880. Uradna geometrija celic (VKIX24*, GURS eZKN, EPSG:4326) je znana →
 * preslikava px ↔ WGS84 brez prostih parametrov.
 *
 * KALIBRACIJA PRINCIPA: kontrola na listu A02 (sekcija cf) pod GEOTRUTH
 * afino (EŠD 2122 + Kolpa, model.ts georef-a02): detektirani neatline N
 * (y≈97) in E (x≈2710) padata na uradni meji celice cf z residualoma 9 in
 * 13 m.
 *
 * REZULTATI:
 * - A04 (cg): vse 4 strani detektirane → merilo sx=0.7765, sy=0.7727 m/px
 *   (medosna konsistenca 0,5 %) + afina 4 vogalov na uradne kote celice
 *   (RMS 0,1 m) → NEATLINE_GEOREFERENCED, ±40 m.
 * - A05 (ch): vse 4 strani (N/W šibkejše pokritosti) → 4-vogalna afina →
 *   NEATLINE_GEOREFERENCED, ±40 m.
 * - A03 (dg): detektirani S in E, N/W implicitno preko skupnega merila
 *   (šibki kandidati potrjujeta v okviru 25 m) →
 *   NEATLINE_PARTIAL_GEOREFERENCED, ±50 m.
 *
 * NE-REGRESIJA: 7/7 P10 kontrolnih napisov na novih afineh — TRIBUTSCH →
 * znotraj k.o. Tribuče, WEIDENDORF (A03 in A04) → znotraj k.o. Bedenj,
 * ADLESCHITZ → izven modernega k.o. Griblje, Bresnik 34 m, Fučkovci 33 m,
 * Pri Jankovichti 33 m od P10 tarč (prej znos ±200–400 m).
 *
 * Premik novih mej vs P10 GRID_APPROX (celična bbox): le 17–18 m —
 * popravek konvergencije mreže, ne premik legе.
 *
 * Status: ANALYSIS-DETERMINISTIC — predlog nadgradnje; človeška potrditev
 * neatline črt + GURS overlay prikaz ostaja odprta. SHEET_GEOREFS v model.ts
 * se NAMERNO ne spreminja (lekcija P9: brez človeške potrditve ne objavljamo
 * nadgradenj statusa).
 *
 * Dokaz: research/issue17/neatline-georef.json (identičen izpis skripta
 * scripts/p46_neatline_georef.py; invarianti I1–I7).
 */
export async function GET() {
  return NextResponse.json(neatlineGeoref, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
