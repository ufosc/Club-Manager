"""
Unit tests for Club business logic.
"""

from clubs.models import Club
from clubs.services import ClubService
from clubs.tests.utils import (
    create_test_club,
    join_club_url,
)
from core.abstracts.tests import TestsBase


class ClubServiceLogicTests(TestsBase):
    """Test club business logic not covered in views."""

    service = ClubService
    model = Club

    def test_join_link(self):
        """Join link should be correct."""
        club = create_test_club()
        link = ClubService(club).join_link

        self.assertEqual(link, join_club_url(club.id))
