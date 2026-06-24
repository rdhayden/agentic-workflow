# Agentic Coding Workflow

## Claude specific setup
Make the status line more informative 
`/statusline` show model name, context percentage with a progress bar, and subscription usage

## Skills sources
https://github.com/mattpocock/skills/tree/main

## Add skills

Use 
`/write-a-skill create a {{some-skill-name}} skill that does {{xxx}}`
`/write-a-skill update {{some-skill-name}} skill so that it does {{yyy}}`

Note it may create a verbose skill, edit it down for brevity, usually being super explicit just wastes
tokens, the frontier models tend to understand more concise prompts

## General codebase hygiene
Run `/improve-codebase-architecture` regularly

## Learning a new codebase
`/teach me about {{~/repo/.../codebase}} I'm new and want to get productive on this codebase`

## Feature engineering

### Define where you're going
Get some design brief e.g. from a product manager

`/grill-with-docs {{@design-brief}}`
Note that you should break out and do research or create a prototype if you need to answer 
some of the questions. For example: 
	`/software-design-research {{describe what you eventually want to implement}}` 
		- this will ask questions, search the web 
		- and create a research document with multiple options and a recommendation
	`/prototype {{describe-what-you-want-to-prototype}}`
		- this either builds several UIs or terminal apps that demonstrate backend logic
You can use `/handoff {{what the next session will be for}}` to create a handoff document in your system
tmp directory which can be used to capture all existing context for research or prototyping
then simply `resume grilling` when you're ready, or start a fresh grilling with the results

Then optionally create a PRD or spec with `/to-prd` if everything is in the context, or if not pull it into 
the context with `@research-doc /to-prd`
The alternative is to go straight to `/to-issues`, see below

### Define how to get there

`/to-issues` or `/to-issues @prd-or-spec-file` creates a set of issues from context each with thier 
dependencies on other issues declared and labelled as AFK (away from keyboard) or HITL (human in the loop).
It also always creates a QA HITL issue

### Implementation

If you want to baby sit implementation for each issue 
`select an issue that has no dependencies or has all dependencies met from {{your issue tracker e.g. github issue board}} and implement it`

Preferably do more hands off iteration then complete the human QA issues manually. 
To do that run a loop which selects the next issue in this priority order and implements it:
1. critical bug fixes
2. Development infrastructure
3. Tracer bullets for new features
4. Polish and quick wins
5. Refactors

Then returns some text sequence when there are no more issues to terminate the loop.

#### Iteration with pysolated or sandcastle

Pysolated (Python based) and Sandcastle (Typescript based) can spin up several different types of 
sandbox (e.g. docker) and execute the implementation loop described above with your chosen coding agent.
It can iteratively issue a prompt which selects the next task in the priority order above and returns
one or more completion tags which can be used to terminate the loop or wait for a user to complete
human in the loop dependencies

Pysolated is at https://pypi.org/project/pysolated/ or https://github.com/rdhayden/pysolated
Sandcastle is at https://github.com/mattpocock/sandcastle

See the .pysolated directory at https://github.com/rdhayden/pysolated for an example implementation
of the loop using podman as the sandbox

You will need to initialise first to create a Container file and other bits using `uv run pysolated init` 
Then build the container with `uv run pysolated podman build-image`
Then make sure yur main script and prompt reflect the loop you want to implement (such as the example in
.pysolated)

### Review

Run a git precommit to run tests and typechecks if appropriate before any commit completes
Use Husky for node/tyepscript projects. Although husky can be used for other types of project, pre-commit.com is written in python as an alternative (use ruff for format checking and mypy for type checks)

There will always be a final user QA and PR/MR but first run some AI reviews

Todo, review compound engineering skills for review e.g.
- https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/skills/ce-code-review/SKILL.md
- https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/skills/ce-simplify-code/SKILL.md 
- consider adding a version of the improve architecture skill with the scope of just the changed files, check whether any new code should be merged into other existing code
