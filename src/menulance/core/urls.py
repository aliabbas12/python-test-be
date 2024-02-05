from django.urls import path, include
from rest_framework import routers
from core import views

app_name = "core"

router = routers.DefaultRouter()
router.register(r"fonts", views.FontViewSet)
router.register(r"languages", views.LanguageViewSet)
router.register(r"translated_words", views.ManuallyTranslatedWordViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
]
