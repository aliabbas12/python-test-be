from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import permissions, status, exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from core.models import Font, Language, ManuallyTranslatedWord
from accounts.permissions import (IsSuperUser,
                                  AllowAny,
                                  IsAuthenticatedUser,
                                  IsAuthenticatedUserTheObjectCreator)
from core.serializers import (FontSerializer,
                              LanguageSerializer,
                              ManuallyTranslatedWordSerializer)

# Create your views here.


class FontViewSet(ModelViewSet):
    queryset = Font.objects.all()
    serializer_class = FontSerializer
    permission_classes = [IsSuperUser]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsSuperUser]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ManuallyTranslatedWordViewSet(ModelViewSet):
    queryset = ManuallyTranslatedWord.objects.all()
    serializer_class = ManuallyTranslatedWordSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ("create", "update"):
            self.permission_classes = [AllowAny]
        return super().get_permissions()