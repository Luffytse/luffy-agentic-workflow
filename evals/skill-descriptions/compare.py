#!/usr/bin/env python3
"""Compares a new run with the baseline by the rule of issue #621. The new run passes when
  1. it picks the expected skill at least as often as the baseline overall,
  2. for every skill, it picks that skill on its cases at least as often as the baseline, and
  3. it has no new near-miss confusion pair: no (expected -> got) miss on a near-miss case that the baseline did
     not also make (on any case).
Confusion pairs that are new but come from other cases, and a drop on the "none" cases, are reported as warnings
and do not fail the run.

Usage: python3 evals/skill-descriptions/compare.py <baseline-run-dir> <new-run-dir>
Exit 0 on pass, 1 on fail.
"""
import argparse
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import cases as case_data  # noqa: E402
import score as scorer  # noqa: E402


def compare(base, new):
    """base, new: score() results. Returns (passed, failures, warnings)."""
    failures, warnings = [], []
    if new["correct"] < base["correct"]:
        failures.append(f"overall: new {new['correct']}/{new['total']} is below baseline {base['correct']}/{base['total']}")
    for skill in sorted(base["per_skill"]):
        b = base["per_skill"][skill][1]
        n = new["per_skill"].get(skill, [0, 0])[1]
        if n < b:
            msg = f"{skill}: new {n} is below baseline {b} of {base['per_skill'][skill][0]}"
            (warnings if skill == "none" else failures).append(msg)
    base_pairs = set(base["confusion"])
    for pair in sorted(new["near_miss_confusion"] - base_pairs):
        failures.append(f"new near-miss confusion: {pair[0]} -> {pair[1]}")
    for pair in sorted(set(new["confusion"]) - base_pairs - new["near_miss_confusion"]):
        warnings.append(f"new confusion (not a near-miss case): {pair[0]} -> {pair[1]}")
    return not failures, failures, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("baseline")
    ap.add_argument("new")
    args = ap.parse_args(argv)
    cases = case_data.load()
    base = scorer.score(cases, scorer.load_answers(args.baseline))
    new = scorer.score(cases, scorer.load_answers(args.new))
    passed, failures, warnings = compare(base, new)
    print(f"baseline: {base['correct']}/{base['total']}   new: {new['correct']}/{new['total']}")
    for w in warnings:
        print(f"warning: {w}")
    for f in failures:
        print(f"FAIL: {f}")
    print("PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
