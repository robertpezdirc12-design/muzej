#!/usr/bin/env python3
# P69 — priprava širokih izrezov cone p73–93 (sistemski pregled P38 pass1 slojev).
# Prenese strani iz VAČ (uodid 373415, docid 41780) in izreže LEVO TABELARNO
# CONO (Nro. des Blattes + Nro. der Parzelle + margini) — 4× Lanczos upscale,
# JPEG q92. ŠIROK izrez (x=0..430) popravlja P59 past "odrezane vodilne števke"
# (p76: 161-180 je bil odrez 1461-1480; p87: 161-180 je bil odrez 1681-1700).
#
# Vhod:  VAČ https://vac.sjas.gov.si/vac/util/pdfPageImage?uodid=373415&docid=41780&page=N
# Izhod: /tmp/p69/raw/<page>.jpg  (posnetek v izvorni ločljivosti)
#        /tmp/p69/wide-<page>.jpg (4× široki izrez)
#        /tmp/p69/manifest.json   (dimenzije + sha256)
# CLI:   python3 scripts/p69_fetch_zone.py "73-93" | "74" | "75,79,80"
import hashlib
import json
import os
import subprocess
import sys
import time

from PIL import Image

BASE = ("https://vac.sjas.gov.si/vac/util/pdfPageImage"
        "?uodid=373415&docid=41780&page={}")
RAW_DIR = "/tmp/p69/raw"
OUT_DIR = "/tmp/p69"
CROP = (0, 0, 430, None)  # levo, zgoraj, desno, spodaj (None = do konca)
SCALE = 4
MANIFEST = os.path.join(OUT_DIR, "manifest.json")


def parse_pages(arg: str) -> list[int]:
    out: list[int] = []
    for part in arg.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return sorted(set(out))


def fetch(page: int) -> str:
    out = os.path.join(RAW_DIR, f"{page}.jpg")
    if os.path.exists(out) and os.path.getsize(out) > 50_000:
        return out
    url = BASE.format(page)
    r = None
    for attempt in range(4):
        r = subprocess.run(
            ["curl", "-sk", "--max-time", "60", "-o", out, "-w", "%{http_code}",
             "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
             url],
            capture_output=True, text=True)
        if r.stdout.strip() == "200" and os.path.exists(out) and os.path.getsize(out) > 50_000:
            return out
        time.sleep(2 + 2 * attempt)
    raise RuntimeError(f"VAČ fetch strani {page} neuspešen: {r.stdout if r else '?'}")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    pages = parse_pages(sys.argv[1]) if len(sys.argv) > 1 else list(range(73, 94))
    os.makedirs(RAW_DIR, exist_ok=True)
    manifest = {}
    if os.path.exists(MANIFEST):
        manifest = json.load(open(MANIFEST, encoding="utf-8"))
    for page in pages:
        raw = fetch(page)
        img = Image.open(raw)
        w, h = img.size
        box = (CROP[0], CROP[1], min(CROP[2], w), CROP[3] if CROP[3] else h)
        crop = img.crop(box)
        big = crop.resize((crop.width * SCALE, crop.height * SCALE), Image.LANCZOS)
        out = os.path.join(OUT_DIR, f"wide-{page}.jpg")
        big.save(out, "JPEG", quality=92)
        manifest[str(page)] = {
            "raw": raw, "rawSha256": sha256(raw),
            "wide": out, "wideSha256": sha256(out),
            "rawSize": [w, h], "crop": list(box), "scale": SCALE,
        }
        print(f"p{page}: raw {w}x{h} -> wide {big.width}x{big.height} "
              f"sha {manifest[str(page)]['wideSha256'][:12]}")
    json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"manifest: {MANIFEST} ({len(manifest)} strani)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
