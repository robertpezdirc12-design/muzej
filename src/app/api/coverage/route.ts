import { NextResponse } from "next/server";
import { computeCoverage, compute3DPipeline, compute3DSummary } from "@/lib/coverage";

export const dynamic = "force-static";

/**
 * ISSUE #4 — strojno berljiv coverage pregled zbirke (113 zapisov)
 * + sistematična 3D/AR priprava zgodovinskih objektov.
 * Vse številke so izračunane iz podatkov (exhibits.json, atlas).
 */
export async function GET() {
  const coverage = computeCoverage();
  const pipeline = compute3DPipeline();
  const summary3d = compute3DSummary();

  return NextResponse.json(
    {
      coverage,
      threeD: {
        summary: summary3d,
        pipeline,
        /** tok: objekt → dokaz → tipologija → geometrija → 3D → lokacija → AR */
        flowSi: "zgodovinski objekt → dokaz → tipologija → geometrija → 3D rekonstrukcija → lokacija → AR",
        flowEn: "historical object → evidence → typology → geometry → 3D reconstruction → location → AR",
      },
    },
    {
      headers: {
        "Cache-Control": "public, max-age=3600",
        "Access-Control-Allow-Origin": "*",
      },
    },
  );
}
