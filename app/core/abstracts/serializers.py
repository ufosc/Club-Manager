from rest_framework import serializers


class ModelSerializerBase(serializers.ModelSerializer):
    """Default functionality for model serializer."""

    datetime_format = "%Y-%m-%d %H:%M:%S"

    id = serializers.IntegerField(label="ID", read_only=True)
    created_at = serializers.DateTimeField(
        format=datetime_format, read_only=True, required=False, allow_null=True
    )
    updated_at = serializers.DateTimeField(
        format=datetime_format, read_only=True, required=False, allow_null=True
    )

    default_fields = ["id", "created_at", "updated_at"]


class ModelSerializer(ModelSerializerBase):
    """Base fields for model serializer."""

    class Meta:
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class StringListField(serializers.CharField):
    """Represent a comma-separated string as a list of strings."""

    def to_representation(self, value: str):
        """Convert to list for json."""

        return value.split(",")

    def to_internal_value(self, data):
        """Convert to string for database."""

        if isinstance(data, list):
            return ",".join(data)

        return data
