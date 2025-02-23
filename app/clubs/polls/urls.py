from django.urls import path
from clubs.polls import views

app_name = "polls"

urlpatterns = [
    path("poll/<int:poll_id>/", views.show_poll_view, name="poll"),
]
