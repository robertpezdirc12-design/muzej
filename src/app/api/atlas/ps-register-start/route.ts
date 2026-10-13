import { NextResponse } from "next/server";
import psRegisterStart from "@/data/atlas/ps-register-start.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P57) — ZAČETEK REGISTRA PS: STRANI 3–4 (ŠTEVILKE 1–40, BLATT I).
 *
 * Strani 3–4 protokola "Der Grund-Parcellen der Gemeinde GRÜBLE" — začetek
 * glavnega registra, ki ju P38/P56 izbora NISTA vključila (edini vir številk
 * 1–36 je bil S3 zapadek str. 138–139) — prebrane s ŠTIRIMI neodvisnimi VLM
 * plastmi in deterministično adjudicirane:
 *  · polna stran ×3 prehodi (ps-00{3,4}{,-pass2,-pass3}.json);
 *  · kolone Haus Nro. ×3 (3× izrezi leve tabele — polnostransko branje je
 *    sistematično mešalo dvomestne hišne številke 60–66 s črkami);
 *  · izrezi površin ×3 (LCS poravnava — na str. 4 VLM vstavi [?]);
 *  · tarčne celice 6× za 10 spornih vrednosti (r9/r10/r12/r23/r29/r30/r32/
 *    r39/r40 + r1 [?]) z odločanjem (r40: 3/3 celice = 413).
 *
 * VERIGA: 1–20 (str. 3) + 21–40 (str. 4) + committed ps-005 (41–60) =
 * neprekinjen Blatt I 1–60.
 *
 * OBNOVA: join po mehaniki P55 poveže 26/40 številskih — TOČNO vseh 26 base,
 * ki jih je P56 moral sanirati; 25 s pari površin (median modern/QK 3.7594 ≈
 * 1 Wiener QK 3.59665 m², Δ +4.53 %; kontrola seed 42 = 3.2098 — 2.4× dlje od
 * konstante; pas ±10 %: 16.0 % vs 6.2 %), številka 1 brez prebrane površine
 * (celica prazna). SOSLEDNOST: 19 parov, median 81.2 m; kontrola seed 7 =
 * 263 m (3.2×), MIN 126 m > opaženi — Monte-Carlo 100 %. Zaupanje STRONG 3 /
 * MEDIUM 14 / WEAK 9; 14 upokojenih številk brez sodobne naslednice.
 *
 * Status: REVIEW (strojno branje ni dokazni vir). SHEET_GEOREFS in dokazi
 * P40–P56 nespremenjeni; P55/P56 runtime nespremenjena (pini qa-p55/p56).
 *
 * Dokaz: research/issue17/ps-register-start.json (celoten izpis skripta
 * scripts/p57_ps_register_start.py; invarianti I1–I8, `--check` =
 * determinizem). Runtime: src/data/atlas/ps-register-start.json (kompakt).
 */
export async function GET() {
  return NextResponse.json(psRegisterStart, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
