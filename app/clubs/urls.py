from django.urls import path
from . import views

app_name = "clubs"

urlpatterns = [path("register/", views.register_user, name="register")]
