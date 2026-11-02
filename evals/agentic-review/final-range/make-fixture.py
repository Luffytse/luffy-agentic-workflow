#!/usr/bin/env python3
"""Build disposable Git histories; report evidence, without scoring skill wording."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
root.mkdir(parents=True, exist_ok=False)
for case in ('bump-text', 'nit-text', 'both-logic', 'disguised-logic', 'unrelated-clean'):
    repo = root / case
    repo.mkdir()
    def git(*args, ok=True):
        result = subprocess.run(['git', '-C', str(repo), *args], text=True, capture_output=True)
        if ok and result.returncode:
            raise RuntimeError(result.stderr)
        return result
    def write(path, contents):
        (repo / path).write_text(contents)
    def commit(subject):
        git('add', '.')
        git('commit', '-qm', subject)
        return git('rev-parse', 'HEAD').stdout.strip()
    git('init', '-q', '-b', 'main')
    git('config', 'user.name', 'Fixture')
    git('config', 'user.email', 'fixture@example.test')
    write('guide.md', 'original wording\n')
    write('rule.md', 'agents may merge\n')
    write('version.json', '{"version":"1.0.0"}\n')
    write('note.md', 'teh heading\n')
    base = commit('base')
    git('switch', '-qc', 'ticket')
    write('guide.md', 'branch wording\n')
    write('rule.md', 'agents may merge after checks\n')
    last = commit('reviewed feature')
    git('tag', 'last-reviewed', last)
    commits = []
    if case in ('nit-text', 'both-logic'):
        write('note.md', 'the heading\n')
        commits.append([commit('fix R5-1 spelling'), 'final Nit R5-1'])
    if case in ('bump-text', 'both-logic', 'disguised-logic'):
        write('version.json', '{"version":"1.1.0"}\n')
        if case == 'disguised-logic':
            write('check.sh', 'exit 0\n')
        commits.append([commit('bump version'), 'claimed version bump'])
    if case == 'unrelated-clean':
        write('check.sh', 'exit 0\n')
        commits.append([commit('extra work'), 'unrelated logic'])
    git('switch', '-q', 'main')
    write('upstream.txt', 'upstream-only change\n')
    if case == 'both-logic':
        write('rule.md', 'only humans may merge\n')
    elif case != 'unrelated-clean':
        write('guide.md', 'main wording\n')
    main = commit('main advance')
    git('switch', '-q', 'ticket')
    merged = git('merge', '--no-ff', 'main', '-m', 'merge main', ok=False)
    conflicted = merged.returncode != 0
    if conflicted:
        if case == 'both-logic':
            write('rule.md', 'only humans may merge after checks\n')
        else:
            write('guide.md', 'combined wording\n')
        merge = commit('merge main')
    else:
        merge = git('rev-parse', 'HEAD').stdout.strip()
    commits.append([merge, 'main merge'])
    if case == 'both-logic':
        write('version.json', '{"version":"1.2.0"}\n')
        commits.append([commit('supersede bump after merge'), 'version-only superseding bump'])
    head = git('rev-parse', 'HEAD').stdout.strip()
    patch = git('log', '-p', '--first-parent', '--remerge-diff', f'{last}..{head}').stdout
    # Plumbing controls: actual command includes all own patches, excludes imported patches.
    assert '+upstream-only change' not in patch
    assert ('+combined wording' in patch) == (conflicted and case != 'both-logic')
    if case == 'both-logic':
        assert '+only humans may merge after checks' in patch
        assert '+{"version":"1.2.0"}' in patch
    if case in ('nit-text', 'both-logic'):
        assert '+the heading' in patch
    if case in ('bump-text', 'both-logic', 'disguised-logic'):
        assert '+{"version":"1.1.0"}' in patch
    if case in ('disguised-logic', 'unrelated-clean'):
        assert '+exit 0' in patch
    (repo / '.git' / 'review-range.patch').write_text(patch)
    record = dict(case=case, base=base, last_reviewed=last, main=main, head=head,
                  conflicts=conflicted, first_parent_commits=commits)
    (repo / '.git' / 'scenario.json').write_text(json.dumps(record, indent=2)+'\n')
    (repo / '.git' / 'release.md').write_text('Pull requests bump. The bump commit changes only version.json version value.\n')
    nit = next((sha for sha, category in commits if category == 'final Nit R5-1'), None)
    rows = (f'| R5-1 | Nit (fix) | spelling | note.md:1 | fixed | fixed in {nit}; entire patch checked: spelling only |\n'
            if nit else '')
    (repo / '.git' / 'round.md').write_text(
        f'<!-- code-review kind=round round=5 depth=Deep head={last} base={base} -->\n'
        '## Code review: Round 5 of at most 5 (Deep)\n\nResult: clean\n'
        'Milestone: outside; source: fixture Ticket\n\n'
        '| id | Severity | Bug class | Locations | Status | Note |\n'
        '|----|----------|-----------|-----------|--------|------|\n' + rows)

    print(json.dumps(record))
print('PASS: five histories; own patches retained and imported main patch excluded')
