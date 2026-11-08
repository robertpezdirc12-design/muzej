"use client";

import {
  MapPin,
  Sparkles,
  Shield,
  Wheat,
  Leaf,
  Waves,
  CameraOff,
  type LucideIcon,
} from "lucide-react";
import type { CategoryCode } from "@/lib/museum";
import { useLang } from "./language-context";

/** ikone kategorij — enak zemljevid kot v CATEGORY_LABELS (museum.ts) */
const CATEGORY_ICONS: Record<CategoryCode, LucideIcon> = {
  kraj: MapPin,
  sege: Sparkles,
  vojna: Shield,
  gospodarstvo: Wheat,
  narava: Leaf,
  kolpa: Waves,
};

/** vodrtli arhivski list — papirnati vzorec, ki sledi svetli/temni temi */
const paperStyle: React.CSSProperties = {
  backgroundImage:
    "repeating-linear-gradient(180deg, transparent 0px, transparent 31px, " +
    "color-mix(in oklch, var(--primary) 10%, transparent) 31px, " +
    "color-mix(in oklch, var(--primary) 10%, transparent) 32px)",
};

/**
 * Arhivski list namesto fotografije v kartici registra.
 * Muzejska praksa: zapis je objavljen, fotografija predmeta še čaka.
 */
export function ArchivalCardImage({
  category,
}: {
  category: CategoryCode;
}) {
  const { t } = useLang();
  const Icon = CATEGORY_ICONS[category] ?? CameraOff;

  return (
    <div
      className="relative h-full w-full overflow-hidden bg-secondary"
      style={paperStyle}
      aria-hidden="true"
    >
      {/* robna črta arhivskega lista */}
      <span className="absolute inset-y-0 left-8 w-px bg-primary/30" />
      <div className="flex h-full w-full flex-col items-center justify-center gap-2.5 px-6 text-center">
        <span className="flex size-10 items-center justify-center rounded-full border border-primary/25 bg-background/60 backdrop-blur">
          <Icon className="size-4 text-primary/70" />
        </span>
        <span className="inline-flex items-center gap-1.5 rounded-full border border-border bg-background/70 px-2.5 py-1 text-[10px] font-medium uppercase tracking-wider text-muted-foreground backdrop-blur">
          <CameraOff className="size-3" />
          {t("Fotografija v pripravi", "Photograph pending")}
        </span>
      </div>
    </div>
  );
}

/**
 * Arhivski pas v glavi podrobnostnega lista, kadar zapis nima fotografije.
 * Ohranja višino in kompozicijo fotografske glave, a kot registratorni list.
 */
export function ArchivalHeaderBand({
  museumNo,
  category,
}: {
  museumNo: string;
  category: CategoryCode;
}) {
  const { t } = useLang();
  const Icon = CATEGORY_ICONS[category] ?? CameraOff;

  return (
    <div
      className="relative h-56 w-full overflow-hidden bg-secondary sm:h-64"
      style={paperStyle}
      aria-hidden="true"
    >
      <span className="absolute inset-y-0 left-8 w-px bg-primary/30" />
      {/* vodni žig — invencijska številka */}
      <span className="pointer-events-none absolute -bottom-4 right-3 select-none font-mono text-8xl font-bold leading-none tracking-tighter text-primary/10">
        {museumNo}
      </span>
      <div className="absolute bottom-4 left-12">
        <span className="inline-flex items-center gap-1.5 rounded-full border border-border bg-background/75 px-3 py-1 text-[10px] font-medium uppercase tracking-wider text-muted-foreground backdrop-blur">
          <CameraOff className="size-3" />
          {t("Fotografija zapisa je v pripravi", "Record photograph pending")}
        </span>
      </div>
      <span className="absolute right-4 top-4 flex size-10 items-center justify-center rounded-full border border-primary/20 bg-background/60 backdrop-blur">
        <Icon className="size-4 text-primary/70" />
      </span>
    </div>
  );
}
