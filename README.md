# Agentic Coding Workflow

## Setup
Copy the skills folder to the project .claude folder if using Claude or .agents if using another model
Run `/setup-workflow-skills` to configure AGENTS.md or CLAUDE.md with the issue tracker, triage labels, 
and where the model should read and write vocabulary and architecture design records

Note skills were originally sourced from https://github.com/mattpocock/skills/tree/main as well as some review agents recast as skills from https://github.com/EveryInc/compound-engineering-plugin/. Both sources content have been modified a little to work well with this workflow and the example scripts in the .pysolated folder which automate implementation and review to scale up

## Aggressive context usage and clearing
Make the status line more informative. In Claude `/statusline` will do it although there are equivalents in most harnesses, I find it convenient to show the model name, context used percentage with a progress bar, and subscription usage

The model is useful if you're switching to cheaper/faster models for sme tasks and the subscription usage gives you a heads up if you're likely to hit any weekly or daily limits so you can calibrate your work accordingly. But the main purpose of this is to track context window usage so you can be quite aggressive in keeping the context window clean. 

Some recommend keeping it to as low as 10% of available context, some think up to 40% still gives you great results. At some point even though you have available context, the AI starts performing worse not because of specific short comings in the AI model but rather because you should think of everything in context as part of the instruction set. Everything in the context may inform the probabilities of subsequent tokens. The more information the AI has to hold in context, the more likely it is that some of that information misdirects the AI. For example you may have made a point to tell the AI to be brief somewhere in the context but would prefer to optimise for completeness later on, neither of those is universally correct, different contexts require different strategies. The longer your context gets the more likely it is that these sorts of contradictions or distractions creep in

If you aggresively clear the context whenever there's a possibility it's accumulating junk (anything that's not immediately relevant to the task at hand) you are paying for it with more tokens because the AI may need to rescan code and other sources to get the information it needs and may have already had before. But you're also clearing out the junk that distracts or misdirects it. You're improving predictive performance, which translates to better code, for higher token costs. Usually the extra token cost is an illusion because it you produce lower quality code, you're more likely to spend more tokens fixing failing tests subsequently. So it may be better to spend more tokens early to give it the best chance of producing good code to avoid spending time and tokens later to fix code.

Of course watching the progress bar and asking yourself that question constantly is a distraction and itself a drag on productivity, so I use 10% of the context window as a heuristic for when to start thinking about it more. At the time of writing (June 2026) I occasionally use up to 15% of the context and seldom need to go much over that. This is a heuristic that will change over time, not a religion, treat it as such.

## Misc recomendations

If using github, it's worth setting up dependabot to automatically create pull requests for outdated packages and security vulnerabilities, its free for public repos at the time of writing (June 2026) and helps reduce supply chain risks for everyone.

Ask the AI to set it up for you, you need to setup a dependabot YAML config file in the repo and specify the package manager/s it should scan, as well as how often to schedule scans (weekly is a good default) 

## Create new skills

If you want to create additional skills this is helpful: 
`/write-a-skill create a {{some-skill-name}} skill that does {{xxx}}`
`/write-a-skill update {{some-skill-name}} skill so that it does {{yyy}}`

Note it may create a verbose skill, edit it down for brevity, usually being super explicit just wastes
tokens, the frontier models tend to understand more concise prompts. Most harnesses have skill writing skills so use the native versions if you prefer, `/write-a-skill` seem to work well for me

## General codebase hygiene
Run `/improve-codebase-architecture` regularly, perhaps weekly depending on the size of the codebase. You could wire it into every CI flow but on large codebases that may unnecesarily burn tokens. Read the skill to see what it does, it mainly deepens modules which helps clarify useful boundaries to test and makes the codebase easier to comprehend. It's not magic and doesn't entirely replace thinking about architecture more broadly, although architecture skills are likely to be a fruitfull area too keep exploring new skills

## Learning a new codebase
`/teach me about {{~/repo/.../codebase}} I'm new and want to get productive on this codebase`

## Engineering features

### Define where you're going
Get some brief description of the feature e.g. from a product manager

`/grill-with-docs {{@design-brief}}`

Note that you should also break out and do research or create a prototype if you need to answer 
some of the more cmplex questions that come up with more clarity. To this without bloating the context window for the grilling session use
`/handoff {{what the next session will be for}}` to create a handoff document in your system
tmp directory which can be used to capture all existing context for research or prototyping
then in a separate session/terminal 
`/software-design-research {{describe what you eventually want to implement and or handoff document}}` to search the web for say which frameworks to use or what other people have done to solve a technical challenge. It creates a research document with multiple options and recommendations
or
`/prototype {{describe-what-you-want-to-prototype}}` this either builds several UIs or terminal apps that demonstrate backend logic

Simply `resume grilling` in the original grilling session when you're ready

### Commit the destination details to a spec

Immediately after the grilling in the same session while all the answers are in the context, create spec with `/to-spec`

### Define how to get there

If in the same session as the grilling `/to-issues` 
Or start a new context window and `/to-issues @prd-or-spec-file` 

This creates a set of issues, each with thier dependencies on other issues declared and labelled as AFK (away from keyboard) or HITL (human in the loop). It uses the concept of tracer bullets to decompose the spec into slices that each demonstrate some useful output.

### Implementation

If you want to baby sit implementation for each issue prompt claude as follows
`select an issue that has no dependencies or has all dependencies met from {{your issue tracker e.g. github issue board}} and implement it`

Although that does not improve productivity as much as possible. To do more hands off implementation run a loop (see next section for how) which selects the next issue in this priority order and implements it:
1. critical bug fixes
2. Development infrastructure
3. Tracer bullets for new features
4. Polish and quick wins
5. Refactors

Then returns some text sequence when there are no more issues that terminates the loop. The implementation need not be strictly sequential, since all issues declare their dependencies it is possible for the loop to spin up multiple agents working on multiple issues in parralel.

#### Automated iteration with pysolated or sandcastle

Pysolated (Python based) and Sandcastle (Typescript based) can spin up several different types of 
sandbox (e.g. docker, podman, vercel) and execute the implementation loop described above with your chosen coding agent.

It can iteratively issue a prompt which selects the next task in the priority order above and returns
one or more completion tags which can be used to terminate the loop or wait for a user to complete
human in the loop dependencies

Pysolated is at https://pypi.org/project/pysolated/ or https://github.com/rdhayden/pysolated simply uv/pip install it into your project
Sandcastle is at https://github.com/mattpocock/sandcastle

See the .pysolated directory at https://github.com/rdhayden/pysolated for an example implementation
of the loop using podman as the sandbox

You will need to initialise pysolated first to create a Container file and other bits using `uv run pysolated init` 
Then build the container with `uv run pysolated podman build-image`
Then make sure your main script and prompt reflect the loop you want to implement. The example main.py in
the .pysolated folder implements issues in parralel where possible to minimise implementation time. See the README.md in the .pysolated folder for details if you want to use this example script

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
