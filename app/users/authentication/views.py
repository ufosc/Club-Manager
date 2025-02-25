from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy

from users.forms import LoginForm

from app.settings import LOGIN_URL


class AuthFormMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' input-field').strip()
        return form

class AuthLoginView(LoginView):
    """
    Wrap default login view.
    Extends FormView.
    """

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({'class': 'field-text'})
        form.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        form.fields['password'].widget.attrs.update({'class': 'field-text'})
        form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        return form

    redirect_authenticated_user = True
    # template_name = "users/authentication/login.html"
    template_name = "users/login-user.html"

    def get_context_data(self, **kwargs):
        kwargs["next"] = self.request.GET.get("next", None)
        return super().get_context_data(**kwargs)


class AuthLogoutView(LogoutView):
    """
    Wrap default logout view.
    Extends TemplateView.
    """

    next_page = LOGIN_URL

# Template for the Password Reset
class AuthFormView:
    """Default view for auth forms."""

    template_name = "users/authentication/auth-form.html"
    extra_context = {"submit_button": "Submit"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget.attrs.update({'class': 'field-text'})
        form.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        return form

# Template for the Email sent to the user requesting the password reset
class AuthPassResetView(AuthFormView, PasswordResetView):
    """
    Wrap default password reset view.
    Extends FormView.
    """

    extra_context = {"submit_button": "Reset Password"}
    success_url = reverse_lazy("users-auth:reset-password-done")
    email_template_name = "users/authentication/reset-pass-email.html"


class AuthPassResetDoneView(PasswordResetDoneView):
    """
    Wrap default password reset done view.
    Extends TemplateView.
    """

    template_name = "users/authentication/reset-pass-done.html"


class AuthPassResetConfirmView(AuthFormView, PasswordResetConfirmView):
    """
    Wrap default password reset confirm view.
    Extends FormView.
    """

    extra_context = {"submit_button": "Confirm"}
    success_url = reverse_lazy("users-auth:reset-password-complete")


class AuthPassResetCompleteView(PasswordResetCompleteView):
    """
    Wrap default password reset complete view.
    Extends TemplateView.
    """

    template_name = "users/authentication/reset-pass-complete.html"


class AuthChangePasswordView(AuthFormView, PasswordChangeView):
    """
    Wrap default change password view.
    Extends FormView.
    """

    extra_context = {"submit_button": "Change Password"}
    success_url = reverse_lazy("users-auth:change-password-done")


class AuthPasswordChangeDoneView(PasswordChangeDoneView):
    """Wrap default password change done view."""

    template_name = "users/authentication/change-pass-done.html"
