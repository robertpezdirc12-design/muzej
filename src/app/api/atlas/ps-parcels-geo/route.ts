import { NextResponse } from "next/server";
import psParcelsGeo from "@/data/atlas/ps-parcels-geo.json";

export const dynamic = "force-static";

/**
 * ISSUE #13 (P55 → P58 v2 → P68 v3) — GEOLOKACIJA GRUNDPARCELLEN: PS PROTOKOL 1825 ↔
 * SODOBNE PARCELE KO 1544 — SANIRANA + RENUMERIFICIRANA PRODUKCIJA.
 *
 * PS = »Protocol der Grund-Parcellen der Gemeinde GRÜBLE« (N083PS, 143 strani):
 * 2505 Grundparzellen + 102 Bauplätze = 2607 vrstic — lastniki, rabe, površine,
 * a brez geometrije. Zgodovina sanacij:
 *  · P55: prva geolokacija (1110 vrstic / 800 števil);
 *  · P58 (v2): −43 lažnih povezav S3 (P56 dokaz) + 26 Blatt I vrstic (P57)
 *    → 1093 vrstic / 800 števil;
 *  · P68 (v3, AKTUALNO): 17 preslikav P67 forenzične specifikacije (dvojna
 *    Kurrent zamenjava: p78 160x→150x, p93 160x→190x, p87 661–680→1681–1700)
 *    + re-join po P55 metodi → 1079 vrstic / 798 pozicioniranih števil;
 *    14 vrstic izpada (base brez PF poligona), p93 3× re-claim na 1903/1904/1905;
 *    površine median 3.8512 ≈ 1 Wiener QK 3.59665 m² (Δ +7.08 %);
 *    soslednost 590 parov / 51.8 m / 28.3×; zaupanje STRONG 171 / MEDIUM 735 /
 *    WEAK 147; registrska branja (ps-raw) NESPREMENJENA — parzella ostaja
 *    originalno branje, sanacija le na join ključu (base).
 *
 * Status: SANITIZED-DETERMINISTIC. SHEET_GEOREFS in dokazi P40–P67
 * nespremanjeni; v2 dokaz arhiviran (research/issue17/ps-parcels-geo-v2.json).
 *
 * Dokaz v3: research/issue17/ps-parcels-geo-v3.json (izpis skripta
 * scripts/p68_ps_v3_renumber.py; invarianti I1–I9, `--check` = determinizem).
 * Runtime: src/data/atlas/ps-parcels-geo.json (version 3).
 */
export async function GET() {
  return NextResponse.json(psParcelsGeo, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
