"use client";

/**
 * Skupna trgovina časovnega stroja (issue #10).
 *
 * Zemljevid muzeja, AR vodnik in ATLAS 1825 odpirajo isti celozaslonski
 * 3D rekonstrukciji vasi; globa povezava `?casovni=1825|1900|danes`
 * jo odpre direktno na izbrani letnici.
 */

import { create } from "zustand";

export type TimeYear = 1825 | 1900 | 2026;

interface TimeMachineState {
  open: boolean;
  year: TimeYear;
  openTM: (year?: TimeYear) => void;
  close: () => void;
  setYear: (year: TimeYear) => void;
}

export const useTimeMachine = create<TimeMachineState>((set) => ({
  open: false,
  year: 1825,
  openTM: (year) => set({ open: true, ...(year ? { year } : {}) }),
  close: () => set({ open: false }),
  setYear: (year) => set({ year }),
}));

/** ?casovni= → TimeYear (neveljavno → 1825) */
export function parseYearParam(v: string | null): TimeYear | null {
  if (!v) return null;
  if (v === "1825") return 1825;
  if (v === "1900") return 1900;
  if (v === "danes" || v === "2026") return 2026;
  return null;
}
