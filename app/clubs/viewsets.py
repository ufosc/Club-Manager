from rest_framework import authentication, permissions
from rest_framework.viewsets import ModelViewSet

from clubs.models import Club, ClubMembership
from clubs.serializers import ClubMembershipSerializer, ClubSerializer


class ClubViewSet(ModelViewSet):
    """CRUD Api routes for Club models."""

    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ClubMembershipViewSet(ModelViewSet):
    """CRUD Api routes for ClubMembership for a specific Club."""

    serializer_class = ClubMembershipSerializer
    queryset = ClubMembership.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        club_id = self.kwargs.get("club_id", None)
        self.queryset = ClubMembership.objects.filter(club__id=club_id)

        return super().get_queryset()

    def perform_create(self, serializer: ClubMembershipSerializer):
        club_id = self.kwargs.get("club_id", None)
        club = Club.objects.get(id=club_id)

        serializer.save(club=club)
