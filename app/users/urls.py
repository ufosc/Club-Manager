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

apipatterns = [
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path(
        "users/",
        include(
            [
                path("create/", views.CreateUserView.as_view(), name="create"),
            ]
        ),
    ),
]
