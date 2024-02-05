from rest_framework.viewsets import ModelViewSet

from accounts.permissions import IsSuperUser, AllowAny, IsAuthenticated
from core.models import Font, Language, ManuallyTranslatedWord
from core.serializers import (
    FontSerializer,
    LanguageSerializer,
    ManuallyTranslatedWordSerializer,
)

# TODO: For Font and languages
#  - Set methods (only GET)
#   - AllowAny access to these viewsets


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
    permission_classes = [IsAuthenticated]
    # TODO: POST, PUT method limit
