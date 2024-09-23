from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.health_check, name="index"),
    path("health/", views.health_check, name="health"),
]
