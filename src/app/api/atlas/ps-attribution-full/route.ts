import { NextResponse } from "next/server";
import psAttributionFull from "@/data/atlas/ps-attribution-full.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P65) — POLNA PER-BLATT ATRIBUCIJA: 101 SINGLE-BLATT
 * VEČ-STRANSKIH BASE.
 *
 * Odprta točka P64 #3 izpolnjena: 101 base, katerih vse vrstice nosijo
 * strani ISTEGA Blatta, dobi ta Blatt kot attributedBlatt (status
 * 'R3-single' — trivialno in nedvoumno: I 3 · II 26 · III 14 · IV 58;
 * 205 vrstic; vseh 101 z izmerjeno površino) → pokritost več-stranskih
 * base POPOLNA: 211/211 (110 čez-Blatt iz P64 — bajtno nespremenjeno,
 * I3 — + 101 single-Blatt), skupaj 172 atributiranih (Blatt II 68 ·
 * IV 63 · III 29 · I 8 · V 4) + 39 split z alternativami (lastniška
 * odločitev o per-Blatt SPLIT joinu).
 *
 * Polna pokritost registra (kontrolni blok coverage): 800 base × 1093
 * vrstic = 589 single-page (implicitno atributirane prek pageAttribution
 * strani: I 145 · I·II 10 · II 183 · III 28 · IV 205 · V 18) + 211
 * multi-page; 0 vrstic brez atribucije strani.
 *
 * Join v2 NESPREMENJEN (meritve brez prerazporeditev — disciplina
 * P56/P58/P59). Status: REVIEW (strojna atribucija ni dokazni vir).
 *
 * Dokaz: research/issue17/ps-attribution-full.json
 * (skripta scripts/p65_ps_attribution_full.py, invariante I1–I8,
 * `--check` bajtno determinističen). Runtime: polni dataset 211 base.
 */
export async function GET() {
  return NextResponse.json(psAttributionFull, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
