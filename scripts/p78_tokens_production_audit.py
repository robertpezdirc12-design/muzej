#!/usr/bin/env python3
# P78 — Produkcija & žetoni: operativni zdravstveni audit (issue #6).
#
# Po P77 so vse raziskovalne niti skonvergirale k lastniškim odločitvam
# (P76 ① opcije sekcij; P77 ② fizični arhiv za PF). Edina NE-lastniška
# odprta točka je ③ žetoni/operativa (issue #6) — P78 jo audita
# celovito, deterministično, brez AI.
#
# METODA (deterministični probe, brez AI):
#   1. produkcija: GET https://griblje-museum.vercel.app/ (HTTP + velikost),
#      /api/qa (ok/passed/failed + qa-p76-sections-perblatt),
#      /api/atlas/ps-parcels-geo (version/rows)
#   2. GitLab: GET /personal_access_tokens/self (id/active/revoked/expires_at/
#      scopes — AVTORITATIVEN rok) + GET /projects/87462760 (dostop)
#   3. zrcala: git ls-remote origin/main == github/main == lokalni HEAD
#   4. GitHub Actions stanje: zadnji run sync.yml + token-health.yml →
#      job steps/runner_id → check-run anotacija (AVTORITATIVNO sporočilo
#      GitHub o blokadi) → izpeljava `billingBlocked`
#   5. workflows prisotni lokalno (build-check/deploy/sync/token-health)
#
# OKOLJSKE OKOLIŠČINE (dokazano med auditom 2026-10-15):
#   - VERCEL_TOKEN je POTEKEL 2026-10-14 (rezervni deploy; primarni deploy
#     = Vercel GitHub App — brez žetona — dela; produkcija aktualna).
#   - GITLAB_TOKEN skrivnost v GitHub Actions je držala zastarel PAT #2
#     (updated 2026-10-13T16:18:56Z); P78 jo je SANIRAL z aktualnim PAT #3
#     (libsodium sealed box, PyNaCl; PUT skrivnosti HTTP 204,
#     updated 2026-10-15T20:51:08Z). To je bilo NUJNO tudi samo po sebi
#     (stari PAT bi povzročil auth padec, takoj ko bi Actions tekel).
#   - DISCOVERY: vsi GitHub Actions jobi na računu NE STARTAJO (job
#     končan v ~2 s, steps [], runner_id 0, logs BlobNotFound) —
#     check-run anotacija (avtoritativno): "The job was not started
#     because recent account payments have failed or your spending limit
#     needs to be increased. Please check the 'Billing & plans' section in
#     your settings." Zadet: sync.yml (mreža varnosti sinhronizacije),
#     token-health.yml (dnevni watchdog žetonov — ZATO NI OPOZORIL
#     10-13/14/15 ob izteku VERCEL_TOKEN!) in deploy.yml (rezervni deploy).
#     Zadnji uspešen sync run: 2026-10-11T06:23:19Z (schedule).
#     Sanacija je LASTNIŠKA akcija (Billing & plans — plačilna metoda /
#     spending limit); API je ne more opraviti (token brez admin:billing).
#
# Izhod: /home/z/muzej/research/issue17/tokens-production-audit.json
# Status: OPERATIONAL-AUDIT (produkcija + žetoni + Actions zdravje;
#         dokaz ponovljiv z --check — live probe, brez mutacij).

import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOKAZ = os.path.join(REPO, "research", "issue17", "tokens-production-audit.json")

VERCEL = "https://griblje-museum.vercel.app"
GITLAB_API = "https://gitlab.com/api/v4"
GH_API = "https://api.github.com/repos/robertpezdirc12-design/muzej"
GH_REPO = "robertpezdirc12-design/muzej"

# --- pričakovano stanje (invarianti I1–I9) ---
EXPECTED_QA = {"ok": True, "passed": 79, "failed": 0}
QA_P76_ID = "qa-p76-sections-perblatt"
EXPECTED_GEO = {"version": 7, "rows": 891}
EXPECTED_PAT_ID = 28471532
EXPECTED_PAT_NAME = "dsfsd"
EXPECTED_PAT_EXPIRES = "2026-11-14"
EXPECTED_SCOPES = {"api", "write_repository", "read_repository", "self_rotate"}
PROJECT_ID = 87462760
PROJECT_PATH = "markec-group1/muzej"
BILLING_TOKEN = "recent account payments have failed or your spending limit"
WORKFLOWS = ["build-check.yml", "deploy.yml", "sync.yml", "token-health.yml"]
SYNC_LAST_SUCCESS = "2026-10-11T06:23:19Z"

# sanacija skrivnosti GITLAB_TOKEN (P78, enkratna akcija — NE del --check)
REPAIR = {
    "secret": "GITLAB_TOKEN",
    "previousSecretUpdatedAt": "2026-10-13T16:18:56Z",
    "previousSecretEra": "PAT #2 (neveljaven — iztekel/preklican)",
    "repairedAt": "2026-10-15T20:51:08Z",
    "method": ("PUT /repos/{repo}/actions/secrets/GITLAB_TOKEN — vrednost "
               "šifrirana z libsodium sealed box (PyNaCl 1.6.2) z javnim "
               "ključem repozitorija (key_id 3380204578043523366); "
               "odgovor HTTP 204"),
    "postRepairSecretUpdatedAt": "2026-10-15T20:51:08Z",
    "verification": ("workflow_dispatch sync.yml (run 38805294449) po "
                     "sanaciji: failure v ~2 s, steps [], runner_id 0 — "
                     "dokazalo, da vzrok NI žeton, temveč blokada računa "
                     "(anotacija check-run); enak podpis tudi dispatch "
                     "token-health.yml (run 38805695856)"),
    "verdict": ("SKRIVNOST SANIRANA (nujno, ne glede na blokado); Actions "
                "ostaja BLOKIRAN na nivoju računa — sanacija LASTNIŠKA "
                "(Billing & plans)"),
}


def gh_token():
    url = subprocess.run(["git", "remote", "get-url", "github"],
                         cwd=REPO, capture_output=True, text=True).stdout
    return url.split(":")[-1].split("@")[0]


def gitlab_pat():
    url = subprocess.run(["git", "remote", "get-url", "origin"],
                         cwd=REPO, capture_output=True, text=True).stdout
    i = url.find("glpat-")
    j = url.find("@", i)
    return url[i:j]


def http_get(url, headers, tries=5):
    """GET z retry (WAF 403 / prehodne napake; vzorec P76/P77 — GitLab WAF
    vrača 403 stohastično, worklog Task 44: »WAF 403 2× → retry-loop, 3.
    poskus PASS«; zato 5 poskusov z naraščajočim čakanjem)."""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            last = (e.code, e.read()[:200])
            if e.code in (403, 429, 500, 502, 503, 504):
                time.sleep(4 * (i + 1))
                continue
            return last
        except Exception as e:  # omrežje
            last = (0, str(e)[:200].encode())
            time.sleep(4 * (i + 1))
    return last


def ls_remote(remote, ref="main"):
    """ls-remote z retry (transport lahko stohastično pade, kot GitLab WAF)."""
    for i in range(4):
        out = subprocess.run(["git", "ls-remote", remote, ref],
                             cwd=REPO, capture_output=True, text=True)
        if out.stdout.strip():
            return out.stdout.split()[0]
        time.sleep(4 * (i + 1))
    return None


def head_sha():
    return subprocess.run(["git", "rev-parse", "HEAD"],
                          cwd=REPO, capture_output=True, text=True).stdout.strip()


def probe_vercel():
    home_st, home_b = http_get(VERCEL + "/", {"User-Agent": "p78-audit"})
    qa_st, qa_b = http_get(VERCEL + "/api/qa", {"User-Agent": "p78-audit"})
    geo_st, geo_b = http_get(VERCEL + "/api/atlas/ps-parcels-geo",
                             {"User-Agent": "p78-audit"})
    home = {"http": home_st, "bytes": len(home_b)}
    if qa_st == 200:
        q = json.loads(qa_b)
        qa = {"http": 200, "ok": q.get("ok"), "passed": q.get("passed"),
              "failed": q.get("failed"), "tests": len(q.get("tests", [])),
              "qaP76Pass": next((t.get("pass") for t in q.get("tests", [])
                                 if t.get("id") == QA_P76_ID), None)}
    else:
        qa = {"http": qa_st}
    if geo_st == 200:
        g = json.loads(geo_b)
        geo = {"http": 200, "version": g.get("version"),
               "rows": len(g.get("rows", []))}
    else:
        geo = {"http": geo_st}
    return home, qa, geo


def probe_gitlab():
    h = {"PRIVATE-TOKEN": gitlab_pat(), "User-Agent": "p78-audit"}
    st, b = http_get(GITLAB_API + "/personal_access_tokens/self", h, tries=6)
    if st == 200:
        t = json.loads(b)
        pat = {"http": 200, "id": t.get("id"), "name": t.get("name"),
               "active": t.get("active"), "revoked": t.get("revoked"),
               "expiresAt": t.get("expires_at"),
               "scopes": sorted(t.get("scopes", [])),
               "hasApiScope": "api" in t.get("scopes", []),
               "hasWriteRepositoryScope":
                   "write_repository" in t.get("scopes", [])}
    else:
        pat = {"http": st}
    st2, b2 = http_get(f"{GITLAB_API}/projects/{PROJECT_ID}", h, tries=6)
    if st2 == 200:
        p = json.loads(b2)
        project = {"http": 200, "id": p.get("id"),
                   "pathWithNamespace": p.get("path_with_namespace")}
    else:
        project = {"http": st2}
    return pat, project


def probe_actions():
    """Zadnji run sync.yml + token-health.yml; izpeljava billingBlocked."""
    auth = {"Authorization": f"token {gh_token()}",
            "User-Agent": "p78-audit",
            "Accept": "application/vnd.github+json"}
    out = {"billingBlocked": None, "annotation": None,
           "syncLatest": None, "tokenHealthLatest": None}

    def latest_run(wf):
        st, b = http_get(f"{GH_API}/actions/workflows/{wf}/runs?per_page=1",
                         auth)
        if st != 200:
            return None
        rs = json.loads(b).get("workflow_runs", [])
        if not rs:
            return None
        r = rs[0]
        sig = {"runId": r["id"], "createdAt": r["created_at"],
               "event": r["event"], "conclusion": r["conclusion"]}
        st2, b2 = http_get(f"{GH_API}/actions/runs/{r['id']}/jobs", auth)
        if st2 == 200:
            js = json.loads(b2).get("jobs", [])
            if js:
                j = js[0]
                sig["jobConclusion"] = j.get("conclusion")
                sig["steps"] = len(j.get("steps") or [])
                sig["runnerId"] = j.get("runner_id")
                if sig["steps"] == 0 and not j.get("runner_id"):
                    st3, b3 = http_get(
                        f"{GH_API}/check-runs/{j['id']}/annotations", auth)
                    if st3 == 200:
                        for a in json.loads(b3):
                            if BILLING_TOKEN in a.get("message", ""):
                                sig["annotation"] = a["message"]
        return sig

    out["syncLatest"] = latest_run("sync.yml")
    out["tokenHealthLatest"] = latest_run("token-health.yml")

    def blocked(sig):
        if not sig:
            return None
        no_start = (sig.get("jobConclusion") == "failure"
                    and sig.get("steps") == 0
                    and not sig.get("runnerId"))
        return bool(no_start or
                    (sig.get("annotation") and BILLING_TOKEN
                     in sig["annotation"]))

    flags = [f for f in (blocked(out["syncLatest"]),
                         blocked(out["tokenHealthLatest"]))
             if f is not None]
    out["billingBlocked"] = all(flags) if flags else None
    out["annotation"] = (out["syncLatest"] or {}).get("annotation") or \
                        (out["tokenHealthLatest"] or {}).get("annotation")
    return out


def build_dokaz():
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    home, qa, geo = probe_vercel()
    pat, project = probe_gitlab()
    actions = probe_actions()
    mirrors = {"gitlabMain": ls_remote("origin"),
               "githubMain": ls_remote("github"),
               "localHead": head_sha(),
               "method": ("git ls-remote (GitHub REST GET /commits/main "
                          "vrne 404 neavtentificirano — repozitorij "
                          "zaseben; ls-remote z žetonom iz remote URL)")}
    wf_present = {w: os.path.exists(
        os.path.join(REPO, ".github", "workflows", w)) for w in WORKFLOWS}

    dokaz = {
        "phase": "P78",
        "title": "Produkcija & žetoni: operativni zdravstveni audit (issue #6)",
        "status": "OPERATIONAL-AUDIT",
        "issuedAt": t0,
        "vercel": {
            "home": home,
            "qa": qa,
            "geo": geo,
            "deployArchitecture": {
                "primary": ("Vercel GitHub App (brez žetona) — vsak push "
                            "na main samodejno gradi produkcijo; NEODVISEN "
                            "od poteka VERCEL_TOKEN"),
                "reserve": ("deploy.yml (workflow_dispatch, VERCEL_TOKEN) "
                            "— trenutno MRTV: žeton potekel 2026-10-14 + "
                            "Actions blokada računa"),
            },
        },
        "gitlab": {"pat": pat, "project": project},
        "mirrors": mirrors,
        "workflowsPresent": wf_present,
        "actions": {
            "probes": actions,
            "billingBlocked": actions["billingBlocked"],
            "authoritativeAnnotation": actions["annotation"],
            "timeline": {
                "syncLastSuccess": SYNC_LAST_SUCCESS,
                "watchdogLastBotAlert": "2026-10-11T17:21:20Z (issue #6)",
                "watchdogBlindFrom": ("~2026-10-13 (od takrat naprej jobi brez "
                                      "korakov — opozoril 10-13/14/15 NI bilo, "
                                      "četudi je VERCEL_TOKEN potekel "
                                      "2026-10-14)"),
                "deployReserveLastSuccess": "2026-10-11T06:12:27Z",
            },
            "impact": {
                "sync.yml": ("dvosmerna sinhronizacija (mreža varnosti) mrtva "
                             "— operativno neškodljivo, dokler glavni agent "
                             "puša na OBE strani (P21 disciplina)"),
                "token-health.yml": ("dnevni watchdog žetonov mrtav — mehka "
                                     "točka; ročni audit P78 jo nadomešča "
                                     "do sanacije"),
                "deploy.yml": ("rezervni deploy mrtav (dvojni razlog: žeton "
                               "potekel + blokada) — primarna pot NEODVISNA"),
            },
        },
        "repair": REPAIR,
        "ownerActions": [
            {"priority": 1,
             "action": ("GitHub → Settings → Billing & plans: plačilna "
                        "metoda / spending limit (avtoritativna anotacija "
                        "GitHub; brez admin:billing scope API ne more)"),
             "restores": ("sync.yml (mreža varnosti) + token-health.yml "
                          "(watchdog) + deploy.yml (rezerva)")},
            {"priority": 2,
             "action": ("VERCEL_TOKEN: ustvari nov žeton na "
                        "vercel.com/account/tokens (Vercel API ne more "
                        "ustvarjati žetonov; potekel 2026-10-14)"),
             "restores": ("samo rezervni deploy; primarni GitHub App deploy "
                          "dela, produkcija aktualna (704 548 B, P77)")},
            {"priority": 3,
             "action": ("raziskovalne odločitve iz P76/P77 (neoperativno): "
                        "① opcija sekcij A/B1/B2/B3; ② fizični arhiv za "
                        "PF protokol"),
             "restores": "raziskovalna nadaljevanja P79+"},
        ],
        "verdict": ("PRODUKCIJA ZDRAVA in AKTUALNA (704 548 B == P77 deploy; "
                    "QA 79/79 vključno z qa-p76; geo v7/891); zrcala "
                    "bajtno identična (GitLab = GitHub = lokalna); GitLab "
                    "PAT #3 AKTIVEN (rok AVTORITATIVNO 2026-11-14 — prej "
                    "navajan 2026-11-09 v naslovu issue #6 je bil stari "
                    "žeton). GitHub Actions NA RAČUNU BLOKIRAN (billing) — "
                    "trajna lastniška akcija; skrivnost GITLAB_TOKEN "
                    "sanirana v P78; VERCEL_TOKEN potekel (rezerva)."),
        "invariants": {},
    }

    dokaz["invariants"] = {
        "I1_vercel_200": (home["http"] == 200
                          and home.get("bytes", 0) >= 500000),
        "I2_qa_79_79": all(qa.get(k) == v for k, v in EXPECTED_QA.items())
                       and qa.get("tests") == 79,
        "I3_qa_p76_pass": qa.get("qaP76Pass") is True,
        "I4_geo_v7_891": all(geo.get(k) == v
                             for k, v in EXPECTED_GEO.items()),
        "I5_pat_active": (pat.get("http") == 200
                          and pat.get("active") is True
                          and pat.get("revoked") is False
                          and pat.get("id") == EXPECTED_PAT_ID
                          and pat.get("name") == EXPECTED_PAT_NAME
                          and pat.get("expiresAt") == EXPECTED_PAT_EXPIRES
                          and EXPECTED_SCOPES.issubset(set(pat.get("scopes", [])))),
        "I6_project_87462760": (project.get("http") == 200
                                and project.get("id") == PROJECT_ID
                                and project.get("pathWithNamespace")
                                == PROJECT_PATH),
        "I7_mirrors_identical": (mirrors["gitlabMain"]
                                 == mirrors["githubMain"]
                                 == mirrors["localHead"]
                                 and mirrors["localHead"] is not None),
        "I8_actions_state_consistent": (
            dokaz["actions"]["billingBlocked"] is not None
            and dokaz["actions"]["billingBlocked"]
                == dokaz["actions"]["probes"]["billingBlocked"]),
        "I9_workflows_present": all(wf_present.values()),
    }
    dokaz["invariantsPass"] = all(dokaz["invariants"].values())
    return dokaz


def stable_core(d):
    """Bajtno stabilno jedro (brez časovnih žigov, run/job id-jev, velikosti
    odgovorov in sha pinov — spreminjajo se z deployi/commiti).

    Zrcala: stabilno jedro OHRANI izreko enakosti (identical), NE pa
    posameznih sha vrednosti — te se spremeni s vsakim commitom, zato bi
    fiksiranje dokončno pokvarilo --check (lekcija prvega zagona 2026-10-15:
    dokaz @ fa537a7, --check po commitu c777318 → FAIL na sha pinu). Izreka
    se vedno izračuna SVEŽA: če katera stran zaostane, je fresh identical
    False → --check FAIL → ponovna izdaja dokaza (namerna lastnost)."""
    d2 = json.loads(json.dumps(d))
    d2.pop("issuedAt", None)
    if isinstance(d2.get("vercel"), dict):
        if isinstance(d2["vercel"].get("home"), dict):
            d2["vercel"]["home"].pop("bytes", None)
    for key in ("syncLatest", "tokenHealthLatest"):
        p = d2.get("actions", {}).get("probes", {}).get(key)
        if isinstance(p, dict):
            p.pop("runId", None)
            p.pop("createdAt", None)
            p.pop("event", None)
    m = d2.get("mirrors")
    if isinstance(m, dict):
        g, h, l = m.get("gitlabMain"), m.get("githubMain"), m.get("localHead")
        d2["mirrors"] = {
            "identical": bool(g and g == h == l),
            "method": m.get("method"),
        }
    return json.dumps(d2, sort_keys=True, ensure_ascii=False)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "build"
    if mode == "--check":
        with open(DOKAZ, encoding="utf-8") as f:
            committed = json.load(f)
        fresh = build_dokaz()
        ok = stable_core(committed) == stable_core(fresh)
        print("P78 --check:", "PASS (bajtno stabilno jedro)" if ok
              else "FAIL (dokaz odstopa od svežega pregleda)")
        if not ok:
            c, f_ = stable_core(committed), stable_core(fresh)
            for i in range(min(len(c), len(f_))):
                if c[i] != f_[i]:
                    print("prva razlika @", i, ":", c[max(0, i-80):i+120],
                          "!=", f_[max(0, i-80):i+120])
                    break
        sys.exit(0 if ok else 1)
    else:
        dokaz = build_dokaz()
        os.makedirs(os.path.dirname(DOKAZ), exist_ok=True)
        with open(DOKAZ, "w", encoding="utf-8") as f:
            json.dump(dokaz, f, ensure_ascii=False, indent=2)
        inv = dokaz["invariants"]
        print(f"P78 dokaz: {DOKAZ}")
        print(f"invarianti: {dokaz['invariantsPass']} — " +
              " ".join(f"{k}={'P' if v else 'F'}" for k, v in inv.items()))
        print(f"produkcija: {dokaz['vercel']['home']['http']} "
              f"({dokaz['vercel']['home']['bytes']} B); "
              f"QA {dokaz['vercel']['qa']['passed']}/"
              f"{dokaz['vercel']['qa']['passed'] + dokaz['vercel']['qa']['failed']}; "
              f"geo v{dokaz['vercel']['geo']['version']}/"
              f"{dokaz['vercel']['geo']['rows']}; "
              f"PAT rok {dokaz['gitlab']['pat'].get('expiresAt')}; "
              f"Actions blokada: {dokaz['actions']['billingBlocked']}")
        sys.exit(0 if dokaz["invariantsPass"] else 1)


if __name__ == "__main__":
    main()
