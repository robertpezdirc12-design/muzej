#!/usr/bin/env python3
"""
P9 — deterministično sledenje Kolpe na listu A04.
Metoda: za vsako višino y poišči kandidatne pasove (svetla vrsta med temnima
bregovoma, širina 80–320 px); nato dinamično programiranje (DP) poveže pasove
v NAJGLADKEJŠO pot čez list (minimalni stranski skoki). To odpravi lažne
kandidate (svetla polja), ki so prostorsko nepovezani.
"""
import cv2
import numpy as np
import json

def column_profile(im_gray, y, win=40):
    dark = (im_gray < 150).astype(np.float32)
    col = dark[y:y+win, :].mean(axis=0)
    col = np.convolve(col, np.ones(9)/9, mode='same')
    return col

def bands_at(im_gray, y, win=40, min_w=80, max_w=320, thr=0.06, bank=0.15):
    col = column_profile(im_gray, y, win)
    water = col < thr
    bands = []
    i = 0
    while i < len(water):
        if water[i]:
            j = i
            while j < len(water) and water[j]: j += 1
            w = j - i
            if min_w <= w <= max_w:
                li, ri = max(0, i-30), min(len(col), j+30)
                lb = col[li:i].max() if i > li else 0
                rb = col[j:ri].max() if ri > j else 0
                if lb > bank and rb > bank:
                    bands.append((i+j)/2)
            i = j
        else:
            i += 1
    return bands

def trace(im_path, y_from=30, y_to=None, stride=20):
    im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
    h, w = im.shape
    y_to = y_to or h - 80
    rows = list(range(y_from, y_to, stride))
    # kandidati po vrsticah
    cand = {}
    for y in rows:
        bs = bands_at(im, y)
        if bs:
            cand[y] = bs
    if not cand:
        return None, {}
    # DP: stanje = pasovni indeks; cena = |dx| med zaporednima vrsticama
    ys = sorted(cand)
    INF = 1e9
    dp = {y: [0.0]*len(cand[y]) for y in ys[:1]}
    back = {}
    prev_y = None
    for k, y in enumerate(ys):
        if k == 0:
            dp[y] = [0.0]*len(cand[y])
            continue
        py = ys[k-1]
        d = {y: [] for _ in [0]}
        dp[y] = []
        back[y] = []
        for cx in cand[y]:
            best_c, best_i = INF, None
            for pi, pcx in enumerate(cand[py]):
                c = dp[py][pi] + min(abs(cx - pcx), 600)  # kazen za skok
                if c < best_c:
                    best_c, best_i = c, pi
            dp[y].append(best_c)
            back[y].append(best_i)
    # sledimo nazaj od najcenejšega konca
    y_last = ys[-1]
    i_last = int(np.argmin(dp[y_last]))
    path = [(y_last, cand[y_last][i_last])]
    for k in range(len(ys)-1, 0, -1):
        y = ys[k]
        i = back[y][path[-1 - 0][0] == y and path[-1][1] and 0 or 0] if False else None
        # enostavneje: shranimo indekse
        break
    # ... naredimo še enkrat z indeksi
    idx = {y: 0 for y in ys}
    y_last = ys[-1]
    cur = int(np.argmin(dp[y_last]))
    seq = [(y_last, cand[y_last][cur])]
    for k in range(len(ys)-1, 0, -1):
        y = ys[k]
        prev = back[y][cur]
        py = ys[k-1]
        seq.append((py, cand[py][prev]))
        cur = prev
    seq.reverse()
    return seq, cand

def main():
    seq, cand = trace('public/atlas/n83-a04.jpg')
    print(f'DP sled: {len(seq)} točk')
    for y, x in seq[::5]:
        print(f'  y={y:4} x={x:6.0f}')
    print(f'\nSkupaj vrstic s kandidati: {len(cand)}')
    json.dump([[y, round(x,1)] for y, x in seq], open('research/georef-n83/p9-a04-dp-trace.json','w'), indent=0)
    print('→ research/georef-n83/p9-a04-dp-trace.json')

if __name__ == '__main__':
    main()
