# Shopping

A simple shared shopping list for one family, used mostly on phones (mobile-first). Everyone adds
what's needed; whoever does the ordering marks items as ordered.

- Shared list of "post-it" items (colourful, slightly rotated, handwritten font) on `/`.
- Any signed-in user adds an item (short text); each shows who added it and how long ago.
- "Ordered" button ticks an item: it fades, is struck through, and moves below the outstanding
  items; "Undo" reverses a mis-tap. Model: `app.models.Item`; views in `app/views.py`.
- Identity: the platform's OIDC login (platform rule: no app passwords), so family members are
  accounts in the login service rather than created in Django admin. Signed-out visitors see only a sign-in link.
- `manage.py seed` adds a few sample items in dev.

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
- Check the look on a real phone; tweak colours/tilt/fonts (Caveat loads from Google Fonts, falls back to cursive).
- Possible additions: edit/delete an item, "clear ordered" after delivery, quantities, live refresh.
- Ensure each family member has an account in the login service.
