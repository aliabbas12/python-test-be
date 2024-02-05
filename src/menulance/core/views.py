from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from accounts.permissions import AllowAny, IsAuthenticated
from core.models import Font, Language, ManuallyTranslatedWord, TranslationCard
from core.serializers import (
    FontSerializer,
    LanguageSerializer,
    ManuallyTranslatedWordSerializer,
    TranslationCardSerializer,
    TokenizeSentenceSerializer
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

class TranslationCardViewSet(GenericViewSet):
    serializer_class = TranslationCardSerializer
    queryset = TranslationCard.objects.all()
    permission_classes = []

    def dummy_translate_api(self, text):
        return {"translated_text": [ "d" + letter + "e" for letter in text ]}

    def dummy_translate_tokens_api(self, tokens):
        return [ "d" + token + "e" for token in tokens]

    @swagger_auto_schema(
        methods=["POST"],
        request_body=TranslationCardSerializer,
        responses={200: TranslationCardSerializer}
    )
    @action(detail=False, url_path='translate', methods=["POST"])
    def translate(self, request):
        data = request.data
        data["creator"] = request.user

        # Tokenize the sentence
        tokens = data["original_text"].split(" ")

        # Send the sentence to translation API
        translated_text = self.dummy_translate_api(data["original_text"])["translated_text"]
        data["translated_text"] = translated_text

        # Send the tokens to translation API
        translated_tokens = self.dummy_translate_tokens_api(tokens)

        # Save the translation object with the creator
        serializer: TranslationCardSerializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @swagger_auto_schema(
        methods=["POST"],
        request_body=TokenizeSentenceSerializer,
        responses={200: TokenizeSentenceSerializer},
    )
    @action(detail=False, url_path='tokenize', methods=["POST"])
    def tokenize(self, request):
        data = request.data

        # Tokenize the sentence
        tokens = data["original_text"].split(" ")

        return Response("")
