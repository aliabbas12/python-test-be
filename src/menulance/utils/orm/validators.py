from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

basic_name_validator = RegexValidator(
    regex="^[a-zA-Z,.'-]*$",
    message=_("Only these special characters are allowed: ,.'-"),
)
