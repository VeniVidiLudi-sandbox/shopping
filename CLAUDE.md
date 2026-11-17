# Shopping

(The worker fills this in from the brief: what the app is for, who uses it, its core features.
The brief's first line is in `app/description.txt`, which the home page shows.)

## How this repo works
- Django 5.2 + Postgres, started from the platform's Django template. The platform's rules are in
  `/etc/claude-code/CLAUDE.md`; `platform.yaml` and `compose.yaml` say how the platform runs it.
- Settings come only from environment variables (`config/settings.py`).
- Login is the platform's login service (OIDC, `app/auth.py`). Members of `superadmin` are Django
  superusers. Apps keep no passwords.
- Dependencies: edit `pyproject.toml`, then `uv lock`. The image installs exactly what `uv.lock` says.
- Tests: `DJANGO_TEST_SQLITE=1 SECRET_KEY=test uv run pytest`.
- Migrations must also work with the previous release's code (add now, remove later).

## Next steps
(The worker keeps this list for the owner.)
