"""
Club models.
"""

# from datetime import datetime, timedelta
from typing import ClassVar, Optional
from django.utils import timezone
from django.utils.timezone import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.abstracts.models import ManagerBase, ModelBase, UniqueModel
from users.models import User
from utils.dates import get_day_count
from utils.models import UploadFilepathFactory


# TODO: Implement RBAC, custom roles
# Ref: https://medium.com/@subhamx/role-based-access-control-in-django-the-right-features-to-the-right-users-9e93feb8a3b1 # noqa: E501
class ClubRoles(models.TextChoices):
    PRESIDENT = "president", _("President")
    OFFICER = "officer", _("Officer")
    MEMBER = "member", _("Member")


class DayChoice(models.IntegerChoices):
    MONDAY = 0, _("Monday")
    TUESDAY = 1, _("Tuesday")
    WEDNESDAY = 2, _("Wednesday")
    THURSDAY = 3, _("Thursday")
    FRIDAY = 4, _("Friday")
    SATURDAY = 5, _("Saturday")
    SUNDAY = 6, _("Sunday")


class Club(UniqueModel):
    """Group of users."""

    get_logo_filepath = UploadFilepathFactory("clubs/logos/")

    name = models.CharField(max_length=64, unique=True)
    logo = models.ImageField(upload_to=get_logo_filepath, blank=True, null=True)

    # Relationships
    memberships: models.QuerySet["ClubMembership"]


class ClubMembership(ModelBase):
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
                name="only_one_owner_per_club",
            )
        ]


class EventFields(ModelBase):
    """Common fields for club event models."""

    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    location = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        abstract = True


class RecurringEvent(EventFields):
    """Template for recurring events."""

    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="recurring_events"
    )

    day = models.IntegerField(choices=DayChoice.choices)
    event_start_time = models.TimeField(
        null=True, blank=True, help_text="Each event will start at this time"
    )
    event_end_time = models.TimeField(
        null=True, blank=True, help_text="Each event will end at this time"
    )

    start_date = models.DateField(help_text="Date of the first occurance of this event")
    end_date = models.DateField(
        null=True, blank=True, help_text="Date of the last occurance of this event"
    )
    # TODO: add skip_dates field

    # Relationships
    events: models.QuerySet["Event"]

    # Dynamic properties & methods
    @property
    def expected_event_count(self):
        if self.end_date is None:
            end_date = timezone.now()
        else:
            end_date = self.end_date

        return get_day_count(self.start_date, end_date, self.day)


class EventManager(ManagerBase["Event"]):
    """Manage event queries."""

    def create(
        self,
        club: Club,
        name: str,
        start_at: Optional[datetime] = None,
        end_at: Optional[datetime] = None,
        **kwargs,
    ):
        return super().create(
            club=club, name=name, start_at=start_at, end_at=end_at, **kwargs
        )


class Event(EventFields):
    """
    Record future events put on by the club.

    DateTimeRange docs:
    https://docs.djangoproject.com/en/5.1/ref/contrib/postgres/fields/#datetimerangefield
    """

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")

    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    recurring_event = models.ForeignKey(
        RecurringEvent,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="events",
    )

    # Overrides
    objects: ClassVar[EventManager] = EventManager()

    def __str__(self) -> str:

        if self.start_at:
            return super().__str__() + f' ({self.start_at.strftime("%a %m/%d")})'

        return super().__str__()

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=("start_at", "end_at", "club", "name"),
                name="unique_event_name_per_timerange_per_club",
            )
        ]


class EventAttendance(ModelBase):
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
