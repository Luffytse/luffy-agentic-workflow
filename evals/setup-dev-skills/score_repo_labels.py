#!/usr/bin/env python3
"""Score one Repo labels run of the setup-dev-skills eval from its outcomes: the rows in the written triage-labels doc, the
labels the tracker stub saw created or deleted, the candidates file and the questions the reply logged. Never reads wording.
Usage: python3 score_repo_labels.py <out-dir> <fresh|rerun-drop|none>   (exit 1 on any FAIL)
The run's final reply is saved by hand to <out-dir>/REPORT.txt."""
import json, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from repo_labels_cases import *  # noqa: F401,F403


def read(p):
    try:
        return open(p).read()
    except OSError:
        return None


def repo_label_rows(doc):
    """{label: line} from the table under `## Repo labels`; None when the section is missing."""
    m = re.search(r"^##\s+Repo labels\s*$(.*?)(?=^##\s|\Z)", doc, re.M | re.S)
    if not m:
        return None
    rows = {}
    for ln in m.group(1).splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")] if ln.strip().startswith("|") else []
        if len(cells) < 2 or set(cells[0]) <= set("-: ") or cells[0].lower().startswith("label"):
            continue
        rows[cells[0].strip("`")] = cells[1]
    return rows


def gh_calls(out):
    """(created, deleted) label names from the stub's log."""
    created, deleted = set(), set()
    for ln in (read(os.path.join(out, "gh.log")) or "").splitlines():
        a = json.loads(ln)
        joined = " ".join(a)
        method = next((a[i + 1].upper() for i, x in enumerate(a[:-1]) if x in ("--method", "-X")), "GET")
        if a[:2] == ["label", "create"] and len(a) > 2:
            created.add(a[2])
        elif a[:2] == ["label", "delete"] and len(a) > 2:
            deleted.add(a[2])
        elif method == "POST" and re.search(r"/labels(\s|$)", joined + " "):
            for i, x in enumerate(a[:-1]):
                if x in ("-f", "-F", "--field", "--raw-field") and a[i + 1].startswith("name="):
                    created.add(a[i + 1][5:])
        elif method == "DELETE" and "/labels" in joined:
            deleted.add(a[-1].rsplit("/", 1)[-1])
    return created, deleted


def score(out, name):
    case, results = CASES[name], []
    def check(ok, msg):
        results.append((bool(ok), msg))
    doc = read(os.path.join(out, "repo/docs/dev-skills/triage-labels.md"))
    check(doc is not None, "docs/dev-skills/triage-labels.md was written")
    rows = repo_label_rows(doc) if doc else None
    check(rows is not None, "the doc has a `## Repo labels` section with a table")
    if doc:
        check(all(f"`{r}`" in doc for r in ROLE_LABELS), "the role tables still carry every role")
    if rows is not None:
        check(set(rows) == case["rows"], f"rows are exactly {sorted(case['rows'])}, got {sorted(rows)}")
        check(all(len(v) >= 4 and "<" not in v for v in rows.values()), "every row has a filled-in line")
        if name == "fresh":
            check("authentication" in rows.get(NEW_LABEL, "").lower(), "the new label's row keeps the user's line")
        if name == "rerun-drop":
            check(rows.get("frontend") == FRONTEND_LINE, "the kept row's line is unchanged")
    created, deleted = gh_calls(out)
    check(created == case["created"], f"labels created are exactly {sorted(case['created'])}, got {sorted(created)}")
    check(not deleted, f"no tracker label deleted, got {sorted(deleted)}")
    try:
        final = {l["name"] for l in json.load(open(os.path.join(out, "gh-state.json")))["labels"]}
    except (OSError, ValueError):
        final = set()
    check(set(ALL_LABELS) <= final, "every label the tracker started with is still there")
    check(case["created"] <= final, "a label the user added is in the tracker")
    cand = read(os.path.join(out, "CANDIDATES.txt"))
    offered = {l.strip().strip("`") for l in (cand or "").splitlines() if l.strip()}
    if name == "rerun-drop":
        check(offered <= {"docs-only", "backend"}, f"a label offered to add is one no row covers, got {sorted(offered)}")
    else:
        check(offered == case["candidates"], f"candidates offered are exactly {sorted(case['candidates'])}, got {sorted(offered)}")
    rep = read(os.path.join(out, "REPORT.txt")) or ""
    qs = [m for m in re.finditer(r"^Q:\s*(.*?)\|\s*recommended:\s*(.*)$", rep, re.M | re.I)
          if re.search(r"label", m.group(1), re.I) and re.search(r"\bown\b", m.group(1), re.I)]
    check(qs, "the reply logs a question about labels of the repo's own")
    check(qs and re.match(r"\W*" + case["recommend"] + r"\b", qs[0].group(2), re.I),
          f"that question's recommended answer is {case['recommend']}")
    return results


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit(__doc__)
    res = score(os.path.abspath(sys.argv[1]), sys.argv[2])
    for ok, msg in res:
        print(("PASS " if ok else "FAIL ") + msg)
    sys.exit(0 if all(ok for ok, _ in res) else 1)
