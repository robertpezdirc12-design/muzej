"use client";

/**
 * Kompas-kalibracija (issue #14, točka 7) — trajna shramba odmika kompasa
 * za to napravo (localStorage mvg-compass-cal). Kalibracija je PROSTOVOLJNA:
 * uporabnik jo preskoči, AR deluje tudi brez nje (surov kompas + vlečenje).
 */

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface CompassCalState {
  /** izmerjen odmik (°) — prišteje se surovemu headingu */
  offsetDeg: number | null;
  /** kdaj je bila kalibracija narejena (epoch ms) */
  calibratedAt: number | null;
  /** ali je uporabnik kalibracijo trajno preskočil */
  dismissed: boolean;
  /** kateri cilj je bil uporabljen (npr. anchor-cerkev) */
  targetSi: string | null;
  setCalibration: (offsetDeg: number, targetSi: string) => void;
  dismiss: () => void;
  reset: () => void;
}

export const useCompassCal = create<CompassCalState>()(
  persist(
    (set) => ({
      offsetDeg: null,
      calibratedAt: null,
      dismissed: false,
      targetSi: null,
      setCalibration: (offsetDeg, targetSi) =>
        set({ offsetDeg, calibratedAt: Date.now(), targetSi, dismissed: false }),
      dismiss: () => set({ dismissed: true }),
      reset: () =>
        set({ offsetDeg: null, calibratedAt: null, targetSi: null, dismissed: false }),
    }),
    { name: "mvg-compass-cal" },
  ),
);
