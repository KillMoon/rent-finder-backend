from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny

from ...core.api.views import ReadOnlyViewSet
from . import serializers

User = get_user_model()


class UsersViewSet(ReadOnlyViewSet):
    """ViewSet for viewing accounts."""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    base_permission_classes = (AllowAny,)
