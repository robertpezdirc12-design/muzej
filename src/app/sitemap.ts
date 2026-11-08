import type { MetadataRoute } from "next";
import exhibitsData from "@/data/museum/exhibits.json";

const SITE = "https://griblje-museum.vercel.app";

type Exhibit = { slug?: string };

const exhibits: Exhibit[] = Array.isArray(exhibitsData)
  ? (exhibitsData as Exhibit[])
  : ((exhibitsData as { exhibits?: Exhibit[] }).exhibits ?? []);

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();

  return [
    {
      url: SITE,
      lastModified,
      changeFrequency: "monthly",
      priority: 1,
    },
    ...exhibits
      .filter((e) => Boolean(e.slug))
      .map((e) => ({
        url: `${SITE}/?exponat=${e.slug}`,
        lastModified,
        changeFrequency: "yearly" as const,
        priority: 0.7,
      })),
  ];
}
