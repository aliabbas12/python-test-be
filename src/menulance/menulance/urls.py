"""
URL configuration for menulance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path

urls_conf = None
if settings.SERVICE_ID == "admin":
    from menulance.admin import urls as admin_urls_conf

    urls_conf = admin_urls_conf

elif settings.SERVICE_ID == "api":
    from menulance.api import urls as api_urls_conf

    urls_conf = api_urls_conf

urlpatterns = getattr(urls_conf, "urlpatterns", [])
handler404 = getattr(urls_conf, "handler404", None)
handler500 = getattr(urls_conf, "handler500", None)
handler403 = getattr(urls_conf, "handler403", None)
handler400 = getattr(urls_conf, "handler400", None)

if settings.LOAD_ADMIN_APP:
    urlpatterns += (path("admin/", admin.site.urls),)
