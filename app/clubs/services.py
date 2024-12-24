from django.core import exceptions
from django.urls import reverse
from clubs.models import Club, ClubMembership, Event, EventAttendance, RecurringEvent
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

    def increase_member_coins(self, user: User, amount: int = 1):
        """Give the user more coins."""
        member = self._get_user_membership(user)
        member.points += amount

    def decrease_member_coins(self, user: User, amount: int = 1):
        """Remove coins from the user."""
        member = self._get_user_membership(user)
        if member.points < amount:
            raise exceptions.BadRequest("Not enough coins to decrease.")
        else:
            member.points -= amount

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

    def create_event(self, name, event_start, event_end, recurring_event=None):
        """Create new club event."""
        if event_start >= event_end:
            raise exceptions.BadRequest(
                "The event start time must be before the end time."
            )

        event = Event.objects.create(
            club=self.obj,
            name=name,
            event_start=event_start,
            event_end=event_end,
            recurring_event=recurring_event,
        )
        return event

    def create_recurring_event(
        self,
        name,
        start_date,
        end_date,
        day,
        event_start_time,
        event_end_time,
        location,
        description=None,
    ):
        """Create new recurring club event."""
        recurring_event = RecurringEvent.objects.create(
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

        recurring_event.sync_events()

        return recurring_event

    def get_registration_link(self):
        """Return link to sign up page."""

        base_url = reverse("clubs:register")
        return f"{base_url}?club={self.obj.name}"

    def get_attendance_link(self, event: Event):
        """Visiting this link will register a user for an event."""

        return reverse("clubs:join-event", event_id=event.id)
