from rest_framework import serializers
from core.models import Font, Language, ManuallyTranslatedWord
from accounts.models import User
from django.utils import timezone

# Create your serializers here.


class FontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Font
        fields = [
            "id",
            "name"
        ]
        read_only_fields = [
            "id"
        ]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = [
            "id",
            "name",
            "short_code"
        ]
        read_only_fields = [
            "id"
        ]


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
            "created_at"
        ]
        read_only_fields = [
            "id",
            "created_at"
        ]

        def create(self, validated_data):
            instance: ManuallyTranslatedWord = ManuallyTranslatedWord.objects.create(**validated_data)
            instance.send_email_to_creator()
            print("created")
            return instance

        def update(self, instance: ManuallyTranslatedWord, validated_data):
            instance.update(**validated_data, updated_at=timezone.now())
            instance.send_email_to_creator(updated=True)
            print("updated")
            return instance