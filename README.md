# Agentic Coding Workflow

## Claude specific setup
Make the status line more informative 
`/statusline` show model name, context percentage with a progress bar, and subscription usage

## Skills sources
https://github.com/mattpocock/skills/tree/main

## General codebase hygiene
Run `/improve-codebase-architecture` regularly

## Feature engineering
Get some design brief e.g. from a product manager

`/grill-with-docs @design-brief`
note that you should break out and do research or create a prototype if you need to answer some of the questions, possibly with PMs etc. For example for front ends, you could ask, give me three prototypes, review this with the PM, feed in the winner and comments

then `/to-prd`

then `/prd-to-plan`

then `@.../prd-file.md @.../plan-file.md do phase 1`
iterate through all plans, human QA at each stage, commit after
