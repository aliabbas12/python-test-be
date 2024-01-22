from django.urls import path, include

app_name = "accounts"

# Wire up our API using automatic URL routing.
urlpatterns = [path("auth/", include("dj_rest_auth.urls"))]
