"""
URL mappings for the user API.
"""

from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.register_user_view, name="register"),
    # path("login/", views.login_user_view, name="login"),
    # path("resetpassword/", views.reset_password, name="reset_password"),
    # path("logout/", views.logout_user_view, name="logout"),
    path("me/", views.user_profile_view, name="profile"),
    path("me/points/", views.user_points_view, name="points"),
]
