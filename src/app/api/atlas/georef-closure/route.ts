import { NextResponse } from "next/server";
import georefClosure from "@/data/atlas/georef-closure.json";

export const dynamic = "force-static";

/**
 * ISSUE #14 / §3 AUDITA (P50) — GEOREF ZAPORA A03–A05: AKTIVACIJA P46 NEATLINE AFIN.
 *
 * Lekcija P9 zahteva več plasti neodvisnih dokazov pred spremembo objavljene lege.
 * P50 šteje plasti, ki VSE merijo isto P46 afino:
 *  L0  P46 neatline  — narisane neatline črte = uradne meje celic eZKN 1:2880
 *                      (kalibrirano na A02 pod GEOTRUTH afino: residuala 9.3/13.2 m)
 *  L1  P47 parcele   — mediana residuala 9.8/5.6/9.3 m (A03/A04/A05), p90 ≤ 13.2 m
 *  L2  P48 stavbe    — A02 149/154 on-symbol (9.8 m), A05 26/95 (10.1 m)
 *  L3  P49 Fučkovci  — sidro 43.2 px od VLM branja; najbližje mesto 48.9 px ≈ 38 m
 *  L4  P10 napisi    — 7/7 kontrolnih napisov pade v prave k.o. pod afinami
 *
 * REZULTAT: SHEET_GEOREFS A03–A05 nadgrajeni iz GRID_APPROX (±200–400 m, REVIEW) na
 * P46 neatline meje: A03 NEATLINE_PARTIAL_GEOREFERENCED ±50 m (S/E detektirana,
 * N/W inferred preko s̄), A04/A05 NEATLINE_GEOREFERENCED ±40 m (4/4 strani).
 * Premik mej vs P10 le 17.4/16.9/18.0 m (konvergencija mreže); merilo popravljeno
 * 0.72/0.73 → 0.7746 m/px. Pogoj iz P46/P47 (človeška potrditev črt) izpolnjen s
 * plastmi L1–L4; vizualni pregled izrezov ostaja priporočen [~].
 *
 * Status: ACTIVATED-DETERMINISTIC. SHEET_GEOREFS A01/A02 (GEOTRUTH) nespremenjena.
 *
 * Dokaz: research/issue17/georef-closure.json (identičen izpis skripta
 * scripts/p50_georef_closure.py; invarianti I1–I10) + sheetGeorefsPatch
 * (navzkrižno povezan z model.ts prek qa-p50).
 */
export async function GET() {
  return NextResponse.json(georefClosure, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
