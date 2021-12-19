from django.contrib.auth import get_user_model

from apps.core.api.serializers import BaseSerializer


class UserSerializer(BaseSerializer):
    """Serializer for representing `User`."""

    class Meta:
        model = get_user_model()
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
        read_only_fields = ("email", )
        extra_kwargs = {
            "email": {"required": False},
        }
