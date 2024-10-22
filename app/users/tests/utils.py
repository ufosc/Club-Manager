import random
from rest_framework.authentication import get_user_model

from users.models import User
from utils.helpers import reverse_query


def create_test_adminuser(**kwargs):
    """
    Create Test Admin User

    Used to create unique admin users quickly for testing, it will return
    admin user with test data.
    """
    prefix = random.randint(0, 500)
    email = f"{prefix}-admin@example.com"
    password = "testpass"

    return User.objects.create_adminuser(
        email=email, password=password, **kwargs
    )


def create_test_user(**kwargs):
    """Create user for testing purposes."""
    prefix = random.randint(0, 500)
    email = f"{prefix}-user@example.com"
    password = "testpass"
    first_name = "John"
    last_name = "Doe"

    return User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        **kwargs,
    )


def register_user_url(club: int | None = None, event: int | None = None):
    query = {}
    if club:
        query["club"] = club
    if event:
        query["event"] = event

    return reverse_query("users:register", query)
