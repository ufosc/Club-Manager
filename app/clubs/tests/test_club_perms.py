from clubs.models import ClubRole
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

    def test_club_initial_roles(self):
        """When a club is created, it should contain initial roles."""

        self.assertEqual(ClubRole.objects.count(), 2)

        member_role = ClubRole.objects.find_one(role_name="Member")
        self.assertIsNotNone(member_role)
        self.assertTrue(member_role.default)

        officer_role = ClubRole.objects.find_one(role_name="Officer")
        self.assertIsNotNone(officer_role)
        self.assertFalse(officer_role.default)

    def test_clubs_view_access(self):
        """Club memberships should have view access."""

        self.assertFalse(self.user.has_perm("clubs.view_club", self.club))

        self.service.add_member(self.user)
        self.assertTrue(self.user.has_perm("clubs.view_club", self.club))
        self.assertFalse(self.user.has_perm("clubs.change_club"), self.club)

    def test_club_role_change_access(self):
        """Member should inherit change perms from club role."""

        role = self.club.roles.get(role_name="Officer")
        self.service.add_member(self.user, roles=[role])

        self.assertTrue(self.user.has_perm("clubs.change_club", self.club))
