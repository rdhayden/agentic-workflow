# COMPLETE AN IN-PROGRESS MERGE

A merge of branch `{{source_branch}}` (the work for issue #{{issue}}) into the
base branch is IN PROGRESS in this repository and has hit conflicts.

Current state:

!`git status`

Conflicted files:

!`git diff --name-only --diff-filter=U`

# YOUR TASK

Resolve the conflicts and COMPLETE this merge. Use the `resolving-merge-conflicts`
skill.

Core rules (from that skill):

- Understand the intent behind BOTH sides — read the commit messages on each
  side and the body of issue #{{issue}}.
- Preserve both intents where possible. Where incompatible, keep the change that
  matches the merge's goal and note the trade-off. Do NOT invent new behaviour.
- Always resolve — never `git merge --abort`.
- Run the project's automated checks (typecheck, then tests, then format) and fix
  anything the merge broke.
- Stage everything and commit to finish the merge.

# COMPLETION

- When the merge commit exists and the working tree is clean:
  output <completion>MERGE-RESOLVED</completion>
- If you genuinely cannot resolve it:
  output <completion>MERGE-FAILED</completion>
