import random
from rest_framework.authentication import get_user_model


def create_test_adminuser(**kwargs):
    """
    Create Test Admin User

    Used to create unique admin users quickly for testing, it will return
    admin user with test data.
    """
    prefix = random.randint(0, 500)
    email = f"{prefix}-admin@example.com"
    password = "testpass"

    return get_user_model().objects.create_adminuser(
        email=email, password=password, **kwargs
    )
