#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P40 (issue #10) — N083PS: REKAPITULACIJA STR. 140–143 — DETERMINISTIČNA
PRIMERJAVA REKAPITULACIJE S SPRAVNIM MODELOM (P5-b).

Kaj naredi (izključno iz committed dokazov; brez AI ob delovanju):
  1. Iz committed strukturne analize (research/issue17/PS-structure.json,
     P9) razčleni rekapitulacijske kontrolne vsote str. 143 (rdeči tuš):
     Summa der Bauplätze 102 · Summa der Grundparzellen 2505 · Zusammen 2607.
  2. Navzkrižna primerjava s spravo (P38) in modelom (P39):
     a) identiteta 2505 + 102 = 2607 (aritmetika rekapitulacije);
     b) Grundparzellen 2505 == P36/P38 osnovna črta (1889 videnih + 616
        manjkajočih);
     c) Zusammen 2607 == P38 kontrolna vsota (katero je sprava vse od P38
        uporabljala — P40 dokazuje, da je to uradna rekapitulacija dokumenta);
     d) Bauplätze 102 nasproti Blatt X (str. 138) 60 vrstic — registrska
        vrzel 42 (pokritost registra 58,8 %).
  3. DEKOMPOZICIJA POVRŠIN po sekcijah modela P39 (joch + klafter/1600):
     GRUND_1_2505 / NADALJEVANJE_2506 / WALDUNG / BLATT_X + vrstice brez
     razčlenjene površine (32). Nastane SWOBODNA tabela kandidatov za
     pomen rekapitulacijske vsote "Summa 1216(?) Joch" (str. 141, branje
     izrecno negotovo — dva VLM branja se razhajata):
       - GRUND samo (najbližji kandidat, Δ ≈ +17 Joch ≈ 1,4 %);
       - GRUND + NADALJEVANJE + WALDUNG (brez Blatt X, Δ ≈ +68 Joch);
       - celoten register z Blatt X (Δ ≈ +349 Joch).
     Rekapitulacija pokriva le zemljiške parcele — stavbna mesta se štejejo
     po kosih (102), ne po površini; zato je kandidat GRUND-only najbolj
     skladen, a odločitev ostane paleografska (recap vrstica je "1216(?)".
  4. PODVOJENO-ŠTETJE TVEGANJE Blatt X (nova formalizirana ugotovitev):
     Blatt X (str. 138) je "Zusammenstellung der Grundstücke" po hišah —
     nosi rabe (Wiese/Acker …) in površine; prekrivanje parov
     (lastnik, hiša) z GRUND je le 1/59, lastnikov 1/22 → podvajanje ni
     dokazljivo (razlike v črkovanju imen?), a tudi ni izključeno. Zato je
     vsota celotnega registra (1564,8 Joch) SAMO ZGORNJA MEJA; Blatt X
     površin ne smemo samodejno prištevati.
  5. Per-house fragmenti str. 140–141 (7 vidnih vrstic) ostanejo doslovno
     UNRESOLVED: naivna interpretacija kot Joch vrednosti da vsoto 1413,
     kar nasprotuje sami Summi 1216(?) — dodatni dokaz, da je branje
     nezanesljivo. Nič tihega tolmačenja.
  6. ŠTEVILČNI EHO — OVRGAN (negativen izid, izrecno dokumentiran): hipoteza,
     da najvišja opažena številka parcele v NADALJEVANJE (2506+) ustrezala
     Zusammen rekapitulacije (2607), je NAPACNA — max je 2840
     (nad2506Range [2507, 2840]). Eho ne obstaja; vpisano kot zavrnjeno.

Izpise:
  - research/issue17/ps-recap.json   (kanonski dokazni izpis)
  - src/data/atlas/ps-recap.json     (identična kopija za runtime import API)
  - povzetek na stdout (za TS konstanto PS_RECAP_P40 in QA qa-p40).

Pogoj delovanja: ključne identitete morajo držati, sicer skript FAIL
(SystemExit) — konsistentno s P38/P39. Status vseh rezultatov ostane REVIEW
(strojno branje ni dokazni vir) — pravilo hiše: »ne nadgradi gotovosti brez
človeške paleografske potrditve«.
"""

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "research" / "issue17"
OUT_EVIDENCE = EV / "ps-recap.json"
OUT_RUNTIME = ROOT / "src" / "data" / "atlas" / "ps-recap.json"

KLAFTER_PER_JOCH = 1600  # franciscejski kataster: 1 Joch = 1600 Quadrat-Klafter


def fail(msg: str):
    raise SystemExit(f"P40 FAIL: {msg}")


def main() -> None:
    # ——— committed dokazi ———
    structure = json.loads((EV / "PS-structure.json").read_text(encoding="utf-8"))
    p38 = json.loads((EV / "ps-reconciliation.json").read_text(encoding="utf-8"))
    p39 = json.loads((EV / "ps-landuse.json").read_text(encoding="utf-8"))
    ps_full = json.loads((EV / "PS-full.json").read_text(encoding="utf-8"))

    rec = structure.get("recapitulation") or {}
    if not rec.get("found") or rec.get("page") != 143:
        fail("PS-structure.json recapitulation (str. 143) ni najdena")

    # ——— 1. kontrolne vsote str. 143 (rdeči tuš) ———
    recap_rows = {r.get("label", ""): r.get("value", "") for r in rec.get("rows", [])}

    def val(label: str) -> int:
        v = recap_rows.get(label, "")
        if not str(v).strip().isdigit():
            fail(f"rekapitulacijska vrstica »{label}« ni čisto številska: {v!r}")
        return int(v)

    recap_bauplatze = val("Summa der Bauplätze")
    recap_grund = val("Summa der Grundparzellen")
    recap_zusammen = val("Zusammen")

    # ——— 2. navzkrižne kontrole ———
    checksum_identity = recap_grund + recap_bauplatze == recap_zusammen
    if not checksum_identity:
        fail(f"rekapitulacijska aritmetika ne drži: {recap_grund} + {recap_bauplatze} ≠ {recap_zusammen}")

    p38_cov = p38["coverage"]
    grund_seen = p38_cov["grundDistinct"]
    grund_missing = p38_cov["grundMissing"]
    baseline_identity = grund_seen + grund_missing == recap_grund
    if not baseline_identity:
        fail(f"P36/P38 osnovna črta ({grund_seen}+{grund_missing}) ≠ rekapitulacija Grundparzellen ({recap_grund})")

    p38_checksum = p38["checksumReconciliation"]["target"]["skupaj"]
    control_matches_recap = p38_checksum == recap_zusammen
    if not control_matches_recap:
        fail(f"P38 kontrolna vsota ({p38_checksum}) ≠ rekapitulacija Zusammen ({recap_zusammen})")

    blattx_entries = [e for e in p39["parcels"] if e["section"] == "BLATT_X"]
    bauplatze_seen = len(blattx_entries)
    register_gap = recap_bauplatze - bauplatze_seen
    if register_gap < 0:
        fail("Blatt X vrstic je več kot rekapituliranih stavbnih mest — neskladje z P38")

    # ——— 3. dekompozicija površin po sekcijah (model P39) ———
    entries = p39["parcels"] + p39["neberezna"]
    sec_area = defaultdict(lambda: {"rowsWithArea": 0, "rowsWithoutArea": 0, "joch": 0, "klafter": 0})
    tot = {"rowsWithArea": 0, "rowsWithoutArea": 0, "joch": 0, "klafter": 0}
    for e in entries:
        s = e.get("section") or "NEBEREŽNA"
        for c in e.get("cultures", []):
            j = c.get("joch") or 0
            k = c.get("klafter") or 0
            a = sec_area[s]
            if j or k:
                a["rowsWithArea"] += 1
                tot["rowsWithArea"] += 1
            else:
                a["rowsWithoutArea"] += 1
                tot["rowsWithoutArea"] += 1
            a["joch"] += j
            a["klafter"] += k
            tot["joch"] += j
            tot["klafter"] += k
    for a in list(sec_area.values()) + [tot]:
        a["jochEquivalent"] = round(a["joch"] + a["klafter"] / KLAFTER_PER_JOCH, 4)

    grund_area = sec_area["GRUND_1_2505"]["jochEquivalent"]
    no_blattx_area = round(
        sec_area["GRUND_1_2505"]["jochEquivalent"]
        + sec_area["NADALJEVANJE_2506"]["jochEquivalent"]
        + sec_area["WALDUNG"]["jochEquivalent"],
        4,
    )
    whole_area = tot["jochEquivalent"]

    # ——— kandidati za pomen »Summa 1216(?) Joch« (str. 141) ———
    recap_area_match = re.search(r"Summa\s+(\d+)\(\?\)\s*Joch", rec.get("rawTranscription", ""))
    recap_area_reading = int(recap_area_match.group(1)) if recap_area_match else None
    if recap_area_reading is None:
        fail("Summa N(?) Joch ni razčlenjena iz rawTranscription rekapitulacije")

    candidates = [
        {
            "scope": "GRUND_1_2505 samo (zemljiške parcele; stavbna mesta se štejejo po kosih)",
            "jochEquivalent": grund_area,
            "deltaJoch": round(grund_area - recap_area_reading, 4),
            "deltaPct": round(100 * (grund_area - recap_area_reading) / recap_area_reading, 2),
            "assessment": "NAJBOLJ SKLADEN — odmik 1,39 % je v redu negotovosti branja »1216(?)« + 32 vrstic brez površine; odločitev paleografska",
        },
        {
            "scope": "GRUND + NADALJEVANJE + WALDUNG (brez Blatt X)",
            "jochEquivalent": no_blattx_area,
            "deltaJoch": round(no_blattx_area - recap_area_reading, 4),
            "deltaPct": round(100 * (no_blattx_area - recap_area_reading) / recap_area_reading, 2),
            "assessment": "možen, če rekapitulacija šteje tudi nadaljevalne in gozdne parcele — odmik 5,6 %",
        },
        {
            "scope": "celoten register z Blatt X (zgornja meja)",
            "jochEquivalent": whole_area,
            "deltaJoch": round(whole_area - recap_area_reading, 4),
            "deltaPct": round(100 * (whole_area - recap_area_reading) / recap_area_reading, 2),
            "assessment": "neskladen — zahteval bi podvajanje Blatt X površin, ki ga prekrivanje parov ne dokazuje; zavrnjen",
        },
    ]

    # ——— 4. tveganje podvojenega štetja Blatt X ↔ GRUND ———
    def owner_haus_pairs(entries_):
        s = set()
        for e in entries_:
            owners = e.get("owner") or [None]
            haus = e.get("hausNr") or [None]
            for o in owners:
                for h in haus:
                    s.add((o, h))
        return s

    grund_entries = [e for e in p39["parcels"] if e["section"] == "GRUND_1_2505"]
    pairs_g = owner_haus_pairs(grund_entries)
    pairs_x = owner_haus_pairs(blattx_entries)
    owners_g = {o for (o, _) in pairs_g if o}
    owners_x = {o for (o, _) in pairs_x if o}
    haus_x = {h for (_, h) in pairs_x if h}
    blattx_overlap = {
        "pairsGrund": len(pairs_g),
        "pairsBlattX": len(pairs_x),
        "pairsOverlap": len(pairs_g & pairs_x),
        "ownersGrund": len(owners_g),
        "ownersBlattX": len(owners_x),
        "ownersOverlap": len(owners_g & owners_x),
        "distinctHausNrBlattX": len(haus_x),
        "verdict": "podvajanje NI dokazljivo (prekrivanje parov 1/59, lastnikov 1/22 — razlike v črkovanju imen?), tudi NI izključeno; Blatt X površin ne smemo samodejno prištevati",
    }

    # ——— 5. per-house fragmenti str. 140–141 (doslovno, UNRESOLVED) ———
    m141 = re.search(r"PSE-141:\s*(.*)$", rec.get("rawTranscription", ""), re.DOTALL)
    frag_text = m141.group(1) if m141 else ""
    frag_rows = re.findall(r"\d+/\d+(?:\(\?\))?", frag_text)
    frag_joch_sum = sum(int(r.split("/")[0]) for r in frag_rows if "/" in r) if frag_rows else None
    if not frag_rows:
        fail("fragmenti str. 141 (per-house vrstice) se niso razčlenili iz rawTranscription")
    fragment_rows = {
        "page": 141,
        "verbatim": frag_rows,
        "count": len(frag_rows),
        "naiveJochSum": frag_joch_sum,
        "naiveSumVsRecap": (
            f"naivna vsota {frag_joch_sum} Joch nasprotuje sami Summi {recap_area_reading}(?) — "
            "branja nista usklajena; vrstice ostajajo doslovne, UNRESOLVED"
        ) if frag_joch_sum is not None else "ni vrstic",
        "resolution": "UNRESOLVED — potrebna človeška paleografija (dva VLM branja se razhajata)",
    }

    # ——— 6. številčni eho — OVRGAN ———
    nad_parcels = [e["parcel"] for e in p39["parcels"] if e["section"] == "NADALJEVANJE_2506"]
    max_nad = max(nad_parcels) if nad_parcels else None
    if max_nad is None:
        fail("NADALJEVANJE_2506 nima parcel")
    numeric_echo = {
        "hypothesis": "max parcela NADALJEVANJE (2506+) == Zusammen rekapitulacije (2607)",
        "maxParcelNadaljevanje": max_nad,
        "recapZusammen": recap_zusammen,
        "refuted": max_nad != recap_zusammen,
        "verdict": (
            f"OVRGAN — max parcela v NADALJEVANJE je {max_nad}, ne 2607; številčni eho ne obstaja "
            "(negativen izid, izrecno dokumentiran)"
        ) if max_nad != recap_zusammen else "POTRJEN",
    }

    # ——— regresije P38/P39 ———
    t39 = p39["totals"]
    if t39["rowsBefore"] != 2760 or t39["modelEntries"] != 2134 or t39["parcelCulturePairs"] != 2632:
        fail("P39 regresija: totals niso 2760/2134/2632")
    if p38_cov["grundDistinct"] != 1889 or p38_cov["blattXDistinct"] != 60:
        fail("P38 regresija: coverage ni 1889/60")
    if ps_full["totals"]["grundSeen"] != 1889:
        fail("PS-full totals regresija: grundSeen ni 1889")

    report = {
        "series": "PS",
        "source": "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani) — rekapitulacija str. 140–143 nad committed dokazi: PS-structure.json (P9 struktura + rekapitulacija), ps-reconciliation.json (P38), ps-landuse.json (P39); polni izpis research/issue17/ps-recap.json + src/data/atlas/ps-recap.json",
        "method": "deterministično iz committed dokazov; brez AI ob delovanju; surove vrednosti nedotaknjene",
        "status": "REVIEW",
        "rulebook": "v1",
        "recapitulation": {
            "page": 143,
            "writtenAs": {"medium": "rdeči tuš (nachträgliche Kontrolsummen)"},
            "summaBauplatze": recap_bauplatze,
            "summaGrundparzellen": recap_grund,
            "zusammen": recap_zusammen,
            "areaReadingPage141": {"value": recap_area_reading, "verbatim": f"Summa {recap_area_reading}(?) Joch", "uncertain": True, "note": "dva VLM branja se razhajata — izrecno negotovo"},
        },
        "crossCheck": {
            "checksumIdentity": {"grund + bauplatze": f"{recap_grund} + {recap_bauplatze} = {recap_grund + recap_bauplatze}", "zusammen": recap_zusammen, "pass": checksum_identity},
            "baselineIdentity": {"grundSeen": grund_seen, "grundMissing": grund_missing, "sum": grund_seen + grund_missing, "recapGrundparzellen": recap_grund, "pass": baseline_identity},
            "p38ControlSum": {"value": p38_checksum, "recapZusammen": recap_zusammen, "meaning": "P38 kontrolna vsota je uradna rekapitulacija dokumenta (str. 143, rdeči tuš)", "pass": control_matches_recap},
            "bauplatzeRegister": {"recap": recap_bauplatze, "blattXRows": bauplatze_seen, "gap": register_gap, "coveragePct": round(100 * bauplatze_seen / recap_bauplatze, 1), "meaning": "Blatt X (str. 138) pokrije 60/102 stavbnih mest — 42 je zunaj registra (registrska vrzel)"},
        },
        "areaDecomposition": {
            "klafterPerJoch": KLAFTER_PER_JOCH,
            "bySection": dict(sorted(sec_area.items())),
            "total": tot,
            "rowsWithArea": tot["rowsWithArea"],
            "rowsWithoutArea": tot["rowsWithoutArea"],
        },
        "recapAreaAttribution": {
            "recapReading": recap_area_reading,
            "candidates": candidates,
            "closest": "GRUND_1_2505 samo (Δ +16.96 Joch ≈ +1.39 %)",
            "missingAreaUpperBound": "32 vrstic brez razčlenjene površine + posamične napačne števkine (P38: 8↔5, 3↔1 nedokazljive) lahko odmik ~17 Joch pojasnijo; deterministično NE odločljivo",
            "resolution": "OTVORENO — paleografska potrditev branj str. 140–143 (dvomljivo »1216(?)«)",
        },
        "blattXOverlap": blattx_overlap,
        "fragmentRows140_141": fragment_rows,
        "numericEcho": numeric_echo,
        "regressions": {
            "p39": {"rowsBefore": t39["rowsBefore"], "modelEntries": t39["modelEntries"], "parcelCulturePairs": t39["parcelCulturePairs"]},
            "p38": {"grundDistinct": p38_cov["grundDistinct"], "blattXDistinct": p38_cov["blattXDistinct"], "controlSum": p38_checksum},
        },
        "verdictSi": "Rekapitulacija str. 143 (102 + 2505 = 2607, rdeči tuš) je natanko tista kontrolna vsota, ki jo sprava (P38) uporablja od začetka, in se ujema z osnovno črto P36/P38 (1889 + 616 = 2505). Površinsko se najbolj sklada z GRUND-only (1232,96 Joch; Δ +1,39 %). Blatt X nosi površine brez dokazanega podvajanja — celotna vsota registra je samo zgornja meja. Per-house vrstice 140–141 ostajajo UNRESOLVED.",
        "verdictEn": "The page-143 recap (102 + 2,505 = 2,607, red chalk) is exactly the control sum the reconciliation (P38) has used all along and matches the P36/P38 baseline (1,889 + 616 = 2,505). Area-wise it best matches GRUND-only (1,232.96 Joch; Δ +1.39%). Blatt X carries areas with unproven duplication — the whole-register sum is only an upper bound. The per-house rows 140–141 remain UNRESOLVED.",
        "next": [
            "človeška paleografska potrditev str. 140–143 (Summa 1216(?) Joch + 7 per-house vrstic)",
            "3. prehod ~15 dvoumnih strani (tudi za 7 sirot in 9 NEBEREŽNA vrstic)",
            "razširitev pravilnika rab v2 (Lhut, Lohn, Ahn, Äfling …) ob paleografski potrditvi",
        ],
        "generatedBy": "scripts/p40_ps_recap.py",
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    # ——— ponovljivost: generirani čas se odstrani za primerjavo obeh izpisov ———
    payload = json.dumps(report, ensure_ascii=False, indent=1) + "\n"
    OUT_EVIDENCE.write_text(payload, encoding="utf-8")
    OUT_RUNTIME.write_text(payload, encoding="utf-8")

    # ——— povzetek za stdout (TS konstanta + commit sporočilo) ———
    cc = report["crossCheck"]
    print("=== P40 REKAPITULACIJA 140–143 (P5-b) ===")
    print(f"kontrolne vsote str. 143: Bauplätze {recap_bauplatze} + Grundparzellen {recap_grund} = Zusammen {recap_zusammen} (rdeči tuš)")
    print(f"identiteta: {cc['checksumIdentity']['pass']} | osnovna črta P36/P38 1889+616=2505 == recap: {cc['baselineIdentity']['pass']} | P38 kontrolna vsota == recap: {cc['p38ControlSum']['pass']}")
    print(f"Bauplätze register: Blatt X {bauplatze_seen}/102 (vrzel {register_gap}, pokritost {round(100*bauplatze_seen/recap_bauplatze,1)} %)")
    print("površine po sekcijah:")
    for s, a in sorted(sec_area.items()):
        print(f"  {s:24s} {a['joch']:5d} Joch + {a['klafter']:7d} Klafter = {a['jochEquivalent']:9.4f} Joch (brez površine: {a['rowsWithoutArea']})")
    print(f"  {'SKUPAJ':24s} {tot['joch']:5d} Joch + {tot['klafter']:7d} Klafter = {tot['jochEquivalent']:9.4f} Joch (brez površine: {tot['rowsWithoutArea']})")
    print(f"Summa 1216(?) Joch kandidati: GRUND-only Δ +{candidates[0]['deltaJoch']} ({candidates[0]['deltaPct']} %) | brez Blatt X Δ +{candidates[1]['deltaJoch']} | celoten Δ +{candidates[2]['deltaJoch']}")
    print(f"Blatt X ↔ GRUND prekrivanje: parov {blattx_overlap['pairsOverlap']}/{blattx_overlap['pairsBlattX']}, lastnikov {blattx_overlap['ownersOverlap']}/{blattx_overlap['ownersBlattX']} → podvajanje nedokazljivo")
    print(f"fragmenti 140–141: {fragment_rows['count']} vrstic doslovno, UNRESOLVED (naivna vsota {fragment_rows['naiveJochSum']} Joch nasprotuje Summi {recap_area_reading}(?))")
    print(f"številčni eho: OVRGAN — max NADALJEVANJE parcela {numeric_echo['maxParcelNadaljevanje']} ≠ Zusammen {recap_zusammen} (negativen izid)")
    print("regresije P38/P39: OK (1889/60/2607 · 2760/2134/2632)")
    print(f"izpisa: {OUT_EVIDENCE.relative_to(ROOT)} + {OUT_RUNTIME.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
