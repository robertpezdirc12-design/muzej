#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — vstavljanje blokov v parish.ts (DATA-DRIVEN: bere blocks-p259.json).
Mehanizem preizkušen na dummy-podatkih; prave bloke zamenjam ko VLM vrstice pridejo.
Vstavi za zadnjim P258-blokom (h49-1833, ~vrstica 14491)."""
import json, re, sys

SRC = "src/data/atlas/parish.ts"
DATA = "research/issue17/blocks-p259.json"   # [{houseNo, year, scan, page, whatSi, whatEn}, ...]

def esc(s):
    return s.replace('"', "'")

def main():
    blocks = json.load(open(DATA, encoding="utf-8"))
    src = open(SRC, encoding="utf-8").read()

    # najdi zadnji P258-blok (h49-1833) — sidro za vstavitev
    m = re.search(r'(\n  \{\n    houseNo: "49",\n    bookSignature: "01738",\n    year: 1833,[^\n]*\n(?:.*?\n)*?  \},)\n', src)
    if not m:
        print("SIDRO (h49-1833) NI NAJDENO!"); sys.exit(1)

    header = blocks[0].get("_header", "  // ——— P259 header ———")
    lines = ["\n" + header]
    for b in blocks:
        lines.append(f'''  {{
    houseNo: "{b["houseNo"]}",
    bookSignature: "01738",
    year: {b["year"]},
    scan: {b["scan"]},
    page: {b["page"]},
    whatSi: "{esc(b["whatSi"])}",
    whatEn: "{esc(b["whatEn"])}",
    status: "DOCUMENTED" as const,
  }},''')
    insert = "\n".join(lines) + "\n"
    src = src[:m.end(1)] + insert + src[m.end(1):]

    # števci na vrhu datoteke (vitalsTotal ipd. — poišči komentar skupnega števca)
    n_old, n_new = b.get("_vitalsOld"), b.get("_vitalsNew")
    if n_old and n_new:
        c = src.count(f"{n_old} vitalov")
        src = src.replace(f"{n_old} vitalov", f"{n_new} vitalov")
        print(f"števec {n_old}→{n_new} vitalov: zamenjanih {c}")

    open(SRC, "w", encoding="utf-8").write(src)
    print(f"VSTAVLJENIH BLOKOV: {len([b for b in blocks if 'houseNo' in b])}")

if __name__ == "__main__":
    main()
