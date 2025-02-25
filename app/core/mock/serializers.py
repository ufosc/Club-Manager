from core.mock.models import Buster, BusterTag
from querycsv.serializers import CsvModelSerializer, WritableSlugRelatedField


class BusterCsvSerializer(CsvModelSerializer):
    """Serialize dummy model for testing."""

    many_tags_int = WritableSlugRelatedField(
        source="many_tags",
        slug_field="id",
        queryset=BusterTag.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )
    many_tags = WritableSlugRelatedField(
        slug_field="name",
        queryset=BusterTag.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )
    one_tag = WritableSlugRelatedField(
        slug_field="name",
        required=False,
        queryset=BusterTag.objects.all(),
        allow_null=True,
    )

    class Meta(CsvModelSerializer.Meta):
        model = Buster
        fields = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "unique_name",
            "one_tag",
            "many_tags",
            "many_tags_int",
        ]
        exclude = None
