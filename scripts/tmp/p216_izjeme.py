#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P215 — krstne-izjeme-1862: allow-termi za h9 (p91) + h10 (p92) v qa-parish.ts.
Vzorec P214 (p214_izjeme): NOVA-hiša-pini + HOUSE_VITALS.some(...) allow-termini."""
from pathlib import Path

p = Path("/home/z/muzej/src/lib/qa-parish.ts")
lines = p.read_text(encoding="utf-8").split("\n")

JOBS = [("P91) že obstaja", "14"), ("P93) že obstaja", "18"), ("P93) že obstaja", "48"), ("P95) že obstaja", "67")]

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

done = {}
for frag, hn in JOBS:
    push_idx = None
    for i, l in enumerate(lines):
        if frag in l and "NOVA hiša" in l and "Errors.push" in l and f'hn === "{hn}"' not in l:
            push_idx = i
            break
    if push_idx is None:
        print(f"⚠ {frag} h{hn}: push-ni-najdena!"); continue
    allow_idx = None
    for i in range(push_idx, max(0, push_idx - 40), -1):
        if lines[i].strip().startswith("const allow"):
            allow_idx = i
            break
    if allow_idx is None:
        print(f"⚠ {frag} h{hn}: allow-ni-najdena!"); continue
    some_idx = next(i for i in range(allow_idx, allow_idx + 4) if "HOUSE_VITALS.some(" in lines[i])
    line = lines[some_idx]
    hcomment = line.split(" // ", 1)[1] if " // " in line else ""
    code = line.split(" // ")[0].rstrip()
    m = code.find("HOUSE_VITALS.some(")
    prefix = code[:m + len("HOUSE_VITALS.some(")]
    after = code[m + len("HOUSE_VITALS.some("):]
    arrow = after.find("=>")
    body = after[arrow + 2:].rstrip()
    assert body.endswith(")))"), (frag, hn, body[-40:])
    body_core = body[:-2]
    terms = split_terms(body_core)
    exc = f'!(v.bookSignature === "04106" && v.year === 1862 && hn === "{hn}")'
    if exc not in terms:
        terms.append(exc)
        newbody = " && ".join(terms)
        newcode = prefix + "(v) => " + newbody + "))"
        assert newcode.count("(") - newcode.count(")") == 0, (frag, hn, "bal!")
        lines[some_idx] = newcode + (" // " + hcomment if hcomment else "")
        print(f"OK {frag} h{hn} -> vrstica-{some_idx + 1} (terms={len(terms)})")
    else:
        print(f"ŽE {frag} h{hn}")

p.write_text("\n".join(lines), encoding="utf-8")
print("SHRANJENO")
