from clubs.models import ClubMembership, ClubRole
from clubs.serializers import ClubMembershipCsvSerializer
from clubs.tests.utils import create_test_club
from lib.faker import fake
from querycsv.tests.utils import UploadCsvTestsBase
from users.models import User


class ClubMembershipCsvUploadTests(UploadCsvTestsBase):
    """Test upload csv functionality for club memberships."""

    model_class = ClubMembership
    serializer_class = ClubMembershipCsvSerializer

    def setUp(self):
        self.club = create_test_club()
        self.club2 = create_test_club()
        # self.user = create_test_user()
        return super().setUp()

    def get_create_params(self, **kwargs):
        return {"club": self.club, "user": self.user, **kwargs}

    def test_create_club_memberships(self):
        """Should create club memberships from a csv."""

        # Initialize data
        payload = [
            {
                "club": self.club.id,
                "user_email": fake.safe_email(),
                "roles": ["Member", "New Role"],
            }
            for _ in range(self.dataset_size)
        ]
        self.data_to_csv(payload)

        # Call service
        _, failed = self.service.upload_csv(path=self.filepath)

        # Validate database,
        # Memberships are non-standard schemas so we do manual testing
        memberships = self.repo.all()
        self.assertEqual(memberships.count(), self.dataset_size, failed)

        for expected in payload:
            self.assertTrue(User.objects.filter(email=expected["user_email"]).exists())

            for role in expected["roles"]:
                self.assertTrue(
                    ClubRole.objects.filter(name=role, club=self.club).exists()
                )

            self.assertTrue(
                self.repo.filter(
                    club=expected["club"], user__email=expected["user_email"]
                ).exists()
            )
