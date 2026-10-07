"use client";

import { useEffect } from "react";

/* Registracija servisnega delavca — samo v produkciji, da ne moti HMR v razvoju.
   Ob novi različici se delavec sam posodobi (skipWaiting + clients.claim). */
export function ServiceWorkerRegistrar() {
  useEffect(() => {
    if (
      typeof window === "undefined" ||
      !("serviceWorker" in navigator) ||
      window.location.protocol !== "https:"
    ) {
      return;
    }
    const register = () => {
      navigator.serviceWorker
        .register("/sw.js", { scope: "/" })
        .catch(() => {
          /* namestitev ni kritična — spletišče deluje tudi brez nje */
        });
    };
    if (document.readyState === "complete") {
      register();
    } else {
      window.addEventListener("load", register, { once: true });
      return () => window.removeEventListener("load", register);
    }
  }, []);

  return null;
}
