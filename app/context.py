from pathlib import Path

from django.conf import settings

# The one-line description from the brief, as plain text: the template
# escapes it like any other value (never pasted into markup or code).
_DESCRIPTION = Path(__file__).with_name("description.txt")


def platform(request):
    try:
        description = _DESCRIPTION.read_text(encoding="utf-8").strip()
    except OSError:
        description = ""
    return {"app_env": settings.APP_ENV, "app_version": settings.APP_VERSION, "app_description": description}
