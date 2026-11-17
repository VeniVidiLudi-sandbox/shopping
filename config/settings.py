"""Settings from the environment only (platform rules, plan §5). The
platform injects APP_ENV, APP_VERSION, APP_URL, SECRET_KEY, DATABASE_URL
and OIDC_*; nothing secret has a fallback."""
import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
APP_ENV = os.environ.get("APP_ENV", "dev")
APP_VERSION = os.environ.get("APP_VERSION", "dev")
APP_URL = os.environ.get("APP_URL", "http://localhost:8000")
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("DJANGO_DEBUG") == "1"

_host = urlparse(APP_URL).hostname or "localhost"
ALLOWED_HOSTS = [_host, "localhost", "127.0.0.1"] + [
    h for h in os.environ.get("EXTRA_ALLOWED_HOSTS", "").split(",") if h]
CSRF_TRUSTED_ORIGINS = [APP_URL]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = APP_URL.startswith("https://")
USE_X_FORWARDED_HOST = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mozilla_django_oidc",
    "app",
]
MIDDLEWARE = [
    "app.middleware.HealthMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "app.context.platform",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"


def _database():
    url = os.environ.get("DATABASE_URL")
    if not url:
        if os.environ.get("DJANGO_COLLECTSTATIC") or os.environ.get("DJANGO_TEST_SQLITE"):
            return {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "test.sqlite3"}
        raise RuntimeError("DATABASE_URL isn't set")
    u = urlparse(url)
    return {"ENGINE": "django.db.backends.postgresql", "NAME": u.path.lstrip("/"), "USER": u.username,
            "PASSWORD": u.password, "HOST": u.hostname, "PORT": u.port or 5432, "CONN_MAX_AGE": 60}


DATABASES = {"default": _database()}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"}}

# Login: the platform's login service (Authelia) over OIDC. Apps keep no
# passwords. `superadmin` maps to Django's superuser and staff (plan §7).
OIDC_ISSUER = os.environ.get("OIDC_ISSUER", "").rstrip("/")
OIDC_RP_CLIENT_ID = os.environ.get("OIDC_CLIENT_ID", "")
OIDC_RP_CLIENT_SECRET = os.environ.get("OIDC_CLIENT_SECRET", "")
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_SCOPES = "openid profile email groups"
OIDC_OP_AUTHORIZATION_ENDPOINT = f"{OIDC_ISSUER}/api/oidc/authorization"
OIDC_OP_TOKEN_ENDPOINT = f"{OIDC_ISSUER}/api/oidc/token"
OIDC_OP_USER_ENDPOINT = f"{OIDC_ISSUER}/api/oidc/userinfo"
OIDC_OP_JWKS_ENDPOINT = f"{OIDC_ISSUER}/jwks.json"
OIDC_USE_PKCE = True
AUTHENTICATION_BACKENDS = ["app.auth.PlatformOIDCBackend"]
LOGIN_URL = "oidc_authentication_init"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

LOGGING = {"version": 1, "disable_existing_loggers": False,
           "handlers": {"console": {"class": "logging.StreamHandler"}},
           "root": {"handlers": ["console"], "level": "INFO"}}
