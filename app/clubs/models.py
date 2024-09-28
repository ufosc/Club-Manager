"""
Club models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.abstracts.models import BaseModel, UniqueModel
from users.models import User


class ClubRoles(models.TextChoices):
    ADMIN = "admin", _("Admin")
    MEMBER = "member", _("Member")


class Club(UniqueModel):
    """Group of users."""

    name = models.CharField(max_length=64, unique=True)

    # Relationships
    memberships: models.QuerySet["ClubMembership"]


class ClubMembership(BaseModel):
    """Connection between user and club."""

    club = models.ForeignKey(Club, related_name="memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="club_memberships", on_delete=models.CASCADE
    )
    role = models.CharField(
        choices=ClubRoles.choices, default=ClubRoles.MEMBER, blank=True
    )
