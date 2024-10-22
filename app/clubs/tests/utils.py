from datetime import datetime, timedelta
from random import randint

from django.urls import reverse
from django.utils import timezone
from clubs.models import Club, Event
from core.abstracts.services import ModelService


CLUB_CREATE_PARAMS = {
    "name": "Test Club",
}
CLUB_UPDATE_PARAMS = {"name": "Updated Club"}


def create_test_club(name=None, **kwargs):
    """Create unique club for unit tests."""
    if name is None:
        name = f"Test Club {randint(0, 100)}"

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
        event_start=event_start,
        event_end=event_end,
        location=location,
        description=description,
        **kwargs,
    )


def join_club_url(club_id: int):
    return reverse("clubs:join", kwargs={"club_id": club_id})


def club_home_url(club_id: int):
    return reverse("clubs:home", kwargs={"club_id": club_id})


class ModelServiceTestsMixin(object):
    """Base tests for model services."""

    # service = ClubService
    # create_params = CLUB_CREATE_PARAMS
    # update_params = CLUB_UPDATE_PARAMS

    service = ModelService
    create_params = {}
    update_params = {}

    def setUp(self) -> None:
        self.model = self.service.model

        return super().setUp()

    def test_create_model(self):
        """Service should create model."""

        obj = self.service.create(**self.create_params)
        self.assertObjFields(obj, self.create_params)

    def test_find_by_id(self):
        """Service should find model by id."""
        self.assertNotImplemented()

    def test_find_one(self):
        """Service should find one model."""
        self.assertNotImplemented()

    def test_find(self):
        """Service should find models with params."""
        self.assertNotImplemented()

    def test_update_one(self):
        """Service should find and update one model."""
        self.assertNotImplemented()

    def test_update_models(self):
        """Service should update model."""
        self.assertNotImplemented()

    def test_delete_one(self):
        """Service should find one model and delete."""
        self.assertNotImplemented()

    def test_delete_models(self):
        """Service should delete models that match params."""
        self.assertNotImplemented()
