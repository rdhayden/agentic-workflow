---
name: code-review
description: Review the diff between a specified start point (e.g. a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.) and finish point (e.g. `HEAD` or `worktree`) with specialised review subagents. The subagents run in parralel to find where code might break, be unreliable, perform badly, be vulnerable to attack, break contracts with existing consumers, violate coding standards or diverge from requirements. If no start point is specified it defaults to the last commit on the current branch. If no finish point is specified it defaults to the current worktree. A start point must be explicitly specified if a finish point is specified. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Review of the diff between a suppied or default starting point (e.g. a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.) and a supplied or default finishing point (e.g. `HEAD`, `worktree` ...etc.) using multiple specialised review agents.

## Process

## 1. Generate the diff

If a start point <start-point> is not specified then it defaults to the last commit in the current branch.
If a finish point <finish-point> is not specified then it defaults to the current worktree.

If both <start-point> and <finish-point> are the defaults the diff should include everything in the current branch that has changed since the last commit, use `git diff HEAD`

If only <start-point> is specified the diff should compare <start-point> to the working tree, use `git diff --merge-base <start-point>`

If only <finish-point> is specified return the error, 'a diff finish point cannot be specified unless a start point is provided'

If both <start-point> and <finish-point> is specified, then the diff should compare the <start-point> and <finish-point> as follows:
  - capture the diff command once: `git diff <start-point>...<finish-point>` (three-dot, so the comparison is against the merge-base)
  - Note the list of commits via `git log <start-point>..<finish-point> --oneline`.
  - Confirm the starting point resolves (`git rev-parse <start-point>`) and the diff is non-empty.

Before going further, a bad ref or empty diff should fail here and not spawn parallel sub-agents.

## 2. Invoke review agents

A list of subagents is given below. Each line in the list has the format '<agent-name> ← <inputs>' where:
  - <agent-name> is the name of the sub-agent to run in parralel 
  - <inputs> is one or both of 'diff' and 'specs' where 'diff' means pass the agent the diff generated using the instructions in section 1 above and 'specs' means pass the agent the originating issue/s, PRD/s or spec/s if that can be determined from the available context

Run each of the following agents as **parallel sub-agents** so they don't pollute each other's context: 
- adversarial-code-reviewer ← diff
- correctness-reviewer ← diff
- reliability-reviewer ← diff
- performance-reviewer ← diff
- security-reviewer ← diff
- api-contract-reviewer ← diff
- code-standards-reviewer ← diff
- spec-faithfullness-reviewer ← diff, specs

## 3. Aggregate results and resolve all problems

For each problem reported by a sub-agent
- If human review is not specified, run a sub-agent in series so that only one sub-agent is changing the code at any given time to avoid the need to merge multiple branches. The sub-agent's purpose is to provide a clean context window to resolve the issue in not to resolve problems in parralel. Pass it the problem description and instruct it to plan a fix and implement the fix with the /tdd skill.
- If the problem title and or description indicates that a human review is required, display the problem details to the user and ask the user how to resolve it, work through the problem until the user is fully satisfied it has been resolved before continuing to the next problem
- If human review is not specified but it is not possible to automatically fix the issue, describe the problem and work through the problem with the user until the user is fully satisfied it has been resolved before continuing to the next problem

Once all problems reported by the code review have been fully resolved run the following in a loop until all tests pass 
 - run the full test suite
 - resolve any failures that occur during testing