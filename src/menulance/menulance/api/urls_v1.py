from django.urls import path, include

app_name = "v1"

urlpatterns = (path("accounts/", include("accounts.urls")),)
