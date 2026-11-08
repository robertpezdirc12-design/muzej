import { NextResponse } from "next/server";
import psPass1Layers from "@/data/atlas/ps-pass1-layers.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P69) — SISTEMSKI PREGLED P38 pass1 SLOJEV, cona p73–93 (+p99).
 *
 * Odprta točka P68 next #3 ("p74/p76/p77 1121–1200 brez kartnih poligonov
 * [~]; p88 721–740 [~]") — RAZREŠENA z očesno forenziko (P67 recept):
 * 4× široki izrezi x=0..430 (popravi P59 past odrezanih vodilnih številk)
 * + 7×–8× zoomi dvomljivih vrstic + kontinuiteta + kartni poligoni +
 * P56 annRecords zamiki + Blatt stolpec + hišne številke + površinska
 * razmerja. 22 strani (p73–93 + kolizijska p99), 166 v3 vrstic
 * klasificiranih.
 *
 * • (A) STARI P38 SLOJI = SISTEMATSKI DIGITALNI ARTEFAKTI: p74 1121–1140
 *   je pravzaprav 1421–1440 (4→1, −300; annRecords 1135/1136/1138 =
 *   prečrtane 1435/1436/1438), p76 1161–1181 = 1461–1480 (4→1), p77
 *   1181–1200 = 1481–1500 (4→1), p79 1821–1842 = 1521–1540 (5→8, +300),
 *   p80 1644+ = 1541–1560 (5→6, +100), p81 1661–1680 = 1561–1580 (5→6),
 *   p82 1681–1700 = 1581–1600 (5→6; pass1 je bil pravilen — join je vzel
 *   p2 → vrstice IZGUBLJENE), p88 721–740 = 601–620 (+120 celostranski;
 *   annRecords 726/728/736/737/740 = 606/608/616/617/620), p89 1921–1941
 *   = 921–940 (+1000 fantom-1; pass1 pravilen!), p90 1941–1960 = 941–960
 *   (+1000), p92 990–1008 = 981–1000 (+9 zamik; P59 arbitraža 1881–1900
 *   = isti 9→19 artefakt), p99 921–940 = 1921–1940 (−1000 izgubljena 1;
 *   ZRCALNI primer p89; Blatt III). Kontinuiteta: p73 (1101–20) → p74
 *   (1421–40) → … → p82 (1581–1600); p91 (961–80) → p92 (981–1000);
 *   p49–52 = 921–1000 glavni tek.
 * • (B) LOKALNE SEKCIJE (5 strani: p83, p84, p85, p86, p88): pisane
 *   številke 161–180 / 641–660 / 601–620 trčijo z Blatt I KO-globalnimi —
 *   dokazano RAZLIČNE parcele (hiše: p85 r641 Hi16 vs p35 r641 Hi68;
 *   lastniki brez prekrivanja; Σ ratio 16–236× proti čistim 1.09) — 56
 *   v3 vrstic = lažne fuzije na Blatt I poligone; opciji exclude / per-
 *   Blatt instance = LASTNIŠKA odločitev (P70).
 * • (C) SPEC P70: 77 renum preslikav (0 kolizij) + 98 rejoin kandidatov
 *   (pisane številke s kartnimi poligoni, izpadle iz v3) — izvedba =
 *   veriga re-run P59–P68 s posodobljenimi pini.
 * • (D) p89/p99 ZRCALNI primer: p89 (II) = 921–940, p99 (III) =
 *   1921–1940 — Blatt stolpec razrešuje.
 *
 * Status: REVIEW (join v3 NESPREMENJEN — disciplina P56–P68; sanacija
 * spec = LASTNIKA, izvedba P70).
 *
 * Dokaz: research/issue17/ps-pass1-layers.json
 * (skripta scripts/p69_ps_pass1_layers.py, invariante I1–I6 + --check
 * bajtno determinističen; sha256 pini vhodov).
 */
export async function GET() {
  return NextResponse.json(psPass1Layers, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
