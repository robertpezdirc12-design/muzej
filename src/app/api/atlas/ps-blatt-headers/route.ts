import { NextResponse } from "next/server";
import psBlattHeaders from "@/data/atlas/ps-blatt-headers.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P59) — GLAVE LISTOV REGISTRA PS ("Nro. des Blattes").
 *
 * Prvo zanesljivo branje glav listov protokola "Der Grund-Parcellen der
 * Gemeinde GRÜBLE": levi stolpec tabele izrezan iz 135 VAČ posnetkov
 * (p59_fetch_strip.py), 2 neodvisna VLM prehoda na stran (p59_ps_read_blatt.mjs)
 * + 25 arbitraž agent-oči na 3× izrezih (hardcoded razlogi, deterministično).
 *
 * REZULTAT: Blatt I = parcele 1–800 (str. 3–40; prehodna cona 721–800 s
 * popravki I→II [~]), Blatt II se začne pri 801 (str. 43–92, p72 = III vmes);
 * interleave lokalnih sekcij (161–180 pod II na 61–62/81/83–87, 601–620,
 * 921–960 ...); p101 z ulomki (196½ ...). PER-BLATT DVoumnost: od 211 base v2
 * na več straneh jih 106 sega čez ≥2 Blatta (P39: ista številka pod različnima
 * Blattoma = druga parcela), 17 ruleCandidate (edina instanca v pasu
 * razmerij [0.8, 1.25]) — MERJENO, join v2 NESPREMENJEN (disciplina P56/P58).
 *
 * Pokritost: S1 5–127 = 123/123 × 2 prehoda; S2 128–132 + 137 (137 samo
 * pass1); 133–136 in 138–139 ni svežega branja (VLM kvota 429 — odprto).
 *
 * Status: REVIEW (strojno branje ni dokazni vir). SHEET_GEOREFS in dokazi
 * P40–P58 nespremenjeni; P55/P56/P57/P58 runtime nespremenjeni (pini QA).
 *
 * Dokaz: research/issue17/ps-blatt-headers.json (celoten izpis skripta
 * scripts/p59_ps_blatt_headers.py; invarianti I1–I9, `--check` = determinizem).
 * Runtime: src/data/atlas/ps-blatt-headers.json (kompakt).
 */
export async function GET() {
  return NextResponse.json(psBlattHeaders, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
