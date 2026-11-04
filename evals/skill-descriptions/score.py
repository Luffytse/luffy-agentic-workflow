#!/usr/bin/env python3
"""Scores one run of the skill-descriptions eval: overall accuracy, accuracy per expected skill, and the
confusion pairs (expected -> got) of the misses.

Usage: python3 evals/skill-descriptions/score.py <run-dir> [--json]
<run-dir> is a make_batches.py output folder whose answers/ holds each subagent's JSON {situation label: skill}.
A name may carry the `dev-skills:` prefix. A case with no answer counts as a miss, got "(no answer)"; a JSON null
or other non-string answer is a miss too, got "(invalid answer)".
"""
import argparse
import collections
import json
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import cases as case_data  # noqa: E402

NO_ANSWER = "(no answer)"
INVALID = "(invalid answer)"


def norm(name):
    if not isinstance(name, str):
        return INVALID  # null, a number, a list: never "none"
    name = name.strip().strip("`").lower()
    return name.split(":", 1)[1] if name.startswith("dev-skills:") else name


def load_answers(run_dir):
    """Reads <run-dir>/batches.json and every <run-dir>/answers/*.json (keyed by the situation labels) and returns
    {case id: normalised answer}. A label that batches.json does not know is an error."""
    run = pathlib.Path(run_dir)
    labels = {}
    for mapping in json.loads((run / "batches.json").read_text(encoding="utf-8")).values():
        labels.update(mapping)
    answers = {}
    for f in sorted((run / "answers").glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{f}: not a JSON object")
        for label, value in data.items():
            if label not in labels:
                raise ValueError(f"{f}: unknown label {label!r}")
            answers[labels[label]] = norm(value)
    return answers


def score(cases, answers):
    """Returns a dict: total, correct, per_skill {expected: [n, correct]}, misses [(id, kind, expected, got)],
    confusion Counter {(expected, got): n}, near_miss_confusion set of pairs from near-miss cases."""
    per_skill = {}
    misses = []
    confusion = collections.Counter()
    near_pairs = set()
    correct = 0
    for c in cases:
        got = answers.get(c["id"], NO_ANSWER)
        row = per_skill.setdefault(c["expected"], [0, 0])
        row[0] += 1
        if got == c["expected"]:
            row[1] += 1
            correct += 1
        else:
            misses.append((c["id"], c["kind"], c["expected"], got))
            confusion[(c["expected"], got)] += 1
            if c["kind"] == "near-miss":
                near_pairs.add((c["expected"], got))
    return {"total": len(cases), "correct": correct, "per_skill": per_skill, "misses": misses,
            "confusion": confusion, "near_miss_confusion": near_pairs}


def report(result):
    lines = [f"overall: {result['correct']}/{result['total']} = {result['correct'] / result['total']:.1%}", "",
             "per expected skill (correct/cases):"]
    for skill, (n, ok) in sorted(result["per_skill"].items()):
        lines.append(f"  {skill}: {ok}/{n}{'' if ok == n else '  <'}")
    lines += ["", "misses (expected -> got):"]
    if not result["misses"]:
        lines.append("  none")
    for cid, kind, exp, got in result["misses"]:
        lines.append(f"  {cid} [{kind}]: {exp} -> {got}")
    lines += ["", "confusion pairs:"]
    if not result["confusion"]:
        lines.append("  none")
    for (exp, got), n in sorted(result["confusion"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"  {exp} -> {got}: {n}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    result = score(case_data.load(), load_answers(args.run_dir))
    if args.json:
        print(json.dumps({"total": result["total"], "correct": result["correct"], "per_skill": result["per_skill"],
                          "misses": result["misses"]}, indent=1))
    else:
        print(report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
