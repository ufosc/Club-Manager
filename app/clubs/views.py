"""
Club views for API and rendering html pages.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


# def register_user_view(request: HttpRequest):
#     """When user hits the registration page."""
#     form = RegisterForm()
#     context = {}

#     if request.POST:
#         form = RegisterForm(request.POST)

#         if form.is_valid():
#             data = form.cleaned_data
#             user = UserService.register_user(**data)
#             UserService.login_user(request, user)

#             return redirect("clubs:join")

#     context["form"] = form
#     return render(request, "clubs/register-user.html", context)


def handle_attendance_view(request: HttpRequest):
    """Records a club member attended an event."""
    return


@login_required()
def join_clubs_view(request: HttpRequest):
    """Display list of clubs to user for them to join."""

    return render(request, "clubs/join-clubs.html")
