"""
Users admin config.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

from users.models import Profile, User


class UserProfileInline(admin.StackedInline):
    """User profile inline."""

    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


class UpdateUserForm(UserChangeForm):
    """Update user."""

    class Meta:
        fields = ("email",)


class CreateUserForm(UserCreationForm):
    """Create user."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)


class UserAdmin(BaseUserAdmin):
    """Manager users in admin dashbaord."""

    readonly_fields = (
        *BaseUserAdmin.readonly_fields,
        "date_joined",
        # "first_name",
        # "last_name",
    )

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    # exclude = ("first_name", "last_name")
    inlines = (UserProfileInline,)
    # form = UpdateUserForm
    # add_form = CreateUserForm


# admin.site.unregister(UserModel)
admin.site.register(User, UserAdmin)
