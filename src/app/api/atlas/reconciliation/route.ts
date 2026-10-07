import { NextResponse } from "next/server";
import { buildReconciliation } from "@/lib/reconciliation";

export const dynamic = "force-static";

/**
 * ISSUE #5 — N83 arhiv → Atlas reconciliation report (zero-loss).
 * Vsaka izvorna vrstica PT/PUA/PS, vsak grafični list in vsaka
 * nereprepisana serija ima vrstico z eksplicitnim stanjem.
 */
export async function GET() {
  const report = buildReconciliation();
  return NextResponse.json(report, {
    status: report.zeroLoss ? 200 : 500,
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
