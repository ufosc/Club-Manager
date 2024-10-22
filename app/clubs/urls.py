from django.urls import path
from . import views

app_name = "clubs"

urlpatterns = [
    path("available/", views.available_clubs_view, name="available"),
    path("club/<int:club_id>/", views.club_home_view, name="home"),
    path("club/<int:club_id>/join/", views.join_club_view, name="join"),
]
