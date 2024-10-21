"""
HTML views.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.http import HttpRequest
from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.urls import reverse

from users.forms import LoginForm, RegisterForm
from users.services import UserService


def register_user_view(request: HttpRequest):
    """Add new user to the system."""
    form = RegisterForm()
    context = {}

    if request.POST:
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            data = form.cleaned_data
            form_data = {
                "first_name": data.get("first_name", None),
                "last_name": data.get("last_name", None),
                "email": data.get("email", None),
                "password": data.get("password", None),
            }

            confirmed_password = data.get("confirm_password", None)

            if confirmed_password != form_data["password"]:
                raise ValidationError("Passwords do not match.")

            user = UserService.register_user(**form_data)
            UserService.login_user(request, user)

            return redirect("clubs:join")

    context["form"] = form
    return render(request, "users/register-user.html", context)


def login_user_view(request: HttpRequest):
    """Authenticate user's credentials, create user session."""
    form = LoginForm()
    context = {}

    if request.POST:
        form = LoginForm(data=request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get("username", None)
            password = data.get("password", None)

            user = UserService.authenticate_user(
                request, username_or_email=username, password=password
            )
            UserService.login_user(request, user)

            return redirect("users:profile")

    context["form"] = form
    return render(request, "users/login-user.html", context)


@login_required()
def logout_user_view(request: HttpRequest):
    """Clear session of current user."""
    return logout_then_login(request, reverse("users:login"))


@login_required()
def user_profile_view(request: HttpRequest):
    """Display user's profile."""
    return render(request, "users/profile.html", context={})


@login_required()
def user_points_view(request: HttpRequest):
    """Summary showing the user's points."""
    return render(request, "users/points.html", context={})
