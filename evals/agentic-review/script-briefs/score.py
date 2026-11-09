#!/usr/bin/env python3
"""Scores one run of the script-briefs case: did the briefs of a Round come from the plugin's brief script?

Usage: score.py <case-dir> [--script <review_briefs.py>]
<case-dir> is what make-case.sh built, after the subagent ran. The scorer builds the briefs the script gives for the
same inputs (the branch's script by default, even when the run was made on main's skill, so main's hand-built briefs
are compared with the script's) and compares them byte for byte with the files the run left in <case-dir>/repo.briefs/round/.
Checks: F1 exactly the four files; B1-B3 the three Finder briefs identical to the script's; B4 the Verifier brief
identical to the script's, which holds the three canned messages byte for byte (a Finder brief's report path is compared
with the run's own directory in its place); H2 the handoff message to the standards Finder (<case-dir>/handoff-standards.txt) names the brief file's
path and is far shorter than the brief, which it does not paste; L1 nothing written inside the
repository. Exit 0 when every check passes. Hand-scored besides: the reply names the command it ran (H1).
Keep this file away from the subagent under test.
"""
import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_SCRIPT = HERE.parents[2] / "plugins/dev-skills/skills/review-rounds/review_briefs.py"
FILES = ["finder-standards.md", "finder-spec.md", "finder-adversarial.md", "verifier.md"]
REPORTS = {"standards": "standards-finder.txt", "spec": "spec-finder.txt", "adversarial": "adversarial-finder.txt"}


def expected(case: pathlib.Path, script: pathlib.Path, tmp: pathlib.Path, run_dir: pathlib.Path) -> dict:
    repo = case / "repo"
    common = ["--base", "main", "--head", "planted", "--repo", str(repo), "--spec", str(repo / ".scratch/SPEC.md")]
    reports = tmp / "reports"
    reports.mkdir()
    for finder, name in REPORTS.items():
        shutil.copy(HERE / "messages" / name, reports / f"{finder}.md")
    out = tmp / "out"
    for argv in (["round1", "--level", "standard", *common, "--out", str(out)],
                 ["verify", "--level", "standard", *common, "--reports", str(reports), "--out", str(out)]):
        r = subprocess.run([sys.executable, str(script), *argv], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"the script failed ({r.returncode}): {r.stderr.strip()}")
    # A Finder brief names its report file under its own out directory; write the run's directory in its place.
    here, there = str(out.resolve()).encode(), str(run_dir.resolve()).encode()
    return {f: (out / f).read_bytes().replace(here, there) for f in FILES}


def score(case: pathlib.Path, script: pathlib.Path) -> list:
    got_dir = case / "repo.briefs" / "round"
    with tempfile.TemporaryDirectory() as t:
        want = expected(case, script, pathlib.Path(t), got_dir)
    found = sorted(p.name for p in got_dir.iterdir()) if got_dir.is_dir() else []
    rows = [("F1", found == sorted(FILES), f"files left: {found or 'none'}")]
    for i, f in enumerate(FILES, 1):
        p = got_dir / f
        same = p.is_file() and p.read_bytes() == want[f]
        state = "identical to the script's" if same else ("differs from the script's" if p.is_file() else "missing")
        rows.append((f"B{i}", same, f"{f} {state}"))
    brief = got_dir / "finder-standards.md"
    hand = case / "handoff-standards.txt"
    if not (hand.is_file() and brief.is_file()):
        rows.append(("H2", False, "handoff message or standards brief missing"))
    else:
        text, body = hand.read_text(), brief.read_text()
        ok = str(brief.resolve()) in text and len(text) < len(body) // 4 and body[:200] not in text
        rows.append(("H2", ok, "handoff gives the brief's path, not its text" if ok else "handoff does not give the brief's path alone"))
    tree = subprocess.run(["git", "-C", str(case / "repo"), "status", "--porcelain"], capture_output=True, text=True).stdout
    rows.append(("L1", tree.strip() == "", "repository left clean" if not tree.strip() else f"repository changed: {tree.strip()}"))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("--script", default=str(DEFAULT_SCRIPT))
    a = ap.parse_args()
    rows = score(pathlib.Path(a.case).resolve(), pathlib.Path(a.script))
    for cid, ok, note in rows:
        print(f"{'PASS' if ok else 'FAIL'} {cid}: {note}")
    passed = sum(ok for _, ok, _ in rows)
    print(f"{passed}/{len(rows)} checks passed")
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
