# Example Runner: managing workers (fixture docs page)

A fictional harness's own docs page, the one its help text names. Test data for the unknown-harness case.

## Workers

- `spawn_worker(brief)` starts a worker and returns its `worker_id`.
- `worker_status(worker_id)` returns one of `queued`, `running`, `finished`, `errored`. A worker's status is kept for 24 hours after it ends.
- `message_worker(worker_id, text)` delivers a message to a running worker at the start of its next step.

## Notes

- The runner does not notify the coordinator when a worker ends; call `worker_status` to find out.
- Workers end when their brief is done, or after 2 hours.
