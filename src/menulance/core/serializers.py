from rest_framework import serializers
from core.models import Font, Language, ManuallyTranslatedWord, TranslationCard
from rest_framework import exceptions


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
        read_only_fields = ["created_at", "created_by"]

    def create(self, validated_data):
        # TODO: requires permissions to be set to be tested
        request = self.context.get("request")
        if (
            request
            and hasattr(request, "user")
            and hasattr(request.user, "is_anonymous")
            and request.user.is_anonymous
        ):
            raise exceptions.PermissionDenied()

        validated_data["created_by"] = request.user

        instance = super().create(validated_data)
        instance.send_email_to_creator()
        return instance

    def update(self, instance: ManuallyTranslatedWord, validated_data)
        # TODO: requires permissions to be set to be tested
        request = self.context.get("request")
        if (
                request
                and hasattr(request, "user")
                and instance.created_by != request.user
        ):
            raise exceptions.PermissionDenied()

        instance = super().update(instance, validated_data)
        instance.send_email_to_creator(updated=True)
        return instance

class TranslationCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationCard
        fields = [
            "id",
            "creator",
            "from_language",
            "to_language",
            "original_text",
            "translated_text"
        ]
        read_only_fields = [
            "creator",
            "id"
        ]


class TokenizeSentenceSerializer(serializers.Serializer):
    sentence = serializers.CharField()
    language_code = serializers.IntegerField()
