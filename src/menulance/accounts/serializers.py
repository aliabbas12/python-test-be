from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.jwt_token_claims import JwtClaims
from accounts.models import User, UserPreferences


class TokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token[JwtClaims.EMAIL.value] = user.email
        token[JwtClaims.IS_SUPERUSER.value] = user.is_superuser

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "last_login",
            "created_at",
            "date_email_verified",
            "is_superuser",
        ]
        read_only_fields = [
            "id",
            "email",
            "last_login",
            "created_at",
            "date_email_verified",
            "is_superuser",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        source="password",
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data: dict):
        validated_data.pop("password2")
        return self.Meta.model.objects.create_user(**validated_data)


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = [
            "id",
            "creator",
            "font",
            "font_size",
            "ui_language",
            "enable_wizard",
            "enable_pro_tips",
            "enable_autodetect",
            "enable_soundfx",
            "enable_notifications"
        ]
        read_only_fields = [
            "id",
            "creator"
        ]
