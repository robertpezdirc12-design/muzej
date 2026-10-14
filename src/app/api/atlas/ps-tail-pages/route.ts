import { NextResponse } from "next/server";
import psTailPages from "@/data/atlas/ps-tail-pages.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P63) — ZAKLJUČNE STRANI REGISTRA PS (138–139).
 *
 * Paleografska zaključitev repa registra "Der Grund-Parcellen der Gemeinde
 * GRÜBLE" s 3 neodvisnimi prehodi (VLM glm-5v-turbo 2× + agent-oči na
 * izrezih 4×–5×, 2-od-3 konsenz, [~] + alternatives na razhodi):
 *
 * - p139 = Blatt IIb (pod-list, NOV v strukturi registra): Parzelle 41–60
 *   (duplikat številk Blatt I pod IIb) + lastninske kolone (Haus Nº rdeče,
 *   'Vor und Zuname' = številke 62–80 — ne imena, Stand + Wohnort rdeče)
 *   + desna stran = kultura rekapitulacija 81–100 / Classe 101–120.
 *   KOREKCIJA: prejšnja očesna razlaga 'Nro. des Hauses.' = očesna napaka
 *   (glava je 'Nro. des Blattes.') → P58 open #6 ZAPRT.
 * - p138 = izbrisana leva tabela (bledi ostanki 'T. 191'[~] @ r14,
 *   parzelle 23/24[~], '89/86'[~] @ r27) + 'Zusammenstellung der
 *   Grundstücke' (Wiese 1–20, Classe 21–40) na desni.
 *
 * Vsote: 82|81 (Dominical/Haus), 125|183 (Stand/Wohnort), Fürtrag 189|1228,
 * 162|1447 (Capital) — razlaga enot ostaja odprta [~].
 *
 * Join v2 NESPREMENJEN (p138/139 brez vrstic v v2 → perBlattAmbiguity
 * 211/110/17 nespremenjeni). Status: REVIEW (strojno branje ni dokazni vir).
 *
 * Dokaz: research/issue17/ps-tail-pages.json (skript scripts/p63_ps_tail_pages.py,
 * invariante I1–I10, `--check` bajtno determinističen). Runtime: kompakt.
 */
export async function GET() {
  return NextResponse.json(psTailPages, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
