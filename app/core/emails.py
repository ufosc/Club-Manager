"""
Configure email sending via SendGrid.
"""

from typing import Iterable
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from sendgrid import Mail


class CustomEmailBackend(BaseEmailBackend):
    """
    Wraps default django backend.
    """

    client: Mail

    def open(self) -> bool | None:
        """Connect to sendgrid's servers."""
        if not self.client:
            self.client = Mail(is_multiple=True)

        return super().open()

    def close(self) -> None:
        """No need to manually close sendgrid client."""
        return super().close()

    def send_messages(self, email_messages: Iterable[EmailMessage]) -> int:
        """Send email messages via Sendgrid. Django already handles message validation."""
        raise NotImplementedError("Sending emails via SendGrid is not implemented yet.")

        return super().send_messages(email_messages)
