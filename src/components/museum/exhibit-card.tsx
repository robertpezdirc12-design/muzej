"use client";

import { motion } from "framer-motion";
import { Star, ChevronRight } from "lucide-react";
import { Card } from "@/components/ui/card";
import { useLang } from "./language-context";
import { EVIDENCE_LABELS, CATEGORY_LABELS, type Exhibit } from "@/lib/museum";

export function ExhibitCard({
  exhibit,
  onOpen,
}: {
  exhibit: Exhibit;
  onOpen: (slug: string) => void;
}) {
  const { t, lang } = useLang();
  const title = lang === "si" ? exhibit.titleSi : exhibit.titleEn;
  const period = lang === "si" ? exhibit.periodSi : exhibit.periodEn;
  const ev = EVIDENCE_LABELS[exhibit.evidenceStatus];
  const cat = CATEGORY_LABELS[exhibit.category];

  return (
    <Card
      role="button"
      tabIndex={0}
      onClick={() => onOpen(exhibit.slug)}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onOpen(exhibit.slug);
        }
      }}
      aria-label={`${exhibit.museumNo} — ${title}`}
      className="group flex cursor-pointer flex-col overflow-hidden p-0 transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-md focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
    >
      <div className="relative aspect-[4/3] overflow-hidden bg-secondary">
        {exhibit.image ? (
          <img
            src={exhibit.image}
            alt={title}
            loading="lazy"
            className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center font-display text-3xl text-muted-foreground/40">
            {exhibit.museumNo}
          </div>
        )}
        <span className="absolute left-3 top-3 rounded-full bg-background/90 px-2.5 py-1 font-mono text-[11px] font-semibold text-primary backdrop-blur">
          {exhibit.museumNo}
        </span>
        {exhibit.featured && (
          <span
            className="absolute right-3 top-3 flex size-7 items-center justify-center rounded-full bg-primary text-primary-foreground"
            title={t("Izpostavljeni zapis", "Featured record")}
          >
            <Star className="size-3.5" aria-hidden="true" />
          </span>
        )}
      </div>

      <div className="flex flex-1 flex-col gap-2 p-4">
        <div className="flex flex-wrap items-center gap-1.5">
          {cat && (
            <span className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              {t(cat.si, cat.en)}
            </span>
          )}
          <span aria-hidden="true" className="text-muted-foreground/50">·</span>
          <span className="text-[11px] text-muted-foreground">{period}</span>
        </div>

        <h3 className="font-display text-lg font-semibold leading-snug text-foreground group-hover:text-primary">
          {title}
        </h3>

        <p className="line-clamp-2 text-xs leading-relaxed text-muted-foreground">
          {lang === "si" ? exhibit.summarySi : exhibit.summaryEn}
        </p>

        <div className="mt-auto flex items-center justify-between pt-2">
          {ev && (
            <span className="inline-flex items-center gap-1.5 rounded-full border border-primary/25 bg-primary/10 px-2.5 py-1 text-[11px] font-medium text-primary">
              <span className="size-1.5 rounded-full bg-primary" aria-hidden="true" />
              {t(ev.si, ev.en)}
            </span>
          )}
          <span className="inline-flex items-center gap-0.5 text-xs font-medium text-primary opacity-0 transition-opacity group-hover:opacity-100">
            {t("Odpri zapis", "Open record")}
            <ChevronRight className="size-3.5" aria-hidden="true" />
          </span>
        </div>
      </div>
    </Card>
  );
}
