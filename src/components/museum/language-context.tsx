"use client";

import {
  createContext,
  useCallback,
  useContext,
  useSyncExternalStore,
  type ReactNode,
} from "react";

export type Lang = "si" | "en";

const STORAGE_KEY = "mvg-lang";
const CHANGE_EVENT = "mvg-lang-change";

function subscribe(callback: () => void) {
  window.addEventListener(CHANGE_EVENT, callback);
  window.addEventListener("storage", callback);
  return () => {
    window.removeEventListener(CHANGE_EVENT, callback);
    window.removeEventListener("storage", callback);
  };
}

function getSnapshot(): Lang {
  const saved = window.localStorage.getItem(STORAGE_KEY);
  return saved === "en" ? "en" : "si";
}

function getServerSnapshot(): Lang {
  return "si";
}

interface LangContextValue {
  lang: Lang;
  setLang: (l: Lang) => void;
  t: (si: string, en: string) => string;
}

const LangContext = createContext<LangContextValue | null>(null);

export function LangProvider({ children }: { children: ReactNode }) {
  const lang = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);

  const setLang = useCallback((l: Lang) => {
    window.localStorage.setItem(STORAGE_KEY, l);
    window.dispatchEvent(new Event(CHANGE_EVENT));
    document.documentElement.lang = l;
  }, []);

  const t = useCallback(
    (si: string, en: string) => (lang === "si" ? si : en),
    [lang],
  );

  return (
    <LangContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LangContext.Provider>
  );
}

export function useLang(): LangContextValue {
  const ctx = useContext(LangContext);
  if (!ctx) {
    return { lang: "si", setLang: () => {}, t: (si) => si };
  }
  return ctx;
}
