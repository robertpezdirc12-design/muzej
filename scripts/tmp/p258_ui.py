#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258 — UI: Notranjost01738Leto1832 komponenta (za Notranjost01738Leto1830_1831!)."""

COMPONENT = r'''
function Notranjost01738Leto1832() {
  const { t } = useLang();
  const e1831k: { m: string; d: string; h?: string; x?: boolean }[] = [
    { m: "14", d: "9. 2. d°", h: "47", x: true },
    { m: "15", d: "14. 2.", h: "17", x: true },
    { m: "16", d: "14. 2. d°", h: "35", x: true },
    { m: "17", d: "6. 6.", h: "26", x: true },
    { m: "18", d: "[~24.] 7.", h: "9", x: true },
    { m: "19", d: "24. 8.", h: "46·8★" },
    { m: "20", d: "24. 8. d°", h: "48·2★" },
    { m: "21", d: "[~1.] 11.", h: "BARON", x: true },
    { m: "22", d: "6. 11. d°", h: "24", x: true },
    { m: "23", d: "20. 11.", h: "9", x: true },
    { m: "24", d: "23. 11. d°", h: "36", x: true },
  ];
  const e1832: { m: string; d: string; h?: string; x?: boolean }[] = [
    { m: "1", d: "18. 1.", h: "49", x: true },
    { m: "2", d: "18. 1. d°", h: "ANOM.", x: true },
    { m: "3", d: "18. 1. d°", h: "30", x: true },
    { m: "4", d: "25. 1. d°", h: "22", x: true },
    { m: "5", d: "29. 1. d°", h: "[18|48]", x: true },
    { m: "6", d: "15. 2.", h: "11", x: true },
    { m: "7", d: "15. 2. d°", h: "27", x: true },
    { m: "8", d: "15. 2. d°", h: "22·35★" },
    { m: "9", d: "15. 2. d°", h: "5", x: true },
    { m: "10", d: "22. 2. d°", h: "7", x: true },
    { m: "11", d: "29. 2. d°", h: "19", x: true },
    { m: "12", d: "29. 2. d°", h: "15", x: true },
    { m: "13", d: "29. 2. d°", h: "19", x: true },
    { m: "14", d: "29. 2. d°", h: "25", x: true },
    { m: "15", d: "29. 2. d°", h: "16", x: true },
    { m: "16", d: "29. 2. d°", h: "2·42★" },
    { m: "17", d: "29. 2. d°", h: "36·35★" },
    { m: "18", d: "29. 2. d°", h: "23", x: true },
    { m: "19", d: "29. 2. d°", h: "CRO", x: true },
    { m: "20", d: "5. 3.", h: "21", x: true },
    { m: "21", d: "28. 5.", h: "[10|0]", x: true },
    { m: "22", d: "20. 6.", h: "66★" },
    { m: "23", d: "28. 11.", h: "56·61★" },
  ];
  const e1833: { m: string; d: string; h?: string; x?: boolean }[] = [
    { m: "1", d: "[~3.|5.] 2.", h: "6", x: true },
    { m: "2", d: "6. 2. d°", h: "3", x: true },
    { m: "3", d: "6. 2. d°", h: "11", x: true },
    { m: "4", d: "6. 2. d°", h: "6", x: true },
    { m: "5", d: "6. 2. d°", h: "25", x: true },
    { m: "6", d: "6. 2. d°", h: "50·49★★" },
  ];
  return (
    <div className="rounded-xl border bg-card/60 p-5">
      <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
        <BookOpenCheck className="h-4 w-4 text-primary" aria-hidden />
        {t(
          "Notranjost knjige 01738: meja-1831/32/33 (11 + 23 + 6 vpisov — 40, največja faza!)",
          "The interior of the book 01738: the 1831/32/33 boundary (11 + 23 + 6 entries — 40, the largest phase!)",
        )}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground [overflow-wrap:anywhere]">
        {t(
          `1831-KONEC (s8, Pag. 13 — leto se nadaljuje ČEZ mejo strani!): ${PREDHODNIK_1831K_TOTAL} vpisov m14–m24 — m14 = 9. Febr d° (12. poroka istega dne!), KLOBUČAR-bratje 24. 8. ×2, BARON-vrstica (k. k. upokojenec!), 24 vpisov leta 1831 skupaj. 1832 (s9+s10, Pag. 15/17 — RESTART 18. Jänner!): ${PREDHODNIK_1832_TOTAL} vpisov — ★ 9 porok na PRESTOPNI DAN 29. 2. 1832 (največji množični dan korpusa!) + ANOMALIJA-m2 (MARIA Vipavc — žensko ime v ženinskem stolpcu, 2. za P257-m7!). 1833 (s10-spodaj): ${PREDHODNIK_1833_TOTAL} vpisov — RESTART z letnico ROKOPISNO nad datumom ([~3.|5.] Febr, 4. restart notranjosti!).`,
          `The 1831-END (s8, Pag. 13 — the year CONTINUES ACROSS the page boundary!): ${PREDHODNIK_1831K_TOTAL} entries m14–m24 — the KLOBUČAR brothers + THE BARON ROW (a retired imperial official!). 1832 (s9+s10, the RESTART of Jan 18!): ${PREDHODNIK_1832_TOTAL} entries — ★ 9 WEDDINGS ON THE LEAP DAY Feb 29 1832 (the largest mass day of the corpus!) + the m2 ANOMALY (MARIA Vipavc in the groom's column!). 1833: ${PREDHODNIK_1833_TOTAL} entries — the RESTART with the year HANDWRITTEN above the date (the 4th restart!).`,
        )}
      </p>

      {/* 16 blokov 10 dvigov — emerald */}
      <div className="mt-4 rounded-lg border border-emerald-500/40 bg-emerald-500/10 p-4">
        <p className="text-sm font-medium text-emerald-700 dark:text-emerald-300 [overflow-wrap:anywhere]">
          {t("★★★★★ 16 BLOKOV — 10 DVOGOV firstYear: ", "★★★★★ 16 BLOCKS — 10 firstYear LIFTS: ")}
          {t(
            `h8 1871→1831 (+40 = 2. največji dvig vseh časov za h22-41-P255!) · h46 +36 · h66 +36 (3. mesto TROJNO s h56!) · h35 +35 · h47 +31 · h42 +29[~] · h2 +27 · h48 +26 · h36 +25 · h49 +25 — ★★★★★ Šest-knjižni klub 23→31 (+8: h2/h8/h35/h36/h42/h46/h47/h48 — 2. največji skok!) + bothEra-poročna 26→34 + h35-×2 DVE DRUŽINI v 14 dneh + h66/h49 = 5 knjig BREZ 04455 (poročni vrzeli!). Korpus ${PREDHODNIK_258_KORPUS.vitalsTotal} vitalov / 01738 = ${PREDHODNIK_258_KORPUS.byBook01738} blokov / leta 1828–1833+1873!`,
            `h8 1871→1831 (+40 = the 2nd-largest lift ever after h22-41!) · h46 +36 · h66 +36 (the triple 3rd place!) · h35 +35 · h47 +31 · h42 +29[~] · h2 +27 · h48 +26 · h36 +25 · h49 +25 — ★★★★★ The six-book club 23→31 (+8 — the 2nd-largest jump!) + the marriage both-era 26→34 + h35 TWICE two families in 14 days + h66/h49 five books WITHOUT 04455 (marriage gaps!). The corpus ${PREDHODNIK_258_KORPUS.vitalsTotal} vitals / 01738 = ${PREDHODNIK_258_KORPUS.byBook01738} blocks / the years 1828–1833+1873!`,
          )}
        </p>
      </div>

      {/* ★★★★★★ PEZDIRC-h50 — primary card */}
      <div className="mt-4 rounded-lg border border-primary/50 bg-primary/10 p-4">
        <p className="text-sm font-medium [overflow-wrap:anywhere]">
          {t(
            "★★★★★★ NIT PEZDIRC-h50 NADGRADNJA (3 VRSTICE — 42 LET!): 1831 Georg PESDIRZ-h50 (P257) + 1833 Johann PESDIRZ-h50 (★ TRIPLE črko-za-črko 'P-e-s-d-i-r-z' — row+duel+region! [~Petroviz zavrnjen]) = ★ DVA SINA ISTEGA OČETA MARCA (oba 21 let!) + priča AND. PEZDIRC-1831 (m14 — 5. vrstica družine: ženin + 2 nevesti + ANOMALIJA + PRIČA!) + 1873 Marcus PEGDIRE-h50 (P251!) — ISTA DRUŽINA 1831–1873! · MILEK-h22 DOMNEVA POTRJDENA: 1830 Anna + 1832 Johann MILEK (oče Johann, duel-'k'!) = brat in sestra — h22 4 bloki v 5 letih (1828/29/30/32!) · KRIŽAN-KONGLOMERAT: 1831-h3 + 1832-h36 + 1832-h66 (★ KRIŽAN×KRIŽAN!) + 1873-h63 = 4 hiše + HRIŽAN-h62-ŠIV!",
            "★★★★★★ THE PEZDIRC h50 UPGRADE (3 ROWS — 42 YEARS!): the 1831 Georg + the 1833 Johann PESDIRZ (★ TRIPLE letter-by-letter 'P-e-s-d-i-r-z'!) = ★ TWO SONS OF THE SAME FATHER MARCO (both 21!) + the witness AND. PEZDIRC-1831 (the 5th row of the family!) + the 1873 Marcus PEGDIRE — THE SAME FAMILY 1831–1873! · THE MILEK h22 HYPOTHESIS CONFIRMED: the 1830 Anna + the 1832 Johann (both children of Johann!) = brother and sister — h22 4 blocks in 5 years! · THE KRIŽAN CONGLOMERATE: 1831-h3 + 1832-h36 + 1832-h66 (★ A KRIŽAN MARRIES A KRIŽAN!) + 1873-h63 = 4 houses + the h62 seam!",
          )}
        </p>
      </div>

      {/* 1831-konec timeline */}
      <div className="mt-4 overflow-x-auto pb-1">
        <p className="mb-1 text-xs font-semibold text-muted-foreground">{t("1831-konec (m14–m24 — čez mejo strani!)", "The 1831-end (m14–m24 — across the page boundary!)")}</p>
        <div className="flex min-w-[880px] items-end gap-1 sm:min-w-0" role="listbox" aria-label={t("Vrstice 1831-konca", "The rows of the 1831-end")}>
          {e1831k.map((e, i) => {
            const isDouble = (e.h || "").includes("·");
            const isBaron = e.h === "BARON";
            return (
              <div key={`c${e.m}-${i}`} role="option" aria-selected={false} className="flex flex-1 flex-col items-center gap-1 rounded-lg border border-transparent px-1 py-2">
                <span className="text-[10px] font-medium text-muted-foreground" style={{ overflowWrap: "anywhere" }}>{e.d}</span>
                <span className={`flex h-9 min-w-9 items-center justify-center rounded-full border px-1 text-[11px] font-semibold ${isDouble ? "border-emerald-500 bg-emerald-500/20 text-emerald-700 dark:text-emerald-300" : isBaron ? "border-violet-500 bg-violet-500/20 text-violet-700 dark:text-violet-300" : e.x ? "border-dashed border-amber-500/60 bg-amber-500/10 text-amber-700 dark:text-amber-300" : "border-primary/50 bg-primary/10 text-primary"}`}>{e.m}</span>
                <span className="text-[10px] text-muted-foreground" style={{ overflowWrap: "anywhere" }}>
                  {e.h ? (isBaron ? "Aloys-BARON!" : isDouble ? e.h.replace("·", "×h").replace("★", "!") : `h${e.h}`) : ""}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* 1832 timeline */}
      <div className="mt-4 overflow-x-auto pb-1">
        <p className="mb-1 text-xs font-semibold text-muted-foreground">{t("Leto 1832 (m1–m23 — 9 porok na prestopni dan!)", "The year 1832 (m1–m23 — 9 weddings on the leap day!)")}</p>
        <div className="flex min-w-[880px] items-end gap-1 sm:min-w-0" role="listbox" aria-label={t("Vrstice leta 1832", "The rows of 1832")}>
          {e1832.map((e, i) => {
            const isDouble = (e.h || "").includes("·");
            const isAnom = e.h === "ANOM.";
            const isCro = e.h === "CRO";
            return (
              <div key={`d${e.m}-${i}`} role="option" aria-selected={false} className="flex flex-1 flex-col items-center gap-1 rounded-lg border border-transparent px-1 py-2">
                <span className="text-[10px] font-medium text-muted-foreground" style={{ overflowWrap: "anywhere" }}>{e.d}</span>
                <span className={`flex h-9 min-w-9 items-center justify-center rounded-full border px-1 text-[11px] font-semibold ${isAnom ? "border-amber-500 bg-amber-500/20 text-amber-700 dark:text-amber-300" : isDouble ? "border-emerald-500 bg-emerald-500/20 text-emerald-700 dark:text-emerald-300" : isCro ? "border-violet-500 bg-violet-500/20 text-violet-700 dark:text-violet-300" : e.x ? "border-dashed border-amber-500/60 bg-amber-500/10 text-amber-700 dark:text-amber-300" : e.h ? "border-primary/50 bg-primary/10 text-primary" : "border-dashed border-muted-foreground/40 text-muted-foreground"}`}>{e.m}</span>
                <span className="text-[10px] text-muted-foreground" style={{ overflowWrap: "anywhere" }}>
                  {e.h ? (isAnom ? "MARIA-VIPAVC!" : isCro ? "Saloka-CRO!" : isDouble ? e.h.replace("·", "×h").replace("★", "!") : `h${e.h}`) : ""}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* 1833 timeline */}
      <div className="mt-4 overflow-x-auto pb-1">
        <p className="mb-1 text-xs font-semibold text-muted-foreground">{t("Leto 1833-začetek (m1–m6 — restart s strani P259!)", "The 1833-start (m1–m6 — the restart continues on P259!)")}</p>
        <div className="flex min-w-[880px] items-end gap-1 sm:min-w-0" role="listbox" aria-label={t("Vrstice leta 1833", "The rows of 1833")}>
          {e1833.map((e, i) => {
            const isPesdirz = (e.h || "").includes("50");
            return (
              <div key={`f${e.m}-${i}`} role="option" aria-selected={false} className="flex flex-1 flex-col items-center gap-1 rounded-lg border border-transparent px-1 py-2">
                <span className="text-[10px] font-medium text-muted-foreground" style={{ overflowWrap: "anywhere" }}>{e.d}</span>
                <span className={`flex h-9 min-w-9 items-center justify-center rounded-full border px-1 text-[11px] font-semibold ${isPesdirz ? "border-primary bg-primary/20 text-primary" : e.x ? "border-dashed border-amber-500/60 bg-amber-500/10 text-amber-700 dark:text-amber-300" : "border-primary/50 bg-primary/10 text-primary"}`}>{e.m}</span>
                <span className="text-[10px] text-muted-foreground" style={{ overflowWrap: "anywhere" }}>
                  {e.h ? (isPesdirz ? "PESDIRZ×Himiz!" : `h${e.h}`) : ""}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* STRUNE + NITI + KRAJI */}
      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <div className="min-w-0 rounded-lg border bg-accent/40 p-4">
          <p className="text-sm [overflow-wrap:anywhere]">{t(PREDHODNIK_1831K_STRUNA.si, PREDHODNIK_1831K_STRUNA.en)}</p>
        </div>
        <div className="min-w-0 rounded-lg border bg-accent/40 p-4">
          <p className="text-sm [overflow-wrap:anywhere]">{t(PREDHODNIK_1832_STRUNA.si, PREDHODNIK_1832_STRUNA.en)}</p>
        </div>
      </div>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        <div className="min-w-0 rounded-lg border border-primary/40 bg-primary/5 p-4">
          <p className="text-sm [overflow-wrap:anywhere]">{t(PREDHODNIK_258_NITI.si, PREDHODNIK_258_NITI.en)}</p>
        </div>
        <div className="min-w-0 rounded-lg border bg-accent/40 p-4">
          <p className="text-sm [overflow-wrap:anywhere]">{t(PREDHODNIK_258_KRAJI.si, PREDHODNIK_258_KRAJI.en)}</p>
        </div>
      </div>
      <p className="mt-2 text-xs text-muted-foreground" style={{ overflowWrap: "anywhere" }}>
        {t(
          "★★★★★ RESTART-1833 (s10-spodaj): letnica '1833' ROKOPISNO nad datumom prve vrstice ([~3.|5.] Febr-DUEL 2:2!) — 4. restart notranjosti (1830/1831/1833 + 1873!). [~X-OPEN]: Mercina-3-variant · [~24.|2.]-Juli · [~1.|13.]-Nov-BARON · MARIA/Marino-m2/m3 · Griblje|Smrečje-h42 · Kreuz|Kraplje · Himiz|Simig-Šimič. P259+: 1833-nadaljevanje (s11 = Pag. 19!)",
          "★★★★★ THE 1833-RESTART: the year '1833' HANDWRITTEN above the first date — the 4th restart of the interior! [~X-OPEN]: the garble battery. P259+: the 1833 continuation (s11 = Pag. 19!)",
        )}
      </p>
    </div>
  );
}
'''

p = "src/components/museum/museum-atlas.tsx"
s = open(p, encoding="utf-8").read()

# 1) uvozi P258-konstant
old_imp = """  PREDHODNIK_257_KORPUS,"""
new_imp = """  PREDHODNIK_257_KORPUS,
  PREDHODNIK_1831K_TOTAL,
  PREDHODNIK_1831K_STRUNA,
  PREDHODNIK_1832_TOTAL,
  PREDHODNIK_1832_STRUNA,
  PREDHODNIK_1833_TOTAL,
  PREDHODNIK_1833_RESTART,
  PREDHODNIK_258_NITI,
  PREDHODNIK_258_KRAJI,
  PREDHODNIK_258_KORPUS,"""
assert old_imp in s, "uvoz-sidro"
s = s.replace(old_imp, new_imp, 1)

# 2) komponenta za Notranjost01738Leto1830_1831 (najdi njen konec = naslednja 'function ' po njej)
anchor = "function Notranjost01738Leto1830_1831() {"
i = s.find(anchor)
assert i > 0
# najdi naslednjo function-deklaracijo po njej
j = s.find("\nfunction ", i + 10)
assert j > 0
s = s[:j] + "\n" + COMPONENT.strip("\n") + "\n" + s[j:]

# 3) render za <Notranjost01738Leto1830_1831 />
old_render = "      <Notranjost01738Leto1830_1831 />"
assert old_render in s
s = s.replace(old_render, old_render + "\n      <Notranjost01738Leto1832 />", 1)

open(p, "w", encoding="utf-8").write(s)
print("Notranjost01738Leto1832 dodana + uvozi + render")
