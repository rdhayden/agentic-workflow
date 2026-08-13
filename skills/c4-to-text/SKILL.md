---
name: c4-to-text
description: Describe a system's architecture as a diagram-free Markdown document — C4 System Context, Container, and Component levels expressed as tables and prose. Use when someone needs to understand the architecture without a diagram renderer, asks for a text/Markdown C4 write-up, or wants the architecture in a form readable in a terminal, diff, or code review.
argument-hint: "Which system (or container) should I describe?"
---

# C4-to-Text

Produce a **plain-Markdown, diagram-free** description of a software system's architecture at the
three most-used C4 levels — **System Context**, **Container**, and **Component** — so an engineer can
understand it anywhere Markdown renders but diagrams do not (a terminal, a diff, a code review, a
plain text viewer).

Every element, relationship, and legend a C4 diagram would carry is expressed instead as **tables and
short prose**. The full method — table schemas per level, conventions, a document skeleton, worked
examples, and a quality checklist — lives in the bundled reference:

**→ Read [`c4-to-text.md`](./c4-to-text.md) before producing anything.** It is the source of truth for
structure and conventions; this file only tells you how to run the task.

## Process

1. **Read the reference.** Load `c4-to-text.md` and follow its conventions and table shapes exactly.

2. **Establish scope.** Confirm which **software system** is in scope (Level 1 / 2) and which
   **container(s)**, if any, warrant a Level 3 breakdown. If there is a human in the loop and they 
   haven't said, ask — or infer from the working directory and confirm. If this is being run without
   a human in the loop infer from the working directory.

3. **Gather the facts from the codebase, not from imagination.** Ground every element and
   relationship in something real:
   - **People / actors** — who uses the system (roles, other teams, external callers).
   - **External systems** — dependencies the code talks to but does not own (APIs, SaaS, mail,
     payment providers). Look at outbound clients, SDKs, config, and env vars.
   - **Containers** — separately runnable/deployable units and data stores. Look for service entry
     points, `Dockerfile`s/compose files, `package.json`/`pyproject`/`go.mod` roots, deploy manifests,
     and database/queue config. Record each container's **technology**.
   - **Components** — the internal building blocks behind a well-defined interface: controllers, 
     services, facades, repositories, modules. Prefer deriving these from the code structure so they 
     don't drift.
   - **Relationships** — who calls whom, in which **direction**, why, and over which **protocol**.
     Read the actual call sites, clients, and wiring; don't guess the arrows.

4. **Write the document** using the reference's skeleton: a title, a **Legend**, then one section per
   level (`Elements` table + `Relationships` table + optional `Notes`). Repeat the Component block 
   once per container you break down.

5. **Check against the reference's quality checklist** before finishing: every element self-describing
   and marked in-scope/external; every relationship directional, labelled with an active verb, and
   annotated with a protocol where it matters; detail kept at the right altitude per level; a legend
   present.

## Output

If there is a user in the loop and not being run in an automated agent, ask the user where the document 
should live if it isn't obvious. A sensible default is a file such as `docs/architecture.md` (or 
alongside existing architecture docs). Do not embed diagrams — the whole point is that this document 
stands on its own as text.

## Notes

- **A "container" is not a Docker container** — it is any separately runnable/deployable app or data
  store. The reference spells this out.
- **Component-level text drifts fastest.** prefer generating it from the code structure.
- If you can only partially ground a level from the codebase, say so in the `Notes` rather than
  inventing elements or arrows.