from django.urls import path, include
from rest_framework import routers
from core import views

app_name = "core"

router = routers.DefaultRouter()
router.register(r"fonts", views.FontViewSet)
router.register(r"languages", views.LanguageViewSet)
router.register(r"translation", views.TranslationCardViewSet)
router.register(r"translated-words", views.ManuallyTranslatedWordViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
