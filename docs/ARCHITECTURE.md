# Architecture: Debugging Workflow for a Legacy Codebase with Dependent Repositories

## Scenario

This repository is a simplified stand-in for a large legacy codebase
depended on by three downstream repositories for example:
`reporting-service`, `sync-service`, and `auth-gateway`. A change to
a shared model or function here can silently break any of the three.

This document sketches a developer-experience-first workflow
(editor/CLI) for catching that risk early, using
Claude Code, skills, hooks, MCP servers, and a lightweight RAG +
dependency index.

## Problem framing (from experience)

At a previous role, I maintained a Django library shared across
~50 repositories. Updating a shared Oracle-backed model required
manually searching the organization's GitHub code search for every
consumer, checking each one out locally, and running it against the
modified library before trusting the change. It worked, but it was
slow, manual, and entirely dependent on my own memory and diligence.
This design automates that same reasoning.

## Components

1. **Knowledge layer — RAG + dependency graph**
   - Semantic RAG index over all 4 codebases (code + docstrings +
     commit messages) — retrieval instead of loading full repos.
   - Structural dependency graph (static analysis of imports/calls)
     — answers "who depends on X" precisely, which semantic
     similarity alone cannot.

2. **MCP servers**
   - `dependency-graph`: exposes `get_consumers(symbol)`.
   - `codebase-search`: exposes `search_code(query)`.
   - Both are long-running services, index kept fresh incrementally
     on every merge to `develop` — not rebuilt per invocation.

3. **Skill — `check-blast-radius`**
   See `.claude/skills/check-blast-radius/SKILL.md`. Single source
   of truth for the logic; invoked from two triggers, never
   duplicated.

4. **Instructions (`AGENTS.md` / `CLAUDE.md`)**
   Each of the 4 repos documents its own conventions; this file
   documents how they relate to each other.

5. **Trigger 1 — Manual, local, editor/CLI**
   Developer runs `/check-blast-radius` or asks in natural language
   inside Claude Code, while still writing code. Fast, optional,
   zero friction — informs design decisions early.

6. **Trigger 2 — Automatic, required, CI**
   `.github/workflows/blast-radius-check.yml` runs on every PR
   targeting `develop`, posting the result as a
   PR comment. This is the compliance guarantee — it does not
   depend on the developer remembering to run anything locally.

7. **Human in the loop**
   The skill only recommends; it never blocks or auto-fixes. A
   human decides whether to proceed, investigate further, or loop
   in the owning team of an affected repo.

## Flow

```
developer edits legacy-core
        |
        v
(optional) "/check-blast-radius" in Claude Code
        |
        v
skill calls dependency-graph + codebase-search (MCP)
        |
        v
summary printed in terminal - developer decides
        |
        v
git push -> PR opened against develop
        |
        v
GitHub Actions: blast-radius-check.yml (required)
        |
        v
same skill, headless mode, --deep (transitive)
        |
        v
comment posted on PR -- visible to reviewers
```

## Why this differs from off-the-shelf tools (e.g. Copilot PR review)

Copilot's PR review only sees the diff (and at most the repo it
lives in). It has no visibility into the 3 downstream repositories.
The dependency graph and codebase-search MCP servers here are what
make cross-repo blast-radius analysis possible at all.

## Next step (production path)

This skill currently lives inside this single repo for
demonstration purposes. In a real multi-repo, 400-developer
environment, it would be published as an internal Claude Code
plugin via a private marketplace, so all 4 repositories consume the
same versioned logic instead of duplicating it.