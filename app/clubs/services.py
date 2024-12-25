from datetime import datetime, time, timedelta, timezone
from typing import Optional

from django.core import exceptions
from django.db import models
from django.urls import reverse

from clubs.models import (
    Club,
    ClubMembership,
    DayChoice,
    Event,
    EventAttendance,
    RecurringEvent,
)
from core.abstracts.services import ServiceBase
from users.models import User


class ClubService(ServiceBase[Club]):
    """Manage club objects, business logic."""

    model = Club

    def _get_user_membership(self, user: User):
        try:
            return ClubMembership.objects.get(club=self.obj, user=user)
        except ClubMembership.DoesNotExist:
            raise exceptions.BadRequest(f"User is not a member of {self.obj}.")

    @property
    def join_link(self):
        """Get link for a new user to create account and register."""

        return reverse("clubs:join", kwargs={"club_id": self.obj.id})

    def add_member(self, user: User):
        """Create membership for pre-existing user."""

        return ClubMembership.objects.create(club=self.obj, user=user)

    def increase_member_points(self, user: User, amount: int = 1):
        """Give the user more coins."""
        member = self._get_user_membership(user)
        member.points += amount
        member.save()

    def decrease_member_points(self, user: User, amount: int = 1):
        """Remove coins from the user."""
        member = self._get_user_membership(user)
        if member.points < amount:
            raise exceptions.BadRequest("Not enough coins to decrease.")
        else:
            member.points -= amount

        member.save()

    def record_member_attendance(self, user: User, event: Event):
        """Record user's attendance for event."""

        member = self._get_user_membership(user)

        if event.club.id != self.obj.id:
            raise exceptions.BadRequest(
                f'Event "{event}" does not belong to club {self.obj}.'
            )

        return EventAttendance.objects.create(member=member, event=event)

    def get_member_attendance(self, user: User):
        """Get event attendance for user, if they are member."""

        member = self._get_user_membership(user)
        return EventAttendance.objects.filter(member=member)

    def create_event(
        self,
        name: str,
        start_at: Optional[datetime] = None,
        end_at: Optional[datetime] = None,
        recurring_event=None,
    ):
        """Create new club event."""
        if start_at and end_at and (start_at >= end_at):
            raise exceptions.BadRequest(
                "The event start time must be before the end time."
            )

        event = Event.objects.create(
            club=self.obj,
            name=name,
            start_at=start_at,
            end_at=end_at,
            recurring_event=recurring_event,
        )
        return event

    def create_recurring_event(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        day: DayChoice,
        event_start_time: time,
        event_end_time: time,
        location: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """Create new recurring club event, trigger signal for syncing event."""

        return RecurringEvent.objects.create(
            name=name,
            club=self.obj,
            start_date=start_date,
            end_date=end_date,
            day=day,
            event_start_time=event_start_time,
            event_end_time=event_end_time,
            location=location,
            description=description,
        )

    def get_registration_link(self):
        """Return link to sign up page."""

        base_url = reverse("clubs:register")
        return f"{base_url}?club={self.obj.name}"

    def get_attendance_link(self, event: Event):
        """Visiting this link will register a user for an event."""

        return reverse("clubs:join-event", event_id=event.id)

    @classmethod
    def sync_recurring_event(cls, rec_ev: RecurringEvent):
        """
        Sync all events for recurring event template.

        Will remove all excess events outside of start/end dates,
        and will create events if missing on a certain day.

        Date filter docs:
        https://docs.djangoproject.com/en/dev/ref/models/querysets/#week-day
        """
        event_count = rec_ev.expected_event_count + 2  # Buffer before/after

        # Remove extra events
        # Get all dates assigned to recurring,
        # delete if they don't overlap with the start/end dates
        range_start = datetime.combine(rec_ev.start_date, rec_ev.event_start_time)
        range_end = datetime.combine(rec_ev.end_date, rec_ev.event_start_time)

        # Django filter starts at Sun=1, python starts Mon=0
        query_day = rec_ev.day + 2 if rec_ev.day > 0 else 6

        query = rec_ev.events.filter(
            ~models.Q(start_at__date__range=(range_start, range_end))
            | ~models.Q(start_at__week_day=query_day)
        )
        query.delete()

        # Create missing events
        for i in range(event_count):
            # Equalize date to monday (0), set to target day, set to target week (i)
            event_date = (
                (rec_ev.start_date - timedelta(days=rec_ev.start_date.weekday()))
                + timedelta(days=rec_ev.day)
                + timedelta(weeks=i)
            )

            if event_date < rec_ev.start_date or event_date > rec_ev.end_date:
                continue

            event_start = datetime.combine(
                event_date, rec_ev.event_start_time, tzinfo=timezone.utc
            )
            event_end = datetime.combine(
                event_date, rec_ev.event_end_time, tzinfo=timezone.utc
            )

            # These fields must all be unique together
            event, _ = Event.objects.update_or_create(
                name=rec_ev.name,
                club=rec_ev.club,
                start_at=event_start,
                end_at=event_end,
                recurring_event=rec_ev,
            )

            # Set other fields
            event.location = rec_ev.location

            # Only add description if not exists
            # Doesn't override custom description for existing events
            if event.description is None:
                event.description = rec_ev.description

            event.save()
