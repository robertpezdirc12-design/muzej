import { NextResponse } from "next/server";
import psPerblattAttribution from "@/data/atlas/ps-perblatt-attribution.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P60) — PER-BLATT ATRIBUCIJA ruleCandidate base.
 *
 * Izvedba P59 pravila pasu [0.8, 1.25]: vsaka od 17 ruleCandidate base
 * (P59: edina instanca z median razmerjem v pasu) dobi attributedBlatt —
 * MERJENO, brez prerazporeditev joina (disciplina P56/P58/P59):
 *   * II 12 · I 1 · III 4 (23 vrstic); npr. 163 → Blatt II @ 0.9813
 *     (4 kulture na straneh 61/83/84/86) vs Blatt I @ 7.0 @ p11;
 *   * soslednost-kontrola 21/23 (671@p36, 934@p99 [~] — prečrtane vrstice);
 *   * STRUKTURA: pas-strani (36, 49, 61, 83–87, 94, 99) nosijo 100 %
 *     več-stranskih base — Kultur-Tabellen re-listing [~];
 *   * UNIT-SEMANTICS: pas ujema modo B (ratio ≈ 1, n=62), ne modo A
 *     (≈ 3.59665 = 1 QK → m², n=226) — absolutna korespondenca ODPRTA.
 *
 * Join v2 NESPREMENJEN — izpisi ne vsebujejo pozicij/površin (I4 po
 * gradnji; sha256 v2 vhoda pinan v dokazu).
 *
 * Status: REVIEW (relativna atribucija — strojna meritev ni dokazni vir).
 *
 * Dokaz: research/issue17/ps-perblatt-attribution.json (celoten izpis
 * skripta scripts/p60_ps_perblatt_attribution.py; invarianti I1–I7,
 * `--check` = determinizem). Runtime: src/data/atlas/
 * ps-perblatt-attribution.json (kompakt).
 */
export async function GET() {
  return NextResponse.json(psPerblattAttribution, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
