"""
Club models.
"""

# from datetime import datetime, timedelta
from pathlib import Path
from typing import ClassVar, Optional
from django.core.files import File
from django.utils.timezone import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.abstracts.models import ManagerBase, ModelBase, UniqueModel
from users.models import User
from utils.dates import get_day_count
from utils.formatting import format_bytes
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
        return get_day_count(self.start_date, self.end_date, self.day)

    # def sync_events(self):
    #     """
    #     Sync all events for recurring event template.

    #     Will remove all excess events outside of start/end dates,
    #     and will create events if missing on a certain day.

    #     Date filter docs:
    #     https://docs.djangoproject.com/en/dev/ref/models/querysets/#week-day
    #     """
    #     event_count = self.expected_event_count + 2  # Buffer before/after

    #     # Remove extra events
    #     # Get all dates assigned to recurring,
    #     # delete if they don't overlap with the start/end dates
    #     range_start = datetime.combine(self.start_date, self.event_start_time)
    #     range_end = datetime.combine(self.end_date, self.event_start_time)

    #     # Django filter starts at Sun=1, python starts Mon=0
    #     query_day = self.day + 2 if self.day > 0 else 6

    #     query = self.events.filter(
    #         ~models.Q(event_start__date__range=(range_start, range_end))
    #         | ~models.Q(event_start__week_day=query_day)
    #     )
    #     query.delete()

    #     # Create missing events
    #     for i in range(event_count):
    #         # Equalize date to monday (0), set to target day, set to target week (i)
    #         event_date = (
    #             (self.start_date - timedelta(days=self.start_date.weekday()))
    #             + timedelta(days=self.day)
    #             + timedelta(weeks=i)
    #         )

    #         if event_date < self.start_date or event_date > self.end_date:
    #             continue

    #         event_start = datetime.combine(
    #             event_date, self.event_start_time, tzinfo=timezone.utc
    #         )
    #         event_end = datetime.combine(
    #             event_date, self.event_end_time, tzinfo=timezone.utc
    #         )

    #         # These fields must all be unique together
    #         event, _ = Event.objects.update_or_create(
    #             name=self.name,
    #             club=self.club,
    #             event_start=event_start,
    #             event_end=event_end,
    #             recurring_event=self,
    #         )

    #         # Set other fields
    #         event.location = self.location

    #         # Only add description if not exists
    #         # Doesn't override custom description for existing events
    #         if event.description is None:
    #             event.description = self.description

    #         event.save()


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


class QRCode(ModelBase):
    """Store image for QR Codes."""

    qrcode_upload_path = UploadFilepathFactory("clubs/qrcodes/")

    image = models.ImageField(null=True, blank=True, upload_to=qrcode_upload_path)
    url = models.URLField()

    def save_image(self, filepath: str):
        """Takes path for image and sets it to the image field."""

        path = Path(filepath)

        with path.open(mode="rb") as f:
            self.image = File(f, name=f.name)
            self.save()

    # Dynamic Properties
    @property
    def width(self):
        if self.image:
            return self.image.width

    @property
    def size(self):
        # if self.image is not None and hasattr(self.image, 'size'):
        if self.image:
            return format_bytes(self.image.size)

    # Overrides
    def __str__(self) -> str:
        return self.url

    class Meta:
        verbose_name = "QR Code"


# class Badge(BaseModel):
#     """Rewards members get when criteria is met."""

#     club = models.ForeignKey(Club, related_name="badges", on_delete=models.CASCADE)

#     image = models.ImageField()
#     name = models.CharField(max_length=32)


# class PointsBadge(Badge):
#     """Marks when members reach certain points."""

#     points_required = models.IntegerField()


# class AttendanceBadge(Badge):
#     """Marks when members reach certain points."""

#     points_required = models.IntegerField()
