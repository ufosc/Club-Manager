from django import forms
from django.contrib.auth.forms import AuthenticationForm

from clubs.models import Club, Event


class AuthForm(forms.Form):
    """Base fields for all auth forms."""

    password = forms.CharField(widget=forms.PasswordInput())
    # event = forms.ModelChoiceField(
    #     widget=forms.HiddenInput(), queryset=Event.objects.all(), required=False
    # )
    # club = forms.ModelChoiceField(
    #     widget=forms.HiddenInput(), queryset=Club.objects.all(), required=False
    # )


class LoginForm(AuthForm):
    """Allow members to authenticate with the club system."""

    username = forms.CharField(help_text="Username or Email")

    field_order = ["username", "password", "event", "club"]


class RegisterForm(AuthForm):
    """New members can create accounts with the system."""

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    confirm_password = forms.CharField(widget=forms.PasswordInput())

    field_order = ["first_name", "last_name", "email", "password", "confirm_password"]
