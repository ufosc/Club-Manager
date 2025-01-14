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

    class Meta:
        read_only_fields = ["id", "created_at", "updated_at"]
