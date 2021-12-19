from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("config.urls.api", namespace="v1")),
]

# Add open_api urls only to not production envs
if settings.ENVIRONMENT != 'prod':
    urlpatterns.append(path(
        "api/v1/open-api/", include("config.urls.open_api"),
    ))
