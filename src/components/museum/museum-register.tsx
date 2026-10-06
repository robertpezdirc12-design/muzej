"use client";

import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Search, SlidersHorizontal, Star } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { useLang } from "./language-context";
import {
  filterExhibits,
  CATEGORY_LABELS,
  EVIDENCE_LABELS,
  type CategoryCode,
  type EvidenceCode,
  type Exhibit,
} from "@/lib/museum";
import { ExhibitCard } from "./exhibit-card";

type CatFilter = CategoryCode | "all";
type EvFilter = EvidenceCode | "all";

export function MuseumRegister({ onOpen }: { onOpen: (slug: string) => void }) {
  const { t } = useLang();
  const [query, setQuery] = useState("");
  const [cat, setCat] = useState<CatFilter>("all");
  const [ev, setEv] = useState<EvFilter>("all");
  const [featured, setFeatured] = useState(false);

  const results = useMemo(
    () => filterExhibits(query, cat, ev, featured),
    [query, cat, ev, featured],
  );

  return (
    <section id="register" className="scroll-mt-20" aria-labelledby="register-naslov">
      <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 id="register-naslov" className="font-display text-3xl font-semibold tracking-tight text-foreground">
              {t("Muzejski register — katalog zbirke", "Museum register — collection catalogue")}
            </h2>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              {t(
                "Vsi zapisi zbirke s trajnimi muzejskimi številkami; vsak vodi na stran zapisa. Register je natisnjen tudi na QR oznakah fizičnega muzeja.",
                "All records of the collection with permanent museum numbers; each leads to the record page. The register is also printed on the QR labels of the physical museum.",
              )}
            </p>
          </div>
          <p className="text-xs font-medium text-muted-foreground" role="status">
            {t(
              `${results.length} od ${113} zapisov`,
              `${results.length} of 113 records`,
            )}
          </p>
        </div>

        {/* iskanje in filtri */}
        <div className="mt-6 grid gap-3 rounded-xl border bg-card p-4 shadow-sm lg:grid-cols-[1fr_auto]">
          <div className="grid gap-3 sm:grid-cols-2">
            <div className="relative">
              <Search
                className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
                aria-hidden="true"
              />
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={t("Išči po naslovu, številki, obdobju …", "Search by title, number, period …")}
                className="h-11 pl-10"
                aria-label={t("Iskanje po zbirki", "Search the collection")}
              />
            </div>
            <div className="flex items-center gap-3 rounded-lg border px-4">
              <Switch
                id="featured-filter"
                checked={featured}
                onCheckedChange={setFeatured}
                aria-label={t("Samo izpostavljeni zapisi", "Featured records only")}
              />
              <Label
                htmlFor="featured-filter"
                className="flex cursor-pointer items-center gap-1.5 text-sm text-muted-foreground"
              >
                <Star className="size-3.5 text-primary" aria-hidden="true" />
                {t("Samo izpostavljeni", "Featured only")}
              </Label>
            </div>
          </div>
        </div>

        <div className="mt-4 flex flex-wrap items-center gap-2" aria-label={t("Filter po kategoriji", "Filter by category")}>
          <span className="flex items-center gap-1 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            <SlidersHorizontal className="size-3.5" aria-hidden="true" />
            {t("Zbirke", "Collections")}
          </span>
          <FilterChip active={cat === "all"} onClick={() => setCat("all")}>
            {t("Vse", "All")}
          </FilterChip>
          {(Object.keys(CATEGORY_LABELS) as CategoryCode[]).map((c) => (
            <FilterChip key={c} active={cat === c} onClick={() => setCat(c)}>
              {t(CATEGORY_LABELS[c].si, CATEGORY_LABELS[c].en)}
            </FilterChip>
          ))}
        </div>

        <div className="mt-2 flex flex-wrap items-center gap-2" aria-label={t("Filter po zanesljivosti", "Filter by evidence")}>
          <span className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            {t("Zanesljivost", "Evidence")}
          </span>
          <FilterChip active={ev === "all"} onClick={() => setEv("all")}>
            {t("Vse ravni", "All levels")}
          </FilterChip>
          {(Object.keys(EVIDENCE_LABELS) as EvidenceCode[]).map((code) => (
            <FilterChip key={code} active={ev === code} onClick={() => setEv(code)}>
              {t(EVIDENCE_LABELS[code].si, EVIDENCE_LABELS[code].en)}
            </FilterChip>
          ))}
        </div>

        {/* mreža kartic */}
        {results.length > 0 ? (
          <ul className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3" aria-live="polite">
            {results.map((e, i) => (
              <motion.li
                key={e.slug}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: Math.min(i * 0.015, 0.4) }}
              >
                <ExhibitCard exhibit={e} onOpen={onOpen} />
              </motion.li>
            ))}
          </ul>
        ) : (
          <div className="mt-10 rounded-xl border border-dashed p-10 text-center">
            <p className="text-sm font-medium text-foreground">
              {t("Ni zapisov, ki ustrezajo iskanju.", "No records match your search.")}
            </p>
            <Button
              variant="outline"
              size="sm"
              className="mt-4"
              onClick={() => {
                setQuery("");
                setCat("all");
                setEv("all");
                setFeatured(false);
              }}
            >
              {t("Počisti filtre", "Clear filters")}
            </Button>
          </div>
        )}
      </div>
    </section>
  );
}

function FilterChip({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={`inline-flex min-h-9 items-center rounded-full border px-3.5 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring ${
        active
          ? "border-primary/50 bg-primary/10 text-primary"
          : "border-border bg-card text-muted-foreground hover:border-primary/30 hover:text-foreground"
      }`}
    >
      {children}
    </button>
  );
}

export function EvidenceBadge({ code, className }: { code: EvidenceCode; className?: string }) {
  const { t } = useLang();
  const labels = EVIDENCE_LABELS[code];
  if (!labels) return null;
  return (
    <Badge
      variant="outline"
      className={`gap-1 border-primary/30 bg-primary/10 text-primary ${className ?? ""}`}
    >
      {t(labels.si, labels.en)}
    </Badge>
  );
}

export function CategoryBadge({ code }: { code: CategoryCode }) {
  const { t } = useLang();
  const labels = CATEGORY_LABELS[code];
  if (!labels) return null;
  return (
    <Badge variant="secondary" className="font-normal text-muted-foreground">
      {t(labels.si, labels.en)}
    </Badge>
  );
}

export type { Exhibit };
