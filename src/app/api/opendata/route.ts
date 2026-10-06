import { NextResponse } from "next/server";
import exhibitsData from "@/data/museum/exhibits.json";
import eventsData from "@/data/museum/events.json";
import metaRaw from "@/data/museum/meta.json";

export const dynamic = "force-static";

/**
 * Odprti podatki muzeja — po vzoru izvirniškega /api/opendata.
 * Vrne muzejske metapodatke, števce, lestvico zanesljivosti,
 * zgodbe, dogodke in konsolidiran seznam eksponatov.
 */
export async function GET() {
  const meta = metaRaw as {
    museum: Record<string, unknown>;
    counts: Record<string, number>;
    evidenceScale: unknown[];
    stories: unknown[];
  };

  const exhibits = (
    exhibitsData as { exhibits: Array<Record<string, unknown>> }
  ).exhibits.map((e) => ({
    slug: e.slug,
    museumNo: e.museumNo,
    category: e.category,
    title: { sl: e.titleSi, en: e.titleEn },
    period: { sl: e.periodSi, en: e.periodEn },
    summary: { sl: e.summarySi, en: e.summaryEn },
    story: { sl: e.storySi, en: e.storyEn },
    evidenceStatus: e.evidenceStatus,
    image: e.image,
    imageCredit: e.imageCredit,
    yearFrom: e.yearFrom,
    yearTo: e.yearTo,
    location: { lat: e.lat, lng: e.lng, approx: e.coordsApprox },
    sources: e.sources,
  }));

  const events = (
    eventsData as { events: Array<Record<string, unknown>> }
  ).events.map((ev) => ({
    title: { sl: ev.titleSi, en: ev.titleEn },
    description: { sl: ev.descriptionSi, en: ev.descriptionEn },
    startsAt: ev.startsAt,
    location: { sl: ev.locationSi, en: ev.locationEn },
    type: ev.eventType,
    isExternal: ev.isExternal,
    externalUrl: ev.externalUrl,
  }));

  return NextResponse.json(
    {
      museum: meta.museum,
      generatedAt: new Date(0).toISOString(),
      counts: meta.counts,
      evidenceScale: meta.evidenceScale,
      data: {
        exhibits,
        stories: meta.stories,
        events,
      },
      license: "CC BY-SA 4.0",
    },
    {
      headers: {
        "Cache-Control": "public, max-age=3600",
        "Access-Control-Allow-Origin": "*",
      },
    },
  );
}
