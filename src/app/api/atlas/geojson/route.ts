import { NextResponse } from "next/server";
import { getAtlasGeoJSON } from "@/lib/atlas";

export const dynamic = "force-static";

/** GeoJSON izvoz prostorskih slojev Atlasa (lokacije, EŠD, objekti ~1825, vas). */
export async function GET() {
  return NextResponse.json(getAtlasGeoJSON(), {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
