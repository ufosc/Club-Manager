"""
User Models.
"""

import os
from typing import Optional
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from core.abstracts.models import BaseModel


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

    username = models.CharField(max_length=64, unique=True)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    date_modified = models.DateTimeField(auto_now=True, editable=False, blank=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    # Relationships
    profile: Optional["Profile"]
    club_memberships: models.QuerySet

    @property
    def name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    def __str__(self):
        return self.name if self.name.strip() != "" else self.email


class Profile(BaseModel):
    """User information."""

    user = models.OneToOneField(
        User, primary_key=True, related_name="profile", on_delete=models.CASCADE
    )

    email = models.EmailField(max_length=128, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    address_1 = models.CharField(max_length=255, null=True, blank=True)
    address_2 = models.CharField(max_length=255, null=True, blank=True)

    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    birthday = models.DateField(null=True, blank=True)

    image = models.ImageField(
        upload_to=profile_image_file_path,
        default="user/profile.jpeg",
        blank=True,
    )

    class Meta:
        _is_unique_nonempty_phone = models.Q(
            models.Q(phone__isnull=False) & ~models.Q(phone__exact="")
        )

        # Ensure non-empty phone fields are unique
        constraints = [
            models.UniqueConstraint(
                fields=("phone",),
                condition=_is_unique_nonempty_phone,
                name="Unique non-null phone number for each profile",
            )
        ]

        # Allow non-empty phone fields to be easily searchable
        indexes = [
            models.Index(
                fields=("phone",), name="phone_idx", condition=_is_unique_nonempty_phone
            )
        ]