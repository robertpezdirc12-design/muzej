#!/bin/bash
# P259 — bash-vodja: za vsako vrstico pokliče one-shot bun-proces z retry.
# Proces lahko umre (SDK-fatal-429) — zanka preprosto poskusi znova.
cd /home/z/my-project
ROWS="s11_r2 s11_r3 s11_r4 s11_r5 s11_r6 s11_r7 s11_r8 s11_r9 s11_r10 s11_r11 s11_r12 s11_r13 s12_r1 s12_r2 s12_r3 s12_r4 s12_r5 s12_r6 s12_r7 s12_r8 s12_r9 s12_r10 s12_r11 s12_r12 s13_r1 s13_r2 s13_r3 s13_r4 s13_r5 s13_r6 s13_r7 s13_r8 s13_r9 s13_r10 s13_r11"
for ROW in $ROWS; do
  TRY=0
  until [ -s "/tmp/p259/full/${ROW}.json" ]; do
    TRY=$((TRY+1))
    echo "$(date +%H:%M:%S) ${ROW} poskus${TRY}" >> /tmp/p259/bashloop.log
    timeout 120 bun scripts/tmp/p259_one.mjs "$ROW" >> /tmp/p259/bashloop.log 2>&1
    RC=$?
    if [ $RC -eq 0 ] && [ -s "/tmp/p259/full/${ROW}.json" ]; then
      break
    fi
    # rastoča pavza: 20s + 10s/poskus, max 90s
    PAUSE=$((20 + TRY * 10)); [ $PAUSE -gt 90 ] && PAUSE=90
    sleep $PAUSE
    [ $TRY -ge 60 ] && { echo "$(date +%H:%M:%S) ${ROW} ODPUŠČEN po 60 poskusih" >> /tmp/p259/bashloop.log; break; }
  done
done
echo "$(date +%H:%M:%S) BASHLOOP DONE" >> /tmp/p259/bashloop.log
