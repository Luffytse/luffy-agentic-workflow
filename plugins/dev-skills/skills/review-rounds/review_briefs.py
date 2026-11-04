#!/usr/bin/env python3
"""Write the Finder briefs of a review Round, one complete Markdown file per agent, from the skill's own brief files.

Usage:
  review_briefs.py round1 --level quick|standard|deep --base <ref> --out <dir>
                   [--head <ref>] [--repo <dir>] [--spec <file>] [--standards <file>] [--earlier <file>]
                   [--design <file>] [--angle <name>]
  review_briefs.py verify --level quick|standard|deep --base <ref> --out <dir> --reports <dir>
                   [--head <ref>] [--repo <dir>] [--spec <file>] [--earlier <file>] [--design <file>]

round1 writes the briefs for Round 1 of a review at the level Round 0 picked: the standards and spec Finders at
quick; plus the adversarial Finder at standard; plus the security Finder at deep (the table in SKILL.md). Without
--spec there is no spec Finder. Later subcommands (later Rounds, a Ticket check, a fixed point) extend this CLI; each
subcommand is a function of the same shape as round1.

verify writes the Verifier's brief (verifier.md) for a Round 1 whose Finders have reported. --reports is a directory
holding one file per Finder of the Round, named <finder>.md with the Finder as the table in SKILL.md names it:
standards, spec (only with --spec), adversarial (standard and deep), security (deep). The thread saves each Finder's
final message there unchanged. First every report is checked: it must hold one or more Findings in the Finding format
(a heading and every field line of the format) or "nothing found". A missing, empty or off-format report stops the
script (exit 3) with every such Finder named, and nothing is written; the thread asks that Finder again. A passing
report goes into the brief byte for byte, in a code fence under a heading naming its Finder. The brief also holds the
Verifier brief and copy rule (VERIFY.md, FINDERS.md), the Finding format, the Round values, the spec, the design
answers, the earlier open Findings with their disputes (--earlier), the meaning of Important and the Skip list, and
only the Always check lines whose name a candidate's Bug class matches (same words, ignoring case and punctuation, or
one containing the other), with the review-record meaning. When every report is "nothing found" and --earlier is
absent or empty, no Verifier runs: nothing is written, any old verifier.md is removed, and the output says so. The
Verifier's tier (premium at Deep) is in the printed line.

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
replaces the finder-*.md (verify: verifier.md) files already there, and writes nothing else anywhere. It calls only `git`.

Exit 0 written, 2 usage error, 3 a section could not be found or a Finder report is missing, empty or off-format (verify). Prints one line per file: file, role, tier.
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


class BadReports(Exception):
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
        verify = read_skill_file("review-rounds/VERIFY.md")
        self.verifier_brief = quoted(verify, "Brief", "Verifier brief")
        m = re.search(r"on the (cheap|regular|premium) tier \((cheap|regular|premium) at Deep\)", verify)
        if not m:
            raise MissingSection("Verifier tier")
        self.verifier_tiers = m.groups()
        self.format_level = len(re.match(r"#+", re.search(r"^#+ .*$", self.format.split("```", 1)[1], re.M)
                                         .group(0)).group(0)) if "```" in self.format else 0
        self.format_fields = re.findall(r"^- ([^:(]+?)(?: \([^)]*\))?:", self.format, re.M)
        if not self.format_level or not self.format_fields:
            raise MissingSection("Finding format fields")
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


class RoundValues:
    """What a Round's briefs share: the diff command, commits and head from git, and the repo's REVIEW.md, Boundary
    record and docs index when present."""

    def __init__(self, rules, a):
        self.repo = repo = pathlib.Path(a.repo).resolve()
        toplevel = pathlib.Path(git(repo, "rev-parse", "--show-toplevel").strip()).resolve()
        self.out = pathlib.Path(a.out).resolve()
        if self.out == toplevel or toplevel in self.out.parents:
            raise Usage("--out must be outside the work tree (%s)" % toplevel)
        self.head = head = git(repo, "rev-parse", a.head).strip()
        self.base = base = a.base
        git(repo, "rev-parse", "--verify", base + "^{commit}")
        commits = git(repo, "log", "--oneline", "%s..%s" % (base, head)).strip() or "(none)"
        self.changed = [p for p in git(repo, "diff", "--name-only", "-z", "%s...%s" % (base, head)).split("\0") if p]
        diff_cmd = "git -C %s diff %s...%s" % (repo, base, head)
        self.important, self.skip, self.always = review_md_parts(repo)
        boundary_path = repo / "docs/dev-skills/boundaries.md"
        self.boundary = boundary_path.read_text().strip() if boundary_path.is_file() else None
        self.has_index = (repo / "docs/dev-skills/index.md").is_file()
        self.diff_part = "Diff command:\n\n%s\n\nCommits:\n\n%s" % (fence(diff_cmd), fence(commits))
        self.important_part = "## Meaning of Important\n\n%s" % (
            self.important + "\n\n" + rules.important_default if self.important and "default" in self.important.lower()
            else self.important or rules.important_default)
        self.skip_part = "## Skip list\n\n%s" % (self.skip or "None.")


def build_round1(rules, a):
    rv = RoundValues(rules, a)
    repo, out, head, base, changed = rv.repo, rv.out, rv.head, rv.base, rv.changed
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

    boundary, has_index, always = rv.boundary, rv.has_index, rv.always
    has_code = any(is_code(p) for p in changed)
    lines = [text for text, globs in always if applies(globs, changed)]

    round_part = "\n\n".join([
        "## This Round\n\nRound 1 of the review, level %s. Head: `%s`. Base: `%s`." % (a.level.capitalize(), head, base),
        rv.diff_part,
        rv.important_part,
        rv.skip_part,
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


# ---- the Verifier brief ----

NOTHING = re.compile(r"^\W*nothing found\W*$", re.I)


def has_findings(rules, text):
    return any(level == rules.format_level for _i, level, _l in headings(text))


def report_problem(rules, text):
    """Why a Finder's report is neither Findings in the Finding format nor "nothing found"; None when it is one."""
    if not text.strip():
        return "it is empty"
    hs = [(i, line) for i, level, line in headings(text) if level == rules.format_level]
    if not hs:
        if any(NOTHING.match(line) for line in text.splitlines()):
            return None
        return "it has no Finding heading and does not say nothing found"
    lines = text.splitlines()
    for n, (i, line) in enumerate(hs):
        block = lines[i + 1:hs[n + 1][0] if n + 1 < len(hs) else len(lines)]
        for f in rules.format_fields:
            if not any(re.match(r"^- %s(?: \([^)]*\))?:" % re.escape(f), b) for b in block):
                return "Finding '%s' has no '%s' line" % (line.lstrip("# ").strip(), f)
    return None


def words(s):
    return " ".join(re.findall(r"\w+", s.lower()))


def named_by(always_text, classes):
    """True when a candidate's Bug class names the Always check line (the bold name starting the line)."""
    m = re.match(r"- \*\*(.+?)\*\*", always_text)
    name = words(m.group(1)) if m else ""
    return bool(name) and any(c and (name in c or c in name) for c in map(words, classes))


def read_report(path):
    try:
        return pathlib.Path(path).read_bytes().decode("utf-8", "surrogateescape")
    except OSError:
        return None


def raw_fence(text):
    """The text unchanged in a code fence longer than any backtick run inside it."""
    ticks = "`" * max(3, max((len(r) for r in re.findall(r"`+", text)), default=0) + 1)
    return "%s\n%s%s%s" % (ticks, text, "" if text.endswith("\n") else "\n", ticks)


def build_verify(rules, a):
    rv = RoundValues(rules, a)
    spec = read_text_file(a.spec, "spec") if a.spec else None
    earlier = read_text_file(a.earlier, "earlier Findings file") if a.earlier else None
    design = read_text_file(a.design, "design answers file") if a.design else None
    rdir = pathlib.Path(a.reports)
    if not rdir.is_dir():
        raise Usage("--reports %s is not a directory" % a.reports)
    finders = [r for r in ROLES[a.level] if r != "spec" or spec is not None]
    reports, problems = {}, []
    for f in finders:
        text = read_report(rdir / (f + ".md"))
        why = "there is no report file %s.md" % f if text is None else report_problem(rules, text)
        if why:
            problems.append("%s Finder: %s" % (f, why))
        else:
            reports[f] = text
    if problems:
        raise BadReports("; ".join(problems))
    raised = [t for t in reports.values() if has_findings(rules, t)]
    if not raised and not (earlier and earlier.strip()):
        return rv.out, None
    classes = [m.group(1) for t in raised for m in re.finditer(r"^- Bug class:[ \t]*(.*)$", t, re.M)]
    lines = [text for text, _globs in rv.always if named_by(text, classes)]
    parts = [
        "# Verifier brief", rules.verifier_brief,
        "## This Round\n\nRound 1 of the review, level %s. Head: `%s`. Base: `%s`." % (a.level.capitalize(), rv.head,
                                                                                    rv.base),
        rv.diff_part, rv.important_part, rv.skip_part,
        "## The spec, the earlier open Findings and the design answers",
        "The spec:\n\n%s" % (fence(spec) if spec else "None available."),
        "Earlier open Findings and their disputes:\n\n%s" % (earlier.strip() if earlier and earlier.strip() else "None."),
        "Design answers:\n\n%s" % (design.strip() if design else "None."),
        "## Always check lines the candidates were raised from\n\n" + ("\n".join(lines) + "\n\n" + rules.record_terms
                                                                    if lines else "None."),
        "## Copy rule\n\n" + rules.copy_rule,
        rules.format,
        "## Candidates, tagged with their Finder",
    ]
    for f in finders:
        parts.append("### Report of the %s Finder\n\n%s" % (f, raw_fence(reports[f])))
    return rv.out, "\n\n".join(parts) + "\n"


def verify(args):
    rules = Rules()
    out, text = build_verify(rules, args)
    out.mkdir(parents=True, exist_ok=True)
    (out / "verifier.md").unlink(missing_ok=True)
    if text is None:
        print("no Verifier runs: every Finder reported nothing found and no earlier Finding is open; nothing written")
        return
    (out / "verifier.md").write_bytes(text.encode("utf-8", "surrogateescape"))
    print("%s\tVerifier\t%s tier" % (out / "verifier.md", rules.verifier_tiers[1 if args.level == "deep" else 0]))


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
    vf = sub.add_parser("verify", help="the Verifier brief from the Finders' reports")
    vf.add_argument("--level", required=True, type=str.lower, choices=LEVELS)
    vf.add_argument("--base", required=True)
    vf.add_argument("--head", default="HEAD")
    vf.add_argument("--repo", default=".")
    vf.add_argument("--out", required=True)
    vf.add_argument("--reports", required=True)
    vf.add_argument("--spec")
    vf.add_argument("--earlier")
    vf.add_argument("--design")
    vf.set_defaults(run=verify)
    args = p.parse_args(argv)
    try:
        if args.cmd == "round1" and args.angle is None:
            args.angle = Rules().angles[0][0]
        args.run(args)
    except Usage as e:
        print("review_briefs.py: %s" % e, file=sys.stderr)
        return 2
    except BadReports as e:
        print("review_briefs.py: ask these Finders again, nothing was written: %s" % e, file=sys.stderr)
        return 3
    except MissingSection as e:
        print("review_briefs.py: could not find %s in the skill files; nothing was written" % e, file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
