from django.db import models
from accounts.models import User
from utils.orm.model_mixins import CreatedAtUpdatedAtModelMixin
from django.template.loader import render_to_string

# Create your models here.


class Font(CreatedAtUpdatedAtModelMixin):
    name = models.CharField(max_length=32, unique=True)


class Language(CreatedAtUpdatedAtModelMixin):
    name = models.CharField(max_length=18)
    short_code = models.CharField(max_length=2, unique=True)


class ManuallyTranslatedWord(CreatedAtUpdatedAtModelMixin):
    original_word = models.CharField(max_length=24)
    from_language = models.ForeignKey(Language, on_delete=models.RESTRICT, related_name="translations_from")
    translated_text = models.CharField(max_length=48)
    to_language = models.ForeignKey(Language, on_delete=models.RESTRICT, related_name="translations_to")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["original_word", "from_language", "to_language", "created_by"]

    @property
    def _creator_email(self):
        return self.created_by.email

    def send_email_to_creator(self, updated=False):
        context = {
            "site_name": "Menulance",
            "original_word": self.original_word,
            "from_language": self.from_language,
            "translated_text": self.translated_text,
            "to_language": self.to_language,
            "updated": updated
        }
        text_content = render_to_string("email/translation_email.txt", context)
        html_content = render_to_string("email/translation_email.html", context)

        self.created_by.email_user(subject=_("Your translation has been saved!"), message=text_content, html_message=html_content)