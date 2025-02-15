from clubs.services import ClubService
from clubs.tests.utils import create_test_club
from core.abstracts.tests import TestsBase
from users.tests.utils import create_test_user


class ClubPermsTests(TestsBase):
    """Club permissions tests."""

    def setUp(self):
        self.club = create_test_club()
        self.service = ClubService(self.club)
        self.user = create_test_user()

        return super().setUp()

    # def test_clubs_view_access(self):
    #     """Club memberships should have view access."""

    #     self.assertFalse(self.user.has_perm("clubs.view_club", self.club))

    #     self.service.add_member(self.user)
    #     self.assertTrue(self.user.has_perm("clubs.view_club", self.club))
