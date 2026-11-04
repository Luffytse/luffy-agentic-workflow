#!/usr/bin/env python3
"""Score a release doc that a setup-dev-skills run wrote (Section E), by its fields, not its wording.

Usage: score_release_doc.py <release-doc> <none|pull-requests-bump|releases-bump>

Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any check fails.
See evals/setup-dev-skills/README.md, case 2.
"""
import re
import sys

POLICIES = {"none": "none", "pull-requests-bump": "pull requests bump", "releases-bump": "Releases bump"}
results = []


def check(name, ok, seen=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("" if ok or not seen else f": {seen}"))


def field(text, name):
    m = re.search(rf"^- \*\*{re.escape(name)}\*\*:(.*(?:\n(?!- \*\*|#).*)*)", text, re.M)
    return m.group(1).strip() if m else None


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in POLICIES:
        sys.exit(__doc__)
    text, policy = open(sys.argv[1], encoding="utf-8").read(), sys.argv[2]
    low = text.lower()

    pol = field(text, "Versioning policy")
    check("versioning policy field names the chosen policy", pol is not None and POLICIES[policy].lower() in pol.lower(), pol)
    other_heads = [v for k, v in POLICIES.items() if k != policy]
    check("the other policies' text is gone", not any(f"## policy: {o}".lower() in low for o in other_heads), "")
    name = field(text, "Release name")
    check("Release name form with a <n> placeholder", bool(name) and "<n>" in name, name)
    size = field(text, "Release size")
    check("Release size is a whole number", bool(size) and re.search(r"\b\d+\b", size) is not None, size)
    check("Changelog path", field(text, "Changelog") is not None)
    check("Cut steps field", field(text, "Cut steps") is not None)
    check("Whole-Release check field", field(text, "Whole-Release check") is not None)
    check("no seed instruction left (an italic note or (Only when)", "_(" not in text and "(only when" not in low)
    check("no unfilled choice placeholder", "|" not in (pol or "") and "<none" not in low)

    has_version_file = field(text, "Version file") is not None
    has_semver = all(w in low for w in ("patch", "minor", "major"))
    has_bump_pr = "bump pull request" in low
    has_versions_line = "versions:" in low
    if policy == "none":
        check("no version fields (no version file, bump, sizes or Versions line)",
              not (has_version_file or has_semver or has_bump_pr or has_versions_line or "bump commit" in low),
              f"version file {has_version_file}, sizes {has_semver}, bump PR {has_bump_pr}, Versions {has_versions_line}")
    elif policy == "pull-requests-bump":
        check("version file, bump commit and the Versions line cut step",
              has_version_file and "bump commit" in low and has_versions_line)
        check("no semver sizes or bump pull request", not (has_semver or has_bump_pr))
    else:
        check("version file, semver sizes and the bump pull request steps",
              has_version_file and has_semver and has_bump_pr and has_versions_line)
        check("no per-pull-request bump commit", "bump commit" not in low)
    sys.exit(0 if all(results) else 1)


main()
