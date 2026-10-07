"use client";

import { Fragment } from "react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/ui/sheet";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  ShieldCheck,
  BookOpen,
  Quote,
  MapPin,
  Footprints,
  Link2,
  Sprout,
  ExternalLink,
  X,
} from "lucide-react";
import { useLang } from "./language-context";
import { ModelViewer3D } from "./model-viewer-3d";
import {
  getExhibit,
  getExtra,
  EVIDENCE_LABELS,
  CATEGORY_LABELS,
  type Exhibit,
} from "@/lib/museum";

export function ExhibitDetail({
  slug,
  onClose,
  onOpen,
}: {
  slug: string | null;
  onClose: () => void;
  onOpen: (slug: string) => void;
}) {
  const { t, lang } = useLang();
  const exhibit: Exhibit | undefined = slug ? getExhibit(slug) : undefined;
  const extra = slug ? getExtra(slug) : null;

  if (!exhibit) {
    return (
      <Sheet open={false} openChange={(o) => !o && onClose()}>
        <SheetContent />
      </Sheet>
    );
  }

  const title = lang === "si" ? exhibit.titleSi : exhibit.titleEn;
  const period = lang === "si" ? exhibit.periodSi : exhibit.periodEn;
  const summary = lang === "si" ? exhibit.summarySi : exhibit.summaryEn;
  const story = lang === "si" ? exhibit.storySi : exhibit.storyEn;
  const ev = EVIDENCE_LABELS[exhibit.evidenceStatus];
  const cat = CATEGORY_LABELS[exhibit.category];
  const storyParagraphs = story.split(/\n\n+/).filter(Boolean);

  return (
    <Sheet open={!!slug} onOpenChange={(o) => !o && onClose()}>
      <SheetContent
        side="right"
        className="muzej-scroll w-full overflow-y-auto p-0 sm:max-w-2xl"
      >
        {/* glava zapisa */}
        <div className="relative">
          {exhibit.image && (
            <div className="relative h-56 w-full overflow-hidden sm:h-64">
              <img
                src={exhibit.image}
                alt={title}
                className="h-full w-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
              {exhibit.imageCredit && (
                <p className="absolute inset-x-0 bottom-0 p-3 pt-8 text-[10px] leading-snug text-white/85">
                  {exhibit.imageCredit}
                </p>
              )}
            </div>
          )}
          <button
            type="button"
            onClick={onClose}
            className="absolute right-3 top-3 flex size-9 items-center justify-center rounded-full bg-background/90 text-foreground shadow backdrop-blur transition-colors hover:bg-background"
            aria-label={t("Zapri zapis", "Close record")}
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </div>

        <div className="px-5 pb-16 sm:px-7">
          <SheetHeader className="px-0 text-left">
            <p className="flex flex-wrap items-center gap-2 pt-5 text-xs text-muted-foreground">
              <span className="font-mono font-semibold text-primary">{exhibit.museumNo}</span>
              {cat && <span className="uppercase tracking-wider">{t(cat.si, cat.en)}</span>}
              <span aria-hidden="true">·</span>
              <span>{period}</span>
            </p>
            <SheetTitle className="font-display text-2xl font-semibold leading-tight sm:text-3xl">
              {title}
            </SheetTitle>
            <SheetDescription className="text-sm leading-relaxed text-muted-foreground">
              {summary}
            </SheetDescription>
          </SheetHeader>

          {/* status dokaza */}
          <section className="mt-6 rounded-lg border bg-card p-4" aria-labelledby="status-dokaza">
            <h2 id="status-dokaza" className="flex items-center gap-2 text-sm font-semibold text-foreground">
              <ShieldCheck className="size-4 text-primary" aria-hidden="true" />
              {t("Status dokaza", "Evidence status")}
            </h2>
            <div className="mt-3 flex flex-wrap items-center gap-2">
              {ev && (
                <>
                  <span className="inline-flex items-center gap-1.5 rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
                    {t(ev.si, ev.en)}
                  </span>
                  <p className="text-xs leading-relaxed text-muted-foreground">
                    {t(ev.descSi, ev.descEn)}
                  </p>
                </>
              )}
            </div>
          </section>

          {/* kako vemo — zgodba */}
          <section className="mt-6" aria-labelledby="kako-vemo">
            <h2 id="kako-vemo" className="flex items-center gap-2 font-display text-xl font-semibold">
              <BookOpen className="size-4 text-primary" aria-hidden="true" />
              {t("Kako vemo", "How we know")}
            </h2>
            <div className="mt-3 space-y-4">
              {storyParagraphs.map((p, i) => (
                <p key={i} className="text-sm leading-7 text-foreground/90">
                  {p}
                </p>
              ))}
            </div>
          </section>

          {/* interpretativni 3D-model zapisa */}
          {exhibit.model3dUrl && (
            <ModelViewer3D
              src={exhibit.model3dUrl}
              credit={exhibit.model3dCredit}
            />
          )}

          {/* življenje predmeta */}
          {extra && extra.lifeStations.length > 0 && (
            <section className="mt-8" aria-labelledby="zivljenje-predmeta">
              <Accordion type="single" collapsible>
                <AccordionItem value="zivljenje" className="rounded-lg border px-4">
                  <AccordionTrigger className="py-4 text-left">
                    <span className="flex flex-col gap-1">
                      <span className="font-display text-xl font-semibold">
                        {t("Življenje predmeta", "Life of the record")}
                      </span>
                      <span className="text-sm text-muted-foreground">
                        {t(
                          `${extra.lifeStations.length} postaj življenja`,
                          `${extra.lifeStations.length} life stations`,
                        )}
                      </span>
                    </span>
                  </AccordionTrigger>
                  <AccordionContent>
                    <p className="mb-5 text-xs italic leading-relaxed text-muted-foreground">
                      {t(
                        "Pot zapisa skozi čas — po vzoru Art Tracks (Carnegie Museum of Art): vsaka točka nosi vir in stopnjo zanesljivosti. Vrzeli so del zgodbe, ne sramota.",
                        "The record's path through time — after Art Tracks (Carnegie Museum of Art): each point carries a source and reliability level. Gaps are part of the story, not a shame.",
                      )}
                    </p>
                    <ol className="relative space-y-6 before:absolute before:bottom-2 before:left-[15px] before:top-2 before:w-px before:bg-border">
                      {extra.lifeStations.map((st, i) => (
                        <li key={i} className="relative pl-11">
                          <span
                            className="absolute left-0 top-0.5 flex size-8 items-center justify-center rounded-full border border-primary/40 bg-background text-primary"
                            aria-hidden="true"
                          >
                            <Sprout className="size-4" />
                          </span>
                          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                            <span className="font-display text-sm font-semibold">{st.year}</span>
                            {st.stage && (
                              <span className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                                {st.stage}
                              </span>
                            )}
                          </div>
                          {st.description && (
                            <p className="mt-1.5 text-sm leading-relaxed text-foreground/90">
                              {st.description}
                            </p>
                          )}
                          <div className="mt-2 flex flex-wrap items-center gap-2">
                            {st.evidence && (
                              <span className="inline-flex items-center gap-1.5 rounded-full border border-primary/30 bg-primary/10 px-2.5 py-1 text-xs font-medium text-primary">
                                {st.evidence}
                              </span>
                            )}
                            {st.sourceUrl && (
                              <a
                                href={st.sourceUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex max-w-full items-center gap-1 text-xs text-muted-foreground underline decoration-border underline-offset-2 hover:text-foreground"
                              >
                                {t("vir", "source")}: {st.sourceName}
                                <ExternalLink className="size-3 shrink-0" aria-hidden="true" />
                              </a>
                            )}
                          </div>
                        </li>
                      ))}
                    </ol>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </section>
          )}

          {/* viri */}
          {exhibit.sources.length > 0 && (
            <section className="mt-6" aria-labelledby="viri">
              <h2 id="viri" className="flex items-center gap-2 font-display text-xl font-semibold">
                <Link2 className="size-4 text-primary" aria-hidden="true" />
                {t(`Viri (${exhibit.sources.length})`, `Sources (${exhibit.sources.length})`)}
              </h2>
              <ScrollArea className="muzej-scroll mt-3 max-h-96 pr-3">
                <ol className="space-y-2">
                  {exhibit.sources.map((s, i) => (
                    <li key={s.id ?? i} className="rounded-lg border bg-card p-3.5 text-sm">
                      <div className="flex items-start justify-between gap-2">
                        <span className="flex gap-2">
                          <span className="font-mono text-xs text-muted-foreground">{i + 1}.</span>
                          <span className="font-medium leading-snug text-foreground">
                            {(lang === "si" ? s.nameSi : s.nameEn) ?? s.nameSi ?? s.nameEn}
                          </span>
                        </span>
                        {s.sourceType && (
                          <span className="shrink-0 text-[10px] uppercase tracking-wider text-muted-foreground">
                            {s.sourceType}
                          </span>
                        )}
                      </div>
                      <div className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted-foreground">
                        {s.license && <span>{s.license}</span>}
                        {s.url && (
                          <a
                            href={s.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 underline decoration-border underline-offset-2 hover:text-foreground"
                          >
                            {t("oglej si vir", "view source")}
                            <ExternalLink className="size-3" aria-hidden="true" />
                          </a>
                        )}
                      </div>
                    </li>
                  ))}
                </ol>
              </ScrollArea>
            </section>
          )}

          {/* zgodovinske trditve */}
          {extra && extra.claims.length > 0 && (
            <section className="mt-6" aria-labelledby="trditve">
              <h2 id="trditve" className="flex items-center gap-2 font-display text-xl font-semibold">
                <ShieldCheck className="size-4 text-primary" aria-hidden="true" />
                {t(
                  `Zgodovinske trditve (${extra.claims.length})`,
                  `Historical claims (${extra.claims.length})`,
                )}
              </h2>
              <p className="mt-2 max-w-2xl text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Izrazite trditve z živo verigo dokazov (vir + stran/enota + status). Izvirni vpisi so v slovenščini; negotova branja so označena, ugibanj ni.",
                  "Distinctive claims with a live chain of evidence (source + page/unit + status). Original entries are in Slovenian; uncertain readings are marked, there is no guessing.",
                )}
              </p>
              <ol className="mt-4 space-y-3">
                {extra.claims.map((c, i) => (
                  <li key={i} className="rounded-lg border bg-card p-4 text-sm">
                    <div className="flex flex-wrap items-start justify-between gap-2">
                      <p className="max-w-3xl font-medium leading-relaxed text-foreground">{c.text}</p>
                      {c.evidence && (
                        <span className="inline-flex shrink-0 items-center gap-1 rounded-full border border-chart-3/30 bg-chart-3/15 px-2.5 py-1 text-xs font-medium text-chart-3">
                          {c.evidence}
                        </span>
                      )}
                    </div>
                    <div className="mt-1.5 space-y-1 text-xs text-muted-foreground">
                      {c.confidence && (
                        <p>
                          {t("Zanesljivost", "Confidence")}: <span className="font-medium">{c.confidence}</span>
                        </p>
                      )}
                      {c.sourceName && (
                        <p>
                          {t("Vir", "Source")}:{" "}
                          {c.sourceUrl ? (
                            <a
                              href={c.sourceUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="underline decoration-border underline-offset-2 hover:text-foreground"
                            >
                              {c.sourceName}
                            </a>
                          ) : (
                            c.sourceName
                          )}
                        </p>
                      )}
                    </div>
                  </li>
                ))}
              </ol>
            </section>
          )}

          {/* citiraj */}
          <section className="mt-6 rounded-lg border bg-secondary/50 p-4" aria-labelledby="citiraj">
            <h2 id="citiraj" className="flex items-center gap-2 text-sm font-semibold text-foreground">
              <Quote className="size-4 text-primary" aria-hidden="true" />
              {t("Citiraj zapis", "Cite this record")}
            </h2>
            <p className="mt-2 font-mono text-xs leading-6 text-foreground/80">
              {t("Muzej vasi Griblje", "Griblje Village Museum")} (2026). „{title}“.{" "}
              {t("Zapis", "Record")} {exhibit.museumNo} · {exhibit.slug}. {t("Licenca CC BY-SA 4.0.", "License CC BY-SA 4.0.")}
            </p>
          </section>

          {/* zapis na sprehodu */}
          {extra?.walk && (
            <section className="mt-6 rounded-lg border border-primary/30 bg-primary/5 p-4" aria-labelledby="sprehod">
              <h2 id="sprehod" className="flex items-center gap-2 text-sm font-semibold text-foreground">
                <Footprints className="size-4 text-primary" aria-hidden="true" />
                {t("Zapis na sprehodu", "Record on a walk")}
              </h2>
              <p className="mt-2 text-sm font-medium text-foreground">{extra.walk.name}</p>
              {extra.walk.station != null && (
                <p className="mt-1 text-xs text-muted-foreground">
                  {t(
                    `Postaja ${extra.walk.station} / ${extra.walk.total} · na sprehodu`,
                    `Station ${extra.walk.station} / ${extra.walk.total} · on the walk`,
                  )}
                </p>
              )}
              {extra.walk.note && (
                <p className="mt-2 text-xs leading-relaxed text-foreground/80">
                  <span className="font-medium">{t("Kuratorska opomba postaje", "Curatorial note")}: </span>
                  {extra.walk.note}
                </p>
              )}
            </section>
          )}

          {/* sorodni zapisi */}
          {extra && extra.related.length > 0 && (
            <section className="mt-6" aria-labelledby="sorodni">
              <h2 id="sorodni" className="flex items-center gap-2 font-display text-xl font-semibold">
                <MapPin className="size-4 text-primary" aria-hidden="true" />
                {t("Sorodni zapisi", "Related records")}
              </h2>
              <p className="mt-1 text-xs text-muted-foreground">
                {t(
                  "Povezave, ki jih nosijo skupna dejstva — isti vir, isto obdobje, bližina.",
                  "Connections carried by shared facts — same source, same period, proximity.",
                )}
              </p>
              <ul className="mt-4 grid gap-3 sm:grid-cols-2">
                {extra.related.map((r) => (
                  <li key={r.slug}>
                    <button
                      type="button"
                      onClick={() => onOpen(r.slug)}
                      className="group flex h-full min-h-11 w-full flex-col gap-2 rounded-lg border p-4 text-left transition-colors hover:border-primary/40"
                    >
                      <span className="text-xs font-semibold text-primary">{r.museumNo}</span>
                      <span className="text-sm font-semibold leading-snug">{r.title}</span>
                      {r.reasons.length > 0 && (
                        <span className="mt-auto flex flex-wrap gap-1">
                          {r.reasons.map((reason) => (
                            <span
                              key={reason}
                              className="rounded-full bg-muted px-2 py-0.5 text-[10px] text-muted-foreground"
                            >
                              {reason}
                            </span>
                          ))}
                        </span>
                      )}
                    </button>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* lokacija zapisa */}
          {exhibit.lat != null && exhibit.lng != null && (
            <section className="mt-6" aria-labelledby="kje">
              <h2 id="kje" className="flex items-center gap-2 font-display text-xl font-semibold">
                <MapPin className="size-5 text-primary" aria-hidden="true" />
                {t("Kje", "Where")}
              </h2>
              <a
                href={`https://www.openstreetmap.org/?mlat=${exhibit.lat.toFixed(5)}&mlon=${exhibit.lng.toFixed(5)}#map=17/${exhibit.lat.toFixed(5)}/${exhibit.lng.toFixed(5)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-2 inline-flex min-h-11 items-center gap-2 rounded-full border px-4 py-2 text-xs font-medium transition-colors hover:border-primary/40 hover:text-primary"
              >
                <ExternalLink className="size-3.5" aria-hidden="true" />
                {exhibit.coordsApprox
                  ? t("Kraj približno → karta OpenStreetMap", "Place approximate → OpenStreetMap map")
                  : t("Prikaži na karti OpenStreetMap", "Show on OpenStreetMap map")}
              </a>
            </section>
          )}

          <p className="mt-8 border-t pt-4 text-[11px] leading-relaxed text-muted-foreground">
            {t(
              "Muzej vasi Griblje · Digitalni muzej resnične vasi ob Kolpi · Vsebina zapisa: CC BY-SA 4.0 · Odprti podatki: /api/exhibits",
              "Griblje Village Museum · A digital museum of a real village on the Kolpa · Record content: CC BY-SA 4.0 · Open data: /api/exhibits",
            )}
          </p>
        </div>
      </SheetContent>
    </Sheet>
  );
}

export function ExhibitDetailFallback() {
  return <Fragment />;
}
