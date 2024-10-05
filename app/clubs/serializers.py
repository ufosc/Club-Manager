from rest_framework import serializers

from clubs.models import Club


class ClubSerializer(serializers.ModelSerializer):
    """Convert club model to JSON fields."""

    class Meta:
        model = Club
        fields = "__all__"
