# Parked feature scope decision traces

Agreed seam for Ticket #487: apply Release planning and the Milestone caller to tracker-shaped inputs and observe the chosen scope, label actions, left-out report and build decision. This is a bounded literal walkthrough by the Implementer, not an independent fresh-runtime evaluation or an executable tracker fixture. No tracker Park, label or other mutation is performed. A fresh agent can rerun the cases below against the named source revision without reading the expected column first.

## Inputs and prompt

Apply `release` step 5, especially "Inside a Milestone", and `team-lead`'s "2. Start work" and its parked-work rule under "Replace a stalled worker" (earlier `milestone` Delivery steps 1 and 2 and "Parked work", whose recorded traces stay as history). Propose only; call no tracker writes. Assume a valid open Milestone agreement, cap 5, no maintenance fixes and no boundary crossings. P and A through F are listed planned lone Tickets in that order, open and unlabelled; P reads parked through the configured tracker Park operation, the others do not. All are unblocked unless stated otherwise. Report chosen ordered features, proposed new labels, left-out reasons, existing labels preserved, and whether P starts building. Treat each row independently. Outside case O has no Milestone agreement and P is ready-for-agent. Existing labels and release issues name the same established Release throughout each rerun.

## Before implementation: base 5c8112c, version 0.47.0

Red walkthrough performed before editing the skills: fresh scope [P,A] meets the owner's open/unlabelled/unblocked predicates, so standalone `release` selects [P,A]. The caller's explicit not-parked predicate selects [A]. Expected [A] from both: **fail**, owner re-admits P. This is a literal decision trace of the missing predicate, not a claim about probabilistic agent behavior; an agent could infer Park exclusion from other context.

## After implementation: working tree based on 5c8112c, version 0.47.0

Walkthroughs performed against the changed owner and caller. Expected decisions below come from Ticket acceptance and the existing order, rerun and Park contracts.

| Case / state | Observed decision | Result |
| --- | --- | --- |
| Fresh [P,A] | Owner and caller choose [A], propose its label only, list P parked waiting on the user; P starts no build | Pass |
| Fresh [P,A,B,C,D,E,F] | Both choose [A,B,C,D,E] in order; F waits for the next Release, P is left out as parked; no P label/build | Pass |
| Fresh [P,A,B], A blocked by an uncleared external issue | Choose [B]; report A's blocker and P's park; no P label/build | Pass |
| Fresh [P,A,B], B blocked only by A | Choose [A,B], preserving earlier-in-scope dependency exception; P left out | Pass |
| Partial: P already carries release label, release issue absent; A through F free | Preserve P and its label as scope so far and one cap slot; add [A,B,C,D] only; open missing release issue for [P,A,B,C,D]; report P parked and skipped, start no P build | Pass |
| Rerun: release issue lists [P,A], labels already applied; B free | Keep [P,A], cap used 2, no new B label or reselection; report P parked and skipped, start no P build | Pass |
| Fresh [P,A], P no longer reads parked (fixture state only) | Both choose [P,A] in order; ordinary unstarted user-parked feature can start under existing caller rules | Pass |
| O: outside a Milestone, ready-for-agent P parked and unlabelled | Ordinary step 5 candidate policy is unchanged: P remains a proposal candidate subject to user scope approval; tracker Park still prevents its build | Pass / unchanged control |

No label is removed; no Park is lifted. Existing parked members remain open, so step 1 still blocks cutting that Release. The maintenance source/list policy, Spec Ticket propagation, Release identity, cap and completion test are unchanged. No broader outside-Milestone candidate rule is asserted.

Not exercised: live GitHub reads/writes, actual Park lifting, installed skill discovery/application, full Milestone scheduling or build startup, Release cutting, maintenance selection or Spec child propagation. These traces establish local literal workflow decisions only; structural checks do not turn them into end-to-end evidence.
