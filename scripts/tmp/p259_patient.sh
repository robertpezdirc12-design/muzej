#!/bin/bash
# P259 — PATIENT driver: vse VLM jobe enega za drugim, 32s ritem (≈18/10min — varno pod 30/10min),
# ob 429 umik 150s. Faze: rows-36 → census-6 → pass1-3 → pag-3. Skupaj 48+3 zahtev.
# Tekče v ozadju; log = /tmp/p259/loop.log
cd /home/z/my-project
LOG=/tmp/p259/loop.log
ROWS="s11_r1 s11_r2 s11_r3 s11_r4 s11_r5 s11_r6 s11_r7 s11_r8 s11_r9 s11_r10 s11_r11 s11_r12 s11_r13 s12_r1 s12_r2 s12_r3 s12_r4 s12_r5 s12_r6 s12_r7 s12_r8 s12_r9 s12_r10 s12_r11 s12_r12 s13_r1 s13_r2 s13_r3 s13_r4 s13_r5 s13_r6 s13_r7 s13_r8 s13_r9 s13_r10 s13_r11"
CENSUS="L11 R11 L12 R12 L13 R13"
P1="11 12 13"
PAG="11 12 13"

say() { echo "[$(date +%H:%M:%S)] $*" >> $LOG; }

for ROW in $ROWS; do
  [ -s "/tmp/p259/full/${ROW}.json" ] && continue
  say "row ${ROW} poskus"
  timeout 110 bun scripts/tmp/p259_one.mjs "$ROW" >> $LOG 2>&1
  if [ -s "/tmp/p259/full/${ROW}.json" ]; then say "row ${ROW} OK"; sleep 32
  else say "row ${ROW} FAIL (429?) — umik 150s"; sleep 150; fi
done
say "ROWS-FAZA-KONCANA ($(ls /tmp/p259/full/s1*_r*.json 2>/dev/null | wc -l)/36)"

for C in $CENSUS; do
  [ -s "/tmp/p259/census_${C}.json" ] && continue
  say "census ${C} poskus"
  timeout 110 bun scripts/tmp/p259_census_one.mjs "$C" >> $LOG 2>&1
  if [ -s "/tmp/p259/census_${C}.json" ]; then say "census ${C} OK"; sleep 32
  else say "census ${C} FAIL — umik 150s"; sleep 150; fi
done
say "CENSUS-FAZA-KONCANA ($(ls /tmp/p259/census_*.json 2>/dev/null | wc -l)/6)"

for S in $P1; do
  [ -s "/tmp/p259/pass1_s${S}.json" ] && continue
  say "pass1 s${S} poskus"
  timeout 110 bun scripts/tmp/p259_pass1_one.mjs "$S" >> $LOG 2>&1
  if [ -s "/tmp/p259/pass1_s${S}.json" ]; then say "pass1 s${S} OK"; sleep 32
  else say "pass1 s${S} FAIL — umik 150s"; sleep 150; fi
done
say "PASS1-FAZA-KONCANA ($(ls /tmp/p259/pass1_s*.json 2>/dev/null | wc -l)/3)"

for S in $PAG; do
  [ -s "/tmp/p259/pag_s${S}.json" ] && continue
  say "pag s${S} poskus"
  timeout 110 bun scripts/tmp/p259_pag_one.mjs "$S" >> $LOG 2>&1
  if [ -s "/tmp/p259/pag_s${S}.json" ]; then say "pag s${S} OK"; sleep 32
  else say "pag s${S} FAIL — umik 150s"; sleep 150; fi
done
say "VSE-FAZE-KONCANE: rows=$(ls /tmp/p259/full/s1*_r*.json 2>/dev/null | wc -l)/36 census=$(ls /tmp/p259/census_*.json 2>/dev/null | wc -l)/6 pass1=$(ls /tmp/p259/pass1_s*.json 2>/dev/null | wc -l)/3 pag=$(ls /tmp/p259/pag_s*.json 2>/dev/null | wc -l)/3"
