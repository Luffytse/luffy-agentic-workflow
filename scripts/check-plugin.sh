#!/usr/bin/env bash
# Structural checks of the dev-skills plugin. This repo's own tooling: it lives at the repo root,
# not in the plugin, so it does not ship in every project's plugin cache.
# Run from anywhere: scripts/check-plugin.sh (or a symlink to it). Requires python3 for its Python checks.
#
# Each check has a short name (the `# name:` comment above its code) and no number, so a new check
# takes no counter that parallel pull requests could collide on. A check tests structure or a
# repo-wide rule; it never pins a phrase of a skill's prose (rewording a skill is the Review's
# business). Do not add a check that greps a skill for a sentence from a past fix.
#
# Checks:
#   skill-layout                 skills/ holds only skill folders, each with a SKILL.md
#   model-invoked                every skill is model-invoked (user-menu hiding is allowed), except a skill on the short person-started list, which sets disable-model-invocation
#   skill-name-matches-folder    each SKILL.md frontmatter name equals its folder name
#   skill-links                  each relative .md link in a SKILL.md points at a file that exists
#   plugin-manifest              plugin.json, README.md, CHANGELOG.md and the licence file exist; plugin.json names its repository
#   release-files                the release skill, its release doc seed and this repo's release doc exist
#   boundary-files               the Boundary record seed and this repo's Boundary record exist
#   vendor-model-names           no vendor model name in the repo's text (ADR 0002): Claude, the Claude model families (haiku, sonnet, opus, fable), GPT (spaced or hyphenated), o-series (o1, o3, o4-mini) and Gemini names
#   no-person-names              no person's name in skill or doc text
#   repo-free-skill-text         skill text names nothing that exists only in this repo
#   tracker-operation-names      each operation cited as the tracker doc's **Name** or "Name" operation exists as a bold bullet in every issue-tracker seed
#   worker-reference-sources     each worker-control reference has methods, each method a Source: line with a doc link, each Detect and harness fact bullet a doc link
#   team-lead-no-harness-detail  team-lead text names no harness tool (no mcp__ name, no `name` a worker-control reference puts in backticks); it calls worker-control
#   milestone-no-delivery-detail the milestone skill plans and reports and hands delivery to team-lead: it names team-lead, and its text names no harness tool and no delivery record kind
#   skill-file-size              no skill file (a SKILL.md or a reference .md under a skill) is over 4,000 words, except the known files, which may not grow
#   index-line-length            no bullet of this repo's docs/dev-skills/index.md is over 60 words (a link, one sentence of what the doc is, one "Read when" sentence)
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

# model-invoked: every skill is model-invoked, except the person-started skills named here (a person types
# their name; the model never starts them). Add a skill to the list only by a decision recorded in an ADR or issue.
person_started="improve-codebase-architecture"
if [ -d "$skills" ]; then
  while IFS= read -r hit; do
    [ -n "$hit" ] || continue
    skill_dir="$(basename "$(dirname "${hit%%:*}")")"
    case " $person_started " in
      *" $skill_dir "*) ;;
      *) echo "$hit"; bad "skill $skill_dir sets disable-model-invocation in frontmatter and is not on the person-started list" ;;
    esac
  done < <(grep -rn --include=SKILL.md -E '^[[:space:]]*["'"'"']?disable-model-invocation["'"'"']?[[:space:]]*:' "$skills")
fi

# skill-name-matches-folder: a skill's SKILL.md frontmatter name: equals its folder name. The frontmatter is the
# block between the first two --- lines; quotes are ignored.
for d in "$skills"/*/; do
  [ -f "${d}SKILL.md" ] || continue
  folder="$(basename "$d")"
  fm_name="$(awk '/^---[[:space:]]*$/ {if (++b == 2) exit; next} b == 1 && /^name:/ {sub(/^name:[[:space:]]*/, ""); gsub(/["'"'"'[:space:]]/, ""); print; exit}' "${d}SKILL.md")"
  [ "$fm_name" = "$folder" ] || bad "skill $folder: SKILL.md frontmatter name \"$fm_name\" differs from its folder name"
done

# skill-links: a relative link in a SKILL.md to a .md file points at a file that exists (a skill's
# reference files and seeds). Anchors are ignored. Other files' links are examples for the reader, not checked.
for sm in "$skills"/*/SKILL.md; do
  [ -f "$sm" ] || continue
  dir="$(dirname "$sm")"
  while IFS= read -r t; do
    t="${t%%#*}"
    case "$t" in ""|http:*|https:*|mailto:*) continue ;; esac
    [ -e "$dir/$t" ] || bad "$(basename "$dir")/SKILL.md links $t, which does not exist"
  done < <(grep -oE '\]\([^) ]+\.md(#[^) ]*)?\)' "$sm" | sed -E 's/^\]\(//; s/\)$//')
done

# plugin-manifest: the manifest, README, changelog and licence exist, and the manifest names the repo
[ -f "$root/LICENSE-mattpocock-skills" ] || bad "missing LICENSE-mattpocock-skills"
[ -f "$root/.claude-plugin/plugin.json" ] || bad "missing .claude-plugin/plugin.json"
[ -f "$root/README.md" ] || bad "missing README.md"
[ -f "$root/CHANGELOG.md" ] || bad "missing CHANGELOG.md"
grep -qE '"repository"[[:space:]]*:[[:space:]]*"https://github.com/[^"/]+/[^"/]+"' "$root/.claude-plugin/plugin.json" 2>/dev/null || bad "plugin.json has no repository field with a GitHub URL"

# release-files: the release skill and the release docs it reads exist (presence only; the skill's text is
# covered by repo-free-skill-text)
for f in "$skills/release/SKILL.md" "$skills/setup-dev-skills/release.md" "$repo/docs/dev-skills/release.md"; do
  [ -f "$f" ] || bad "missing ${f#"$repo"/}"
done

# boundary-files: the Boundary record seed that setup-dev-skills writes from, and this repo's own record (presence only)
for f in "$skills/setup-dev-skills/boundaries.md" "$repo/docs/dev-skills/boundaries.md"; do
  [ -f "$f" ] || bad "missing ${f#"$repo"/}"
done

# vendor-model-names: no vendor model names (Claude, its model families haiku, sonnet, opus and fable, GPT with an optional space or hyphen before its number, o-series such as o1 or o4-mini, Gemini) in the repo's text (ADR 0002): skills name cheap, regular, premium or
# top tiers. The tier map in the `model-tiers` skill (the plugin's one place that names the models) and this script are exempt.
plugin_rel="plugins/dev-skills"
# NUL-separated file list and a check on grep's output (not xargs' exit code), so file
# names with spaces and multi-batch xargs runs cannot hide a match.
hits="$(cd "$repo" && find . -type f -not -path './.git/*' \
  -not -path "./$plugin_rel/skills/model-tiers/SKILL.md" \
  -not -path './scripts/check-plugin.sh' -not -path './LICENSE*' \
  -not -path "./$plugin_rel/LICENSE-mattpocock-skills" -print0 |
  xargs -0 grep -nIiE '\b(haiku|sonnet|opus|fable)\b|claude[-_]?(opus|sonnet|haiku|[0-9])|\bgpt[ -]?[0-9]|\bo[0-9](-(mini|pro|preview))?\b|\bgemini\b')"
if [ -n "$hits" ]; then
  echo "$hits"
  bad "text names a vendor model"
fi

# no-person-names: no person's name in skill or doc text: text says "the user", never the maintainer's name.
# The marketplace and repo names (luffy-agentic-workflow, and the earlier luffy-dev, luffy-dev-skills), the GitHub owner Luffytse and the project name
# luffydev are not people, nor is the skill name ask-luffy (the token alone: a person's name beside it still fails). Checks skills/ and the plugin README, and the repo's CLAUDE.md and
# docs/ (all of it, the glossary in docs/dev-skills/ included). Not the manifests (author fields).
# Paths are relative to each root (in a subshell, so cwd is unchanged), so a checkout
# under a home folder named after its user cannot trip the check. awk keeps the script portable (no GNU-only flags).
name_awk='{l=tolower($0); gsub(/luffy-agentic-workflow|luffy-dev-skills|luffy-dev|luffytse|luffydev|ask-luffy/,"",l); if (l ~ /lufei|luffy/) print FILENAME ":" FNR ": " $0}'
name_hits="$(
  (cd "$root" && find skills README.md -type f -print0 2>/dev/null | xargs -0 awk "$name_awk" 2>/dev/null)
  (cd "$repo" && find CLAUDE.md docs -type f -print0 2>/dev/null | xargs -0 awk "$name_awk" 2>/dev/null)
)"
if [ -n "$name_hits" ]; then
  echo "$name_hits"
  bad "skill or doc text names a person (Lufei or Luffy); say \"the user\""
fi

# repo-free-skill-text: skill text leans on nothing that exists only in this repo, because every project that loads
# the plugin reads it. Under skills/ (*.md): no "ADR NNNN" (this repo's ADR numbers mean another decision,
# or nothing, elsewhere), no "Upstream" (this repo's glossary word for Matt Pocock's repo; lowercase "upstream", a
# fork's parent repo, is fine), no project, repo or maintainer name, and no path of this repo's own tooling or of
# another plugin. An example docs index line that links its own ADR file ("[ADR 0003](adr/0003-...") is fine.
hits="$(grep -rnE --include='*.md' 'ADR [0-9]{4}|\bUpstream\b' "$skills" | grep -vE '\[ADR [0-9]{4}\]\(adr/')"
hits="$hits
$(grep -rniE --include='*.md' 'luffydev|luffytse|luffy-dev|luffy-agentic-workflow|lufei|check-plugin|dai-portal' "$skills")"
hits="$(printf '%s\n' "$hits" | grep .)"
if [ -n "$hits" ]; then
  echo "$hits"
  bad "skill text names something only this repo has (an ADR number, \"Upstream\", a project, repo or person, or this repo's tooling)"
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

# milestone-no-delivery-detail: the milestone skill holds planning, the Plugin version check and the report;
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

# skill-file-size: a skill file (every .md under skills/) over 4,000 words is a split-or-redesign question for the user
# (Boundary record). Words are whitespace-separated tokens. A file over the limit when this check landed is listed in
# known_over with its word count then: it may not grow, and it comes off the list once it is back to 4,000 or fewer.
# Any other file over the limit fails.
if [ -d "$skills" ] && ! python3 - "$skills" <<'PYCODE'
import pathlib
import sys

LIMIT = 4000
known_over = {  # path under skills/ -> words when the limit went to 4,000
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

# index-line-length: a bullet (a line starting "- ") of this repo's docs/dev-skills/index.md is over 60 words. Words are
# whitespace-separated tokens of the whole line. The index is a pointer, not a retelling of the doc it links.
index_file="$repo/docs/dev-skills/index.md"
if [ -f "$index_file" ] && ! python3 - "$index_file" <<'PYCODE'
import pathlib
import sys

LIMIT = 60
failed = False
for line in pathlib.Path(sys.argv[1]).read_text().splitlines():
    if line.startswith("- "):
        words = len(line.split())
        if words > LIMIT:
            print(f"FAIL: index-line-length: {line[:60]}: {words} words, over {LIMIT}")
            failed = True
sys.exit(1 if failed else 0)
PYCODE
then
  bad "index-line-length failed (see above; requires python3)"
fi

[ "$fail" -eq 0 ] && echo "OK: dev-skills plugin checks passed"
exit "$fail"
