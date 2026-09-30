# legacy-core (demo)

A minimal Django project standing in for a large legacy codebase
with three downstream dependent repositories
(`reporting-service`, `sync-service`, `auth-gateway`).

Built to sketch an agentic debugging/blast-radius workflow — see
[ARCHITECTURE.md](./docs/ARCHITECTURE.md) for the full design.

## Commands

```bash
uv sync                                  # install deps into .venv
uv run python manage.py runserver        # dev server (admin at /admin/)
uv run python manage.py migrate
uv run python manage.py makemigrations
uv run python manage.py test             # all tests
uv run python manage.py test app_legacy.tests.SomeTest.test_x   # single test
```