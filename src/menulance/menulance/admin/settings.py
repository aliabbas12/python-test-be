"""
Django settings for Menulance Backend (Admin).
"""
from menulance.settings_base import *

# Application definition
INSTALLED_APPS.insert(0, "django.contrib.admin")

INSTALLED_APPS += [
    "django.contrib.sessions",
    "django.contrib.messages",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
] + MIDDLEWARE

TEMPLATES[0]["DIRS"] = [os.path.join(BASE_DIR, "menulance/admin/templates")]
