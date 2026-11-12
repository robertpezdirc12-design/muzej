#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — generira /tmp/p259/hints.json: pilot-s11_r1 + H-dict iz p259_rows.mjs (35)."""
import json, re

src = open("scripts/tmp/p259_rows.mjs", encoding="utf-8").read()
m = re.search(r"const H = \{(.*?)\n\};", src, re.S)
body = m.group(1)
# JS object literal → JSON: ključi so goli (s11_r2:) → dodaj navednice
body = re.sub(r"(?m)^\s*(s1[123]_r\d+):", r'  "\1":', body)

pilot = open("scripts/tmp/p259_pilot.mjs", encoding="utf-8").read()
pm = re.search(r"const HINTS = \{(.*?)\n\};", pilot, re.S)
pbody = re.sub(r"(?m)^\s*(s11_r\d+):", r'  "\1":', pm.group(1))

obj = json.loads("{" + body.rstrip().rstrip(",") + "}")
pobj = json.loads("{" + pbody.rstrip().rstrip(",") + "}")

hints = {}
hints["s11_r1"] = pobj["s11_r1"]  # pilot verzija (rows.mxs nima r1)
for k, v in obj.items():
    hints[k] = v

assert len(hints) == 36, len(hints)
order = [f"s11_r{i}" for i in range(1, 14)] + [f"s12_r{i}" for i in range(1, 13)] + [f"s13_r{i}" for i in range(1, 12)]
assert set(order) == set(hints.keys()), sorted(set(order) ^ set(hints.keys()))
out = {k: hints[k] for k in order}
open("/tmp/p259/hints.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(f"hints.json: {len(out)} vrstic (pilot-r1 + rows-35)")
