#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — generator UI-komponente Notranjost01738Leto1833_1834 iz podatkov.
Bere ui-p259-data.json: {e1833n: [{m,d,h,x}], e1834: [...], hi_labele: {...}} →
izpiše scripts/tmp/ui-p259-component.txt + ui-p259-usage.txt + ui-p259-imports.txt.
POZOR: whatSi/En niti so ročno dodane v DATA (nitiSi/nitiEn)."""
import json, sys

DATA = "scripts/tmp/ui-p259-data.json"

def esc(s):
    return s.replace('"', "'").replace("`", "'")

def arr(name, rows):
    out = [f"  const {name}: {{ m: string; d: string; h?: string; x?: boolean }}[] = ["]
    for e in rows:
        h = f', h: "{e["h"]}"' if e.get("h") else ""
        x = ", x: true" if e.get("x") else ""
        out.append(f'    {{ m: "{e["m"]}", d: "{esc(e["d"])}"{h}{x} }},')
    out.append("  ];")
    return "\n".join(out)

def timeline_jsx(name, label_si, label_en, keyprefix):
    # POZOR: predloga je NAVADEN niz (ne f-string!) — zamenjave @@…@@.
    # Razlog: f-string bi zahteval podvajanje VSEH zavitih oklepajev JSX ({{/}}),
    # kar je v prejšnji različici povzročilo NEURAVNOVEŠEN izpis (68:64)!
    # Vzorec sledi delujoči P258-komponenti (museum-atlas.tsx ~L1632–1650!).
    t = '''      {/* @@NAME@@ timeline */}
      <div className="mt-4 overflow-x-auto pb-1">
        <p className="mb-1 text-xs font-semibold text-muted-foreground">{t("@@LSI@@", "@@LEN@@")}</p>
        <div className="flex min-w-[880px] items-end gap-1 sm:min-w-0" role="listbox" aria-label={t("Vrstice @@NAME@@", "The rows of @@NAME@@")}>
          {@@NAME@@.map((e, i) => {
            const isDouble = (e.h || "").includes("·");
            const isViolet = e.h === "BARON" || e.h === "CRO" || e.h === "GROS";
            return (
              <div key={`@@KP@@-${e.m}-${i}`} role="option" aria-selected={false} className="flex flex-1 flex-col items-center gap-1 rounded-lg border border-transparent px-1 py-2">
                <span className="text-[10px] font-medium text-muted-foreground" style={{ overflowWrap: "anywhere" }}>{e.d}</span>
                <span className={`flex h-9 min-w-9 items-center justify-center rounded-full border px-1 text-[11px] font-semibold ${isDouble ? "border-emerald-500 bg-emerald-500/20 text-emerald-700 dark:text-emerald-300" : isViolet ? "border-violet-500 bg-violet-500/20 text-violet-700 dark:text-violet-300" : e.x ? "border-dashed border-amber-500/60 bg-amber-500/10 text-amber-700 dark:text-amber-300" : "border-primary/50 bg-primary/10 text-primary"}`}>{e.m}</span>
                <span className="text-[10px] text-muted-foreground" style={{ overflowWrap: "anywhere" }}>
                  {e.h ? (isDouble ? e.h.replace("·", "×h").replace("★", "!") : e.h) : ""}
                </span>
              </div>
            );
          })}
        </div>
      </div>'''
    for k, v in {
        "@@NAME@@": name,
        "@@LSI@@": esc(label_si),
        "@@LEN@@": esc(label_en),
        "@@KP@@": keyprefix,
    }.items():
        t = t.replace(k, v)
    return t

def main():
    import os
    if not os.path.exists(DATA):
        print(f"MANJKA {DATA}! Zapiši ga po integraciji (e1833n/e1834/hi_labele/nitiSi/nitiEn + korpus_card/kraji_card — glej p259-runbook KORAK 4-5!) in ponovno zaženi.")
        sys.exit(2)
    d = json.load(open(DATA, encoding="utf-8"))
    n3 = len(d["e1833n"]); n4 = len(d["e1834"])
    _intro_si = d.get("introSi", "1833-NADALJEVANJE (s11+s12, Pag. 19/21): kaskada 6. Febr se nadaljuje — skupaj ★ 13 POROK NA 6. 2. 1833 (novi rekord korpusa!) + 13. 2. ×5 + leto 1833 = 25 vpisov (največje leto notranjosti!). ★ ROBNO ŠTEVLJENJE se začne z rob=1 (27. 11. 1833) in teče čez mejo leta do rob=18! 1834-RESTART (s12: [~22.|27.] Jän, rob=2 — 5. restart!) + 29. Jän ×4 + februarska kaskada rob 8–14 ([~5.×7-ali-9.+10.×5 — s13_dates-duel!]) + 9. Febr + 10. Febr ×3 — nadaljevanje na s14 (P260!)")
    _intro_en = d.get("introEn", "The 1833-CONTINUATION (s11+s12, Pag. 19/21): the Feb-6 cascade continues — ★ 13 WEDDINGS ON FEB 6 1833 altogether (the new corpus record!) + Feb 13 ×5 + the year 1833 = 25 entries (the largest interior year!). ★ THE MARGIN NUMBERING begins with rob=1 (Nov 27 1833) and runs ACROSS the year boundary to rob=18! The 1834-RESTART (s12, rob=2 — the 5th restart!) + Jan 29 ×4 + the February cascade rob 8–14 ([~5×7-vs-9+10×5 — the s13_dates duel!]) + Feb 9 + Feb 10 ×3 — continues on s14 (P260!)")
    _intro_si = esc(_intro_si); _intro_en = esc(_intro_en)
    tl = "\n".join([
        timeline_jsx("e1833n", d.get("label1833n", "1833-konec (m7–m25 — 13 porok na 6. 2. + robno številčenje!)"), d.get("label1833nEn", "The 1833-end (m7–m25 — 13 weddings on Feb 6 + the margin numbering!)"), "g"),
        timeline_jsx("e1834", d.get("label1834", "Leto 1834 (m1–m17 — restart + februarska kaskada [~5.×7-ali-9.+10.×5-duel!])"), d.get("label1834En", "The year 1834 (m1–m17 — the restart + the February cascade)"), "h"),
    ])
    korp = d["korpus_card"]
    niti = d["niti_card"]
    kraj = d["kraji_card"]
    comp = f'''function Notranjost01738Leto1833_1834() {{
  const {{ t }} = useLang();
{arr("e1833n", d["e1833n"])}
{arr("e1834", d["e1834"])}
  return (
    <div className="rounded-xl border bg-card/60 p-5">
      <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
        <BookOpenCheck className="h-4 w-4 text-primary" aria-hidden />
        {{t(
          "Notranjost knjige 01738: 1833-konec + 1834-začetek ({n3} + {n4} vpisov — 13 porok na 6. 2. 1833 = rekord!)",
          "The interior of the book 01738: the 1833-end + the 1834-start ({n3} + {n4} entries — 13 weddings on Feb 6 1833 = the record!)",
        )}}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground [overflow-wrap:anywhere]">
        {{t(
          "{_intro_si}",
          "{_intro_en}",
        )}}
      </p>

{korp}

{niti}

{tl}

{kraj}
      <p className="mt-2 text-xs text-muted-foreground" style={{{{ overflowWrap: "anywhere" }}}}>
        {{t(
          "★★★★★ Datumska dueli: [~19.|12.]-Febr-m20 · [~19.|10.|26.]-Oct-m24 · [~22.|27.]-Jän-1834 · [~5.|8.]-Febr-rob8 (post-1834-začne-12.2. — koledar-ne-odloča!). P260+: 1834-nadaljevanje (s14 = Pag. 25!).",
          "★★★★★ The date duels: [~19.|12.]-Feb-m20 · [~19.|10.|26.]-Oct-m24 · [~22.|27.]-Jan-1834 · [~5.|8.]-Feb-rob8 (Lent-1834-starts-12.2.-calendar-neutral!). P260+: the 1834 continuation (s14 = Pag. 25!).",
        )}}
      </p>
    </div>
  );
}}
'''
    open("scripts/tmp/ui-p259-component.txt", "w", encoding="utf-8").write(comp)
    open("scripts/tmp/ui-p259-usage.txt", "w", encoding="utf-8").write("      <Notranjost01738Leto1833_1834 />")
    imps = "\n".join(d["imports"])
    open("scripts/tmp/ui-p259-imports.txt", "w", encoding="utf-8").write(imps)
    print(f"UI komponenta generirana: {n3}+{n4} vrstic.")

if __name__ == "__main__":
    main()
