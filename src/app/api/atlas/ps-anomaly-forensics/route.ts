import { NextResponse } from "next/server";
import psAnomalyForensics from "@/data/atlas/ps-anomaly-forensics.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P67) — FORENZIČNI PAKET ANOMALIJ.
 *
 * Štiri merjena dela (deterministično, brez AI ob delovanju; v2 join
 * NESPREMENJEN — disciplina P56–P66):
 *
 * • (A) SKOK II·IV (1603/1604) = ARTIFAKT DVOJNE KURRENT ZAMENJAVE:
 *   p78 (Blatt II, Wüstung "Pod Grabino") prave 1501–1520 (strip 2×
 *   bajtno, vrstice 5–14 rdeče prečrtane, kontinuiteta 1461→1520,
 *   karta 1461–1500 = 12 poligonov / 1121–1200 PRAZNO) → v2 1603–1605
 *   napaka 5→6, prave 1503/1504/1505; p93 (Blatt IV) prave 1901–1920
 *   (strip 2× r11–20 bajtno; karta blok 1901–1907 = TOČNO 7 poligonov;
 *   P38 pass1 9→0, pass2 9→6) → prave 1903/1904/1905; p87 (Blatt II)
 *   prave 1681–1700 (pass2 + oči; pass1 661–680 = izguba vodilne 1 +
 *   8→6) → 11 v2 vrstic napačno (+1020) z LAŽNO geometrijo (== p36
 *   koordinate). Posledica: 1603/1604/1605/661/671 = lažne fuzije —
 *   skok II·IV IZGINE, čez-Blatt primera 661/671 RAZPADETA; p93 (IV) ×
 *   p98 (III) = isti obseg 1901–1920 (disjunktni lastniki). RENUMERI-
 *   FIKACIJA 17 preslikav, 0 kolizij = P68; projekcija: base 802,
 *   multi-page 208, čez-Blatt 107.
 * • (B) 5 SOSLEDJE FLAGOV (646, 661, 1821, 2141, 2143; 11 vrstic) =
 *   ARTEFAKT OBSEGA JOINA: manjkajoči sosedje obstajajo v registru
 *   (P38 z imeni), brez poligonov v karti → izpad iz v2; 1820/2140 na
 *   prejšnjih straneh (meja strani); 11/11 razloženih.
 * • (C) R1↔R2: 671 RAZREŠENA (II instanca = 1691); 930 ostaja [~]
 *   (moda B ✓@p49 ✗@p99, disjunktna lastnika, sosedi ±1 obeh strani).
 * • (D) UNIVERZALNA DISJUNKTNOST: lastniki per Blatt DISJUNKTNI
 *   110/110 čez-Blatt base (39 split == P66 bajtno, 71 atributiranih
 *   71/71) → ista številka pod različnima Blattoma = 2 RAZLIČNI
 *   realni parceli.
 *
 * Status: REVIEW (renumerifikacija in SPLIT join = odločitev LASTNIKA
 * — P68/P69).
 *
 * Dokaz: research/issue17/ps-anomaly-forensics.json
 * (skripta scripts/p67_ps_anomaly_forensics.py, invariante I1–I8,
 * `--check` bajtno determinističen; 28× sha256 pini).
 */
export async function GET() {
  return NextResponse.json(psAnomalyForensics, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
