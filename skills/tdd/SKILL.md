---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle — consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behaviors that are expected from the system exposed through public interfaces. Never test implementation details. Implementation code can change entirely and the tests should not unless there is a corresponding explicitly requested change in system behaviour. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — it survives refactors because it tests capability not a specific implementation of a capability.

For Python see [PYTHON-TDD-TEST-EXAMPLES.md](../_language-references/PYTHON-TDD-TEST-EXAMPLES.md) and [PYTHON-MOCKABILITY-EXAMPLES.md](../_language-references/PYTHON-MOCKABILITY-EXAMPLES.md)

For Typescript see [TYPESCRIPT-TDD-TEST-EXAMPLES.md](../_language-references/TYPESCRIPT-TDD-TEST-EXAMPLES.md) and [TYPESCRIPT-MOCKABILITY-EXAMPLES.md](../_language-references/TYPESCRIPT-MOCKABILITY-EXAMPLES.md)

For other languages see the Typescript examples and apply the same principles where possible

## Seams — where tests go

A **seam** is the public boundary where you can observe behavior without knowledge of how the behaviour is implemented. Tests are applied to seams where behaviour is exposed but implementation is hidden, tests are never applied to internal implementations of the seam. Testing everything is not desirable, testing all behaviours expressed at seams is desired.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test would break if you refactored the code to produce the same behaviour or when you have refactored the code but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests become insensitive to behavioural changes that are meaningful to system users, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead — one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.
