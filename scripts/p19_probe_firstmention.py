#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P19: prototip regresijske kontrole 'prva omemba vasi' (1468, ne 1526).
Preizkuša vzorce na dejanskih podatkih, da se izognemo lažnim pozitivom."""
import json
import re

BASE = "/home/z/my-project/muzej-analysis"

# fraze visoke natančnosti: če se pojavijo v stavku, mora biti v stavku 1468
PHRASES = [
    "prva omemba vasi", "prva pisna omemba vasi",
    "prva omemba Gribelj", "prva pisna omemba Gribelj",
    "first mention of the village", "first written mention of Griblje",
    "first mention of Griblje",
]

# prožnejši vzorec (oba reda, razdalja 150): prvi* + (omemba/izpriča/zapiše/...) + vas-beseda
W1 = r"omemb\w*|izpri\w*|zapi[sš]e\b|zapisala\b|zapisan\w*|attest\w*|mention\w*|record\w*"
V1 = r"vasi\b|vas\b|Griblje\b|Griblach\b|village\b"
PATTERNS = [
    re.compile(rf"\bprv[ai]\w*\b[^.{{}}]{{0,150}}\b(?:{W1})\b[^.{{}}]{{0,150}}\b(?:{V1})", re.I),
    re.compile(rf"\b(?:{V1})[^.{{}}]{{0,150}}\bprv[ai]\w*\b[^.{{}}]{{0,150}}\b(?:{W1})\b", re.I),
]

def sentences(text):
    return re.split(r"(?<=[.!?])\s+|\n", text or "")

# cerkveni kontekst pri vzorcu (ne pri frazah!): »cerkev prvič zapisana 1526« je legitimna
CHURCH = re.compile(r"cerkev\b|cerkve\b|cerkvi\b|church\b|sv\.? Vid|St\.? Vitus|sv\.? Mark|St\.? Mark", re.I)

def violations(blob, where, year=""):
    out = []
    for s in sentences(blob):
        # letnica postaje (polje year) šteje kot zasidranje trditve
        anchor = s + " " + (year or "")
        phrase_hit = any(p in s.lower() for p in PHRASES)
        pattern_hit = not CHURCH.search(s) and any(p.search(s) for p in PATTERNS)
        if (phrase_hit or pattern_hit) and "1468" not in anchor:
            out.append((where, s.strip()[:160], "frazа" if phrase_hit else "vzorec"))
    return out

ev = json.load(open(f"{BASE}/src/data/museum/events.json", encoding="utf-8"))
ex = json.load(open(f"{BASE}/src/data/museum/exhibits.json", encoding="utf-8"))
extra = json.load(open(f"{BASE}/src/data/museum/extra.json", encoding="utf-8"))

bad = []
for e in ev["events"]:
    for k in ("titleSi", "titleEn", "descriptionSi", "descriptionEn"):
        bad += violations(e.get(k), f"dogodek/{e['id'][:8]}/{k}")
for e in ex["exhibits"]:
    for k in ("summarySi", "summaryEn"):
        bad += violations(e.get(k), f"{e['museumNo']}/{k}")
for slug, story in extra.items():
    for st in story.get("lifeStations") or []:
        bad += violations(st.get("description"), f"postaja {slug}/{st.get('year')}", st.get("year") or "")

print(f"KONTROLA 1 (dogodki + povzetki + postaje, letnica postaje šteje): {len(bad)} kršitev")
for w, s, kind in bad:
    print(f"  ✗ [{kind}] {w}: {s}")

#kontrola 2: tudi zgodbe (lahko hrupno — samo poročilo)
bad2 = []
for e in ex["exhibits"]:
    for k in ("storySi", "storyEn"):
        bad2 += violations(e.get(k), f"{e['museumNo']}/{k}")
print(f"\nKONTROLA 2 (+ zgodbe): {len(bad2)} kršitev")
for w, s, kind in bad2[:12]:
    print(f"  ✗ {w}: {s}")
