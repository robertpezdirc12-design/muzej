"use client";

import { motion } from "framer-motion";
import { MapPin, BookOpen, ShieldCheck, Languages } from "lucide-react";
import { useLang } from "./language-context";
import { STATS } from "@/lib/museum";

export function MuseumHero() {
  const { t } = useLang();

  const stats = [
    {
      icon: BookOpen,
      value: String(STATS.exhibits),
      si: "zapisov v zbirki",
      en: "records in the collection",
    },
    {
      icon: MapPin,
      value: String(STATS.firstYear),
      si: "prva omemba vasi",
      en: "first record of the village",
    },
    {
      icon: ShieldCheck,
      value: String(STATS.sources),
      si: "dokazljivih virov",
      en: "verifiable sources",
    },
    {
      icon: Languages,
      value: "SI · EN",
      si: "dvojezična postavitev",
      en: "bilingual exhibition",
    },
  ];

  return (
    <section className="muzej-paper relative border-b border-border/60" aria-labelledby="hero-naslov">
      <div className="mx-auto grid max-w-6xl gap-10 px-4 py-14 sm:px-6 sm:py-20 lg:grid-cols-[1.1fr_1fr] lg:items-center">
        <div>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-medium text-primary"
          >
            <MapPin className="size-3.5" aria-hidden="true" />
            {t("Bela krajina · občina Črnomelj · ob Kolpi", "Bela krajina · Municipality of Črnomelj · on the Kolpa")}
          </motion.p>

          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, delay: 0.06 }}
            id="hero-naslov"
            className="mt-5 font-display text-4xl font-semibold leading-[1.08] tracking-tight text-foreground sm:text-5xl lg:text-6xl"
          >
            {t("Muzej vasi Griblje", "The Griblje Village Museum")}
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, delay: 0.12 }}
            className="mt-4 max-w-xl text-base leading-relaxed text-foreground/80 sm:text-lg"
          >
            {t(
              "Digitalni muzej resnične vasi ob Kolpi. Vsak zapis nosi muzejsko številko, dokazljive vire in lestvico zanesljivosti — zgodovina, katere sledi lahko preverite sami.",
              "A digital museum of a real village on the Kolpa river. Every record carries a museum number, verifiable sources and a reliability scale — history whose traces you can check yourself.",
            )}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, delay: 0.18 }}
            className="mt-7 flex flex-wrap gap-3"
          >
            <a
              href="#register"
              className="inline-flex h-11 items-center justify-center rounded-md bg-primary px-6 text-sm font-semibold text-primary-foreground shadow-sm transition-colors hover:bg-primary/90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
            >
              {t("Vstopi v zbirko", "Enter the collection")}
            </a>
            <a
              href="#stories"
              className="inline-flex h-11 items-center justify-center rounded-md border border-border bg-card px-6 text-sm font-semibold text-foreground shadow-sm transition-colors hover:border-primary/40 hover:bg-secondary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
            >
              {t("Preberi zgodbe", "Read the stories")}
            </a>
          </motion.div>
        </div>

        <motion.figure
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.65, delay: 0.15 }}
          className="relative overflow-hidden rounded-xl border border-border shadow-lg"
        >
          <img
            src="/images/authentic/griblje-vas.jpg"
            alt={t(
              "Vas Griblje ob Kolpi — panorama z Gorjanci v ozadju",
              "The village of Griblje on the Kolpa — panorama with the Gorjanci in the background",
            )}
            className="h-64 w-full object-cover sm:h-80 lg:h-96"
            loading="eager"
          />
          <figcaption className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 to-transparent p-4 pt-10 text-[11px] leading-snug text-white/90">
            Foto: Andrejj · Wikimedia Commons · CC BY-SA 3.0 — vas Griblje ob Kolpi
          </figcaption>
        </motion.figure>
      </div>

      <dl className="mx-auto grid max-w-6xl grid-cols-2 gap-px overflow-hidden border-t border-border/60 bg-border/40 sm:grid-cols-4">
        {stats.map((s) => (
          <div key={s.si} className="flex flex-col gap-1 bg-background px-4 py-5 sm:px-6">
            <dt className="flex items-center gap-2 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              <s.icon className="size-3.5 text-primary" aria-hidden="true" />
              {t(s.si, s.en)}
            </dt>
            <dd className="font-display text-2xl font-semibold text-foreground sm:text-3xl">
              {s.value}
            </dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
