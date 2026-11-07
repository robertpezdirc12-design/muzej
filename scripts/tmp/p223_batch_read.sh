#!/bin/bash
# P223 foreground batch reader — bere manjkajoče kropo po vrsti do timeouta
cd /home/z/my-project
TODO=("$@")
for b in "${TODO[@]}"; do
  if [ -f "/tmp/p223/vlm-krop/$b.json" ]; then continue; fi
  if [ -f "/tmp/p223/krop-grib/$b.png" ]; then DIR=krop-grib; else DIR=krop2; fi
  bun scripts/tmp/p223_read_krop.mjs "$b" 2>&1 | grep -E "OK|FAIL" | head -1
done
echo "BATCH-KONEC: $(ls /tmp/p223/vlm-krop/ | wc -l)/66"
