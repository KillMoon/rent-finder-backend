from django.urls import include, path

app_name = "api"


urlpatterns = [
    # API URLS
    path("users/", include("apps.users.api.urls")),
    path("auth/", include("apps.users.api.auth.urls")),
]
