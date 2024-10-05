from rest_framework import authentication, permissions
from rest_framework.viewsets import ModelViewSet

from clubs.models import Club
from clubs.serializers import ClubSerializer


class ClubViewSet(ModelViewSet):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
