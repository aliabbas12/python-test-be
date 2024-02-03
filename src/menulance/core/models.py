from django.db import models
from accounts.models import User
from utils.orm.model_mixins import CreatedAtUpdatedAtModelMixin

# Create your models here.


class Font(CreatedAtUpdatedAtModelMixin):
    name = models.CharField(max_length=32)


class Language(CreatedAtUpdatedAtModelMixin):
    name = models.CharField(max_length=18)
    short_code = models.CharField(max_length=2)


class ManuallyTranslatedWord(CreatedAtUpdatedAtModelMixin):
    original_word = models.CharField(max_length=24)
    from_language = models.ForeignKey(Language, on_delete=models.RESTRICT, related_name="translations_from")
    translated_text = models.CharField(max_length=48)
    to_language = models.ForeignKey(Language, on_delete=models.RESTRICT, related_name="translations_to")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
