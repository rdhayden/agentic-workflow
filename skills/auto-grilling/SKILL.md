---
name: auto-grilling
description: Walk every branch of the decision tree and resolve all dependencies to form a complete picture of what needs to be implemented.
---

Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. Provide all answers in the context window without asking the user.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than guessing and check.

Check if there are any existing terms described in Context.md files and architecture decisions defined in architecture decision files (ADR files). 

If context exists it may be a single context with the following directory structure:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Read and conform to any existing architecture decisions and term definitions in context.md files. If it is impossible to conform while making the change required then stop and ask the user how they want to resolve the conflict and update the context and ADRs based on what is agreed with the user.

Do not act on it just publish all questions and decisions into the context window so it is available for other skills.