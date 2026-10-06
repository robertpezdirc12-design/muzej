import { NextResponse } from "next/server";
import eventsData from "@/data/museum/events.json";

export const dynamic = "force-static";

export async function GET() {
  return NextResponse.json(eventsData, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
