#!/usr/bin/env bash
# Builds the convergence fixtures of the agentic-review eval (returned and flip, each inside and outside a Milestone)
# and checks each holds what the check needs: the Boundary record, the tracker operations, the earlier Round comments,
# the fixed rows, the line shift the matching must follow, the kept Findings in the prompt, and (flip, inside) the
# earlier attempt record. Run: bash evals/agentic-review/convergence/test-fixture.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
out="$(mktemp -d)"
fail=0
bad() { echo "FAIL: $*"; fail=1; }
# line_has <repo> <rev> <file> <line> <fixed-text>: that line of the file at rev holds the text.
line_has() { git -C "$1" show "$2:$3" | sed -n "$4p" | grep -qF -- "$5"; }
# marker_head <comment-file>: the head= sha of its marker line.
marker_head() { head -1 "$1" | sed -n 's/.* head=\([0-9a-f]\{40\}\).*/\1/p'; }

for fx in returned flip; do
  for case in inside outside; do
    t="$fx/$case"; d="$out/$fx-$case"
    err="$(bash "$here/make-fixture.sh" "$d" "$fx" "$case" 2>&1 >/dev/null)" || { bad "$t: make-fixture failed: $err"; continue; }
    [ -z "$err" ] || bad "$t: make-fixture wrote to stderr: $err"
    r="$d/repo"
    [ -d "$r/.git" ] || { bad "$t: no repo"; continue; }
    git -C "$r" rev-parse -q --verify main >/dev/null || bad "$t: no branch main"
    grep -q 'Milestone label form.*milestone-<n>' "$r/docs/agents/boundaries.md" 2>/dev/null || bad "$t: Boundary record has no label form"
    grep -q 'docs/agents/boundaries.md' "$r/CLAUDE.md" 2>/dev/null || bad "$t: CLAUDE.md does not point to the Boundary record"
    for op in 'Comment on an issue' 'Create an issue'; do
      grep -q "^- \*\*$op\*\*" "$r/docs/agents/issue-tracker.md" 2>/dev/null || bad "$t: tracker doc has no $op operation"
    done
    (cd "$r" && bash test.sh >/dev/null 2>&1) || bad "$t: the fixture's own tests fail on main"

    if [ "$fx" = returned ]; then
      issue="$r/.scratch/issues/20-backup.md"; pr=1; branch=backup; rounds=2; script=src/backup.sh
    else
      issue="$r/.scratch/issues/30-count.md"; pr=2; branch=count; rounds=1; script=src/count.sh
    fi
    [ -f "$issue" ] || { bad "$t: no issue file"; continue; }
    grep -q '^Type: ticket' "$issue" || bad "$t: the issue is not a lone Ticket"
    git -C "$r" rev-parse -q --verify "$branch" >/dev/null || { bad "$t: no branch $branch"; continue; }
    grep -q "^Head: $branch" "$r/.scratch/pulls/$pr.md" 2>/dev/null || bad "$t: pull request $pr does not name branch $branch"
    if [ "$case" = inside ]; then
      grep -q '^Labels:.*milestone-1' "$issue" || bad "$t: issue lacks milestone-1"
      grep -q '^Labels:.*milestone-1' "$r/.scratch/issues/00-milestone.md" 2>/dev/null || bad "$t: no Milestone issue"
    else
      grep -q '^Labels:.*milestone-' "$issue" && bad "$t: issue carries a Milestone label"
    fi
    # the fixture's tests pass on the pull request's branch too: the planted problems are the kind tests miss
    (cd "$r" && git switch -q "$branch" && bash test.sh >/dev/null 2>&1; s=$?; git switch -q main; exit $s) || bad "$t: tests fail on $branch"

    # the earlier Round comments, each marker's head on the branch
    n=0
    for c in "$r/.scratch/pulls/$pr"/0*-round-*.md; do
      [ -f "$c" ] || continue; n=$((n + 1))
      head -1 "$c" | grep -q "^<!-- code-review kind=round round=$n depth=Standard head=[0-9a-f]\{40\} base=[0-9a-f]\{40\} -->$" || bad "$t: Round $n marker malformed"
      git -C "$r" merge-base --is-ancestor "$(marker_head "$c")" "$branch" 2>/dev/null || bad "$t: Round $n head is not on $branch"
    done
    [ "$n" = "$rounds" ] || bad "$t: expected $rounds earlier Round comments, found $n"
    last="$r/.scratch/pulls/$pr/0$rounds-round-$rounds.md"
    lh="$(marker_head "$last")"
    [ "$lh" != "$(git -C "$r" rev-parse "$branch")" ] || bad "$t: no fix commit since the last Round"

    if [ "$fx" = returned ]; then
      # R1-1 (unquoted path) is fixed as of Round 2, at src/backup.sh:8 at Round 2's head; one line is added above
      # it since, so the cp line is line 9 at the head, and the fix commit since Round 2 drops its quoting.
      grep -q '^| R1-1 | Important | unquoted path | .*src/backup.sh:8.* | fixed | fixed in [0-9a-f]\{7,\}' "$last" || bad "$t: Round 2 does not hold R1-1 fixed at src/backup.sh:8"
      grep -q '^| R2-1 | Important | .* | open |' "$last" || bad "$t: Round 2 does not hold R2-1 open"
      line_has "$r" "$lh" "$script" 8 'cp "$list"' || bad "$t: backup.sh:8 at Round 2's head is not the quoted cp line"
      line_has "$r" "$branch" "$script" 9 'cp -- $list' || bad "$t: backup.sh:9 at the head is not the unquoted cp line"
      line_has "$r" "$branch" "$script" 6 '[ -f "$list" ]' || bad "$t: backup.sh:6 at the head is not the added check"
      [ "$(git -C "$r" diff -U0 "$lh" "$branch" -- "$script" | grep -c '^@@')" -ge 2 ] || bad "$t: the fix commit should add a line above and change the cp line"
      git -C "$r" show main:src/add.sh | sed -n 5p | grep -qF 'echo $item >> $list' || bad "$t: main's src/add.sh:5 lacks the Pre-existing unquoted line"
    else
      # Round 1 raised R1-1 (a missing file read as an empty list); the fix commit since makes line 5 exit 1, and the
      # prompt's Round 2 Verify confirms it fixed and keeps R2-1, which asks to undo that fix.
      grep -q '^| R1-1 | Important | missing file read as empty | src/count.sh:5 | open |' "$last" || bad "$t: Round 1 does not hold R1-1 open at src/count.sh:5"
      line_has "$r" "$lh" "$script" 5 'echo 0; exit 0' || bad "$t: count.sh:5 at Round 1's head is not the exit-0 line"
      line_has "$r" "$branch" "$script" 5 'exit 1' || bad "$t: count.sh:5 at the head is not the exit-1 fix"
      grep -q '^State: closed' "$r/.scratch/pulls/1.md" 2>/dev/null || bad "$t: no closed first pull request"
      if [ "$case" = inside ]; then
        grep -q '^<!-- code-review kind=attempt attempt=1 ' "$issue" || bad "$t: the issue has no earlier attempt record"
        grep -q 'kind=attempt.*pr=1' "$issue" || bad "$t: the earlier attempt record does not name pull request 1"
      else
        grep -q 'kind=attempt' "$issue" && bad "$t: an attempt record outside a Milestone"
      fi
    fi

    # the scoring file stays out of the repo; the prompt holds the kept Findings and its Expected line
    [ -z "$(find "$r" -name 'EXPECTED*')" ] || bad "$t: a scoring file is inside the repo"
    p="$d/PROMPT.md"
    grep -q '^Expected:' "$p" 2>/dev/null || bad "$t: PROMPT.md has no Expected line"
    if [ "$fx" = returned ]; then ids='R2-1 R3-1 R3-2 R3-3'; else ids='R1-1 R2-1 R2-2'; fi
    for id in $ids; do grep -q "#### $id " "$p" || bad "$t: PROMPT.md lacks kept Finding $id"; done
    grep -v '^Score with' "$p" | grep -q EXPECTED && bad "$t: PROMPT.md names the scoring file outside its footer"
  done
done
rm -rf "$out"
[ "$fail" = 0 ] && echo "OK: convergence fixtures" || exit 1
