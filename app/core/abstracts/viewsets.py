from rest_framework import authentication, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class ViewSetBase(GenericViewSet):
    """Provide core functionality for most viewsets."""

    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]


class ModelViewSetBase(ModelViewSet, GenericViewSet):
    """Base viewset for model CRUD operations."""

    pass
