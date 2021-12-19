from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class BaseAdmin(
    admin.ModelAdmin,
):
    """Base admin representation."""
    save_on_top = True
    list_per_page = 25
    # Fields that should be enabled only on creation
    create_only_fields = tuple()

    def get_fieldsets(self, request, obj=None):
        """Add created and modified to fieldsets."""
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets += (
            (_("Extra info"), {
                "fields": [
                    "created",
                    "modified",
                ],
            }),
        )
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        """Add created and modified to readonly_fields.

        Also if create_only_fields were specified add them to readonly_fields,
        if user is working on already created object.

        """
        readonly_fields = super().get_readonly_fields(
            request,
            obj,
        )
        readonly_fields = readonly_fields + (
            "created",
            "modified",
        )
        if not self.create_only_fields or not obj:
            return readonly_fields

        return readonly_fields + self.create_only_fields


class ReadOnlyMixin:
    """Forbid editing for admin panel or inline."""

    def has_add_permission(self, request, *args, **kwargs):
        """Disable creation."""
        return False

    def has_change_permission(self, request, *args, **kwargs):
        """Disable editing."""
        return False

    def has_delete_permission(self, request, *args, **kwargs):
        """Disable deletion."""
        return False


class ReadOnlyAdmin(ReadOnlyMixin, BaseAdmin):
    """Base admin read only representation."""


class ReadOnlyInline(ReadOnlyMixin, admin.TabularInline):
    """Read only inline."""
