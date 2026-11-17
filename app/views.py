from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST


from .middleware import HealthMiddleware
from .models import Heartbeat, Item

# /health is answered by HealthMiddleware; this is only for the URL name.
health = HealthMiddleware(lambda request: None)


def home(request):
    ctx = {"last_heartbeat": Heartbeat.objects.first()}
    if request.user.is_authenticated:
        ctx["items"] = Item.objects.select_related("added_by", "ordered_by")
    return render(request, "app/home.html", ctx)


@login_required
@require_POST
def add_item(request):
    text = " ".join(request.POST.get("text", "").split())[:120]
    if text:
        Item.objects.create(text=text, added_by=request.user)
    return redirect("home")


@login_required
@require_POST
def toggle_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.ordered = not item.ordered
    item.ordered_by = request.user if item.ordered else None
    item.ordered_at = timezone.now() if item.ordered else None
    item.save()
    return redirect("home")


_FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<g transform="rotate(-6 32 32)"><rect x="8" y="10" width="48" height="46" rx="3" fill="#fff176" '
    'stroke="#d9b800" stroke-width="2"/>'
    '<path d="M18 30l8 9 20-20" fill="none" stroke="#2b2a33" stroke-width="6" stroke-linecap="round" '
    'stroke-linejoin="round"/></g>'
    '<circle cx="32" cy="10" r="6" fill="#e53935" stroke="#9c1c1c" stroke-width="1.5"/></svg>'
)


def favicon(request):
    r = HttpResponse(_FAVICON, content_type="image/svg+xml")
    r["Cache-Control"] = "public, max-age=86400"
    return r
