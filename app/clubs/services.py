from django.core import exceptions
from django.urls import reverse
from clubs.models import Club, ClubMembership, Event, EventAttendance,RecurringEvent
from core.abstracts.services import ModelService
from users.models import User


class ClubService(ModelService):
    """Manage club objects, business logic."""

    model = Club
    club: Club

    def __init__(self, club: Club | int) -> None:
        if isinstance(club, int):
            club = Club.objects.get(id=club)

        self.club = club

        super().__init__()

    @classmethod
    def create(cls, name: str, logo=None, **kwargs):
        """Create Club model."""
        return super().create(name=name, logo=logo, **kwargs)

    def _get_user_membership(self, user: User):
        try:
            membership = ClubMembership.objects.get(club=self.club, user=user)
            return membership
        except ClubMembership.DoesNotExist:
            raise exceptions.BadRequest(f"User is not a member of {self.club}.")

    @property
    def join_link(self):
        """Get link for a new user to create account and register."""

        return reverse("clubs:join", kwargs={"club_id": self.club.id})

    def add_member(self, user: User):
        """Create membership for pre-existing user."""
        ClubMembership.objects.create(club=self.club, user=user)

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

        if event.club.id != self.club.id:
            raise exceptions.BadRequest(
                f'Event "{event}" does not belong to club {self.club}.'
            )

        return EventAttendance.objects.create(member=member, event=event)

    def get_member_attendance(self, user: User):
        """Get event attendance for user, if they are member."""

        member = self._get_user_membership(user)
        return EventAttendance.objects.filter(member=member)

    def create_event(self, name: str, **kwargs):
        event_start = 2024-11-2
        event_end = 2024-11-4

        """Create new club event."""
        if event_start >= event_end:
            raise exceptions.BadRequest("The event start time must be before the end time.")

        # Crear el evento
        event = Event.objects.create(
            club=self.club,
            name=name,
            event_start=event_start,
            event_end=event_end,
            **kwargs
        )
        return event

    def create_recurring_event(self, name, club, start_date, end_date, day, event_start_time, event_end_time, location, description=None):
        """Create new recurring club event."""
        recurring_event = RecurringEvent.objects.create(
            name=name,
            club=club,
            start_date=start_date,
            end_date=end_date,
            day=day,
            event_start_time=event_start_time,
            event_end_time=event_end_time,
            location=location,
            description=description,
        )
        
        # Sincronizar los eventos individuales según el rango de fechas
        recurring_event.sync_events()

        return recurring_event