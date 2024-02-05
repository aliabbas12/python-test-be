from django.db import models
from accounts.models import User
from utils.orm.model_mixins import CreatedAtUpdatedAtModelMixin
from django.utils.translation import gettext_lazy as _
from utils.orm.validators import basic_name_validator


class ContactFormEntry(CreatedAtUpdatedAtModelMixin):
    email = models.EmailField(_("Email address"))
    first_name = models.CharField(
        _("First name"), max_length=50, validators=[basic_name_validator]
    )
    last_name = models.CharField(
        _("Last name"), max_length=50, validators=[basic_name_validator]
    )
    message = models.TextField(_("Message"))
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_("Creator"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "ContactFormEntry"
        verbose_name_plural = "ContactFormEntries"
