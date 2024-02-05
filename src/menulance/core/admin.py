from django.contrib import admin
from core.models import Font, Language, ManuallyTranslatedWord

# Register your models here.


@admin.register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display=("name",)
    search_fields=("name",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display=("name", "short_code")
    search_fields=("name", "short_code")


@admin.register(ManuallyTranslatedWord)
class ManuallyTranslatedWord(admin.ModelAdmin):
    list_display = ("original_word", "from_language", "translated_text", "to_language", "_creator_email")
    search_fields = ("original_word", "_creator_email")