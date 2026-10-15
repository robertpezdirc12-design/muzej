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
 *  · P68 (v3): 17 preslikav P67 forenzične specifikacije (dvojna
 *    Kurrent zamenjava: p78 160x→150x, p93 160x→190x, p87 661–680→1681–1700)
 *    + re-join po P55 metodi → 1079 vrstic / 798 pozicioniranih števil;
 *    14 vrstic izpada (base brez PF poligona), p93 3× re-claim na 1903/1904/1905;
 *  · P70 (v4, AKTUALNO): IZVEDBA P69 očesne forenzike — 77 renum preslikav
 *    (bajtno po P69 renumSpec: p74 +300, p79 −300, p80/p81 −100,
 *    p89/p90 ±1000 fantom-1, p92 −9, p99 +1000) + 95 rejoin vrstic iz starih
 *    P38 slojev po P55 metodi (sloji po P69; 3 kandidati p80 1541–1543 brez
 *    vira [~]) → 1145 vrstic / 878 pozicioniranih števil; 29 preslikanih
 *    izpada (base brez PF poligona); 33 fuzij isti-Blatt (dva bloka registra
 *    921–1000: p49–52 + p89–92; SPLIT = LASTNIKA); površine median
 *    3.8843 ≈ 1 Wiener QK 3.59665 m² (Δ +8.0 %); soslednost 654 parov /
 *    52.0 m / 27.6×; 56 sekijskih vrstic (p83–86, p88) nespremanjenih
 *    (exclude/per-Blatt = LASTNIKA); registrska branja (ps-raw) NESPREMENJENA.
 *
 * Status: SANITIZED-DETERMINISTIC. SHEET_GEOREFS in dokazi P40–P69
 * nespremanjeni; v2/v3 dokaza arhivirana (research/issue17/
 * ps-parcels-geo-v2.json, -v3.json).
 *
 * Dokaz v4: research/issue17/ps-parcels-geo-v4.json (izpis skripta
 * scripts/p70_ps_v4_rejoin.py; invarianti I1–I9, `--check` = determinizem).
 * Runtime: src/data/atlas/ps-parcels-geo.json (version 4).
 */
export async function GET() {
  return NextResponse.json(psParcelsGeo, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
