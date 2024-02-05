from rest_framework.viewsets import ModelViewSet

from accounts.permissions import AllowAny, IsAuthenticated
from core.models import Font, Language, ManuallyTranslatedWord
from core.serializers import (
    FontSerializer,
    LanguageSerializer,
    ManuallyTranslatedWordSerializer,
)


class FontViewSet(ModelViewSet):
    queryset = Font.objects.all()
    serializer_class = FontSerializer
    http_method_names = ["get"]
    permission_classes = [AllowAny]


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    http_method_names = ["get"]
    permission_classes = [AllowAny]


class ManuallyTranslatedWordViewSet(ModelViewSet):
    queryset = ManuallyTranslatedWord.objects.all()
    serializer_class = ManuallyTranslatedWordSerializer
    http_method_names = ["post", "put"]
    permission_classes = [IsAuthenticated]
