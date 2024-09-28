"""
Club models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.abstracts.models import BaseModel, UniqueModel
from users.models import User
from utils.models import UploadFilepathFactory


# TODO: Implement RBAC, custom roles
# Ref: https://medium.com/@subhamx/role-based-access-control-in-django-the-right-features-to-the-right-users-9e93feb8a3b1
class ClubRoles(models.TextChoices):
    PRESIDENT = "president", _("President")
    OFFICER = "officer", _("Officer")
    MEMBER = "member", _("Member")


class Club(UniqueModel):
    """Group of users."""

    get_logo_filepath = UploadFilepathFactory("clubs/logos/")

    name = models.CharField(max_length=64, unique=True)
    logo = models.ImageField(upload_to=get_logo_filepath, blank=True, null=True)

    # Relationships
    memberships: models.QuerySet["ClubMembership"]

    def __str__(self):
        return self.name


class ClubMembership(BaseModel):
    """Connection between user and club."""

    club = models.ForeignKey(Club, related_name="memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="club_memberships", on_delete=models.CASCADE
    )
    role = models.CharField(
        choices=ClubRoles.choices, default=ClubRoles.MEMBER, blank=True
    )
    owner = models.BooleanField(default=False, blank=True)

    class Meta:
        # TODO: Edgecase - owner's user is deleted, deleting membership
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "club",
                    "owner",
                ),
                condition=models.Q(owner=True),
                name="Only one club owner per club.",
            )
        ]
