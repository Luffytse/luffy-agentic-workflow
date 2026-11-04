#!/usr/bin/env python3
"""Writes the batch prompt files for one run of the eval: each holds the skill listing and a few case prompts,
without the expected answers, and asks for one JSON object mapping case id to the skill the session would load.

Usage: python3 evals/skill-descriptions/make_batches.py <skills-dir> <out-dir> [--size 7] [--seed 621]
Writes <out-dir>/listing.txt, <out-dir>/batch-NN.md (one per fresh subagent), <out-dir>/batches.json (batch ->
{label: case id}) and an empty <out-dir>/answers/ folder where each subagent's JSON answer is saved as batch-NN.json.
Situations carry opaque labels S1, S2, ... (unique across the run), never the case ids, which name the answer;
batches.json maps each label back to its case id and score.py reads it. Cases are shuffled with a fixed seed, so main's and the branch's runs get the same batches.
"""
import argparse
import json
import pathlib
import random
import sys

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import build_listing  # noqa: E402
import cases as case_data  # noqa: E402

TEMPLATE = """You are a coding agent. Below are the skills you can load, each with its description, exactly as your
harness lists them. For each situation after the list, say which ONE skill you would load first, or "none" if no
skill applies. Judge only from the names and descriptions. Do not open any file or run any tool.

## Skills

{listing}
## Situations

{situations}
## Answer

Reply with one JSON object and nothing else. Its keys are the situation labels above (S1, S2, ...); each value is
the skill name exactly as listed (with its `dev-skills:` prefix), or "none". Example: {{"{example_id}": "dev-skills:some-skill"}}
"""


def make_batches(cases, size, seed):
    order = list(cases)
    random.Random(seed).shuffle(order)
    return [order[i:i + size] for i in range(0, len(order), size)]


def render_batch(listing_text, batch):
    """batch: [(label, case)]. Situations are headed by an opaque label, never the case id (ids hold the answer)."""
    situations = "".join(f"### {label}\n{c['prompt']}\n\n" for label, c in batch)
    return TEMPLATE.format(listing=listing_text, situations=situations, example_id=batch[0][0])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skills_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--size", type=int, default=7)
    ap.add_argument("--seed", type=int, default=621)
    args = ap.parse_args(argv)
    skills = build_listing.load_skills(args.skills_dir)
    if not skills:
        print(f"no SKILL.md under {args.skills_dir}", file=sys.stderr)
        return 2
    listing_text = build_listing.listing(skills)
    out = pathlib.Path(args.out_dir)
    (out / "answers").mkdir(parents=True, exist_ok=True)
    (out / "listing.txt").write_text(listing_text, encoding="utf-8")
    index = {}
    label = 0
    for n, batch in enumerate(make_batches(case_data.load(), args.size, args.seed), 1):
        name = f"batch-{n:02d}"
        labelled = []
        for c in batch:
            label += 1
            labelled.append((f"S{label}", c))
        (out / f"{name}.md").write_text(render_batch(listing_text, labelled), encoding="utf-8")
        index[name] = {lab: c["id"] for lab, c in labelled}
    (out / "batches.json").write_text(json.dumps(index, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {len(index)} batches to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
