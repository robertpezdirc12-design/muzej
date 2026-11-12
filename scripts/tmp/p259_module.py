#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — dodajanje P259-sekcije v parish-marriage-early.ts (za PREDHODNIK_258_KORPUS,
vrstica ~1347 '} as const;'). Data-driven: bere module-p259.txt (surov TS blok)."""
import sys

SRC = "src/data/atlas/parish-marriage-early.ts"
PART = "scripts/tmp/module-p259.txt"
ANCHOR = '  p259: "1833-nadaljevanje (s11 = Pag. 19: 6.-Febr-1833-restart-vrstice-šle-do-konca-strani!) → desetletja-1830er-do-šiva-1873",\n} as const;\n'

def main():
    src = open(SRC, encoding="utf-8").read()
    if ANCHOR not in src:
        print("SIDRO (P258_KORPUS konec) NI NAJDENO!"); sys.exit(1)
    part = open(PART, encoding="utf-8").read()
    if "PREDHODNIK_1833N_BLOCKS" not in part:
        print("ODLOMek ne vsebuje PREDHODNIK_1833N_BLOCKS — preveri vsebino!"); sys.exit(2)
    if "PREDHODNIK_1833N_BLOCKS" in src:
        print("P259-sekcija ŽE obstaja — preskok!"); sys.exit(0)
    src = src.replace(ANCHOR, ANCHOR + "\n" + part, 1)
    open(SRC, "w", encoding="utf-8").write(src)
    print("P259-sekcija dodana.")

if __name__ == "__main__":
    main()
