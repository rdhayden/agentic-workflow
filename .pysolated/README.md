# `.pysolated/` — parallel AFK issue driver

`main.py` drives AI coding agents through your GitHub issue backlog, sandboxed
with [pysolated](https://github.com/rdhayden/pysolated) + podman. It implements
issues **in parallel** whenever their dependencies allow.

## What `main.py` does

The backlog is a dependency graph: each issue declares what it is blocked by, so
at any moment several issues may be unblocked at once. `main.py` runs the graph
in **waves**. Each wave:

1. **Fetches** every issue with `gh` and computes the **ready set** on the host —
   open issues labelled `ready-for-agent` (AFK) whose every `## Blocked by`
   reference is already closed.
2. **Dispatches one sandbox per ready issue, in parallel** (capped at
   `MAX_PARALLEL`). The host assigns each sandbox a *specific* issue number, so
   parallel agents never collide on the same work.
3. **Merges** each completed issue's branch into the base branch, **sequentially**
   (so git never races). A clean merge just commits; a **merge conflict** is
   handed to a Claude session driving the `resolving-merge-conflicts` skill.
4. **Repeats** — finishing a wave closes issues, which unblocks the next wave.

The loop ends when no open AFK issues remain. If open AFK issues exist but are
all blocked (e.g. waiting on a HITL issue) or have exhausted their retries, it
pauses and asks you to resolve the blockers before continuing.

### Isolation via clones (not worktrees)

Parallel runs must not share a working tree. The podman sandbox bind-mounts only
its `work_dir`, and pysolated's worktree branch strategies require the
`no_sandbox` provider — so each run instead gets its own **full local clone**
(`git clone --local`, self-contained `.git`, hardlinked objects so it is cheap).
Clones live under `.pysolated/runs/` (gitignored) and are removed after their
issue merges. Because a clone's `origin` is a local path, `GH_REPO` is passed
into the container so `gh` still resolves the right GitHub repo.

## Issue format the driver expects

Issues are produced by the `to-issues` skill and must carry:

- **A triage label** — `ready-for-agent` (AFK, driven by this script) or
  `ready-for-human` (HITL, skipped).
- **A `## Blocked by` section** listing blocking issues as `- #NN`, or
  `None - can start immediately`. An issue becomes ready once every issue it is
  blocked by is **closed**.

## Prerequisites

- **podman** installed and working.
- **[uv](https://docs.astral.sh/uv/)** and **pysolated** available
  (`uv add pysolated` / `pip install pysolated`).
- Credentials in `.pysolated/.env` (gitignored, never mounted into the sandbox):
  ```
  CLAUDE_CODE_OAUTH_TOKEN=...
  GH_TOKEN=...
  ```
- The `skills/` directory at the repo root (its skills are copied into
  `.claude/skills/` and into each clone so the sandboxed agent can invoke `tdd`
  and `resolving-merge-conflicts` by name).

## Setup

From the repo root:

```bash
# 1. Build the sandbox image (tagged pysolated:pysolated, matching IMAGE in main.py)
uv run pysolated podman build-image

# 2. Add credentials
$EDITOR .pysolated/.env
```

## Run

```bash
uv run python .pysolated/main.py
```

Run it from the repo root — `main.py` locates the repo as its own parent
directory and reads/writes issues for that repo's GitHub remote.

## Configuration

Tunable constants at the top of `main.py`:

| Constant       | Default              | Meaning                                            |
| -------------- | -------------------- | -------------------------------------------------- |
| `MODEL`        | `claude-opus-4-7`    | Coding model each sandbox runs.                    |
| `IMAGE`        | `pysolated:pysolated`| Podman image tag (must match `build-image`).       |
| `AFK_LABEL`    | `ready-for-agent`    | Label marking an issue as AFK-implementable.       |
| `MAX_PARALLEL` | `5`                  | Most sandboxes to run at once in a wave.           |
| `MAX_ATTEMPTS` | `2`                  | Retries before an issue is skipped as stuck.       |

## Files

| File                   | Purpose                                                        |
| ---------------------- | ------------------------------------------------------------- |
| `main.py`              | The wave scheduler described above.                           |
| `prompt-afk-issue.md`  | Prompt to implement one *assigned* issue (`ISSUE-DONE` / `ISSUE-FAILED`). |
| `prompt-merge.md`      | Prompt to complete a conflicted merge (`MERGE-RESOLVED` / `MERGE-FAILED`). |
| `Containerfile` / `Dockerfile` | Sandbox image (git, `gh`, Claude Code + Codex CLIs).  |
| `.env`                 | Credentials (gitignored).                                     |
| `runs/`                | Per-issue clones, created and cleaned up at runtime (gitignored). |
