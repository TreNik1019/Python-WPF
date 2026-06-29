"""Django settings for the Frontend project."""

from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Do not store a production secret key in source control. Read from
# the environment instead. Prefer `django-environ` and a project `.env` file.
env = environ.Env()
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-fallback-key-only-for-development",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "patient",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
]

SECURE_CSP = {
    "default-src": ["'self'"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "script-src": ["'self'"],
    "img-src": ["'self'", "data:"],
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {}

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

# URL to use when referring to static files located in STATICFILES_DIRS.
STATIC_URL = "/static/"

# Additional directories where Django will look for static files
STATICFILES_DIRS = [BASE_DIR / "static"]

# Development server runs on port 8001, da FastAPI/Backend 8080/8000 nutzt.
# Start with: python manage.py runserver 8001
DJANGO_DEV_PORT = 8001

# Backend API URL used by the Django frontend services (can be overridden in
# environment-specific settings).
BACKEND_URL = env("BACKEND_URL", default="https://127.0.0.1:8000/rest")

# TLS-Zertifikatsprüfung für Requests an das Backend. In lokaler Entwicklung
# nutzt das Backend ein selbstsigniertes Zertifikat, daher Default = DEBUG.
# In Produktion (DEBUG = False) muss ein gültiges Zertifikat verwendet werden.
BACKEND_TLS_VERIFY = env.bool("BACKEND_TLS_VERIFY", default=not DEBUG)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Logging
# https://docs.djangoproject.com/en/6.0/topics/logging
# https://docs.python.org/3/howto/logging.html
# Analog zum Backend (config/logger.py): nur die eigenen App-Logger (Namespace
# "patient") bekommen einen zusaetzlichen Rotating-File-Sink (log/frontend.log,
# Rotation bei 1 MB) + Konsolen-Ausgabe. Djangos interne Logger (autoreload,
# db.backends, request, server) bleiben unangetastet und behalten ihre
# Standard-Konfiguration (django.utils.log.DEFAULT_LOGGING) - genauso wie beim
# Backend, wo loguru nur explizite eigene logger.*()-Aufrufe in die Datei
# schreibt und Uvicorn-/Framework-Rauschen unangetastet bleibt.
LOG_DIR = BASE_DIR / "log"
LOG_DIR.mkdir(exist_ok=True)
LOG_LEVEL = env("DJANGO_LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "frontend.log",
            "maxBytes": 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "patient": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}
