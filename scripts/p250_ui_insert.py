#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P250-OBNOVA: UI MarriageEarly1874 (importi + komponenta + uporaba v ParishTab)."""
p = 'src/components/museum/museum-atlas.tsx'
src = open(p, encoding='utf-8').read()

imports = '''  MARRIAGE_1874_BLOCKS,
  MARRIAGE_1874_GRIBLJE,
  MARRIAGE_1874_TOTAL,
  MARRIAGE_1874_MEJA,
  MARRIAGE_1874_NUMBERING,
  FOLIACIJA_1874,
  MNOZICNI_DANI_1874,
  FIRSTYEAR_1874_REKORDI,
  H43_1874_PARALELA,
  HRIZAN_MILEK_1874,
  DOVGAN_1874_PODALJŠITEV,
  STAROSTI_1874,
  MARRIAGE_1874_METODA,
  MARRIAGE_1874_DUELS,
  MARRIAGE_1874_KONTEKST,
  MARRIAGE_1875_BLOCKS,'''
assert '  MARRIAGE_1875_BLOCKS,' in src, 'import-anchor!'
if 'MARRIAGE_1874_BLOCKS,' not in src:
    src = src.replace('  MARRIAGE_1875_BLOCKS,', imports, 1)
    print('importi-vstavljeni')

comp = '''function MarriageEarly1874() {
  const { t } = useLang();
  return (
    <div className="rounded-xl border bg-card/60 p-5">
      <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
        <BookOpen className="h-4 w-4 text-primary" aria-hidden />
        {t(
          "Poročna predzgodovina 04455 (P250): leto 1874 = 12/13",
          "The marriage prehistory 04455 (P250): the year 1874 = 12/13",
        )}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {t(
          `12/13 poročne predzgodovine (1873–1885): skeni s1–s7 (+ s1-vezalo!), ${MARRIAGE_1874_TOTAL} vpisov leta 1874 — BREZ preskokov (9. leto!). RESTART-1874 = s2-DNO (12. mejna varianta!-P249-napoved-FALSIFICIRANA!) + KNIJIŽNO-ODPIRANJE-Pag.-1-=-m18-'1873-Juni-11' (1873-m1–m17-NISO-v-tej-knjigi!) + ${MARRIAGE_1874_GRIBLJE} BLOKOV-NOV-REKORD (prej-6-P248!) + 10-DVIGOV (h43-34-let-NOV-ABSOLUTNI-REKORD!) + 3-MNOŽIČNI-DANI (8.-Februar-×5 + 11.-Februar-×5 + 14.-Juni-×2!) + P249-KOREKCIJA-m28-'28.-Avgust'!`,
          `12/13 of the marriage prehistory (1873–1885): scans s1–s7 (+ s1-the-cover!), ${MARRIAGE_1874_TOTAL} entries of 1874 — WITHOUT skips (the 9th year!). THE-RESTART = s2-BOTTOM (the-12th-boundary-variant!-the-P249-forecast-FALSIFIED!) + the-BOOK-OPENING-Pag.-1-=-m18-'Jun-11-1873' (the-1873-entries-m1–m17-NOT-in-this-book!) + ${MARRIAGE_1874_GRIBLJE} BLOCKS-NEW-RECORD (previously-6-P248!) + 10-FIRSTYEAR-LIFTS (h43-34-years-NEW-ABSOLUTE-RECORD!) + 3-MASS-WEDDING-DAYS + the-P249-CORRECTION-m28-'Aug-28'!`,
        )}
      </p>

      {/* Griblje poroke 1874 — vrstni red blokov */}
      <div className="mt-4 rounded-lg border bg-background/60 p-4">
        <h4 className="text-sm font-semibold">
          {t("Griblje poroke 1874 — vrstni red blokov (REKORD ×11!)", "The Griblje marriages 1874 — the block order (the RECORD ×11!)")}
          <span className="ml-2 rounded-full border px-2 py-0.5 text-[10px] font-medium text-primary">
            ×{MARRIAGE_1874_GRIBLJE}
          </span>
        </h4>
        <div className="mt-3 grid gap-2 sm:grid-cols-11">
          {MARRIAGE_1874_BLOCKS.map((h) => (
            <div key={h.houseNo + h.scan + h.whatSi.slice(40, 80)} className="rounded border bg-card/60 px-2 py-1.5 text-center min-w-0 [overflow-wrap:anywhere]">
              <div className="text-xs font-semibold tabular-nums">h{h.houseNo}</div>
              <div className="text-[9px] text-muted-foreground">s{h.scan} · Pag. {h.page}</div>
            </div>
          ))}
        </div>
        <p className="mt-1.5 text-[11px] font-mono text-muted-foreground">
          {t(MARRIAGE_1874_NUMBERING, MARRIAGE_1874_NUMBERING)}
        </p>
      </div>

      {/* anomalije */}
      <div className="mt-4 grid gap-3">
        <div className="rounded-lg border border-emerald-600/40 bg-emerald-600/10 p-4 text-emerald-900 dark:text-emerald-100">
          <h4 className="text-sm font-semibold">
            {t("★★★★★ 11-BLOKOV-NOV-REKORD + 10-DVIGOV (h43-34-let-NOV-ABSOLUTNI-REKORD!) + MNOŽIČNI-DANI-×3", "★★★★★ 11-BLOCKS-THE-NEW-RECORD + 10-FIRSTYEAR-LIFTS (h43-34-years-THE-NEW-ABSOLUTE-RECORD!) + the-MASS-DAYS-×3")}
          </h4>
          <p className="mt-1.5 text-xs">
            {t(
              `${FIRSTYEAR_1874_REKORDI} · ${MNOZICNI_DANI_1874}`,
              `${FIRSTYEAR_1874_REKORDI} · ${MNOZICNI_DANI_1874}`,
            )}
          </p>
          <p className="mt-2 text-[11px] text-muted-foreground">
            {t(MARRIAGE_1874_MEJA.restartSi, MARRIAGE_1874_MEJA.restartEn)}
          </p>
        </div>
        <div className="rounded-lg border border-amber-600/40 bg-amber-600/10 p-4 text-amber-900 dark:text-amber-100">
          <h4 className="text-sm font-semibold">
            {t("★★★ H43-BRULA-PARALELA (Marina-1874 == Katharina-1878!) + h42-PROMOCIJA-NAPAVED-IZPOLNJENA (Maria-Pegdirc!) + HRIŽAN-×4 + MILEK-×3", "★★★ THE-H43-BRULA-PARALLEL (Marina-1874 == Katharina-1878!) + the-h42-PROMOTION-FORECAST-FULFILLED (Maria-Pegdirc!) + HRIŽAN-×4 + MILEK-×3")}
          </h4>
          <p className="mt-1.5 text-xs">
            {t(
              `${H43_1874_PARALELA} · ${HRIZAN_MILEK_1874}`,
              `${H43_1874_PARALELA} · ${HRIZAN_MILEK_1874}`,
            )}
          </p>
          <p className="mt-2 text-[11px] text-muted-foreground">
            {t(MARRIAGE_1874_MEJA.tailSi, MARRIAGE_1874_MEJA.tailEn)}
          </p>
        </div>
        <div className="rounded-lg border border-sky-600/40 bg-sky-600/10 p-4 text-sky-900 dark:text-sky-100">
          <h4 className="text-sm font-semibold">
            {t("★★★ KNIŽNO-ODPIRANJE-m18/1873 (s1-vezalo!-1873-m1–m17-NISO-v-tej-knjigi!) + FOLIACIJA-5/5 (28/28!) + DOVGAN-12-LET + STAROSTI (52-l-rekord!-63-l-×2!-mladoletnici!)", "★★★ THE-BOOK-OPENING-m18/1873 (s1-the-cover!-the-1873-entries-m1–m17-NOT-in-this-book!) + FOLIACIJA-5/5 (28/28!) + DOVGAN-12-YEARS + the-AGES (the-52-y-record!-63-y-×2!-the-minors!)")}
          </h4>
          <p className="mt-1.5 text-xs">
            {t(
              `${MARRIAGE_1874_MEJA.knjiznoSi} · ${FOLIACIJA_1874} · ${DOVGAN_1874_PODALJŠITEV}`,
              `${MARRIAGE_1874_MEJA.knjiznoEn} · ${FOLIACIJA_1874} · ${DOVGAN_1874_PODALJŠITEV}`,
            )}
          </p>
          <p className="mt-2 text-[11px] text-muted-foreground">
            {t(MARRIAGE_1874_MEJA.tailSi, MARRIAGE_1874_MEJA.tailEn)}
          </p>
        </div>
        <div className="rounded-lg border border-rose-600/40 bg-rose-600/10 p-4 text-rose-900 dark:text-rose-100">
          <h4 className="text-sm font-semibold">
            {t("★★★ DATUM-DUELI-REŠENI (m12-'Jänner'→'Februar'-KROP!-m28-P249-KOREKCIJA-'28.-Avgust'!) + P-forenzika-m22-'Pribež' + KONTEKST-1874+1873", "★★★ THE-DATE-DUELS-RESOLVED (m12-'Jänner'→'February'-KROP!-m28-the-P249-CORRECTION-'Aug-28'!) + the-P-forensics-m22-'Pribež' + the-CONTEXT-1874+1873")}
          </h4>
          <p className="mt-1.5 text-xs">
            {t(MARRIAGE_1874_DUELS.join(" · "), MARRIAGE_1874_DUELS.join(" · "))}
          </p>
          <p className="mt-2 text-[11px] text-muted-foreground">
            {t(MARRIAGE_1874_KONTEKST.join(" · "), MARRIAGE_1874_KONTEKST.join(" · "))}
          </p>
        </div>
        <div className="rounded-lg border bg-background/60 p-4">
          <h4 className="text-sm font-semibold">
            {t("Metoda P250 (md5-7/7!-s7-križ-1:1-identičen-P249!-očesi-NAJPREJ!-mikro-forenzika-8×!-pasma-artefakti!)", "The P250 method (md5-7/7!-the-s7-cross-1:1-identical-to-P249!-the-eyes-FIRST!-the-micro-forensics-8×!-the-band-artifacts!)")}
          </h4>
          <p className="mt-1.5 text-[11px] font-mono text-muted-foreground">
            {t(MARRIAGE_1874_METODA, MARRIAGE_1874_METODA)}
          </p>
        </div>
      </div>
    </div>
  );
}

function MarriageEarly1875() {'''
assert 'function MarriageEarly1875() {' in src, 'comp-anchor!'
if 'function MarriageEarly1874()' not in src:
    src = src.replace('function MarriageEarly1875() {', comp, 1)
    print('komponenta-vstavljena')

usage = '''      {/* P250: poročna predzgodovina 04455 — leto 1874 = 12/13 */}
      <MarriageEarly1874 />
      {/* P249: poročna predzgodovina 04455 — leto 1875 = 11/13 */}
      <MarriageEarly1875 />'''
if '<MarriageEarly1874 />' not in src:
    src = src.replace('      <MarriageEarly1875 />', usage, 1)
    print('uporaba-vstavljena')

open(p, 'w', encoding='utf-8').write(src)
print('UI-obnovljen')
