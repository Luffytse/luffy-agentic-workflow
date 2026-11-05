#!/usr/bin/env python3
"""Pre-publish check: fail if any commit of a repo's history still holds a private trace.

It walks every commit reachable from the repo's refs (or only the refs named with --ref) and fails, naming
the commit and what it found, on:
  - dai-portal path: a file under the dai-portal-data plugin folder in any commit's tree;
  - personal email: an author or committer email that is not a no-reply address (GitHub's
    noreply@github.com, any *@users.noreply.github.com, Anthropic's noreply@anthropic.com), and any known
    personal email in a commit message or file;
  - hostname: an email at a Mac's .local hostname, and any known such hostname, in a message or file;
  - session link: a claude.ai session, project, chat or share link, a bare claude.ai session id, or a
    Claude session trailer line, in a message or file (the bare https://claude.ai/code link is fine);
  - home path: a macOS home-folder path (the Users folder, a name, a slash) in a message or file;
  - private term: a database name of the dai-portal-data plugin, or a term from --terms, in a message or
    file outside that plugin's folder.
It passes on a clean history and prints PASS with the counts. Each unique blob is read once (git cat-file
--batch), and a file finding names the oldest commit that brought that blob in, with its path.

Where the private values come from. This file is published with the history it guards, so it holds no
personal email, Mac user or host name and no database name, and its own patterns are written so that they
do not match themselves (for example the home-folder pattern spells its slashes as [/]). The values are
derived at run time, from the checked repo itself and from each --source repo (the unrewritten clone):
  - personal emails: every author and committer email that is not a no-reply address;
  - hostnames: the host part of every such email at a .local domain;
  - database names: every identifier that starts with the plugin's prefix and an underscore (the plugin
    folder's name up to its first hyphen) in any file the plugin folder ever held;
  - anything else: a local terms file passed as --terms, one literal per line, # for comments, matched
    without regard to case. Keep it outside the repo; never commit it.

Usage: scripts/check-public-history.py [--repo DIR] [--ref REF ...] [--source DIR ...] [--terms FILE]
Exit codes: 0 clean, 1 findings, 2 usage or git error.
"""
import argparse
import re
import subprocess
import sys

PLUGIN_DIR = "plugins/dai-portal-data/"
NOREPLY_EMAIL = re.compile(r"^(noreply@github\.com|noreply@anthropic\.com|[^@\s]+@users\.noreply\.github\.com)$",
                           re.IGNORECASE)
MAX_LINES = 300

# Generic patterns, matched against commit messages and file contents (bytes).
SESSION_PATTERNS = [
    re.compile(rb"claude\.ai/(?:code/)?(?:session_|sessions/|projects?/|chat/|share/)[^\s)\]>\"'`]*", re.I),
    re.compile(rb"\bsession_01[A-Za-z0-9]{20,}"),
    re.compile(rb"\bclaude-session[ \t]*:", re.I),
]
HOME_PATTERN = re.compile(rb"[/]Users[/][^/\s]+[/]")
LOCAL_EMAIL_PATTERN = re.compile(rb"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.local\b", re.I)
IDENT_LINE = re.compile(rb"^(author|committer|tagger) (.*?) <([^>]*)>", re.M)


class GitError(Exception):
    pass


def git(repo, *args, data=None):
    result = subprocess.run(["git", "-C", str(repo), *args], input=data, capture_output=True)
    if result.returncode != 0:
        raise GitError(f"git {' '.join(args)} failed in {repo}: {result.stderr.decode(errors='replace').strip()}")
    return result.stdout


def cat_batch(repo, shas):
    """Yield (sha, type, content) for each object, read in one git cat-file --batch run."""
    if not shas:
        return
    out = git(repo, "cat-file", "--batch", data=("\n".join(shas) + "\n").encode())
    pos = 0
    while pos < len(out):
        end = out.index(b"\n", pos)
        header = out[pos:end].split()
        if len(header) < 3:
            raise GitError(f"cat-file: missing object {header[0].decode()}")
        size = int(header[2])
        content = out[end + 1:end + 1 + size]
        pos = end + 1 + size + 1
        yield header[0].decode(), header[1].decode(), content


def rev_args(refs):
    return list(refs) if refs else ["--all"]


def list_commits(repo, refs):
    return git(repo, "rev-list", *rev_args(refs), "--").decode().split()


def blob_origins(repo, refs):
    """Map each blob to the oldest commit (and path) whose diff brought it in, and list plugin paths."""
    out = git(repo, "-c", "core.quotePath=false", "log", *rev_args(refs), "--raw", "-z", "--no-abbrev",
              "--no-renames", "-m", "--format=%x01%H", "--")
    origins, plugin_paths = {}, {}
    commit, meta = None, None
    for token in out.split(b"\0"):
        token = token.strip(b"\n")
        if token.startswith(b"\x01"):
            commit, meta = token[1:].decode(), None
        elif token.startswith(b":"):
            meta = token
        elif meta is not None and token:
            fields = meta.split()
            new_sha, status = fields[3].decode(), fields[4][:1]
            path = token.decode(errors="replace")
            if status != b"D" and set(new_sha) != {"0"}:
                origins[new_sha] = (commit, path)  # log runs newest first, so the last write is the oldest
                if path.startswith(PLUGIN_DIR):
                    plugin_paths[(commit, path)] = True
            meta = None
    return origins, list(plugin_paths)


def ident_emails(commit_bytes):
    head = commit_bytes.split(b"\n\n", 1)[0]
    return [(m.group(1).decode(), m.group(2).decode(errors="replace"), m.group(3).decode(errors="replace"))
            for m in IDENT_LINE.finditer(head)]


def derive_terms(repo, refs=None):
    """Private values found in a repo's history: personal emails, .local hostnames, database names."""
    emails = set()
    for sha, _, content in cat_batch(repo, list_commits(repo, refs)):
        for _, _, email in ident_emails(content):
            if email and not NOREPLY_EMAIL.match(email):
                emails.add(email)
    hosts = {e.split("@", 1)[1][:-len(".local")] for e in emails if e.lower().endswith(".local")}
    prefix = PLUGIN_DIR.rstrip("/").rsplit("/", 1)[1].split("-", 1)[0]
    db_pattern = re.compile(rb"\b" + re.escape(prefix.encode()) + rb"_[A-Za-z0-9_]+")
    origins, _ = blob_origins(repo, refs)
    names = set()
    plugin_blobs = [sha for sha, (_, path) in origins.items() if path.startswith(PLUGIN_DIR)]
    for _, _, content in cat_batch(repo, plugin_blobs):
        names.update(m.group(0).decode() for m in db_pattern.finditer(content))
    return {"personal email": emails, "hostname": {h for h in hosts if h}, "private term": names}


def read_terms_file(path):
    with open(path, encoding="utf-8") as handle:
        return {line.strip() for line in handle if line.strip() and not line.lstrip().startswith("#")}


def compile_terms(terms):
    """terms: kind -> set of literals. Returns a list of (kind, regex); longest literal first."""
    compiled = []
    for kind, values in terms.items():
        values = sorted({v for v in values if v}, key=lambda v: (-len(v), v))
        if values:
            compiled.append((kind, re.compile(b"|".join(re.escape(v.encode()) for v in values), re.I)))
    return compiled


def scan_text(content, term_patterns, skip_terms=False):
    """Yield (kind, matched text) for every private trace in a message or file."""
    for pattern in SESSION_PATTERNS:
        for m in pattern.finditer(content):
            yield "session link", m.group(0)
    for m in HOME_PATTERN.finditer(content):
        yield "home path", m.group(0)
    for m in LOCAL_EMAIL_PATTERN.finditer(content):
        yield "hostname", m.group(0)
    if not skip_terms:
        for kind, pattern in term_patterns:
            for m in pattern.finditer(content):
                yield kind, m.group(0)


def check(repo, refs=None, sources=(), terms_file=None):
    """Return (findings, commit count, blob count). A finding is (commit, where, kind, detail)."""
    terms = derive_terms(repo, refs)
    for source in sources:
        for kind, values in derive_terms(source).items():
            terms[kind] |= values
    if terms_file:
        terms["private term"] |= read_terms_file(terms_file)
    term_patterns = compile_terms(terms)
    findings = []

    def add(commit, where, kind, detail):
        if isinstance(detail, bytes):
            detail = detail.decode(errors="replace")
        item = (commit, where, kind, detail.strip())
        if item not in seen:
            seen.add(item)
            findings.append(item)
    seen = set()

    commits = list_commits(repo, refs)
    for sha, _, content in cat_batch(repo, commits):
        for role, name, email in ident_emails(content):
            if not NOREPLY_EMAIL.match(email):
                add(sha, role, "personal email", f"{name} <{email}>")
        message = content.split(b"\n\n", 1)[1] if b"\n\n" in content else b""
        for kind, detail in scan_text(message, term_patterns):
            add(sha, "message", kind, detail)

    origins, plugin_paths = blob_origins(repo, refs)
    for commit, path in plugin_paths:
        add(commit, "tree " + path, "dai-portal path", path)
    for sha, _, content in cat_batch(repo, list(origins)):
        commit, path = origins[sha]
        in_plugin = path.startswith(PLUGIN_DIR)  # already a dai-portal path finding
        for kind, detail in scan_text(content, term_patterns, skip_terms=in_plugin):
            add(commit, "file " + path, kind, detail)
    return findings, len(commits), len(origins)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--repo", default=".", help="the repo to check (default: the current folder)")
    parser.add_argument("--ref", action="append", default=[], help="walk only this ref (repeatable); default all refs")
    parser.add_argument("--source", action="append", default=[], help="an unrewritten repo to derive private values from")
    parser.add_argument("--terms", help="a local file of extra private terms, one per line")
    args = parser.parse_args(argv)
    try:
        findings, commits, blobs = check(args.repo, args.ref, args.source, args.terms)
    except (GitError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    for commit, where, kind, detail in findings[:MAX_LINES]:
        print(f"FAIL {commit} {where}: {kind}: {detail}")
    if len(findings) > MAX_LINES:
        print(f"... and {len(findings) - MAX_LINES} more")
    if findings:
        kinds = sorted({f[2] for f in findings})
        print(f"FAIL: {len(findings)} findings in {len({f[0] for f in findings})} commits ({', '.join(kinds)}); "
              f"checked {commits} commits, {blobs} blobs")
        return 1
    print(f"PASS: checked {commits} commits, {blobs} blobs; no private trace found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
