# Agentic Coding Workflow

## Claude specific setup
Make the status line more informative 
`/statusline` show model name, context percentage with a progress bar, and subscription usage

## Skills sources
https://github.com/mattpocock/skills/tree/main

## General codebase hygiene
Run `/improve-codebase-architecture` regularly

## Learning a new codebase
/teach me about ~/repo/.../codebase - I'm a new starter and I want to get productive on this codebase

## Feature engineering
Get some design brief e.g. from a product manager

`/grill-with-docs @design-brief`
note that you should break out and do research or create a prototype if you need to answer some of the questions, possibly with PMs etc. For example for front ends, you could ask, give me three prototypes, review this with the PM, feed in the winner and comments

then `/to-prd`

then `/prd-to-plan`

then `@.../prd-file.md @.../plan-file.md do phase 1`
iterate through all plans, human QA at each stage, commit after

## Code review
Implement a client side git precommit hook to perform linting and tests to enforce model reviews
Setup directly, see https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
Or use one of these libraries:
- https://pre-commit.com/ a python based library that provides multi-language support
- https://typicode.github.io/husky/ a node based library
