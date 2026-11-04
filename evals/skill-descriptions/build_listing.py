#!/usr/bin/env python3
"""Builds the skill listing the harness shows a session: one `- <prefix>:<name>: <description>` line per skill,
descriptions read from each SKILL.md frontmatter (hidden skills, `user-invocable: false`, are listed too, as the
harness lists them). Also counts the words of each description.

Usage:
  python3 evals/skill-descriptions/build_listing.py <skills-dir> [--prefix dev-skills]   # the listing
  python3 evals/skill-descriptions/build_listing.py <skills-dir> --counts                 # words per skill, then total
<skills-dir> is a checkout's plugins/dev-skills/skills or the same folder inside a `git archive` of main.
"""
import argparse
import json
import pathlib
import sys

PREFIX = "dev-skills"


def parse_frontmatter(text):
    """Returns the frontmatter's top-level `key: value` pairs. Handles the two scalar forms the skills use
    (a double-quoted string, read as JSON, and a plain one-line string); anything else raises."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("no frontmatter")
    out = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return out
        if not line or line[0] in " \t#" or ":" not in line:
            continue  # nested block (metadata:) or comment
        key, _, value = line.partition(":")
        value = value.strip()
        if value and value[0] in ">|":
            raise ValueError(f"block scalar for {key!r} is not supported")
        if value[:1] == '"':
            value = json.loads(value)
        elif value[:1] == "'":
            value = value[1:-1].replace("''", "'")
        out[key.strip()] = value
    raise ValueError("frontmatter is not closed")


def load_skills(skills_dir):
    """Returns [(name, description, hidden)] sorted by folder name."""
    skills = []
    for path in sorted(pathlib.Path(skills_dir).glob("*/SKILL.md")):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        name = fm.get("name", path.parent.name)
        if "description" not in fm:
            raise ValueError(f"{path}: no description")
        hidden = str(fm.get("user-invocable", "true")).lower() == "false"
        skills.append((name, fm["description"], hidden))
    return skills


def listing(skills, prefix=PREFIX):
    return "\n".join(f"- {prefix}:{name}: {desc}" for name, desc, _ in skills) + "\n"


def word_counts(skills):
    """Returns ([(name, words)], total)."""
    rows = [(name, len(desc.split())) for name, desc, _ in skills]
    return rows, sum(w for _, w in rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skills_dir")
    ap.add_argument("--prefix", default=PREFIX)
    ap.add_argument("--counts", action="store_true", help="print words per description and the total, not the listing")
    args = ap.parse_args(argv)
    skills = load_skills(args.skills_dir)
    if not skills:
        print(f"no SKILL.md under {args.skills_dir}", file=sys.stderr)
        return 2
    if args.counts:
        rows, total = word_counts(skills)
        for name, words in sorted(rows, key=lambda r: (-r[1], r[0])):
            print(f"{words:4d}  {name}")
        print(f"{total:4d}  TOTAL ({len(rows)} skills, longest {max(w for _, w in rows)})")
    else:
        sys.stdout.write(listing(skills, args.prefix))
    return 0


if __name__ == "__main__":
    sys.exit(main())
