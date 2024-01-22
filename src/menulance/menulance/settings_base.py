import enum
import logging
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

env = os.environ.get


def get_bool_env(key, default=None):
    value = os.environ.get(key, None)
    if value is None:
        return default
    if value.isdigit():
        return bool(int(value))
    return value.lower() == "true"


# Load dotenv files
load_dotenv()
load_dotenv("../../../app.default.env", override=True)


# BASE DIRS
resolved_path = Path(__file__).resolve()
BASE_DIR = resolved_path.parent.parent
MODULE_BASE_DIR = BASE_DIR.parent
PROJECT_BASE_DIR = MODULE_BASE_DIR.parent


# Environment
class ServerEnvironment(enum.Enum):
    DEV = "dev"
    STAGE = "stage"
    PRODUCTION = "production"


# This will fail deployment if a valid env string is not provided
ENVIRONMENT = ServerEnvironment(env("ENVIRONMENT", "dev"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")
if ENVIRONMENT == ServerEnvironment.DEV and not SECRET_KEY:
    SECRET_KEY = "django-insecure-this-key-is-unsafe!!!!"
elif (
    ENVIRONMENT in (ServerEnvironment.STAGE, ServerEnvironment.PRODUCTION)
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
SERVICE_ID = env("SERVICE_ID", "api")
# TODO: Self domain recognition

# TODO: This and CORS configuration in API settings
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

# Application definition
INSTALLED_APPS = [
    # Django Defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party
    "corsheaders",
    # Menulance
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
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

# Other essential Configurations / Misc Configurations
WSGI_APPLICATION = "menulance.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "menulance.urls"
# TODO: Implement the suer model as needed by the applicaiton
# AUTH_USER_MODEL = "accounts.User"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "menulance"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", None),
        "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
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


# Internationalization and Localization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Figure out how to implement a CDN into media implementation
MEDIA_ROOT = env("MEDIA_ROOT", os.path.join(os.path.dirname(BASE_DIR), "media"))

# We probably don't need a static implementation, but we are still going to define one static root so if later we do
# bring in something, we can just implement it as it is
STATIC_ROOT = os.path.join(
    os.environ.get("STATIC_ROOT", os.path.join(BASE_DIR, "static")),
    SERVICE_ID,
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# See django-storages section for STATIC_URL and STATICFILES_STORAGE
STATIC_ROOT = os.path.join(
    env("STATIC_ROOT", os.path.join(os.path.dirname(BASE_DIR), "static")), SERVICE_ID
)
