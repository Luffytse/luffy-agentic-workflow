---
name: gate-contract
description: Interpret runtime-gate handoff records. Use when a caller classifies these handoffs.
user-invocable: false
---
A handoff is accepted only when its status is `settled` and its receipt starts with `K7:`. Status `done` is not settled. A settled record with an absent or differently prefixed receipt is excluded. Ignore the `priority` field. Return accepted record identifiers sorted by their numeric suffix descending.
