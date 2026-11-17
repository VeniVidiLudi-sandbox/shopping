from django.db import connection
from django.http import HttpResponse, JsonResponse


class HealthMiddleware:
    """Answers /health before host checking: the platform's health checks
    reach the container by its own name, not the site's (plan §5)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/health":
            try:
                with connection.cursor() as c:
                    c.execute("SELECT 1")
            except Exception:  # noqa: BLE001
                return JsonResponse({"ok": False}, status=503)
            return HttpResponse("ok", content_type="text/plain")
        return self.get_response(request)
