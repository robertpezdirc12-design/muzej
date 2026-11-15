import io,re
for p in ["scripts/gen-pwa-icons.py","scripts/p248_restore_parish.py","scripts/p245_korekcija_json.py","scripts/p245_korekcija_modul.py","scripts/p245_worklog.py","scripts/p45-sheet-anchors.py","scripts/p45-verify.py","scripts/process-panoramas.py","scripts/p252_oldverifier_update.py"]:
    s=io.open(p,encoding="utf-8").read()
    print(p, "| ROOT:", bool(re.search(r'^ROOT = ',s,re.M)), "| import os:", bool(re.search(r'^import os$',s,re.M)), "| hardcoded:", "/home/z/my-project" in s)
