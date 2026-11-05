#!/usr/bin/env python3
"""Write the cleaned public history of dev-skills from a full clone of this repo, check it, push only main.

The user runs it on a fresh full clone of Luffytse/luffy-dev-skills on their Mac. It never changes that
clone: it makes its own clone of one branch (main by default) in --workdir and rewrites that with
git filter-repo:
  - removes the dai-portal-data plugin folder from every commit (commits left empty are dropped);
  - maps every author and committer email to the owner's GitHub no-reply address, with the name Luffytse,
    except the no-reply addresses that name no person: Anthropic's noreply@anthropic.com (Claude's
    commits and co-author lines), GitHub's noreply@github.com (web-merge committer) and any
    *@users.noreply.github.com address;
  - in commit messages and in text files: replaces each personal email with that no-reply address, each Mac
    hostname with my-mac and each dai-portal database name with example_db; deletes Claude session trailer
    lines and lines that hold only a claude.ai session or project link; turns any other such link into the
    bare https://claude.ai/code link and a bare session id into session_REMOVED; rewrites home-folder paths
    (the Users folder, a name, a slash) to ~/; replaces each --terms entry with [removed]. Every other line
    of a message is kept, Co-Authored-By lines included.
Then it runs scripts/check-public-history.py on the result's main, with the private values of the source,
and pushes main (as main, with no tag and no other branch) to --push-url only if the check passes. With
--dry-run it pushes nothing and leaves the result in --workdir to look over. It prints the commit count
before and after and lists the files at the branch tip whose content the rewrite changed, so that a rule
hitting text it should not (these scripts included) shows. git filter-repo leaves binary
files as they are, so a trace inside one fails the check and stops the push.

Where the private values come from: like the check, this file holds none. The personal emails are every
author and committer email of the source that is not a no-reply address, the hostnames are their .local
hosts, and the database names are read from the files the source's dai-portal-data folder ever held (see the
check's header); --terms adds a local file of literals that must never be committed. The rule files handed
to git filter-repo are written to a temporary folder outside both repos and deleted afterwards.

Usage:
  scripts/rewrite-public-history.py --source CLONE --workdir NEW_DIR --dry-run
  scripts/rewrite-public-history.py --source CLONE --workdir NEW_DIR --push-url URL
  options: --branch NAME (source branch to publish as main, default main), --terms FILE
Exit codes: 0 done (pushed, or dry run passed), 1 check failed or push failed (nothing pushed on a failed
check), 2 usage, setup or git error. With no arguments it prints the steps and exits 2.
"""
import argparse
import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True  # loading the check below leaves no __pycache__ in scripts/
HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("check_public_history", HERE / "check-public-history.py")
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)

OWNER_NAME = "Luffytse"
OWNER_EMAIL = "12742482+Luffytse@users.noreply.github.com"
TARGET_REPO = "Luffytse/luffy-agentic-workflow"

STEPS = f"""Steps (you run these on your Mac):
  1. On GitHub, create the PRIVATE repo {TARGET_REPO} with no initial commit
     (no README, no license, no .gitignore).
  2. Make a fresh FULL clone of this repo (not shallow) and install git filter-repo:
       git clone https://github.com/Luffytse/luffy-dev-skills.git luffy-dev-skills-source
       pip3 install git-filter-repo        (or: brew install git-filter-repo)
  3. Dry run, from that clone, into a new empty folder:
       python3 scripts/rewrite-public-history.py --source . --workdir ../public-dry --dry-run
     Read the check's result at the end: a PASS line, or FAIL lines naming each commit and what it found.
     Look the result over (git -C ../public-dry log --stat main).
  4. Real run, into another new empty folder, naming the new repo:
       python3 scripts/rewrite-public-history.py --source . --workdir ../public-push \\
         --push-url git@github.com:{TARGET_REPO}.git
     It pushes main only, and only if the check passes; on FAIL nothing is pushed.
  5. Read the check's result again and report it (PASS, or the FAIL lines) to the project thread.
     Keep the new repo private until you have looked it over on GitHub.
"""


class SetupError(Exception):
    pass


def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        raise SetupError(f"{' '.join(map(str, cmd))} failed: {(result.stderr or result.stdout).strip()}")
    return result.stdout.strip()


def git(repo, *args):
    return run(["git", "-C", str(repo), *args])


def rule(pattern, replacement):
    """One git filter-repo replace rule; patterns are Python regexes on bytes."""
    if isinstance(pattern, bytes):
        pattern = pattern.decode()
    if "\n" in pattern or "==>" in pattern or "\n" in replacement:
        raise SetupError(f"cannot write a filter-repo rule for {pattern!r}")
    return f"regex:{pattern}==>{replacement}"


def literal_rules(values, replacement):
    return [rule("(?i)" + re.escape(v), replacement) for v in sorted(values, key=lambda v: (-len(v), v)) if v]


def replace_rules(terms, extra_terms):
    """The rules for file contents and commit messages, in the order git filter-repo applies them."""
    link = "(?i:" + check.SESSION_PATTERNS[0].pattern.decode() + ")"
    rules = []
    rules += literal_rules(terms["personal email"], OWNER_EMAIL)
    rules += literal_rules(terms["hostname"], "my-mac")
    rules += literal_rules(terms["private term"], "example_db")
    rules += literal_rules(extra_terms, "[removed]")
    rules.append(rule(r"(?m)^[ \t]*(?:https?://)?" + link + r"[ \t]*(?:\r?\n|\Z)", ""))
    rules.append(rule(r"(?mi)^[ \t]*claude-session[ \t]*:[^\n]*(?:\n|\Z)", ""))
    rules.append(rule(r"(?:https?://)?" + link, "https://claude.ai/code"))
    rules.append(rule(check.SESSION_PATTERNS[1].pattern, "session_REMOVED"))
    rules.append(rule(check.HOME_PATTERN.pattern, "~/"))
    return rules


def mailmap(emails):
    return "".join(f"{OWNER_NAME} <{OWNER_EMAIL}> <{e}>\n" for e in sorted(emails))


def prepare(args):
    source = pathlib.Path(args.source).resolve()
    work = pathlib.Path(args.workdir).resolve()
    if work.exists() and (not work.is_dir() or any(work.iterdir())):
        raise SetupError(f"--workdir {work} must be a new or empty folder")
    if git(source, "rev-parse", "--is-shallow-repository") != "false":
        raise SetupError(f"{source} is a shallow clone; make a full clone (git clone without --depth)")
    git(source, "rev-parse", "--verify", "--quiet", f"refs/heads/{args.branch}^{{commit}}")
    if subprocess.run(["git", "filter-repo", "--version"], capture_output=True).returncode != 0:
        raise SetupError("git filter-repo is not installed (pip3 install git-filter-repo)")
    if work == source or source in work.parents:
        raise SetupError("--workdir must be outside the source clone")
    return source, work


def rewrite(source, work, branch, extra_terms):
    terms = check.derive_terms(source)
    print(f"Private values found in the source: {len(terms['personal email'])} personal emails, "
          f"{len(terms['hostname'])} hostnames, {len(terms['private term'])} database names, "
          f"{len(extra_terms)} terms from --terms (values not printed).")
    git(source.parent, "clone", "--quiet", "--no-local", "--single-branch", "--no-tags", "--branch", branch,
        str(source), str(work))
    rules = "".join(r + "\n" for r in replace_rules(terms, extra_terms))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "mailmap").write_text(mailmap(terms["personal email"]))
        (tmp / "rules").write_text(rules)
        cmd = ["git", "-C", str(work), "filter-repo", "--invert-paths", "--path", check.PLUGIN_DIR,
               "--mailmap", str(tmp / "mailmap"), "--replace-text", str(tmp / "rules"),
               "--replace-message", str(tmp / "rules")]
        print("Running git filter-repo in", work)
        run(cmd)
    for ref in git(work, "for-each-ref", "--format=%(refname)").splitlines():
        if ref != f"refs/heads/{branch}":
            git(work, "update-ref", "-d", ref)
    if branch != "main":
        git(work, "branch", "-M", branch, "main")
    git(work, "symbolic-ref", "HEAD", "refs/heads/main")


def tip_changes(source, branch, work):
    """Paths at the branch tip whose content the rewrite changed (the plugin folder's removal aside)."""
    def tree(repo, ref):
        rows = git(repo, "-c", "core.quotePath=false", "ls-tree", "-r", ref).splitlines()
        return {row.split("\t", 1)[1]: row.split()[2] for row in rows}
    before, after = tree(source, f"refs/heads/{branch}"), tree(work, "refs/heads/main")
    return sorted(p for p, sha in before.items() if not p.startswith(check.PLUGIN_DIR) and after.get(p) != sha)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    print(STEPS)
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--source", required=True, help="the fresh full clone (left unchanged)")
    parser.add_argument("--workdir", required=True, help="a new empty folder for the rewritten repo")
    parser.add_argument("--branch", default="main", help="the source branch to publish as main")
    parser.add_argument("--terms", help="a local file of extra private terms, one per line (never commit it)")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="rewrite and check, push nothing")
    mode.add_argument("--push-url", help="the new repo's URL; main is pushed there if the check passes")
    if not argv:
        parser.print_usage()
        return 2
    args = parser.parse_args(argv)
    try:
        source, work = prepare(args)
        extra = check.read_terms_file(args.terms) if args.terms else set()
        before = int(git(source, "rev-list", "--count", f"refs/heads/{args.branch}"))
        rewrite(source, work, args.branch, extra)
        after = int(git(work, "rev-list", "--count", "refs/heads/main"))
        changed = tip_changes(source, args.branch, work)
        findings, commits, blobs = check.check(work, ["refs/heads/main"], [source], args.terms)
    except (SetupError, check.GitError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(f"commits on main: {before} before, {after} after")
    print(f"files at the tip that the rewrite changed: {len(changed)}")
    for path in changed:
        print("  " + path)
    print("Pre-publish check of the result's main:")
    for commit, where, kind, detail in findings[:check.MAX_LINES]:
        print(f"FAIL {commit} {where}: {kind}: {detail}")
    if findings:
        print(f"FAIL: {len(findings)} findings; not pushed. The result is in {work}.")
        return 1
    print(f"PASS: checked {commits} commits, {blobs} blobs; no private trace found")
    if args.dry_run:
        print(f"DRY RUN: nothing pushed. The result is in {work}.")
        return 0
    result = subprocess.run(["git", "-C", str(work), "-c", "push.followTags=false", "push", "--no-tags",
                             args.push_url, "refs/heads/main:refs/heads/main"], text=True, capture_output=True)
    print(result.stdout + result.stderr, end="")
    if result.returncode != 0:
        print("FAIL: the push failed; see git's message above.")
        return 1
    print(f"Pushed main (only) to {args.push_url}. Keep the repo private until you have looked it over.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
