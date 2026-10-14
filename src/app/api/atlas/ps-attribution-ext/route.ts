import { NextResponse } from "next/server";
import psAttributionExt from "@/data/atlas/ps-attribution-ext.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P64) — RAZŠIRITEV PER-BLATT ATRIBUCIJE NA VSEH 110 ČEZ-BLATT BASE.
 *
 * Odprta točka P60/P62 #7 (»razširiti atribucijo na vseh 110 čez-Blatt base«)
 * izpolnjena z MERJENO hierarhijo pravil (deterministično, brez prerazporeditev
 * joina — disciplina P56/P58/P59):
 *
 * - R1 (pas, P60): 17 ruleCandidate base — attributedBlatt = instanca v pasu
 *   [0.8, 1.25] (moda B), bajtno konsistentno s P60 evidence.
 * - R2a (area-dominanca ≥ 0.75): 53 base — dominantni Blatt po Σ areaQK
 *   (II 29 · III 11 · IV 5 · I 4 · V 4).
 * - R2b (ena sama Blatt s površino): 1 base (1605 — II 2688 QK, IV brez
 *   areaQK) + flag areaIncomplete.
 * → skupaj 71/110 atributiranih (Blatt II 42 · III 15 · I 5 · IV 5 · V 4).
 * - split: 39 base z dominantnim deležem 0.5–0.75 (II 19 · III 9 · IV 6 ·
 *   V 4 · I 1) — attributedBlatt = null + alternativе po deležih; kandidati
 *   za lastniško odločitev o per-Blatt SPLIT joinu.
 * - Konsistenca R1↔R2: 15/17 soglasij; 2 merjeni divergence (930: R1 II vs
 *   R2 dom III @ 0.763; 671: R1 I vs R2 dom II @ 0.8844) — R1 ima prednost [~].
 *
 * Join v2 NESPREMENJEN (meritve brez prerazporeditev). Status: REVIEW
 * (strojna atribucija ni dokazni vir).
 *
 * Dokaz: research/issue17/ps-attribution-ext.json
 * (skripta scripts/p64_ps_attribution_ext.py, invariante I1–I8,
 * `--check` bajtno determinističen). Runtime: kompakt.
 */
export async function GET() {
  return NextResponse.json(psAttributionExt, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
