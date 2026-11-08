import { NextResponse } from "next/server";
import { checkIntegrity } from "@/lib/atlas";

export const dynamic = "force-static";

/** Testni končna točka: preveri povezave hiša ↔ parcela ↔ lastnik ↔ vir (issue #2 zahteva testi). */
export async function GET() {
  const report = checkIntegrity();
  return NextResponse.json(
    { ...report, at: new Date().toISOString() },
    {
      status: report.ok ? 200 : 500,
      headers: {
        "Cache-Control": "public, max-age=300",
        "Access-Control-Allow-Origin": "*",
      },
    },
  );
}
