import { NextResponse } from "next/server";
import psParcelsGeo from "@/data/atlas/ps-parcels-geo.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P55 v2 @ P58) — GEOLOKACIJA GRUNDPARCELLEN: PS PROTOKOL 1825 ↔ SODOBNE
 * PARCELE KO 1544 — SANIRANA PRODUKCIJA.
 *
 * PS = »Protocol der Grund-Parcellen der Gemeinde GRÜBLE« (N083PS, 143 strani):
 * 2505 Grundparzellen + 102 Bauplätze = 2607 vrstic — lastniki, rabe, površine,
 * a brez geometrije. P55 protokol prvič geolocira; P58 (v2) produkcijo SANIRA:
 *  · −43 lažnih povezav S3 (str. 138–139, zapadek z lastnim oštevilčenjem
 *    1–100; P56 dokaz: površine ~42× od 1 QK + pass-razhajanje) — nabor
 *    bajtno enak P56 kontaminacijskemu seznamu;
 *  · +26 vrstic Blatt I (str. 3–4, številke 1–36) iz primarnega vira P57
 *    (štiri neodvisne VLM plasti) — točno vseh 26 lostBases P56;
 *  · rezultat: 1093 vrstic / 800 pozicioniranih števil; serije BI/S1/S2;
 *  · površine median 3.7709 ≈ 1 Wiener QK 3.59665 m² (Δ +4.85 % — v1 3.6984
 *    je bil umetno snizan z lažnimi povezavami; kontrola 4.0829);
 *  · soslednost NEINVARIANTNA — 590 parov / 51.8 m / 27.8× bajtno enako v1
 *    (pozicije per base, množica pozicioniranih števil 800 nespremenjena);
 *  · zaupanje STRONG 174 / MEDIUM 759 / WEAK 160 (S1/S2 bajtno enako v1);
 *  · odkritje: »Furkofze« (Fučkovci) = 2 vrstici, parceli 2159/2160,
 *    lastnik Van Wawech Mihó — prvi imenovani Fučkovci v arhivu.
 *
 * Status: SANITIZED-DETERMINISTIC. SHEET_GEOREFS in dokazi P40–P57
 * nespremenjeni; v1 dokaz arhiviran (research/issue17/ps-parcels-geo.json).
 *
 * Dokaz v2: research/issue17/ps-parcels-geo-v2.json (izpis skripta
 * scripts/p58_ps_parcels_geo_v2.py; invarianti I1–I9, `--check` = determinizem).
 * Runtime: src/data/atlas/ps-parcels-geo.json (version 2).
 */
export async function GET() {
  return NextResponse.json(psParcelsGeo, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
