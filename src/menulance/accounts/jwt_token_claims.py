from enum import Enum


class JwtClaims(str, Enum):
    USER_ID = "uid"
    EMAIL = "email"
    IS_SUPERUSER = "su"
