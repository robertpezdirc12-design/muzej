"use client";

import { useMemo } from "react";
import { motion } from "framer-motion";
import { BookHeart, CalendarDays, MapPin, ExternalLink, Feather, ScrollText, Megaphone } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useLang } from "./language-context";
import { stories, events, storyTitle, storyText, storyAttribution, EVIDENCE_LABELS, type EvidenceCode } from "@/lib/museum";

const KIND_META: Record<string, { si: string; en: string; icon: typeof Feather }> = {
  ZGODBA: { si: "Zgodba", en: "Story", icon: BookHeart },
  NACELO: { si: "Načelo", en: "Principle", icon: ScrollText },
  RAZPIS: { si: "Razpis", en: "Call", icon: Megaphone },
};

export function MuseumStories() {
  const { t, lang } = useLang();

  return (
    <section id="stories" className="scroll-mt-20 border-t border-border/60" aria-labelledby="stories-naslov">
      <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <h2 id="stories-naslov" className="font-display text-3xl font-semibold tracking-tight">
          {t("Zgodbe in načela", "Stories & principles")}
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
          {t(
            "Kuratorska besedila, ki držijo zbirko skupaj — od načel dela do vaških zgodb.",
            "Curatorial texts that hold the collection together — from working principles to village stories.",
          )}
        </p>

        <ul className="mt-8 grid gap-4 md:grid-cols-2">
          {stories.map((story, i) => {
            const kind = KIND_META[story.kind] ?? KIND_META.ZGODBA;
            const evCode = (story.evidenceStatus as EvidenceCode) ?? "DOCUMENTED";
            const ev = EVIDENCE_LABELS[evCode];
            const Icon = kind.icon;
            const text = storyText(story, lang);
            const paragraphs = text.split(/\n\n+/).filter(Boolean);
            return (
              <motion.li
                key={i}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ duration: 0.4, delay: Math.min(i * 0.06, 0.3) }}
                className="rounded-xl border bg-card p-6 shadow-sm"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="flex items-center gap-1.5 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                    <Icon className="size-3.5 text-primary" aria-hidden="true" />
                    {t(kind.si, kind.en)}
                  </span>
                  {ev && (
                    <Badge variant="outline" className="border-primary/30 bg-primary/10 text-primary">
                      {t(ev.si, ev.en)}
                    </Badge>
                  )}
                </div>
                <h3 className="mt-3 font-display text-xl font-semibold leading-snug text-foreground">
                  {storyTitle(story, lang)}
                </h3>
                <div className="mt-3 space-y-3">
                  {paragraphs.map((p, j) => (
                    <p key={j} className="text-sm leading-7 text-foreground/85">
                      {p}
                    </p>
                  ))}
                </div>
                {storyAttribution(story, lang) && (
                  <p className="mt-4 border-t pt-3 text-[11px] text-muted-foreground">
                    {storyAttribution(story, lang)}
                  </p>
                )}
              </motion.li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}

export function MuseumEvents() {
  const { t, lang } = useLang();

  /* pretekli dogodki pridejo na konec (novejši prej) in so jasno označeni */
  const { upcoming, past } = useMemo(() => {
    const now = Date.now();
    const isPast = (e: (typeof events)[number]) => new Date(e.startsAt).getTime() < now;
    return {
      upcoming: events.filter((e) => !isPast(e)).sort((a, b) => a.startsAt.localeCompare(b.startsAt)),
      past: events.filter(isPast).sort((a, b) => b.startsAt.localeCompare(a.startsAt)),
    };
  }, []);

  const fmt = (iso: string) =>
    new Date(iso).toLocaleDateString(lang === "si" ? "sl-SI" : "en-GB", {
      weekday: "short",
      day: "numeric",
      month: "long",
      year: "numeric",
    });

  const renderCard = (ev: (typeof events)[number], i: number, isPast: boolean) => (
    <motion.li
      key={ev.id}
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.35, delay: Math.min(i * 0.05, 0.25) }}
      className={`rounded-xl border bg-card p-5 shadow-sm ${isPast ? "opacity-70" : ""}`}
      aria-label={isPast ? t("Pretekli dogodek", "Past event") : undefined}
    >
      <div className="flex items-start justify-between gap-3">
        <h3 className="font-display text-lg font-semibold leading-snug">
          {lang === "si" ? ev.titleSi : ev.titleEn}
        </h3>
        {isPast ? (
          <Badge variant="outline" className="shrink-0 font-normal text-muted-foreground">
            {t("pretekli", "past")}
          </Badge>
        ) : (
          ev.eventType && (
            <Badge variant="secondary" className="shrink-0 font-normal text-muted-foreground">
              {ev.eventType}
            </Badge>
          )
        )}
      </div>
      <p className="mt-2 text-sm leading-relaxed text-foreground/85">
        {lang === "si" ? ev.descriptionSi : ev.descriptionEn}
      </p>
      <p className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted-foreground">
        <span className="inline-flex items-center gap-1.5">
          <CalendarDays className="size-3.5 text-primary" aria-hidden="true" />
          {fmt(ev.startsAt)}
        </span>
        {(lang === "si" ? ev.locationSi : ev.locationEn) && (
          <span className="inline-flex items-center gap-1.5">
            <MapPin className="size-3.5 text-primary" aria-hidden="true" />
            {lang === "si" ? ev.locationSi : ev.locationEn}
          </span>
        )}
      </p>
      {ev.isExternal && ev.externalUrl && (
        <a
          href={ev.externalUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-primary underline decoration-border underline-offset-2"
        >
          {t("zunanja povezava", "external link")}
          <ExternalLink className="size-3" aria-hidden="true" />
        </a>
      )}
    </motion.li>
  );

  return (
    <section id="events" className="scroll-mt-20 border-t border-border/60 bg-secondary/30" aria-labelledby="events-naslov">
      <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <h2 id="events-naslov" className="font-display text-3xl font-semibold tracking-tight">
          {t("Dogodki", "Events")}
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
          {t(
            "Kronika živih dogodkov — predstavitve, oglede in obletnice, ki pišejo naslednja poglavja.",
            "A chronicle of live events — presentations, viewings and anniversaries writing the next chapters.",
          )}
        </p>

        {upcoming.length > 0 ? (
          <ul className="mt-8 grid gap-4 md:grid-cols-2">
            {upcoming.map((ev, i) => renderCard(ev, i, false))}
          </ul>
        ) : (
          <p className="mt-8 rounded-xl border border-dashed p-6 text-sm text-muted-foreground">
            {t(
              "Trenutno ni objavljenih prihajajočih dogodkov — sledite spominom spodaj.",
              "No upcoming events are currently published — see the memories below.",
            )}
          </p>
        )}

        {past.length > 0 && (
          <div className="mt-10">
            <h3 className="flex items-center gap-3 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
              <span aria-hidden="true" className="h-px flex-1 bg-border" />
              {t("Pretekli dogodki", "Past events")}
              <span aria-hidden="true" className="h-px flex-1 bg-border" />
            </h3>
            <ul className="mt-5 grid gap-4 md:grid-cols-2">
              {past.map((ev, i) => renderCard(ev, i, true))}
            </ul>
          </div>
        )}
      </div>
    </section>
  );
}
