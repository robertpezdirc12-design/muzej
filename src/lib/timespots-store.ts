"use client";

/**
 * Zbirka odklenjenih AR TIME SPOTOV (issue #11).
 *
 * TimeLens vzorec: obiskovalec ob prihodu ODKLENE točko; obisk ostane
 * v zbirki (ponovni ogled, tudi offline). Shranjeno lokalno v brskalniku
 * (localStorage) — brez računa, brez strežnika, brez sledenja.
 */

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { TIME_SPOTS } from "@/data/atlas/timespots";

interface TimespotsState {
  unlocked: string[];
  unlock: (id: string) => void;
  isUnlocked: (id: string) => boolean;
  reset: () => void;
}

export const useTimespots = create<TimespotsState>()(
  persist(
    (set, get) => ({
      unlocked: [],
      unlock: (id) =>
        set((s) =>
          s.unlocked.includes(id) ? s : { unlocked: [...s.unlocked, id] },
        ),
      isUnlocked: (id) => get().unlocked.includes(id),
      reset: () => set({ unlocked: [] }),
    }),
    { name: "mvg-timespots" },
  ),
);

/** Skupno število točk (za prikaz »x / n odklenjenih«). */
export const TOTAL_SPOTS = TIME_SPOTS.length;
