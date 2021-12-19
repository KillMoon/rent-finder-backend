from django.utils.translation import gettext_lazy as _

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import extend_schema, extend_schema_view
from knox.views import LogoutAllView, LogoutView

from libs.open_api.extend_schema import fix_api_view_warning
from libs.open_api.serializers import DetailSerializer

from . import serializers, views


class KnoxTokenScheme(OpenApiAuthenticationExtension):
    """Scheme to describe knox auth scheme."""
    target_class = "knox.auth.TokenAuthentication"
    name = "TokenAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": _(
                "Token-based authentication with required prefix '%s'",
            ) % "Token",
        }


fix_api_view_warning(views.LoginView)
fix_api_view_warning(LogoutView)
fix_api_view_warning(LogoutAllView)

extend_schema_view(
    post=extend_schema(
        request=serializers.AuthTokenSerializer,
        responses=serializers.TokenSerializer,
    ),
)(views.LoginView)

extend_schema_view(
    post=extend_schema(
        request=serializers.PasswordResetSerializer,
        responses=DetailSerializer,
    ),
)(views.PasswordResetView)

extend_schema_view(
    post=extend_schema(
        request=serializers.PasswordResetConfirmSerializer,
        responses=DetailSerializer,
    ),
)(views.PasswordResetConfirmView)
