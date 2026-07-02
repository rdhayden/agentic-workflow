# Agentic Coding Workflow

This is a workflow for building features reliably with AI. It includes a set of skills that throughly align with the user on design intent, a sandboxing library and example script that loops of tasks for parralel execution where appropriate, and a set of review agents that improve code robustness, reliability, performance and maintainability.

## Setup

Copy the skills folder to the project .claude folder if using Claude or .agents if using another model
Run `/setup-workflow-skills` to configure AGENTS.md or CLAUDE.md with the issue tracker, triage labels, 
and where the model should read and write vocabulary and architecture design records

Note many of the skills were originally sourced from https://github.com/mattpocock/skills/ which in turn encapsulate practices from The Pragmatic Programmer and philosophies for engineering with AI that I've heard people like Dex Horthy from human layer describe as well. It also layers in some review agents recast as skills from https://github.com/EveryInc/compound-engineering-plugin/. The content from both sources have been modified a little to work well with this workflow and augmented with a sandboxing library and example scripts that automate parts of the dev process to maximise efficiency.

## Aggressive context clearing

Before starting the workflow it is recommended to make the CLI status line more informative. In Claude `/statusline` will do it although there are equivalents in most other harnesses and this workflow is deliberately model and harness agnostic. I find it convenient to show the model name, the percentage of the context window used and subscription usage in real real time in the status line.

Displaying the model and subscription usage is a convenience, but the main purpose of this, for this workflow, is to track context window usage so you can be quite aggressive about keeping the context window clean. 

At some point even though the AI may be able to accept more context, it may start performing worse. Not because of any specific short comings of the AI model, but rather because you should think of everything in the context as part of the instruction set. If its in context it informs the probabilities of subsequent tokens (subject to attention weightings). The more information the AI has to hold in context, the more likely it is that some of that information misdirects the AI. 

For example you may have made a point to tell the AI to be brief somewhere in the context, but later wanted to optimise for completeness over brevity. Neither of those choices is universally correct but they may each be apprpriate at different times. The longer your context gets, the more likely it is that these sorts of contradictions creep in, which can lead to unexpected results.

If you aggresively clear the context whenever there's a possibility it's accumulating junk, and by that I mean anything that's not immediately relevant to the task at hand, you are paying for it with more tokens because the AI may need to reread code and other sources it previously read. But you're also clearing out junk that may distract or misdirect it. You're improving predictive performance by only given it relevant information, which translates to better code, but on the surface you're trading that for higher token costs. The extra token costs may be an illusion because if you produce lower quality code, your tests are more likely to fail, or worse edge cases fail in production. Then you spend more tokens and time fixing the issues. So I take the view that it's better to spend more tokens early to give the AI the best chance of producing good code and avoid spending time and tokens to fix issues, and sometimes reputational damage, later.

Of course asking yourself constantly whether the current context only includes necesary information is also a distraction and a drag on productivity, so I use 10% of the context window as a heuristic for when to start thinking about it more. At the time of writing (June 2026) I occasionally use up to 15% of the context and seldom need to go much over that. This is a heuristic that will change over time, not a religion, treat it as such. But typically as I get close to 10%, if I have finished a given phase of this workflow (I have completed one of the skills in the workflow), I clear the context and start a new session before running the next skill or script. But I've pushed it over 20% without obvious quality issues, in part because the process itself has multiple layers of validation and alignment.

## Miscellaneous recomendations

If using github, it's worth setting up dependabot on your repo to automatically create pull requests for outdated packages and security vulnerabilities, its free for public repos at the time of writing (June 2026) and helps reduce supply chain risks for everyone.

Ask the AI to set it up for you, it sets up a dependabot YAML config file in the repo which specifies the package manager/s it should scan for dependencies, as well as how often to schedule scans (weekly is a good default) 

## Create new skills

This repo comes with the skills you need for this workflow but you should extend or adapt these skills as you work with them and discover further optimisations. Most harnesses have skill writing skills so use the native versions if you prefer. `/write-a-skill` seem to work well for me
 
`/write-a-skill create a {{some-skill-name}} skill that does {{xxx}}`
`/write-a-skill update {{some-skill-name}} skill so that it does {{yyy}}`

Note it may create a verbose skill, you may want to edit it down for brevity afterwards. Being overly explicit may just waste tokens and the frontier models tend to understand the intent of more concise prompts. 

## General codebase hygiene

While not part of the feature creation workflow you may also want to run `/improve-codebase-architecture` regularly, perhaps weekly depending on the size of the codebase. 

You could wire it into the CI flow so it runs with every merge of production code, but on large codebases that may unnecesarily burn tokens. Read the skill to see what it does, it mainly deepens modules which is a way to clarify critical test boundaries and make the purpose of each module in the wider architecture  easier to comprehend. That makes it both easier for the user to evaluate the test suite in PR/MR reviews and for the AI to understand the codebase which in turn leads to better code. 

It's not magic and doesn't entirely replace thinking about architecture more broadly, although additional architecture skills are likely to be a useful and may be added as this workflow evolves.

## Learning a new codebase

This workflow emphasises human AI alignment so if you're working on an existing codebase, having a good grasp of the existing code is still particularly important. How can you confidently guide the AI on design decisions without a reasonable understanding of what the existing code does and what design decisions preceeded your involvement.

There are many useful tools emerging to enable both AI and people to digest larger and larger codebases. One such example is https://github.com/Egonex-AI/Understand-Anything which can be very useful but it burns through a lot of tokens to create an initial graph of the code and can produce a graph that is still quite large to consume. There are still many good arguments for great knowledge graphs, they can for example be great when you're trying to evaluate the blast radius of a potential change so when the subject is understanding a large codebase, no single tool is sufficient. The `/teach` skill is a little lighter and tries to implement a teaching philosophy that brings you up to speed on something new in a user friendly way, great for diving in quickly without getting too overwhelmed, especially where the existing documentation is lacking or stale.

`/teach me about {{~/repo/.../codebase}} I'm new and want to get productive on this codebase`

## Engineering features

And finally we get to the feature development workflow. Note there are simple features where you may feel the risk of 'one shotting it' is low. That is simply asking the AI to implement something and letting it figure out the rest. That may sometimes be appropriate, but for most software that must survive the chaos of the real world at scale, a little more rigour is needed. This workflow tries to slot the human in where they have maximum impact and offloads to the AI where where it is safe to do so and accelerates feature delivery. 

### Define where you're going

Get some brief description of the feature e.g. from a product manager then

`/grill-with-docs {{description of the feature or @link-to-feature-doc}}`

Note that you should also break out and do research or create a prototype when you can't answer a question the AI asks you quickly. For example when discussing competing software libraries or UI design you may want to branch off into a little research instead of casually making a decision. To this without bloating the context window for the grilling session use

`/handoff {{what the next session will be for}}` to create a handoff document in your system
tmp directory which captures all the context captured so far that is relevant for the research or prototyping

then in a separate session/terminal 
`/software-design-research {{describe what you eventually want to implement and or @handoff-document}}` to have an agent search the web for say which frameworks to use or what other people have done to solve a technical challenge and iterate over options. It creates a research document with multiple options and recommendations

or
`/prototype {{describe-what-you-want-to-prototype}}` this either builds several UIs for front end prototypes or several terminal apps that demonstrate different backend logic

Simply `resume grilling` in the original grilling session when you're ready

### Write the destination details to a spec

Immediately after the grilling, in the same session while all the answers are in the context, create spec with `/to-spec`

You could skip this and go straight to issues (next section) but I find it useful to have user stories to refer back to later for human reviews and testing

### Define how to get there

If in the same session as the grilling `/to-issues` 
Or start a new context window and `/to-issues @spec-file`

This creates a set of issues, that each declare thier dependencies on other issues and are labelled ready-for-agent or ready-for-human. It uses the concept of tracer bullets to decompose the spec into slices that each demonstrate some useful output.

It's worth noting that people often seem to assume tracer bullets mean you need to produce a UI component and then start asking about mono-repos vs multi-repos. Think of tracer bullets as producing whatever your consumers consume. If you're a back end team producing a set of APIs, it could be a single endpoint or even a thin initial implementation of an endpoint including the minimum data required to test that endpoint.

Real tracer bullets, as in artillery, function to show where the bullets are eventually going, so the gunner can keep turning the gun towards the intended target. Software tracer bullets capture the same spirit. You want to produce something that your stakeholders (which may be another engineering team) can engage with, because it's easier to evaluate whether that has taken you closer to your stated destination, and if not its easier to understand how to evolve it so it does.

In practice coding agents tend to interpret the spirit of tracer bullets quite well with this skill, they decompose specs into multiple seperate implementations that make it relatively easy to judge if real progress has been made. If a feature spans several repos each managed by different teams, your tracer bullet is generally some consumable that is within your repo. But if your team manages multiple repos, you can also have sub folders for each repo in a parent folder and instantiate the AI coding agent in the parent folder so it can operate across all repos.

### Implementation

If you want to baby sit the implementation for each issue prompt the coding agent as follows
`select an issue that has no dependencies or has all dependencies met from {{your issue tracker e.g. github issue board}} and implement it using the implement skill`

That however leaves a lot of productivity on the table. To do more hands off implementation run a loop (see next section for a concrete implementation) which selects the next issue in this priority order and implements it:
1. Critical bug fixes
2. Development infrastructure
3. Tracer bullets for new features
4. Polish and quick wins
5. Refactors

Then returns some text sequence when there are no more issues that is used to terminate the loop. The implementation need not be strictly sequential, since all issues declare their dependencies, it is possible to spin up multiple agents working on multiple issues in parralel in different work trees that are then merged before implementing the next wave. That is what the implemented example described later does.

#### Automated iteration with pysolated or sandcastle

Pysolated (Python based) and Sandcastle (Typescript based) can spin up several different types of 
sandbox (e.g. docker, podman, vercel ...) and execute the implementation loop described above with your chosen coding agent.

It can iteratively issue a prompt which selects the next task in the priority order above and returns
one or more completion tags which can be used to terminate the loop or wait for a user to complete
human in the loop dependencies

Pysolated can be found at https://pypi.org/project/pysolated/ or https://github.com/rdhayden/pysolated, simply install it into your project
Sandcastle can be found at https://github.com/mattpocock/sandcastle

See the .pysolated directory in this repo for an example implementation of the loop using podman as the sandbox

After installing Pysolated you need to initialise it first to create a Container file and other bits using `uv run pysolated init` 
Then build the container image with `uv run pysolated podman build-image`
Then make sure your main script and prompt reflect the loop you want to implement. The example main.py in
the .pysolated folder implements issues in parralel where possible to minimise implementation time. See the README.md in the .pysolated folder for details of this example script

#### Review

TODO - (note review skill called from implement, review that if this gets triggered by a script or create that skill) create another script using pysolated to run review agents from compound engineering https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/skills/ce-code-review/SKILL.md
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

#### Documentation and human review

TODO
	- Update readme docs to add descriptions of new features, update usage instructions to incorporate  new features added, and updates to how to install it if that has changed
	- Update architecture doc with
		- add any new components to the mermaid C4 component diagram
		- add unique number to each integration point along with its label
		- add any new tests to testing section which lists integration point number, and description component x component y with each of the tests associated with that integration also numbered
	- Then agent 
		- reviews every user story in the spec against test cases, if any user stories are not tested, add tests, 
		- also checks if any component interfaces are not tested and if so add tests
		- runs any new tests until they pass
		- finally create a pull request on the spec issue that adds link to architecture doc and readme, lists tests for each user story and tests against any component interface added or changed, describe what was updated in the readme if anything  
		- user must tick
			- each user story manually tested
			- confirm automated tests for each user story are complete and correct
			- confirm automated tests for each interface between components touched are complete and correct
			- confirm architecture doc is correct and cmplete
			- confirm the readme is crrect and complete
 
#### Commit hooks

Run a git precommit hook to run tests and typechecks if appropriate before any commit completes. You need to setup Husky (https://typicode.github.io/husky/) or Pre-commit (https://pre-commit.com/) to invoke pre-commit hooks

Husky is written in Typescript and Pre-commit in Python but both support running pre-commit hooks written in any language (e.g. you can run ruff and mypy for Python projects from Husky)

Note that the original `/implement` skill included the instruction 'Run typechecking regularly, single test files regularly, and the full test suite once at the end.' The full test suite instruction was removed because in this workflow that is run reliably by the pre-commit hook and the agent will see that output when it attempts to commit anyway. If you don't implement the pre-commit hook then add that instruction into the implement skill, but a pre-commit hook is guaranteed. In theory the agent could disregard your instruction although in practice it generally won't, but there's no good reason to leave that as an unmitigated risk, pre-commit hooks are more deterministic so they are preffered in this workflow.