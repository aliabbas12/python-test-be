from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from utils.orm.model_mixins import CreatedAtUpdatedAtModelMixin


class Font(CreatedAtUpdatedAtModelMixin):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name = "Font"
        verbose_name_plural = "Fonts"

    def __str__(self):
        return self.name


class Language(CreatedAtUpdatedAtModelMixin):
    name = models.CharField(max_length=64)
    short_code = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.short_code


class ManuallyTranslatedWord(CreatedAtUpdatedAtModelMixin):
    original_word = models.CharField(max_length=255)
    from_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="manual_translations_from"
    )
    translated_text = models.CharField(max_length=255)
    to_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="manual_translations_to"
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            "original_word",
            "from_language",
            "to_language",
            "creator",
        ]
        verbose_name = "ManuallyTranslatedWord"
        verbose_name_plural = "ManuallyTranslatedWord"

    @property
    def _creator_email(self):
        return self.creator.email

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

        self.creator.email_user(
            subject=_("Your translation has been saved!"),
            message=text_content,
            html_message=html_content,
        )
