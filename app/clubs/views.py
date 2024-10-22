"""
Club views for API and rendering html pages.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from clubs.services import ClubService
from utils.helpers import reverse_query


def join_club_view(request: HttpRequest, club_id: int):
    """Registers a new or existing user to a club."""

    if not request.user.is_authenticated:
        url = reverse_query("users:register", query={"club": club_id})
        return redirect(url)

    club_svc = ClubService(club_id)
    club_svc.add_member(request.user)

    url = reverse("clubs:home", kwargs={"club_id": club_svc.club.id})
    return redirect(url)


def club_home_view(request: HttpRequest, club_id: int):
    """Base page for a club."""

    return render(request, "clubs/club-home.html")


def handle_attendance_view(request: HttpRequest):
    """Records a club member attended an event."""
    return


@login_required()
def available_clubs_view(request: HttpRequest):
    """Display list of clubs to user for them to join."""

    return render(request, "clubs/available-clubs.html")
