"""
Club models.
"""

# from datetime import datetime, timedelta
from typing import ClassVar, Optional

from django.core import exceptions
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

from analytics.models import Link
from core.abstracts.models import ManagerBase, ModelBase, UniqueModel
from users.models import User
from utils.dates import get_day_count
from utils.helpers import get_full_url
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
    teams: models.QuerySet["Team"]


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

    # # Foreign Relationships
    # teams: models.QuerySet["Team"]

    def __str__(self):
        return self.user.__str__()

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


class Team(ModelBase):
    """Smaller groups within clubs."""

    name = models.CharField(max_length=64)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="teams")
    points = models.IntegerField(default=0, blank=True)

    # Foreign Relationships
    memberships: models.QuerySet["TeamMembership"]

    # Overrides
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_team_per_club", fields=("club", "name")
            )
        ]


class TeamMembership(ModelBase):
    """Manage club member's assignment to a team."""

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="team_memberships"
    )

    # Overrides
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="user_single_team_membership", fields=("user", "team")
            )
        ]

    def clean(self):
        """Run model validation."""

        if not self.user.club_memberships.filter(club__id=self.team.club.id).exists():
            raise exceptions.ValidationError(
                f"User must be a member of club {self.team.club} to join team {self.team}."
            )

        return super().clean()


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
        # create_attendance_link=True,
        **kwargs,
    ):
        """Create new event, and attendance link."""

        event = super().create(
            club=club, name=name, start_at=start_at, end_at=end_at, **kwargs
        )

        # if create_attendance_link:
        #     EventAttendanceLink.objects.create(event=event, reference="Default")

        return event


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

    # Foreign Relationships
    attendance_links: models.QuerySet["EventAttendanceLink"]

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


class EventAttendanceLinkManager(ManagerBase["EventAttendanceLink"]):
    """Manage queries for event links."""

    def create(self, event: Event, reference: str, **kwargs):
        """Create event attendance link, and QRCode."""

        path = reverse(
            "clubs:join-event", kwargs={"club_id": event.club.id, "event_id": event.id}
        )
        url = get_full_url(path)
        display_name = kwargs.pop("display_name", f"Join {event} Link")

        return super().create(
            target_url=url,
            event=event,
            club=event.club,
            display_name=display_name,
            reference=reference,
            **kwargs,
        )


class EventAttendanceLink(Link):
    """
    Manage links for event attendance.

    Extends Link model via one-to-one relationship, sharing a pk.
    All fields from link are accessible on this model.
    """

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="attendance_links"
    )
    reference = models.CharField(
        null=True, blank=True, help_text="Used to differentiate between links"
    )

    # Overrides
    objects: ClassVar["EventAttendanceLinkManager"] = EventAttendanceLinkManager()

    def __str__(self):
        if self.reference:
            return f"{self.event} Link ({self.reference})"
        else:
            return f"{self.event} Link"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("event", "reference"),
                name="unique_reference_per_event_attendance_link",
            )
        ]
