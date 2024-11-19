from django.core.mail.backends.base import BaseEmailBackend


class CustomEmailBackend(BaseEmailBackend):
    """
    Wraps default django backend.
    """

    pass
