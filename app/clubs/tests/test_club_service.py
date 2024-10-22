"""
Unit tests for Club business logic.
"""

import unittest

from clubs.models import Club
from clubs.services import ClubService
from clubs.tests.utils import (
    CLUB_CREATE_PARAMS,
    CLUB_UPDATE_PARAMS,
    ModelServiceTestsMixin,
    create_test_club,
    join_club_url,
)
from core.abstracts.tests import TestsBase


@unittest.skip("Not implemented yet")
class ClubServiceModelTests(TestsBase, ModelServiceTestsMixin):
    """Test club services methods."""

    service = ClubService
    create_params = CLUB_CREATE_PARAMS
    update_params = CLUB_UPDATE_PARAMS


class ClubServiceLogicTests(TestsBase):
    """Test club business logic not covered in views."""

    service = ClubService
    model = Club

    def test_join_link(self):
        """Join link should be correct."""
        club = create_test_club()
        link = ClubService(club).join_link

        self.assertEqual(link, join_club_url(club.id))
