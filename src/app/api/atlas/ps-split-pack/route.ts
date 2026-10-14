import { NextResponse } from "next/server";
import psSplitPack from "@/data/atlas/ps-split-pack.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P66) — SPLIT DECISION PACK: 39 SPLIT BASE.
 *
 * Odločitveni paket za per-Blatt SPLIT joina (odprta točka P64 #8 /
 * kandidat #1 iz P65 `next`): P66 NE odloča namesto lastnika — MERI in
 * DOKAZUJE dejstva (deterministično, brez AI ob delovanju; join v2
 * NESPREMENJEN — disciplina P56/P58/P59/P65):
 *
 * • vseh 39 base ima TOČNO 2 deleža (blattShares), 93 vrstic
 *   (25 × 2 + 13 × 3 + 1 × 4);
 * • Blatt pari: I·II 7 · II·III 21 · II·IV 2 · IV·V 9 (37/39 sosednja
 *   Blatta, 2 skoka II·IV — 1603/1604, isti kulturi na obeh Blattih);
 * • LASTNIŠKA RAZČLENITEV PER BLATT: 39/39 DISJUNKTNI lastniki — vsak
 *   split base ima različne lastnike po Blattih (močan dokaz, da je
 *   ista številka pod različnima Blattoma 2 RAZLIČNI realni parceli);
 *   2–3 edinstvenih lastnikov (25/13/1);
 * • dominantni deleži [0.50,0.60) 23 · [0.60,0.70) 11 · [0.70,0.75) 5;
 * • kulture 92 (kulturesByBlatt razčlenitev);
 * • GEO: 39/39 base nosi VSEH vrstic ENAKO geometrijo joina v2
 *   (0 različnih) — join v2 je na nivoju številke, zato SPLIT join bi
 *   zahteval 2 geometriji (števec merjen brez koordinat — I6);
 * • areaSuspect 0; sosledje split del 82/93 (flag 11 — 5 base: 646,
 *   661, 1821, 2141, 2143);
 * • P65 polja 39× bajtno (I3).
 *
 * Status: REVIEW (strojna atribucija ni dokazni vir; odločitev LASTNIKA).
 *
 * Dokaz: research/issue17/ps-split-pack.json
 * (skripta scripts/p66_ps_split_pack.py, invariante I1–I8,
 * `--check` bajtno determinističen). Runtime: polni dataset 39 base
 * z per-vrstično razčlenitvijo.
 */
export async function GET() {
  return NextResponse.json(psSplitPack, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
