// parish-forensics.ts — P237: FORENZIKA NITI (MILIČ↔MILEK križ · h69 zgodba · duhovniški križ)
// Meritve so izpeljane ob zagonu IZ korpusa HOUSE_VITALS (parish.ts) — qa-p237 jih živo
// preverja proti fiksnim vrednostim meritvene seje P237 (scripts/tmp/p237_measure*.ts,
// 2026-11-09). Rezultati so naslovnica za X-open vprašanja iz sinteze P236.
// Viri: krstna 04104 (1871–1885) · krstna 04105 (1886–1919) · mrliška 04106 (1857–1885)
// · mrliška 04894 (1886–1924) · poročna 04455 (1886–1922) — vse Matricula Online.

import { HOUSE_VITALS } from "./parish";

/** Kurirana lista grafij MILIČ-družine (MILIČ/MILEK/MIHELČ-Kurrent-continuum).
 *  Zavestno IZKLJUČUJE 'Michael/Michel/Michl' (krstna imena, lažni pozitiv). */
export const MILIC_FAMILY_RE =
  /MILIČ|MILEK|MIHELČ|MIHELIČ|MIHELIK|Mihelik|Milech|Milhoeluc|MILCH|Mihelk|Mihelt|Mihek|Milih|Mihelitsch|Mihelj|Mihelčič|Mihelovic|Milek\[|Mileh\[|Mek\/Milek|Milek-variant|MILEK-grafija/i;

export const FORENSIC_BOOKS = ["04104", "04105", "04106", "04894", "04455"] as const;

export interface MilicPerBook {
  signature: string;
  /** vseh blokov (Griblje-vpisi) v knjigi */
  blocks: number;
  /** blokov z MILIČ-družinsko grafijo */
  mentions: number;
}

/** MILIČ/MILEK/MIHELČ-bloki po knjigah (izpeljano iz korpusa). */
export const MILIC_PER_BOOK: MilicPerBook[] = FORENSIC_BOOKS.map((signature) => {
  const bloki = HOUSE_VITALS.filter((h) => h.bookSignature === signature);
  return {
    signature,
    blocks: bloki.length,
    mentions: bloki.filter((h) => MILIC_FAMILY_RE.test(h.whatSi)).length,
  };
});

/** Skupno število blokov z MILIČ-družino čez vseh 5 knjig (meritev: 235). */
export const MILIC_FAMILY_TOTAL = MILIC_PER_BOOK.reduce((s, b) => s + b.mentions, 0);

/** MILIČ-družina v predzgodovinski krstni 04104 po letih (1885→1871, kot PEZDIRC_PER_YEAR).
 *  1885 = 0 (iskreno! — P236-LEAD 'z105-botra-MILEK' je ne-Griblje-vrstica, izven korpusa). */
export const MILIC_PER_YEAR_04104: { year: number; count: number }[] = Array.from(
  { length: 15 },
  (_, i) => {
    const year = 1885 - i;
    return {
      year,
      count: HOUSE_VITALS.filter(
        (h) => h.bookSignature === "04104" && h.year === year && MILIC_FAMILY_RE.test(h.whatSi),
      ).length,
    };
  },
);

/** Mathias/Matija-veriga na h65 (oče istega imena 1871–1914 = 43 let!) — št. blokov. */
export const MATHIAS_H65_TOTAL = HOUSE_VITALS.filter(
  (h) => h.houseNo === "65" && /Mathias|Matija|Matihe/i.test(h.whatSi),
).length;

/** Kraji verige: prvi in zadnji dokaz (meritev: 1871 → 1914 — poročna 04455!). */
export const MATHIAS_H65_SPAN = (() => {
  const leta = HOUSE_VITALS.filter(
    (h) => h.houseNo === "65" && /Mathias|Matija|Matihe/i.test(h.whatSi),
  ).map((h) => h.year);
  return { first: Math.min(...leta), last: Math.max(...leta) };
})();

/** h65 = MILEK-hiša (mrliška 04894 1907: 'h65 = MILEK-hiša!' eksplicitno!). */
export const H65_STATS = (() => {
  const vsi = HOUSE_VITALS.filter((h) => h.houseNo === "65");
  const druzina = vsi.filter((h) => MILIC_FAMILY_RE.test(h.whatSi));
  return { total: vsi.length, family: druzina.length, others: vsi.length - druzina.length };
})();

/** h69 zgodba — vseh 25 blokov čez 5 knjig (04104×4 · 04105×8 · 04106×6 · 04894×5 · 04455×2). */
export const H69_TOTAL = HOUSE_VITALS.filter((h) => h.houseNo === "69").length;

export interface H69Era {
  id: string;
  labelSi: string;
  labelEn: string;
  spanSi: string;
  spanEn: string;
  proofs: number;
  familiesSi: string;
  familiesEn: string;
}

/** Obdobja h69: pred-Brinec (10) + BRINEC-doba (11) + poznejša menjava (4) = 25. */
export const H69_ERAS: H69Era[] = [
  {
    id: "pred-brinec",
    labelSi: "Pred-Brinec doba",
    labelEn: "The pre-Brinec era",
    spanSi: "1859–1884",
    spanEn: "1859–1884",
    proofs: 10,
    familiesSi:
      "Parič (1859) · Husič (1871) · Borin (1872) · Kuss (1873) · Brinc/Brune-priselitev (1874: 69-letni Joannes Brune umrl @h69 — KROP »Griblje-69« jasno!) · Husič-DUEL (1875) · TERDIČ-wirth (1882) · oče-PRAZNO (1884) · otrok-BRINE (04106-1884)",
    familiesEn:
      "Parič (1859) · Husič (1871) · Borin (1872) · Kuss (1873) · the Brinc/Brune arrival (1874: the 69-year-old Joannes Brune died @h69 — the KROP »Griblje-69« clear!) · the Husič DUEL (1875) · TERDIČ-wirth (1882) · the empty father (1884) · the BRINE child (04106-1884)",
  },
  {
    id: "brinec-doba",
    labelSi: "BRINEC-doba",
    labelEn: "The BRINEC era",
    spanSi: "1886–1895 (11 dokazov v 10 letih!)",
    spanEn: "1886–1895 (11 proofs in 10 years!)",
    proofs: 11,
    familiesSi:
      "krstna 04105 ×5 (oče Janez Brinec: 1888+1889+1890+1894+1895 — ISTI oče vseh 5×!) · mrliška 04894 ×4 (1886 Katarina »Brginec«-prečrtano-vdova-Podec-VODENICA · 1888 Marija-5 dni · 1889 Janez-16 dni · 1893 Katarina-Grinec-roj.-Straus) · poročna 04455 ×2 (1887 + 1893 ženin Johann BRINEC, GRIBLJE 69!)",
    familiesEn:
      "baptism 04105 ×5 (father Janez Brinec: 1888+1889+1890+1894+1895 — the SAME father all 5×!) · death 04894 ×4 (1886 Katarina »Brginec«-struck-out-widow-Podec-MILLER · 1888 Marija-5 days · 1889 Janez-16 days · 1893 Katarina-Grinec-born-Straus) · marriage 04455 ×2 (1887 + 1893 groom Johann BRINEC, GRIBLJE 69!)",
  },
  {
    id: "pozneje",
    labelSi: "Poznejša menjava",
    labelEn: "The later succession",
    spanSi: "1898–1924",
    spanEn: "1898–1924",
    proofs: 4,
    familiesSi:
      "Straus (1898, 7. pin — menjava) · Željko-bajtar (1904 + 1906, isti oče) · Dragos-samska-delavka-VODENICA (1924)",
    familiesEn:
      "Straus (1898, the 7th pin — a succession) · Željko-the-farmhand (1904 + 1906, the same father) · Dragos-single-worker-MILLER (1924)",
  },
];

/** Duovniški križ: Weisel/Wenzel/Wessely po knjigah (meritev: samo 04104 ×3!). */
export const PRIEST_CROSS: Record<string, number> = Object.fromEntries(
  FORENSIC_BOOKS.map((signature) => [
    signature,
    HOUSE_VITALS.filter(
      (h) => h.bookSignature === signature && /Weisel|Wenzel|Wessely/i.test(h.whatSi),
    ).length,
  ]),
);

/** Presek niti: Milek-družina pri h69 (botra Katarina Milek, 1898 — družabna mreža h65↔h69!). */
export const MILIC_H69_OVERLAP = HOUSE_VITALS.filter(
  (h) => h.houseNo === "69" && MILIC_FAMILY_RE.test(h.whatSi),
).length;

export type ForensicStatus = "POTRJENO" | "RAZREŠENO-DELNO" | "X-OPEN-OSTAJA";

export interface ForensicVerdict {
  id: string;
  titleSi: string;
  titleEn: string;
  status: ForensicStatus;
  bodySi: string;
  bodyEn: string;
  xOpenSi?: string;
  xOpenEn?: string;
}

/** Tri forenzične sodbe P237 (odgovori na P236 X-open vprašanja). */
export const FORENSIC_VERDICTS: ForensicVerdict[] = [
  {
    id: "milek-kriz",
    titleSi: "MILIČ↔MILEK-križ: h65-veja POTRJENA (×235 blokov čez 5 knjig!)",
    titleEn: "The MILIČ↔MILEK cross: the h65 branch CONFIRMED (×235 blocks across 5 books!)",
    status: "POTRJENO",
    bodySi:
      "Mathias @ h65: 1871 »Milič« (krstna 04104) → 1874 »Milek« → 1877 »Milek« → 1882 »MILEK«/»Milech«/»Mihelč« ×2 — ISTI oče zapisan z 4 grafijami čez 11 let! Krstna 04105 nadaljuje z istim očetom »Matija« 1887–1913 (×11 — MILEK/Mihelt/Mihek/Mitek/Milfelt-Kurrent) = veriga 1871–1914 = 43 let (zaključi jo poročna 04455 1914!); poročna 04455: ženin Mathias Milek 1886 (mrliška piše »Mileh« = pisateljska varianta!) + 1903 »MÜCK [~ Milek]« + 1905 nevesta Catharina MILEK — vse GRIBLJE 65; mrliška 04894 1907 eksplicitno: »h65 = MILEK-hiša!«. Skupaj 235 blokov (04104 ×53 · 04105 ×78 · 04106 ×20 · 04894 ×36 · 04455 ×48) — Kurrent-garble MILIČ/MILEK/MIHELČ = ISTI priimek (za h65-vejo 1:1). Bonus: h65 ima pred-MILEK dobo Brinc/Brune (1863–1869: Johan Brinc 43 l. + Georg Brine »Grenzwachter« 44½ l.) — BRINC/BRINEC-mreža povezuje h65 in h69!",
    bodyEn:
      "Mathias @ h65: 1871 »Milič« (baptism 04104) → 1874 »Milek« → 1877 »Milek« → 1882 »MILEK«/»Milech«/»Mihelč« ×2 — the SAME father written with 4 graphies across 11 years! Baptism 04105 continues with the same father »Matija« 1887–1913 (×11 — the MILEK/Mihelt/Mihek/Mitek/Milfelt Kurrent) = the chain 1871–1914 = 43 years (capped by marriage 04455 1914!); marriage 04455: groom Mathias Milek 1886 (the death register writes »Mileh« = a scribe's variant!) + 1903 »MÜCK [~ Milek]« + 1905 bride Catharina MILEK — all GRIBLJE 65; death 04894 1907 explicitly: »h65 = MILEK-hiša!« (the MILEK house). 234 blocks in total (04104 ×53 · 04105 ×78 · 04106 ×20 · 04894 ×36 · 04455 ×48) — the Kurrent garble MILIČ/MILEK/MIHELČ = ONE surname (for the h65 branch 1:1). Bonus: h65 has a pre-MILEK Brinc/Brune era (1863–1869: Johan Brinc 43 y. + Georg Brine »Grenzwachter« 44½ y.) — the BRINC/BRINEC network links h65 and h69!",
    xOpenSi:
      "Ne-h65 veje ostajajo odprte: botri 'Mathe/Mate Milič' (1871 z81/z83, h28) brez direktnega križa; MILIČ-1871-rekord ×5 oseb vključuje h23/h26 — krščenci teh vej nimajo mrliške/poročne potrditve istovetnosti.",
    xOpenEn:
      "The non-h65 branches stay open: the godmothers 'Mathe/Mate Milič' (1871 z81/z83, h28) without a direct cross; the MILIČ-1871-record ×5 persons includes h23/h26 — the children of those branches have no death/marriage identity confirmation.",
  },
  {
    id: "h69-zgodba",
    titleSi: "h69 zgodba: hiša je RES menjala gospodinjstva — in je vodeniška hiša (mlin!)",
    titleEn: "The h69 story: the house really changed households — and it is the miller's house (a mill!)",
    status: "RAZREŠENO-DELNO",
    bodySi:
      "P236 vprašanje: »trije različni priimki v treh letih — menjava ali prenosna št.?« → 25 blokov čez 5 knjig (04104 ×4 · 04105 ×8 · 04106 ×6 · 04894 ×5 · 04455 ×2): menjava gospodinjstev je DOKUMENTIRANA (obdobja spodaj); od 1886 se utrdi BRINEC-doba z 11 dokazi v 10 letih (isti oče Janez Brinec ×5 + mrliška ×4 + poroki ×2 — hiša 69 v izrekih!). Ključni signal vloge hiše: »Vodenica« ×2 — 1886 (Katarina, vdova Podec) in 1924 (Bara Dragos, samska delavka) → h69 = vodeniška/mlinarska hiša. Botra-presek: 1898 botra Katarina Milek (Milek-družina z h65 pri h69 — družabna mreža!)",
    bodyEn:
      "The P236 question: »three different surnames in three years — a succession or a transferable number?« → 25 blocks across 5 books (04104 ×4 · 04105 ×8 · 04106 ×6 · 04894 ×5 · 04455 ×2): the household succession is DOCUMENTED (the eras below); from 1886 the BRINEC era consolidates with 11 proofs in 10 years (the same father Janez Brinec ×5 + deaths ×4 + marriages ×2 — house 69 in the wording!). The key signal of the house's role: »Mller's wife/miller« ×2 — 1886 (Katarina, the Podec widow) and 1924 (Bara Dragos, a single worker) → h69 = the miller's house. The godparent cross: 1898 godmother Katarina Milek (the Milek family from h65 at h69 — a social network!)",
    xOpenSi:
      "Prenosna št. ni dokazana NI v eno smer: vse menjave so združljive z realno menjavo prebivalcev; da je '69' kdaj označevalo sosednjo hišo, ni mogoče izključiti za 1859–1884 (redki dokazi).",
    xOpenEn:
      "A transferable number is not proven in either direction: all successions are compatible with a real change of residents; whether '69' ever labelled a neighbouring house cannot be excluded for 1859–1884 (scarce proofs).",
  },
  {
    id: "duhovniki-kriz",
    titleSi: "Duhovniški križ: Weisel/Wenzel/Wessely ≠ najdeni drugje → X-open OSTAJA",
    titleEn: "The priests' cross: Weisel/Wenzel/Wessely not found elsewhere → the X-open REMAINS",
    status: "X-OPEN-OSTAJA",
    bodySi:
      "Iskanje Weisel/Wenzel/Wessely po vseh 5 knjigah: 04104 ×3 (vsi 1871: h24 Weisel-'D.H. Cap.' · h72 'Wilhelm-Wenzel?-Coop.' skupni-podpis · h6 'Daniel-Wessely-cop.') · 04105 ×0 · 04106 ×0 · 04894 ×0 · 04455 ×0. Križ torej NE prinese neodvisnega dokaza — trio je specifičen za leto 1871 knjige 04104. Pošten rezultat: X-open vprašanje (ista oseba? garble-continuum?) ostaja odprto do novega vira (npr. duhovniški katalog ali druge župnije).",
    bodyEn:
      "A search for Weisel/Wenzel/Wessely across all 5 books: 04104 ×3 (all 1871: h24 Weisel-'D.H. Cap.' · h72 'Wilhelm-Wenzel?-Coop.' a joint signature · h6 'Daniel-Wessely-cop.') · 04105 ×0 · 04106 ×0 · 04894 ×0 · 04455 ×0. The cross therefore does NOT bring independent proof — the trio is specific to the year 1871 of book 04104. An honest result: the X-open question (one person? the garble continuum?) stays open until a new source (e.g. a clergy catalogue or other parishes).",
  },
];

/** Skupne statistike forenzične seje (izpeljano, konsistentno zgoraj). */
export const FORENSICS_TOTALS = {
  books: FORENSIC_BOOKS.length,
  milicTotal: MILIC_FAMILY_TOTAL,
  milicPerBook: Object.fromEntries(MILIC_PER_BOOK.map((b) => [b.signature, b.mentions])),
  mathiasH65: MATHIAS_H65_TOTAL,
  h65: H65_STATS,
  h69: H69_TOTAL,
  verdicts: FORENSIC_VERDICTS.length,
  label: "P237 · FORENZIKA NITI",
} as const;
