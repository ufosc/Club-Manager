import re
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import get_object_or_404

User = get_user_model()


class CustomBackend(ModelBackend):
    """Custom backend for managing permissions, etc."""

    def authenticate(self, request, username=None, **kwargs):
        # Email Regex from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", username):
            username = get_object_or_404(User, email=username)

        return super().authenticate(request, username, **kwargs)
