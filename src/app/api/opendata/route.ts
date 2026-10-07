import { NextResponse } from "next/server";
import exhibitsData from "@/data/museum/exhibits.json";
import eventsData from "@/data/museum/events.json";
import metaRaw from "@/data/museum/meta.json";
import { DATA_VERSION } from "@/lib/provenance";

export const dynamic = "force-static";

/** ISSUE #3 #10 — dejanski čas generiranja (build/render čas, ne 1970) */
const GENERATED_AT = new Date().toISOString();

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
      dataVersion: DATA_VERSION,
      generatedAt: GENERATED_AT,
      counts: meta.counts,
      evidenceScale: meta.evidenceScale,
      data: {
        exhibits,
        stories: meta.stories,
        events,
      },
      /** ISSUE #3 #9 — licenca je razdeljena po plasteh, globalni CC BY-SA 4.0
       * velja le za lastne metapodatke sklopa, ne za vse vključene vire. */
      license: {
        dataset: "CC BY-SA 4.0",
        scopeSi:
          "Licenca CC BY-SA 4.0 velja SAMO za lastne strukturne metapodatke tega podatkovnega sklopa (razvrstitev zapisa, povzetki, evidenceStatus, geopovezave). Za vsak posamezen vir, sliko in reprodukcijo veljajo lastne pravice — glej sources[].license in imageCredit vsakega zapisa.",
        scopeEn:
          "The CC BY-SA 4.0 license applies ONLY to the structural metadata of this dataset (record classification, summaries, evidenceStatus, geolinks). Each individual source, image and reproduction carries its own rights — see sources[].license and imageCredit of each record.",
        perSource: "vsak vir ima svoj licenčni podatek v sources[].license",
        perImage: "pravice fotografij so v imageCredit vsakega zapisa",
        reproductionSi:
          "Reprodukcija arhivskih in muzejskih predmetov (Arhiv RS/VAČ, SEM, zasebni arhivi) zahteva soglasje imetnika pravic; javno dostopni arhivski viri (VAČ) ne zahtevajo dovoljenja za vpogled in citiranje.",
        reproductionEn:
          "Reproduction of archival and museum objects (Arhiv RS/VAČ, SEM, private archives) requires the rights holder's consent; publicly accessible archival sources (VAČ) require no permission for consultation and citation.",
        attributionSi:
          "Obvezna atribucija: Muzej vasi Griblje (sklop podatkov) + izvorni vir posameznega zapisa.",
        attributionEn:
          "Required attribution: Muzej vasi Griblje (the dataset) + the original source of each record.",
        provenanceApi: "/api/provenance",
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
