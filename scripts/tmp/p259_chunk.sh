#!/bin/bash
# P259 — CHUNK: en kos potrpežljivega VLM cikla (BUDGET sekund, default 480).
# Nadaljuje kje je ostal (skip obstoječih JSON). Faze: rows → census → pass1 → pag.
# Pokliče ga cron-agent vsakih ~15 min dokler vse ni končano.
BUDGET=${1:-480}
START=$(date +%s)
cd /home/z/my-project
LOG=/tmp/p259/loop.log
ROWS="s11_r1 s11_r2 s11_r3 s11_r4 s11_r5 s11_r6 s11_r7 s11_r8 s11_r9 s11_r10 s11_r11 s11_r12 s11_r13 s12_r1 s12_r2 s12_r3 s12_r4 s12_r5 s12_r6 s12_r7 s12_r8 s12_r9 s12_r10 s12_r11 s12_r12 s13_r1 s13_r2 s13_r3 s13_r4 s13_r5 s13_r6 s13_r7 s13_r8 s13_r9 s13_r10 s13_r11"
CENSUS="L11 R11 L12 R12 L13 R13"
say() { echo "[$(date +%H:%M:%S)] $*" >> $LOG; }
elapsed() { echo $(( $(date +%s) - START )); }

for ROW in $ROWS; do
  [ $(( $(elapsed) )) -gt $BUDGET ] && break
  [ -s "/tmp/p259/full/${ROW}.json" ] && continue
  say "row ${ROW} poskus"
  timeout 110 bun scripts/tmp/p259_one.mjs "$ROW" >> $LOG 2>&1
  if [ -s "/tmp/p259/full/${ROW}.json" ]; then say "row ${ROW} OK"
  else say "row ${ROW} FAIL — umik 150s"; [ $(( $(elapsed) )) -le $BUDGET ] && sleep 150; fi
  [ $(( $(elapsed) )) -le $BUDGET ] && sleep 32
done
for C in $CENSUS; do
  [ $(( $(elapsed) )) -gt $BUDGET ] && break
  [ -s "/tmp/p259/census_${C}.json" ] && continue
  say "census ${C} poskus"
  timeout 110 bun scripts/tmp/p259_census_one.mjs "$C" >> $LOG 2>&1
  if [ -s "/tmp/p259/census_${C}.json" ]; then say "census ${C} OK"
  else say "census ${C} FAIL — umik 150s"; [ $(( $(elapsed) )) -le $BUDGET ] && sleep 150; fi
  [ $(( $(elapsed) )) -le $BUDGET ] && sleep 32
done
for S in 11 12 13; do
  [ $(( $(elapsed) )) -gt $BUDGET ] && break
  [ -s "/tmp/p259/pass1_s${S}.json" ] && continue
  say "pass1 s${S} poskus"
  timeout 110 bun scripts/tmp/p259_pass1_one.mjs "$S" >> $LOG 2>&1
  if [ -s "/tmp/p259/pass1_s${S}.json" ]; then say "pass1 s${S} OK"
  else say "pass1 s${S} FAIL — umik 150s"; [ $(( $(elapsed) )) -le $BUDGET ] && sleep 150; fi
  [ $(( $(elapsed) )) -le $BUDGET ] && sleep 32
done
for S in 11 12 13; do
  [ $(( $(elapsed) )) -gt $BUDGET ] && break
  [ -s "/tmp/p259/pag_s${S}.json" ] && continue
  say "pag s${S} poskus"
  timeout 110 bun scripts/tmp/p259_pag_one.mjs "$S" >> $LOG 2>&1
  if [ -s "/tmp/p259/pag_s${S}.json" ]; then say "pag s${S} OK"
  else say "pag s${S} FAIL — umik 150s"; [ $(( $(elapsed) )) -le $BUDGET ] && sleep 150; fi
  [ $(( $(elapsed) )) -le $BUDGET ] && sleep 32
done
# FAZA 5: DUELI (samo ko so VSE vrstice prebrane — kompoziti v /tmp/p259/duels/!)
if [ $(( $(ls /tmp/p259/full/s1*_r*.json 2>/dev/null | wc -l) )) -ge 36 ]; then
  for D in s11_dates s12_dates s13_dates s11_r2_gosling s12_r1_r2 s12_r5_schmig s12_r7_restart s13_r1_restart s13_r6_vrh s13_r11_marentic; do
    [ $(( $(elapsed) )) -gt $BUDGET ] && break
    [ -s "/tmp/p259/duels/${D}.json" ] && continue
    say "duel ${D} poskus"
    timeout 110 bun scripts/tmp/p259_duels.mjs "${D}" >> $LOG 2>&1 || true
    # p259_duels.mjs požene VSE jobe — skip-logika znotraj; preverimo ali je ta gotov:
    if [ -s "/tmp/p259/duels/${D}.json" ]; then say "duel ${D} OK"
    else say "duel ${D} FAIL/429 — umik 150s"; [ $(( $(elapsed) )) -le $BUDGET ] && sleep 150; fi
    [ $(( $(elapsed) )) -le $BUDGET ] && sleep 32
  done
fi
R=$(ls /tmp/p259/full/s1*_r*.json 2>/dev/null | wc -l)
C=$(ls /tmp/p259/census_*.json 2>/dev/null | wc -l)
P=$(ls /tmp/p259/pass1_s*.json 2>/dev/null | wc -l)
G=$(ls /tmp/p259/pag_s*.json 2>/dev/null | wc -l)
U=$(ls /tmp/p259/duels/*.json 2>/dev/null | wc -l)
say "CHUNK-KONEC: rows=${R}/36 census=${C}/6 pass1=${P}/3 pag=${G}/3 duels=${U}/10"
echo "rows=${R}/36 census=${C}/6 pass1=${P}/3 pag=${G}/3 duels=${U}/10"
