# AGENTS.md

This file provides guidance to Claude Code (and other agentic coding tools) when working with code in this repository.

## Overview

Minimal Django project (Django >=6.1.1, Python 3.14, managed with `uv`) that demos a "legacy" shared model and an agentic blast-radius-check workflow for multi-repo dependency safety.

- `config/` — Django project package (settings, urls, wsgi/asgi). Only `admin/` is routed.
- `app_legacy/` — the single app. Contains `LegacyModel` (registered in the admin) and one initial migration. `tests.py` is an empty placeholder.
- `.claude/skills/check-blast-radius/` — the skill that powers the blast-radius workflow described in `ARCHITECTURE.md`.
- `.github/workflows/blast-radius-check.yml` — the CI-side trigger for the same skill, required on PRs targeting `develop`.
- Database is SQLite at `db.sqlite3` (gitignored/untracked).

## Commands

```bash
uv sync                                  # install deps into .venv
uv run python manage.py runserver        # dev server (admin at /admin/)
uv run python manage.py migrate
uv run python manage.py makemigrations
uv run python manage.py test             # all tests
uv run python manage.py test app_legacy.tests.SomeTest.test_x   # single test
```

No linter or formatter is configured.

## Constraints on `LegacyModel`

`app_legacy/models.py` documents `LegacyModel` as a shared, Oracle-backed entity (since 2015) consumed by three downstream repos: `reporting-service`, `sync-service`, and `auth-gateway`. Changing its fields, the `legacy_code` uniqueness, or the signature/behavior of `legacy_code_upper()` has a known blast radius outside this repo.

Before editing anything on `LegacyModel`, run the `check-blast-radius` skill (`.claude/skills/check-blast-radius/SKILL.md`) — manually via `/check-blast-radius`, or let it trigger automatically on a matching natural-language prompt. See `docs/ARCHITECTURE.md` for the full design, including the CI-enforced counterpart of this same check..