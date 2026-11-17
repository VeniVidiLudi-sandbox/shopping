from django.contrib.auth.decorators import login_required
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
