from django.contrib import admin
from django.urls import include, path

from apps.core.views import IndexView

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    # Custom checks at lib/health_checks
    path("health/", include("health_check.urls")),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
