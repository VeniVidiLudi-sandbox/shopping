from django.contrib import admin
from django.urls import include, path

from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add", views.add_item, name="add_item"),
    path("item/<int:pk>/toggle", views.toggle_item, name="toggle_item"),
    path("health", views.health, name="health"),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("admin/", admin.site.urls),
]
