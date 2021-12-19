from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
app_name = "open_api"

# OpenApi urls
urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'ui/',
        SpectacularSwaggerView.as_view(url_name='open_api:schema'),
        name='ui',
    ),
]
