from django.db import models
from django.template.loader import render_to_string
from accounts.models import User
from utils.orm.model_mixins import CreatedAtUpdatedAtModelMixin
from django.utils.translation import gettext_lazy as _


class Font(CreatedAtUpdatedAtModelMixin):
    name = models.CharField(max_length=32, unique=True)


class Language(CreatedAtUpdatedAtModelMixin):
    name = models.CharField(max_length=64)
    short_code = models.CharField(max_length=32, unique=True)


class ManuallyTranslatedWord(CreatedAtUpdatedAtModelMixin):
    original_word = models.CharField(max_length=255)
    from_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="manual_translations_from"
    )
    translated_text = models.CharField(max_length=255)
    to_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="manual_translations_to"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            "original_word",
            "from_language",
            "to_language",
            "created_by",
        ]

    @property
    def _creator_email(self):
        return self.created_by.email

    def send_email_to_creator(self, updated=False):
        context = {
            "site_name": "Menulance",
            "original_word": self.original_word,
            "from_language": self.from_language.name,
            "translated_text": self.translated_text,
            "to_language": self.to_language.name,
            "updated": updated,
        }
        text_content = render_to_string("email/translation_email.txt", context)
        html_content = render_to_string("email/translation_email.html", context)

        self.created_by.email_user(
            subject=_("Your translation has been saved!"),
            message=text_content,
            html_message=html_content,
        )


class TranslationCard(models.Model):
    """
    Class representing a translation card
    """

    creator = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name='Created By'
    )
    from_language = models.ForeignKey(
        "core.Language",
        on_delete=models.CASCADE,
        verbose_name='From Language',
        help_text='The language from which the text is translated.',
        related_name='translationcards_from'
    )
    to_language = models.ForeignKey(
        "core.Language",
        on_delete=models.CASCADE,
        verbose_name='From Language',
        help_text='The language to which the text is translated.',
        related_name='translationcards_to'
    )
    original_text = models.TextField(
        _('Original Text')
    )
    translated_text = models.TextField(
        _('Translated Text')
    )

    class Meta:
        verbose_name = _("TranslationCard")
        verbose_name_plural = _("TranslationCards")
