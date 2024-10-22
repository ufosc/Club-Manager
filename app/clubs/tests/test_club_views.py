from django.urls import reverse
from rest_framework import status
from clubs.models import ClubMembership
from clubs.tests.utils import club_home_url, create_test_club, join_club_url
from core.abstracts.tests import ViewsTestsBase
from users.tests.utils import create_test_user, register_user_url




class ClubViewTests(ViewsTestsBase):
    """Unit tests for club views."""

    def setUp(self):
        self.club = create_test_club()

        return super().setUp()

    def test_join_club_view_guest(self):
        """Should redirect to register page with query param."""

        url = join_club_url(self.club.id)
        redirect_url = register_user_url(club=self.club.id)
        res = self.client.get(url)

        self.assertRedirects(
            res, expected_url=redirect_url, status_code=status.HTTP_302_FOUND
        )
        self.assertEqual(ClubMembership.objects.all().count(), 0)

    def test_join_club_view_auth(self):
        """Should redirect to club home page, create membership."""

        user = create_test_user()
        self.client.force_login(user)

        url = join_club_url(self.club.id)
        redirect_url = club_home_url(self.club.id)
        res = self.client.get(url)

        self.assertRedirects(
            res, expected_url=redirect_url, status_code=status.HTTP_302_FOUND
        )
        self.assertEqual(ClubMembership.objects.all().count(), 1)
