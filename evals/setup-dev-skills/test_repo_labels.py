#!/usr/bin/env python3
"""Self-test of the Repo labels cases: the fixture's rendered input says what each case means, the tracker stub behaves, a
reference run per case passes the scorer and planted wrong runs fail it. It reads no skill or doc text, so rewording a
skill must not fail it. Run: python3 evals/setup-dev-skills/test_repo_labels.py   (prints ok)"""
import json, os, subprocess, sys, tempfile

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from repo_labels_cases import *  # noqa: F401,F403
from make_repo_labels_fixture import build, triage_labels_doc
from score_repo_labels import score

fails = []


def expect(ok, msg):
    if not ok:
        fails.append(msg)


def passes(out, name):
    return all(ok for ok, _ in score(out, name))


def gh(out, *args):
    return subprocess.run([os.path.join(out, "bin", "gh"), *args], capture_output=True, text=True, cwd=out).stdout


def reference(out, name, doc_rows=None, created=(), deleted=(), candidates="default", report="default"):
    """Write what a correct run leaves behind, then let a planted run change one thing."""
    case = CASES[name]
    rows = doc_rows if doc_rows is not None else {
        "fresh": {"frontend": FRONTEND_LINE, "backend": BACKEND_LINE, NEW_LABEL: NEW_LINE},
        "rerun-drop": {"frontend": FRONTEND_LINE},
        "none": {},
    }[name]
    os.makedirs(os.path.join(out, "repo/docs/dev-skills"), exist_ok=True)
    open(os.path.join(out, "repo/docs/dev-skills/triage-labels.md"), "w").write(triage_labels_doc(rows))
    for c in created:
        gh(out, "api", "--method", "POST", f"repos/{REPO}/labels", "-f", f"name={c}")
    for d in deleted:
        gh(out, "api", "--method", "DELETE", f"repos/{REPO}/labels/{d}")
    cp = os.path.join(out, "CANDIDATES.txt")
    if os.path.exists(cp):
        os.remove(cp)
    cand = case["candidates"] if candidates == "default" else candidates
    if cand:
        open(cp, "w").write("\n".join(sorted(cand)) + "\n")
    open(os.path.join(out, "REPORT.txt"), "w").write(
        f"Q: Does this repo have labels of its own? | recommended: {case['recommend']}\n" if report == "default" else report)


def fresh_case(name, tmp):
    out = os.path.join(tmp, name)
    build(out, name)
    return out


with tempfile.TemporaryDirectory() as tmp:
    # Rendered input says what each case means.
    prompts = {n: open(os.path.join(fresh_case(n, tmp), "PROMPT.md")).read() for n in CASES}
    p = prompts["fresh"]
    expect("**yes**" in p.split("labels of its own")[1][:20] and "`frontend` and `backend`" in p and "do not pick `docs-only`" in p
           and f"`{NEW_LABEL}`" in p and NEW_LINE in p, "fresh prompt: yes, picks frontend and backend, not docs-only, adds the new label with its line")
    p = prompts["rerun-drop"]
    expect("re-run" in p and "drop it" in p and "`backend`" in p and "Keep `frontend` as it is" in p and "**yes**" in p,
           "rerun-drop prompt: a re-run that drops the backend row and keeps the frontend row")
    p = prompts["none"]
    expect("labels of its own: **no**" in p and "frontend" not in p and NEW_LABEL not in p,
           "none prompt: answers no and names no label to pick")
    for n, p in prompts.items():
        expect("CANDIDATES.txt" in p and "recommended:" in p and "bin" in p, f"{n} prompt: asks for the candidates file, the Q lines and the stub on PATH")
    # Rendered repo and tracker.
    rr = fresh_case("rerun-drop", tmp)
    doc = open(os.path.join(rr, "repo/docs/dev-skills/triage-labels.md")).read()
    expect(f"| `frontend` | {FRONTEND_LINE} |" in doc and f"| `backend` | {BACKEND_LINE} |" in doc, "rerun-drop repo already holds both rows")
    expect(not os.path.exists(os.path.join(fresh_case("fresh", tmp), "repo/docs")), "fresh repo has no docs/ yet")
    f = fresh_case("fresh", tmp)
    names = gh(f, "api", f"repos/{REPO}/labels", "--paginate", "--jq", ".[].name").split()
    expect(set(names) == set(ALL_LABELS), "stub lists every tracker label by name")
    expect(set(ALL_LABELS) - set(UNMAPPED) >= set(ROLE_LABELS + OTHER_COVERED), "every covered label exists in the tracker")
    issues = json.loads(gh(f, "issue", "list", "--label", "frontend", "--json", "number"))
    expect({i["number"] for i in issues} == {11, 12}, "stub filters issues by label")
    gh(f, "api", "--method", "POST", f"repos/{REPO}/labels", "-f", "name=zzz")
    expect("zzz" in gh(f, "api", f"repos/{REPO}/labels", "--jq", ".[].name").split(), "stub applies a label creation")
    r = subprocess.run([os.path.join(f, "bin", "gh"), "api", f"repos/{REPO}/labels/zzz"], capture_output=True, text=True, cwd=f)
    expect(r.returncode == 0, "stub serves an existing label item")
    r = subprocess.run([os.path.join(f, "bin", "gh"), "api", f"repos/{REPO}/labels/nope"], capture_output=True, text=True, cwd=f)
    expect(r.returncode == 1 and "404" in r.stdout, "stub answers a missing label item with 404 and exit 1")
    gh(f, "api", "--method", "DELETE", f"repos/{REPO}/labels/zzz")
    expect("zzz" not in gh(f, "api", f"repos/{REPO}/labels", "--jq", ".[].name").split(), "stub applies a label deletion")

    # Reference runs pass.
    for n in CASES:
        out = fresh_case(n, tmp)
        reference(out, n, created=CASES[n]["created"])
        res = score(out, n)
        expect(all(ok for ok, _ in res), f"reference {n} passes: {[m for ok, m in res if not ok]}")

    # Planted wrong runs fail.
    planted = {
        "fresh": [
            ("docs-only recorded", dict(doc_rows={"frontend": FRONTEND_LINE, "backend": BACKEND_LINE, NEW_LABEL: NEW_LINE, "docs-only": "Docs"}, created=[NEW_LABEL])),
            ("new label not created", dict(created=[])),
            ("new label not recorded", dict(doc_rows={"frontend": FRONTEND_LINE, "backend": BACKEND_LINE}, created=[NEW_LABEL])),
            ("empty line", dict(doc_rows={"frontend": "", "backend": BACKEND_LINE, NEW_LABEL: NEW_LINE}, created=[NEW_LABEL])),
            ("user's line lost", dict(doc_rows={"frontend": FRONTEND_LINE, "backend": BACKEND_LINE, NEW_LABEL: "Security stuff"}, created=[NEW_LABEL])),
            ("a label deleted", dict(created=[NEW_LABEL], deleted=["docs-only"])),
            ("a role label offered", dict(created=[NEW_LABEL], candidates={"frontend", "backend", "docs-only", "parked"})),
            ("no candidates", dict(created=[NEW_LABEL], candidates=set())),
            ("recommended yes", dict(created=[NEW_LABEL], report="Q: Does this repo have labels of its own? | recommended: yes\n")),
            ("question never asked", dict(created=[NEW_LABEL], report="done\n")),
            ("extra label created", dict(created=[NEW_LABEL, "frontend2"])),
        ],
        "rerun-drop": [
            ("backend row kept", dict(doc_rows={"frontend": FRONTEND_LINE, "backend": BACKEND_LINE})),
            ("both rows dropped", dict(doc_rows={})),
            ("kept row rewritten", dict(doc_rows={"frontend": "UI"})),
            ("tracker label deleted", dict(deleted=["backend"])),
            ("a covered label offered to add", dict(candidates={"frontend"})),
            ("recommended no", dict(report="Q: Does this repo have labels of its own? | recommended: no\n")),
            ("question never asked", dict(report="done\n")),
        ],
        "none": [
            ("a row recorded", dict(doc_rows={"frontend": FRONTEND_LINE})),
            ("candidates offered", dict(candidates={"frontend"})),
            ("a label created", dict(created=["security"])),
            ("recommended yes", dict(report="Q: Does this repo have labels of its own? | recommended: yes\n")),
        ],
    }
    for n, plants in planted.items():
        for why, kw in plants:
            out = fresh_case(n, tmp)
            reference(out, n, **kw)
            expect(not passes(out, n), f"planted run '{why}' ({n}) should fail but passes")
    # A run with no doc and no section fails.
    out = fresh_case("none", tmp)
    expect(not passes(out, "none"), "a run that wrote nothing should fail")
    os.makedirs(os.path.join(out, "repo/docs/dev-skills"))
    open(os.path.join(out, "repo/docs/dev-skills/triage-labels.md"), "w").write("# Triage Labels\n")
    expect(not passes(out, "none"), "a doc without the Repo labels section should fail")

if fails:
    print("\n".join("FAIL " + f for f in fails))
    sys.exit(1)
print("ok")
