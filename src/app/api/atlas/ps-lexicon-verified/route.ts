import { NextResponse } from "next/server";
import psLexiconVerified from "@/data/atlas/ps-lexicon-verified.json";

export const dynamic = "force-static";

/**
 * ISSUE #10 (P45) — PS 1825: verifikacija leksikografskih virov P43 leksikona.
 *
 * Kampanja nad 49 tarčami (adjudikacija + raw dokazi v research/issue17/
 * lexicon-verification-raw/): direktni geslarski izseki fran.si (SSKJ²,
 * Pleteršnik, Novak SSP — 18 tarč), Wikipedia API (zvezčne mape DWB 33
 * zvezkov, Schmellerjeve izdaje Cotta 1827–37 / Frommann 1872–77, seznami
 * del, bibliografija — 14 tarč), deterministična preverba committed PV.json
 * (1 tarča), 16 tarč z viri, ki so v peskovniku nedosegljivi (DWB/Schmeller
 * polni teksti — kanonični URL v dokazih).
 *
 * REZULTAT: 0/70 hipotez POTRJENIH v celoti; 33 NEPOTRJENIH (geslo manjka /
 * pomen drugačen / citat zvezka ali atribucija ne stoji), 7 DELNO,
 * 17 NEVERIFIKATORNO, 13 BREZ-VIRA. Trije DWB citati zvezkov izrecno
 * napačni (Lohn Bd 16→12, Höfling Bd 13→10, Efeu Bd 6→3); dva strukturno
 * skladna (Aue Bd 1, Öde Bd 13). SSKJ refutacije z verbatim definicijami
 * (log = "(močviren) travnik ob vodi"; líza = "kdor rad liže"; gesla jedar,
 * ving, orga, horga, ajna, einhart, guten, poggi, šlifa NE obstajajo).
 * PV-Gypf: okrajšava NI v PV.json — JE v PS registru (+ "Schüttwiese,
 * Gypfang").
 *
 * Nič ne spreminja P43 hipotez ali rabe (vse ostaja NEKLASIFICIRANO) —
 * sloj verifikacije je zvezan bajtno na ps-lexicon.json (invarianta I2).
 * Status REVIEW — nič ne nadomešča človeške paleografske potrditve.
 * Dokaz: research/issue17/ps-lexicon-verified.json (identičen izpis skripta).
 */
export async function GET() {
  return NextResponse.json(psLexiconVerified, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
