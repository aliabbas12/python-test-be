from rest_framework import serializers
from core.models import Font, Language, ManuallyTranslatedWord
from accounts.models import User
from django.utils import timezone

# Create your serializers here.


class FontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Font
        fields = ["id", "name"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name", "short_code"]


class ManuallyTranslatedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuallyTranslatedWord
        fields = [
            "id",
            "original_word",
            "from_language",
            "translated_text",
            "to_language",
            "created_by",
            "created_at",
        ]
        read_only_fields = [
            "created_at"
            #     TODO: Created_by
        ]

    def create(self, validated_data):
        instance: ManuallyTranslatedWord = ManuallyTranslatedWord.objects.create(
            **validated_data
        )
        instance.send_email_to_creator()
        return instance

    def update(self, instance: ManuallyTranslatedWord, validated_data):
        super().update(instance, validated_data)
        instance.send_email_to_creator(updated=True)
        return instance
