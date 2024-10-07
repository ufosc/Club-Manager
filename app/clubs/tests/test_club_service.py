"""
Unit tests for Club business logic.
"""

from clubs.services import ClubService
from clubs.tests.utils import (
    CLUB_CREATE_PARAMS,
    CLUB_UPDATE_PARAMS,
    ModelServiceTestsMixin,
)
from core.abstracts.tests import TestsBase


class ClubServiceTests(TestsBase, ModelServiceTestsMixin):
    """Test club services methods."""

    service = ClubService
    create_params = CLUB_CREATE_PARAMS
    update_params = CLUB_UPDATE_PARAMS
