"""Wave-based parallel driver.

The serial version spun up one sandbox at a time; that sandbox self-selected a
single AFK issue and implemented it. Issues declare their dependencies in a
`## Blocked by` section, so at any moment there may be several issues whose
dependencies are already met — those are independent and can be implemented at
the same time.

This driver moves issue selection onto the host. Each iteration ("wave"):

  1. Fetch every issue and compute the READY set — open AFK issues
     (label `ready-for-agent`) whose `## Blocked by` references are all closed.
  2. Dispatch one sandbox PER ready issue, in parallel (capped), each assigned a
     specific issue number so they never collide on the same work.
  3. Merge each completed issue's branch into the base branch, sequentially.
     A merge conflict is handed to a Claude session driving the
     `resolving-merge-conflicts` skill.
  4. Repeat — finishing a wave closes issues, which unblocks the next wave.

## Isolation

Parallel runs must not share a working tree. The podman sandbox bind-mounts only
its `work_dir` (ADR 0004), so a linked git *worktree* would break — its `.git`
points at the main repo's `.git/worktrees/...`, which is outside the mount. So
each run instead gets its own full **local clone** (self-contained `.git`,
mounts cleanly). Completed clones are fetched + merged back into the host's base
branch, keeping the dependency graph coherent for the next wave.
"""

import asyncio
import json
import os
import re
import shutil
from pathlib import Path

from dotenv import load_dotenv
from pysolated import RunResult, claude_code, run
from pysolated.errors import PysolatedError
from pysolated.sandboxes.podman import podman

CONFIG_DIR = Path(__file__).parent
REPO_ROOT = CONFIG_DIR.parent  # .pysolated/ lives at the repo root
AFK_PROMPT = CONFIG_DIR / "prompt-afk-issue.md"
MERGE_PROMPT = CONFIG_DIR / "prompt-merge.md"
RUNS_DIR = CONFIG_DIR / "runs"  # gitignored; holds the per-issue clones

MODEL = "claude-opus-4-7"
IMAGE = "pysolated:pysolated"
AFK_LABEL = "ready-for-agent"  # HITL issues carry `ready-for-human` and are skipped
MAX_PARALLEL = 5  # most sandboxes to run at once in a wave
MAX_ATTEMPTS = 2  # give up on an issue after this many failed waves

# Load credentials from .pysolated/.env (gitignored) into the host environment.
# The .env is never mounted into the sandbox; values are passed explicitly via
# the provider's `env=`.
load_dotenv(CONFIG_DIR / ".env")


def _require_env(name: str) -> str:
    """Read a required credential from the environment, failing fast if unset.

    Credentials must never be committed to this driver script — the sandbox has
    no access to the host environment, so they are read here and passed
    explicitly via the provider's `env=`.
    """
    value = os.environ.get(name)
    if not value:
        raise SystemExit(
            f"missing required environment variable {name!r}; "
            f"export it before running (e.g. `export {name}=...`)"
        )
    return value


OAUTH_TOKEN = _require_env("CLAUDE_CODE_OAUTH_TOKEN")
GH_TOKEN = _require_env("GH_TOKEN")


def _podman(gh_repo: str) -> object:
    """A fresh podman provider for one run.

    `GH_REPO` is passed explicitly because a clone's `origin` points at the local
    base repo, so `gh` inside the container cannot infer the GitHub repo the way
    it can from the real remote — `GH_REPO=owner/name` makes `gh` unambiguous.
    """
    return podman(
        image=IMAGE,
        env={
            "CLAUDE_CODE_OAUTH_TOKEN": OAUTH_TOKEN,
            "GH_TOKEN": GH_TOKEN,
            "GH_REPO": gh_repo,
        },
    )


# --------------------------------------------------------------------------- #
# Host-side git / gh helpers
# --------------------------------------------------------------------------- #


async def _git(cwd: Path, *args: str) -> tuple[int, str, str]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        *args,
        cwd=str(cwd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    return proc.returncode or 0, out.decode(), err.decode()


async def _gh(*args: str) -> tuple[int, str, str]:
    proc = await asyncio.create_subprocess_exec(
        "gh",
        *args,
        cwd=str(REPO_ROOT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "GH_TOKEN": GH_TOKEN},
    )
    out, err = await proc.communicate()
    return proc.returncode or 0, out.decode(), err.decode()


async def detect_gh_repo() -> str:
    code, out, err = await _gh("repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")
    if code != 0:
        raise SystemExit(f"could not detect the GitHub repo: {err.strip()}")
    return out.strip()


async def detect_base_branch() -> str:
    _, out, _ = await _git(REPO_ROOT, "rev-parse", "--abbrev-ref", "HEAD")
    return out.strip() or "main"


async def fetch_issues() -> list[dict]:
    code, out, err = await _gh(
        "issue", "list", "--state", "all",
        "--json", "number,title,body,labels,state", "--limit", "1000",
    )
    if code != 0:
        raise SystemExit(f"`gh issue list` failed: {err.strip()}")
    return json.loads(out)


# --------------------------------------------------------------------------- #
# Dependency resolution
# --------------------------------------------------------------------------- #

# The `## Blocked by` section lists `- #NN` references (or "None ..."). Capture
# everything under that heading up to the next heading, then pull out the refs.
_BLOCKED_BY_RE = re.compile(
    r"^#{1,6}[ \t]*Blocked by\b.*?$(.*?)(?=^#{1,6}[ \t]|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)


def parse_blockers(body: str | None) -> list[int]:
    """Issue numbers this issue is blocked by (empty when it can start)."""
    match = _BLOCKED_BY_RE.search(body or "")
    if not match:
        return []
    return sorted({int(n) for n in re.findall(r"#(\d+)", match.group(1))})


def compute_ready(issues: list[dict], attempts: dict[int, int]) -> tuple[list[dict], list[dict]]:
    """Split issues into (ready-to-run, all-open-AFK).

    An issue is ready when it is open, labelled AFK, has not exhausted its retry
    budget, and every issue in its `## Blocked by` list is closed.
    """
    closed = {i["number"] for i in issues if i["state"] == "CLOSED"}
    open_afk: list[dict] = []
    ready: list[dict] = []
    for issue in issues:
        if issue["state"] != "OPEN":
            continue
        labels = {label["name"] for label in issue.get("labels") or []}
        if AFK_LABEL not in labels:
            continue
        open_afk.append(issue)
        if attempts.get(issue["number"], 0) >= MAX_ATTEMPTS:
            continue
        if all(blocker in closed for blocker in parse_blockers(issue.get("body"))):
            ready.append(issue)
    ready.sort(key=lambda i: i["number"])  # stable order; oldest first when capped
    return ready, open_afk


# --------------------------------------------------------------------------- #
# Per-issue clones (isolation) + skill seeding
# --------------------------------------------------------------------------- #


def _seed_skills(target_repo: Path) -> None:
    """Copy `skills/` into `<target>/.claude/skills/` so the sandboxed agent can
    invoke them by name (the podman image does not ship the skills, and clones
    only carry committed state). Mirrors the repo's documented setup step."""
    src = REPO_ROOT / "skills"
    if not src.is_dir():
        return
    dst = target_repo / ".claude" / "skills"
    dst.mkdir(parents=True, exist_ok=True)
    for skill in src.iterdir():
        if skill.is_dir():
            shutil.copytree(skill, dst / skill.name, dirs_exist_ok=True)


async def make_clone(issue_number: int) -> Path:
    """A fresh, self-contained local clone on branch `pysolated/issue-N`.

    Cloned each attempt from the current base so retries start from the latest
    merged state. `--local` hardlinks objects, so this is cheap on disk/time.
    """
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    gitignore = RUNS_DIR / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("*\n")

    clone = RUNS_DIR / f"issue-{issue_number}"
    if clone.exists():
        shutil.rmtree(clone)
    code, _, err = await _git(REPO_ROOT, "clone", "--quiet", "--local", str(REPO_ROOT), str(clone))
    if code != 0:
        raise RuntimeError(f"clone failed for issue #{issue_number}: {err.strip()}")
    await _git(clone, "checkout", "-b", f"pysolated/issue-{issue_number}")
    _seed_skills(clone)
    return clone


def _cleanup_clone(issue_number: int) -> None:
    shutil.rmtree(RUNS_DIR / f"issue-{issue_number}", ignore_errors=True)


# --------------------------------------------------------------------------- #
# Run + merge
# --------------------------------------------------------------------------- #


async def run_issue(issue: dict, gh_repo: str) -> RunResult:
    """Implement one assigned issue inside its own clone."""
    number = issue["number"]
    clone = await make_clone(number)
    return await run(
        agent=claude_code(MODEL),
        sandbox=_podman(gh_repo),
        prompt_file=str(AFK_PROMPT),
        prompt_args={"issue": str(number)},
        cwd=str(clone),  # the clone is the working tree; agent commits on its branch
        max_iterations=4,
        completion_signal=[
            "<completion>ISSUE-DONE</completion>",
            "<completion>ISSUE-FAILED</completion>",
        ],
        idle_timeout_seconds=600,
        completion_timeout_seconds=60,
        name=f"issue-{number}",
    )


async def merge_issue(base: str, number: int, gh_repo: str) -> bool:
    """Merge a completed issue's branch into `base`, sequentially and race-free.

    Clean merge → done. Conflict → hand the in-progress merge to a Claude session
    driving the `resolving-merge-conflicts` skill. If that can't finish it,
    abort so a later wave (or a human) can retry.
    """
    branch = f"pysolated/issue-{number}"
    clone = RUNS_DIR / f"issue-{number}"

    await _git(REPO_ROOT, "checkout", base)
    code, _, err = await _git(REPO_ROOT, "fetch", "--quiet", str(clone), branch)
    if code != 0:
        print(f"  ! could not fetch {branch} from clone: {err.strip()}")
        return False

    code, out, err = await _git(
        REPO_ROOT, "merge", "--no-ff", "-m", f"Merge issue #{number} ({branch})", "FETCH_HEAD"
    )
    if code == 0:
        print(f"  ✓ merged issue #{number}")
        _cleanup_clone(number)
        return True

    _, unmerged, _ = await _git(REPO_ROOT, "diff", "--name-only", "--diff-filter=U")
    if not unmerged.strip():
        print(f"  ! merge of issue #{number} failed (non-conflict): {(err or out).strip()}")
        return False

    print(f"  … merge conflict on issue #{number}; launching resolver agent")
    _seed_skills(REPO_ROOT)  # ensure resolving-merge-conflicts is available in the base repo
    try:
        await run(
            agent=claude_code(MODEL),
            sandbox=_podman(gh_repo),
            prompt_file=str(MERGE_PROMPT),
            prompt_args={"source_branch": branch, "issue": str(number)},
            cwd=str(REPO_ROOT),  # resolve the in-progress merge in the base repo itself
            max_iterations=3,
            completion_signal=[
                "<completion>MERGE-RESOLVED</completion>",
                "<completion>MERGE-FAILED</completion>",
            ],
            idle_timeout_seconds=900,
            completion_timeout_seconds=60,
            name=f"merge-{number}",
        )
    except (PysolatedError, OSError) as exc:
        print(f"  ! resolver run errored for issue #{number}: {exc}")

    _, still_unmerged, _ = await _git(REPO_ROOT, "diff", "--name-only", "--diff-filter=U")
    mid_merge = (REPO_ROOT / ".git" / "MERGE_HEAD").exists()
    if not still_unmerged.strip() and not mid_merge:
        print(f"  ✓ resolved & merged issue #{number}")
        _cleanup_clone(number)
        return True

    print(f"  ! resolver did not finish merge for issue #{number}; aborting")
    await _git(REPO_ROOT, "merge", "--abort")
    return False


# --------------------------------------------------------------------------- #
# Wave loop
# --------------------------------------------------------------------------- #


async def main() -> None:
    gh_repo = await detect_gh_repo()
    base = await detect_base_branch()
    _seed_skills(REPO_ROOT)
    print(f"repo: {gh_repo} | base branch: {base} | max parallel: {MAX_PARALLEL}")

    attempts: dict[int, int] = {}
    while True:
        issues = await fetch_issues()
        ready, open_afk = compute_ready(issues, attempts)

        if not open_afk:
            print("No more AFK issues. Done.")
            break

        if not ready:
            blocked = [i["number"] for i in open_afk]
            print(
                f"{len(open_afk)} open AFK issue(s) {blocked} but none are ready — "
                "blocked by unresolved dependencies (possibly HITL) or exhausted retries."
            )
            answer = await asyncio.to_thread(
                input, "Resolve the blocking dependencies, then continue? [y/N]: "
            )
            if answer.strip().lower() not in ("y", "yes"):
                print("Stopping until dependencies are resolved.")
                break
            attempts.clear()  # after manual intervention, give exhausted issues another chance
            continue

        batch = ready[:MAX_PARALLEL]
        numbers = [i["number"] for i in batch]
        print(f"\n=== Wave: {len(batch)} issue(s) in parallel: {numbers} ===")
        results = await asyncio.gather(
            *(run_issue(issue, gh_repo) for issue in batch), return_exceptions=True
        )

        succeeded: list[int] = []
        for issue, result in zip(batch, results):
            number = issue["number"]
            done = (
                isinstance(result, RunResult)
                and result.completion_signal == "<completion>ISSUE-DONE</completion>"
            )
            if done:
                succeeded.append(number)
                print(f"  ✓ issue #{number} implemented ({result.branch}, {result.usage})")
            else:
                attempts[number] = attempts.get(number, 0) + 1
                if isinstance(result, BaseException):
                    reason = repr(result)
                elif isinstance(result, RunResult):
                    reason = result.completion_signal or "no completion signal"
                else:
                    reason = "unknown"
                print(f"  ✗ issue #{number} not completed (attempt {attempts[number]}/{MAX_ATTEMPTS}): {reason}")

        if not succeeded:
            answer = await asyncio.to_thread(
                input, "No issues completed this wave. Continue anyway? [y/N]: "
            )
            if answer.strip().lower() not in ("y", "yes"):
                print("Stopping.")
                break
            continue

        print(f"Merging {len(succeeded)} completed issue(s) into {base} sequentially...")
        for number in succeeded:
            await merge_issue(base, number, gh_repo)
        # loop back: re-fetch — merged & closed issues now unblock the next wave


asyncio.run(main())
