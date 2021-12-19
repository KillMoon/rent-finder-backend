# Rest framework API configuration
from datetime import timedelta

from libs.utils import get_latest_version

# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = dict(
    DEFAULT_AUTHENTICATION_CLASSES=(
        "knox.auth.TokenAuthentication",
        # SessionAuthentication is also used for CSRF
        # validation on ajax calls from the frontend
        "rest_framework.authentication.SessionAuthentication",
    ),
    DEFAULT_PERMISSION_CLASSES=(
        "rest_framework.permissions.AllowAny",
    ),
    DEFAULT_SCHEMA_CLASS="drf_spectacular.openapi.AutoSchema",
    DEFAULT_FILTER_BACKENDS=(
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    DEFAULT_PAGINATION_CLASS="rest_framework.pagination.LimitOffsetPagination",
    EXCEPTION_HANDLER="libs.api.exceptions.custom_exception_handler_simple",
    TEST_REQUEST_DEFAULT_FORMAT="json",
)

# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = dict(
    TITLE="rent-checker Api",
    DESCRIPTION="Api for rent-checker",
    VERSION=get_latest_version("CHANGELOG.md"),
)

# https://james1345.github.io/django-rest-knox/settings/
REST_KNOX = dict(
    SECURE_HASH_ALGORITHM="cryptography.hazmat.primitives.hashes.SHA512",
    AUTH_TOKEN_CHARACTER_LENGTH=64,
    TOKEN_TTL=timedelta(weeks=2),
    TOKEN_LIMIT_PER_USER=None,
    AUTO_REFRESH=False,
    USER_SERIALIZER="apps.users.api.serializers.UserSerializer",
)
