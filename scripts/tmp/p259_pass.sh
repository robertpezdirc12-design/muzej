#!/bin/bash
# P259 — sinhroni vodja z ČASOVNIM PRORAČUNOM (default 240s): poskuša nedokončane vrstice,
# izstopa ko je proračun porabljen. Stanje = obstoječi JSON-i (skip če obstajajo).
BUDGET=${1:-240}
START=$(date +%s)
cd /home/z/my-project
ROWS="s11_r2 s11_r3 s11_r4 s11_r5 s11_r6 s11_r7 s11_r8 s11_r9 s11_r10 s11_r11 s11_r12 s11_r13 s12_r1 s12_r2 s12_r3 s12_r4 s12_r5 s12_r6 s12_r7 s12_r8 s12_r9 s12_r10 s12_r11 s12_r12 s13_r1 s13_r2 s13_r3 s13_r4 s13_r5 s13_r6 s13_r7 s13_r8 s13_r9 s13_r10 s13_r11"
DONE=0; LEFT=0
for ROW in $ROWS; do
  if [ -s "/tmp/p259/full/${ROW}.json" ]; then DONE=$((DONE+1)); continue; fi
  NOW=$(date +%s); ELAPSED=$((NOW-START))
  if [ $ELAPSED -gt $BUDGET ]; then LEFT=$((LEFT+1)); continue; fi
  echo "[$(date +%H:%M:%S)] ${ROW} poskus (elapsed ${ELAPSED}s)" >> /tmp/p259/bashloop.log
  timeout 100 bun scripts/tmp/p259_one.mjs "$ROW" >> /tmp/p259/bashloop.log 2>&1
  RC=$?
  NOW=$(date +%s); ELAPSED=$((NOW-START))
  if [ $RC -eq 0 ] && [ -s "/tmp/p259/full/${ROW}.json" ]; then
    echo "[$(date +%H:%M:%S)] ${ROW} OK" >> /tmp/p259/bashloop.log
  else
    LEFT=$((LEFT+1))
    # pavza 25s (v proračun!) pred naslednjo vrstico/v poskusom
    REMAIN=$((BUDGET-ELAPSED)); [ $REMAIN -gt 25 ] && sleep 25
  fi
done
TOTAL=$(ls /tmp/p259/full/s1*_r*.json 2>/dev/null | wc -l)
echo "[$(date +%H:%M:%S)] KONEC PASA: done=${DONE} left=${LEFT} skupaj-json=${TOTAL}/36" >> /tmp/p259/bashloop.log
tail -1 /tmp/p259/bashloop.log
