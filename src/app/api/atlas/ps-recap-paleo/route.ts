import { NextResponse } from "next/server";
import psRecapPaleo from "@/data/atlas/ps-recap-paleo.json";

export const dynamic = "force-static";

/**
 * ISSUE #10 (P41) — PS 1825: paleografija str. 140–143 — "Abschluß der
 * Gemeinde" in per-Lage rekapitulacija.
 * 12 neodvisnih VLM prehodov (3×4 strani 140–143) + deterministična sprava
 * (scripts/p41_ps_recap_paleo.py, brez AI ob delovanju):
 * 7 vrstic "Grundstückslagen" → 831 J 702 K = "Summa der Grundparzellen";
 * "Area der Gemeinde" 1220 J 1493 K — prvi ujeti skupna površina občine,
 * aritmetično zvezana (1215|490 + 5|1003 = 1220|1493). Model GRUND odmika
 * le +0,99 % — nadomešča P40 atribucijo "Summa 1216(?)" (+1,39 %).
 * Razcepi (K1/K2, semantika par referenc) ostajajo izrecno UNRESOLVED.
 * Status REVIEW — strojno branje ni dokazni vir.
 * Dokaz: research/issue17/ps-recap-paleo.json (identičen izpis skripta).
 */
export async function GET() {
  return NextResponse.json(psRecapPaleo, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
