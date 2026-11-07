#!/bin/bash
# P223 — resilient krop reader (sequential, retried)
cd /home/z/my-project
for round in $(seq 1 40); do
  ALLDONE=1
  for part in 1 2 3; do
    MISSING=""
    while read b; do
      [ -f "/tmp/p223/vlm-krop/$b.json" ] || MISSING="$MISSING $b"
    done < /tmp/p223/part_$part
    if [ -n "$MISSING" ]; then
      ALLDONE=0
      bun /home/z/my-project/scripts/tmp/p223_read_krop.mjs $MISSING >> /tmp/p223/reader_$part.log 2>&1
    fi
  done
  K2MISS=""
  for b in $(ls /tmp/p223/krop2/*.png 2>/dev/null | sed 's|/tmp/p223/krop2/||;s|\.png||'); do
    [ -f "/tmp/p223/vlm-krop/$b.json" ] || K2MISS="$K2MISS $b"
  done
  if [ -n "$K2MISS" ]; then
    ALLDONE=0
    bun /home/z/my-project/scripts/tmp/p223_read_krop2.mjs $K2MISS >> /tmp/p223/reader_k2.log 2>&1
  fi
  [ "$ALLDONE" = "1" ] && echo "VSE PREBRANO round=$round" >> /tmp/p223/reader_master.log && break
  echo "round=$round krop=$(ls /tmp/p223/vlm-krop/ | wc -l)/66" >> /tmp/p223/reader_master.log
  sleep 5
done
