import { NextResponse } from "next/server";
import psRegisterTopology from "@/data/atlas/ps-register-topology.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P56) — TOPOLOGIJA REGISTRA PS: SERIJE, SPREMEMBE 1805–1934, SANACIJA P55.
 *
 * Register PS NI homogen — P56 razčleni topologijo v štiri serije (vse
 * deterministično iz committed artefaktov):
 *  · S1 glavni register (str. 5–127, 123 strani): per-Blatt številčenje,
 *    Grund ≈ 1–2505 (številke 1–40 = strani 3–4 NISO v P38 izboru branj);
 *  · S2 spremembni register (str. 128–137): številke 2507–2840 kot prebrano,
 *    dodatki/spremembe z anmerkung (»einf. Vermessung vom Jahr 1805, bezogen
 *    vom Hof Nr 1003«, »hinzugekommen 1841«, »Grundsteuerkataster 1841«);
 *  · S3 zapadek »Zusammenstellung der Grundstücke« (str. 138–139): LASTNO
 *    oštevilčenje 1–100, pass2/pass3 razhajanje [1..40] vs [421..440];
 *  · S4 rekapitulacija + »Abschluß der Gemeinde« (str. 140–143, izven joina).
 *
 * SANACIJA P55: 43 S3 vrstic je bilo lažno povezanih (median razmerja
 * površin 0.0892 ≪ 3.7188 v S1 — ~42× odmik od 1 Wiener QK = 3.59665 m²) —
 * sanitiran join: 1110 → 1067 vrstic, 800 → 774 base (izgubljene 1–40 območje,
 * ker strani 3–4 niso prebrane). P55 runtime se NE spreminja (pini qa-p55).
 *
 * PER-BLATT DVOUMNOST kvantificirana: 515 base številk na več straneh
 * (475 znotraj S1); 529 povezanih vrstic dvoumnih (512 na sanitiranem joinu)
 * — brez prerazporeditev (blatt stolpec ~50 % šumen).
 *
 * SODOBNA PRAZNINA: 0 parcel 2507–2607 v k.o. 1544 (87 PS dodatkov brez
 * naslednic) proti 53 base / 78 parcelam 2608–2700 — vzrok [~].
 *
 * ČASOVNICA: 584 označenih vrstic (anmerkung), letnice 1515–1934, pik 1841
 * (83 vrstic na 44 straneh — prehod na Franziszeischer Kataster).
 *
 * Status: ANALYSIS-DETERMINISTIC. SHEET_GEOREFS in dokazi P40–P55
 * nespremenjeni; P55 runtime (ps-parcels-geo.json) nespremenjen.
 *
 * Dokaz: research/issue17/ps-register-topology.json (celoten izpis skripta
 * scripts/p56_ps_register_topology.py; invarianti I1–I8, `--check` =
 * determinizem). Runtime: src/data/atlas/ps-register-topology.json (kompakt).
 */
export async function GET() {
  return NextResponse.json(psRegisterTopology, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
