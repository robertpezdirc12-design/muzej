"use client";

/**
 * Skupna trgovina časovnega stroja (issue #10, razširjeno #11).
 *
 * Zemljevid muzeja, AR vodnik in ATLAS 1825 odpirajo isti celozaslonski
 * 3D rekonstrukciji vasi; globa povezava `?casovni=1825|1900|danes`
 * (od #11 tudi `&spot=<id>` AR Time Spota) jo odpre direktno na izbrani
 * letnici s kontekstom točke.
 */

import { create } from "zustand";

export type TimeYear = 1825 | 1900 | 2026;

interface TimeMachineState {
  open: boolean;
  year: TimeYear;
  /** AR Time Spot kontekst (id iz TIME_SPOTS) ali null */
  spot: string | null;
  openTM: (year?: TimeYear, spot?: string | null) => void;
  close: () => void;
  setYear: (year: TimeYear) => void;
  setSpot: (spot: string | null) => void;
}

export const useTimeMachine = create<TimeMachineState>((set) => ({
  open: false,
  year: 1825,
  spot: null,
  openTM: (year, spot) =>
    set({ open: true, ...(year ? { year } : {}), spot: spot ?? null }),
  close: () => set({ open: false }),
  setYear: (year) => set({ year }),
  setSpot: (spot) => set({ spot }),
}));

/** ?casovni= → TimeYear (neveljavno → 1825) */
export function parseYearParam(v: string | null): TimeYear | null {
  if (!v) return null;
  if (v === "1825") return 1825;
  if (v === "1900") return 1900;
  if (v === "danes" || v === "2026") return 2026;
  return null;
}
