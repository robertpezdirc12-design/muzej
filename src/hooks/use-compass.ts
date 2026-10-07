"use client";

/**
 * Kompas za AR (issue #14, točki 7–8) — surov DeviceOrientation nikoli
 * ne gre naravnost v sceno:
 *
 *  · glajenje: eksponentni low-pass (α = 0,3) — scena se premika mehko;
 *  · zavrnitev odstopnikov: skok > 25° v vzorcu zavržen, razen če se nadaljuje
 *    v isti smeri (resnični hiter obrat telefona);
 *  · prag gibanja: spremembe < 0,4° ne sprožijo posodobitve stanja;
 *  · stabilnost: stddev zadnjih 8 vzorcev → stable (≤ 2°) / settling (≤ 6°)
 *    / unstable — UI pokaže »Poravnava kompasa …« in scena ne skače;
 *  · iOS: dovoljenje prek DeviceOrientationEvent.requestPermission();
 *  · kalibracija: prišteje trajni odmik iz useCompassCal (issue #14, točka 7).
 *
 * Na SSR hook mirno počiva (heading = null, stability = unavailable).
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { useCompassCal } from "@/lib/compass-cal";
import type { CompassStability } from "@/data/atlas/geotruth";

export interface UseCompass {
  /** glajen heading z odmikom kalibracije [0, 360), null = ni podatka */
  heading: number | null;
  /** surov (neglajen) heading brez odmika — za diagnostiko */
  rawHeading: number | null;
  stability: CompassStability;
  /** iOS zahteva eksplicitno dovoljenje za gibanje naprave */
  needsPermission: boolean;
  requestPermission: () => Promise<void>;
}

interface DeviceOrientationEventIOS extends DeviceOrientationEvent {
  webkitCompassHeading?: number;
}

const ALPHA_SMOOTH = 0.3;
const OUTLIER_DEG = 25;
const MOVE_EPS = 0.4;
const STABLE_SIGMA = 2.0;
const SETTLING_SIGMA = 6.0;
const WINDOW = 8;

function norm360(deg: number): number {
  return ((deg % 360) + 360) % 360;
}

function angleDelta(from: number, to: number): number {
  return ((to - from + 540) % 360) - 180;
}

export function useCompass(): UseCompass {
  const [heading, setHeading] = useState<number | null>(null);
  const [rawHeading, setRawHeading] = useState<number | null>(null);
  const [stability, setStability] = useState<CompassStability>("unavailable");
  const [needsPermission, setNeedsPermission] = useState(false);

  const offset = useCompassCal((s) => s.offsetDeg);
  const offsetRef = useRef(offset);
  useEffect(() => {
    offsetRef.current = offset;
  }, [offset]);

  const smoothRef = useRef<number | null>(null);
  const lastOutlierRef = useRef<number | null>(null);
  const samplesRef = useRef<number[]>([]);
  const lastEmittedRef = useRef<number | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const onOrient = (e: DeviceOrientationEvent) => {
      const ios = e as DeviceOrientationEventIOS;
      let raw: number | null = null;
      if (typeof ios.webkitCompassHeading === "number") {
        raw = norm360(ios.webkitCompassHeading);
      } else if (e.alpha != null) {
        raw = norm360(360 - e.alpha);
      }
      if (raw == null) return;
      setRawHeading(raw);

      /* zavrnitev odstopnikov: skok > 25° je sumljiv, razen če gre za
         nadaljevanje prejšnjega skoka (hiter obrat) ali resnično hitro vrtenje */
      const prev = smoothRef.current;
      if (prev != null) {
        const d = Math.abs(angleDelta(prev, raw));
        if (d > OUTLIER_DEG && lastOutlierRef.current == null) {
          lastOutlierRef.current = raw;
          return; /* zavržemo prvi vzorec skoka */
        }
      }
      lastOutlierRef.current = null;

      /* glajenje (low-pass prek krožne razlike) */
      const smoothed =
        prev == null ? raw : norm360(prev + ALPHA_SMOOTH * angleDelta(prev, raw));
      smoothRef.current = smoothed;

      /* stabilnost: stddev okrog glajenega povprečja */
      const samples = samplesRef.current;
      samples.push(raw);
      if (samples.length > WINDOW) samples.shift();
      let sig = 999;
      if (samples.length >= 4) {
        const deltas = samples.map((s) => angleDelta(smoothed, s));
        const mean = deltas.reduce((a, b) => a + b, 0) / deltas.length;
        sig = Math.sqrt(
          deltas.reduce((a, b) => a + (b - mean) ** 2, 0) / deltas.length,
        );
      }
      const nextStability: CompassStability =
        sig <= STABLE_SIGMA ? "stable" : sig <= SETTLING_SIGMA ? "settling" : "unstable";
      setStability(nextStability);

      /* apliciramo kalibracijski odmik + prag gibanja */
      const withOffset =
        offsetRef.current != null
          ? norm360(smoothed + offsetRef.current)
          : smoothed;
      const last = lastEmittedRef.current;
      if (last == null || Math.abs(angleDelta(last, withOffset)) >= MOVE_EPS) {
        lastEmittedRef.current = withOffset;
        setHeading(withOffset);
      }
    };

    window.addEventListener("deviceorientation", onOrient, true);
    const probe = window.setTimeout(() => {
      const DOE = DeviceOrientationEvent as typeof DeviceOrientationEvent & {
        requestPermission?: () => Promise<"granted" | "denied">;
      };
      if (typeof DOE.requestPermission === "function") setNeedsPermission(true);
    }, 900);
    return () => {
      window.removeEventListener("deviceorientation", onOrient, true);
      window.clearTimeout(probe);
    };
  }, []);

  const requestPermission = useCallback(async () => {
    const DOE = DeviceOrientationEvent as typeof DeviceOrientationEvent & {
      requestPermission?: () => Promise<"granted" | "denied">;
    };
    if (typeof DOE.requestPermission === "function") {
      try {
        const r = await DOE.requestPermission();
        if (r !== "granted") return;
      } catch {
        return;
      }
    }
    setNeedsPermission(false);
  }, []);

  return { heading, rawHeading, stability, needsPermission, requestPermission };
}
