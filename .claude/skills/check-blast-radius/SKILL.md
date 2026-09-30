---
name: check-blast-radius
description: Use this skill whenever a developer changes a shared/legacy module (a model, function, or class consumed by other repositories) and wants to know which downstream codebases might break. Trigger on phrases like "check the impact of this change", "does this break other repos", "blast radius", "what depends on this", or when reviewing a diff that touches a known shared module.
---

# Check Blast Radius

## Purpose
Given a code change in this repository, determine which of the
dependent downstream repositories (reporting-service, sync-service,
auth-gateway) reference the changed symbol(s), and summarize the
risk in plain language.

## Steps

1. **Identify changed symbols.**
   Inspect the current diff (staged changes, or the PR diff when
   running in CI) and extract the names of changed classes,
   functions, and methods.

2. **Query the dependency graph.**
   Call the `dependency-graph` MCP tool's `get_consumers(symbol)`
   for each changed symbol. This returns a structural list of
   files/repos that import or call it — not a semantic guess.

3. **Query the codebase search index (if consumers are found).**
   For each consumer found, call the `codebase-search` MCP tool's
   `search_code(query)` to retrieve the actual usage snippet, so the
   summary can explain *how* it's used, not just *that* it's used.

4. **Summarize.**
   Produce a short, structured report:
   - Which repos are affected, and where (file:line)
   - A one-line explanation of how each usage could break
   - A suggested next action (which tests to run, or who to notify)

5. **Recommend, never block.**
   This skill only informs. It does not modify code, revert
   changes, or halt the commit/PR on its own. The developer (or,
   in CI, a required PR check) decides how to proceed.

## Output format

```
Blast radius: <N> of <total> dependent repos affected

<repo-name>: <symbol> used in <file>:<line>
  → <one-line explanation>

Suggested: <concrete next step>
```


## Notes
- Depth is configurable: default checks direct consumers only.
  Pass `--deep` to also resolve transitive (second-degree)
  consumers — slower, used mainly in the CI/PR path, not the local
  fast path.
- This skill is intentionally the *only* place this logic lives.
  Both the local invocation and the CI workflow
  (`.github/workflows/blast-radius-check.yml`) call this same
  skill — no duplicated logic between environments.