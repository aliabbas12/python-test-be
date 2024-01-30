import abc
import typing

from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _


class CreatedAtUpdatedAtModelMixin(models.Model):
    """
    Everything needed to implement created_at and updated_at functionality to models.

    This means that created_at and updated_at fields should not be defined or edited in the other models. Updated at
    field will get overwritten regardless.
    """

    created_at = models.DateTimeField(
        verbose_name=_("Entity created at"),
        null=False,
        default=timezone.now,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Entity updated at"), null=True, blank=True
    )

    class Meta:
        abstract = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.updated_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)


class SoftDeletableModelMixin(models.Model):
    # Flag to mark the user as being in the deletion process
    is_being_deleted = models.BooleanField(_("Is being deleted?"), default=False)

    @property
    def soft_delete_attributes(self) -> typing.Dict[str, typing.Any]:
        return {}

    def soft_delete(
        self, override_soft_delete_attributes: typing.Dict[str, typing.Any] = None
    ):
        self.is_being_deleted = True
        override_soft_delete_attributes = override_soft_delete_attributes or []
        for attribute, value in list(self.soft_delete_attributes.items()) + list(
            override_soft_delete_attributes.items()
        ):
            setattr(self, attribute, value)
        self.save()

    class Meta:
        abstract = True
