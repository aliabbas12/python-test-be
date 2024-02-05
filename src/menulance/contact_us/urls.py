from django.urls import path, include
from rest_framework import routers
from contact_us import views

app_name = "contact_us"

router = routers.DefaultRouter()
router.register(r"contact-form", views.ContactFormEntryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
