"""
Views for the user API.
"""

# access base classes/methods django uses to create objects to override them
from rest_framework import generics, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from core.abstracts.viewsets import ModelViewSetBase, ViewSetBase
from users.serializers import AuthTokenSerializer, TokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RetrieveTokenView(mixins.RetrieveModelMixin, ViewSetBase):
    """Separate view for obtaining token from session."""

    serializer_class = TokenSerializer

    def get_object(self):

        token, _ = Token.objects.get_or_create(user=self.request.user)
        return token


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = ModelViewSetBase.authentication_classes
    permission_classes = ModelViewSetBase.permission_classes

    def get_object(self):
        """Retrieve and return the authenticated user."""

        return self.request.user
