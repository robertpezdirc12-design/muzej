import { NextResponse } from "next/server";
import psLanduse from "@/data/atlas/ps-landuse.json";

export const dynamic = "force-static";

/**
 * ISSUE #10 (P39) — PS 1825: spravni model rabe tal (parcela × raba).
 * Razdvojitev večkulturnih vrstic iz strojnega prepisa (P36/P38) v model po
 * parcelah: 2134 vnosi (2125 parcel + 9 NEBEREŽNA), 2632 parov parcela×raba,
 * klasifikacija rab po pravilniku v1 (brez AI). Status REVIEW — strojno
 * branje ni dokazni vir; surove vrednosti ostanejo nedotaknjene.
 * Dokaz: research/issue17/ps-landuse.json (identičen izpis skripta).
 */
export async function GET() {
  return NextResponse.json(psLanduse, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
