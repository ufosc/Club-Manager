"""
User Models.
"""

import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def profile_image_file_path(instance: "User", filename):
    """Generate file path for profile image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{instance.name.replace(" ", "-")}-{instance.pk}{ext}'

    return os.path.join("uploads", "user", filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save, and return a new user. Add user to base group."""
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a new superuser."""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_adminuser(self, email, password, **extra_fields):
        """Create and return a new admin user."""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)

        return user

    def create_random_password(self):
        """Create and return a random password."""
        return self.make_random_password()


class User(AbstractBaseUser, PermissionsMixin):
    """User model for system."""

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=128, unique=True)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    image = models.ImageField(
        upload_to=profile_image_file_path,
        default="users/profile.jpeg",
        blank=True,
        null=True,
    )

    date_joined = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    date_modified = models.DateTimeField(auto_now=True, editable=False, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    @property
    def name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()
        # if self.first_name and not self.last_name:
        #     return self.first_name
        # elif self.last_name and not self.first_name:
        #     return self.last_name
        # elif self.first_name and self.last_name:
        #     return f"{self.first_name} {self.last_name}"
        # else:
        #     return ""

    def __str__(self):
        return self.name if self.name.strip() != "" else self.email
