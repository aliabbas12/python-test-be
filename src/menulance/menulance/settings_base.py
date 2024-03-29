import enum
import logging
import os
from pathlib import Path

import sentry_sdk
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

env = os.environ.get


# TODO: Secrets management


def get_bool_env(key, default=None):
    value = env(key, None)
    if value is None:
        return default
    if value.isdigit():
        return bool(int(value))
    return value.lower() == "true"


# Some settings will be different if app is on docker
IS_ON_DOCKER = get_bool_env("ON_DOCKER", False)

# BASE DIRS
resolved_file_path = Path(__file__).resolve()
BASE_DIR = resolved_file_path.parent.parent
PROJECT_BASE_DIR = BASE_DIR.parent.parent
RUNTIME_HELPERS_DIR = os.path.join(BASE_DIR, "runtime_helpers")

if not IS_ON_DOCKER:
    # Load dotenv file for local non-docker development
    load_dotenv(os.path.join(PROJECT_BASE_DIR, "app.default.env"))
    load_dotenv(".env-local", override=True)


# Environment
class ServerEnvironment(str, enum.Enum):
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"


# This will fail deployment if a valid env string is not provided
ENVIRONMENT = ServerEnvironment(env("ENVIRONMENT", "dev"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")
if ENVIRONMENT == ServerEnvironment.DEV and not SECRET_KEY:
    SECRET_KEY = "django-insecure-this-key-is-unsafe!!!!"
elif (
    ENVIRONMENT in (ServerEnvironment.STAGING, ServerEnvironment.PRODUCTION)
    and not SECRET_KEY
):
    raise ImproperlyConfigured(
        f'A safe secret key must be defined in {ENVIRONMENT} deployment\'s environment variables ("DJANGO_SECRET_KEY")!'
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_env("DJANGO_DEBUG", False)
if DEBUG and ENVIRONMENT == ServerEnvironment.PRODUCTION:
    logging.warning(
        "Running Production server with DEBUG enabled. This is very dangerous!"
    )

# Custom attributes for determine further DJANGO settings, api is the default service setting
SERVICE_ID = env("SERVICE_ID", "api") or "api"

# TODO: Self domain recognition
APP_DOMAIN = env("APP_DOMAIN", "menulance.com") or "menulance.com"

# Allowed hosts
ALLOWED_HOSTS = None if not env("ALLOWED_HOSTS") else env("ALLOWED_HOSTS").split(",")

# allow loopback interface and service domain by default
if not ALLOWED_HOSTS and ENVIRONMENT == ServerEnvironment.DEV:
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        "host.docker.internal",
        "api",
    ]

# Allowed hosts injection without updating the main ALLOWED_HOSTS env variable
ALLOWED_HOSTS_ADD = (
    []
    if not env("ALLOWED_HOSTS_ADD", None)
    else os.environ["ALLOWED_HOSTS_ADD"].split(",")
)
if ALLOWED_HOSTS_ADD:
    ALLOWED_HOSTS += ALLOWED_HOSTS_ADD

# Application definition
INSTALLED_APPS = [
    # Menulance
    "accounts",
    # Django Defaults
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.staticfiles",
    # Third Party
    "corsheaders",
]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", "menulance"),
        "USER": env("POSTGRES_USER", "postgres"),
        "PASSWORD": env("POSTGRES_PASSWORD", None),
        "HOST": env("POSTGRES_HOST", "127.0.0.1"),
        "PORT": env("POSTGRES_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# TODO: Logging

# Internationalization and Localization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Figure out how to implement a CDN into media implementation
MEDIA_ROOT = env(
    "MEDIA_ROOT",
    os.path.join(os.path.dirname(PROJECT_BASE_DIR), "data", "media")
    if not IS_ON_DOCKER
    else "/var/www/data/media",
)
MEDIA_URL = "media/"

# We probably don't need a static implementation since this is an API
STATIC_ROOT = os.path.join(
    env("STATIC_ROOT", os.path.join(BASE_DIR, "staticfiles")), SERVICE_ID
)
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "assets")]

# Email settings
DEFAULT_FROM_EMAIL = f"Menulance <no-reply@{APP_DOMAIN}"
SERVER_EMAIL = "error@menulance.com"
EMAIL_SUBJECT_PREFIX = "[Menulance]"

_EMAIL_BACKEND_CHOICES = {
    "smtp": "django.core.mail.backends.smtp.EmailBackend",
    "console": "django.core.mail.backends.console.EmailBackend",  # Email to console stdout
    "file": "django.core.mail.backends.filebased.EmailBackend",
    "locmem": "django.core.mail.backends.locmem.EmailBackend",
    "dummy": "django.core.mail.backends.dummy.EmailBackend",  # Does nothing
}

_EMAIL_BACKEND_NAME = env("EMAIL_BACKEND", "console")
EMAIL_BACKEND = _EMAIL_BACKEND_CHOICES[_EMAIL_BACKEND_NAME]

# switch EMAIL_BACKEND when running in DEBUG mode
if DEBUG:
    EMAIL_BACKEND = _EMAIL_BACKEND_CHOICES[env("DEBUG_EMAIL_BACKEND", "console")]

# TODO: SMTP Config
if _EMAIL_BACKEND_NAME == "smtp":
    SMTP_DEFAULT_EMAIL_HOST = ""
    SMTP_DEFAULT_EMAIL_PORT = 25
    SMTP_EMAIL_USE_TLS = False
    SMTP_EMAIL_HOST_USER = ""
    SMTP_EMAIL_HOST_PASSWORD = ""
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = env("EMAIL_PORT")
    EMAIL_USE_TLS = env("EMAIL_USE_TLS")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# Django will send emails to these accounts if a code error occurs and DEBUG is False
ADMINS = [("Hassan Ahmed", "ahmed.hassan.112.ha@gmail.com")]

# TODO: System info application
# SYSTEM_DATA_ROOT = env(
#     "SYSTEM_DATA_ROOT", os.path.join(os.path.dirname(BASE_DIR), "system")
# )

# Interfacing with frontend config
FRONTEND_UI_BASE_URL = env("FRONTEND_UI_BASE_URL", "http://localhost:8000")
FRONTEND_UI_VERIFY_EMAIL_PATH = env(
    "FRONTEND_UI_VERIFY_EMAIL_URL", "/account/email-verification"
)

# TODO: Appropriate security middleware settings as needed
# TODO: Appropriate CSP settings as needed

# Sentry Configuration
# TODO: Test
SENTRY_DSN = env("SENTRY_DSN")
FORCE_SENTRY_IN_DEBUG = get_bool_env("FORCE_SENTRY_IN_DEBUG", False)

if SENTRY_DSN and (not DEBUG or FORCE_SENTRY_IN_DEBUG):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
        environment=ENVIRONMENT.value,
    )

"""Other essential Configurations / Misc Configurations"""
AUTH_USER_MODEL = "accounts.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "menulance.urls"
WSGI_APPLICATION = "menulance.wsgi.application"
# Start shell plus with ipython by default
SHELL_PLUS = "ipython"
CREATOR_ATTRIBUTE_NAME = "creator"

ALLOW_DJANGO_SHELL_PLUS = get_bool_env("ALLOW_DJANGO_SHELL_PLUS", False)
NOTEBOOK_ARGUMENTS = []
# Usually, never allow shell_plus and notebook allow-root on production
if not DEBUG or not ENVIRONMENT == ServerEnvironment.PRODUCTION:
    ALLOW_DJANGO_SHELL_PLUS = False
if ALLOW_DJANGO_SHELL_PLUS:
    NOTEBOOK_ARGUMENTS = [
        "--ip",
        "0.0.0.0",
        "--port",
        env("DJANGO_SHELL_PLUS_PORT", "8888"),
        "--allow-root",
    ]

# Load admin application?
LOAD_ADMIN_APP = SERVICE_ID != "admin" and get_bool_env("LOAD_ADMIN_APP", False)

if LOAD_ADMIN_APP:
    from menulance.admin.settings import *
