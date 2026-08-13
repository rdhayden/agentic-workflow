---
name: c4-diagram
description: Draw a system's architecture as Mermaid diagrams — C4 System Context, Container, and Component levels expressed as renderable Mermaid code blocks. Use when someone asks for a C4 diagram, an architecture diagram, or a Mermaid/visual view of how a system fits together, or wants the architecture in a form that renders in GitHub, docs sites, or an artifact.
argument-hint: "Which system (or container) should I diagram?"
---

# C4-Diagram

Produce **Mermaid diagrams** of a software system's architecture at the three most-used C4 levels —
**System Context**, **Container**, and **Component** — so an engineer can see the shape of the system
anywhere Mermaid renders (GitHub, GitLab, most docs sites, Obsidian, an artifact page).

Every element, relationship, and legend a C4 diagram carries is expressed as **Mermaid nodes, edges,
and a legend subgraph**. The full method — which Mermaid dialect to use, node/edge syntax per level,
the C4 colour palette, escaping rules, worked examples, and a quality checklist — lives in the
bundled reference:

**→ Read [`c4-diagram.md`](./c4-diagram.md) before producing anything.** It is the source of truth for
syntax and conventions; this file only tells you how to run the task.

This is the diagram-bearing twin of the `c4-to-text` skill. Same model, same facts, same discipline
about altitude — different output medium. If the reader needs something that survives a terminal, a
diff, or a plain-text viewer, use `c4-to-text` instead (or as well).

## Process

1. **Read the reference.** Load `c4-diagram.md` and follow its dialect choice, syntax, and palette
   exactly.

2. **Establish scope.** Confirm which **software system** is in scope (Level 1 / 2) and which
   **container(s)**, if any, warrant a Level 3 breakdown. If there is a human in the loop and they
   haven't said, ask — or infer from the working directory and confirm. If this is being run without
   a human in the loop infer from the working directory.

3. **Gather the facts from the codebase, not from imagination.** Ground every node and edge in
   something real:
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

4. **Draw one diagram per level** using the reference's templates: a fenced ```mermaid block per
   level, each with a title, a boundary for what's in scope, styled nodes, labelled directional
   edges, and a legend. Repeat the Component diagram once per container you break down. Surround each
   with a sentence or two of prose saying what the reader should take from it.

5. **Verify the Mermaid actually renders.** A diagram that doesn't render is worse than no diagram.
   Follow the reference's escaping rules and re-read each block for unquoted labels, stray
   parentheses, and undefined node ids. Where you can render — an artifact preview, an IDE Mermaid
   preview, or `npx @mermaid-js/mermaid-cli -i d.mmd -o d.png` — **look at the picture**, not just
   the source: overlapping edge labels and crossing arrows are invisible in the text.

6. **Check against the reference's quality checklist** before finishing: every node labelled with
   name, type, and technology where the level calls for it; in-scope vs external visually distinct;
   every edge directional and labelled with an active verb plus a protocol where it matters; detail
   kept at the right altitude per level; a legend present; node count per diagram kept readable.

## Output

If there is a user in the loop and not being run in an automated agent, ask where the document should
live if it isn't obvious. A sensible default is a file such as `docs/architecture.md` (or alongside
existing architecture docs). If the diagrams are the deliverable for an audience rather than a repo
file, an artifact page renders Mermaid natively and may serve better — offer it.

## Notes

- **A "container" is not a Docker container** — it is any separately runnable/deployable app or data
  store. The reference spells this out.
- **Component-level diagrams drift fastest.** Prefer generating them from the code structure.
- **Keep each diagram readable.** Past roughly 20 nodes a C4 diagram stops communicating; split by
  boundary or drop to the next level down rather than cramming.
- If you can only partially ground a level from the codebase, say so in the surrounding prose rather
  than inventing nodes or arrows.
