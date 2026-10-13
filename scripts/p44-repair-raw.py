#!/usr/bin/env python3
"""P44: v2 popravilo — ubežni notranji narekovaji v vrednostih, popravljeni ključi,
dopolnitev odrezanih JSON-ov. Strani, ki ostanejo odrezane, gredo na ponovni VLM klic."""
import json, re, glob

RAW_DIR = "research/issue11/pz-raw"

STR_KEYS = ["label", "culture", "par", "narrativeBrief", "values", "yields", "rawText",
            "confidence", "pageKind", "pageNote", "sectionKind"]

def fix_value_quotes(line: str) -> str:
    """V vrsticah oblike "key": "value", ubeži notranje narekovaje v value."""
    m = re.match(r'^(\s*"[^"]+"\s*:\s*)"((.*)")(\s*,?\s*)$', line, re.S)
    if not m:
        return line
    prefix, value, rest = m.group(1), m.group(2), m.group(4)
    inner = value[1:-1]  # brez obrobnih narekovajev
    # ubeži vse notranje narekovaje
    inner = inner.replace('\\"', '\x00').replace('"', '\\"').replace('\x00', '\\"')
    return f'{prefix}"{inner}"{rest}'

def repair(text: str):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```\s*$", "", t)
    t = t.replace("\u201e", '"').replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2018", "'").replace("\u2019", "'")
    # manjkajoči narekovaj ključa: "areaKlafter: null → "areaKlafter": null
    t = re.sub(r'"([A-Za-z][A-Za-z0-9_]*)(:)', r'"\1"\2', t) if False else t  # prenevarno izpuščeno
    t = re.sub(r'"\s*areaKlafter\s*:', '"areaKlafter":', t)
    t = re.sub(r'"\s*areaJoch\s*:', '"areaJoch":', t)
    # po vrsticah: ubeži notranje narekovaje v nizovnih vrednostih
    lines = t.split("\n")
    lines = [fix_value_quotes(l) for l in lines]
    t = "\n".join(lines)
    # sledilne vejice
    t = re.sub(r",(\s*[}\]])", r"\1", t)
    # podvojeni ubežni: \"\" → \"
    t = t.replace(':\\"', ':"').replace('\\"}', '"}')
    return t

def try_parse(t):
    try:
        return json.loads(t)
    except Exception:
        return None

def complete_json(t):
    """Za odrezane izpise: poišči zadnji CELO sections[] element in dopolni."""
    for extra in ("}", "]}", "]}", "}]}", "}]}", "}}", "}}}"):
        p = try_parse(t + extra)
        if p:
            return p, extra
    # odreži do zadnjega popolnega elementa v rows/sections in dopolni
    for cut in list(re.finditer(r'\{\s*"(?:label|culture)"', t)):
        cand = t[:cut.start()]
        for extra in ("}}]}", "]}", "}]}", "}}", "}"):
            p = try_parse(cand + extra)
            if p and isinstance(p.get("sections"), list):
                return p, f"odrezano pri znaku {cut.start()} + {extra}"
    return None, None

fixed, needs_vlm = [], []
for f in sorted(glob.glob(f"{RAW_DIR}/pz-*.json")):
    d = json.load(open(f))
    if d["parseOk"]:
        continue
    page, raw = d["page"], d.get("raw") or ""
    t = repair(raw)
    parsed = try_parse(t)
    note = "lokalno popravljeno (ubežni narekovaji, fences)"
    if not parsed:
        parsed, how = complete_json(t)
        note = f"rekonstruirano iz odrezanega raw ({how})"
    if parsed and isinstance(parsed.get("sections"), list):
        d["parseOk"] = True
        d["structured"] = parsed
        d["repairNote"] = note
        json.dump(d, open(f, "w"), indent=1, ensure_ascii=False)
        fixed.append((page, note[:50]))
    else:
        needs_vlm.append(page)

print("POPRAVLJENE:")
for p, n in fixed:
    print(f"  pz-{p}: {n}")
print("POTREBUJEJO PONOVNI VLM KLIC:", needs_vlm)
