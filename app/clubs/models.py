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


class DayChoices(models.TextChoices):
    MONDAY = "M", _("Monday")
    TUESDAY = "T", _("Tuesday")
    WEDNESDAY = "W", _("Wednesday")
    THURSDAY = "R", _("Thursday")
    FRIDAY = "F", _("Friday")
    SATURDAY = "SA", _("Saturday")
    SUNDAY = "SU", _("Sunday")


class Club(UniqueModel):
    """Group of users."""

    get_logo_filepath = UploadFilepathFactory("clubs/logos/")

    name = models.CharField(max_length=64, unique=True)
    logo = models.ImageField(upload_to=get_logo_filepath, blank=True, null=True)

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
    owner = models.BooleanField(default=False, blank=True)

    # TODO: Should this be split to own model? Keep history of point changes?
    points = models.IntegerField(default=0, blank=True)

    class Meta:
        # TODO: Edgecase - owner's user is deleted, deleting membership
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "club",
                    "owner",
                ),
                condition=models.Q(owner=True),
                # name="Only one club owner per club.",
                name="only_one_owner_per_club",
            )
        ]


class EventFields(BaseModel):
    """Common fields for club event models."""

    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    location = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        abstract = True


class RecurringEvent(EventFields):
    """Template for recurring events."""

    day = models.CharField(choices=DayChoices.choices, max_length=2)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    start_date = models.DateField(help_text="Date of the first occurance of this event")
    end_date = models.DateField(
        null=True, blank=True, help_text="Date of the last occurance of this event"
    )


class Event(EventFields):
    """Record future events put on by the club."""

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")

    starts = models.DateTimeField(null=True, blank=True)
    ends = models.DateTimeField(null=True, blank=True)
    recurring_event = models.ForeignKey(
        RecurringEvent, on_delete=models.CASCADE, null=True, blank=True
    )


class EventAttendance(BaseModel):
    """Records when members attend club event."""

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="member_attendance"
    )
    member = models.ForeignKey(
        ClubMembership, on_delete=models.CASCADE, related_name="event_attendance"
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=("event", "member"),
                name="record_attendance_once_per_member_per_event",
            )
        ]
