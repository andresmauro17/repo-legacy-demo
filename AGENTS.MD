# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Minimal Django project (Django >=6.1.1, Python 3.14, managed with `uv`) that demos a "legacy" shared model. `README.md` is empty and `main.py` is an unused stub; the real entry point is `manage.py`.

- `config/` — Django project package (settings, urls, wsgi/asgi). Only `admin/` is routed.
- `app_legacy/` — the single app. Contains `LegacyModel` (registered in the admin) and one initial migration. `tests.py` is an empty placeholder.
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

`app_legacy/models.py` documents `LegacyModel` as a shared, Oracle-backed entity (since 2015) consumed by three downstream repos: `reporting-service`, `sync-service`, and `auth-gateway`. Changing its fields, the `legacy_code` uniqueness, or the signature/behavior of `legacy_code_upper()` has a known blast radius outside this repo, so treat those as breaking changes and flag them before editing. The docstring points to an `ARCHITECTURE.md` for details, but that file does not exist in this repo.
