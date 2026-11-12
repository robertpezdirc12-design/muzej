#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — UI: komponenta Notranjost01738Leto1833_1834 v museum-atlas.tsx.
Data-driven: bere ui-p259-component.txt (komponenta) + ui-p259-usage.txt (vrstica).
- komponento vstavi PRED 'function Notranjost01738Leto1832' (za-consistency: novejše gor? NE —
  P258-šlo-za-1832! P259-gre-ZA-njo: vstavi PRED prvo uporabo po definiciji 1832-komponente.)
  Dejansko: vstavi za zaključkom komponente Notranjost01738Leto1832 (iskalnik: naslednja
  'function ' po njenem 'return' koncu) + usage vrstico za '<Notranjost01738Leto1832 />'
  + importe (iz module-p259-imports.txt) za obstoječi import blok."""
import sys

SRC = "src/components/museum/museum-atlas.tsx"
COMP = "scripts/tmp/ui-p259-component.txt"
USAGE = "scripts/tmp/ui-p259-usage.txt"
IMPORTS = "scripts/tmp/ui-p259-imports.txt"

def main():
    src = open(SRC, encoding="utf-8").read()
    if "Notranjost01738Leto1833_1834" in src:
        print("UI P259 ŽE obstaja — preskok!"); sys.exit(0)
    comp = open(COMP, encoding="utf-8").read()
    usage = open(USAGE, encoding="utf-8").read()
    imps = open(IMPORTS, encoding="utf-8").read().strip().split("\n")

    # 1) usage: za '<Notranjost01738Leto1832 />'
    u = "      <Notranjost01738Leto1832 />"
    if u not in src:
        print("USAGE-sidro ni najdeno!"); sys.exit(1)
    src = src.replace(u, u + "\n" + usage.rstrip("\n"), 1)

    # 2) komponenta: za 'function Notranjost01738Leto1832' ... do naslednjega 'function ' ali konec —
    # vstavi PRED 'function Notranjost01738Leto1832' (št. vrstic 1904) — P259-starejše-po-vsebini-novejše-po-fazi:
    # kronološko gredo komponente 1829 → 1830_1831 → 1832 → 1833_1834 — torej ZA 1832!
    anchor = "function Notranjost01738Leto1832() {"
    if anchor not in src:
        print("COMP-sidro ni najdeno!"); sys.exit(1)
    # poišči konec 1832-komponente = naslednja vrstica 'function ' po njenem začetku
    i0 = src.index(anchor)
    j = src.find("\nfunction ", i0 + 10)
    if j == -1:
        print("konec-1832-komponente ni najden!"); sys.exit(1)
    src = src[:j] + "\n" + comp.rstrip("\n") + "\n" + src[j:]

    # 3) importi: za zadnji PREDHODNIK-import (poišči '  PREDHODNIK_258_KORPUS,' in dodaj za)
    ia = "  PREDHODNIK_258_KORPUS,"
    if ia not in src:
        print("IMPORT-sidro ni najdeno!"); sys.exit(1)
    src = src.replace(ia, ia + "\n" + "\n".join(imps), 1)

    open(SRC, "w", encoding="utf-8").write(src)
    print("UI P259 dodan (komponenta + usage + importi).")

if __name__ == "__main__":
    main()
