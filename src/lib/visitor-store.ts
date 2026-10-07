"use client";

/**
 * MUSEUM VISITOR EXPERIENCE — stanje obiska (issue #15).
 *
 * Obiskovalčeva pot: prihod → dobrodošlica → voden ogled → raziskovanje
 * → zbiranje odkritij → zaključek → deljenje spomina.
 *
 * Pošteno arhitektura: to stanje NE podvaja zbirke odkritij — odklenjene
 * točke ostanejo v useTimespots (collection sistem, issue #11). Ta
 * trgovina hrani le okvir obiska: kdaj je začel, katero osebo je izbral,
 * ali je zaključil in ali je shranil spomin.
 *
 * Shranjeno lokalno (localStorage) — brez računa, brez strežnika,
 * brez sledenja (enak vzorec kot mvg-timespots).
 */

import { create } from "zustand";
import { persist } from "zustand/middleware";

/** Osebe obiskovalcev (issue #15, točka 8) — osnova, ne nov sistem. */
export type VisitorPersona = "druzina" | "sola" | "turist" | "raziskovalec";

interface VisitorState {
  /** ali je obiskovalec začel muzejski obisk */
  started: boolean;
  /** ISO datum začetka obiska */
  startAt: string | null;
  /** izbrana oseba (null = standardna pot) */
  persona: VisitorPersona | null;
  /** ali je obisk zaključen (ročno ali samodejno ob odklepu vseh postaj) */
  completed: boolean;
  completedAt: string | null;
  /** kdaj je shranil digitalni spomin (razglednico) */
  souvenirSavedAt: string | null;
  /** ali je videl AR onboarding (3 koraki) */
  onboardingSeen: boolean;
  /** ali je skril plavajoči dok (postaja) na mobilnem */
  dockDismissed: boolean;
  /** ali je odklical uvodni zaslon brez začetka obiska */
  startDismissed: boolean;

  startVisit: (persona?: VisitorPersona | null) => void;
  setPersona: (p: VisitorPersona) => void;
  completeVisit: () => void;
  reopenVisit: () => void;
  saveSouvenir: () => void;
  sawOnboarding: () => void;
  dismissDock: () => void;
  showDock: () => void;
  dismissStart: () => void;
  resetVisit: () => void;
}

export const useVisitor = create<VisitorState>()(
  persist(
    (set) => ({
      started: false,
      startAt: null,
      persona: null,
      completed: false,
      completedAt: null,
      souvenirSavedAt: null,
      onboardingSeen: false,
      dockDismissed: false,
      startDismissed: false,

      startVisit: (persona = null) =>
        set((s) => ({
          started: true,
          startAt: s.started ? s.startAt : new Date().toISOString(),
          persona: persona ?? s.persona,
          startDismissed: false,
        })),

      setPersona: (p) => set({ persona: p }),

      completeVisit: () =>
        set((s) => ({
          completed: true,
          completedAt: s.completed ? s.completedAt : new Date().toISOString(),
        })),

      reopenVisit: () => set({ completed: false, completedAt: null }),

      saveSouvenir: () =>
        set({ souvenirSavedAt: new Date().toISOString() }),

      sawOnboarding: () => set({ onboardingSeen: true }),

      dismissDock: () => set({ dockDismissed: true }),

      showDock: () => set({ dockDismissed: false }),

      dismissStart: () => set({ startDismissed: true }),

      resetVisit: () =>
        set({
          started: false,
          startAt: null,
          persona: null,
          completed: false,
          completedAt: null,
          souvenirSavedAt: null,
          dockDismissed: false,
          startDismissed: false,
        }),
    }),
    { name: "mvg-visit" },
  ),
);

/** Zaporedje postaj osnovne poti (issue #15 — vrstni red iz primera). */
export const CORE_STATION_ORDER = [
  "cerkev",
  "jedro",
  "kolpa",
  "ribnik",
  "gornje",
  "meja",
] as const;

/** Oseba → postaje njenega ogleda (obstoječi TimeSpot sistemi, nič novega). */
export function personaStations(persona: VisitorPersona | null): string[] {
  switch (persona) {
    case "druzina":
      /* krajša, bolj igriva pot — 3 postaje */
      return ["cerkev", "jedro", "kolpa"];
    case "raziskovalec":
      /* vsa postaja + oddaljene točke (viri in evidence) */
      return [...CORE_STATION_ORDER, "mlini", "otok", "cerkvisce"];
    default:
      /* turist, šola, standard: vseh 6 postaj vasi */
      return [...CORE_STATION_ORDER];
  }
}

/** Oseba → predviden čas ogleda (SI/EN besedilo za prikaz). */
export function personaTime(persona: VisitorPersona | null): { si: string; en: string } {
  switch (persona) {
    case "druzina":
      return { si: "20–45 minut", en: "20–45 minutes" };
    default:
      return { si: "45–90 minut", en: "45–90 minutes" };
  }
}
