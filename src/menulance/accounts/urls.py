from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from accounts import views
from accounts.views import MenulanceTokenObtainPairView

app_name = "accounts"

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("token/", MenulanceTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("", include(router.urls)),
]
