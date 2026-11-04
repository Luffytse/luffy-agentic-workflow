#!/usr/bin/env python3
"""Tests of the review-rounds brief script (review_briefs.py round1) as a command, on scratch git repos.

Run: python3 evals/review-briefs/test_review_briefs.py
Each test builds a scratch repo with a planted change, writes the inputs to files, runs the script and reads the briefs
back. What a brief must hold is read from the skill files the same way the script reads them (a section cut out, a
quoted brief), never from a sentence of the skill's wording, so rewording a skill never fails a test. No agent runs.
"""
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

SKILLS = pathlib.Path(__file__).resolve().parents[2] / "plugins/dev-skills/skills"
REVIEW_ROUNDS = SKILLS / "review-rounds"
SCRIPT_NAME = "review_briefs.py"

REVIEW_MD = """\
# Review rules

## Important

PLANTED-IMPORTANT: a change is Important when the planted rule says so.

## Skip

- **planted skip entry**: PLANTED-SKIP text.

## Always check

Each line names the files it applies to.

- **py line** (files: `*.py`; from #1): PLANTED-PY check for python files.
- **sh line** (files: `*.sh`; from #2): PLANTED-SH check for shell scripts.
- **docs line** (files: `docs/*`; from #3): PLANTED-DOCS check for docs.
- **any line**: PLANTED-ANY check that names no kinds of file.
"""


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, text=True, capture_output=True).stdout


# ---- reading the skill files the way a reader would (independent of the script) ----

def sections_of(text):
    """Yield (level, heading line, body lines) for each heading, a line inside a code fence never being a heading."""
    out, fence = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        m = None if fence or line.startswith("```") else re.match(r"^(#+) ", line)
        if m:
            out.append([len(m.group(1)), line, [line]])
        elif out:
            out[-1][2].append(line)
    return out


def cut(text, prefix):
    """The heading starting with prefix and everything under it up to the next heading of the same or a higher level."""
    secs = sections_of(text)
    for i, (lvl, head, _body) in enumerate(secs):
        if head.startswith(prefix):
            lines = list(secs[i][2])
            for lvl2, _h, body2 in secs[i + 1:]:
                if lvl2 <= lvl:
                    break
                lines += body2
            return "\n".join(lines).rstrip("\n")
    raise AssertionError("no heading " + prefix)


def quoted(text, label):
    m = re.search(r"^" + re.escape(label) + r': "(.*?)"$', text, re.S | re.M)
    assert m, label
    return m.group(1)


FINDERS = (REVIEW_ROUNDS / "FINDERS.md").read_text()
DEEP = (REVIEW_ROUNDS / "DEEP.md").read_text()
SKILL = (REVIEW_ROUNDS / "SKILL.md").read_text()
SHARED = quoted(FINDERS, "Shared brief")
COPY = quoted(FINDERS, "Copy rule")
FORMAT = cut(FINDERS, "## Finding format")
SMELL = cut(FINDERS, "### Smell baseline")
DRIFT = cut(FINDERS, "### Docs index drift")
STANDARDS_BRIEF = quoted(cut(FINDERS, "## Standards Finder"), "Brief")
SPEC_BRIEF = quoted(cut(FINDERS, "## Spec Finder"), "Brief")
ADV_BRIEF = quoted(cut(FINDERS, "## Adversarial Finder"), "Brief")
SECURITY_BRIEF = quoted(cut(DEEP, "## Security Finder"), "Brief")
EARLIER_LINE = re.search(r'^The standards, spec and later-Round Finders also get .*? with: "(.*)"$', FINDERS, re.M).group(1)
IMPORTANT_DEFAULT = re.search(r"Without it, (\*\*Important\*\* means.*)$", SKILL, re.M).group(1)
RECORD_TERMS = cut((SKILLS / "review-record/SKILL.md").read_text(), "## Terminology")
INDEX_CONTRACT = (SKILLS / "docs-index/SKILL.md").read_text().split("\n---\n", 1)[1].strip()
ANGLES = re.findall(r"^- \*\*(.+?)\*\*: ", cut(FINDERS, "## Adversarial Finder").split("Angles:", 1)[1], re.M)


def table_rows():
    rows = {}
    for line in cut(SKILL, "## Who runs").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0].startswith("Round 1,"):
            rows[cells[0].split(",")[1].strip().lower()] = cells[1]
    return rows


def table_finders(level):
    """The Finder files the skill's table names for Round 1 at a level (Deep says 'Standard's three, plus ...')."""
    rows, cell, names = table_rows(), table_rows()[level], set()
    if "Standard's three" in cell:
        names |= table_finders("standard")
    for word in ("standards", "spec", "adversarial", "security"):
        if re.search(r"\b" + word + r"\b", cell):
            names.add(word)
    return names


def tier_of(heading_prefix, text):
    head = next(h for _l, h, _b in sections_of(text) if h.startswith(heading_prefix))
    return re.search(r"\((cheap|regular|premium)\b", head).group(1)


class Scratch:
    """A scratch repo: branch main with a base commit, branch feature with the planted change."""

    def __init__(self, root, review=REVIEW_MD, index=True, boundary=True, change="code"):
        self.root = pathlib.Path(root)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.name", "t")
        git(self.repo, "config", "user.email", "t@example.invalid")
        self.write("README.md", "readme\n")
        self.write("src/app.py", "def f():\n    return 1\n")
        if review is not None:
            self.write("REVIEW.md", review)
        if index:
            self.write("docs/dev-skills/index.md", "# Index\n")
        if boundary:
            self.write("docs/dev-skills/boundaries.md", "# Boundary record\n\nPLANTED-BOUNDARY: nothing ships on Friday.\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "base")
        git(self.repo, "switch", "-q", "-c", "feature")
        if change == "code":
            self.write("src/app.py", "def f():\n    return 2\n")
        self.write("docs/note.md", "a note\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "planted change")
        self.out = self.root / "out"
        self.spec = self.write_at(self.root / "spec.md", "PLANTED-SPEC: split the bill evenly.\n")
        self.standards = self.write_at(self.root / "standards.txt", "CLAUDE.md\n")
        self.write("CLAUDE.md", "PLANTED-STANDARD: name things well.\n")  # untracked, like a standards file the thread found
        self.earlier = self.write_at(self.root / "earlier.md", "PLANTED-EARLIER: R1-1 open, src/app.py:2.\n")
        self.design = self.write_at(self.root / "design.md", "PLANTED-DESIGN: keep the even split.\n")

    def write(self, rel, text):
        return self.write_at(self.repo / rel, text)

    def write_at(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def run(self, level, *extra, script=None, with_inputs=True, env=None, out=None):
        args = [sys.executable, "-B", str(script or REVIEW_ROUNDS / SCRIPT_NAME), "round1", "--level", level,
                "--repo", str(self.repo), "--base", "main", "--out", str(out or self.out)]
        if with_inputs:
            args += ["--spec", str(self.spec), "--standards", str(self.standards),
                     "--earlier", str(self.earlier), "--design", str(self.design)]
        return subprocess.run(args + list(extra), text=True, capture_output=True, env=env)

    def brief(self, name):
        return (self.out / name).read_text()

    def files(self):
        return sorted(p.name for p in self.out.iterdir()) if self.out.exists() else []


class Base(unittest.TestCase):
    def scratch(self, **kw):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Scratch(tmp.name, **kw)

    def ok(self, r):
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class WhoRuns(Base):
    def test_files_written_are_the_finders_the_table_names_at_each_level(self):
        for level in ("quick", "standard", "deep"):
            with self.subTest(level=level):
                s = self.scratch()
                self.ok(s.run(level))
                self.assertEqual(s.files(), sorted("finder-%s.md" % n for n in table_finders(level)))

    def test_no_spec_writes_no_spec_finder(self):
        s = self.scratch()
        r = subprocess.run([sys.executable, "-B", str(REVIEW_ROUNDS / SCRIPT_NAME), "round1", "--level", "standard",
                            "--repo", str(s.repo), "--base", "main", "--out", str(s.out)], text=True, capture_output=True)
        self.ok(r)
        self.assertNotIn("finder-spec.md", s.files())
        self.assertEqual(s.files(), sorted("finder-%s.md" % n for n in table_finders("standard") - {"spec"}))

    def test_printed_list_names_each_file_role_and_tier(self):
        s = self.scratch()
        r = s.run("deep")
        self.ok(r)
        tiers = {"standards": tier_of("## Standards Finder", FINDERS), "spec": tier_of("## Spec Finder", FINDERS),
                 "adversarial": tier_of("## Adversarial Finder", FINDERS), "security": tier_of("## Security Finder", DEEP)}
        for role, tier in tiers.items():
            line = next(l for l in r.stdout.splitlines() if "finder-%s.md" % role in l)
            self.assertIn(role, line)
            self.assertIn(tier, line)


class Contents(Base):
    def test_every_finder_has_the_common_sections_and_round_values(self):
        s = self.scratch()
        self.ok(s.run("deep"))
        head = git(s.repo, "rev-parse", "feature").strip()
        for name in s.files():
            with self.subTest(file=name):
                t = s.brief(name)
                for part in (SHARED, COPY, FORMAT):
                    self.assertIn(part, t)
                self.assertIn("PLANTED-IMPORTANT", t)
                self.assertIn("PLANTED-SKIP", t)
                self.assertIn("PLANTED-BOUNDARY", t)
                self.assertIn(head, t)
                self.assertIn("planted change", t)  # the commit list
                self.assertRegex(t, r"git -C \S+ diff \S*main\S*feature|git -C \S+ diff \S*main\S*" + head[:7])

    def test_standards_finder(self):
        s = self.scratch()
        self.ok(s.run("quick"))
        t = s.brief("finder-standards.md")
        for part in (STANDARDS_BRIEF, EARLIER_LINE, RECORD_TERMS, SMELL, DRIFT, INDEX_CONTRACT):
            self.assertIn(part, t)
        for marker in ("PLANTED-SPEC", "PLANTED-STANDARD", "PLANTED-EARLIER", "PLANTED-DESIGN"):
            self.assertIn(marker, t)

    def test_spec_finder(self):
        s = self.scratch()
        self.ok(s.run("quick"))
        t = s.brief("finder-spec.md")
        for part in (SPEC_BRIEF, EARLIER_LINE):
            self.assertIn(part, t)
        for marker in ("PLANTED-SPEC", "PLANTED-EARLIER", "PLANTED-DESIGN"):
            self.assertIn(marker, t)
        for gone in (SMELL, DRIFT, "PLANTED-PY", "PLANTED-STANDARD", RECORD_TERMS):
            self.assertNotIn(gone, t)

    def test_adversarial_finder_gets_no_standards_inputs(self):
        s = self.scratch()
        self.ok(s.run("standard"))
        t = s.brief("finder-adversarial.md")
        self.assertIn(ADV_BRIEF.split("<angle>")[0], t)
        for gone in ("PLANTED-PY", "PLANTED-ANY", "PLANTED-STANDARD", "PLANTED-SPEC", "PLANTED-EARLIER", SMELL, DRIFT,
                     RECORD_TERMS, EARLIER_LINE):
            self.assertNotIn(gone, t)

    def test_security_finder_is_built_from_the_deep_file_and_gets_the_spec(self):
        s = self.scratch()
        self.ok(s.run("deep"))
        t = s.brief("finder-security.md")
        self.assertIn(SECURITY_BRIEF, t)
        self.assertIn("PLANTED-SPEC", t)
        for gone in ("PLANTED-PY", "PLANTED-STANDARD", SMELL):
            self.assertNotIn(gone, t)


class AlwaysCheck(Base):
    def test_lines_included_only_when_their_kinds_match_a_changed_file(self):
        s = self.scratch()
        self.ok(s.run("quick"))
        t = s.brief("finder-standards.md")
        self.assertIn("PLANTED-PY", t)       # src/app.py changed
        self.assertIn("PLANTED-DOCS", t)     # docs/note.md changed
        self.assertNotIn("PLANTED-SH", t)    # no shell script changed
        self.assertIn("PLANTED-ANY", t)      # a line naming no kinds is always included

    def test_a_line_matching_nothing_is_left_out_and_a_kindless_line_stays(self):
        s = self.scratch(change="docs")
        self.ok(s.run("quick"))
        t = s.brief("finder-standards.md")
        self.assertNotIn("PLANTED-PY", t)
        self.assertIn("PLANTED-ANY", t)


class Conditionals(Base):
    def test_smell_baseline_only_when_code_changed(self):
        code = self.scratch()
        self.ok(code.run("quick"))
        self.assertIn(SMELL, code.brief("finder-standards.md"))
        docs = self.scratch(change="docs")
        self.ok(docs.run("quick"))
        self.assertNotIn(SMELL, docs.brief("finder-standards.md"))

    def test_items_the_skill_says_to_drop_are_dropped_from_the_standards_brief(self):
        items = lambda text: dict(re.findall(r"\(([a-d])\) ([^;]*?)(?:;|\.(?: |$))", text))
        full = items(STANDARDS_BRIEF)
        self.assertEqual(sorted(full), list("abcd"))
        s = self.scratch(change="docs", review=None, index=False)
        self.ok(s.run("quick"))
        t = s.brief("finder-standards.md")
        self.assertIn(full["a"], t)
        for letter in "bcd":  # no code, no Always check lines, no docs index
            self.assertNotIn(full[letter], t)
        self.assertNotIn(STANDARDS_BRIEF, t)

    def test_docs_index_check_only_when_the_repo_has_an_index(self):
        s = self.scratch(index=False)
        self.ok(s.run("quick"))
        t = s.brief("finder-standards.md")
        self.assertNotIn(DRIFT, t)
        self.assertNotIn(INDEX_CONTRACT, t)

    def test_defaults_without_review_boundary_and_index(self):
        s = self.scratch(review=None, index=False, boundary=False)
        self.ok(s.run("deep"))
        self.assertEqual(s.files(), sorted("finder-%s.md" % n for n in table_finders("deep")))
        for name in s.files():
            t = s.brief(name)
            self.assertIn(IMPORTANT_DEFAULT, t)
            self.assertNotIn("PLANTED", t.replace("PLANTED-SPEC", "").replace("PLANTED-STANDARD", "")
                             .replace("PLANTED-EARLIER", "").replace("PLANTED-DESIGN", ""))
        self.assertNotIn("Always check line", s.brief("finder-adversarial.md"))


class Angles(Base):
    def test_default_angle_is_the_first_of_the_skill_list_by_name(self):
        s = self.scratch()
        self.ok(s.run("standard"))
        self.assertIn(ANGLES[0].lower(), s.brief("finder-adversarial.md").lower())

    def test_every_angle_in_the_skill_list_is_written_in_by_name(self):
        for angle in ANGLES:
            with self.subTest(angle=angle):
                s = self.scratch()
                self.ok(s.run("standard", "--angle", angle.upper()))
                t = s.brief("finder-adversarial.md")
                self.assertIn(angle.lower(), t.lower())
                self.assertNotIn("<angle>", t)
                other = next(a for a in ANGLES if a != angle)
                self.assertNotIn("**%s**" % other, t)

    def test_unknown_angle_stops_with_a_message(self):
        s = self.scratch()
        r = s.run("standard", "--angle", "no such angle")
        self.assertEqual(r.returncode, 2)
        self.assertIn("no such angle", r.stderr)
        self.assertEqual(s.files(), [])


class Nits(Base):
    def test_non_ascii_changed_file_counts_for_globs_and_code(self):
        s = self.scratch(review=REVIEW_MD.replace("`*.py`", "`caf*.py`"), change="docs")
        s.write("caf\u00e9.py", "x = 1\n")
        git(s.repo, "add", "-A")
        git(s.repo, "commit", "-q", "-m", "non-ascii file")
        self.ok(s.run("quick"))
        t = s.brief("finder-standards.md")
        self.assertIn("PLANTED-PY", t)
        self.assertIn(SMELL, t)

    def test_unknown_angle_is_refused_at_quick_too(self):
        s = self.scratch()
        r = s.run("quick", "--angle", "no such angle")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(s.files(), [])

    def test_a_fenced_block_in_the_spec_does_not_break_the_fencing(self):
        s = self.scratch()
        s.write_at(s.spec, "PLANTED-SPEC\n```\ncode\n```\n````\nfour\n````\n")
        self.ok(s.run("quick"))
        t = s.brief("finder-spec.md")
        m = re.search(r"^(`{3,})\nPLANTED-SPEC\n.*?\n\1$", t, re.S | re.M)
        self.assertIsNotNone(m)
        self.assertGreater(len(m.group(1)), 4)

    def test_review_md_that_refers_to_the_default_gets_the_default_text_too(self):
        refers = REVIEW_MD.replace("PLANTED-IMPORTANT: a change is Important when the planted rule says so.",
                                   "PLANTED-IMPORTANT: the default meaning of Important applies, with one sentence added.")
        s = self.scratch(review=refers)
        self.ok(s.run("quick"))
        self.assertIn(IMPORTANT_DEFAULT, s.brief("finder-spec.md"))
        s2 = self.scratch()
        self.ok(s2.run("quick"))
        self.assertNotIn(IMPORTANT_DEFAULT, s2.brief("finder-spec.md"))


class Failures(Base):
    def skill_copy(self, s):
        dest = pathlib.Path(s.root) / "skills"
        for name in ("review-rounds", "review-record", "docs-index"):
            shutil.copytree(SKILLS / name, dest / name)
        return dest

    def test_a_missing_section_stops_with_its_name_and_exit_3(self):
        cases = [
            ("review-rounds/FINDERS.md", "## Finding format", "## Format of findings", "Finding format"),
            ("review-rounds/FINDERS.md", "### Smell baseline", "### Smells", "Smell baseline"),
            ("review-rounds/FINDERS.md", "### Docs index drift", "### Drift", "Docs index drift"),
            ("review-rounds/FINDERS.md", "Shared brief:", "Common brief:", "Shared brief"),
            ("review-rounds/FINDERS.md", "Copy rule:", "Read rule:", "Copy rule"),
            ("review-rounds/DEEP.md", "## Security Finder", "## Guard Finder", "Security Finder"),
        ]
        for rel, old, new, name in cases:
            with self.subTest(section=name):
                s = self.scratch()
                skills = self.skill_copy(s)
                f = skills / rel
                text = f.read_text()
                self.assertIn(old, text)
                f.write_text(text.replace(old, new))
                r = s.run("deep", script=skills / "review-rounds" / SCRIPT_NAME)
                self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
                self.assertIn(name.lower(), r.stderr.lower())
                self.assertEqual(s.files(), [])

    def test_usage_errors_exit_2(self):
        s = self.scratch()
        for extra in (["--level", "mega"],):
            r = subprocess.run([sys.executable, "-B", str(REVIEW_ROUNDS / SCRIPT_NAME), "round1", "--repo", str(s.repo),
                                "--base", "main", "--out", str(s.out)] + extra, text=True, capture_output=True)
            self.assertEqual(r.returncode, 2)
        r = subprocess.run([sys.executable, "-B", str(REVIEW_ROUNDS / SCRIPT_NAME)], text=True, capture_output=True)
        self.assertEqual(r.returncode, 2)
        r = s.run("quick", "--spec", str(s.root / "missing.md"))
        self.assertEqual(r.returncode, 2)

    def test_an_output_directory_inside_the_work_tree_is_refused(self):
        s = self.scratch()
        r = s.run("quick", out=s.repo / "briefs")
        self.assertEqual(r.returncode, 2)
        self.assertFalse((s.repo / "briefs").exists())

    def test_a_rerun_at_a_lower_level_leaves_no_stale_finder(self):
        s = self.scratch()
        self.ok(s.run("deep"))
        self.ok(s.run("quick"))
        self.assertEqual(s.files(), sorted("finder-%s.md" % n for n in table_finders("quick")))


class Boundaries(Base):
    def test_only_git_is_called(self):
        s = self.scratch()
        bin_dir = pathlib.Path(s.root) / "bin"
        bin_dir.mkdir()
        (bin_dir / "git").symlink_to(shutil.which("git"))
        env = {"PATH": str(bin_dir), "HOME": str(s.root), "GIT_CONFIG_NOSYSTEM": "1"}
        r = s.run("deep", env=env)
        self.ok(r)

    def test_writes_nothing_outside_the_output_directory(self):
        s = self.scratch()
        before = {p: p.stat().st_mtime_ns for p in s.root.rglob("*") if p.is_file() and ".git/" not in str(p)}
        status = git(s.repo, "status", "--porcelain")
        self.ok(s.run("deep"))
        after = {p: p.stat().st_mtime_ns for p in s.root.rglob("*") if p.is_file() and ".git/" not in str(p)
                 and s.out not in p.parents}
        self.assertEqual(before, after)
        self.assertEqual(status, git(s.repo, "status", "--porcelain"))

    def test_script_names_no_tracker_command_or_host_api(self):
        text = (REVIEW_ROUNDS / SCRIPT_NAME).read_text().lower()
        for word in ("gh ", "api.github", "gitlab", "urllib", "http.client", "socket"):
            self.assertNotIn(word, text)


# ---- the Verifier brief (review_briefs.py verify) ----

FORMAT_FIELDS = re.findall(r"^- ([^:(]+?)(?: \([^)]*\))?:", FORMAT, re.M)
VERIFIER_BRIEF = quoted(VERIFY := (REVIEW_ROUNDS / "VERIFY.md").read_text(), "Brief")
VERIFIER_TIERS = re.search(r"on the (cheap|regular|premium) tier \((cheap|regular|premium) at Deep\)", VERIFY).groups()


def finding(title, bug_class, n_locations=3, marker="X"):
    """A Finding in the Finding format, its fields taken from the skill's format block, with several Locations."""
    values = {"Bug class": bug_class,
              "Locations": ", ".join("src/app.py:%d" % (i + 1) for i in range(n_locations))}
    lines = ["### " + title]
    for f in FORMAT_FIELDS:
        lines.append("- %s: %s" % (f, values.get(f, "%s-%s value" % (marker, f))))
    return "\n".join(lines) + "\n"


class VerifierBrief(Base):
    def verify(self, s, reports, *extra, level="standard", script=None, spec=True, earlier=False):
        """Write reports (finder -> text or bytes or None for none) to a dir and run the verify subcommand."""
        rdir = s.root / "reports"
        rdir.mkdir(exist_ok=True)
        for old in rdir.iterdir():
            old.unlink()
        for name, text in reports.items():
            if text is None:
                continue
            (rdir / ("%s.md" % name)).write_bytes(text if isinstance(text, bytes) else text.encode())
        args = [sys.executable, "-B", str(script or REVIEW_ROUNDS / SCRIPT_NAME), "verify", "--level", level,
                "--repo", str(s.repo), "--base", "main", "--out", str(s.out), "--reports", str(rdir),
                "--design", str(s.design)]
        if spec:
            args += ["--spec", str(s.spec)]
        if earlier:
            args += ["--earlier", str(s.earlier)]
        return subprocess.run(args + list(extra), text=True, capture_output=True)

    def all_clear(self, level="standard", spec=True):
        names = [n for n in table_finders(level) if spec or n != "spec"]
        return {n: "Nothing found.\n" for n in names}

    def test_a_report_with_several_findings_and_locations_is_carried_over_byte_for_byte(self):
        s = self.scratch()
        std = finding("First", "unescaped input", 4) + "\n" + finding("Second", "missing test", 3) + "\n"
        # odd bytes on purpose: CRLF, trailing spaces, a non-ascii character, no final newline
        adv = (finding("Third", "off by one", 5).replace("\n", "\r\n").rstrip() + " \u00e9  ").encode()
        reports = {"standards": std, "spec": "Nothing found.\n", "adversarial": adv}
        r = self.verify(s, reports)
        self.ok(r)
        t = (s.out / "verifier.md").read_bytes()
        self.assertIn(std.encode(), t)
        self.assertIn(adv, t)
        text = t.decode()
        for name in ("standards", "adversarial"):  # each report sits under a heading naming its Finder
            m = re.search(r"^#+ .*\b%s\b.*$" % name, text, re.M | re.I)
            self.assertIsNotNone(m, name)
        self.assertLess(text.index(std), text.index(adv.decode()))
        self.assertEqual(s.files(), ["verifier.md"])

    def test_brief_holds_the_verifier_brief_copy_rule_format_and_round_values(self):
        s = self.scratch()
        reports = self.all_clear()
        reports["standards"] = finding("First", "unescaped input")
        self.ok(self.verify(s, reports, earlier=True))
        t = (s.out / "verifier.md").read_text()
        head = git(s.repo, "rev-parse", "feature").strip()
        for part in (VERIFIER_BRIEF, COPY, FORMAT):
            self.assertIn(part, t)
        for marker in ("PLANTED-IMPORTANT", "PLANTED-SKIP", "PLANTED-SPEC", "PLANTED-DESIGN", "PLANTED-EARLIER", head,
                       "planted change"):
            self.assertIn(marker, t)

    def test_printed_list_gives_the_verifier_tier_premium_at_deep(self):
        for level, want in (("quick", VERIFIER_TIERS[0]), ("standard", VERIFIER_TIERS[0]), ("deep", VERIFIER_TIERS[1])):
            with self.subTest(level=level):
                s = self.scratch()
                reports = self.all_clear(level)
                reports["standards"] = finding("First", "unescaped input")
                r = self.verify(s, reports, level=level)
                self.ok(r)
                line = next(l for l in r.stdout.splitlines() if "verifier.md" in l)
                self.assertIn("Verifier", line)
                self.assertIn(want, line)

    def test_missing_empty_and_off_format_reports_each_stop_and_are_all_named(self):
        bad = {"missing": None, "empty": "", "blank": "  \n\n", "prose": "Looks fine to me, no problems.\n",
               "partial": "### A title\n- Severity (proposed): Nit\n", "no-heading": "- Bug class: x\n- Locations: a:1\n"}
        for kind, text in bad.items():
            with self.subTest(kind=kind):
                s = self.scratch()
                reports = self.all_clear("deep")
                reports["adversarial"] = text
                r = self.verify(s, reports, level="deep")
                self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
                self.assertIn("adversarial", r.stderr)
                for ok in ("standards", "spec", "security"):
                    self.assertNotIn(ok, r.stderr)
                self.assertEqual(s.files(), [])
        s = self.scratch()
        reports = self.all_clear("deep")
        reports.update({"standards": None, "spec": "", "security": "prose only\n"})
        r = self.verify(s, reports, level="deep")
        self.assertEqual(r.returncode, 3)
        for name in ("standards", "spec", "security"):
            self.assertIn(name, r.stderr)
        self.assertNotIn("adversarial", r.stderr)
        self.assertEqual(s.files(), [])

    def test_a_good_report_next_to_one_bad_report_writes_nothing(self):
        s = self.scratch()
        reports = self.all_clear()
        reports["standards"] = finding("First", "unescaped input")
        reports["spec"] = ""
        self.assertEqual(self.verify(s, reports).returncode, 3)
        self.assertEqual(s.files(), [])

    def test_a_finding_missing_a_field_of_the_format_is_off_format(self):
        for field in FORMAT_FIELDS:
            with self.subTest(field=field):
                s = self.scratch()
                text = re.sub(r"^- %s.*\n" % re.escape(field), "", finding("First", "x"), flags=re.M)
                reports = self.all_clear()
                reports["standards"] = text
                r = self.verify(s, reports)
                self.assertEqual(r.returncode, 3)
                self.assertIn("standards", r.stderr)

    def test_nothing_found_in_every_report_and_no_earlier_finding_writes_no_verifier_brief(self):
        s = self.scratch()
        s.out.mkdir()
        (s.out / "verifier.md").write_text("stale")
        r = self.verify(s, self.all_clear())
        self.ok(r)
        self.assertEqual(s.files(), [])
        self.assertRegex(r.stdout.lower(), r"no verifier")

    def test_nothing_found_still_gets_a_verifier_when_an_earlier_finding_is_open(self):
        s = self.scratch()
        r = self.verify(s, self.all_clear(), earlier=True)
        self.ok(r)
        t = (s.out / "verifier.md").read_text()
        self.assertIn("PLANTED-EARLIER", t)
        self.assertIn("verifier.md", r.stdout)

    def test_always_check_lines_only_for_the_bug_class_a_candidate_names(self):
        s = self.scratch()
        reports = self.all_clear()
        reports["standards"] = finding("A py thing", "py line")  # names the REVIEW.md line "py line"
        self.ok(self.verify(s, reports))
        t = (s.out / "verifier.md").read_text()
        self.assertIn("PLANTED-PY", t)
        for gone in ("PLANTED-SH", "PLANTED-DOCS", "PLANTED-ANY"):  # even lines that fit the changed files stay out
            self.assertNotIn(gone, t)
        self.assertIn(RECORD_TERMS, t)

    def test_no_always_check_line_when_no_candidate_names_one(self):
        s = self.scratch()
        reports = self.all_clear()
        reports["adversarial"] = finding("Something", "unrelated kind of problem")
        self.ok(self.verify(s, reports))
        t = (s.out / "verifier.md").read_text()
        for gone in ("PLANTED-PY", "PLANTED-SH", "PLANTED-DOCS", "PLANTED-ANY", RECORD_TERMS):
            self.assertNotIn(gone, t)

    def test_two_candidates_name_two_lines(self):
        s = self.scratch()
        reports = self.all_clear()
        reports["standards"] = finding("One", "Py Line") + "\n" + finding("Two", "the sh line broke")
        self.ok(self.verify(s, reports))
        t = (s.out / "verifier.md").read_text()
        self.assertIn("PLANTED-PY", t)
        self.assertIn("PLANTED-SH", t)
        self.assertNotIn("PLANTED-DOCS", t)

    def test_heading_inside_a_code_fence_is_not_a_finding(self):
        s = self.scratch()
        reports = self.all_clear()
        reports["standards"] = "Nothing found.\n\n```\n### example\n```\n"
        self.ok(self.verify(s, reports))

    def test_no_spec_means_no_spec_finder_is_expected(self):
        s = self.scratch()
        reports = self.all_clear(spec=False)
        reports["standards"] = finding("One", "x")
        self.ok(self.verify(s, reports, spec=False))
        self.assertEqual(s.files(), ["verifier.md"])

    def test_a_missing_verifier_section_stops_with_its_name_and_exit_3(self):
        s = self.scratch()
        skills = pathlib.Path(s.root) / "skills"
        for name in ("review-rounds", "review-record", "docs-index"):
            shutil.copytree(SKILLS / name, skills / name)
        f = skills / "review-rounds/VERIFY.md"
        f.write_text(f.read_text().replace("Brief:", "Text:"))
        reports = self.all_clear()
        reports["standards"] = finding("One", "x")
        r = self.verify(s, reports, script=skills / "review-rounds" / SCRIPT_NAME)
        self.assertEqual(r.returncode, 3)
        self.assertIn("verifier", r.stderr.lower())
        self.assertEqual(s.files(), [])

    def test_usage_errors_and_an_output_directory_in_the_work_tree(self):
        s = self.scratch()
        reports = self.all_clear()
        reports["standards"] = finding("One", "x")
        self.assertEqual(self.verify(s, reports, "--level", "mega").returncode, 2)
        s2 = self.scratch()
        r = subprocess.run([sys.executable, "-B", str(REVIEW_ROUNDS / SCRIPT_NAME), "verify", "--level", "quick",
                            "--repo", str(s2.repo), "--base", "main", "--out", str(s2.repo / "b"),
                            "--reports", str(s2.root)], text=True, capture_output=True)
        self.assertEqual(r.returncode, 2)
        r = subprocess.run([sys.executable, "-B", str(REVIEW_ROUNDS / SCRIPT_NAME), "verify", "--level", "quick",
                            "--repo", str(s2.repo), "--base", "main", "--out", str(s2.out)], text=True, capture_output=True)
        self.assertEqual(r.returncode, 2)  # --reports is required


if __name__ == "__main__":
    unittest.main()
