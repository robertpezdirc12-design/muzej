"use client";

/**
 * Geolokacija za AR vodnika — watchPosition z visoko natančnostjo.
 *
 * Zagon je VEDNO ročen (gumb »Priklopi GPS«): brskalniki zahtevajo
 * dejanje uporabnika za dovoljenje, implicitno spraševanje je slab bonton.
 * Na strežniku (SSR) hook mirno počiva — vse je za odjemalcem.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import type { GeoFix } from "@/lib/geo";

export type GeoStatus =
  | "idle" // še nismo zažegnali
  | "watching" // spremljamo
  | "denied" // uporabnik zavrnil
  | "unsupported" // brskalnik brez geolokacije
  | "error"; // druga napaka (časovna omejitev …)

export interface UseGeolocation {
  fix: GeoFix | null;
  status: GeoStatus;
  /** kratek opis napake za prikaz (null, če je vse v redu) */
  error: string | null;
  start: () => void;
  stop: () => void;
}

export function useGeolocation(): UseGeolocation {
  const [fix, setFix] = useState<GeoFix | null>(null);
  const [status, setStatus] = useState<GeoStatus>("idle");
  const [error, setError] = useState<string | null>(null);
  const watchRef = useRef<number | null>(null);

  const stop = useCallback(() => {
    if (watchRef.current != null && typeof navigator !== "undefined") {
      navigator.geolocation.clearWatch(watchRef.current);
      watchRef.current = null;
    }
    setStatus("idle");
    setFix(null);
  }, []);

  const start = useCallback(() => {
    if (typeof navigator === "undefined" || !navigator.geolocation) {
      setStatus("unsupported");
      return;
    }
    if (watchRef.current != null) return; // že teče

    setStatus("watching");
    setError(null);

    watchRef.current = navigator.geolocation.watchPosition(
      (pos) => {
        setFix({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
          accuracy: pos.coords.accuracy ?? null,
          heading:
            pos.coords.heading != null && !Number.isNaN(pos.coords.heading)
              ? pos.coords.heading
              : null,
          timestamp: pos.timestamp,
        });
      },
      (err) => {
        if (err.code === err.PERMISSION_DENIED) setStatus("denied");
        else {
          setStatus("error");
          setError(err.message);
        }
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 5000 },
    );
  }, []);

  /* varnostno: ob odklopu komponente prenehamo spremljati */
  useEffect(() => {
    return () => {
      if (watchRef.current != null && typeof navigator !== "undefined") {
        navigator.geolocation.clearWatch(watchRef.current);
        watchRef.current = null;
      }
    };
  }, []);

  return { fix, status, error, start, stop };
}
