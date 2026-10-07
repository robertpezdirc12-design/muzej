import { NextResponse } from "next/server";
import { getAtlasModel } from "@/lib/atlas";

export const dynamic = "force-static";

/** Celoten ATLAS 1825 podatkovni model (JSON; strojna uporaba, provenienca vključena). */
export async function GET() {
  return NextResponse.json(getAtlasModel(), {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
