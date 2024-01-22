"""
Django settings for Menulance Backend (API).
"""

from corsheaders.defaults import default_headers

from menulance.settings_base import *

# TODO: Roberto: Verify authentication schemes (token authentication or JWT along with OAuth?)
# TODO: If going with Token Authentication, implement using Django REST Knox
# Application definition
INSTALLED_APPS += [
    # third party
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "drf_yasg",
]

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

# django-rest-framework settings
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("utils.drf.renderers.CamelCaseJSONRenderer",),
    "DEFAULT_PARSER_CLASSES": ("utils.drf.parsers.CamelCaseJSONParser",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("accounts.permissions.IsAuthenticatedUser",),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_VERSION": "v1",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "menulance.api.exceptions.custom_exception_handler",
}

REST_CUSTOM_SETTINGS = {
    "DEFAULT_QUERY_PARAMETER_PARSER_CLASS": "utils.drf.parsers.CamelCaseJSONQueryParameterParser",
}

# drf-yasg settings
# https://drf-yasg.readthedocs.io/en/stable/settings.html
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "PERSIST_AUTH": True,
    "REFETCH_SCHEMA_WITH_AUTH": True,
    "REFETCH_SCHEMA_ON_LOGOUT": True,
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "description": "Token",
            "name": "Authorization",
            "in": "header",
        },
    },
}

# django-cors-header settings
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_HEADERS = default_headers + ("content-disposition",)
CORS_ALLOWED_ORIGINS = (
    env("CORS_ALLOWED_ORIGINS", "http://localhost:8000") or "http://localhost:8000"
)

# drf-rest-auth settings
# TODO: Verify with frontend team
# https://github.com/iMerica/dj-rest-auth
REST_AUTH = {"JWT_AUTH_COOKIE": "__Secure-token"}
