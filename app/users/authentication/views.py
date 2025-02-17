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

from app.settings import LOGIN_URL


class AuthLoginView(LoginView):
    """
    Wrap default login view.
    Extends FormView.
    """

    redirect_authenticated_user = True
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


class AuthFormView:
    """Default view for auth forms."""

    template_name = "users/authentication/auth-form.html"
    extra_context = {"submit_button": "Submit"}


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
