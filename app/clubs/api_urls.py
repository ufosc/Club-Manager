from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register("clubs", viewsets.ClubViewSet, basename="club")

app_name = "api-clubs"

urlpatterns = [path("", include(router.urls))]
