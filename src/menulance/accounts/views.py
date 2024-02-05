# Create your views here.
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.permissions import IsSuperUser
from accounts.serializers import (
    TokenPairSerializer,
    UserSerializer,
    UserRegistrationSerializer,
)
from accounts.utils import account_confirm_token_generator
from utils.django_overrides import get_user_model


class MenulanceTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenPairSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_being_deleted=False)
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

    def get_serializer_class(self):
        if self.action == "register_user":
            return UserRegistrationSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ("register_user", "verify_email"):
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def _parse_user_from_uid_b64(self, uid_b64) -> User:
        try:
            uid = force_str(urlsafe_base64_decode(uid_b64))
        except (TypeError, ValueError, OverflowError):
            raise exceptions.ParseError()

        User = get_user_model()
        try:
            return User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise exceptions.ParseError()

    @swagger_auto_schema(
        methods=["POST"],
        request_body=UserRegistrationSerializer,
        responses={200: UserSerializer},
    )
    @action(
        detail=False,
        methods=["POST"],
        url_path="register",
        url_name="register-new",
    )
    def register_user(self, request: Request):
        request_serializer: UserRegistrationSerializer = self.get_serializer(
            data=request.data
        )

        request_serializer.is_valid(raise_exception=True)
        user = request_serializer.save()
        user.send_email_verification_email()

        return Response(UserSerializer(instance=user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["POST"],
        request_body=no_body,
        responses={200: UserSerializer},
    )
    @action(
        detail=False,
        methods=["POST"],
        url_path="verify-email/(?P<uid_b64>[0-9A-Za-z]+)/(?P<token>.+)",
        url_name="verify-email",
    )
    def verify_email(self, request: Request, uid_b64: str, token: str):
        user = self._parse_user_from_uid_b64(uid_b64)

        if (
            not account_confirm_token_generator.check_token(user, token)
            or user.date_email_verified
        ):
            raise exceptions.PermissionDenied()

        serializer = UserSerializer(instance=user, data={})

        serializer.is_valid(raise_exception=True)
        serializer.save(date_email_verified=timezone.now(), is_active=True)
        user.send_registration_completed_email()
        return Response(serializer.data, status=status.HTTP_200_OK)
