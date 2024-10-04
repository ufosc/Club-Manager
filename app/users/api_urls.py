"""
URL Patterns for users REST API.
"""

from django.urls import include, path
from users import views

app_name = "api-users"

urlpatterns = [
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
