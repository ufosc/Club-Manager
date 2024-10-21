from django.urls import path
from . import views

app_name = "clubs"

urlpatterns = [
    path("join/", views.join_clubs_view, name="join"),
]
