import { NextResponse } from "next/server";
import psUnitSemantics from "@/data/atlas/ps-unit-semantics.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P61) — UNIT-SEMANTICS moda B: merjena karakterizacija.
 *
 * Odprta točka P60 #1 ("kolonialna enota ali delna površina?") merjeno
 * RAZREŠENA s preusmeritvijo — deterministična skripta
 * scripts/p61_ps_unit_semantics.py (invarianti I1–I9, `--check` bajtno):
 *
 *   * M1 pasovi == P60: moda A [3.3, 4.3] n=226 · moda B [0.8, 1.25] n=62
 *     (ratio = areaModern / areaQK; 1 QK = 3.59665 m²);
 *   * M4 PERMUTACIJSKA KONTROLA hipoteze H1 (napačen številčni join P55):
 *     deterministične FNV-1a-32 točke (bajtno enako Python/TS), radija
 *     50/100 m, površinski pas ±25 % glede na target = areaQK × 3.59665:
 *       moda A real @50 0.9248 vs perm 0.1637 (5.6×) — ujeta = prava parcela;
 *       moda B real @50 0.2903 vs perm 0.1774 (1.6×) — prava parcela
 *       (QK×3.6) NI tik zraven → H1 ZAVRŽEN kot glavni mehanizem;
 *       @100 m base rate raste z gostoto parcel (A perm 0.5221, B perm
 *       0.6129) — diskriminator je 50 m;
 *   * M3 Blatt distribucija moda B (P59 pageAttribution):
 *     II 31 · IV 11 · III 9 · I 5 · I·II 1 · null 5 (42 strani 5–137);
 *   * M2 bloki ≥2 sosedenih vrstic: 3 bloki / 9 vrstic (p85 n5
 *     'Wiese und Gfrett' 653–657, p86 n2, p117 n2) — moda B razpršena;
 *   * M5 H3 delna površina NEUPORABNA: samo 2 base z ≥2 moda B vrsticami
 *     (163: 226+214 @ p61/p86; 176: 334+289 @ p83/p86).
 *
 * VERDIKT: moda B = dosledna DRUGAČNA registracijska konvencija površin
 * (številka ≈ sodobna meritev v m²) — ne napaka ujeme, ne delna površina;
 * identiteta enote ODPRTA [~] (paleografija/dokumenti).
 *
 * IMPLIKACIJA za P60: pas pravilo [0.8, 1.25] izbere vrstico v konvenciji,
 * številčno primerljivi s sodobno meritvijo — atribucija smiselna kot
 * RELATIVA [~]; atribucije P60 in join v2 NESPREMENJENI.
 *
 * Runtime vsebuje gursCompact (2117 parcel KO 1544: st, površina, lat, lng)
 * za produkcijo preracun kontrole na runtime kopijah (lekcija P58).
 *
 * Dokaz: research/issue17/ps-unit-semantics.json (celoten izpis; I1–I9).
 * Status: REVIEW (identiteta enote odprta; meritve deterministične).
 */
export async function GET() {
  return NextResponse.json(psUnitSemantics, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
