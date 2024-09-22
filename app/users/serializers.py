"""
User serializers.
"""

from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "image",
            "password",
            "projects",
            "companies",
            # "uuid",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unabled to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
