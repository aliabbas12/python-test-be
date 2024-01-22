"""
Menulance Backend URL Configuration for API endpoints
"""

from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.openapi import Contact, License
from drf_yasg.views import get_schema_view
from rest_framework import permissions

handler500 = "rest_framework.exceptions.server_error"
handler400 = "rest_framework.exceptions.bad_request"
handler404 = "menulance.api.views.not_found"
handler403 = "menulance.api.views.permission_denied"

# TODO: Content
schema_view = get_schema_view(
    openapi.Info(
        title="Menulance REST API",
        default_version="v1",
        description="TODO",
        terms_of_service="TODO",
        contact=Contact(name="TODO", url="TODO", email="TODO"),
        license=License(name="TODO", url="TODO"),
    ),
    public=False,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/v1/", include("menulance.api.urls_v1")),
]
