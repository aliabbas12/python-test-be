from django.urls import path, include

app_name = "v1"

# TODO: System and git info
urlpatterns = [
    path("accounts/", include("accounts.urls", "accounts")),
]
