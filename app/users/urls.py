"""
URL mappings for the user API.
"""

from django.urls import include, path

from users import views


app_name = "users"

urlpatterns = [
    path("me/", views.user_profile_view, name="profile"),
    path("me/points/", views.user_points_view, name="points"),
]


