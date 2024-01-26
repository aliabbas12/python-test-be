"""
Django settings for Menulance Backend (API).
"""
import datetime

from corsheaders.defaults import default_headers

from accounts.jwt_token_claims import JwtClaims
from menulance.settings_base import *

# TODO: Roberto: Verify authentication schemes (token authentication or JWT along with OAuth?)
# TODO: If going with Token Authentication, implement using Django REST Knox
# Application definition
INSTALLED_APPS += [
    # third party
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
]

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

# django-rest-framework settings
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("utils.drf.renderers.CamelCaseJSONRenderer",),
    "DEFAULT_PARSER_CLASSES": ("utils.drf.parsers.CamelCaseJSONParser",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "accounts.authentication.MenulanceJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("accounts.permissions.IsAuthenticatedUser",),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_VERSION": "v1",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "menulance.api.exceptions.custom_exception_handler",
}
# django-rest-framework-simplejwt settings
_JWT_EXPIRATION_DELTA_IN_MINUTES = datetime.timedelta(
    minutes=int(env("JWT_EXPIRATION_DELTA_IN_MINUTES", 60 * 24 if DEBUG else 60))
)
_JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS = datetime.timedelta(
    minutes=int(env("JWT_EXPIRATION_DELTA_IN_MINUTES", 60 * 24 if DEBUG else 120))
)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": _JWT_EXPIRATION_DELTA_IN_MINUTES,
    "REFRESH_TOKEN_LIFETIME": _JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS,
    # Rotate refresh token on usage
    "ROTATE_REFRESH_TOKENS": True,
    # Don't allow same refresh token to be reused
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    # Signing. Verify key not needed for HMAC algorithms
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    # Request Auth Header: {"Authorization": "Bearer ..."}
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # User id field
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": JwtClaims.USER_ID.value,
    # User must have is_active=True
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    # Sliding token config
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": _JWT_EXPIRATION_DELTA_IN_MINUTES,
    "SLIDING_TOKEN_REFRESH_LIFETIME": _JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS,
    # Log out user after password change
    "CHECK_REVOKE_TOKEN": True,
    "REVOKE_TOKEN_CLAIM": "rtc",
}

# drf-yasg settings
# https://drf-yasg.readthedocs.io/en/stable/settings.html
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "PERSIST_AUTH": True,
    "REFETCH_SCHEMA_WITH_AUTH": True,
    "REFETCH_SCHEMA_ON_LOGOUT": True,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
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
).split(",")
