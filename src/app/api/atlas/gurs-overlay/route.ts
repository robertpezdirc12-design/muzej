import { NextResponse } from "next/server";
import gursOverlay from "@/data/atlas/gurs-overlay.json";

export const dynamic = "force-static";

/**
 * ISSUE #14 / §3 AUDITA (P47) — GURS PARCEL OVERLAY: neodvisna validacija
 * P46 neatline afin (A03–A05).
 *
 * PRINCIP (determinističen, brez AI ob delovanju): sodobne katastrske parcele
 * (GURS eZKN WFS, poligoni EPSG:3794 → WGS84) preslikane skozi P46 neatline
 * afine morajo pasti na narisane črte franciscejskega katastra 1825.
 *
 * METRIKI: (a) pokritost črnila oboda parcel (plus-oblika 3×3 temno, prag
 * 195) pri brez zamika in pri najboljšem zamiku ±12 px; (b) residual
 * registracije (razdalja najboljšega zamika). Kontrole: isti obodi, zamaknjeni
 * 100/200/400 px v 8 smeri. Strata: DRAWN (lokalna gostota temnega ≥ 0.06) /
 * EMPTY (v 1825 nenarisano — WAIDENDORF skupna paša, gozd).
 *
 * REZULTATI (mediana residuala, DRAWN stratum):
 * - A03 (dg): 9.8 m (p90 13.2) — 112 DRAWN parcel
 * - A04 (cg): 5.6 m (p90 10.2) — 498 DRAWN parcel
 * - A05 (ch): 9.3 m (p90 13.1) — 165 DRAWN + 394 EMPTY (WAIDENDORF)
 * - A02 (cf, GEOTRUTH kontrola metode): 9.8 m — skladno z ±40–80 m
 *
 * To je neodvisna validacija z ZUNANJIM virom (GURS eZKN): sodobna parcelna
 * mreža se registrira na risbo 1825 z mediano 6–10 m — znotraj neatline
 * negotovosti ±40–50 m, daleč pod staro GRID_APPROX ±200–400 m.
 *
 * Status: ANALYSIS-DETERMINISTIC — človeška potrditev neatline črt prek
 * izrezov (research/issue17/neatline-crops/, 16 dokaznih slik) ostaja pogoj
 * za nadgradnjo SHEET_GEOREFS (lekcija P9).
 *
 * Dokaz: research/issue17/gurs-overlay.json (identičen izpis skripta
 * scripts/p47_gurs_overlay.py; invarianti I1–I7).
 */
export async function GET() {
  return NextResponse.json(gursOverlay, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
