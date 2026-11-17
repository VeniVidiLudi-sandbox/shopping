import pytest
from django.contrib.auth import get_user_model

from app.auth import PlatformOIDCBackend
from app.models import Heartbeat


@pytest.mark.django_db
def test_health_and_home(client):
    assert client.get("/health").status_code == 200
    r = client.get("/")
    assert r.status_code == 200 and b"Sign in" in r.content


@pytest.mark.django_db
def test_superadmin_maps_to_superuser_and_follows_the_group():
    b = PlatformOIDCBackend()
    claims = {"sub": "s1", "preferred_username": "owner", "email": "o@example.com", "groups": ["superadmin"]}
    u = b.create_user(claims)
    assert u.is_superuser and u.is_staff
    assert list(b.filter_users_by_claims(claims)) == [u]
    u = b.update_user(u, claims | {"groups": ["dev-access"]})
    assert not u.is_superuser and not u.is_staff


@pytest.mark.django_db
def test_existing_user_is_adopted_by_email():
    old = get_user_model().objects.create_user(username="legacy", email="friend@example.com")
    found = list(PlatformOIDCBackend().filter_users_by_claims({"sub": "s2", "email": "FRIEND@example.com"}))
    assert found == [old]


@pytest.mark.django_db
def test_jobs():
    from django.core.management import call_command
    call_command("seed")
    call_command("heartbeat")
    assert Heartbeat.objects.count() == 2


@pytest.mark.django_db
def test_the_description_is_escaped(client, tmp_path, monkeypatch):
    from app import context
    d = tmp_path / "description.txt"
    d.write_text("{{ evil }} {% load x %} <script>alert(1)</script>\n")
    monkeypatch.setattr(context, "_DESCRIPTION", d)
    body = client.get("/").content.decode()
    assert "&lt;script&gt;" in body and "<script>alert" not in body and "{{ evil }}" in body


@pytest.mark.django_db
def test_list_add_and_order(client):
    from app.models import Item
    u = get_user_model().objects.create_user(username="mum", first_name="Mum")
    assert client.post("/add", {"text": "Milk x2"}).status_code == 302
    assert Item.objects.count() == 0  # anonymous can't add
    client.force_login(u)
    client.post("/add", {"text": "Milk x2"})
    client.post("/add", {"text": "  "})
    i = Item.objects.get()
    assert i.added_by == u
    body = client.get("/").content.decode()
    assert "Milk x2" in body and "Mum" in body
    client.post(f"/item/{i.pk}/toggle")
    i.refresh_from_db()
    assert i.ordered and i.ordered_by == u
    client.post(f"/item/{i.pk}/toggle")
    i.refresh_from_db()
    assert not i.ordered and i.ordered_by is None
