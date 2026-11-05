#!/usr/bin/env bash
# Structural checks of the dev-skills plugin. This repo's own tooling: it lives at the repo root,
# not in the plugin, so it does not ship in every project's plugin cache.
# Run from anywhere: scripts/check-plugin.sh (or a symlink to it). Requires python3 for JSON checks.
#
# Each check has a short name (the `# name:` comment above its code) and no number, so a new check
# takes no counter that parallel pull requests could collide on. A check tests structure or a
# repo-wide rule; it never pins a phrase of a skill's prose (rewording a skill is the Review's
# business). Do not add a check that greps a skill for a sentence from a past fix.
#
# Checks:
#   skill-layout                 skills/ holds only skill folders, each with a SKILL.md
#   model-invoked                every skill remains model-loadable; user-menu hiding is allowed
#   skill-name-matches-folder    each SKILL.md frontmatter name equals its folder name
#   skill-links                  each relative .md or .yaml link in a SKILL.md points at a file that exists
#   plugin-manifest              plugin.json, README.md, CHANGELOG.md and the licence file exist; plugin.json names its repository
#   codex-packaging              Codex marketplace exposes only dev-skills, with matching manifest identity and shared skills path
#   release-files                the release skill, its release doc seed and this repo's release doc exist
#   boundary-files               the Boundary record seed and this repo's Boundary record exist
#   openai-metadata-present      every skill folder has agents/openai.yaml
#   codex-implicit-invocation    no agents/openai.yaml turns implicit invocation off
#   openai-display-name          each agents/openai.yaml display_name reads like its skill's folder name
#   vendor-model-names           no vendor model name in the repo's text (ADR 0002): Claude, GPT (spaced or hyphenated), o-series (o1, o3, o4-mini) and Gemini names
#   no-person-names              no person's name in skill or doc text
#   repo-free-skill-text         skill text names nothing that exists only in this repo
#   no-repo-merge-rules          skill text does not name this repo's merge-time rules (the version hand-out, the Ticket re-read); a skill says to follow the repo's own docs
#   no-agent-label-strings       the plugin names no repo's agent-only label strings (a repo maps the role in its triage-labels.md)
#   tracker-operation-names      each operation cited as the tracker doc's **Name** or "Name" operation exists as a bold bullet in every issue-tracker seed
#   worker-reference-sources     each worker-control reference has methods, each method a Source: line with a doc link, each Detect and harness fact bullet a doc link
#   team-lead-no-harness-detail  team-lead text names no harness tool (no mcp__ name, no `name` a worker-control reference puts in backticks); it calls worker-control
#   milestone-no-delivery-detail the milestone skill plans and reports and hands delivery to team-lead: it names team-lead, and its text names no harness tool and no delivery record kind
#   skill-file-size              no skill file (a SKILL.md or a reference .md under a skill) is over 5,000 words, except the known files, which may not grow
#
# `claude plugin validate .` is not run here: CI runs it as its own step; the README says to run it before pushing.
#
# Same result however it runs: under `bash -e` or SHELLOPTS=errexit (this script reports every failure itself
# with bad(), and a no-match grep or find in a command substitution is a normal answer, not an error), and
# through a symlink (the repo is found from the script's real path).
set -u
set +e
src="${BASH_SOURCE[0]:-$0}"
# follow symlinks one hop at a time with plain readlink: `readlink -f` is GNU-only and macOS lacks it
while [ -L "$src" ]; do
  link_dir="$(CDPATH= cd -P "$(dirname "$src")" && pwd -P)"
  src="$(readlink "$src")"
  case "$src" in /*) ;; *) src="$link_dir/$src" ;; esac
done
# -P / pwd -P: physical paths, so a symlinked parent directory (a linked scripts/ folder) does not make ".." the link's parent
repo="$(CDPATH= cd -P "$(dirname "$src")/.." && pwd -P)"
root="$repo/plugins/dev-skills" # the plugin tree
skills="$root/skills" # every skill lives here
fail=0
bad() { echo "FAIL: $*"; fail=1; }

# skill-layout: skills/ holds only skill folders, each with a SKILL.md
if [ ! -d "$skills" ]; then bad "missing $skills"
else
  for f in "$skills"/* "$skills"/.[!.]*; do
    [ -e "$f" ] && [ ! -d "$f" ] && bad "stray file in skills: $(basename "$f")"
  done
  for d in "$skills"/*/; do
    [ -d "$d" ] || continue
    [ -f "${d}SKILL.md" ] || bad "skill folder $(basename "$d") has no SKILL.md"
  done
fi

# model-invoked: every skill is model-invoked
if [ -d "$skills" ] && grep -rn --include=SKILL.md -E '^[[:space:]]*["'"'"']?disable-model-invocation["'"'"']?[[:space:]]*:' "$skills"; then
  bad "a skill sets disable-model-invocation in frontmatter"
fi

# skill-name-matches-folder: a skill's SKILL.md frontmatter name: equals its folder name. The frontmatter is the
# block between the first two --- lines; quotes are ignored.
for d in "$skills"/*/; do
  [ -f "${d}SKILL.md" ] || continue
  folder="$(basename "$d")"
  fm_name="$(awk '/^---[[:space:]]*$/ {if (++b == 2) exit; next} b == 1 && /^name:/ {sub(/^name:[[:space:]]*/, ""); gsub(/["'"'"'[:space:]]/, ""); print; exit}' "${d}SKILL.md")"
  [ "$fm_name" = "$folder" ] || bad "skill $folder: SKILL.md frontmatter name \"$fm_name\" differs from its folder name"
done

# skill-links: a relative link in a SKILL.md to a .md or .yaml file points at a file that exists (a skill's
# reference files and seeds). Anchors are ignored. Other files' links are examples for the reader, not checked.
for sm in "$skills"/*/SKILL.md; do
  [ -f "$sm" ] || continue
  dir="$(dirname "$sm")"
  while IFS= read -r t; do
    t="${t%%#*}"
    case "$t" in ""|http:*|https:*|mailto:*) continue ;; esac
    [ -e "$dir/$t" ] || bad "$(basename "$dir")/SKILL.md links $t, which does not exist"
  done < <(grep -oE '\]\([^) ]+\.(md|yaml)(#[^) ]*)?\)' "$sm" | sed -E 's/^\]\(//; s/\)$//')
done

# plugin-manifest: the manifest, README, changelog and licence exist, and the manifest names the repo
[ -f "$root/LICENSE-mattpocock-skills" ] || bad "missing LICENSE-mattpocock-skills"
[ -f "$root/.claude-plugin/plugin.json" ] || bad "missing .claude-plugin/plugin.json"
[ -f "$root/README.md" ] || bad "missing README.md"
[ -f "$root/CHANGELOG.md" ] || bad "missing CHANGELOG.md"
grep -qE '"repository"[[:space:]]*:[[:space:]]*"https://github.com/[^"/]+/[^"/]+"' "$root/.claude-plugin/plugin.json" 2>/dev/null || bad "plugin.json has no repository field with a GitHub URL"

# codex-packaging: Codex publishes only dev-skills and shares Claude's identity and skill tree.
# Parse JSON rather than grepping formatting; missing or malformed packaging fails too.
if ! python3 - "$repo" <<'PYCODE'
import json
import pathlib
import sys

repo = pathlib.Path(sys.argv[1])
root = repo / "plugins/dev-skills"
try:
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    claude = json.loads((root / ".claude-plugin/plugin.json").read_text())
    codex = json.loads((root / ".codex-plugin/plugin.json").read_text())
    marketplace = json.loads((repo / ".agents/plugins/marketplace.json").read_text())
    require(codex.get("name") == claude["name"], "Codex manifest name differs from Claude manifest")
    require(codex.get("version") == claude["version"], "Codex manifest version differs from Claude manifest")
    def skill_paths(manifest):
        paths = manifest.get("skills")
        if isinstance(paths, str):
            paths = [paths]
        require(isinstance(paths, list) and paths and all(isinstance(path, str) for path in paths), "manifest skills must name directories")
        return [path.rstrip("/") for path in paths]
    require(skill_paths(codex) == skill_paths(claude) == ["./skills"], "Codex and Claude manifests must use the shared ./skills tree")
    require((root / "skills").is_dir(), "shared skills directory is missing")
    entries = marketplace["plugins"]
    require(marketplace["name"] == "luffy-dev", "Codex marketplace name differs from luffy-dev")
    require(len(entries) == 1 and entries[0]["name"] == claude["name"], "Codex marketplace must offer only dev-skills")
    source = entries[0]["source"]
    require(source == {"source": "local", "path": "./plugins/dev-skills"}, "Codex marketplace must use the shared dev-skills plugin")
except (AttributeError, KeyError, TypeError, ValueError, OSError) as error:
    print(f"FAIL: codex-packaging: {error}")
    sys.exit(1)
PYCODE
then
  bad "codex-packaging failed (see above; requires python3)"
fi

# release-files: the release skill and the release docs it reads exist (presence only; the skill's text is
# covered by repo-free-skill-text)
for f in "$skills/release/SKILL.md" "$skills/setup-dev-skills/release.md" "$repo/docs/dev-skills/release.md"; do
  [ -f "$f" ] || bad "missing ${f#"$repo"/}"
done

# boundary-files: the Boundary record seed that setup-dev-skills writes from, and this repo's own record (presence only)
for f in "$skills/setup-dev-skills/boundaries.md" "$repo/docs/dev-skills/boundaries.md"; do
  [ -f "$f" ] || bad "missing ${f#"$repo"/}"
done

# openai-metadata-present: every skill folder carries Codex/OpenAI metadata
for d in "$skills"/*/; do
  [ -d "$d" ] || continue
  [ -f "${d}agents/openai.yaml" ] || bad "skill $(basename "$d"): missing agents/openai.yaml"
done

# codex-implicit-invocation: every skill is implicitly invocable in the Codex/OpenAI metadata too
if [ -d "$skills" ] && grep -rn --include=openai.yaml 'allow_implicit_invocation: false' "$skills"; then
  bad "a skill's agents/openai.yaml sets allow_implicit_invocation: false"
fi

# openai-display-name: a skill's display_name in agents/openai.yaml names the skill. The display_name, lowercased with
# each run of other characters turned into one hyphen, equals the skill's folder name ("Grill with Docs" is
# grill-with-docs, "PR" is pr). So a display_name that is another skill's or a built-in skill's name fails.
for y in "$skills"/*/agents/openai.yaml; do
  [ -f "$y" ] || continue
  folder="$(basename "$(dirname "$(dirname "$y")")")"
  dn="$(sed -n 's/^[[:space:]]*display_name:[[:space:]]*//p' "$y" | head -n 1 | sed -E 's/^["'"'"']//; s/["'"'"'][[:space:]]*$//')"
  norm="$(printf '%s' "$dn" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-//; s/-$//')"
  [ -n "$dn" ] || bad "skill $folder: agents/openai.yaml has no display_name"
  [ -z "$dn" ] || [ "$norm" = "$folder" ] || bad "skill $folder: display_name \"$dn\" does not match the skill name (it should read like \"$folder\")"
done

# vendor-model-names: no vendor model names (Claude, GPT with an optional space or hyphen before its number, o-series such as o1 or o4-mini, Gemini) in the repo's text (ADR 0002): skills name cheap, regular or
# premium tiers. The tier map in the `model-tiers` skill (the plugin's one place that names the models) and this script are exempt.
plugin_rel="plugins/dev-skills"
# NUL-separated file list and a check on grep's output (not xargs' exit code), so file
# names with spaces and multi-batch xargs runs cannot hide a match.
hits="$(cd "$repo" && find . -type f -not -path './.git/*' \
  -not -path "./$plugin_rel/skills/model-tiers/SKILL.md" \
  -not -path './scripts/check-plugin.sh' -not -path './LICENSE*' \
  -not -path "./$plugin_rel/LICENSE-mattpocock-skills" -print0 |
  xargs -0 grep -nIiE '\b(haiku|sonnet|opus)\b|claude[-_]?(opus|sonnet|haiku|[0-9])|\bgpt[ -]?[0-9]|\bo[0-9](-(mini|pro|preview))?\b|\bgemini\b')"
if [ -n "$hits" ]; then
  echo "$hits"
  bad "text names a vendor model"
fi

# no-person-names: no person's name in skill or doc text: text says "the user", never the maintainer's name.
# The marketplace and repo names (luffy-dev, luffy-dev-skills), the GitHub owner Luffytse and the project name
# luffydev are not people. Checks skills/ and the plugin README, and the repo's CLAUDE.md and
# docs/ (all of it, the glossary in docs/dev-skills/ included). Not the manifests (author fields) or dai-portal-data.
# Paths are relative to each root (in a subshell, so cwd is unchanged), so a checkout
# under a home folder named after its user cannot trip the check. awk keeps the script portable (no GNU-only flags).
name_awk='{l=tolower($0); gsub(/luffy-dev-skills|luffy-dev|luffytse|luffydev/,"",l); if (l ~ /lufei|luffy/) print FILENAME ":" FNR ": " $0}'
name_hits="$(
  (cd "$root" && find skills README.md -type f -print0 2>/dev/null | xargs -0 awk "$name_awk" 2>/dev/null)
  (cd "$repo" && find CLAUDE.md docs -type f -print0 2>/dev/null | xargs -0 awk "$name_awk" 2>/dev/null)
)"
if [ -n "$name_hits" ]; then
  echo "$name_hits"
  bad "skill or doc text names a person (Lufei or Luffy); say \"the user\""
fi

# repo-free-skill-text: skill text leans on nothing that exists only in this repo, because every project that loads
# the plugin reads it. Under skills/ (*.md and *.yaml): no "ADR NNNN" (this repo's ADR numbers mean another decision,
# or nothing, elsewhere), no "Upstream" (this repo's glossary word for Matt Pocock's repo; lowercase "upstream", a
# fork's parent repo, is fine), no project, repo or maintainer name, and no path of this repo's own tooling or of
# another plugin. An example docs index line that links its own ADR file ("[ADR 0003](adr/0003-...") is fine.
hits="$(grep -rnE --include='*.md' --include='*.yaml' 'ADR [0-9]{4}|\bUpstream\b' "$skills" | grep -vE '\[ADR [0-9]{4}\]\(adr/')"
hits="$hits
$(grep -rniE --include='*.md' --include='*.yaml' 'luffydev|luffytse|luffy-dev|lufei|check-plugin|dai-portal' "$skills")"
hits="$(printf '%s\n' "$hits" | grep .)"
if [ -n "$hits" ]; then
  echo "$hits"
  bad "skill text names something only this repo has (an ADR number, \"Upstream\", a project, repo or person, or this repo's tooling)"
fi

# no-repo-merge-rules: the version hand-out (the coordinator gives each skill-changing pull request its number, one at a
# time) and the Ticket re-read after a skill merge are this repo's own merge-time rules (CLAUDE.md, docs/dev-skills/release.md).
# Skill text only says to follow the merge-time steps the repo's own docs give, so it never names either rule: no
# "version hand-out", no "Ticket re-read" (hyphenated, spaced or joined; "Tickets" too). Names only, never the prose
# around them: whether a sentence restates a rule in other words is the Review's question (REVIEW.md, "plugin text names nothing only this repo has").
hits="$(grep -rniE --include='*.md' --include='*.yaml' 'version hand[- ]?out|tickets? re[- ]?read' "$skills")"
if [ -n "$hits" ]; then
  echo "$hits"
  bad "skill text names a merge-time rule that only fits this repo (the version hand-out, the Ticket re-read); say to follow the merge-time steps the repo's own docs give"
fi

# no-agent-label-strings: the plugin speaks of the "agent-only" label role, never of one repo's label strings for it
# (those name particular coding agents and live in each repo's docs/dev-skills/triage-labels.md). Checks the whole plugin tree
# except CHANGELOG.md, which records releases in this repo's words.
hits="$(grep -rnE --exclude=CHANGELOG.md '(claude|codex)-only' "$root")"
if [ -n "$hits" ]; then
  echo "$hits"
  bad "plugin text names an agent-only label string (claude-only or codex-only); say the role and let the repo's triage-labels.md map it"
fi

# tracker-operation-names: skill text that cites an operation of the tracker doc by name
# (the tracker doc's **<Name>** operation, or the tracker doc's "<Name>" operation) names an operation that exists:
# a bold bullet (- **<Name>**) in every issue-tracker seed (setup-dev-skills/issue-tracker-*.md). Checks the cited
# name only, never the surrounding prose.
for seed in "$skills"/setup-dev-skills/issue-tracker-*.md; do
  [ -f "$seed" ] || continue
  ops="$(sed -nE 's/^- \*\*([^*]+)\*\*.*/\1/p' "$seed")"
  while IFS= read -r hit; do
    [ -n "$hit" ] || continue
    loc="${hit%%: *}"
    name="${hit#*: }"
    name="$(printf '%s' "$name" | sed -E "s/^tracker doc's //; s/ operation\$//; s/^(\*\*|\")//; s/(\*\*|\")\$//")"
    printf '%s\n' "$ops" | grep -qxF -- "$name" || bad "${loc#"$repo"/}: cited tracker operation \"$name\" is not a bold bullet in $(basename "$seed")"
  done <<EOF_HITS
$(grep -rnoE --include='*.md' "tracker doc's (\*\*[^*]+\*\*|\"[^\"]+\") operation" "$skills" | grep -v "/setup-dev-skills/issue-tracker-" | sed -E 's/^([^:]+:[0-9]+):/\1: /')
EOF_HITS
done

# worker-reference-sources: a worker-control reference (any .md in skills/worker-control other than SKILL.md) is looked up,
# never guessed, so its structure carries a doc page for every claim: at least one ### method under
# "## Methods the coordinator adds", a "Source:" line with an https link in every ### section, and an https link in
# every bullet under "## Detect" and "## What the harness does by itself". Structure only, never the wording.
if [ -d "$skills/worker-control" ] && ! python3 - "$skills/worker-control" <<'PYCODE'
import pathlib
import sys

failed = False


def report(message):
    global failed
    print(f"FAIL: worker-reference-sources: {message}")
    failed = True


for ref in sorted(pathlib.Path(sys.argv[1]).glob("*.md")):
    if ref.name == "SKILL.md":
        continue
    name = f"worker-control/{ref.name}"
    section, method, sourced, methods = None, None, False, 0
    for n, line in enumerate(ref.read_text().splitlines() + ["## end"], 1):
        if line.startswith("## ") or line.startswith("### "):
            if method is not None and not sourced:
                report(f"{name}: method \"{method}\" has no Source: line with a doc link")
            if line.startswith("## "):
                section, method = line[3:].strip(), None
            else:
                method, sourced = line[4:].strip(), False
                methods += section == "Methods the coordinator adds"
        elif method is not None:
            sourced = sourced or (line.startswith("Source:") and "(https://" in line)
        elif section in ("Detect", "What the harness does by itself") and line.startswith("- ") and "(https://" not in line:
            report(f"{name}:{n}: bullet has no doc link: {line[:80]}")
    if methods == 0:
        report(f"{name}: no ### method under \"## Methods the coordinator adds\"")
sys.exit(1 if failed else 0)
PYCODE
then
  bad "worker-reference-sources failed (see above; requires python3)"
fi

# team-lead-no-harness-detail: the team-lead skill manages work and takes every worker action through worker-control, so
# its text (*.md under skills/team-lead) names no harness tool or state: no mcp__ name, and no backticked name that a
# worker-control reference puts in backticks (its tool names, states and variables). Names only, never the wording.
if [ -d "$skills/team-lead" ] && ! python3 - "$skills" <<'PYCODE'
import pathlib
import re
import sys

skills = pathlib.Path(sys.argv[1])
names = set()
for ref in (skills / "worker-control").glob("*.md"):
    if ref.name != "SKILL.md":
        names |= set(re.findall(r"`([^`\n]+)`", ref.read_text()))
failed = False
for page in sorted((skills / "team-lead").rglob("*.md")):
    for n, line in enumerate(page.read_text().splitlines(), 1):
        hits = sorted(set(re.findall(r"`([^`\n]+)`", line)) & names) + re.findall(r"mcp__\w+", line)
        for hit in hits:
            print(f"FAIL: team-lead-no-harness-detail: {page.relative_to(skills)}:{n}: names {hit}")
            failed = True
sys.exit(1 if failed else 0)
PYCODE
then
  bad "team-lead-no-harness-detail failed (see above; requires python3): say it through worker-control"
fi

# milestone-no-delivery-detail: the milestone skill holds planning, adding a feature, Startup verification and the report;
# delivery is the team-lead skill's and worker lifecycle is worker-control's. So milestone's SKILL.md names team-lead, and its
# text (*.md under skills/milestone) names no harness tool (no mcp__ name, no backticked name a worker-control reference puts
# in backticks) and no delivery record kind (a `<!-- milestone <kind> -->` or `<!-- team-lead <kind> -->` marker other than
# the report's own). Names only, never the wording.
if [ -d "$skills/milestone" ] && ! python3 - "$skills" <<'PYCODE'
import pathlib
import re
import sys

skills = pathlib.Path(sys.argv[1])
names = set()
for ref in (skills / "worker-control").glob("*.md"):
    if ref.name != "SKILL.md":
        names |= set(re.findall(r"`([^`\n]+)`", ref.read_text()))
failed = False
if (skills / "worker-control").is_dir() and not names:
    print("FAIL: milestone-no-delivery-detail: worker-control references yield no backticked names")
    failed = True
if "team-lead" not in (skills / "milestone" / "SKILL.md").read_text():
    print("FAIL: milestone-no-delivery-detail: milestone/SKILL.md does not name team-lead")
    failed = True
for page in sorted((skills / "milestone").rglob("*.md")):
    for n, line in enumerate(page.read_text().splitlines(), 1):
        hits = sorted(set(re.findall(r"`([^`\n]+)`", line)) & names) + re.findall(r"mcp__\w+", line)
        hits += [m for m in re.findall(r"<!-- (?:milestone|team-lead) [a-z -]+ -->", line) if m != "<!-- milestone report -->"]
        for hit in hits:
            print(f"FAIL: milestone-no-delivery-detail: {page.relative_to(skills)}:{n}: names {hit}")
            failed = True
sys.exit(1 if failed else 0)
PYCODE
then
  bad "milestone-no-delivery-detail failed (see above; requires python3): delivery is team-lead's, worker lifecycle is worker-control's"
fi

# skill-file-size: a skill file (every .md under skills/) over 5,000 words is a split-or-redesign question for the user
# (Boundary record). Words are whitespace-separated tokens. A file over the limit when this check landed is listed in
# known_over with its word count then: it may not grow, and it comes off the list once it is back to 5,000 or fewer.
# Any other file over the limit fails.
if [ -d "$skills" ] && ! python3 - "$skills" <<'PYCODE'
import pathlib
import sys

LIMIT = 5000
known_over = {  # path under skills/ -> words when this check landed; empty since release/SKILL.md came back under
}
skills = pathlib.Path(sys.argv[1])
failed = False
seen = set()
for page in sorted(skills.rglob("*.md")):
    rel = page.relative_to(skills).as_posix()
    words = len(page.read_text().split())
    seen.add(rel)
    if rel in known_over:
        if words > known_over[rel]:
            print(f"FAIL: skill-file-size: {rel}: {words} words, grown past its recorded {known_over[rel]}; see writing-for-agents' \"When to split\"")
            failed = True
        elif words <= LIMIT:
            print(f"FAIL: skill-file-size: {rel}: {words} words, under {LIMIT} now; remove it from known_over")
            failed = True
    elif words > LIMIT:
        print(f"FAIL: skill-file-size: {rel}: {words} words, over {LIMIT}; see writing-for-agents' \"When to split\" and bring the user in to decide a split or a redesign")
        failed = True
for rel in known_over:
    if rel not in seen:
        print(f"FAIL: skill-file-size: {rel} no longer exists; remove it from known_over")
        failed = True
sys.exit(1 if failed else 0)
PYCODE
then
  bad "skill-file-size failed (see above; requires python3)"
fi

[ "$fail" -eq 0 ] && echo "OK: dev-skills plugin checks passed"
exit "$fail"
