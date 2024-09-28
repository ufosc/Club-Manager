"""
Club views for API and rendering html pages.
"""

from django.http import HttpRequest
from django.shortcuts import render


def register_user(request: HttpRequest):
    """When user hits the registration page."""

    return render(request, "clubs/register-user.html")
