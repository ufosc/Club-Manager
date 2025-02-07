"""
Unit tests for generic model functions, validation, etc.
"""

from django.urls import reverse
from analytics.models import Link
from clubs.models import Club, Event
from clubs.tests.utils import CLUB_CREATE_PARAMS, CLUB_UPDATE_PARAMS, create_test_club
from core.abstracts.tests import TestsBase
from utils.helpers import get_full_url


class BaseModelTests(TestsBase):
    """Base tests for django models."""

    model = Club
    create_params = CLUB_CREATE_PARAMS
    update_params = CLUB_UPDATE_PARAMS

    def test_create_model(self):
        """Should create model."""
        obj = self.model.objects.create(**self.create_params)
        self.assertIsNotNone(obj.created_at)

        for key, expected_value in self.create_params.items():
            actual_value = getattr(obj, key)

            self.assertEqual(actual_value, expected_value)

    def test_update_model(self):
        """Should update model."""

        obj = self.model.objects.create(**self.create_params)

        for key, expected_value in self.update_params.items():
            actual_value = getattr(obj, key)
            self.assertNotEqual(actual_value, expected_value)

            setattr(obj, key, expected_value)
            obj.save()

            actual_value = getattr(obj, key)
            self.assertEqual(actual_value, expected_value)

    def test_delete_model(self):
        """Should delete model."""

        obj = self.model.objects.create(**self.create_params)

        obj_count = self.model.objects.all().count()
        self.assertEqual(obj_count, 1)

        self.model.objects.filter(id=obj.id).delete()

        obj_count = self.model.objects.all().count()
        self.assertEqual(obj_count, 0)


class ClubEventTests(TestsBase):
    """Unit tests for club events."""

    def test_create_event_link(self):
        """Creating an event should createa new event attendance link."""

        self.assertEqual(Link.objects.count(), 0)

        club = create_test_club()
        event = Event.objects.create(club=club, name="Test Event")

        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(event.attendance_links.count(), 1)
        link = event.attendance_links.first()

        expected_url_path = reverse(
            "clubs:join-event", kwargs={"club_id": event.club.id, "event_id": event.id}
        )
        expected_url = get_full_url(expected_url_path)
        self.assertEqual(link.target_url, expected_url)
        self.assertEqual(link.reference, "Default")
