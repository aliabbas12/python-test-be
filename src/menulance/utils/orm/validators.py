from django.core.validators import RegexValidator

basic_name_validator = RegexValidator(regex="[a-zA-Z.'-]")
