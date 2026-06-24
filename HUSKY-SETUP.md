# Setting up Husky

## What it is

A framework to make it easier to implement pre-commit checks using a git pre-commit hook

## Install and initialize Husky

`pnpm install --save-dev husky`
`pnpm exec husky init`

## Create a .husky/pre-commit file that runs your checks

Create a .husky/pre-commit file that runs your checks. Example content:

```
pnpm typecheck
pnpm test
npx lint-staged
```

If any step fails, the commit is blocked and the AI gets an error message.

## Set Up Automatic Code Formatting

Use lint-staged with Prettier to auto-format code before commits.

lint-staged runs arbitrary shell tasks with the list of staged git files, 
this ensures you only run linting on the specific files you have updated instead of an 
expensive lint run on the entire codebase

Install lint-staged:

`pnpm install --save-dev lint-staged`

Configure .lintstagedrc:

```
{
  "*": "prettier --ignore-unknown --write"
}
```

This runs Prettier on all staged files and automatically restages them. 
All AI-generated code now conforms to your formatting standards.

For javascript and typescript we could also run ESLint here since it works nicely with lint-staged.
