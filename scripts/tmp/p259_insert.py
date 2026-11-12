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

    header = next((b.get("_header") for b in blocks if b.get("_header")), "  // ——— P259 ———")
    lines = ["\n" + header]
    pravih = 0
    for b in blocks:
        if "houseNo" not in b:
            continue  # psevdo-vnos (samo _header/_vitals*) — PRESKOČI!
        pravih += 1
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
    if pravih == 0:
        print("NOBENIH PRAVIH BLOKOV (brez houseNo) — preveri blocks-p259.json!"); sys.exit(1)
    insert = "\n".join(lines) + "\n"
    src = src[:m.end(1)] + insert + src[m.end(1):]

    # števci: POZOR — 'N vitalov' v parish.ts NE obstaja (števci živijo v pt-luknja-18-final.json
    # + qa-parish.ts — posodobita ju p259_oldverifier_update.py!). Tu le varnostna zamenjava:
    n_old = next((b.get("_vitalsOld") for b in blocks if b.get("_vitalsOld")), None)
    n_new = next((b.get("_vitalsNew") for b in blocks if b.get("_vitalsNew")), None)
    if n_old and n_new:
        c = src.count(f"{n_old} vitalov")
        if c:
            src = src.replace(f"{n_old} vitalov", f"{n_new} vitalov")
        print(f"števec {n_old}→{n_new} 'vitalov': zamenjanih {c} (0 = pričakovano, števci so v pt-luknja/qa!)")

    open(SRC, "w", encoding="utf-8").write(src)
    print(f"VSTAVLJENIH BLOKOV: {len([b for b in blocks if 'houseNo' in b])}")

if __name__ == "__main__":
    main()
