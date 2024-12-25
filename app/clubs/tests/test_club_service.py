"""
Unit tests for Club business logic.
"""

import datetime

from django.core import exceptions
from django.utils import timezone

from clubs.models import Club, DayChoice, Event
from clubs.services import ClubService
from clubs.tests.utils import create_test_club, join_club_url
from core.abstracts.tests import TestsBase
from lib.faker import fake
from users.tests.utils import create_test_user


class ClubServiceLogicTests(TestsBase):
    """Test club business logic not covered in views."""

    model = Club

    def setUp(self):
        self.club = create_test_club()
        self.service = ClubService(self.club)

        return super().setUp()

    def test_join_link(self):
        """Join link should be correct."""

        link = self.service.join_link
        self.assertEqual(link, join_club_url(self.club.id))

    def test_memberships(self):
        """Should manage relationships between clubs and users."""

        user = create_test_user()
        with self.assertRaises(exceptions.BadRequest):
            self.service.increase_member_points(user, 1)

        mem = self.service.add_member(user)
        self.assertEqual(self.club.memberships.count(), 1)
        self.assertEqual(mem.points, 0)

        self.service.increase_member_points(user, 1)
        mem.refresh_from_db()
        self.assertEqual(mem.points, 1)

        self.service.increase_member_points(user, 5)
        mem.refresh_from_db()
        self.assertEqual(mem.points, 6)

        self.service.decrease_member_points(user, 1)
        mem.refresh_from_db()
        self.assertEqual(mem.points, 5)

        with self.assertRaises(exceptions.BadRequest):
            self.service.decrease_member_points(user, 6)
        mem.refresh_from_db()
        self.assertEqual(mem.points, 5)


class ClubEventTests(TestsBase):
    """Unit tests for club events."""

    def setUp(self):
        self.club = create_test_club()
        self.service = ClubService(self.club)

        return super().setUp()

    def test_create_event(self):
        """Should create event."""

        # Without dates
        self.service.create_event(name=fake.title())
        self.assertEqual(Event.objects.count(), 1)

        # With dates
        event_start = timezone.now() - timezone.timedelta(hours=2)
        event_end = timezone.now()
        event = self.service.create_event(
            name=fake.title(), start_at=event_start, end_at=event_end
        )

        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(event.start_at, event_start)
        self.assertEqual(event.end_at, event_end)

    def test_create_recurring_event(self):
        """
        Recurring event should create multiple events.

        Between 9/1/24 and 12/1/24 there are 13 tuesdays.
        """
        EXPECTED_EV_COUNT = 13
        EXPECTED_DATES = [
            (9, 3),
            (9, 10),
            (9, 17),
            (9, 24),
            (10, 1),
            (10, 8),
            (10, 15),
            (10, 22),
            (10, 29),
            (11, 5),
            (11, 12),
            (11, 19),
            (11, 26),
        ]

        payload = {
            "name": fake.title(),
            "start_date": timezone.datetime(2024, 9, 1),
            "end_date": timezone.datetime(2024, 12, 1),
            "day": DayChoice.TUESDAY,
            "event_start_time": datetime.time(17, 0, 0),
            "event_end_time": datetime.time(19, 0, 0),
        }

        self.assertEqual(Event.objects.count(), 0)

        rec = self.service.create_recurring_event(**payload)
        self.assertEqual(Event.objects.count(), EXPECTED_EV_COUNT)

        for i, event in enumerate(list(Event.objects.all().order_by("start_at"))):
            self.assertEqual(event.name, rec.name)
            self.assertIsNone(event.description)

            self.assertEqual(event.start_at.weekday(), 1)
            self.assertEqual(event.start_at.hour, 17)
            self.assertEqual(event.start_at.minute, 0)

            self.assertEqual(event.end_at.weekday(), 1)
            self.assertEqual(event.end_at.hour, 19)
            self.assertEqual(event.end_at.minute, 0)

            expected_month, expected_day = EXPECTED_DATES[i]
            self.assertEqual(event.start_at.month, expected_month)
            self.assertEqual(event.start_at.day, expected_day)

        Event.objects.all().delete()
        self.assertEqual(Event.objects.count(), 0)

        self.service.sync_recurring_event(rec)
        self.assertEqual(Event.objects.count(), 13)
