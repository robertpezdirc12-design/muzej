import io
for p in ["scripts/p248_restore_parish.py","scripts/p245_korekcija_modul.py","scripts/p245_worklog.py","scripts/process-panoramas.py","scripts/p45-sheet-anchors.py","scripts/p45-verify.py","scripts/p252_oldverifier_update.py"]:
    print("="*10,p)
    print("\n".join(io.open(p,encoding="utf-8").read().splitlines()[:8]))
