from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from . import mixins as core_mixins


class BaseViewSet(
    core_mixins.ActionPermissionsMixin,
    core_mixins.ActionSerializerMixin,
    GenericViewSet,
):
    """Base viewset for api."""
    base_permission_classes = (IsAuthenticated,)

    def get_viewset_permissions(self):
        """Custom method to prepare viewset permissions

        Method returns union of `base_permission_classes` and
        `permission_classes`, specified in child classes.

        """
        extra_permissions = tuple(
            permission for permission in self.permission_classes
            if permission not in self.base_permission_classes
        )
        permissions = self.base_permission_classes + extra_permissions
        return [permission() for permission in permissions]


class CRUDViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """CRUD viewset for api views."""


class ReadOnlyViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    BaseViewSet,
):
    """Read only viewset for api views."""
