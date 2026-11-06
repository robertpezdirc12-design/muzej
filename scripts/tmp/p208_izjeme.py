#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P208 — krstne-izjeme-1869: paren-scanner-rebuild (recept-v3, HEAD-ancor + allow-ancor)."""
from pathlib import Path
import subprocess

head = subprocess.run(["git", "show", "HEAD:src/lib/qa-parish.ts"], capture_output=True, text=True,
                      cwd="/home/z/my-project/muzej-backup").stdout.split("\n")
p = Path("/home/z/my-project/muzej-backup/src/lib/qa-parish.ts")
lines = p.read_text(encoding="utf-8").split("\n")


def split_terms(body):
    terms, depth, cur, i = [], 0, "", 0
    while i < len(body):
        c = body[i]
        if c == '"':
            cur += c
            i += 1
            while i < len(body) and body[i] != '"':
                cur += body[i]
                i += 1
            cur += '"'
            i += 1
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if c == "&" and depth == 0 and body[i:i + 2] == "&&":
            terms.append(cur.strip())
            cur = ""
            i += 2
            continue
        cur += c
        i += 1
    terms.append(cur.strip())
    return [t for t in terms if t]


JOBS = [("P86) že obstaja", "28"), ("P87) že obstaja", "12"), ("P87) že obstaja", "73"),
        ("P88) že obstaja", "70"), ("P90) že obstaja", "20"), ("P94) že obstaja", "22"),
        ("P94) že obstaja", "49")]
done = set()
for frag, hn in JOBS:
    if (frag, hn) in done:
        continue
    push_idx = next(i for i, l in enumerate(lines) if frag in l and "NOVA hiša" in l and "Errors.push" in l)
    allow_idx = max(i for i in range(push_idx) if lines[i].strip().startswith("const allow"))
    some_idx = next(i for i in range(allow_idx + 1, push_idx + 1) if "HOUSE_VITALS.some(" in lines[i])
    code = lines[some_idx].split(" // ")[0].rstrip()
    key = code.strip()[:300]
    cands = [l for l in head if l.strip().startswith(key[:60])]
    # izberi-kandidata-z-NAJDALJŠIM-skupnim-prefiksom-s-code
    def cplen(l):
        a, b = l.strip(), code.strip()
        n = 0
        while n < min(len(a), len(b)) and a[n] == b[n]:
            n += 1
        return n
    orig = max(cands, key=cplen) if cands else None
    assert orig, (frag, hn, "head-match")
    ocode = orig.split(" // ")[0].rstrip()
    assert ocode.count("(") - ocode.count(")") == 0, (frag, hn, "head-balance")
    m = ocode.find("HOUSE_VITALS.some(")
    after = ocode[m + len("HOUSE_VITALS.some("):]
    arrow = after.find("=>")
    body = after[arrow + 2:].rstrip()
    assert body.endswith(")))"), (frag, hn, body[-20:])
    body_core = body[:-2]  # odstrani-some+-if-zaklepa (izjema-skrbi-za-svojo-')')
    assert body_core.count("(") - body_core.count(")") == 0, (frag, hn, "body-balance")
    terms = split_terms(body_core)
    assert terms[0].strip() == "v.houseNo === hn"
    exc = f'!(v.bookSignature === "04106" && v.year === 1869 && hn === "{hn}")'
    terms = [t for t in terms if not (t.startswith("!(") and "year === 1869" in t and f'hn === "{hn}"' in t)]
    terms.append(exc)
    newbody = " && ".join(terms)
    newcode = ocode[:m + len("HOUSE_VITALS.some(")] + "(v) => " + newbody + ")))"
    assert newcode.count("(") - newcode.count(")") == 0
    comment = " // " + orig.split(" // ", 1)[1] if " // " in orig else ""
    lines[some_idx] = newcode + comment
    done.add((frag, hn))
    print(f"OK {frag} h{hn} -> vrstica-{some_idx + 1} (terms={len(terms)})")
p.write_text("\n".join(lines), encoding="utf-8")
print("SHRANJENO")
