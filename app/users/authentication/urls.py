from django.urls import path

from . import views

app_name = "users-auth"

urlpatterns = [
    path(
        "login/",
        views.AuthLoginView.as_view(),
        name="login",
    ),
    path("logout/", views.AuthLogoutView.as_view(), name="logout"),
    path("reset-password/", views.AuthPassResetView.as_view(), name="reset-password"),
    path(
        "reset-password/done/",
        views.AuthPassResetDoneView.as_view(),
        name="reset-password-done",
    ),
    path(
        "reset-password/complete/",
        views.AuthPassResetCompleteView.as_view(),
        name="reset-password-complete",
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        views.AuthPassResetConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "change-password/",
        views.AuthChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "change-password/done/",
        views.AuthPasswordChangeDoneView.as_view(),
        name="change-password-done",
    ),
]
