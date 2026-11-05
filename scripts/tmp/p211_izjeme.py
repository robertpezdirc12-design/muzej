#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P211 — krstne-izjeme-1866 v1: allow-ANCKOR + HEAD-if + paren-scanner + '))'-emit."""
from pathlib import Path
import subprocess

head = subprocess.run(["git", "show", "HEAD:src/lib/qa-parish.ts"], capture_output=True, text=True,
                      cwd="/home/z/muzej").stdout.split("\n")
p = Path("/home/z/muzej/src/lib/qa-parish.ts")
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


JOBS = [("P90) že obstaja", "37"), ("P91) že obstaja", "14"), ("P93) že obstaja", "48")]
done = {}
for frag, hn in JOBS:
    push_idx = next(i for i, l in enumerate(lines) if frag in l and "NOVA hiša" in l and "Errors.push" in l)
    allow_idx = max(i for i in range(push_idx) if lines[i].strip().startswith("const allow"))
    allow_key = lines[allow_idx].split(" // ")[0].strip()[:120]
    if allow_key not in done:
        h_allow = next(i for i, l in enumerate(head) if l.split(" // ")[0].strip()[:120] == allow_key)
        h_some = next(i for i in range(h_allow + 1, h_allow + 4) if "HOUSE_VITALS.some(" in head[i])
        ocode = head[h_some].split(" // ")[0].rstrip()
        assert ocode.count("(") - ocode.count(")") == 0, (frag, hn, "head-bal")
        m = ocode.find("HOUSE_VITALS.some(")
        after = ocode[m + len("HOUSE_VITALS.some("):]
        arrow = after.find("=>")
        body = after[arrow + 2:].rstrip()
        assert body.endswith(")))"), (frag, hn, body[-30:])
        body_core = body[:-2]
        assert body_core.count("(") - body_core.count(")") == 0, (frag, hn, "body-bal")
        terms = split_terms(body_core)
        assert terms[0].strip() == "v.houseNo === hn"
        some_idx = next(i for i in range(allow_idx + 1, push_idx + 1) if "HOUSE_VITALS.some(" in lines[i])
        hcomment = head[h_some].split(" // ", 1)[1] if " // " in head[h_some] else ""
        done[allow_key] = (some_idx, terms, ocode[:m + len("HOUSE_VITALS.some(")], hcomment)
    some_idx, terms, prefix, hcomment = done[allow_key]
    exc = f'!(v.bookSignature === "04106" && v.year === 1866 && hn === "{hn}")'
    if exc not in terms:
        terms.append(exc)
    newbody = " && ".join(terms)
    newcode = prefix + "(v) => " + newbody + "))"
    assert newcode.count("(") - newcode.count(")") == 0
    lines[some_idx] = newcode + (" // " + hcomment if hcomment else "")
    print(f"OK {frag} h{hn} -> vrstica-{some_idx + 1} (terms={len(terms)})")
p.write_text("\n".join(lines), encoding="utf-8")
print("SHRANJENO")
