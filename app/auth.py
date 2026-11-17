"""Users come from the platform's login service (plan §7). A user row is
linked by the OIDC `sub`; on first login an existing row with the same
email is adopted. Membership of `superadmin` makes a superuser and staff,
and is checked at every login, so removing someone from the group takes
effect at their next login."""
from django.contrib.auth import get_user_model
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from .models import Profile


class PlatformOIDCBackend(OIDCAuthenticationBackend):
    def filter_users_by_claims(self, claims):
        sub = claims.get("sub")
        if not sub:
            return get_user_model().objects.none()
        linked = get_user_model().objects.filter(profile__oidc_sub=sub)
        if linked.exists():
            return linked
        email = claims.get("email")
        if email:
            return get_user_model().objects.filter(email__iexact=email, profile__isnull=True)
        return get_user_model().objects.none()

    def _apply(self, user, claims):
        user.username = claims.get("preferred_username") or user.username or claims["sub"]
        user.email = claims.get("email", user.email)
        user.first_name = (claims.get("name") or "")[:150]
        admin = "superadmin" in (claims.get("groups") or [])
        user.is_superuser = user.is_staff = admin
        user.save()
        Profile.objects.update_or_create(user=user, defaults={"oidc_sub": claims["sub"]})
        return user

    def create_user(self, claims):
        user = get_user_model().objects.create_user(
            username=claims.get("preferred_username") or claims["sub"], email=claims.get("email", ""))
        return self._apply(user, claims)

    def update_user(self, user, claims):
        return self._apply(user, claims)
