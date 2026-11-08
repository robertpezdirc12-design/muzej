#!/bin/bash
# P227 — odpor Watchdog-branec: probe s112–s119 (MEJA-1878/79 pred s119!)
cd /home/z/my-project
PAGES="112 113 114 115 116 117 118 119"
START=$(date +%s)
DEADLINE=$((START + 7200))  # 2 h budget
while [ $(date +%s) -lt $DEADLINE ]; do
  ALLDONE=1
  for s in $PAGES; do
    if [ ! -f "/tmp/p227/vlm-page/s$s.json" ]; then
      ALLDONE=0
      echo "=== branje s$s ($(date +%H:%M:%S)) ==="
      timeout 2400 bun scripts/tmp/p227_read_page.mjs "s$s" 2>&1 | grep -E "OK vrstice|FAIL|poskus" | tail -1
      sleep 45
    fi
  done
  [ $ALLDONE -eq 1 ] && { echo "VSE STRANI PREBRANE $(date +%H:%M:%S)"; exit 0; }
  sleep 30
done
echo "TIMEOUT 2h $(date +%H:%M:%S)"
