#!/usr/bin/env python3
# P59 — priprava izrezov glav listov registra PS ("Nro. des Blattes").
# Prenese strani 5–139 iz VAČ pdfPageImage (uodid 373415, docid 41780) in
# izreže LEVI STOLPEC tabele (Nro. des Blattes + Bezeichnung + Nro. der
# Parzelle kot kontrola) — 3× Lanczos upscale, JPEG q92 (recept p41/P57).
#
# Izrez: x=30..250 (v izvornih ~1266×1023), polna višina — zajame numeralo
# tudi sred-strani (sprememba Blatta znotraj strani) in parčne številke kot
# samokontroliranje branja (navzkrižje s pageMap P56).
#
# Vhod:  VAČ https://vac.sjas.gov.si/vac/util/pdfPageImage?uodid=373415&docid=41780&page=N
# Izhod: /tmp/p59/raw/<page>.jpg  (posnetek v izvorni ločljivosti)
#        /tmp/p59/send-<page>.jpg (3× izrez)
#        /tmp/p59/manifest.json   (dimenzije + sha256 posnetkov)
import hashlib
import json
import os
import subprocess
import sys
import time

from PIL import Image

BASE = ("https://vac.sjas.gov.si/vac/util/pdfPageImage"
        "?uodid=373415&docid=41780&page={}")
RAW_DIR = "/tmp/p59/raw"
OUT_DIR = "/tmp/p59"
CROP = (30, 0, 250, None)  # levo, zgoraj, desno, spodaj(None=do konca)
SCALE = 3
PAGES = list(range(5, 140))  # S1 (5–127) + S2 (128–137) + S3 (138–139)


def fetch(page: int) -> str:
    out = os.path.join(RAW_DIR, f"{page}.jpg")
    if os.path.exists(out) and os.path.getsize(out) > 50_000:
        return out
    url = BASE.format(page)
    for attempt in range(4):
        r = subprocess.run(
            ["curl", "-sk", "--max-time", "60", "-o", out, "-w", "%{http_code}",
             "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
             url],
            capture_output=True, text=True)
        if r.stdout.strip() == "200" and os.path.getsize(out) > 50_000:
            return out
        time.sleep(2 + 2 * attempt)
    raise RuntimeError(f"VAČ fetch strani {page} neuspešen: {r.stdout}")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    os.makedirs(RAW_DIR, exist_ok=True)
    manifest = {"task": "P59 blatt header strips", "pages": {}}
    only = None
    if len(sys.argv) > 1:
        only = [int(x) for x in sys.argv[1].split(",")]
    for page in (only or PAGES):
        raw = fetch(page)
        im = Image.open(raw)
        w, h = im.size
        x0, y0, x1, _ = CROP
        strip = im.crop((x0, y0, x1, h))
        sw, sh = strip.size
        send = os.path.join(OUT_DIR, f"send-{page}.jpg")
        strip.resize((sw * SCALE, sh * SCALE), Image.LANCZOS).convert("RGB").save(
            send, "JPEG", quality=92)
        manifest["pages"][str(page)] = {
            "rawSize": [w, h],
            "rawSha256": sha256(raw),
            "stripSize": [sw * SCALE, sh * SCALE],
            "sendSha256": sha256(send),
        }
        print(f"stran {page}: {w}x{h} -> izrez {sw*SCALE}x{sh*SCALE} OK")
    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    print(f"manifest: {len(manifest['pages'])} strani")


if __name__ == "__main__":
    main()
