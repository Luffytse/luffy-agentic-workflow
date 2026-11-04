#!/usr/bin/env python3
"""Score a triage repo-labels run: <out-dir>/repo/.scratch/proposed-actions.md against the case's expected outcome.

Usage: score.py <out-dir> <table|empty>
Prints one line per check (PASS or FAIL with what it saw) and exits 1 when any check fails. It reads outcomes only: the
labels each issue ends with (its fixture labels plus the run's Apply / remove labels blocks, in order), the comments
on it and any label the run creates, never how the run phrased a comment. See evals/triage/README.md.
"""
import importlib.util
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from label_case import CASES, DISCLAIMER, EXPECT, ISSUES, ROLE_LABELS, TABLE  # noqa: E402

_spec = importlib.util.spec_from_file_location("triage_sweep_score", HERE.parent / "backlog-sweep/score.py")
sweep = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sweep)  # defines parse and labels_split; main() runs only when called

results = []


def check(name, ok, seen=""):
    results.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok or seen == "" else f": {seen}"))


def final_labels(blocks):
    """Each issue's labels after the run's Apply / remove labels blocks, in order."""
    labels = {i["n"]: set(i["labels"]) for i in ISSUES}
    for b in blocks:
        if b["op"].startswith("apply") and b["n"] in labels:
            labels[b["n"]] -= sweep.labels_split(b["remove"])
            labels[b["n"]] |= sweep.labels_split(b["add"])
    return labels


def main(out, name):
    repo = pathlib.Path(out) / "repo"
    actions = repo / ".scratch/proposed-actions.md"
    blocks = sweep.parse(actions.read_text() if actions.exists() else "")
    comments = [b for b in blocks if b["op"].startswith("comment")]
    final = final_labels(blocks)
    start = {i["n"]: set(i["labels"]) for i in ISSUES}
    repo_labels = set(TABLE)

    check("the run wrote tracker blocks at all", bool(blocks), "no blocks in .scratch/proposed-actions.md")
    if name == "table":
        e = EXPECT["table"]
        for n, want in e["has"].items():
            check(f"#{n} ends with {sorted(want)}", want <= final[n], f"ends with {sorted(final[n])}")
        for n, no in e["lacks"].items():
            check(f"#{n} does not end with {sorted(no)}", not (no & final[n]), f"ends with {sorted(final[n])}")
        s = e["stale"]
        check(f"#{s}'s removal of `frontend` is explained in a comment on #{s} that names it",
              any(b["n"] == s and "frontend" in b["body"].lower() for b in comments), "no comment on the issue names frontend")
        added = set()
        for n in final:
            added |= final[n] - start[n]
        stray = sorted(added - ROLE_LABELS - repo_labels)
        check("no label outside the roles and the Repo labels table is applied", not stray, f"applied {stray}")
        made = sorted({lab for b in blocks if b["op"].startswith("create a label")
                       for lab in sweep.labels_split(b["label"])})
        check("no label is created", not made, f"created {made}")
    else:
        for n in final:
            kept = {lab for lab in start[n] if lab in EXPECT["empty"]["unchanged_of"]}
            now = {lab for lab in final[n] if lab in EXPECT["empty"]["unchanged_of"]}
            check(f"#{n}: no repo label applied or removed (the table is empty)", kept == now,
                  f"had {sorted(kept)}, ends with {sorted(now)}")
        stray = sorted(set().union(*[final[n] - start[n] for n in final]) - ROLE_LABELS)
        check("no label outside the roles is applied", not stray, f"applied {stray}")
    bare = sorted({b["n"] for b in comments if not b["body"].lstrip().startswith(DISCLAIMER)})
    check("every comment starts with the triage disclaimer", not bare, f"without it: {bare}")
    print(f"{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit("usage: score.py <out-dir> <" + "|".join(CASES) + ">")
    sys.exit(main(*sys.argv[1:]))
