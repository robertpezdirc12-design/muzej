import { NextResponse } from "next/server";
import psRecap from "@/data/atlas/ps-recap.json";

export const dynamic = "force-static";

/**
 * ISSUE #10 (P40) — PS 1825: rekapitulacija str. 140–143 — deterministična
 * primerjava rekapitulacije s spravnim modelom (P5-b).
 * Kontrolne vsote str. 143 (rdeči tuš): 102 stavbnih mest + 2505 zemljiških
 * parcel = 2607 — natanko P38 kontrolna vsota in P36/P38 osnovna črta
 * (1889 + 616 = 2505). Površine po sekcijah modela P39; kandidati za pomen
 * "Summa 1216(?) Joch"; Blatt X prekrivanje (podvajanje nedokazljivo);
 * per-house vrstice 140–141 UNRESOLVED; številčni eho OVRGAN.
 * Status REVIEW — strojno branje ni dokazni vir.
 * Dokaz: research/issue17/ps-recap.json (identičen izpis skripta).
 */
export async function GET() {
  return NextResponse.json(psRecap, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
