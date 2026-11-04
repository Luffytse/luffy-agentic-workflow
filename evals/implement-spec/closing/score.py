#!/usr/bin/env python3
"""Score an implement-spec closing run: <out-dir>/repo/.scratch/proposed-actions.md and report.md.

Usage: score.py <out-dir>
Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any fails. It reads what the run would
have done (the dry-run blocks, in order), never the skill's text: only the Spec and the landed Tickets close, after
the merge, and the dropped Ticket stays open and out of the pull request body.
"""
import json
import pathlib
import re
import subprocess
import sys

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent.parent / "merging"))
from make_fixture import tree_hash  # noqa: E402
from score import parse  # noqa: E402

CLOSE, STAY = {20, 21, 22}, {23}


def closed_numbers(blocks, after):
    return {int(m.group(0)) for i in after for m in [re.search(r"\d+", blocks[i]["issue"])] if m}


def score(out):
    out = pathlib.Path(out)
    repo = out / "repo"
    fx = json.loads((out / "fixture.json").read_text())
    actions = repo / ".scratch/proposed-actions.md"
    blocks = parse(actions.read_text()) if actions.exists() else []
    results = []

    def check(name, ok, seen=""):
        results.append(bool(ok))
        print(("PASS " if ok else "FAIL ") + name + ("" if ok or not seen else f": {seen}"))

    rev = lambda ref: subprocess.run(["git", "-C", str(repo), "rev-parse", ref], capture_output=True, text=True).stdout.strip()  # noqa: E731
    check("dry run: main and spec-20 unchanged in git", rev("main") == fx["main"] and rev("spec-20") == fx["branch"])
    check("dry run: no file outside the two dry-run files changed", tree_hash(repo) == fx["tree"])
    merges = [i for i, b in enumerate(blocks) if b["op"] == "merge a pr"]
    closes = [i for i, b in enumerate(blocks) if b["op"] == "close"]
    check("merged once", len(merges) == 1, f"{len(merges)} merge blocks")
    if merges:
        m = blocks[merges[0]]
        check("merge: pull request 1, a merge commit (not a squash)", m["pull"].lstrip("#") == "1" and m["method"] == "merge", f"{m['pull']} {m['method']}")
        check("merge: titled with the Spec pull request's typed title", m["title"].strip("`'\" ") == fx["title"], m["title"])
        edits = [i for i, b in enumerate(blocks) if b["op"] == "edit a pull request body" and i < merges[0]]
        final = blocks[edits[-1]]["body"] if edits else ""
        check("the body is edited before the merge, dropping Ticket 23's Closes line",
              bool(edits) and not re.search(r"#23\b", final), "no edit" if not edits else "line kept")
        check("the edited body keeps the Spec's and both landed Tickets' Closes lines",
              all(re.search(rf"Closes #{n}\b", final) for n in sorted(CLOSE)))
        before = closed_numbers(blocks, [i for i in closes if i < merges[0]])
        check("nothing closed before the merge", not before, str(sorted(before)))
        after = [i for i in closes if i > merges[0]]
        got = closed_numbers(blocks, after)
        check("after the merge, exactly the Spec and the landed Tickets close", got == CLOSE, f"closed {sorted(got)}")
        check("each close is as completed, naming the pull request",
              bool(after) and all(blocks[i]["outcome"].startswith("completed") and re.search(r"(#1\b|pull request 1|PR 1|pulls/1)", blocks[i]["reason"], re.I) for i in after))
    check("the dropped Ticket 23 is never closed, and not as not planned either", not closed_numbers(blocks, closes) & STAY)
    return all(results)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: score.py <out-dir>")
    sys.exit(0 if score(sys.argv[1]) else 1)
