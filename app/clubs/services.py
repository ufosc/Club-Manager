from clubs.models import Club, Event
from core.abstracts.services import ModelService
from users.models import User


class ClubService(ModelService):
    """Manage club objects, business logic."""

    model = Club
    club: Club

    def __init__(self, club: Club) -> None:
        self.club = club

        super().__init__()

    @classmethod
    def create(cls, name: str, logo=None, **kwargs):
        """Create Club model."""
        return super().create(name=name, logo=logo, **kwargs)

    def get_registration_link(self):
        """Get link for a new user to create account and register."""
        pass

    def register_member(self, user: User):
        """Create membership for pre-existing user."""
        pass

    def increase_member_tokens(self, user: User, amount: int = 1):
        """Give the user more tokens."""
        pass

    def decrease_member_tokens(self, user: User, amount: int = 1):
        """Remove tokens from the user."""
        pass

    def record_member_attendance(self, user: User, event: Event):
        """Record user's attendance for event."""
        pass

    def create_event(self):
        """Create new club event."""
        pass

    def create_recurring_event(self):
        """Create new recurring club event."""
        pass



