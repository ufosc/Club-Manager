"""
Users admin config.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Profile, User


class UserProfileInline(admin.StackedInline):
    """User profile inline."""

    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    """Manager users in admin dashbaord."""

    readonly_fields = (
        *BaseUserAdmin.readonly_fields,
        "date_joined",
        "first_name",
        "last_name",
    )
    inlines = (UserProfileInline,)


admin.site.register(User, UserAdmin)
