/**
 * DETERMINISTIČNI NARRATOR (P15) — edini govorilni mehanizem muzeja.
 *
 * Načelo: GLAS MUZEJA SO SKRIPTE. Besedila so kuratorsko pripravljena
 * (govorne skripte časovnih točk v src/data/atlas/narrations.ts,
 * kuratorska besedila zapisov pri vodenem sprehodu in AR kamere) —
 * predvaja jih izključno brskalnikova vgrajena speechSynthesis:
 *   · zastonj — nobenega plačljivega API-ja,
 *   · lokalno — nobenega omrežnega klica,
 *   · brez AI modelov — nobenega TTS v oblaku, nobenih ključev.
 *
 * Vsi trije glasovi muzeja (časovni stroj, vodeni sprehod, AR kamera)
 * gredo čez ta modul: enaka izbira glasu za jezik, enaka hitrost,
 * enak življenjski cikel. Kvaliteta glasu je odvisna od naprave
 * obiskovalca — to je pošteno zapisano tudi v UI.
 */

export type NarrationLang = "si" | "en";

/** Je govor podprt na tej napravi? (Varno tudi ob strežniškem izrisu.) */
export function narrationSupported(): boolean {
  return (
    typeof window !== "undefined" &&
    typeof window.speechSynthesis !== "undefined"
  );
}

/** Prekini predvajanje (varno tudi, če sinteze ni). */
export function stopNarration(): void {
  if (narrationSupported()) window.speechSynthesis.cancel();
}

/**
 * Preberi skripto na glas.
 *
 * @param text besedilo skripte (za govor; enako besedilo je transkript)
 * @param lang jezik — določa izbiro glasu (sl-SI / en-GB)
 * @param onDone klic ob koncu, napaki ali prekinitvi (točno enkrat)
 * @returns true, če je predvajanje zagnano; false, če sinteze ni —
 *          klicnik lahko namesto govora pokaže transkript.
 */
export function speakScript(
  text: string,
  lang: NarrationLang,
  onDone: () => void,
): boolean {
  if (!narrationSupported()) return false;
  const synth = window.speechSynthesis;
  synth.cancel();

  const u = new SpeechSynthesisUtterance(text);
  const want = lang === "si" ? "sl" : "en";
  /* izberi glas ciljnega jezika, če ga naprava ima (seznam glasov se
     nalaga asinhrono — ob prvem klicu je lahko še prazen) */
  const voices = synth.getVoices();
  const v =
    voices.find((x) => x.lang.toLowerCase().startsWith(want)) ??
    voices.find((x) => x.lang.toLowerCase().startsWith("en"));
  if (v) u.voice = v;
  u.lang = lang === "si" ? "sl-SI" : "en-GB";
  u.rate = 0.95;

  let settled = false;
  const done = () => {
    if (!settled) {
      settled = true;
      onDone();
    }
  };
  u.onend = done;
  u.onerror = done;

  synth.speak(u);
  return true;
}
