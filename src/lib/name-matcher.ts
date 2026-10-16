// name-matcher.ts — deterministični ujemovalnik priimkov 1886 ↔ imena 1825 (P81).
// Zrcali Python izvedbo v scripts/p81_parish_name_linkage.py (norm/pass1+pass2,
// Levenshtein razmerje, stoplist krstnih imen, uredniški žetoni, sorted
// tie-break); vsaka sprememba tukaj MORA biti zrcaljena v Python skripto in
// obratno (I5 determinizem). Prag 0.72 = ponovna uporaba praga P43 W-most.

export const P81_THRESHOLD = 0.72;
export const P81_NEAR_MISS = 0.55;

const MIN_TOKEN = 4;
const EXACT_LEN = 5;

/** Krstna imena (stoplist) — verbatim iz vesolja 1825; zrcali Python
 * GIVEN_NAME_TOKENS. */
const GIVEN_NAME_TOKENS = new Set([
  "wufa", "luina", "ludwig", "michael", "migan", "malfa", "miklo", "mis",
  "martin", "johann", "jhan", "johan", "janez", "mada", "manda", "magdalena",
  "mako", "matho", "mufa", "matthaus", "nicolaus", "georg", "gregor",
  "jurgen", "peter", "jetter", "miho", "musto", "marko", "mihel", "maro",
  "maffa", "juttan", "jakob", "laurentz", "stoffe", "mariz", "mihlo",
  "manko", "pitter", "mida", "wolf", "michl", "matja", "matija", "jurij",
  "hanss", "matha", "mattha", "niklo", "baron",
]);

/** Uredniški žetoni (puaRef »[PT rokopis: …]«, PUA »(alternative: …)«). */
const EDITORIAL_TOKENS = new Set([
  "rokopis", "alternative", "alternativa", "institucija", "institucionalna",
]);

const TRANS: Record<string, string> = {
  š: "s", ž: "z", č: "c", ć: "c", ß: "ss", ä: "a", ö: "o", ü: "u", ŕ: "r",
  á: "a", é: "e", è: "e", ê: "e", ì: "i", ù: "u", ſ: "s",
};

function stripCombining(s: string): string {
  return s.normalize("NFD").replace(/\p{M}/gu, "");
}

/** pass1: male črke + de-diacritika; pass2 (german): + nem. Kurrent sch→s. */
export function p81Norm(s: string, german = false): string {
  let t = s.toLowerCase();
  t = t.replace(/[šžčćßäöüŕáéèêìùſ]/g, (c) => TRANS[c] ?? c);
  t = stripCombining(t);
  t = t.replace(/\[~\]|\[\?\]/g, " ");
  t = t.replace(/[^a-z]+/g, " ");
  t = t.replace(/\s+/g, " ").trim();
  if (german) t = t.replace(/sch/g, "s");
  return t;
}

function round4(x: number): number {
  return Math.round((x + 1e-12) * 10000) / 10000;
}

/** Levenshtein razdalja (standardni DP; zrcali Python). */
export function p81Lev(a: string, b: string): number {
  if (a === b) return 0;
  if (!a) return b.length;
  if (!b) return a.length;
  let prev = new Array<number>(b.length + 1);
  for (let j = 0; j <= b.length; j++) prev[j] = j;
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    for (let j = 1; j <= b.length; j++) {
      cur[j] = Math.min(
        prev[j] + 1,
        cur[j - 1] + 1,
        prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1),
      );
    }
    prev = cur;
  }
  return prev[b.length];
}

/** Razmerje 1 − d/max, zaokroženo na 4 decimalki (zrcali Python r4). */
export function p81Sim(a: string, b: string): number {
  const m = Math.max(a.length, b.length);
  return m ? round4(1 - p81Lev(a, b) / m) : 0;
}

/** Žetoni 1825 imena: unija pass1+pass2, ≥ 4 znake, brez krstnih/uredniških;
 * SORTIRANI (determinističen tie-break — zrcali Python sorted(tokens)). */
export function p81Tokens(name: string): string[] {
  const out = new Set<string>();
  for (const german of [false, true]) {
    for (const t of p81Norm(name, german).split(" ")) {
      if (t.length >= MIN_TOKEN && !GIVEN_NAME_TOKENS.has(t) && !EDITORIAL_TOKENS.has(t)) {
        out.add(t);
      }
    }
  }
  return [...out].sort();
}

export interface P81Match {
  score: number;
  pass: 1 | 2;
  token: string;
}

/** Najboljše razmerje priimka 1886 proti žetonom 1825 imena; kratki priimki
 * (< 5 znakov) LE natančna enakost žetona (zrcali Python best_match). */
export function p81BestMatch(surname: string, name1825: string): P81Match | null {
  let best: P81Match | null = null;
  for (const german of [1, 2] as const) {
    const sn = p81Norm(surname, german === 2);
    if (!sn || sn.length < MIN_TOKEN) continue;
    const exactOnly = sn.length < EXACT_LEN;
    for (const tok of p81Tokens(name1825)) {
      let sc: number | null = null;
      if (exactOnly) {
        if (tok === sn) sc = 1;
      } else {
        sc = p81Sim(sn, tok);
      }
      if (sc !== null && (best === null || sc > best.score)) {
        best = { score: sc, pass: german, token: tok };
      }
    }
  }
  return best;
}
