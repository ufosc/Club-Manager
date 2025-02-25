from rest_framework import serializers

from clubs.models import Club, ClubMembership
from core.abstracts.serializers import ModelSerializerBase
from querycsv.serializers import CsvModelSerializer
from users.models import User


class ClubMemberNestedSerializer(serializers.ModelSerializer):
    """Represents a user's membership within a club."""

    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    owner = serializers.BooleanField(read_only=True)

    class Meta:
        model = ClubMembership
        fields = [
            *ModelSerializerBase.default_fields,
            "user_id",
            "username",
            "owner",
            # "role",
            "points",
        ]


class ClubSerializer(ModelSerializerBase):
    """Convert club model to JSON fields."""

    members = ClubMemberNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = [
            *ModelSerializerBase.default_fields,
            "name",
            "logo",
            "members",
        ]


class ClubCsvSerializer(CsvModelSerializer):
    """Represents clubs in csvs."""

    class Meta:
        model = Club
        fields = "__all__"


class ClubMembershipSerializer(ModelSerializerBase):
    """Represents a club membership to use for CRUD operations."""

    user_id = serializers.SlugRelatedField(
        slug_field="id", source="user", queryset=User.objects.all()
    )
    club_id = serializers.SlugRelatedField(
        slug_field="id", source="club", read_only=True
    )

    class Meta:
        model = ClubMembership
        fields = [
            *ModelSerializerBase.default_fields,
            "user_id",
            "club_id",
            # "role",
            "owner",
            "points",
        ]


class ClubMembershipCsvSerializer(CsvModelSerializer, ClubMembershipSerializer):
    """Serialize club memberships for a csv."""

    class Meta:
        model = ClubMembership
        fields = [
            *ModelSerializerBase.default_fields,
            "user_id",
            "club_id",
            "owner",
            "points",
        ]
