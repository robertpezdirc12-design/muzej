"use client";

/**
 * Skupna trgovina časovnega stroja (issue #10, razširjeno #11 in #12).
 *
 * Zemljevid muzeja, AR vodnik in ATLAS 1825 odpirajo isti celozaslonski
 * 3D rekonstrukciji vasi; globa povezava `?casovni=1825|1900|danes`
 * (od #11 tudi `&spot=<id>` AR Time Spota, od #12 pa `&360=1` — virtualni
 * 360° pogled s cerkve) jo odpre direktno na izbrani letnici s kontekstom.
 */

import { create } from "zustand";

export type TimeYear = 1825 | 1900 | 2026;

interface TimeMachineState {
  open: boolean;
  year: TimeYear;
  /** AR Time Spot kontekst (id iz TIME_SPOTS) ali null */
  spot: string | null;
  /** 360° način — fiksno stališče pri cerkvi sv. Vida (issue #12) */
  p360: boolean;
  openTM: (year?: TimeYear, spot?: string | null, p360?: boolean) => void;
  close: () => void;
  setYear: (year: TimeYear) => void;
  setSpot: (spot: string | null) => void;
  setP360: (on: boolean) => void;
}

export const useTimeMachine = create<TimeMachineState>((set) => ({
  open: false,
  year: 1825,
  spot: null,
  p360: false,
  openTM: (year, spot, p360) =>
    set({
      open: true,
      ...(year ? { year } : {}),
      spot: spot ?? null,
      p360: p360 ?? false,
    }),
  close: () => set({ open: false, p360: false }),
  setYear: (year) => set({ year }),
  setSpot: (spot) => set({ spot }),
  setP360: (on) => set({ p360: on }),
}));

/** ?casovni= → TimeYear (neveljavno → 1825) */
export function parseYearParam(v: string | null): TimeYear | null {
  if (!v) return null;
  if (v === "1825") return 1825;
  if (v === "1900") return 1900;
  if (v === "danes" || v === "2026") return 2026;
  return null;
}
