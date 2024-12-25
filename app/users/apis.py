"""
URL Patterns for users REST API.
"""

from django.urls import include, path

from users import viewsets

app_name = "api-users"

urlpatterns = [
    path("token/", viewsets.CreateTokenView.as_view(), name="token"),
    path("me/", viewsets.ManageUserView.as_view(), name="me"),
    path(
        "users/",
        include(
            [
                path("create/", viewsets.CreateUserView.as_view(), name="create"),
            ]
        ),
    ),
]
