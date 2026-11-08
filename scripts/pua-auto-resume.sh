#!/bin/bash
# P5-b SAMODEJNO NADALJEVANJE — čaka na dvig VLM kvote (429), nato:
#   1) prebere PUA strani 35–49 (priimki P–Ž)
#   2) zgosti podatke (pua-parse.py) in generira TS vrstice (pua-gen-ts.py)
#   3) ponovno zažene OBE deterministični analizi (P5-a cross, P5-c W-most)
#      → preverba napovedi h32/h64/h65/h68 iz P5-c
#   4) commit + push (ročna integracija v research.ts/kartice ostane)
# Zagon: setsid nohup bash scripts/pua-auto-resume.sh &
# Omejitve: sandbox periodično čisti detached procese (znano iz P4/P5) —
# pošteno dokumentirano; skript je idempotenten (preskoči že prebrane strani).
cd /home/z/my-project || exit 1
LOG=research/p5/auto-log.txt
PAGES="35 36 37 38 39 40 41 42 43 44 45 46 47 48 49"

echo "=== $(date -u '+%Y-%m-%dT%H:%M:%SZ') zagon samodejnega nadaljevanja P5-b ===" >> "$LOG"
for i in $(seq 1 288); do   # 288 × 5 min = 24 h največ
  if timeout 90 bun scripts/probe-quick.mjs 2>/dev/null | grep -q "LLM probe OK"; then
    echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') kvota DVIGNJENA — berem strani 35–49" >> "$LOG"
    bun scripts/pua-read.mjs $PAGES >> "$LOG" 2>&1
    echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') branje končano — parse + gen + analizi" >> "$LOG"
    python3 scripts/pua-parse.py  >> "$LOG" 2>&1
    python3 scripts/pua-gen-ts.py >> "$LOG" 2>&1
    python3 scripts/pua-pt-cross.py    >> "$LOG" 2>&1
    python3 scripts/pua-pt-wbridge.py  >> "$LOG" 2>&1
    git add research/ scripts/ >> "$LOG" 2>&1
    git commit -m "P5-b (samodejno): PUA strani 35–49 prebrane + parse + gen + obe analizi ponovno zagnani [~] — preverba napovedi W.32/64/65/68" >> "$LOG" 2>&1
    for p in 1 2 3 4 5; do
      if git push deploy main >> "$LOG" 2>&1; then
        echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') push USPEL — samodejni cikel zaključen" >> "$LOG"
        break
      fi
      sleep 6
    done
    break
  fi
  # vsako uro zapiši status, da je viden napredek
  if [ $((i % 12)) -eq 0 ]; then
    echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') sonda $i: kvota še vedno 429" >> "$LOG"
  fi
  sleep 300
done
