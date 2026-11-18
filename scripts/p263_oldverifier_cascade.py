#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P263 — KASKADA starih verifierjev (p200–p262) + qa-parish: živi števci 2081→2085,
01738 69→73, sixBook 41→42/fiveBook 27→26, bothEraPorocna 41→42, tiers 41→42,
h29 (nov 01738 blok), h60-span 90→91, h11 31→33, SIX-listi +h29.

Uporaba: python scripts/p263_oldverifier_cascade.py [--dry]
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv

# (a) splošni števci — velja v VSEH verifierjih + qa-parish
GENERIC = [
    ("2081", "2085"),
    ("!== 69", "!== 73"),
    ('"01738": 69', '"01738": 73'),
    ("sixBook: 41", "sixBook: 42"),
    ("sixBook !== 41", "sixBook !== 42"),
    ("sixBook-41", "sixBook-42"),
    ("fiveBook: 27", "fiveBook: 26"),
    ("fiveBook !== 27", "fiveBook !== 26"),
    ("fiveBook-27", "fiveBook-26"),
    ("bothEraPorocna !== 41", "bothEraPorocna !== 42"),
    ("bothEra-poročna ≠ 41", "bothEra-poročna ≠ 42"),
    ("HOUSE_STORY_TIERS[0]?.houses !== 41", "HOUSE_STORY_TIERS[0]?.houses !== 42"),
    ("h60st.span !== 90", "h60st.span !== 91"),
    ("h60st.span !== 90", "h60st.span !== 91"),
    ("span-90/firstYear-1833", "span-91/firstYear-1833"),
    ("h11-31-bl", "h11-33-bl"),
]

# (b) SIX-listi: dodaj h29 (samo tam, kjer je 6-knjižna lista)
SIX_LIST_OLD = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "16", "17", "18", "19", "20", "22", "24", "26", "27", "28", "31", "32", "33", "35", "36", "39", "41", "42", "46", "47", "48", "53", "56", "60", "61", "62", "63", "65", "73"]
SIX_LIST_NEW = SIX_LIST_OLD[:-0] if False else ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "16", "17", "18", "19", "20", "22", "24", "26", "27", "28", "29", "31", "32", "33", "35", "36", "39", "41", "42", "46", "47", "48", "53", "56", "60", "61", "62", "63", "65", "73"]


def six_literal(nums):
    return "[" + ", ".join(f'"{n}"' for n in nums) + "]"


def patch(path):
    src = open(path, encoding="utf-8").read()
    orig = src
    for a, b in GENERIC:
        src = src.replace(a, b)
    # SIX-listi (dvojni narekovaji, kot v qa-parish)
    src = src.replace(six_literal(SIX_LIST_OLD), six_literal(SIX_LIST_NEW))
    if src != orig:
        if not DRY:
            open(path, "w", encoding="utf-8").write(src)
        print(f"[UPDATED] {os.path.relpath(path, ROOT)}")
        return 1
    return 0


def main():
    changed = 0
    files = [f"{ROOT}/src/lib/qa-parish.ts"]
    files += [p for p in sorted(glob.glob(f"{ROOT}/scripts/p2*.py"))
              if "oldverifier" not in os.path.basename(p) and "cascade" not in os.path.basename(p)
              and "p263" not in os.path.basename(p)]
    for f in files:
        changed += patch(f)
    print(("DRY-RUN: " if DRY else "") + f"skupaj spremenjenih: {changed}/{len(files)}")


if __name__ == "__main__":
    main()
