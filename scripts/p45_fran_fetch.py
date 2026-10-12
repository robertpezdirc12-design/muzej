#!/usr/bin/env python3
"""P45 — fran.si fetcher: SSKJ2 / Pleteršnik / Snoj-ETA entries for lexicon targets.
Saves raw fetch results to research/issue17/lexicon-verification-raw/{target}.json.
Read-only wrt lexicon data — verification layer only. No AI at runtime.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path

RAW = Path("/home/z/muzej/research/issue17/lexicon-verification-raw")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) muzej-griblje-verify/1.0"}

# target id -> headwords to query on fran.si (search form)
HEADWORDS = {
    "sskj-log": ["log"],
    "sskj-luta": ["luta", "luti"],
    "sskj-lopata": ["lopata"],
    "sskj-ajna": ["ajna", "ajn", "ajda"],
    "sskj-jedar": ["jedar", "jedarití"],
    "sskj-luka": ["luka"],
    "sskj-liza": ["liza"],
    "sskj-horga": ["horga", "hurga", "hurgati", "hurkati"],
    "sskj-orga": ["orga"],
    "sskj-golica": ["golica", "golec"],
    "sskj-sindel": ["šindel", "šindra"],
    "sskj-trava": ["trava"],
    "sskj-ving": ["ving", "vinga"],
    "sskj-einhart": ["einhart"],
    "sskj-guten": ["guten", "guta"],
    "sskj-poggi": ["poggi", "pog"],
    "pletersnik-slifa": ["šlifa", "šlif", "šljif"],
}


def get(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_html(seg: str) -> str:
    t = re.sub(r"<[^>]+>", " ", seg)
    t = unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def search_counts(page: str) -> dict:
    """fran.si search page: per-dictionary hit counts, e.g. 'SSKJ² 2 3'."""
    out = {}
    for m in re.finditer(r">([A-Za-zŠšŽžČčĐđ0-9²e\- ]{2,20})\s*<[^>]*>\s*(\d+)\s*<[^>]*>\s*(\d+)\s*<", page):
        name = m.group(1).strip()
        if name and int(m.group(2)) > 0:
            out[name] = {"entries": int(m.group(2)), "hits": int(m.group(3))}
    return out


def entry_links(page: str) -> dict:
    """entry URLs grouped by dictionary id path prefix."""
    out = {}
    for m in re.finditer(r'href="(/(\d{1,3})/[^"]+?/(\d+)/[^"?]+)\?[^"]*"', page):
        path, dictid, entryid = m.group(1), m.group(2), m.group(3)
        out.setdefault(dictid, []).append({"path": path, "id": entryid})
    return out


def entry_text(url: str) -> dict:
    try:
        page = get(url)
    except Exception as e:  # noqa: BLE001
        return {"url": url, "error": str(e)}
    # main content: entry heading + definitions
    m = re.search(r'<div[^>]*(?:class="[^"]*entry[^"]*"|id="[^"]*entry[^"]*")[^>]*>(.*?)(?:<div class="[^"]*related|<footer)', page, re.S)
    body = m.group(1) if m else page
    text = strip_html(body)
    # cut cookie banner noise
    for marker in ["Ta stran uporablja piškotke", "Piškotke uporablja"]:
        if marker in text:
            text = text.split(marker)[0] if text.index(marker) > 200 else text.split(marker)[-1]
    # keep the core definition window around the headword
    return {"url": url, "excerpt": text[:900]}


def main() -> int:
    only = set(sys.argv[1:])
    ok = fail = 0
    for tid, words in HEADWORDS.items():
        if only and tid not in only:
            continue
        out = {"target": tid, "source": "fran.si", "queries": {}}
        try:
            for w in words:
                q = urllib.parse.quote(w)
                page = get(f"https://fran.si/iskanje?View=1&Query={q}")
                counts = search_counts(page)
                links = entry_links(page)
                # SSKJ2 = dict 133, Pleteršnik = 136, ETA(Snoj) = 137, Zgodovinski = 138 (check by name)
                top = {}
                for did, lst in links.items():
                    if did in ("133", "136", "137", "138"):
                        top[did] = lst[:2]
                ex = []
                for did in ("133", "136", "137", "138"):
                    for lnk in top.get(did, [])[:1]:
                        ex.append(entry_text("https://fran.si" + lnk["path"] + f"?View=1&Query={q}"))
                out["queries"][w] = {"counts": counts, "links": top, "entries": ex}
                time.sleep(1.2)
            ok += 1
        except Exception as e:  # noqa: BLE001
            out["error"] = str(e)
            fail += 1
        (RAW / f"{tid}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{'OK ' if 'error' not in out else 'ERR'} {tid}")
    print(f"done: {ok} ok, {fail} err")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
