"""Development settings."""
from .base import *

DEBUG = True

INSTALLED_APPS += ["django_extensions"]

# Django Debug Toolbar
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable HTTPS redirects in development
SECURE_SSL_REDIRECT = False

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True
