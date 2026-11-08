import { NextResponse } from "next/server";
import psK1K2 from "@/data/atlas/ps-k1k2.json";

export const dynamic = "force-static";

/**
 * ISSUE #10 (P44) — PS 1825: RAZCEP K1/K2 v "Abschluß der Gemeinde"
 * (str. 140 desno, rdeči tuš) — RAZREŠEN [~].
 *
 * PROBLEM (P41 §21 UNRESOLVED): vrstici Grundparzellen (nach Anlage) 831|K1
 * in Zinsb./Ziffer 1041 383|K2 se seštejeta v 1215|490; ker je 831+383 = 1214
 * J, mora biti K1+K2 = 2090 K. VLM branja (K1: 968/468/9?8; K2: 1288/1388)
 * niso zadostila omejitve — noben par branj ni vsota 2090.
 *
 * REŠITEV P44 (deterministična, brez AI ob delovanju):
 * 1. STRUKTURNA PARALELNOST "nach Anlage": desna vrstica 4 (Baup 3|312) je
 *    identična levi vrstici 132 (3|312) — P41 identiteta PASS. Po istem
 *    vzorcu mora desna vrstica 1 (Grund 831|K1) rekapitulirati levo "Summa
 *    der Grundparzellen" 831|702 (Joch 831 == 831) → K1 = 702.
 * 2. Hipoteza (968, 1122) pade z podmnožinskim argumentom: 831|968 bi
 *    presegla vsoto Anlage 831|702 pri istem Joch — nemogoče.
 * 3. K2 = 2090 − 702 = 1388 == DIREKTNO VLM branje pass2 (p1/p3 bereta 1288,
 *    razlika le v 2. števki).
 * 4. Celoten Abschluß se zapre: 831|702 + 383|1388 = 1215|490;
 *    + 5|1003 = 1220|1493 (Area der Gemeinde); 3|312 + 2|691 = 5|1003.
 *
 * Struktura občine: Grundparzellen 1215|490 = rustikalne hiše po Anlagi
 * 831|702 (hiše 124–130) + "Ziffer 1041" (Gütl/gingl.) 383|1388.
 *
 * Status: RESOLVED-ARITMETIČNO [~] — aritmetično vsiljeno z dvema
 * neodvisnima korelacijama; človeška paleografska potrditev ostaja odprta.
 * Dokaz: research/issue17/ps-k1k2.json (identičen izpis skripta
 * scripts/p44_ps_k1k2.py; invarianti I1–I7).
 */
export async function GET() {
  return NextResponse.json(psK1K2, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
