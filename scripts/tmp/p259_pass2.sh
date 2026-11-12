#!/bin/bash
# P259 — sinhroni vodja v2: potrpi na PRVI manjkajoči vrstici (30s med poskusi),
# ko uspe — teči skozi ostale zaporedno. Časovni proračun default 480s.
BUDGET=${1:-480}
START=$(date +%s)
cd /home/z/my-project
ROWS="s11_r2 s11_r3 s11_r4 s11_r5 s11_r6 s11_r7 s11_r8 s11_r9 s11_r10 s11_r11 s11_r12 s11_r13 s12_r1 s12_r2 s12_r3 s12_r4 s12_r5 s12_r6 s12_r7 s12_r8 s12_r9 s12_r10 s12_r11 s12_r12 s13_r1 s13_r2 s13_r3 s13_r4 s13_r5 s13_r6 s13_r7 s13_r8 s13_r9 s13_r10 s13_r11"

first_missing() {
  for R in $ROWS; do
    [ -s "/tmp/p259/full/${R}.json" ] || { echo "$R"; return; }
  done
  echo ""
}

while true; do
  NOW=$(date +%s); ELAPSED=$((NOW-START))
  [ $ELAPSED -gt $BUDGET ] && { echo "[$(date +%H:%M:%S)] proračun porabljen (${ELAPSED}s)" >> /tmp/p259/bashloop.log; break; }
  ROW=$(first_missing)
  [ -z "$ROW" ] && { echo "[$(date +%H:%M:%S)] VSE VRSTICE KONČANE!" >> /tmp/p259/bashloop.log; break; }
  echo "[$(date +%H:%M:%S)] ${ROW} poskus (elapsed ${ELAPSED}s)" >> /tmp/p259/bashloop.log
  timeout 100 bun scripts/tmp/p259_one.mjs "$ROW" >> /tmp/p259/bashloop.log 2>&1
  RC=$?
  NOW=$(date +%s); ELAPSED=$((NOW-START))
  if [ $RC -eq 0 ] && [ -s "/tmp/p259/full/${ROW}.json" ]; then
    echo "[$(date +%H:%M:%S)] ${ROW} OK ✓" >> /tmp/p259/bashloop.log
    # uspeh → 25s pavza (LIMIT 30/10min — varčen ritem 24/10min!)
    REMAIN=$((BUDGET-ELAPSED))
    [ $REMAIN -gt 25 ] && sleep 25
  else
    REMAIN=$((BUDGET-ELAPSED))
    [ $REMAIN -gt 30 ] && sleep 30
  fi
done
TOTAL=$(ls /tmp/p259/full/s1*_r*.json 2>/dev/null | wc -l)
echo "skupaj-json=${TOTAL}/36"
