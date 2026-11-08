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
 *  · P71 (v5): KOREKCIJE v4 — (C1) 56 sekijskih vrstic
 *    (p83–86, p88) EXCLUDE iz joina (P69 sectionClass bajtno; dokazane
 *    lažne fuzije na Blatt I poligone; LASTNIŠKA odločitev: opcija exclude;
 *    vrstice ostanejo v registru brez geometrije; 0 poligonov ostane
 *    praznih) + (C2) P93 REVERZIJA — P68 renum 160x→190x OVRŽEN z
 *    notranjo glifno forenziko (r9 = 1609 / r19 = 1619: 6 ≠ 9, isti
 *    pisar; kontrole p98 '1916' in p92 981–983) + annRecords anotatorja
 *    (1601–1619) + pageMap P56 + P38 pass2: 15 vrstic base := parzella,
 *    PF ujemanja {1603, 1604, 1605} (prej prazni poligoni dobili prve
 *    vrstice), 12 izpadlih; PF 1901–1920 brez lažnih dvojnih zahtevkov
 *    p93 (ostane p98 III); v5: 1077 vrstic / 879 pozicioniranih števil;
 *    površine median 3.9052 ≈ 1 Wiener QK 3.59665 m² (Δ +8.58 %);
 *    soslednost 652 parov / 51.8 m / 25.5×.
 *  · P72: paket dvojnosti (odločitveni paket za isti-Blatt SPLIT joina —
 *    135 dual base; P70 33 kolizij = podmnožica; opcija A predračun rows
 *    939) — v5 runtime NESPREMENJEN (dokaz research/issue17/
 *    ps-dual-occurrence-pack.json; odločitev LASTNIKA).
 *  · P73 (v6, AKTUALNO): ISTI-BLATT SPLIT opcija A — 135 dual base
 *    (P72 dual pack; lastniki disjunktni 135/135; P70 33 = podmnožica):
 *    drop 137 kombinacij = 138 vrstic (drugi blok, keep = min stran)
 *    → 939 vrstic / 879 base / multi 50 / cross 48; area median 3.8941
 *    (Δ +8.27 %); sosledje 652/51.8 m (nespremenjeno); nearDual
 *    2080/2081 ostanejo; v5 arhiviran v dokazu.
 *  · P74: CROSS-BLATT dvojnosti registra (odločitveni paket za
 *    cross-Blatt SPLIT joina — odprta točka P73 ①; P66 vzorec
 *    re-izpeljan iz v6; NE odloča namesto lastnika — MERI in DOKAZUJE)
 *    — 48 cross base / 96 vrstic / 1 vrstica per Blatt 48/48; lastniki
 *    med Blatti disjunktni 48/48; opciji A1/A2 (rows 891, cross 0) —
 *    v6 runtime NESPREMENJEN (dokaz research/issue17/
 *    ps-cross-blatt-pack.json; odločitev LASTNIKA).
 *  · P75 (v7, AKTUALNO): CROSS-BLATT SPLIT opcija A1 — izvedba C4 iz
 *    P74 paketa (lastniška odločitev 2026-10-15; keep = DOMINANT Blatt
 *    po Σ areaQK; ties 0): za 48 cross base (P74 pack; ista številka
 *    pod dvema Blattoma = 2 realni parceli) je vrstica ne-dominantnega
 *    Blatta izpadla iz joina — drop 48 kombinacij = 48 vrstic → 891
 *    vrstic / 879 base / multi 2 / cross 0; area median 3.8102
 *    (Δ +5.94 %); sosledje 652/51.8 m (nespremenjeno); vrstice ostanejo
 *    v registru brez geometrije; v6 arhiviran v dokazu; PAYLOAD/
 *    schema NESPREMENJENA.
 *  · P76: LOKALNE SEKCIJE — per-Blatt instance odločitveni paket
 *    (odprta točka P70 ①/P71 C1; vzorec P72/P74 — MERI, NE odloča)
 *    — 56 sekcij vrstic (p83–86 + p88; Blatt II) × 31 base identitetno
 *    disjunktne od counterpartov (lastniki 0/0, hn 31/31 različne);
 *    counterpar v v7 31/31 (I 23 / II 8); P60 band 12/56; opcije
 *    A/B1/B2/B3 predračunane (B1 krši NIL-CLAIM z base-ključem →
 *    per-instanca ključ) — v7 runtime NESPREMENJEN (dokaz research/
 *    issue17/ps-sections-perblatt-pack.json; izbira LASTNIKA).
 *
 * Status: SANITIZED-DETERMINISTIC. SHEET_GEOREFS in dokazi P40–P75
 * nespremanjeni; v2/v3/v4/v5/v6 dokazi arhivirani (research/issue17/
 * ps-parcels-geo-v2.json, -v3.json, -v4.json, -v5.json, -v6.json).
 *
 * Dokaz v7: research/issue17/ps-parcels-geo-v7.json (izpis skripta
 * scripts/p75_ps_v7_cross_split_a1.py; invarianti I1–I8, `--check` =
 * determinizem; nasledstvo v5Delta + v6Delta + v7Delta v runtime).
 * Runtime: src/data/atlas/ps-parcels-geo.json (version 7).
 */
export async function GET() {
  return NextResponse.json(psParcelsGeo, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
