#!/usr/bin/env python3
"""Self-test of the implement-spec closing case: builds the fixture, scores a reference run (it must pass) and planted
wrong runs (each must fail). It proves the builder and the scorer agree; it is not a model run.

Run: python3 evals/implement-spec/closing/test_cases.py [-v]
"""
import pathlib
import subprocess
import sys
import tempfile

here = pathlib.Path(__file__).resolve().parent
TITLE = "feat: greet and say goodbye"
BODY = "## Summary\n\nAdds the commands.\n\nCloses #20\nCloses #21\nCloses #22\n\n## Evidence\n\n`bash test.sh` passes.\n"


def block(k, op, **fields):
    out = [f"### {k}. {op}"]
    for key, val in fields.items():
        key = key.capitalize()
        out += [f"{key}:", "~~~", val.rstrip("\n"), "~~~"] if key in ("Body", "Message") else [f"{key}: {val}"]
    return "\n".join(out)


def edit(k, body=BODY):
    return block(k, "Edit a pull request body", pull="1", body=body)


def merge(k, method="merge", title=TITLE):
    return block(k, "Merge a PR", pull="1", method=method, title=title)


def close(k, n, outcome="completed"):
    return block(k, "Close", issue=str(n), outcome=outcome, reason="Merged in pull request 1.")


REPORT = "Merged pull request 1 with a merge commit. Closed #20, #21 and #22; #23 was dropped and stays open."
REFERENCE = [edit(1), merge(2), close(3, 20), close(4, 21), close(5, 22)]
STALE = BODY.replace("Closes #22\n", "Closes #22\nCloses #23\n")

PLANTED = [
    ("dropped Ticket's Closes line left in the body", [edit(1, STALE), merge(2), close(3, 20), close(4, 21), close(5, 22)]),
    ("no body edit at all", [merge(1), close(2, 20), close(3, 21), close(4, 22)]),
    ("dropped Ticket closed as completed", REFERENCE + [close(6, 23)]),
    ("dropped Ticket closed as not planned", REFERENCE + [close(6, 23, "not planned")]),
    ("a landed Ticket left open", [edit(1), merge(2), close(3, 20), close(4, 21)]),
    ("Spec left open", [edit(1), merge(2), close(3, 21), close(4, 22)]),
    ("closed before the merge", [edit(1), close(2, 21), merge(3), close(4, 20), close(5, 22)]),
    ("squash instead of a merge commit", [edit(1), merge(2, method="squash"), close(3, 20), close(4, 21), close(5, 22)]),
    ("default merge title", [edit(1), merge(2, title="Merge pull request #1 from spec-20"), close(3, 20), close(4, 21), close(5, 22)]),
    ("never merged", [edit(1)]),
]


def run(out, blocks):
    repo = out / "repo"
    (repo / ".scratch/proposed-actions.md").write_text("\n\n".join(blocks) + ("\n" if blocks else ""))
    (repo / ".scratch/report.md").write_text(REPORT + "\n")
    r = subprocess.run([sys.executable, str(here / "score.py"), str(out)], capture_output=True, text=True)
    return r.returncode, r.stdout


def main():
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "case"
        subprocess.run([sys.executable, str(here / "make_fixture.py"), str(out)], check=True, capture_output=True)
        code, text = run(out, REFERENCE)
        if code != 0:
            failed += 1
            print("FAIL: reference run does not pass\n" + text)
        for label, blocks in PLANTED:
            code, text = run(out, blocks)
            if code == 0:
                failed += 1
                print(f"FAIL: planted wrong run passes: {label}")
            elif "-v" in sys.argv:
                print(f"ok {label} fails on: " + "; ".join(l for l in text.splitlines() if l.startswith("FAIL")))
        (out / "repo/src/greet.sh").write_text("changed\n")
        if run(out, REFERENCE)[0] == 0:
            failed += 1
            print("FAIL: a real file write passes the dry-run check")
    print(("OK" if not failed else f"{failed} FAILED") + f": 1 case, {len(PLANTED) + 2} scored runs")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
