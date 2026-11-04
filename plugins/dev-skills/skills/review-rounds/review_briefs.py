#!/usr/bin/env python3
"""Write the Finder briefs of a review Round, one complete Markdown file per agent, from the skill's own brief files.

Usage:
  review_briefs.py round1 --level quick|standard|deep --base <ref> --out <dir>
                   [--head <ref>] [--repo <dir>] [--spec <file>] [--standards <file>] [--earlier <file>]
                   [--design <file>] [--angle <name>]

round1 writes the briefs for Round 1 of a review at the level Round 0 picked: the standards and spec Finders at
quick; plus the adversarial Finder at standard; plus the security Finder at deep (the table in SKILL.md). Without
--spec there is no spec Finder. Later subcommands (the Verifier brief, later Rounds, a Ticket check, a fixed point)
extend this CLI; each subcommand is a function of the same shape as round1.

Inputs the thread passes, all files: --spec (the spec's text), --standards (a list of standards files, one path per
line, relative to --repo), --earlier (the earlier open Findings with their disputes), --design (the design answers),
and --angle, a name from the adversarial angle list in FINDERS.md (default: the first, "Bugs and edge cases").
Round values come from git: the diff command, commit list and head. From the repo it reads, when present, REVIEW.md
(the meaning of Important, the Skip list, the Always check lines with the kinds of file they apply to),
docs/dev-skills/boundaries.md (the Boundary record) and docs/dev-skills/index.md (the docs index); each absent one
falls back to the skill's default.

Every brief sentence is cut out of the skill's brief files (FINDERS.md, DEEP.md, SKILL.md here; the review-record and
docs-index skills beside this one) when the script runs; none is copied into it. A section it cannot find stops it
with a message naming the section (exit 3) and nothing is written. --out must be outside the work tree; the script
replaces the finder-*.md files already there, and writes nothing else anywhere. It calls only `git`.

Exit 0 written, 2 usage error, 3 a section could not be found. Prints one line per file: file, role, tier.
"""
import argparse
import fnmatch
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SKILLS = HERE.parent

# Kinds of changed file that are not code: the smell baseline applies only when a changed file is none of these.
NOT_CODE = {".md", ".markdown", ".txt", ".rst", ".adoc", ".csv", ".json", ".yaml", ".yml", ".toml", ".ini", ".lock",
            ".svg", ".png", ".jpg", ".jpeg", ".gif", ".pdf"}
LEVELS = ("quick", "standard", "deep")
# Who runs at Round 1, by level: the table in SKILL.md.
ROLES = {
    "quick": ("standards", "spec"),
    "standard": ("standards", "spec", "adversarial"),
    "deep": ("standards", "spec", "adversarial", "security"),
}


class MissingSection(Exception):
    pass


class Usage(Exception):
    pass


# ---- cutting text out of the skill files ----

def read_skill_file(rel):
    path = SKILLS / rel
    try:
        return path.read_text()
    except OSError:
        raise MissingSection("file %s" % rel)


def headings(text):
    """(line index, level, heading line) for each Markdown heading; a line inside a code fence is never one."""
    out, fence = [], False
    for i, line in enumerate(text.splitlines()):
        if line.startswith("```"):
            fence = not fence
            continue
        m = None if fence else re.match(r"^(#+) ", line)
        if m:
            out.append((i, len(m.group(1)), line))
    return out


def section(text, prefix, name):
    """The heading starting with prefix and everything under it, up to the next heading of the same or higher level."""
    lines, hs = text.splitlines(), headings(text)
    for n, (i, level, line) in enumerate(hs):
        if line.startswith(prefix):
            end = len(lines)
            for j, lvl2, _ in hs[n + 1:]:
                if lvl2 <= level:
                    end = j
                    break
            return "\n".join(lines[i:end]).rstrip("\n")
    raise MissingSection(name)


def heading_of(text, prefix, name):
    for _, _, line in headings(text):
        if line.startswith(prefix):
            return line
    raise MissingSection(name)


def quoted(text, label, name):
    """The text after `<label>: "` up to the quote that ends a line, which may run over several lines."""
    m = re.search(r"^" + re.escape(label) + r': "(.*?)"$', text, re.S | re.M)
    if not m or not m.group(1).strip():
        raise MissingSection(name)
    return m.group(1)


def tier(text, prefix, name):
    m = re.search(r"\((cheap|regular|premium)\b", heading_of(text, prefix, name))
    if not m:
        raise MissingSection("tier of the " + name)
    return m.group(1)


def strip_front_matter(text):
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():].strip() if m else text.strip()


class Rules:
    """Everything the briefs say, cut from the skill files at run time."""

    def __init__(self):
        finders = read_skill_file("review-rounds/FINDERS.md")
        deep = read_skill_file("review-rounds/DEEP.md")
        skill = read_skill_file("review-rounds/SKILL.md")
        self.shared = quoted(finders, "Shared brief", "shared brief")
        self.copy_rule = quoted(finders, "Copy rule", "copy rule")
        m = re.search(r'^The standards, spec and later-Round Finders also get .*? with: "(.*)"$', finders, re.M)
        if not m:
            raise MissingSection("earlier-Findings line")
        self.earlier_line = m.group(1)
        self.format = section(finders, "## Finding format", "Finding format")
        self.smell = section(finders, "### Smell baseline", "Smell baseline")
        self.drift = section(finders, "### Docs index drift", "Docs index drift")
        std = section(finders, "## Standards Finder", "Standards Finder")
        self.standards_brief = quoted(std, "Brief", "Standards Finder brief")
        self.spec_brief = quoted(section(finders, "## Spec Finder", "Spec Finder"), "Brief", "Spec Finder brief")
        adv = section(finders, "## Adversarial Finder", "Adversarial Finder")
        self.adv_brief = quoted(adv, "Brief", "Adversarial Finder brief")
        if "<angle>" not in self.adv_brief:
            raise MissingSection("angle place in the Adversarial Finder brief")
        if "Angles:" not in adv:
            raise MissingSection("Adversarial Finder angle list")
        self.angles = [(m.group(1), m.group(2)) for m in
                       re.finditer(r"^- \*\*(.+?)\*\*: (.*)$", adv.split("Angles:", 1)[1], re.M)]
        if not self.angles:
            raise MissingSection("Adversarial Finder angle list")
        self.security_brief = quoted(section(deep, "## Security Finder", "Security Finder"), "Brief",
                                     "Security Finder brief")
        m = re.search(r"Without it, (\*\*Important\*\* means.*)$", skill, re.M)
        if not m:
            raise MissingSection("default meaning of Important")
        self.important_default = m.group(1)
        self.record_terms = section(read_skill_file("review-record/SKILL.md"), "## Terminology",
                                    "review-record Terminology")
        self.index_contract = strip_front_matter(read_skill_file("docs-index/SKILL.md"))
        if not self.index_contract:
            raise MissingSection("docs-index contract")
        self.tiers = {
            "standards": tier(finders, "## Standards Finder", "Standards Finder"),
            "spec": tier(finders, "## Spec Finder", "Spec Finder"),
            "adversarial": tier(finders, "## Adversarial Finder", "Adversarial Finder"),
            "security": tier(deep, "## Security Finder", "Security Finder"),
        }


def angle_text(rules, name):
    """The adversarial brief with the named angle written in, as the skill's list names it."""
    for title, _desc in rules.angles:
        if title.lower() == name.lower():
            return rules.adv_brief.replace("<angle>", title.rstrip("."))
    raise Usage("no angle called '%s'; the angles are: %s" % (name, ", ".join(t for t, _ in rules.angles)))


def drop_items(brief, keep):
    """Drop the lettered items (a), (b)... the skill says to drop; keep is the set of letters to keep.

    The brief's item list is `(a) ...; (b) ...; (c) ...; (d) ... . Sentence after.`; a sentence after the last item
    stays. A brief that no longer has that shape is returned whole.
    """
    parts = re.split(r"(?=\([a-d]\) )", brief)
    prefix, items, tails = parts[0], [], []
    for part in parts[1:]:
        m = re.match(r"\(([a-d])\) (.*?)(;\s*$|\.\s+(?=[A-Z])|\.\s*$)(.*)$", part, re.S)
        if not m:
            return brief
        items.append((m.group(1), m.group(2)))
        tails.append(m.group(4).strip())
    if not items:
        return brief
    kept = ["(%s) %s" % (letter, text) for letter, text in items if letter in keep]
    if not kept:
        return brief
    return prefix + "; ".join(kept) + "." + "".join(" " + t for t in tails if t)


# ---- reading the repository ----

def git(repo, *args):
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    except OSError:
        raise Usage("git could not be run")
    if r.returncode != 0:
        raise Usage("git %s failed: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def read_text_file(path, what):
    try:
        return pathlib.Path(path).read_text()
    except OSError as e:
        raise Usage("cannot read %s %s: %s" % (what, path, e.strerror))


def review_md_parts(repo):
    """(important, skip, always lines as (text, globs)) from REVIEW.md; each None / empty when absent."""
    path = repo / "REVIEW.md"
    if not path.is_file():
        return None, None, []
    secs, name = {}, None
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            name = line[3:].strip()
            secs[name] = []
        elif name is not None:
            secs[name].append(line)
    body = lambda k: ("\n".join(secs[k]).strip() or None) if k in secs else None
    always, cur = [], None
    for line in secs.get("Always check", []):
        if line.startswith("- "):
            cur = [line]
            always.append(cur)
        elif cur is not None and line.strip():
            cur.append(line)
        else:
            cur = None
    lines = []
    for chunk in always:
        text = "\n".join(chunk)
        m = re.search(r"\(files: ([^)]*)\)", text)
        lines.append((text, re.findall(r"`([^`]+)`", m.group(1)) if m else []))
    return body("Important"), body("Skip"), lines


def applies(globs, changed):
    return not globs or any(fnmatch.fnmatch(p, g) for p in changed for g in globs)


def is_code(path):
    return pathlib.PurePosixPath(path).suffix.lower() not in NOT_CODE


# ---- building ----

def fence(text):
    """The text in a code fence longer than any backtick run inside it."""
    ticks = "`" * max(3, max((len(r) for r in re.findall(r"`+", text)), default=0) + 1)
    return "%s\n%s\n%s" % (ticks, text.rstrip("\n"), ticks)


def build_round1(rules, a):
    repo = pathlib.Path(a.repo).resolve()
    toplevel = pathlib.Path(git(repo, "rev-parse", "--show-toplevel").strip()).resolve()
    out = pathlib.Path(a.out).resolve()
    if out == toplevel or toplevel in out.parents:
        raise Usage("--out must be outside the work tree (%s)" % toplevel)
    head = git(repo, "rev-parse", a.head).strip()
    base = a.base
    git(repo, "rev-parse", "--verify", base + "^{commit}")
    commits = git(repo, "log", "--oneline", "%s..%s" % (base, head)).strip() or "(none)"
    changed = [p for p in git(repo, "diff", "--name-only", "-z", "%s...%s" % (base, head)).split("\0") if p]
    diff_cmd = "git -C %s diff %s...%s" % (repo, base, head)

    spec = read_text_file(a.spec, "spec") if a.spec else None
    earlier = read_text_file(a.earlier, "earlier Findings file") if a.earlier else None
    design = read_text_file(a.design, "design answers file") if a.design else None
    standards = []
    if a.standards:
        for rel in read_text_file(a.standards, "standards list").splitlines():
            rel = rel.strip()
            if rel:
                standards.append((rel, read_text_file(repo / rel, "standards file")))
    angle = angle_text(rules, a.angle)  # validated at every level, written in only where an adversarial Finder runs

    important, skip, always = review_md_parts(repo)
    boundary_path = repo / "docs/dev-skills/boundaries.md"
    boundary = boundary_path.read_text().strip() if boundary_path.is_file() else None
    has_index = (repo / "docs/dev-skills/index.md").is_file()
    has_code = any(is_code(p) for p in changed)
    lines = [text for text, globs in always if applies(globs, changed)]

    round_part = "\n\n".join([
        "## This Round\n\nRound 1 of the review, level %s. Head: `%s`. Base: `%s`." % (a.level.capitalize(), head, base),
        "Diff command:\n\n%s" % fence(diff_cmd),
        "Commits:\n\n%s" % fence(commits),
        "## Meaning of Important\n\n%s" % (
            important + "\n\n" + rules.important_default if important and "default" in important.lower()
            else important or rules.important_default),
        "## Skip list\n\n%s" % (skip or "None."),
        "## Boundary record\n\n%s" % (boundary or "None: the project has no Boundary record."),
    ])
    common = "\n\n".join([
        "## Shared brief\n\n" + rules.shared,
        "## Copy rule\n\n" + rules.copy_rule,
        rules.format,
    ])
    spec_part = "\n\n".join([
        "## The spec, the earlier Findings and the design answers",
        "The spec:\n\n%s" % (fence(spec) if spec else "None available."),
        "Earlier Findings:\n\n%s" % (earlier.strip() if earlier else "None."),
        "Design answers:\n\n%s" % (design.strip() if design else "None."),
        rules.earlier_line,
    ])

    def brief(title, text, *parts):
        return "\n\n".join(["# %s" % title, text, round_part, *parts, common]) + "\n"

    files = {}
    roles = ROLES[a.level]
    if "standards" in roles:
        keep = {"a"} | ({"b"} if has_code else set()) | ({"c"} if lines else set()) | ({"d"} if has_index else set())
        parts = []
        parts.append("## Standards files\n\n" + ("\n\n".join("`%s`:\n\n%s" % (r, fence(t)) for r, t in standards)
                                                 if standards else "None."))
        parts.append("## Always check lines for the files this diff touches\n\n" + ("\n".join(lines) if lines else "None.")
                     + ("\n\n" + rules.record_terms if lines else ""))
        if has_code:
            parts.append(rules.smell)
        if has_index:
            parts.append(rules.drift + "\n\n## Docs index contract\n\n" + rules.index_contract)
        parts.append(spec_part)
        files["finder-standards.md"] = ("standards", brief("Standards Finder brief",
                                                           drop_items(rules.standards_brief, keep), *parts))
    if "spec" in roles and spec is not None:
        files["finder-spec.md"] = ("spec", brief("Spec Finder brief", rules.spec_brief, spec_part))
    if "adversarial" in roles:
        files["finder-adversarial.md"] = ("adversarial", brief("Adversarial Finder brief", angle))
    if "security" in roles:
        sec = "The spec:\n\n%s" % (fence(spec) if spec else "None available.")
        files["finder-security.md"] = ("security", brief("Security Finder brief", rules.security_brief,
                                                         "## The spec\n\n" + sec))
    return out, files


def round1(args):
    rules = Rules()
    out, files = build_round1(rules, args)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("finder-*.md"):
        old.unlink()
    for name, (_role, text) in files.items():
        (out / name).write_text(text)
    for name, (role, _text) in files.items():
        print("%s\t%s Finder\t%s tier" % (out / name, role, rules.tiers[role]))


def main(argv):
    p = argparse.ArgumentParser(prog="review_briefs.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    r1 = sub.add_parser("round1", help="Round 1 Finder briefs")
    r1.add_argument("--level", required=True, type=str.lower, choices=LEVELS)
    r1.add_argument("--base", required=True)
    r1.add_argument("--head", default="HEAD")
    r1.add_argument("--repo", default=".")
    r1.add_argument("--out", required=True)
    r1.add_argument("--spec")
    r1.add_argument("--standards")
    r1.add_argument("--earlier")
    r1.add_argument("--design")
    r1.add_argument("--angle", default=None)
    r1.set_defaults(run=round1)
    args = p.parse_args(argv)
    try:
        if args.angle is None:
            args.angle = Rules().angles[0][0]
        args.run(args)
    except Usage as e:
        print("review_briefs.py: %s" % e, file=sys.stderr)
        return 2
    except MissingSection as e:
        print("review_briefs.py: could not find %s in the skill files; nothing was written" % e, file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
