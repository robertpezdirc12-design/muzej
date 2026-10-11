import fs from "node:fs";
import path from "node:path";
import { NextResponse } from "next/server";
import { runQA } from "@/lib/qa";

export const dynamic = "force-static";

/**
 * ISSUE #4 — end-to-end kontrola kakovosti (avtomatski testi).
 * HTTP 200 = vsi testi zeleni; 500 = vsaj en test rdeč.
 *
 * P19: ta strežniški klic vbrizga preverjanje datotek na disku
 * (fs.existsSync) — odjemalski izris (museum-coverage) fs nima,
 * zato tam teče ista kontrola v načinu oblike poti.
 */
export async function GET() {
  const report = runQA({
    fileExists: (relativePath) => fs.existsSync(path.join(process.cwd(), relativePath)),
    readFile: (relativePath) => {
      try {
        return fs.readFileSync(path.join(process.cwd(), relativePath), "utf8");
      } catch {
        return null;
      }
    },
  });
  return NextResponse.json(report, {
    status: report.ok ? 200 : 500,
    headers: {
      "Cache-Control": "public, max-age=300",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
