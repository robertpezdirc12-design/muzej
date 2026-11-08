#!/bin/bash
# P226 — odpor Watchdog-branec: bere s134/s135 + s119–s128, ponavlja do konca (429-varno!)
cd /home/z/my-project
PAGES="134 135 119 120 121 122 123 124 125 126 127 128"
START=$(date +%s)
DEADLINE=$((START + 7200))  # 2 h budget
while [ $(date +%s) -lt $DEADLINE ]; do
  ALLDONE=1
  for s in $PAGES; do
    if [ ! -f "/tmp/p226/vlm-page/s$s.json" ]; then
      ALLDONE=0
      echo "=== branje s$s ($(date +%H:%M:%S)) ==="
      timeout 540 bun scripts/tmp/p226_read_page.mjs "s$s" 2>&1 | grep -E "OK vrstice|FAIL|poskus" | tail -1
      sleep 15
    fi
  done
  [ $ALLDONE -eq 1 ] && { echo "VSE STRANI PREBRANE $(date +%H:%M:%S)"; exit 0; }
  sleep 30
done
echo "TIMEOUT 2h $(date +%H:%M:%S)"
