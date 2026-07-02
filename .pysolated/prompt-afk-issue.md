# YOUR ASSIGNED ISSUE

You have been assigned exactly ONE GitHub issue to implement: issue #{{issue}}.

Full details:

!`gh issue view {{issue}} --json number,title,body,comments`

The orchestrator has already selected this issue for you: it is an AFK (away from
keyboard) issue whose dependencies are all resolved. Do NOT pick a different
issue, and do NOT work on more than this one issue.

# COMPLETION SIGNALS

- When issue #{{issue}} is implemented, committed, and closed:
  output <completion>ISSUE-DONE</completion>
- If you cannot fully complete it (genuinely blocked, ambiguous, or the feedback
  loops cannot be made to pass): leave a comment on issue #{{issue}} explaining
  what you did and what remains, then output <completion>ISSUE-FAILED</completion>

# EXPLORATION

Explore the repo to understand the current state of the code relevant to this issue.

# IMPLEMENTATION

Complete the task using the tdd skill.

# FEEDBACK LOOPS

Before committing, run the feedback loops:

- run tests for any files that have changed
- run mypy in strict mode for the files that have changed
- run ruff to check formatting and linting for files that have changed

# COMMIT

Make a git commit. The commit message must:

1. Include key decisions made
2. Include files changed
3. Blockers or notes for next iteration

# THE ISSUE

If the task is complete, close GitHub issue #{{issue}} and output
<completion>ISSUE-DONE</completion>.

If the task is not complete, leave a comment on issue #{{issue}} with what was
done and what remains, then output <completion>ISSUE-FAILED</completion>.

# FINAL RULES

ONLY work on issue #{{issue}}. If the issue turns out to be larger than a single
vertical slice, implement what you can, capture the remainder in your commit
message and an issue comment, and treat it as ISSUE-FAILED so it can be picked
up again — do not close a half-finished issue.
