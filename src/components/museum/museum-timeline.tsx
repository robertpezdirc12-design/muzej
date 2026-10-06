"use client";

import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Clock } from "lucide-react";
import { useLang } from "./language-context";
import { exhibitsByMuseumNo, EVIDENCE_LABELS, type Exhibit } from "@/lib/museum";

interface Era {
  label: string;
  from: number;
  to: number;
  noteSi: string;
  noteEn: string;
}

const ERAS: Era[] = [
  {
    label: "1468–1790",
    from: 1400,
    to: 1790,
    noteSi: "Prve omembe, urbarji, turški vpadi in obmejni svet",
    noteEn: "First records, urbaria, Ottoman incursions and the frontier world",
  },
  {
    label: "1790–1918",
    from: 1790,
    to: 1918,
    noteSi: "Katastri, šola, železnica in konec imperija",
    noteEn: "Cadastres, school, railway and the end of the empire",
  },
  {
    label: "1918–1945",
    from: 1918,
    to: 1945,
    noteSi: "Meja, okupacija, partizansko letališče in zračni most",
    noteEn: "Border, occupation, partisan airfield and the airlift",
  },
  {
    label: "1945–1991",
    from: 1945,
    to: 1991,
    noteSi: "Jugoslavija, Kanižarica, Turpedo in nova država",
    noteEn: "Yugoslavia, Kanižarica, Torpedo and a new country",
  },
  {
    label: "1991–danes",
    from: 1991,
    to: 2100,
    noteSi: "Schengen, biodiverziteta, digitalizacija in skupnost",
    noteEn: "Schengen, biodiversity, digitisation and the community",
  },
];

export function MuseumTimeline({ onOpen }: { onOpen: (slug: string) => void }) {
  const { t, lang } = useLang();
  const [eraIdx, setEraIdx] = useState(0);
  const era = ERAS[eraIdx];

  const items = useMemo(() => {
    return exhibitsByMuseumNo()
      .filter((e) => {
        const y = e.yearFrom;
        if (y == null) return false;
        return y >= era.from && y < era.to;
      })
      .sort((a, b) => (a.yearFrom ?? 0) - (b.yearFrom ?? 0));
  }, [era]);

  return (
    <section id="timeline" className="scroll-mt-20 border-t border-border/60 bg-secondary/30" aria-labelledby="timeline-naslov">
      <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 id="timeline-naslov" className="font-display text-3xl font-semibold tracking-tight">
              {t("Časovnica vasi", "Village timeline")}
            </h2>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              {t(
                "Zapisi, razporejeni po letu prve omembe — od prve omembe vasi 1468 do danes.",
                "Records arranged by year of first mention — from the village's first record in 1468 to today.",
              )}
            </p>
          </div>
          <p className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Clock className="size-3.5 text-primary" aria-hidden="true" />
            {t(`${items.length} zapisov v obdobju`, `${items.length} records in the period`)}
          </p>
        </div>

        <div className="mt-6 flex flex-wrap gap-2" role="tablist" aria-label={t("Obdobja", "Eras")}>
          {ERAS.map((e, i) => (
            <button
              key={e.label}
              type="button"
              role="tab"
              aria-selected={i === eraIdx}
              onClick={() => setEraIdx(i)}
              className={`min-h-9 rounded-full border px-4 text-xs font-medium transition-colors ${
                i === eraIdx
                  ? "border-primary/50 bg-primary/10 text-primary"
                  : "border-border bg-card text-muted-foreground hover:border-primary/30 hover:text-foreground"
              }`}
            >
              {e.label}
            </button>
          ))}
        </div>

        <p className="mt-4 text-xs italic text-muted-foreground">
          {t(era.noteSi, era.noteEn)}
        </p>

        <ol className="relative mt-6 space-y-3 before:absolute before:bottom-2 before:left-[15px] before:top-2 before:w-px before:bg-border">
          {items.map((e: Exhibit, i) => {
            const ev = EVIDENCE_LABELS[e.evidenceStatus];
            return (
              <motion.li
                key={e.slug}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: Math.min(i * 0.03, 0.3) }}
                className="relative pl-11"
              >
                <span
                  className="absolute left-0 top-1.5 flex size-8 items-center justify-center rounded-full border border-primary/40 bg-background font-mono text-[10px] font-semibold text-primary"
                  aria-hidden="true"
                >
                  {String(e.yearFrom).slice(-2)}
                </span>
                <button
                  type="button"
                  onClick={() => onOpen(e.slug)}
                  className="group flex w-full flex-wrap items-baseline gap-x-3 gap-y-1 rounded-lg border bg-card px-4 py-3 text-left transition-colors hover:border-primary/40"
                >
                  <span className="font-mono text-xs font-semibold text-primary">{e.yearFrom}</span>
                  <span className="text-sm font-medium text-foreground group-hover:text-primary">
                    {lang === "si" ? e.titleSi : e.titleEn}
                  </span>
                  <span className="text-[11px] text-muted-foreground">{e.museumNo}</span>
                  {ev && (
                    <span className="ml-auto hidden rounded-full border border-primary/25 bg-primary/10 px-2 py-0.5 text-[10px] font-medium text-primary sm:inline">
                      {t(ev.si, ev.en)}
                    </span>
                  )}
                </button>
              </motion.li>
            );
          })}
        </ol>

        {items.length === 0 && (
          <p className="mt-6 rounded-lg border border-dashed p-6 text-center text-sm text-muted-foreground">
            {t("V tem obdobju še ni zapisov.", "No records in this period yet.")}
          </p>
        )}
      </div>
    </section>
  );
}
