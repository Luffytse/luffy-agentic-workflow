### 1. Edit a pull request body
Pull: 1
Body:
~~~
## Summary

Adds `greet.sh bye <name>` and `greet.sh shout <name>`.

Closes #20
Closes #21
Closes #22

## Evidence

`bash test.sh` passes.

**Door:** two-way. Reverting the merge removes both commands.
~~~

### 2. Run a command
Command: `bash test.sh` on the head of `spec-20` (f4d5888), in the Spec-branch Implementer's checkout

### 3. Merge a PR
Pull: 1
Method: merge
Title: feat: greet and say goodbye

### 4. Close
Issue: #20
Outcome: completed
Reason: Built by the Spec pull request 1, merged into main with a merge commit.

### 5. Close
Issue: #21
Outcome: completed
Reason: Landed on spec-20 as "feat: add a bye command" and merged into main with pull request 1.

### 6. Close
Issue: #22
Outcome: completed
Reason: Landed on spec-20 as "feat: add a shout command" and merged into main with pull request 1.
