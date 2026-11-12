#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — QA-sekcija v qa-parish.ts: vstavi za qa-p258 (pred qa-p246-headerjem).
Data-driven: bere qa-p259-section.txt."""
import sys

SRC = "src/lib/qa-parish.ts"
SECT = "scripts/tmp/qa-p259-section.txt"
ANCHOR = "  // ——— qa-p246: POROČNA PREDZGOVINA 04455 — leto 1878 = 8/13 (P246) ———"

def main():
    src = open(SRC, encoding="utf-8").read()
    if 'qa-p259' in src:
        print("qa-p259 ŽE obstaja — preskok!"); sys.exit(0)
    if ANCHOR not in src:
        print("QA-sidro (qa-p246-header) ni najdeno!"); sys.exit(1)
    sect = open(SECT, encoding="utf-8").read()
    if "PREDHODNIK_1833N_BLOCKS" not in sect:
        print("ODLOMEK ne vsebuje P259-kontrol — preveri!"); sys.exit(2)
    # importi za P259-module (poišči PREDHODNIK_258_KORPUS v import bloku)
    imps = open("scripts/tmp/qa-p259-imports.txt", encoding="utf-8").read().strip()
    if imps:
        ia = "  PREDHODNIK_258_KORPUS,"
        if ia not in src:
            print("IMPORT-sidro v qa-parish.ts ni najdeno!"); sys.exit(3)
        src = src.replace(ia, ia + "\n" + imps, 1)
    src = src.replace(ANCHOR, sect.rstrip("\n") + "\n\n" + ANCHOR, 1)
    open(SRC, "w", encoding="utf-8").write(src)
    print("qa-p259-sekcija dodana.")

if __name__ == "__main__":
    main()
