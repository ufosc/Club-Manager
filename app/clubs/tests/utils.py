from datetime import datetime, timedelta
import uuid

from django.urls import reverse
from django.utils import timezone

from clubs.models import Club, Event, Team

CLUB_CREATE_PARAMS = {
    "name": "Test Club",
}
CLUB_UPDATE_PARAMS = {"name": "Updated Club"}


def create_test_club(name=None, **kwargs):
    """Create unique club for unit tests."""
    if name is None:
        name = f"Test Club {uuid.uuid4()}"

    return Club.objects.create(name=name, **kwargs)


def create_test_event(
    club: Club,
    name: str = "Test event",
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    **kwargs,
):
    """Create valid event for unit tests."""
    event_start = (
        start_datetime if start_datetime else timezone.now() - timedelta(days=1)
    )
    event_end = end_datetime if end_datetime else timezone.now() + timedelta(days=1)
    location = kwargs.pop("location", "CSE A101")
    description = kwargs.pop("description", "Lorem ipsum dolor sit amet")

    return Event.objects.create(
        name=name,
        club=club,
        start_at=event_start,
        end_at=event_end,
        location=location,
        description=description,
        **kwargs,
    )


def create_test_team(club: Club, **kwargs):
    """Create valid team for unit tests."""

    payload = {"name": kwargs.pop("name", f"Team {uuid.uuid4()}"), **kwargs}

    return Team.objects.create(club=club, **payload)


def join_club_url(club_id: int):
    return reverse("clubs:join", kwargs={"club_id": club_id})


def club_home_url(club_id: int):
    return reverse("clubs:home", kwargs={"club_id": club_id})
