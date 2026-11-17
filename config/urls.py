from django.contrib import admin
from django.urls import include, path

from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("health", views.health, name="health"),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("admin/", admin.site.urls),
]
