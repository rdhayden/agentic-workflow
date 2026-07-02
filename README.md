# Agentic Coding Workflow

## Setup
Copy the skills folder to the project .claude flder if using Claude or .agents if using another model
Run `/setup-workflow-skills` to configure AGENTS.md or CLAUDE.md with the issue tracker, triage labels, 
and where the model should read and write vocabulary and architecture design records

Note skills were originally sourced from https://github.com/mattpocock/skills/tree/main although they have
been modified slightly

## Claude specific setup
Make the status line more informative 
`/statusline` show model name, context percentage with a progress bar, and subscription usage

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

Create a parent spec with `/to-spec` if everything is in the context, or if not pull it into 
the context with `@research-doc /to-spec`

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

Then returns some text sequence when there are no more issues to terminate the loop. But the default workflow 
automates much of the implementation, review and review response as follows

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
Then make sure your main script and prompt reflect the loop you want to implement (such as the example in
.pysolated)

Todo, create script that
	- fetches all AFK available for implementation issues
	- spins up a new agent for each
	- repeats until there are no AFK available, then either pauses if there are ready-for-human left or terminates

#### Review

Todo - create another script using pysolated to run review agents from compound engineering https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/skills/ce-code-review/SKILL.md
        - spins up agents that review and create issue/s (AFK or HITL) for each of the following implemented as skills ...
                - adversarial-reviewer
                - api-contract-reviewer
                - correctness-reviewer
                - deployment-verification-agent
                - julik-frontend-races-reviewer
                - performance-reviewer
                - reliability-reviewer
                - security-reviewer
	- when all complete, implements tickets as before
	- Then finally create a QA issue so that the user validates the features of all slices linked to the parent spec, should span all user stories
 

#### Commit hooks

Run a git precommit to run tests and typechecks if appropriate before any commit completes. You need to setup
Husky (https://typicode.github.io/husky/) or Pre-commit (https://pre-commit.com/) to invoke pre-commit hooks
Husky is written in Typescript and Pre-commit in python but both support running pre-commit hooks written in any 
language (e.g. run ruff and mypy from husky)

- https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/skills/ce-simplify-code/SKILL.md 
- consider adding a version of the improve architecture skill with the scope of just the changed files, check whether any new code should be merged into other existing code
