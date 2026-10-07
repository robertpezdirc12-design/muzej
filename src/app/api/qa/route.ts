import { NextResponse } from "next/server";
import { runQA } from "@/lib/qa";

export const dynamic = "force-static";

/**
 * ISSUE #4 — end-to-end kontrola kakovosti (avtomatski testi).
 * HTTP 200 = vsi testi zeleni; 500 = vsaj en test rdeč.
 */
export async function GET() {
  const report = runQA();
  return NextResponse.json(report, {
    status: report.ok ? 200 : 500,
    headers: {
      "Cache-Control": "public, max-age=300",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
